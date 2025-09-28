"""
Admin configuration for internships app
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Internship, InternshipSkill, InternshipSkillRequirement


class InternshipSkillRequirementInline(admin.TabularInline):
    """
    Inline admin for skill requirements
    """
    model = InternshipSkillRequirement
    extra = 1
    autocomplete_fields = ['skill']


@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    """
    Admin interface for internships
    """
    list_display = (
        'title', 'department', 'internship_type', 'location',
        'application_deadline', 'is_active', 'application_count',
        'supervisor', 'created_at'
    )
    list_filter = (
        'internship_type', 'duration', 'is_active', 'is_featured',
        'department', 'location', 'created_at'
    )
    search_fields = (
        'title', 'description', 'department', 'location', 'requirements'
    )
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'title', 'description', 'department', 'location'
            )
        }),
        ('Details', {
            'fields': (
                'requirements', 'responsibilities', 'internship_type',
                'duration', 'salary_amount', 'benefits'
            )
        }),
        ('Timeline', {
            'fields': (
                'application_deadline', 'start_date', 'end_date', 'max_applicants'
            )
        }),
        ('Assignment', {
            'fields': ('supervisor', 'created_by')
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured')
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    inlines = [InternshipSkillRequirementInline]
    
    autocomplete_fields = ['supervisor', 'created_by']
    
    actions = ['activate_internships', 'deactivate_internships', 'feature_internships']
    
    def application_count(self, obj):
        """Display application count with color coding"""
        count = obj.application_count
        if count == 0:
            return format_html('<span style="color: gray;">0</span>')
        elif count < 10:
            return format_html('<span style="color: green;">{}</span>', count)
        elif count < 25:
            return format_html('<span style="color: orange;">{}</span>', count)
        else:
            return format_html('<span style="color: red;">{}</span>', count)
    application_count.short_description = 'Applications'
    
    def activate_internships(self, request, queryset):
        """Activate selected internships"""
        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            f'{updated} internship(s) were successfully activated.'
        )
    activate_internships.short_description = "Activate selected internships"
    
    def deactivate_internships(self, request, queryset):
        """Deactivate selected internships"""
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            f'{updated} internship(s) were successfully deactivated.'
        )
    deactivate_internships.short_description = "Deactivate selected internships"
    
    def feature_internships(self, request, queryset):
        """Feature selected internships"""
        updated = queryset.update(is_featured=True)
        self.message_user(
            request,
            f'{updated} internship(s) were successfully featured.'
        )
    feature_internships.short_description = "Feature selected internships"


@admin.register(InternshipSkill)
class InternshipSkillAdmin(admin.ModelAdmin):
    """
    Admin interface for skills
    """
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'category')
    ordering = ('category', 'name')


@admin.register(InternshipSkillRequirement)
class InternshipSkillRequirementAdmin(admin.ModelAdmin):
    """
    Admin interface for skill requirements
    """
    list_display = ('internship', 'skill', 'level', 'is_required')
    list_filter = ('level', 'is_required', 'skill__category')
    search_fields = ('internship__title', 'skill__name')
    autocomplete_fields = ['internship', 'skill']
