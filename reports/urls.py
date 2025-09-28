"""
URL configuration for reports app
"""
from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    # Intern report URLs
    path('', views.ReportListView.as_view(), name='list'),
    path('create/', views.ReportCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ReportDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.ReportUpdateView.as_view(), name='edit'),
    path('<int:pk>/submit/', views.SubmitReportView.as_view(), name='submit'),
    path('<int:pk>/delete/', views.ReportDeleteView.as_view(), name='delete'),
    
    # Supervisor review URLs
    path('review/', views.SupervisorReportListView.as_view(), name='supervisor_list'),
    path('review/<int:pk>/', views.ReviewReportView.as_view(), name='review'),
    path('review/<int:pk>/complete/', views.CompleteReviewView.as_view(), name='complete_review'),
    
    # Evaluation URLs
    path('evaluations/', views.EvaluationListView.as_view(), name='evaluation_list'),
    path('evaluations/create/', views.EvaluationCreateView.as_view(), name='evaluation_create'),
    path('evaluations/<int:pk>/', views.EvaluationDetailView.as_view(), name='evaluation_detail'),
    path('evaluations/<int:pk>/edit/', views.EvaluationUpdateView.as_view(), name='evaluation_edit'),
]
