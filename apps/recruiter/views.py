# TALENTNEXT/apps/recruiter/views.py

from django.shortcuts import render, redirect, get_object_or_404
from apps.common.decorators import role_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from apps.job.models import Job, Application
from django.core.paginator import Paginator
from .forms import JobForm

User = get_user_model()

@role_required('recruiter')
@login_required
def recruiter_dashboard(request):
    return render(request, 'recruiter/dashboard.html')

@role_required('recruiter')
@login_required
def recruiter_profile(request):
    user = request.user
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.username = request.POST.get('username')
        user.save()
        messages.success(request, 'Your profile has been updated successfully.')
        return redirect('recruiter:recruiter_profile')  # Use namespaced URL
    return render(request, 'recruiter/profile/myprofile.html', {'user': user})

@role_required('recruiter')
@login_required
def job_listing(request):
    status_filter = request.GET.get('status', None)  # Get the status filter from the query params
    jobs = Job.objects.filter(recruiter=request.user).order_by('-created_at')

    # Apply the status filter if it's set
    if status_filter:
        jobs = jobs.filter(status=status_filter)

    paginator = Paginator(jobs, 10)  # 10 jobs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'recruiter/job/job.html', {'jobs': page_obj})

@role_required('recruiter')
@login_required
def create_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user  # Assign recruiter
            job.status = 'draft'  # Default status is draft
            job.save()

            messages.success(request, 'Job created successfully!')
            return redirect('recruiter:job_listing')
        else:
            # If form is not valid, render the page with error messages
            messages.error(request, 'Please correct the errors below.')
    else:
        form = JobForm()

    return render(request, 'recruiter/job/newjob.html', {'form': form})

@role_required('recruiter')
@login_required
def job_details(request, job_id):
    job = get_object_or_404(Job, id=job_id, recruiter=request.user)

    if request.method == 'POST':
        # Detect which button was clicked
        if 'publish_job' in request.POST:
            # Handle Publish Job action
            if job.status != 'draft':
                messages.error(request, 'Only jobs with status "Draft" can be published.')
            else:
                job.status = 'published'
                job.save()
                messages.success(request, 'Job published successfully!')
        elif 'save_changes' in request.POST:
            # Handle Save Changes action
            form = JobForm(request.POST, instance=job, job_status=job.status)
            if form.is_valid():
                new_status = form.cleaned_data['status']
                if job.status == 'published' and new_status not in ['published', 'closed']:
                    messages.error(request, 'Published jobs can only be closed.')
                else:
                    form.save()
                    messages.success(request, 'Job updated successfully!')
            else:
                messages.error(request, 'Please correct the errors below.')
        else:
            messages.error(request, 'Invalid action. Please try again.')

        return redirect('recruiter:job_details', job_id=job.id)  # Use namespaced URL
    else:
        form = JobForm(instance=job, job_status=job.status)

    # Fetch candidates who applied for this job
    applications = job.applications.all().order_by('-applied_at')
    paginator = Paginator(applications, 10)  # 10 applications per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'job': job,
        'applications': page_obj,
        'form': form,
    }
    return render(request, 'recruiter/job/job_details.html', context)

    # Fetch candidates who applied for this job
    applications = job.applications.all().order_by('-applied_at')
    paginator = Paginator(applications, 10)  # 10 applications per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'job': job,
        'applications': page_obj,
        'form': form,
    }
    return render(request, 'recruiter/job/job_details.html', context)

@role_required('recruiter')
@login_required
def view_application(request, application_id):
    # Fetch the application and related job
    application = get_object_or_404(Application, id=application_id, job__recruiter=request.user)
    
    if request.method == 'POST':
        # Handle form submission for status change
        new_status = request.POST.get('status')
        if new_status and new_status in dict(application.STATUS_CHOICES):
            application.status = new_status
            application.save()
            messages.success(request, 'The application status has been updated successfully!')
        else:
            messages.error(request, 'Invalid status selected.')

    context = {
        'application': application,
    }
    return render(request, 'recruiter/job/view_application.html', context)