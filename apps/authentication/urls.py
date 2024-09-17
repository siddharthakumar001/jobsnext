from django.urls import path
from . import views

urlpatterns = [
    path('signup/recruiter/', views.signup_recruiter_view, name='signup_recruiter'),
    path('register/candidate/', views.register_candidate_view, name='register_candidate'),
    path('signup/admin/', views.signup_admin_view, name='signup_admin'),
    path('signin/', views.signin_view, name='signin'),
    path('signout/', views.signout_view, name='signout'),
]