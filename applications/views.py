"""
Views for applications app
"""
from django.views.generic import CreateView, TemplateView, ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.conf import settings
from .models import InternshipApplication
from .forms import InternshipApplicationForm
from internships.models import Internship


class ApplicationCreateView(CreateView):
    """
    View for visitors to submit internship applications
    """
    model = InternshipApplication
    form_class = InternshipApplicationForm
    template_name = 'applications/apply.html'
    success_url = reverse_lazy('applications:success')
    
    def get_initial(self):
        """Pre-populate internship if specified in URL"""
        initial = super().get_initial()
        internship_id = self.kwargs.get('internship_id')
        if internship_id:
            initial['internship'] = get_object_or_404(Internship, id=internship_id)
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['internships'] = Internship.objects.filter(is_active=True)
        internship_id = self.kwargs.get('internship_id')
        if internship_id:
            context['selected_internship'] = get_object_or_404(Internship, id=internship_id)
        return context
    
    def form_valid(self, form):
        messages.success(
            self.request,
            'Your application has been submitted successfully! '
            'You will receive an email notification once it has been reviewed.'
        )
        return super().form_valid(form)


class ApplicationSuccessView(TemplateView):
    """
    Success page after application submission
    """
    template_name = 'applications/success.html'


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin to ensure only admin users can access views
    """
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.can_access_admin()


class ApplicationListView(AdminRequiredMixin, ListView):
    """
    Admin view to list all applications
    """
    model = InternshipApplication
    template_name = 'applications/manage.html'
    context_object_name = 'applications'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = InternshipApplication.objects.select_related(
            'internship', 'reviewed_by', 'created_intern'
        ).order_by('-submitted_at')
        
        # Filter by status if requested
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by internship if requested
        internship_id = self.request.GET.get('internship')
        if internship_id:
            queryset = queryset.filter(internship_id=internship_id)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = InternshipApplication.Status.choices
        context['internships'] = Internship.objects.all()
        context['current_status'] = self.request.GET.get('status', '')
        context['current_internship'] = self.request.GET.get('internship', '')
        
        # Statistics
        context['stats'] = {
            'total': InternshipApplication.objects.count(),
            'pending': InternshipApplication.objects.filter(status='pending').count(),
            'approved': InternshipApplication.objects.filter(status='approved').count(),
            'rejected': InternshipApplication.objects.filter(status='rejected').count(),
            'intern_created': InternshipApplication.objects.filter(status='intern_created').count(),
        }
        
        return context


class ApplicationDetailView(AdminRequiredMixin, DetailView):
    """
    Admin view to see application details
    """
    model = InternshipApplication
    template_name = 'applications/detail.html'
    context_object_name = 'application'


class ApproveApplicationView(AdminRequiredMixin, View):
    """
    Admin view to approve an application
    """
    def post(self, request, pk):
        application = get_object_or_404(InternshipApplication, pk=pk)
        
        if application.status != InternshipApplication.Status.PENDING:
            messages.error(request, 'Only pending applications can be approved.')
            return redirect('applications:detail', pk=pk)
        
        notes = request.POST.get('notes', '')
        application.approve(request.user, notes)
        
        messages.success(
            request,
            f'Application for {application.get_full_name()} has been approved.'
        )
        
        return redirect('applications:detail', pk=pk)


class RejectApplicationView(AdminRequiredMixin, View):
    """
    Admin view to reject an application
    """
    def post(self, request, pk):
        application = get_object_or_404(InternshipApplication, pk=pk)
        
        if application.status != InternshipApplication.Status.PENDING:
            messages.error(request, 'Only pending applications can be rejected.')
            return redirect('applications:detail', pk=pk)
        
        notes = request.POST.get('notes', '')
        application.reject(request.user, notes)
        
        messages.success(
            request,
            f'Application for {application.get_full_name()} has been rejected.'
        )
        
        return redirect('applications:detail', pk=pk)


class CreateInternAccountView(AdminRequiredMixin, View):
    """
    Admin view to create intern account for approved application
    """
    def post(self, request, pk):
        application = get_object_or_404(InternshipApplication, pk=pk)
        
        if application.status != InternshipApplication.Status.APPROVED:
            messages.error(request, 'Only approved applications can have intern accounts created.')
            return redirect('applications:detail', pk=pk)
        
        if application.created_intern:
            messages.error(request, 'Intern account already exists for this application.')
            return redirect('applications:detail', pk=pk)
        
        try:
            intern_user = application.create_intern_account(
                password=settings.DEFAULT_INTERN_PASSWORD
            )
            
            messages.success(
                request,
                f'Intern account created successfully for {application.get_full_name()}. '
                f'Login credentials: Email: {intern_user.email}, '
                f'Password: {settings.DEFAULT_INTERN_PASSWORD}'
            )
            
        except Exception as e:
            messages.error(
                request,
                f'Error creating intern account: {str(e)}'
            )
        
        return redirect('applications:detail', pk=pk)
