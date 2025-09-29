"""
Views for dashboard app
"""
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.db.models import Count, Q, Avg
from django.db import models
from django.utils import timezone
from datetime import timedelta

from applications.models import InternshipApplication
from internships.models import Internship
from reports.models import InternReport, Evaluation
from accounts.models import User


class DashboardHomeView(LoginRequiredMixin, TemplateView):
    """
    Main dashboard that redirects to role-specific dashboard
    """
    def get(self, request, *args, **kwargs):
        user = request.user
        
        if user.is_admin:
            return redirect('dashboard:admin')
        elif user.is_supervisor:
            return redirect('dashboard:supervisor')
        elif user.is_intern:
            return redirect('dashboard:intern')
        else:
            return redirect('accounts:profile')


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin to ensure only admin users can access views"""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.can_access_admin()


class SupervisorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin to ensure only supervisors can access views"""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.can_supervise()


class InternRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin to ensure only interns can access views"""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.can_submit_reports()


class AdminDashboardView(AdminRequiredMixin, TemplateView):
    """
    Admin dashboard with system overview
    """
    template_name = 'dashboard/admin.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Application Statistics
        applications = InternshipApplication.objects.all()
        context['application_stats'] = {
            'total': applications.count(),
            'pending': applications.filter(status='pending').count(),
            'approved': applications.filter(status='approved').count(),
            'rejected': applications.filter(status='rejected').count(),
            'intern_created': applications.filter(status='intern_created').count(),
        }
        
        # User Statistics
        users = User.objects.all()
        context['user_stats'] = {
            'total': users.count(),
            'admins': users.filter(role='admin').count(),
            'supervisors': users.filter(role='supervisor').count(),
            'interns': users.filter(role='intern').count(),
            'pending_approval': users.filter(is_approved=False).count(),
        }
        
        # Internship Statistics
        internships = Internship.objects.all()
        context['internship_stats'] = {
            'total': internships.count(),
            'active': internships.filter(is_active=True).count(),
            'featured': internships.filter(is_featured=True).count(),
            'with_supervisor': internships.filter(supervisor__isnull=False).count(),
        }
        
        # Report Statistics
        reports = InternReport.objects.all()
        context['report_stats'] = {
            'total': reports.count(),
            'submitted': reports.filter(status='submitted').count(),
            'under_review': reports.filter(status='under_review').count(),
            'reviewed': reports.filter(status='reviewed').count(),
            'needs_revision': reports.filter(status='needs_revision').count(),
        }
        
        # Recent Activity
        context['recent_applications'] = InternshipApplication.objects.select_related(
            'internship'
        ).order_by('-submitted_at')[:5]
        
        context['recent_reports'] = InternReport.objects.select_related(
            'intern', 'internship'
        ).order_by('-created_at')[:5]
        
        # Monthly trends (last 6 months)
        six_months_ago = timezone.now() - timedelta(days=180)
        context['monthly_applications'] = applications.filter(
            submitted_at__gte=six_months_ago
        ).extra(
            select={'month': 'EXTRACT(month FROM submitted_at)'}
        ).values('month').annotate(count=Count('id')).order_by('month')
        
        return context


class SupervisorDashboardView(SupervisorRequiredMixin, TemplateView):
    """
    Supervisor dashboard with supervised internships overview
    """
    template_name = 'dashboard/supervisor.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Supervised internships
        supervised_internships = user.supervised_internships.all()
        context['supervised_internships'] = supervised_internships
        
        # Get interns from applications for these internships
        supervised_interns = User.objects.filter(
            application__internship__in=supervised_internships,
            application__status='intern_created',
            role='intern'
        ).distinct()
        
        context['supervised_interns'] = supervised_interns
        
        # Report Statistics
        reports = InternReport.objects.filter(internship__in=supervised_internships)
        context['report_stats'] = {
            'total': reports.count(),
            'pending_review': reports.filter(status='submitted').count(),
            'under_review': reports.filter(status='under_review').count(),
            'reviewed': reports.filter(status='reviewed').count(),
            'needs_revision': reports.filter(status='needs_revision').count(),
        }
        
        # Evaluation Statistics
        evaluations = Evaluation.objects.filter(supervisor=user)
        context['evaluation_stats'] = {
            'total': evaluations.count(),
            'this_month': evaluations.filter(
                evaluation_date__gte=timezone.now().replace(day=1)
            ).count(),
            'average_rating': evaluations.aggregate(
                avg_rating=Avg('overall_performance')
            )['avg_rating'] or 0,
        }
        
        # Recent Reports to Review
        context['recent_reports'] = reports.filter(
            status__in=['submitted', 'under_review']
        ).select_related('intern', 'internship').order_by('-submitted_at')[:5]
        
        # Recent Evaluations
        context['recent_evaluations'] = evaluations.select_related(
            'intern', 'internship'
        ).order_by('-evaluation_date')[:5]
        
        # Performance Overview
        context['performance_overview'] = evaluations.values(
            'overall_performance'
        ).annotate(count=Count('id')).order_by('overall_performance')
        
        return context


class InternDashboardView(InternRequiredMixin, TemplateView):
    """
    Intern dashboard with personal progress overview
    """
    template_name = 'dashboard/intern.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get intern's application and internship
        try:
            application = InternshipApplication.objects.get(
                created_intern=user,
                status='intern_created'
            )
            context['application'] = application
            context['internship'] = application.internship
        except InternshipApplication.DoesNotExist:
            context['application'] = None
            context['internship'] = None
        
        # Report Statistics
        reports = InternReport.objects.filter(intern=user)
        context['report_stats'] = {
            'total': reports.count(),
            'draft': reports.filter(status='draft').count(),
            'submitted': reports.filter(status='submitted').count(),
            'reviewed': reports.filter(status='reviewed').count(),
            'needs_revision': reports.filter(status='needs_revision').count(),
        }
        
        # Recent Reports
        context['recent_reports'] = reports.select_related(
            'internship', 'reviewed_by'
        ).order_by('-created_at')[:5]
        
        # Evaluations received
        evaluations = Evaluation.objects.filter(intern=user)
        context['evaluations'] = evaluations.select_related(
            'supervisor', 'internship'
        ).order_by('-evaluation_date')[:3]
        
        # Performance metrics
        if evaluations.exists():
            context['performance_metrics'] = {
                'average_rating': evaluations.aggregate(
                    avg_rating=models.Avg('overall_performance')
                )['avg_rating'],
                'latest_evaluation': evaluations.first(),
                'total_evaluations': evaluations.count(),
            }
        else:
            context['performance_metrics'] = None
        
        # Progress tracking
        if context['internship']:
            internship = context['internship']
            start_date = internship.start_date
            end_date = internship.end_date
            current_date = timezone.now().date()
            
            if start_date <= current_date <= end_date:
                total_days = (end_date - start_date).days
                elapsed_days = (current_date - start_date).days
                progress_percentage = (elapsed_days / total_days) * 100 if total_days > 0 else 0
                
                context['internship_progress'] = {
                    'percentage': min(progress_percentage, 100),
                    'days_elapsed': elapsed_days,
                    'total_days': total_days,
                    'days_remaining': max(0, total_days - elapsed_days),
                }
            else:
                context['internship_progress'] = None
        
        # Goals and achievements
        latest_evaluation = evaluations.first() if evaluations.exists() else None
        if latest_evaluation:
            context['current_goals'] = latest_evaluation.goals_next_period
            context['recent_achievements'] = latest_evaluation.achievements
        
        return context
