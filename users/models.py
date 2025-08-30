from django.contrib.auth.models import AbstractUser
from django.db import models
import secrets
import string

class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'users'

class Developer(models.Model):
    """Developer model for API access"""
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    description = models.TextField(
        blank=True, 
        help_text="Brief description of how you plan to use the API"
    )
    api_key = models.CharField(max_length=40, unique=True, editable=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Rate limiting fields (optional for future use)
    requests_per_hour = models.PositiveIntegerField(default=1000)
    requests_per_day = models.PositiveIntegerField(default=10000)
    
    class Meta:
        db_table = 'developers'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.email})"
    
    def save(self, *args, **kwargs):
        if not self.api_key:
            self.api_key = self.generate_api_key()
        super().save(*args, **kwargs)
    
    @staticmethod
    def generate_api_key():
        """Generate a secure API key"""
        # Generate a 40-character API key with letters and digits
        characters = string.ascii_letters + string.digits
        api_key = ''.join(secrets.choice(characters) for _ in range(40))
        
        # Ensure uniqueness
        while Developer.objects.filter(api_key=api_key).exists():
            api_key = ''.join(secrets.choice(characters) for _ in range(40))
        
        return api_key
    
    def regenerate_api_key(self):
        """Regenerate API key for this developer"""
        self.api_key = self.generate_api_key()
        self.save(update_fields=['api_key', 'updated_at'])
        return self.api_key