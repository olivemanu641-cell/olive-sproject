"""
Models for internship applications
New workflow: Visitor applies -> Admin approves -> Auto-create Intern account
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator

User = get_user_model()


class InternshipApplication(models.Model):
    """
    Application submitted by visitors for internships
    This is the first step before becoming an intern
    """
    
    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending Review')
        APPROVED = 'approved', _('Approved')
        REJECTED = 'rejected', _('Rejected')
        INTERN_CREATED = 'intern_created', _('Intern Account Created')
    
    # Personal Information
    first_name = models.CharField(_('First Name'), max_length=150)
    last_name = models.CharField(_('Last Name'), max_length=150)
    email = models.EmailField(_('Email Address'))
    phone = models.CharField(_('Phone Number'), max_length=20)
    
    # Address Information
    address = models.TextField(_('Address'))
    city = models.CharField(_('City'), max_length=100)
    country = models.CharField(_('Country'), max_length=100)
    postal_code = models.CharField(_('Postal Code'), max_length=20, blank=True)
    
    # Educational Information
    institution = models.CharField(
        _('Educational Institution'), 
        max_length=200,
        help_text=_('Name of your school/university')
    )
    field_of_study = models.CharField(
        _('Field of Study'), 
        max_length=200,
        help_text=_('Your major or area of study')
    )
    academic_level = models.CharField(
        _('Academic Level'), 
        max_length=100,
        help_text=_('e.g., Bachelor, Master, PhD')
    )
    graduation_year = models.PositiveIntegerField(
        _('Expected Graduation Year'),
        help_text=_('Year you expect to graduate')
    )
    gpa = models.DecimalField(
        _('GPA/Grade'), 
        max_digits=4, 
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_('Your current GPA or grade average')
    )
    
    # Internship Preferences
    internship = models.ForeignKey(
        'internships.Internship',
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name=_('Desired Internship')
    )
    
    # Application Materials
    cv_resume = models.FileField(
        _('CV/Resume'),
        upload_to='applications/cv/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])],
        help_text=_('Upload your CV or resume (PDF, DOC, DOCX)')
    )
    cover_letter = models.FileField(
        _('Cover Letter'),
        upload_to='applications/cover_letters/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])],
        blank=True,
        help_text=_('Upload your cover letter (optional)')
    )
    transcript = models.FileField(
        _('Academic Transcript'),
        upload_to='applications/transcripts/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        blank=True,
        help_text=_('Upload your academic transcript (optional)')
    )
    
    # Motivation and Experience
    motivation_letter = models.TextField(
        _('Motivation Letter'),
        help_text=_('Tell us why you want this internship and what you hope to achieve')
    )
    previous_experience = models.TextField(
        _('Previous Experience'),
        blank=True,
        help_text=_('Describe any relevant work or internship experience')
    )
    skills = models.TextField(
        _('Skills and Competencies'),
        blank=True,
        help_text=_('List your relevant skills and competencies')
    )
    
    # Availability
    available_start_date = models.DateField(
        _('Available Start Date'),
        help_text=_('When can you start the internship?')
    )
    duration_months = models.PositiveIntegerField(
        _('Preferred Duration (months)'),
        help_text=_('How many months would you like to intern?')
    )
    
    # Application Status and Processing
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        help_text=_('Current status of the application')
    )
    
    # Admin Review
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_applications',
        limit_choices_to={'role': 'admin'},
        verbose_name=_('Reviewed By')
    )
    review_date = models.DateTimeField(
        _('Review Date'),
        null=True,
        blank=True
    )
    review_notes = models.TextField(
        _('Review Notes'),
        blank=True,
        help_text=_('Admin notes about the application')
    )
    
    # Created Intern Account (after approval)
    created_intern = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='application',
        limit_choices_to={'role': 'intern'},
        verbose_name=_('Created Intern Account')
    )
    
    # Timestamps
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Internship Application')
        verbose_name_plural = _('Internship Applications')
        ordering = ['-submitted_at']
        unique_together = ['email', 'internship']  # Prevent duplicate applications
    
    def __str__(self):
        return f"{self.get_full_name()} - {self.internship.title}"
    
    def get_full_name(self):
        """Return the full name of the applicant."""
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def is_pending(self):
        return self.status == self.Status.PENDING
    
    @property
    def is_approved(self):
        return self.status == self.Status.APPROVED
    
    @property
    def is_rejected(self):
        return self.status == self.Status.REJECTED
    
    @property
    def has_intern_account(self):
        return self.created_intern is not None
    
    def approve(self, admin_user, notes=''):
        """Approve the application"""
        self.status = self.Status.APPROVED
        self.reviewed_by = admin_user
        self.review_date = models.timezone.now()
        self.review_notes = notes
        self.save()
    
    def reject(self, admin_user, notes=''):
        """Reject the application"""
        self.status = self.Status.REJECTED
        self.reviewed_by = admin_user
        self.review_date = models.timezone.now()
        self.review_notes = notes
        self.save()
    
    def create_intern_account(self, password='intern2024'):
        """
        Create an intern account after approval
        This is called automatically when application is approved
        """
        if self.status != self.Status.APPROVED:
            raise ValueError("Application must be approved before creating intern account")
        
        if self.created_intern:
            raise ValueError("Intern account already exists for this application")
        
        # Create the intern user account
        intern_user = User.objects.create_user(
            username=self.email.split('@')[0],  # Use email prefix as username
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            phone=self.phone,
            role=User.Role.INTERN,
            is_approved=True,  # Auto-approve since admin already approved application
            password=password
        )
        
        # Update the intern's profile with application data
        profile = intern_user.profile
        profile.address = self.address
        profile.city = self.city
        profile.country = self.country
        profile.postal_code = self.postal_code
        profile.institution = self.institution
        profile.field_of_study = self.field_of_study
        profile.academic_level = self.academic_level
        profile.save()
        
        # Link the created intern to this application
        self.created_intern = intern_user
        self.status = self.Status.INTERN_CREATED
        self.save()
        
        return intern_user
