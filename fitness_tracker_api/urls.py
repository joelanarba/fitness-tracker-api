from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.http import HttpResponse

def home(request):
    html = """
    <html>
      <head>
        <title>Fitness Tracker API Playground</title>
        <style>
          body { font-family: Arial, sans-serif; padding: 2rem; }
          h1 { color: #333; }
          .endpoint { margin-bottom: 1rem; }
          a { text-decoration: none; color: white; background-color: #007bff; padding: 0.5rem 1rem; border-radius: 4px; }
          a:hover { background-color: #0056b3; }
        </style>
      </head>
      <body>
        <h1>Fitness Tracker API Playground</h1>
        <p>Click the buttons below to explore endpoints in a new tab.</p>

        <div class="endpoint"><strong>Admin:</strong> <a href="/admin/" target="_blank">Open</a></div>
        <div class="endpoint"><strong>Auth:</strong> <a href="/api/auth/" target="_blank">Open</a></div>
        <div class="endpoint"><strong>Activities:</strong> <a href="/api/activities/" target="_blank">Open</a></div>
        <div class="endpoint"><strong>Get Token:</strong> <a href="/api/token/" target="_blank">Open</a></div>
        <div class="endpoint"><strong>Refresh Token:</strong> <a href="/api/token/refresh/" target="_blank">Open</a></div>
      </body>
    </html>
    """
    return HttpResponse(html)

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/activities/', include('activities.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
