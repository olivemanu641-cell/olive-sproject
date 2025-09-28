"""
Forms for reports app
"""
from django import forms
from django.contrib.auth import get_user_model
from .models import InternReport, Evaluation

User = get_user_model()


class InternReportForm(forms.ModelForm):
    """
    Form for interns to create and edit reports
    """
    
    class Meta:
        model = InternReport
        fields = [
            'title', 'period_label', 'internship',
            'summary', 'activities_completed', 'challenges_faced',
            'solutions_implemented', 'skills_learned', 'goals_next_period',
            'self_rating', 'hours_worked',
            'report_file', 'additional_files'
        ]
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Weekly Report - Week 1'}),
            'period_label': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Week 1, Month 1'}),
            'internship': forms.Select(attrs={'class': 'form-select'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Brief summary of your activities...'}),
            'activities_completed': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Detailed description of completed tasks...'}),
            'challenges_faced': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Any challenges encountered...'}),
            'solutions_implemented': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'How you addressed challenges...'}),
            'skills_learned': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'New skills acquired...'}),
            'goals_next_period': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Goals for next period...'}),
            'self_rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'hours_worked': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': '40'}),
            'report_file': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx'}),
            'additional_files': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user and user.is_intern:
            # Filter internships to only show those the intern is assigned to
            from applications.models import InternshipApplication
            intern_internships = InternshipApplication.objects.filter(
                created_intern=user,
                status='intern_created'
            ).values_list('internship', flat=True)
            
            self.fields['internship'].queryset = self.fields['internship'].queryset.filter(
                id__in=intern_internships
            )
        
        # Make required fields
        self.fields['title'].required = True
        self.fields['period_label'].required = True
        self.fields['internship'].required = True
        self.fields['summary'].required = True
        self.fields['activities_completed'].required = True
        self.fields['self_rating'].required = True
        self.fields['hours_worked'].required = True
        
        # Add help text
        self.fields['self_rating'].help_text = 'Rate your performance (1=Poor, 5=Excellent)'
        self.fields['hours_worked'].help_text = 'Total hours worked during this period'
        self.fields['report_file'].help_text = 'Optional: Upload detailed report document'


class ReviewReportForm(forms.Form):
    """
    Form for supervisors to review reports
    """
    supervisor_feedback = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Provide detailed feedback on the intern\'s report...'
        }),
        required=True,
        help_text='Provide constructive feedback on the intern\'s performance and report'
    )
    
    supervisor_rating = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 1,
            'max': 5
        }),
        required=True,
        help_text='Rate the intern\'s performance (1=Poor, 5=Excellent)'
    )
    
    action = forms.ChoiceField(
        choices=[
            ('complete', 'Complete Review'),
            ('revision', 'Request Revision')
        ],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        required=True
    )


class EvaluationForm(forms.ModelForm):
    """
    Form for supervisors to create evaluations
    """
    
    class Meta:
        model = Evaluation
        fields = [
            'intern', 'internship', 'period_type', 'period_label', 'evaluation_date',
            'technical_skills', 'communication_skills', 'teamwork', 'initiative', 'reliability',
            'overall_performance',
            'strengths', 'areas_for_improvement', 'achievements', 'recommendations',
            'goals_met', 'goals_next_period',
            'would_recommend', 'additional_comments'
        ]
        
        widgets = {
            'intern': forms.Select(attrs={'class': 'form-select'}),
            'internship': forms.Select(attrs={'class': 'form-select'}),
            'period_type': forms.Select(attrs={'class': 'form-select'}),
            'period_label': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Week 1-4, Month 1'}),
            'evaluation_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            
            # Rating fields
            'technical_skills': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'communication_skills': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'teamwork': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'initiative': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'reliability': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'overall_performance': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            
            # Text fields
            'strengths': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'areas_for_improvement': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'achievements': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'recommendations': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'goals_met': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'goals_next_period': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'would_recommend': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'additional_comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user and user.is_supervisor:
            # Filter to show only interns supervised by this supervisor
            supervised_internships = user.supervised_internships.all()
            
            # Get interns from applications for these internships
            from applications.models import InternshipApplication
            supervised_interns = User.objects.filter(
                application__internship__in=supervised_internships,
                application__status='intern_created',
                role='intern'
            ).distinct()
            
            self.fields['intern'].queryset = supervised_interns
            self.fields['internship'].queryset = supervised_internships
        
        # Set required fields
        required_fields = [
            'intern', 'internship', 'period_type', 'period_label', 'evaluation_date',
            'technical_skills', 'communication_skills', 'teamwork', 'initiative', 
            'reliability', 'overall_performance', 'strengths', 'areas_for_improvement'
        ]
        
        for field_name in required_fields:
            self.fields[field_name].required = True
        
        # Add help text for rating fields
        rating_fields = [
            'technical_skills', 'communication_skills', 'teamwork', 
            'initiative', 'reliability', 'overall_performance'
        ]
        
        for field_name in rating_fields:
            self.fields[field_name].help_text = '1=Poor, 2=Below Average, 3=Average, 4=Good, 5=Excellent'
