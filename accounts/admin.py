"""
Admin configuration for accounts app
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Profile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom User admin with role-based management
    """
    list_display = (
        'email', 'first_name', 'last_name', 'role', 
        'is_approved', 'is_active', 'created_at'
    )
    list_filter = (
        'role', 'is_approved', 'is_active', 'is_staff', 'created_at'
    )
    search_fields = ('email', 'first_name', 'last_name', 'username')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'username', 'phone', 'bio', 'profile_picture')
        }),
        (_('Role & Permissions'), {
            'fields': ('role', 'is_approved', 'is_active', 'is_staff', 'is_superuser')
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'username', 'first_name', 'last_name', 
                'role', 'password1', 'password2', 'is_approved'
            ),
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    actions = ['approve_users', 'disapprove_users']
    
    def approve_users(self, request, queryset):
        """Approve selected users"""
        updated = queryset.update(is_approved=True)
        self.message_user(
            request,
            f'{updated} user(s) were successfully approved.'
        )
    approve_users.short_description = "Approve selected users"
    
    def disapprove_users(self, request, queryset):
        """Disapprove selected users"""
        updated = queryset.update(is_approved=False)
        self.message_user(
            request,
            f'{updated} user(s) were successfully disapproved.'
        )
    disapprove_users.short_description = "Disapprove selected users"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Profile admin configuration
    """
    list_display = (
        'user', 'institution', 'field_of_study', 'department', 'position'
    )
    list_filter = ('user__role', 'institution', 'department')
    search_fields = (
        'user__email', 'user__first_name', 'user__last_name',
        'institution', 'field_of_study', 'department', 'position'
    )
    
    fieldsets = (
        (_('User'), {'fields': ('user',)}),
        (_('Contact Information'), {
            'fields': ('address', 'city', 'country', 'postal_code')
        }),
        (_('Educational Information'), {
            'fields': ('institution', 'field_of_study', 'academic_level'),
            'classes': ('collapse',)
        }),
        (_('Professional Information'), {
            'fields': ('department', 'position', 'experience_years'),
            'classes': ('collapse',)
        }),
        (_('Social Links'), {
            'fields': ('linkedin_url', 'github_url', 'portfolio_url'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
