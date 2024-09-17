from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CandidateSignUpForm, SignInForm  # Use the correct form
from .models import User

# Recruiter Signup View
def signup_recruiter_view(request):
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
    return render(request, 'authentication/signup_recruiter.html', {'form': form})

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
def signup_admin_view(request):
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
    return render(request, 'authentication/signup_admin.html', {'form': form})

def signin_view(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Role-based redirection after login
                if user.role == 'recruiter':
                    return redirect('recruiter_dashboard')
                elif user.role == 'candidate':
                    return redirect('candidate_dashboard')
                elif user.role == 'admin':
                    return redirect('admin_dashboard')
            else:
                messages.error(request, 'Invalid login credentials')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignInForm()
    return render(request, 'authentication/signin.html', {'form': form})

# Sign-out View
def signout_view(request):
    logout(request)
    return redirect('signin')