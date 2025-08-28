from django.urls import path
from .views import (
    ActivityListCreateView,
    ActivityDetailView,
    GoalListCreateView,
    GoalDetailView,
    activity_metrics,
    activity_history,
    leaderboard,
)

urlpatterns = [
    path('', ActivityListCreateView.as_view(), name='activity-list-create'),
    path('<int:pk>/', ActivityDetailView.as_view(), name='activity-detail'),
    path('goals/', GoalListCreateView.as_view(), name='goal-list-create'),
    path('goals/<int:pk>/', GoalDetailView.as_view(), name='goal-detail'),
    path('metrics/', activity_metrics, name='activity-metrics'),
    path('history/', activity_history, name='activity-history'),
    path('leaderboard/', leaderboard, name='leaderboard'),
]