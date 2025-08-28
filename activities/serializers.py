from rest_framework import serializers
from .models import Activity, Goal
from django.utils import timezone
from datetime import date

class ActivitySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Activity
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')
    
    def validate_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("Activity date cannot be in the future.")
        return value
    
    def validate(self, attrs):
        # Validate that distance is provided for activities that typically have distance
        distance_activities = ['running', 'cycling', 'swimming', 'walking', 'hiking']
        if attrs.get('activity_type') in distance_activities and not attrs.get('distance'):
            attrs['distance'] = None  # Allow null but recommend distance
        return attrs

class ActivityCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('activity_type', 'duration', 'distance', 'calories_burned', 'date', 'notes')
    
    def validate_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("Activity date cannot be in the future.")
        return value

class GoalSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    progress = serializers.SerializerMethodField()
    
    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'updated_at', 'progress')
    
    def get_progress(self, obj):
        # Calculate progress based on user's activities
        from django.db.models import Sum
        from decimal import Decimal
        
        activities = Activity.objects.filter(
            user=obj.user,
            date__gte=obj.start_date,
            date__lte=obj.end_date
        )
        
        if obj.activity_type:
            activities = activities.filter(activity_type=obj.activity_type)
        
        if obj.goal_type == 'distance':
            current = activities.aggregate(
                total=Sum('distance')
            )['total'] or Decimal('0')
        elif obj.goal_type == 'duration':
            current = activities.aggregate(
                total=Sum('duration')
            )['total'] or 0
        elif obj.goal_type == 'calories':
            current = activities.aggregate(
                total=Sum('calories_burned')
            )['total'] or 0
        elif obj.goal_type == 'frequency':
            current = activities.count()
        else:
            current = 0
        
        return {
            'current': float(current) if isinstance(current, Decimal) else current,
            'target': float(obj.target_value),
            'percentage': min(100, (float(current) / float(obj.target_value)) * 100) if obj.target_value > 0 else 0
        }
    
    def validate(self, attrs):
        if attrs['start_date'] >= attrs['end_date']:
            raise serializers.ValidationError("End date must be after start date.")
        return attrs

class ActivityMetricsSerializer(serializers.Serializer):
    total_activities = serializers.IntegerField()
    total_duration = serializers.IntegerField()
    total_distance = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_calories = serializers.IntegerField()
    average_duration = serializers.DecimalField(max_digits=8, decimal_places=2)
    most_common_activity = serializers.CharField()
    activities_by_type = serializers.DictField()