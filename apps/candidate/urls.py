from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.candidate_dashboard, name='candidate_dashboard'),
]