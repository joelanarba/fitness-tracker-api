from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import Developer

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password_confirm', 
                 'first_name', 'last_name')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 
                 'date_joined', 'created_at', 'updated_at')
        read_only_fields = ('id', 'date_joined', 'created_at', 'updated_at')

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    confirm_password = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("New passwords don't match")
        return attrs

# Developer API serializers
class DeveloperRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = ('email', 'name', 'company', 'website', 'description')
    
    def validate_email(self, value):
        if Developer.objects.filter(email=value, is_active=True).exists():
            raise serializers.ValidationError("A developer account with this email already exists.")
        return value

class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = ('id', 'email', 'name', 'company', 'website', 'description', 
                 'api_key', 'is_active', 'requests_per_hour', 'requests_per_day',
                 'created_at', 'updated_at')
        read_only_fields = ('id', 'api_key', 'created_at', 'updated_at')

class DeveloperPublicSerializer(serializers.ModelSerializer):
    """Serializer for public developer info (without sensitive data)"""
    class Meta:
        model = Developer
        fields = ('id', 'name', 'company', 'website', 'created_at')

class APIKeyResponseSerializer(serializers.ModelSerializer):
    """Serializer for returning API key after registration"""
    message = serializers.CharField(read_only=True)
    
    class Meta:
        model = Developer
        fields = ('id', 'email', 'name', 'api_key', 'message', 'created_at')
        read_only_fields = ('id', 'api_key', 'created_at')