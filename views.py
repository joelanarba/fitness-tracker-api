from django.http import HttpResponse
from django.urls import reverse

def home(request):
    html_content = f"""
    <html>
        <head>
            <title>Fitness Tracker API</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 40px;
                    background-color: #f9f9f9;
                    color: #333;
                }}
                h1 {{
                    color: #2c3e50;
                }}
                p {{
                    font-size: 1.1em;
                }}
                ul {{
                    list-style: none;
                    padding: 0;
                }}
                li {{
                    margin: 10px 0;
                    font-size: 1em;
                }}
                a {{
                    text-decoration: none;
                    color: #2980b9;
                    font-weight: bold;
                }}
                a:hover {{
                    text-decoration: underline;
                }}
                .endpoint {{
                    background-color: #ecf0f1;
                    padding: 10px;
                    border-radius: 5px;
                    display: inline-block;
                }}
            </style>
        </head>
        <body>
            <h1>Fitness Tracker API</h1>
            <p>Welcome! Here are the available endpoints:</p>
            <ul>
                <li class="endpoint"><a href="{reverse('admin:index')}">Admin Dashboard</a></li>
                <li class="endpoint"><a href="/api/auth/">Auth Endpoints</a></li>
                <li class="endpoint"><a href="/api/activities/">Activities Endpoints</a></li>
                <li class="endpoint"><a href="/api/token/">Get Token</a></li>
                <li class="endpoint"><a href="/api/token/refresh/">Refresh Token</a></li>
            </ul>
            <p>Happy tracking!</p>
        </body>
    </html>
    """
    return HttpResponse(html_content)
