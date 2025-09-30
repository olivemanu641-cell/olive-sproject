"""
Forms for accounts app
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import User, Profile


class EmailAuthenticationForm(AuthenticationForm):
    """
    Custom authentication form that uses email instead of username
    """
    username = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com',
            'autocomplete': 'email'
        })
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'autocomplete': 'current-password'
        })
    )
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username is not None and password:
            self.user_cache = authenticate(
                self.request, 
                username=username, 
                password=password
            )
            if self.user_cache is None:
                raise forms.ValidationError(
                    'Please enter a correct email and password. Note that both fields may be case-sensitive.',
                    code='invalid_login'
                )
            else:
                self.confirm_login_allowed(self.user_cache)
        
        return self.cleaned_data


class ProfileForm(forms.ModelForm):
    """
    Form for editing user profile
    """
    
    class Meta:
        model = Profile
        fields = [
            'address', 'city', 'country', 'postal_code',
            'institution', 'field_of_study', 'academic_level',
            'department', 'position', 'experience_years',
            'linkedin_url', 'github_url', 'portfolio_url'
        ]
        
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'experience_years': forms.NumberInput(attrs={'min': 0, 'max': 50}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add CSS classes for styling
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
        # Conditional field display based on user role
        if hasattr(self.instance, 'user'):
            user = self.instance.user
            
            if user.is_intern:
                # Show educational fields for interns
                self.fields['institution'].required = True
                self.fields['field_of_study'].required = True
                # Hide professional fields
                del self.fields['department']
                del self.fields['position']
                del self.fields['experience_years']
                
            elif user.is_supervisor:
                # Show professional fields for supervisors
                self.fields['department'].required = True
                self.fields['position'].required = True
                # Hide educational fields
                del self.fields['institution']
                del self.fields['field_of_study']
                del self.fields['academic_level']
