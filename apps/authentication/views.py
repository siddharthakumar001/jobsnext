# TALENTNEXT/apps/authentication/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CandidateSignUpForm, SignInForm  # Use the correct form
from .models import User
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
import logging
# for debugging db query
from django.db import connection
from django.db import transaction


logger = logging.getLogger(__name__)

# Recruiter Signup View
def register_recruiter_view(request):
    if request.method == 'POST':
        form = CandidateSignUpForm(request.POST)  # Adjust form name for recruiters if needed
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'recruiter'  # Automatically set role
            user.save()
            messages.success(request, 'Account created successfully. Please sign in.')
            return redirect('signin')
    else:
        form = CandidateSignUpForm()  # Adjust form name for recruiters if needed
    return render(request, 'authentication/register_recruiter.html', {'form': form})

# Candidate Signup View
def register_candidate_view(request):
    if request.method == 'POST':
        form = CandidateSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'candidate'  # Automatically set role
            user.save()
            messages.success(request, 'Account created successfully. Please sign in.')
            return redirect('signin')
    else:
        form = CandidateSignUpForm()
    return render(request, 'authentication/register_candidate.html', {'form': form})

# Admin Signup View
def register_admin_view(request):
    if request.method == 'POST':
        form = CandidateSignUpForm(request.POST)  # Adjust form name for admin if needed
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'admin'  # Automatically set role
            user.save()
            messages.success(request, 'Account created successfully. Please sign in.')
            return redirect('signin')
    else:
        form = CandidateSignUpForm()  # Adjust form name for admin if needed
    return render(request, 'authentication/register_admin.html', {'form': form})

def signin_view(request):
    logger.info("Sign-in view accessed")
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('user')
            login(request, user)

            # Redirect to password change form if it's the user's first login (candidates only)
            if user.role == 'candidate' and user.is_first_login:
                logger.info(f"User {user.username} has is_first_login=True. Redirecting to updatepass.")
                return redirect('updatepass')  # No namespace needed as it's defined in authentication app

            # Role-based dashboard redirection with namespaces
            if user.role == 'recruiter':
                return redirect('recruiter:recruiter_dashboard')
            elif user.role == 'candidate':
                return redirect('candidate:candidate_dashboard')
            elif user.role == 'admin':
                return redirect('admin:admin_dashboard')  # Ensure admin app is namespaced similarly
    else:
        form = SignInForm()

    return render(request, 'authentication/signin.html', {'form': form})



# Sign-out View
def signout_view(request):
    logout(request)
    return redirect('authentication:signin')

class CustomPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('update_pass_done')
    template_name = 'authentication/update_pass.html'

    def form_valid(self, form):
        logger.info("CustomPasswordChangeView: form_valid called")
        user = self.request.user
        
        # Log before updating the flag
        logger.info(f"User {user.username} is attempting to change their password.")
        
        # Update is_first_login flag
        user.is_first_login = False  # Setting the flag to False
        user.save(update_fields=['is_first_login'])  # Ensure the specific field is updated
        
        # Check the flag after saving
        logger.info(f"Updated is_first_login flag for {user.username}: {user.is_first_login}")
        
        # Log the SQL queries to check the update
        logger.info("SQL queries executed:")
        for query in connection.queries:
            logger.info(query['sql'])
        
        # Flush the session to clear all session data
        self.request.session.flush()
        logger.info(f"Session flushed for user {user.username}.")
        
        # Log out the user to invalidate the session
        logout(self.request)
        logger.info(f"User {user.username} has been logged out after password change.")
        
        return super().form_valid(form)

class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'authentication/update_pass_done.html'

    def get(self, request, *args, **kwargs):
        # Log the user out if they are still authenticated
        if request.user.is_authenticated:
            logger.info(f"Logging out user {request.user.username} after password change.")
            logout(request)

        # Inform the user to log in again
        messages.success(request, "Your password has been successfully changed. Please log in again.")
        return render(request, self.template_name)
    