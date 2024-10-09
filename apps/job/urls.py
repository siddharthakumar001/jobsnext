# apps/job/urls.py

from django.urls import path
from . import views

app_name = 'job'

urlpatterns = [
    path('recruiter/<str:recruiter_username>/jobs/', views.recruiter_jobs, name='recruiter_jobs'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
]