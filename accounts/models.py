"""
User models for Shaderl Internships system.
Simplified roles: Admin, Supervisor, Intern (removed coordinator)
"""
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Custom user manager for email-based authentication"""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user with an email and password."""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with an email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_approved', True)
        extra_fields.setdefault('role', 'admin')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom User model with role-based access
    """
    
    class Role(models.TextChoices):
        ADMIN = 'admin', _('Administrator')
        SUPERVISOR = 'supervisor', _('Supervisor')
        INTERN = 'intern', _('Intern')
    
    # Override username to allow null/blank since we use email
    username = models.CharField(max_length=150, blank=True, null=True)
    
    # Basic Information
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    phone = models.CharField(_('phone number'), max_length=20, blank=True)
    
    # Role and Status
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.INTERN,
        help_text=_('User role in the system')
    )
    
    is_approved = models.BooleanField(
        default=False,
        help_text=_('Whether the user account has been approved by admin')
    )
    
    # Profile Information
    profile_picture = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True,
        help_text=_('User profile picture')
    )
    
    bio = models.TextField(
        blank=True,
        help_text=_('Short biography or description')
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Use email as username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    # Custom manager
    objects = UserManager()
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
    
    def get_full_name(self):
        """Return the full name of the user."""
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name
    
    @property
    def is_admin(self):
        """Check if user is an administrator."""
        return self.role == self.Role.ADMIN
    
    @property
    def is_supervisor(self):
        """Check if user is a supervisor."""
        return self.role == self.Role.SUPERVISOR
    
    @property
    def is_intern(self):
        """Check if user is an intern."""
        return self.role == self.Role.INTERN
    
    def can_access_admin(self):
        """Check if user can access admin features."""
        return self.is_admin and self.is_approved
    
    def can_supervise(self):
        """Check if user can supervise interns."""
        return self.is_supervisor and self.is_approved
    
    def can_submit_reports(self):
        """Check if user can submit reports."""
        return self.is_intern and self.is_approved


class Profile(models.Model):
    """
    Extended profile information for users
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    
    # Contact Information
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    
    # Educational Information (for interns)
    institution = models.CharField(
        max_length=200,
        blank=True,
        help_text=_('Educational institution name')
    )
    field_of_study = models.CharField(
        max_length=200,
        blank=True,
        help_text=_('Field of study or major')
    )
    academic_level = models.CharField(
        max_length=100,
        blank=True,
        help_text=_('Academic level (Bachelor, Master, etc.)')
    )
    
    # Professional Information (for supervisors)
    department = models.CharField(
        max_length=200,
        blank=True,
        help_text=_('Department or division')
    )
    position = models.CharField(
        max_length=200,
        blank=True,
        help_text=_('Job title or position')
    )
    experience_years = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text=_('Years of professional experience')
    )
    
    # Social Links
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
    
    def __str__(self):
        return f"{self.user.get_full_name()}'s Profile"
