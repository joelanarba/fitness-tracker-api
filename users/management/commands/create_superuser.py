import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decouple import config

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a superuser account if none exists'

    def handle(self, *args, **options):
        # Get credentials from environment variables or use defaults
        username = config('ADMIN_USERNAME', default='admin')
        email = config('ADMIN_EMAIL', default='admin@example.com')
        password = config('ADMIN_PASSWORD', default='admin123')
        
        # Check if any superuser already exists
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(
                self.style.WARNING('Superuser already exists, skipping creation')
            )
            return
        
        # Check if user with this username already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'User "{username}" already exists but is not a superuser')
            )
            return
        
        # Create superuser
        try:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f'✅ Successfully created superuser "{username}"')
            )
            self.stdout.write(f'📧 Email: {email}')
            self.stdout.write('🔐 Use this account to access /admin/')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error creating superuser: {str(e)}')
            )