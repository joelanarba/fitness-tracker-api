from rest_framework import authentication, exceptions
from django.contrib.auth.models import AnonymousUser
from .models import Developer

class APIKeyAuthentication(authentication.BaseAuthentication):
    """
    Custom authentication class for API key authentication.
    Clients should authenticate by passing the API key in the "Authorization"
    HTTP header, prepended with the string "Api-Key ".  For example:
    
        Authorization: Api-Key 401f7ac837da42b97f613d789819ff93537bee6a
    """
    keyword = 'Api-Key'
    
    def authenticate(self, request):
        auth = authentication.get_authorization_header(request).split()
        
        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None
        
        if len(auth) == 1:
            msg = 'Invalid API key header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid API key header. API key string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)
        
        try:
            api_key = auth[1].decode()
        except UnicodeError:
            msg = 'Invalid API key header. API key string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)
        
        return self.authenticate_credentials(api_key)
    
    def authenticate_credentials(self, key):
        try:
            developer = Developer.objects.get(api_key=key, is_active=True)
        except Developer.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid API key.')
        
        # Create a fake user object for the developer
        # This allows us to use Django's permission system if needed
        user = AnonymousUser()
        user.is_authenticated = True
        user.developer = developer  # Attach developer info to user
        
        return (user, developer)
    
    def authenticate_header(self, request):
        return self.keyword


class DeveloperAPIKeyAuthentication(authentication.BaseAuthentication):
    """
    Alternative implementation that returns the Developer instance as the user.
    Use this if you want developer-specific permissions or want to track 
    API usage per developer.
    """
    keyword = 'Api-Key'
    
    def authenticate(self, request):
        auth = authentication.get_authorization_header(request).split()
        
        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None
        
        if len(auth) == 1:
            msg = 'Invalid API key header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid API key header. API key string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)
        
        try:
            api_key = auth[1].decode()
        except UnicodeError:
            msg = 'Invalid API key header. API key string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)
        
        return self.authenticate_credentials(api_key)
    
    def authenticate_credentials(self, key):
        try:
            developer = Developer.objects.get(api_key=key, is_active=True)
        except Developer.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid API key.')
        
        return (developer, key)
    
    def authenticate_header(self, request):
        return self.keyword