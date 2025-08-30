from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate
from .serializers import (
    UserRegistrationSerializer, 
    UserSerializer, 
    UserUpdateSerializer,
    PasswordChangeSerializer,
    DeveloperRegistrationSerializer,
    DeveloperSerializer,
    APIKeyResponseSerializer
)
from .models import Developer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate tokens for the new user
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        serializer = UserUpdateSerializer(
            self.get_object(), 
            data=request.data, 
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserSerializer(self.get_object()).data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = PasswordChangeSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        if user.check_password(serializer.validated_data['old_password']):
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'Password changed successfully'})
        else:
            return Response(
                {'error': 'Invalid old password'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    user = request.user
    user.delete()
    return Response(
        {'message': 'Account deleted successfully'}, 
        status=status.HTTP_204_NO_CONTENT
    )

# Developer API Views
class DeveloperRegisterView(generics.CreateAPIView):
    """
    Register as a developer to get API access.
    
    POST /api/developers/register/
    {
        "email": "developer@example.com",
        "name": "John Developer",
        "company": "Tech Corp",
        "website": "https://techcorp.com",
        "description": "Building a fitness app for mobile users"
    }
    """
    queryset = Developer.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = DeveloperRegistrationSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        developer = serializer.save()
        
        response_data = APIKeyResponseSerializer(developer).data
        response_data['message'] = (
            "Registration successful! Please save your API key securely. "
            "You will not be able to retrieve it again."
        )
        
        return Response(response_data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([AllowAny])
def developer_info(request):
    """
    Get information about the API and how to use it.
    """
    info = {
        "api_name": "Fitness Tracker API",
        "version": "1.0",
        "description": "A comprehensive API for tracking fitness activities, goals, and progress",
        "authentication": {
            "type": "API Key",
            "header": "Authorization",
            "format": "Api-Key YOUR_API_KEY_HERE"
        },
        "base_url": request.build_absolute_uri('/api/'),
        "endpoints": {
            "activities": "/api/activities/",
            "goals": "/api/activities/goals/",
            "metrics": "/api/activities/metrics/",
            "leaderboard": "/api/activities/leaderboard/"
        },
        "rate_limits": {
            "default": "1000 requests per hour",
            "daily": "10000 requests per day"
        },
        "support": {
            "documentation": "https://github.com/your-repo/fitness-api",
            "contact": "api-support@yourcompany.com"
        }
    }
    return Response(info)

@api_view(['POST'])
@permission_classes([AllowAny])
def regenerate_api_key(request):
    """
    Regenerate API key for a developer.
    Requires the current API key for authentication.
    """
    current_key = request.data.get('current_api_key')
    email = request.data.get('email')
    
    if not current_key or not email:
        return Response(
            {'error': 'Both current_api_key and email are required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        developer = Developer.objects.get(
            api_key=current_key, 
            email=email, 
            is_active=True
        )
        new_key = developer.regenerate_api_key()
        
        return Response({
            'message': 'API key regenerated successfully',
            'new_api_key': new_key,
            'warning': 'Your old API key has been deactivated. Update your applications immediately.'
        })
        
    except Developer.DoesNotExist:
        return Response(
            {'error': 'Invalid API key or email'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )