from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.db.models import Sum, Avg, Count
from django.utils.dateparse import parse_date
from datetime import datetime, timedelta
from decimal import Decimal
from .models import Activity, Goal
from .serializers import (
    ActivitySerializer, 
    ActivityCreateSerializer, 
    GoalSerializer,
    ActivityMetricsSerializer
)
from .filters import ActivityFilter

class ActivityListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ActivityFilter
    ordering_fields = ['date', 'duration', 'calories_burned', 'distance']
    ordering = ['-date']
    
    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ActivityCreateSerializer
        return ActivitySerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ActivityDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ActivitySerializer
    
    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user)

class GoalListCreateView(generics.ListCreateAPIView):
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class GoalDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def activity_metrics(request):
    """
    Get activity metrics for the authenticated user.
    Optional query parameters:
    - start_date: YYYY-MM-DD
    - end_date: YYYY-MM-DD
    - activity_type: activity type to filter by
    """
    user = request.user
    activities = Activity.objects.filter(user=user)
    
    # Apply date filters
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    activity_type = request.query_params.get('activity_type')
    
    if start_date:
        start_date = parse_date(start_date)
        if start_date:
            activities = activities.filter(date__gte=start_date)
    
    if end_date:
        end_date = parse_date(end_date)
        if end_date:
            activities = activities.filter(date__lte=end_date)
    
    if activity_type:
        activities = activities.filter(activity_type=activity_type)
    
    # Calculate metrics
    metrics = activities.aggregate(
        total_duration=Sum('duration'),
        total_distance=Sum('distance'),
        total_calories=Sum('calories_burned'),
        average_duration=Avg('duration'),
        total_activities=Count('id')
    )
    
    # Handle None values
    for key, value in metrics.items():
        if value is None:
            if 'total' in key or key == 'total_activities':
                metrics[key] = 0
            elif 'average' in key:
                metrics[key] = Decimal('0.00')
    
    # Get most common activity
    most_common = activities.values('activity_type').annotate(
        count=Count('activity_type')
    ).order_by('-count').first()
    
    metrics['most_common_activity'] = (
        most_common['activity_type'] if most_common else 'None'
    )
    
    # Get activities by type
    activities_by_type = dict(
        activities.values('activity_type').annotate(
            count=Count('activity_type')
        ).values_list('activity_type', 'count')
    )
    
    metrics['activities_by_type'] = activities_by_type
    
    serializer = ActivityMetricsSerializer(metrics)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def activity_history(request):
    """
    Get activity history with filters, sorting, and pagination.
    This is an alias for the ActivityListCreateView but as a function-based view.
    """
    activities = Activity.objects.filter(user=request.user)
    
    # Apply filters
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    activity_type = request.query_params.get('activity_type')
    
    if start_date:
        start_date = parse_date(start_date)
        if start_date:
            activities = activities.filter(date__gte=start_date)
    
    if end_date:
        end_date = parse_date(end_date)
        if end_date:
            activities = activities.filter(date__lte=end_date)
    
    if activity_type:
        activities = activities.filter(activity_type=activity_type)
    
    # Apply sorting
    ordering = request.query_params.get('ordering', '-date')
    activities = activities.order_by(ordering)
    
    # Paginate results
    from django.core.paginator import Paginator
    page_size = int(request.query_params.get('page_size', 20))
    page = int(request.query_params.get('page', 1))
    
    paginator = Paginator(activities, page_size)
    activities_page = paginator.get_page(page)
    
    serializer = ActivitySerializer(activities_page, many=True)
    
    return Response({
        'count': paginator.count,
        'next': activities_page.has_next(),
        'previous': activities_page.has_previous(),
        'results': serializer.data
    })