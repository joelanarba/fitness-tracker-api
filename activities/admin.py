from django.contrib import admin
from .models import Activity, Goal

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'duration', 'distance', 'calories_burned', 'date')
    list_filter = ('activity_type', 'date', 'created_at')
    search_fields = ('user__username', 'activity_type', 'notes')
    date_hierarchy = 'date'
    ordering = ('-date', '-created_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'activity_type', 'date')
        }),
        ('Metrics', {
            'fields': ('duration', 'distance', 'calories_burned')
        }),
        ('Additional Info', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('user', 'goal_type', 'target_value', 'period', 'activity_type', 'is_active', 'start_date', 'end_date')
    list_filter = ('goal_type', 'period', 'activity_type', 'is_active', 'created_at')
    search_fields = ('user__username', 'goal_type', 'activity_type')
    date_hierarchy = 'start_date'
    ordering = ('-created_at',)