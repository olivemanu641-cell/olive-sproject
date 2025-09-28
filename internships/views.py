"""
Views for internships app
"""
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Internship
from .forms import InternshipForm


class InternshipListView(ListView):
    """
    Public view to list all active internships
    """
    model = Internship
    template_name = 'internships/list.html'
    context_object_name = 'internships'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Internship.objects.filter(is_active=True).select_related(
            'supervisor', 'created_by'
        ).prefetch_related('skill_requirements__skill')
        
        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(title__icontains=search) |
                models.Q(description__icontains=search) |
                models.Q(department__icontains=search) |
                models.Q(location__icontains=search)
            )
        
        # Filter by type
        internship_type = self.request.GET.get('type')
        if internship_type:
            queryset = queryset.filter(internship_type=internship_type)
        
        # Filter by location
        location = self.request.GET.get('location')
        if location:
            queryset = queryset.filter(location__icontains=location)
        
        # Filter by department
        department = self.request.GET.get('department')
        if department:
            queryset = queryset.filter(department__icontains=department)
        
        # Order by featured first, then by creation date
        return queryset.order_by('-is_featured', '-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add filter options
        context['types'] = Internship.Type.choices
        context['locations'] = Internship.objects.filter(
            is_active=True
        ).values_list('location', flat=True).distinct()
        context['departments'] = Internship.objects.filter(
            is_active=True
        ).values_list('department', flat=True).distinct()
        
        # Current filter values
        context['current_search'] = self.request.GET.get('search', '')
        context['current_type'] = self.request.GET.get('type', '')
        context['current_location'] = self.request.GET.get('location', '')
        context['current_department'] = self.request.GET.get('department', '')
        
        # Statistics
        context['total_internships'] = Internship.objects.filter(is_active=True).count()
        context['featured_internships'] = Internship.objects.filter(
            is_active=True, is_featured=True
        ).count()
        
        return context


class InternshipDetailView(DetailView):
    """
    Public view to see internship details
    """
    model = Internship
    template_name = 'internships/detail.html'
    context_object_name = 'internship'
    
    def get_queryset(self):
        return Internship.objects.filter(is_active=True).select_related(
            'supervisor', 'created_by'
        ).prefetch_related('skill_requirements__skill')


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin to ensure only admin users can access views
    """
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.can_access_admin()


class InternshipManageView(AdminRequiredMixin, ListView):
    """
    Admin view to manage internships
    """
    model = Internship
    template_name = 'internships/manage.html'
    context_object_name = 'internships'
    paginate_by = 20
    
    def get_queryset(self):
        return Internship.objects.select_related(
            'supervisor', 'created_by'
        ).order_by('-created_at')


class InternshipCreateView(AdminRequiredMixin, CreateView):
    """
    Admin view to create new internships
    """
    model = Internship
    form_class = InternshipForm
    template_name = 'internships/create.html'
    success_url = reverse_lazy('internships:manage')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(
            self.request,
            f'Internship "{form.instance.title}" has been created successfully!'
        )
        return super().form_valid(form)


class InternshipUpdateView(AdminRequiredMixin, UpdateView):
    """
    Admin view to edit internships
    """
    model = Internship
    form_class = InternshipForm
    template_name = 'internships/edit.html'
    success_url = reverse_lazy('internships:manage')
    
    def form_valid(self, form):
        messages.success(
            self.request,
            f'Internship "{form.instance.title}" has been updated successfully!'
        )
        return super().form_valid(form)


class InternshipDeleteView(AdminRequiredMixin, DeleteView):
    """
    Admin view to delete internships
    """
    model = Internship
    template_name = 'internships/delete.html'
    success_url = reverse_lazy('internships:manage')
    
    def delete(self, request, *args, **kwargs):
        internship = self.get_object()
        messages.success(
            request,
            f'Internship "{internship.title}" has been deleted successfully!'
        )
        return super().delete(request, *args, **kwargs)
