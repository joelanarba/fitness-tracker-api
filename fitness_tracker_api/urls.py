from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.http import HttpResponse

def home(request):
    html = """
    <html>
      <head>
        <title>Fitness Tracker API</title>
        <style>
          body { 
            font-family: Arial, sans-serif; 
            padding: 2rem; 
            max-width: 1200px; 
            margin: 0 auto;
            background-color: #f5f5f5;
          }
          .container {
            background: white;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
          }
          h1 { color: #333; margin-bottom: 0.5rem; }
          .subtitle { color: #666; margin-bottom: 2rem; font-size: 1.1rem; }
          .section { margin-bottom: 2rem; }
          .section h2 { color: #2c5aa0; border-bottom: 2px solid #2c5aa0; padding-bottom: 0.5rem; }
          .endpoint { 
            margin-bottom: 1rem; 
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 5px;
            border-left: 4px solid #2c5aa0;
          }
          a { 
            text-decoration: none; 
            color: white; 
            background-color: #007bff; 
            padding: 0.5rem 1rem; 
            border-radius: 4px; 
            display: inline-block;
            margin-right: 0.5rem;
          }
          a:hover { background-color: #0056b3; }
          .api-example {
            background-color: #2d3748;
            color: #e2e8f0;
            padding: 1rem;
            border-radius: 4px;
            font-family: monospace;
            margin: 1rem 0;
            overflow-x: auto;
          }
          .highlight { background-color: #fff3cd; padding: 1rem; border-radius: 4px; margin: 1rem 0; }
        </style>
      </head>
      <body>
        <div class="container">
          <h1>🏃‍♂️ Fitness Tracker API</h1>
          <p class="subtitle">A comprehensive REST API for tracking fitness activities, goals, and progress</p>

          <div class="section">
            <h2>🚀 Quick Start for Developers</h2>
            <div class="highlight">
              <strong>New to our API?</strong> Register for an API key to get started!
              <br><br>
              <a href="/api/developers/register/" target="_blank">Register for API Access</a>
              <a href="/api/developers/info/" target="_blank">API Documentation</a>
            </div>
          </div>

          <div class="section">
            <h2>📖 API Endpoints</h2>
            <div class="endpoint">
              <strong>Developer Registration:</strong> 
              <a href="/api/developers/register/" target="_blank">Register</a>
              <a href="/api/developers/info/" target="_blank">Info</a>
            </div>
            <div class="endpoint">
              <strong>Activities:</strong> 
              <a href="/api/activities/" target="_blank">Activities</a>
              <a href="/api/activities/metrics/" target="_blank">Metrics</a>
              <a href="/api/activities/leaderboard/" target="_blank">Leaderboard</a>
            </div>
            <div class="endpoint">
              <strong>User Auth (JWT):</strong> 
              <a href="/api/auth/" target="_blank">Auth</a>
              <a href="/api/token/" target="_blank">Get Token</a>
            </div>
            <div class="endpoint">
              <strong>Admin Panel:</strong> 
              <a href="/admin/" target="_blank">Admin Dashboard</a>
            </div>
          </div>

          <div class="section">
            <h2>🔑 API Key Authentication</h2>
            <p>Use your API key in the Authorization header:</p>
            <div class="api-example">curl -X GET "https://your-api.com/api/activities/metrics/" \\
  -H "Authorization: Api-Key YOUR_API_KEY_HERE" \\
  -H "Content-Type: application/json"</div>
          </div>

          <div class="section">
            <h2>📊 Example Response</h2>
            <div class="api-example">{
  "total_activities": 25,
  "total_duration": 1250,
  "total_distance": "125.50",
  "total_calories": 8750,
  "most_common_activity": "running",
  "activities_by_type": {
    "running": 12,
    "cycling": 8,
    "swimming": 5
  }
}</div>
          </div>

          <div class="section">
            <h2>🛠 Rate Limits</h2>
            <p>Default limits: 1,000 requests/hour, 10,000 requests/day</p>
          </div>
        </div>
      </body>
    </html>
    """
    return HttpResponse(html)

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    
    # User authentication (JWT)
    path('api/auth/', include('users.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Developer API registration
    path('api/developers/', include('users.urls', namespace='developers')),
    
    # Main API endpoints
    path('api/activities/', include('activities.urls')),
]