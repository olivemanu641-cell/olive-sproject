"""
Models for intern reports and supervisor evaluations
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator

User = get_user_model()


class InternReport(models.Model):
    """
    Reports submitted by interns
    """
    
    class Status(models.TextChoices):
        DRAFT = 'draft', _('Draft')
        SUBMITTED = 'submitted', _('Submitted')
        UNDER_REVIEW = 'under_review', _('Under Review')
        REVIEWED = 'reviewed', _('Reviewed')
        NEEDS_REVISION = 'needs_revision', _('Needs Revision')
    
    # Report Information
    title = models.CharField(
        _('Report Title'),
        max_length=200,
        help_text=_('Title of your report')
    )
    
    period_label = models.CharField(
        _('Reporting Period'),
        max_length=100,
        help_text=_('e.g., Week 1, Month 1, Q1 2025')
    )
    
    # Relationships
    intern = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='submitted_reports',
        limit_choices_to={'role': 'intern'},
        verbose_name=_('Intern')
    )
    
    internship = models.ForeignKey(
        'internships.Internship',
        on_delete=models.CASCADE,
        related_name='reports',
        verbose_name=_('Internship')
    )
    
    # Report Content
    summary = models.TextField(
        _('Executive Summary'),
        help_text=_('Brief summary of your activities and achievements')
    )
    
    activities_completed = models.TextField(
        _('Activities Completed'),
        help_text=_('Detailed description of tasks and activities completed')
    )
    
    challenges_faced = models.TextField(
        _('Challenges Faced'),
        blank=True,
        help_text=_('Any challenges or obstacles encountered')
    )
    
    solutions_implemented = models.TextField(
        _('Solutions Implemented'),
        blank=True,
        help_text=_('How you addressed the challenges')
    )
    
    skills_learned = models.TextField(
        _('Skills Learned'),
        blank=True,
        help_text=_('New skills or knowledge acquired')
    )
    
    goals_next_period = models.TextField(
        _('Goals for Next Period'),
        blank=True,
        help_text=_('What you plan to achieve in the next reporting period')
    )
    
    # Self Assessment
    self_rating = models.PositiveIntegerField(
        _('Self Rating'),
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text=_('Rate your performance (1-5 scale)')
    )
    
    hours_worked = models.PositiveIntegerField(
        _('Hours Worked'),
        help_text=_('Total hours worked during this period')
    )
    
    # File Attachments
    report_file = models.FileField(
        _('Report Document'),
        upload_to='reports/documents/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])],
        blank=True,
        help_text=_('Upload detailed report document (optional)')
    )
    
    additional_files = models.FileField(
        _('Additional Files'),
        upload_to='reports/attachments/',
        blank=True,
        help_text=_('Any additional files or evidence')
    )
    
    # Status and Review
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )
    
    supervisor_feedback = models.TextField(
        _('Supervisor Feedback'),
        blank=True,
        help_text=_('Feedback from supervisor')
    )
    
    supervisor_rating = models.PositiveIntegerField(
        _('Supervisor Rating'),
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text=_('Supervisor rating (1-5 scale)')
    )
    
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_reports',
        limit_choices_to={'role': 'supervisor'},
        verbose_name=_('Reviewed By')
    )
    
    review_date = models.DateTimeField(
        _('Review Date'),
        null=True,
        blank=True
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    submitted_at = models.DateTimeField(
        _('Submitted At'),
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = _('Intern Report')
        verbose_name_plural = _('Intern Reports')
        ordering = ['-created_at']
        unique_together = ['intern', 'internship', 'period_label']
    
    def __str__(self):
        return f"{self.title} - {self.intern.get_full_name()} ({self.period_label})"
    
    @property
    def is_draft(self):
        return self.status == self.Status.DRAFT
    
    @property
    def is_submitted(self):
        return self.status in [self.Status.SUBMITTED, self.Status.UNDER_REVIEW, self.Status.REVIEWED]
    
    @property
    def is_reviewed(self):
        return self.status == self.Status.REVIEWED
    
    def submit(self):
        """Submit the report for review"""
        if self.status == self.Status.DRAFT:
            self.status = self.Status.SUBMITTED
            self.submitted_at = models.timezone.now()
            self.save()
    
    def start_review(self, supervisor):
        """Start review process"""
        if self.status == self.Status.SUBMITTED:
            self.status = self.Status.UNDER_REVIEW
            self.reviewed_by = supervisor
            self.save()
    
    def complete_review(self, supervisor, feedback, rating):
        """Complete the review process"""
        self.status = self.Status.REVIEWED
        self.reviewed_by = supervisor
        self.supervisor_feedback = feedback
        self.supervisor_rating = rating
        self.review_date = models.timezone.now()
        self.save()
    
    def request_revision(self, supervisor, feedback):
        """Request revision from intern"""
        self.status = self.Status.NEEDS_REVISION
        self.reviewed_by = supervisor
        self.supervisor_feedback = feedback
        self.review_date = models.timezone.now()
        self.save()


class ReportTemplate(models.Model):
    """
    Templates for different types of reports
    """
    name = models.CharField(_('Template Name'), max_length=200)
    description = models.TextField(_('Description'), blank=True)
    
    # Template Structure
    sections = models.JSONField(
        _('Report Sections'),
        help_text=_('JSON structure defining report sections and fields')
    )
    
    # Usage
    is_active = models.BooleanField(_('Active'), default=True)
    is_default = models.BooleanField(_('Default Template'), default=False)
    
    # Metadata
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_templates',
        limit_choices_to={'role': 'admin'}
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Report Template')
        verbose_name_plural = _('Report Templates')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Evaluation(models.Model):
    """
    Supervisor evaluation of intern performance
    """
    
    class Period(models.TextChoices):
        WEEKLY = 'weekly', _('Weekly')
        MONTHLY = 'monthly', _('Monthly')
        QUARTERLY = 'quarterly', _('Quarterly')
        FINAL = 'final', _('Final Evaluation')
    
    # Basic Information
    intern = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='evaluations',
        limit_choices_to={'role': 'intern'},
        verbose_name=_('Intern')
    )
    
    supervisor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='conducted_evaluations',
        limit_choices_to={'role': 'supervisor'},
        verbose_name=_('Supervisor')
    )
    
    internship = models.ForeignKey(
        'internships.Internship',
        on_delete=models.CASCADE,
        related_name='evaluations',
        verbose_name=_('Internship')
    )
    
    period_type = models.CharField(
        _('Evaluation Period'),
        max_length=20,
        choices=Period.choices,
        default=Period.MONTHLY
    )
    
    period_label = models.CharField(
        _('Period Label'),
        max_length=100,
        help_text=_('e.g., Week 1-4, Month 1, Q1 2025')
    )
    
    # Performance Ratings (1-5 scale)
    technical_skills = models.PositiveIntegerField(
        _('Technical Skills'),
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text=_('Rate technical competency (1-5)')
    )
    
    communication_skills = models.PositiveIntegerField(
        _('Communication Skills'),
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text=_('Rate communication abilities (1-5)')
    )
    
    teamwork = models.PositiveIntegerField(
        _('Teamwork'),
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text=_('Rate collaboration and teamwork (1-5)')
    )
    
    initiative = models.PositiveIntegerField(
        _('Initiative'),
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text=_('Rate proactiveness and initiative (1-5)')
    )
    
    reliability = models.PositiveIntegerField(
        _('Reliability'),
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text=_('Rate dependability and reliability (1-5)')
    )
    
    overall_performance = models.PositiveIntegerField(
        _('Overall Performance'),
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text=_('Overall performance rating (1-5)')
    )
    
    # Qualitative Feedback
    strengths = models.TextField(
        _('Strengths'),
        help_text=_('What the intern does well')
    )
    
    areas_for_improvement = models.TextField(
        _('Areas for Improvement'),
        help_text=_('Areas where the intern can improve')
    )
    
    achievements = models.TextField(
        _('Key Achievements'),
        blank=True,
        help_text=_('Notable accomplishments during this period')
    )
    
    recommendations = models.TextField(
        _('Recommendations'),
        blank=True,
        help_text=_('Recommendations for future development')
    )
    
    # Goals and Development
    goals_met = models.TextField(
        _('Goals Met'),
        blank=True,
        help_text=_('Goals that were successfully achieved')
    )
    
    goals_next_period = models.TextField(
        _('Goals for Next Period'),
        blank=True,
        help_text=_('Suggested goals for the next evaluation period')
    )
    
    # Final Assessment
    would_recommend = models.BooleanField(
        _('Would Recommend'),
        default=True,
        help_text=_('Would you recommend this intern for future opportunities?')
    )
    
    additional_comments = models.TextField(
        _('Additional Comments'),
        blank=True,
        help_text=_('Any additional feedback or comments')
    )
    
    # Timestamps
    evaluation_date = models.DateField(_('Evaluation Date'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Evaluation')
        verbose_name_plural = _('Evaluations')
        ordering = ['-evaluation_date']
        unique_together = ['intern', 'internship', 'period_type', 'period_label']
    
    def __str__(self):
        return f"{self.intern.get_full_name()} - {self.get_period_type_display()} ({self.period_label})"
    
    @property
    def average_rating(self):
        """Calculate average rating across all criteria"""
        ratings = [
            self.technical_skills,
            self.communication_skills,
            self.teamwork,
            self.initiative,
            self.reliability
        ]
        return sum(ratings) / len(ratings)
    
    @property
    def performance_level(self):
        """Get performance level based on overall rating"""
        if self.overall_performance >= 5:
            return 'Excellent'
        elif self.overall_performance >= 4:
            return 'Good'
        elif self.overall_performance >= 3:
            return 'Satisfactory'
        elif self.overall_performance >= 2:
            return 'Needs Improvement'
        else:
            return 'Unsatisfactory'
