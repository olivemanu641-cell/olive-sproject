"""
Forms for internship applications
"""
from django import forms
from django.core.validators import FileExtensionValidator
from .models import InternshipApplication


class InternshipApplicationForm(forms.ModelForm):
    """
    Form for visitors to apply for internships
    """
    
    class Meta:
        model = InternshipApplication
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'address', 'city', 'country', 'postal_code',
            'institution', 'field_of_study', 'academic_level',
            'graduation_year', 'gpa',
            'internship',
            'cv_resume', 'cover_letter', 'transcript',
            'motivation_letter', 'previous_experience', 'skills',
            'available_start_date', 'duration_months'
        ]
        
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your.email@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1234567890'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Your full address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'}),
            'institution': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'University/School name'}),
            'field_of_study': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Computer Science, Engineering, etc.'}),
            'academic_level': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bachelor, Master, PhD'}),
            'graduation_year': forms.NumberInput(attrs={'class': 'form-control', 'min': 2024, 'max': 2030}),
            'gpa': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '4.0', 'placeholder': '3.50'}),
            'internship': forms.Select(attrs={'class': 'form-select'}),
            'cv_resume': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx'}),
            'cover_letter': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx'}),
            'transcript': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
            'motivation_letter': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Tell us why you want this internship...'}),
            'previous_experience': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe any relevant experience...'}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'List your relevant skills...'}),
            'available_start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'duration_months': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 12, 'placeholder': '6'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Make certain fields required
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['phone'].required = True
        self.fields['address'].required = True
        self.fields['city'].required = True
        self.fields['country'].required = True
        self.fields['institution'].required = True
        self.fields['field_of_study'].required = True
        self.fields['academic_level'].required = True
        self.fields['graduation_year'].required = True
        self.fields['internship'].required = True
        self.fields['cv_resume'].required = True
        self.fields['motivation_letter'].required = True
        self.fields['available_start_date'].required = True
        self.fields['duration_months'].required = True
        
        # Add help text
        self.fields['cv_resume'].help_text = 'Upload your CV/Resume (PDF, DOC, DOCX - Max 5MB)'
        self.fields['cover_letter'].help_text = 'Optional: Upload your cover letter'
        self.fields['transcript'].help_text = 'Optional: Upload your academic transcript'
        self.fields['gpa'].help_text = 'Optional: Your current GPA or grade average'
        self.fields['duration_months'].help_text = 'How many months would you like to intern?'
    
    def clean_email(self):
        """Validate email uniqueness for the selected internship"""
        email = self.cleaned_data.get('email')
        internship = self.cleaned_data.get('internship')
        
        if email and internship:
            existing = InternshipApplication.objects.filter(
                email=email,
                internship=internship
            ).exclude(pk=self.instance.pk if self.instance else None)
            
            if existing.exists():
                raise forms.ValidationError(
                    'You have already applied for this internship with this email address.'
                )
        
        return email
    
    def clean_cv_resume(self):
        """Validate CV file size"""
        cv_file = self.cleaned_data.get('cv_resume')
        if cv_file:
            if cv_file.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError('File size must be less than 5MB.')
        return cv_file
