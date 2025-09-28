"""
Views for reports app
"""
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from .models import InternReport, Evaluation
from .forms import InternReportForm, ReviewReportForm, EvaluationForm


class InternRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin to ensure only interns can access views"""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_intern


class SupervisorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin to ensure only supervisors can access views"""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_supervisor


# ===== INTERN REPORT VIEWS =====

class ReportListView(InternRequiredMixin, ListView):
    """List all reports for the current intern"""
    model = InternReport
    template_name = 'reports/list.html'
    context_object_name = 'reports'
    paginate_by = 10
    
    def get_queryset(self):
        return InternReport.objects.filter(
            intern=self.request.user
        ).select_related('internship', 'reviewed_by').order_by('-created_at')


class ReportDetailView(InternRequiredMixin, DetailView):
    """View report details"""
    model = InternReport
    template_name = 'reports/detail.html'
    context_object_name = 'report'
    
    def get_queryset(self):
        return InternReport.objects.filter(intern=self.request.user)


class ReportCreateView(InternRequiredMixin, CreateView):
    """Create a new report"""
    model = InternReport
    form_class = InternReportForm
    template_name = 'reports/create.html'
    success_url = reverse_lazy('reports:list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.intern = self.request.user
        messages.success(
            self.request,
            'Report created successfully! You can edit it before submitting.'
        )
        return super().form_valid(form)


class ReportUpdateView(InternRequiredMixin, UpdateView):
    """Edit an existing report"""
    model = InternReport
    form_class = InternReportForm
    template_name = 'reports/edit.html'
    success_url = reverse_lazy('reports:list')
    
    def get_queryset(self):
        # Only allow editing of draft reports
        return InternReport.objects.filter(
            intern=self.request.user,
            status__in=['draft', 'needs_revision']
        )
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, 'Report updated successfully!')
        return super().form_valid(form)


class SubmitReportView(InternRequiredMixin, View):
    """Submit a report for review"""
    def post(self, request, pk):
        report = get_object_or_404(
            InternReport,
            pk=pk,
            intern=request.user,
            status__in=['draft', 'needs_revision']
        )
        
        report.submit()
        messages.success(
            request,
            f'Report "{report.title}" has been submitted for review!'
        )
        
        return redirect('reports:detail', pk=pk)


class ReportDeleteView(InternRequiredMixin, DeleteView):
    """Delete a report"""
    model = InternReport
    template_name = 'reports/delete.html'
    success_url = reverse_lazy('reports:list')
    
    def get_queryset(self):
        # Only allow deletion of draft reports
        return InternReport.objects.filter(
            intern=self.request.user,
            status='draft'
        )
    
    def delete(self, request, *args, **kwargs):
        report = self.get_object()
        messages.success(
            request,
            f'Report "{report.title}" has been deleted.'
        )
        return super().delete(request, *args, **kwargs)


# ===== SUPERVISOR REVIEW VIEWS =====

class SupervisorReportListView(SupervisorRequiredMixin, ListView):
    """List reports for supervisor review"""
    model = InternReport
    template_name = 'reports/supervisor_list.html'
    context_object_name = 'reports'
    paginate_by = 15
    
    def get_queryset(self):
        # Get reports from interns in supervised internships
        supervised_internships = self.request.user.supervised_internships.all()
        
        queryset = InternReport.objects.filter(
            internship__in=supervised_internships
        ).select_related('intern', 'internship').order_by('-submitted_at')
        
        # Filter by status if requested
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = InternReport.Status.choices
        context['current_status'] = self.request.GET.get('status', '')
        
        # Statistics
        supervised_internships = self.request.user.supervised_internships.all()
        all_reports = InternReport.objects.filter(internship__in=supervised_internships)
        
        context['stats'] = {
            'total': all_reports.count(),
            'pending': all_reports.filter(status='submitted').count(),
            'under_review': all_reports.filter(status='under_review').count(),
            'reviewed': all_reports.filter(status='reviewed').count(),
            'needs_revision': all_reports.filter(status='needs_revision').count(),
        }
        
        return context


class ReviewReportView(SupervisorRequiredMixin, DetailView):
    """View report for review"""
    model = InternReport
    template_name = 'reports/review.html'
    context_object_name = 'report'
    
    def get_queryset(self):
        supervised_internships = self.request.user.supervised_internships.all()
        return InternReport.objects.filter(internship__in=supervised_internships)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = ReviewReportForm()
        return context


class CompleteReviewView(SupervisorRequiredMixin, View):
    """Complete review of a report"""
    def post(self, request, pk):
        supervised_internships = request.user.supervised_internships.all()
        report = get_object_or_404(
            InternReport,
            pk=pk,
            internship__in=supervised_internships
        )
        
        form = ReviewReportForm(request.POST)
        if form.is_valid():
            feedback = form.cleaned_data['supervisor_feedback']
            rating = form.cleaned_data['supervisor_rating']
            action = form.cleaned_data['action']
            
            if action == 'complete':
                report.complete_review(request.user, feedback, rating)
                messages.success(
                    request,
                    f'Review completed for "{report.title}"'
                )
            else:  # revision
                report.request_revision(request.user, feedback)
                messages.success(
                    request,
                    f'Revision requested for "{report.title}"'
                )
        else:
            messages.error(request, 'Please correct the errors in the form.')
        
        return redirect('reports:review', pk=pk)


# ===== EVALUATION VIEWS =====

class EvaluationListView(SupervisorRequiredMixin, ListView):
    """List evaluations created by supervisor"""
    model = Evaluation
    template_name = 'reports/evaluation_list.html'
    context_object_name = 'evaluations'
    paginate_by = 15
    
    def get_queryset(self):
        return Evaluation.objects.filter(
            supervisor=self.request.user
        ).select_related('intern', 'internship').order_by('-evaluation_date')


class EvaluationDetailView(SupervisorRequiredMixin, DetailView):
    """View evaluation details"""
    model = Evaluation
    template_name = 'reports/evaluation_detail.html'
    context_object_name = 'evaluation'
    
    def get_queryset(self):
        return Evaluation.objects.filter(supervisor=self.request.user)


class EvaluationCreateView(SupervisorRequiredMixin, CreateView):
    """Create a new evaluation"""
    model = Evaluation
    form_class = EvaluationForm
    template_name = 'reports/evaluation_create.html'
    success_url = reverse_lazy('reports:evaluation_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.supervisor = self.request.user
        messages.success(
            self.request,
            f'Evaluation created for {form.instance.intern.get_full_name()}'
        )
        return super().form_valid(form)


class EvaluationUpdateView(SupervisorRequiredMixin, UpdateView):
    """Edit an existing evaluation"""
    model = Evaluation
    form_class = EvaluationForm
    template_name = 'reports/evaluation_edit.html'
    success_url = reverse_lazy('reports:evaluation_list')
    
    def get_queryset(self):
        return Evaluation.objects.filter(supervisor=self.request.user)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        messages.success(
            self.request,
            f'Evaluation updated for {form.instance.intern.get_full_name()}'
        )
        return super().form_valid(form)
