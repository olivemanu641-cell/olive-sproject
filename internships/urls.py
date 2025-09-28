"""
URL configuration for internships app
"""
from django.urls import path
from . import views

app_name = 'internships'

urlpatterns = [
    # Public internship browsing
    path('', views.InternshipListView.as_view(), name='list'),
    path('<int:pk>/', views.InternshipDetailView.as_view(), name='detail'),
    
    # Admin internship management
    path('manage/', views.InternshipManageView.as_view(), name='manage'),
    path('create/', views.InternshipCreateView.as_view(), name='create'),
    path('edit/<int:pk>/', views.InternshipUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', views.InternshipDeleteView.as_view(), name='delete'),
]
