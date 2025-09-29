"""
Views for accounts app
"""
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import User, Profile
from .forms import ProfileForm


class CustomLoginView(LoginView):
    """
    Custom login view with additional checks
    """
    template_name = 'accounts/login.html'
    redirect_authenticated_user = False  # Changed to False to prevent conflicts
    
    def get_success_url(self):
        """Redirect based on user role after successful login"""
        user = self.request.user
        
        if user.is_admin:
            return reverse_lazy('dashboard:admin')
        elif user.is_supervisor:
            return reverse_lazy('dashboard:supervisor')
        elif user.is_intern:
            return reverse_lazy('dashboard:intern')
        else:
            return reverse_lazy('accounts:profile')
    
    def form_valid(self, form):
        """Check if user is approved before allowing login"""
        user = form.get_user()
        if not user.is_approved and not user.is_superuser:
            messages.error(
                self.request,
                'Your account is pending approval. Please contact the administrator.'
            )
            return self.form_invalid(form)
        
        messages.success(
            self.request,
            f'Welcome back, {user.get_full_name()}!'
        )
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, DetailView):
    """
    User profile view
    """
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'user'
    
    def get_object(self):
        return self.request.user


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """
    Edit user profile
    """
    model = Profile
    form_class = ProfileForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile
    
    def form_valid(self, form):
        messages.success(
            self.request,
            'Your profile has been updated successfully!'
        )
        return super().form_valid(form)
