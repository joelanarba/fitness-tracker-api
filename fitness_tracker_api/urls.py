from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.http import HttpResponse

def home(request):
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Fitness Tracker API Playground</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f0f2f5; color: #333; }
            h1 { color: #2c3e50; }
            table { border-collapse: collapse; width: 100%; max-width: 1000px; }
            th, td { border: 1px solid #ddd; padding: 12px; text-align: left; vertical-align: top; }
            th { background-color: #2c3e50; color: white; }
            tr:nth-child(even) { background-color: #f9f9f9; }
            a { text-decoration: none; color: #2980b9; font-weight: bold; }
            a:hover { text-decoration: underline; }
            button { padding: 6px 12px; background-color: #2980b9; color: white; border: none; border-radius: 4px; cursor: pointer; }
            button:hover { background-color: #3498db; }
            pre { background-color: #1e1e1e; color: #d4d4d4; padding: 12px; border-radius: 6px; max-height: 300px; overflow: auto; }
            .success { color: #2ecc71; }
            .error { color: #e74c3c; }
            .info { color: #3498db; }
            textarea { width: 100%; max-width: 500px; height: 100px; padding: 8px; margin-top: 4px; border-radius: 4px; border: 1px solid #ccc; font-family: monospace; }
        </style>
    </head>
    <body>
        <h1>Fitness Tracker API Playground</h1>
        <p>Click "Test" to try endpoints and optionally provide a JSON payload for POST requests.</p>

        <table>
            <tr>
                <th>Endpoint</th>
                <th>URL</th>
                <th>Method</th>
                <th>Description</th>
                <th>Action</th>
            </tr>
            <tr>
                <td>Admin</td>
                <td>/admin/</td>
                <td>GET</td>
                <td>Access the admin dashboard</td>
                <td><button onclick="testEndpoint('/admin/', 'GET')">Test</button></td>
            </tr>
            <tr>
                <td>Auth</td>
                <td>/api/auth/</td>
                <td>POST</td>
                <td>Register or login users</td>
                <td>
                    <textarea id="authPayload">{}</textarea><br>
                    <button onclick="testEndpoint('/api/auth/', 'POST', 'authPayload')">Test</button>
                </td>
            </tr>
            <tr>
                <td>Activities</td>
                <td>/api/activities/</td>
                <td>GET/POST</td>
                <td>View or add activities</td>
                <td>
                    <textarea id="activitiesPayload">{}</textarea><br>
                    <button onclick="testEndpoint('/api/activities/', 'POST', 'activitiesPayload')">POST</button>
                    <button onclick="testEndpoint('/api/activities/', 'GET')">GET</button>
                </td>
            </tr>
            <tr>
                <td>Get Token</td>
                <td>/api/token/</td>
                <td>POST</td>
                <td>Obtain JWT token</td>
                <td>
                    <textarea id="tokenPayload">{ "username": "", "password": "" }</textarea><br>
                    <button onclick="testEndpoint('/api/token/', 'POST', 'tokenPayload')">Test</button>
                </td>
            </tr>
            <tr>
                <td>Refresh Token</td>
                <td>/api/token/refresh/</td>
                <td>POST</td>
                <td>Refresh JWT token</td>
                <td>
                    <textarea id="refreshPayload">{ "refresh": "" }</textarea><br>
                    <button onclick="testEndpoint('/api/token/refresh/', 'POST', 'refreshPayload')">Test</button>
                </td>
            </tr>
        </table>

        <h2>Response:</h2>
        <pre id="responseOutput" class="info">Click "Test" to see output here...</pre>

        <script>
            async function testEndpoint(url, method, textareaId = null) {
                let options = { method: method };

                if (method === 'POST') {
                    options.headers = { 'Content-Type': 'application/json' };
                    if (textareaId) {
                        try {
                            options.body = document.getElementById(textareaId).value;
                            JSON.parse(options.body);
                        } catch (err) {
                            document.getElementById('responseOutput').textContent = 'Invalid JSON: ' + err;
                            document.getElementById('responseOutput').className = 'error';
                            return;
                        }
                    }
                }

                try {
                    const response = await fetch(url, options);
                    const data = await response.json();
                    document.getElementById('responseOutput').textContent = JSON.stringify(data, null, 2);
                    if (response.ok) {
                        document.getElementById('responseOutput').className = 'success';
                    } else {
                        document.getElementById('responseOutput').className = 'error';
                    }
                } catch (err) {
                    document.getElementById('responseOutput').textContent = 'Error: ' + err;
                    document.getElementById('responseOutput').className = 'error';
                }
            }
        </script>
    </body>
    </html>
    """
    return HttpResponse(html_content)

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/activities/', include('activities.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
