from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/recruiter/', views.register_recruiter_view, name='register_recruiter'),
    path('register/candidate/', views.register_candidate_view, name='register_candidate'),
    path('register/admin/', views.register_admin_view, name='register_admin'),
    path('signin/', views.signin_view, name='signin'),
    path('signout/', views.signout_view, name='signout'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    # Password Change URLs
    path('updatepass/', views.CustomPasswordChangeView.as_view(), name='updatepass'),
    path('updatepass/done/', views.CustomPasswordChangeDoneView.as_view(), name='update_pass_done'),  # Use custom view

]
