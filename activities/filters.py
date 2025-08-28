import django_filters
from django.utils import timezone
from .models import Activity

class ActivityFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    activity_type = django_filters.CharFilter(field_name='activity_type')
    min_duration = django_filters.NumberFilter(field_name='duration', lookup_expr='gte')
    max_duration = django_filters.NumberFilter(field_name='duration', lookup_expr='lte')
    min_distance = django_filters.NumberFilter(field_name='distance', lookup_expr='gte')
    max_distance = django_filters.NumberFilter(field_name='distance', lookup_expr='lte')
    min_calories = django_filters.NumberFilter(field_name='calories_burned', lookup_expr='gte')
    max_calories = django_filters.NumberFilter(field_name='calories_burned', lookup_expr='lte')
    
    class Meta:
        model = Activity
        fields = ['activity_type']