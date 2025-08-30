from django.urls import path
from .views import (
    RegisterView, ProfileView, change_password, delete_account,
    DeveloperRegisterView, developer_info, regenerate_api_key
)

# Default URLs (user auth)
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change-password/', change_password, name='change_password'),
    path('delete-account/', delete_account, name='delete_account'),
]


app_name = 'developers'
urlpatterns += [
    path('register/', DeveloperRegisterView.as_view(), name='register'),
    path('info/', developer_info, name='info'),
    path('regenerate-key/', regenerate_api_key, name='regenerate-key'),
]