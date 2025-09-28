"""
URL configuration for applications app
"""
from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    # Public application URLs
    path('apply/', views.ApplicationCreateView.as_view(), name='apply'),
    path('apply/<int:internship_id>/', views.ApplicationCreateView.as_view(), name='apply_specific'),
    path('success/', views.ApplicationSuccessView.as_view(), name='success'),
    
    # Admin application management URLs
    path('manage/', views.ApplicationListView.as_view(), name='manage'),
    path('detail/<int:pk>/', views.ApplicationDetailView.as_view(), name='detail'),
    path('approve/<int:pk>/', views.ApproveApplicationView.as_view(), name='approve'),
    path('reject/<int:pk>/', views.RejectApplicationView.as_view(), name='reject'),
    path('create-intern/<int:pk>/', views.CreateInternAccountView.as_view(), name='create_intern'),
]
