from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from .models import Developer

User = get_user_model()

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'created_at')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'created_at')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-created_at',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'email', 'company', 'is_active', 
        'requests_per_hour', 'requests_per_day', 'created_at'
    )
    list_filter = ('is_active', 'created_at', 'company')
    search_fields = ('name', 'email', 'company', 'api_key')
    readonly_fields = ('api_key', 'created_at', 'updated_at', 'api_key_display')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Developer Information', {
            'fields': ('name', 'email', 'company', 'website', 'description')
        }),
        ('API Access', {
            'fields': ('is_active', 'api_key_display', 'requests_per_hour', 'requests_per_day')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['deactivate_developers', 'activate_developers', 'regenerate_api_keys']
    
    def api_key_display(self, obj):
        """Display API key with copy button"""
        if obj.api_key:
            return format_html(
                '<code style="background: #f0f0f0; padding: 4px; border-radius: 3px;">{}</code>'
                '<br><small style="color: #666;">Click to select and copy</small>',
                obj.api_key
            )
        return 'No API key'
    api_key_display.short_description = 'API Key'
    
    def deactivate_developers(self, request, queryset):
        """Deactivate selected developers"""
        count = queryset.update(is_active=False)
        self.message_user(
            request, 
            f'{count} developer(s) were successfully deactivated.'
        )
    deactivate_developers.short_description = 'Deactivate selected developers'
    
    def activate_developers(self, request, queryset):
        """Activate selected developers"""
        count = queryset.update(is_active=True)
        self.message_user(
            request, 
            f'{count} developer(s) were successfully activated.'
        )
    activate_developers.short_description = 'Activate selected developers'
    
    def regenerate_api_keys(self, request, queryset):
        """Regenerate API keys for selected developers"""
        count = 0
        for developer in queryset:
            developer.regenerate_api_key()
            count += 1
        
        self.message_user(
            request,
            f'API keys regenerated for {count} developer(s). '
            f'Make sure to notify the developers of their new keys.'
        )
    regenerate_api_keys.short_description = 'Regenerate API keys for selected developers'
    
    def get_readonly_fields(self, request, obj=None):
        """Make API key editable only for superusers"""
        if request.user.is_superuser:
            return ('created_at', 'updated_at')
        return ('api_key', 'created_at', 'updated_at', 'api_key_display')

#Create a custom admin site for API management
class APIAdminSite(admin.AdminSite):
    site_header = 'Fitness Tracker API Administration'
    site_title = 'API Admin'
    index_title = 'Welcome to API Administration'

# use custom admin site
api_admin_site = APIAdminSite(name='api_admin')
api_admin_site.register(Developer, DeveloperAdmin)