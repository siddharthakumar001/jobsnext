# TALENTNEXT/apps/recruiter/urls.py

from django.urls import path
from . import views

app_name = 'recruiter'  # Correct namespacing

urlpatterns = [
    path('dashboard/', views.recruiter_dashboard, name='recruiter_dashboard'),
    path('profile/', views.recruiter_profile, name='recruiter_profile'),  # Profile URL
    path('jobs/', views.job_listing, name='job_listing'),
    path('jobs/create/', views.create_job, name='create_job'),
    path('jobs/<int:job_id>/', views.job_details, name='job_details'),
    path('applications/<int:application_id>/', views.view_application, name='view_application'),  # View Application URL
]