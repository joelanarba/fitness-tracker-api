from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from decimal import Decimal

User = get_user_model()

class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('running', 'Running'),
        ('cycling', 'Cycling'),
        ('swimming', 'Swimming'),
        ('walking', 'Walking'),
        ('weightlifting', 'Weight Lifting'),
        ('yoga', 'Yoga'),
        ('basketball', 'Basketball'),
        ('football', 'Football'),
        ('tennis', 'Tennis'),
        ('hiking', 'Hiking'),
        ('dancing', 'Dancing'),
        ('boxing', 'Boxing'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    duration = models.PositiveIntegerField(
        help_text="Duration in minutes",
        validators=[MinValueValidator(1)]
    )
    distance = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Distance in kilometers",
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    calories_burned = models.PositiveIntegerField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(1)]
    )
    date = models.DateField()
    notes = models.TextField(blank=True, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
        db_table = 'activities'
    
    def __str__(self):
        return f"{self.user.username} - {self.get_activity_type_display()} on {self.date}"

class Goal(models.Model):
    GOAL_TYPES = [
        ('distance', 'Distance'),
        ('duration', 'Duration'),
        ('calories', 'Calories'),
        ('frequency', 'Frequency'),
    ]
    
    PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPES)
    target_value = models.DecimalField(max_digits=10, decimal_places=2)
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    activity_type = models.CharField(
        max_length=20, 
        choices=Activity.ACTIVITY_TYPES, 
        blank=True,
        help_text="Leave blank for all activities"
    )
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        db_table = 'goals'
    
    def __str__(self):
        return f"{self.user.username} - {self.goal_type} goal: {self.target_value}"