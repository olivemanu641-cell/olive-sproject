"""
Forms for internships app
"""
from django import forms
from django.contrib.auth import get_user_model
from .models import Internship, InternshipSkill, InternshipSkillRequirement

User = get_user_model()


class InternshipForm(forms.ModelForm):
    """
    Form for creating and editing internships
    """
    
    class Meta:
        model = Internship
        fields = [
            'title', 'description', 'requirements', 'responsibilities',
            'department', 'location', 'internship_type', 'duration',
            'salary_amount', 'benefits',
            'application_deadline', 'start_date', 'end_date', 'max_applicants',
            'supervisor', 'is_active', 'is_featured'
        ]
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Software Development Intern'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Detailed description of the internship...'}),
            'requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Required skills and qualifications...'}),
            'responsibilities': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Main tasks and responsibilities...'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., IT Department'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Dakar, Senegal or Remote'}),
            'internship_type': forms.Select(attrs={'class': 'form-select'}),
            'duration': forms.Select(attrs={'class': 'form-select'}),
            'salary_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'placeholder': '50000'}),
            'benefits': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Additional benefits offered...'}),
            'application_deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'max_applicants': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '1000', 'value': '50'}),
            'supervisor': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filter supervisor choices to only show supervisors
        self.fields['supervisor'].queryset = User.objects.filter(
            role='supervisor',
            is_approved=True,
            is_active=True
        )
        
        # Make certain fields required
        self.fields['title'].required = True
        self.fields['description'].required = True
        self.fields['requirements'].required = True
        self.fields['responsibilities'].required = True
        self.fields['department'].required = True
        self.fields['location'].required = True
        self.fields['application_deadline'].required = True
        self.fields['start_date'].required = True
        self.fields['end_date'].required = True
        
        # Add help text
        self.fields['salary_amount'].help_text = f'Monthly amount in {getattr(settings, "CURRENCY", "CFA")}'
        self.fields['max_applicants'].help_text = 'Maximum number of applications to accept'
        self.fields['is_featured'].help_text = 'Featured internships appear prominently on the homepage'
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        application_deadline = cleaned_data.get('application_deadline')
        
        # Validate date relationships
        if start_date and end_date:
            if start_date >= end_date:
                raise forms.ValidationError('End date must be after start date.')
        
        if application_deadline and start_date:
            if application_deadline >= start_date:
                raise forms.ValidationError('Application deadline must be before start date.')
        
        return cleaned_data


class InternshipSearchForm(forms.Form):
    """
    Form for searching and filtering internships
    """
    search = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search internships...',
            'id': 'searchInput'
        })
    )
    
    internship_type = forms.ChoiceField(
        choices=[('', 'All Types')] + list(Internship.Type.choices),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    location = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Location...'
        })
    )
    
    department = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Department...'
        })
    )
