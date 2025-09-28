"""
URL configuration for dashboard app
"""
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardHomeView.as_view(), name='home'),
    path('admin/', views.AdminDashboardView.as_view(), name='admin'),
    path('supervisor/', views.SupervisorDashboardView.as_view(), name='supervisor'),
    path('intern/', views.InternDashboardView.as_view(), name='intern'),
]
