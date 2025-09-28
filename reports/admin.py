"""
Admin configuration for reports app
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import InternReport, ReportTemplate, Evaluation


@admin.register(InternReport)
class InternReportAdmin(admin.ModelAdmin):
    """
    Admin interface for intern reports
    """
    list_display = (
        'title', 'intern', 'internship', 'period_label', 
        'status', 'self_rating', 'supervisor_rating', 
        'submitted_at', 'reviewed_by'
    )
    list_filter = (
        'status', 'internship', 'self_rating', 'supervisor_rating',
        'created_at', 'submitted_at', 'review_date'
    )
    search_fields = (
        'title', 'intern__first_name', 'intern__last_name',
        'intern__email', 'internship__title', 'period_label'
    )
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Report Information', {
            'fields': ('title', 'period_label', 'intern', 'internship')
        }),
        ('Report Content', {
            'fields': (
                'summary', 'activities_completed', 'challenges_faced',
                'solutions_implemented', 'skills_learned', 'goals_next_period'
            ),
            'classes': ('collapse',)
        }),
        ('Self Assessment', {
            'fields': ('self_rating', 'hours_worked')
        }),
        ('File Attachments', {
            'fields': ('report_file', 'additional_files'),
            'classes': ('collapse',)
        }),
        ('Review & Feedback', {
            'fields': (
                'status', 'supervisor_feedback', 'supervisor_rating',
                'reviewed_by', 'review_date'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'submitted_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'submitted_at', 'review_date')
    
    actions = ['mark_as_reviewed', 'request_revision']
    
    def mark_as_reviewed(self, request, queryset):
        """Mark selected reports as reviewed"""
        updated = queryset.filter(
            status__in=['submitted', 'under_review']
        ).update(status='reviewed')
        
        self.message_user(
            request,
            f'{updated} report(s) marked as reviewed.'
        )
    mark_as_reviewed.short_description = "Mark as reviewed"
    
    def request_revision(self, request, queryset):
        """Request revision for selected reports"""
        updated = queryset.filter(
            status__in=['submitted', 'under_review']
        ).update(status='needs_revision')
        
        self.message_user(
            request,
            f'{updated} report(s) marked as needing revision.'
        )
    request_revision.short_description = "Request revision"


@admin.register(ReportTemplate)
class ReportTemplateAdmin(admin.ModelAdmin):
    """
    Admin interface for report templates
    """
    list_display = ('name', 'is_active', 'is_default', 'created_by', 'created_at')
    list_filter = ('is_active', 'is_default', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)
    
    fieldsets = (
        ('Template Information', {
            'fields': ('name', 'description', 'created_by')
        }),
        ('Template Structure', {
            'fields': ('sections',),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('is_active', 'is_default')
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    """
    Admin interface for evaluations
    """
    list_display = (
        'intern', 'supervisor', 'internship', 'period_type',
        'period_label', 'overall_performance', 'average_rating_display',
        'would_recommend', 'evaluation_date'
    )
    list_filter = (
        'period_type', 'overall_performance', 'would_recommend',
        'evaluation_date', 'internship'
    )
    search_fields = (
        'intern__first_name', 'intern__last_name', 'intern__email',
        'supervisor__first_name', 'supervisor__last_name',
        'internship__title', 'period_label'
    )
    ordering = ('-evaluation_date',)
    
    fieldsets = (
        ('Evaluation Information', {
            'fields': (
                'intern', 'supervisor', 'internship',
                'period_type', 'period_label', 'evaluation_date'
            )
        }),
        ('Performance Ratings', {
            'fields': (
                'technical_skills', 'communication_skills', 'teamwork',
                'initiative', 'reliability', 'overall_performance'
            )
        }),
        ('Qualitative Feedback', {
            'fields': (
                'strengths', 'areas_for_improvement', 'achievements',
                'recommendations'
            ),
            'classes': ('collapse',)
        }),
        ('Goals and Development', {
            'fields': ('goals_met', 'goals_next_period'),
            'classes': ('collapse',)
        }),
        ('Final Assessment', {
            'fields': ('would_recommend', 'additional_comments')
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def average_rating_display(self, obj):
        """Display average rating with color coding"""
        avg = obj.average_rating
        if avg >= 4.5:
            color = 'green'
        elif avg >= 3.5:
            color = 'orange'
        else:
            color = 'red'
        
        return format_html(
            '<span style="color: {};">{:.1f}</span>',
            color, avg
        )
    average_rating_display.short_description = 'Avg Rating'
    average_rating_display.admin_order_field = 'overall_performance'
