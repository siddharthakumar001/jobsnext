#TALENTNEXT/apps/job/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from .models import Job, Application
from .forms import ApplicationForm
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings

import logging

logger = logging.getLogger(__name__)

User = get_user_model()

def recruiter_jobs(request, recruiter_username):
    recruiter = get_object_or_404(User, username=recruiter_username, role='recruiter')
    jobs = Job.objects.filter(recruiter=recruiter, status='published').order_by('-created_at')
    
    context = {
        'recruiter': recruiter,
        'jobs': jobs,
    }
    return render(request, 'job/recruiter_jobs.html', context)

def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id, status='published')
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES, job=job)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job

            if request.user.is_authenticated and request.user.role == 'candidate':
                # Associate the application with the logged-in user
                application.candidate = request.user
            else:
                # Candidate is applying without being logged in
                application.candidate = None

            application.save()

            # Handle account creation if user chooses to register later
            if application.interested_in_account:
                existing_user = User.objects.filter(email=application.email).first()
                if existing_user:
                    messages.warning(request, 'An account with this email already exists. Please log in to see your applications.')
                else:
                    # Create a new candidate user with a random password
                    random_password = get_random_string(length=12)
                    user = User.objects.create_user(
                        username=application.email,
                        email=application.email,
                        password=random_password,
                        first_name=application.first_name,
                        last_name=application.last_name,
                        mobile_number=application.mobile_number,
                        role='candidate',
                        is_first_login=True  # Candidate needs to change password on first login
                    )
                    user.save()

                    # Send email with random password
                    send_mail(
                        'Your TalentNext Account Password',
                        f"Hello {user.first_name},\n\nYour account has been created on TalentNext.\nYour password is: {random_password}\nPlease log in and change your password.\n\nThank you!",
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                        fail_silently=False,
                    )
                    messages.success(request, 'Your application has been submitted successfully! An account has been created for you. Please check your email for login details.')
                    return redirect('job:job_detail', job_id=job.id)
            else:
                messages.success(request, 'Your application has been submitted successfully!')
                return redirect('job:job_detail', job_id=job.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ApplicationForm(job=job)

    return render(request, 'job/job_detail.html', {'job': job, 'form': form})