"""
Admin configuration for applications app
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from .models import InternshipApplication


@admin.register(InternshipApplication)
class InternshipApplicationAdmin(admin.ModelAdmin):
    """
    Admin interface for managing internship applications
    """
    list_display = (
        'get_full_name', 'email', 'internship', 'status', 
        'submitted_at', 'reviewed_by', 'has_intern_account'
    )
    list_filter = (
        'status', 'internship', 'institution', 'field_of_study', 
        'submitted_at', 'review_date'
    )
    search_fields = (
        'first_name', 'last_name', 'email', 'institution', 
        'field_of_study', 'internship__title'
    )
    ordering = ('-submitted_at',)
    
    readonly_fields = (
        'submitted_at', 'updated_at', 'review_date', 'created_intern'
    )
    
    fieldsets = (
        ('Personal Information', {
            'fields': (
                'first_name', 'last_name', 'email', 'phone',
                'address', 'city', 'country', 'postal_code'
            )
        }),
        ('Educational Information', {
            'fields': (
                'institution', 'field_of_study', 'academic_level',
                'graduation_year', 'gpa'
            )
        }),
        ('Internship Details', {
            'fields': (
                'internship', 'available_start_date', 'duration_months'
            )
        }),
        ('Application Materials', {
            'fields': (
                'cv_resume', 'cover_letter', 'transcript',
                'motivation_letter', 'previous_experience', 'skills'
            ),
            'classes': ('collapse',)
        }),
        ('Review & Status', {
            'fields': (
                'status', 'reviewed_by', 'review_date', 'review_notes',
                'created_intern'
            )
        }),
        ('Timestamps', {
            'fields': ('submitted_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_applications', 'reject_applications', 'create_intern_accounts']
    
    def get_full_name(self, obj):
        """Display full name of applicant"""
        return obj.get_full_name()
    get_full_name.short_description = 'Applicant Name'
    get_full_name.admin_order_field = 'first_name'
    
    def has_intern_account(self, obj):
        """Show if intern account has been created"""
        if obj.created_intern:
            return format_html(
                '<span style="color: green;">✓ Yes</span>'
            )
        return format_html(
            '<span style="color: red;">✗ No</span>'
        )
    has_intern_account.short_description = 'Intern Account'
    has_intern_account.boolean = True
    
    def approve_applications(self, request, queryset):
        """Approve selected applications"""
        pending_applications = queryset.filter(status='pending')
        
        if not pending_applications.exists():
            self.message_user(
                request,
                'No pending applications selected.',
                level=messages.WARNING
            )
            return
        
        approved_count = 0
        for application in pending_applications:
            application.approve(request.user, 'Approved via admin action')
            approved_count += 1
        
        self.message_user(
            request,
            f'{approved_count} application(s) were successfully approved.'
        )
    approve_applications.short_description = "Approve selected applications"
    
    def reject_applications(self, request, queryset):
        """Reject selected applications"""
        pending_applications = queryset.filter(status='pending')
        
        if not pending_applications.exists():
            self.message_user(
                request,
                'No pending applications selected.',
                level=messages.WARNING
            )
            return
        
        rejected_count = 0
        for application in pending_applications:
            application.reject(request.user, 'Rejected via admin action')
            rejected_count += 1
        
        self.message_user(
            request,
            f'{rejected_count} application(s) were successfully rejected.'
        )
    reject_applications.short_description = "Reject selected applications"
    
    def create_intern_accounts(self, request, queryset):
        """Create intern accounts for approved applications"""
        approved_applications = queryset.filter(
            status='approved',
            created_intern__isnull=True
        )
        
        if not approved_applications.exists():
            self.message_user(
                request,
                'No approved applications without intern accounts selected.',
                level=messages.WARNING
            )
            return
        
        created_count = 0
        for application in approved_applications:
            try:
                intern_user = application.create_intern_account(
                    password=settings.DEFAULT_INTERN_PASSWORD
                )
                created_count += 1
            except Exception as e:
                self.message_user(
                    request,
                    f'Error creating account for {application.get_full_name()}: {str(e)}',
                    level=messages.ERROR
                )
        
        self.message_user(
            request,
            f'{created_count} intern account(s) were successfully created.'
        )
    create_intern_accounts.short_description = "Create intern accounts for approved applications"
