from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.http import JsonResponse   

def home(request):   
    return JsonResponse({
        "message": "Welcome to the Fitness Tracker API",
        "available_endpoints": {
            "admin": "/admin/",
            "auth": "/api/auth/",
            "activities": "/api/activities/",
            "token": "/api/token/",
            "token_refresh": "/api/token/refresh/",
        }
    })

urlpatterns = [
    path('', home),   
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/activities/', include('activities.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
