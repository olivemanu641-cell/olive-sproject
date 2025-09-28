"""
Models for internship opportunities
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Internship(models.Model):
    """
    Internship opportunity model
    """
    
    class Type(models.TextChoices):
        PAID = 'paid', _('Paid')
        UNPAID = 'unpaid', _('Unpaid')
        STIPEND = 'stipend', _('Stipend')
    
    class Duration(models.TextChoices):
        SHORT = '1-3', _('1-3 months')
        MEDIUM = '3-6', _('3-6 months')
        LONG = '6-12', _('6-12 months')
        EXTENDED = '12+', _('12+ months')
    
    # Basic Information
    title = models.CharField(
        _('Title'),
        max_length=200,
        help_text=_('Internship position title')
    )
    
    description = models.TextField(
        _('Description'),
        help_text=_('Detailed description of the internship')
    )
    
    requirements = models.TextField(
        _('Requirements'),
        help_text=_('Skills and qualifications required')
    )
    
    responsibilities = models.TextField(
        _('Responsibilities'),
        help_text=_('Main tasks and responsibilities')
    )
    
    # Internship Details
    department = models.CharField(
        _('Department'),
        max_length=200,
        help_text=_('Department or team')
    )
    
    location = models.CharField(
        _('Location'),
        max_length=200,
        help_text=_('Work location (city, country or remote)')
    )
    
    internship_type = models.CharField(
        _('Type'),
        max_length=20,
        choices=Type.choices,
        default=Type.UNPAID
    )
    
    duration = models.CharField(
        _('Duration'),
        max_length=10,
        choices=Duration.choices,
        default=Duration.MEDIUM
    )
    
    # Compensation
    salary_amount = models.DecimalField(
        _('Salary/Stipend Amount'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_('Monthly amount in CFA')
    )
    
    benefits = models.TextField(
        _('Benefits'),
        blank=True,
        help_text=_('Additional benefits offered')
    )
    
    # Application Details
    application_deadline = models.DateField(
        _('Application Deadline'),
        help_text=_('Last date to apply')
    )
    
    start_date = models.DateField(
        _('Expected Start Date'),
        help_text=_('When the internship is expected to start')
    )
    
    end_date = models.DateField(
        _('Expected End Date'),
        help_text=_('When the internship is expected to end')
    )
    
    max_applicants = models.PositiveIntegerField(
        _('Maximum Applicants'),
        default=50,
        help_text=_('Maximum number of applications to accept')
    )
    
    # Supervisor Assignment
    supervisor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='supervised_internships',
        limit_choices_to={'role': 'supervisor'},
        verbose_name=_('Assigned Supervisor')
    )
    
    # Status and Visibility
    is_active = models.BooleanField(
        _('Active'),
        default=True,
        help_text=_('Whether this internship is currently accepting applications')
    )
    
    is_featured = models.BooleanField(
        _('Featured'),
        default=False,
        help_text=_('Whether to feature this internship prominently')
    )
    
    # Meta Information
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_internships',
        limit_choices_to={'role': 'admin'},
        verbose_name=_('Created By')
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Internship')
        verbose_name_plural = _('Internships')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.department}"
    
    def get_absolute_url(self):
        return reverse('internships:detail', kwargs={'pk': self.pk})
    
    @property
    def is_paid(self):
        return self.internship_type == self.Type.PAID
    
    @property
    def application_count(self):
        """Get number of applications for this internship"""
        return self.applications.count()
    
    @property
    def pending_applications_count(self):
        """Get number of pending applications"""
        return self.applications.filter(status='pending').count()
    
    @property
    def approved_applications_count(self):
        """Get number of approved applications"""
        return self.applications.filter(status='approved').count()
    
    @property
    def is_application_open(self):
        """Check if applications are still open"""
        from django.utils import timezone
        return (
            self.is_active and 
            self.application_deadline >= timezone.now().date() and
            self.application_count < self.max_applicants
        )
    
    def get_salary_display(self):
        """Get formatted salary display"""
        if self.salary_amount:
            return f"{self.salary_amount:,.0f} CFA/month"
        return "Not specified"


class InternshipSkill(models.Model):
    """
    Skills required for internships
    """
    name = models.CharField(_('Skill Name'), max_length=100, unique=True)
    category = models.CharField(
        _('Category'),
        max_length=50,
        blank=True,
        help_text=_('e.g., Programming, Design, Marketing')
    )
    
    class Meta:
        verbose_name = _('Skill')
        verbose_name_plural = _('Skills')
        ordering = ['category', 'name']
    
    def __str__(self):
        return self.name


class InternshipSkillRequirement(models.Model):
    """
    Through model for internship-skill relationships
    """
    
    class Level(models.TextChoices):
        BEGINNER = 'beginner', _('Beginner')
        INTERMEDIATE = 'intermediate', _('Intermediate')
        ADVANCED = 'advanced', _('Advanced')
        EXPERT = 'expert', _('Expert')
    
    internship = models.ForeignKey(
        Internship,
        on_delete=models.CASCADE,
        related_name='skill_requirements'
    )
    skill = models.ForeignKey(
        InternshipSkill,
        on_delete=models.CASCADE,
        related_name='internship_requirements'
    )
    level = models.CharField(
        _('Required Level'),
        max_length=20,
        choices=Level.choices,
        default=Level.BEGINNER
    )
    is_required = models.BooleanField(
        _('Required'),
        default=True,
        help_text=_('Whether this skill is required or preferred')
    )
    
    class Meta:
        verbose_name = _('Skill Requirement')
        verbose_name_plural = _('Skill Requirements')
        unique_together = ['internship', 'skill']
    
    def __str__(self):
        return f"{self.internship.title} - {self.skill.name} ({self.get_level_display()})"
