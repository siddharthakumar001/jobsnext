from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.candidate_dashboard, name='candidate_dashboard'),
    path('profile/', views.candidate_profile, name='candidate_profile'),  # Profile URL
    path('my-jobs-status/', views.my_jobs_status, name='my_jobs_status'),
]