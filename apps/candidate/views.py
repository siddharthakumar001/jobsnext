# TALENTNEXT/apps/candidate/views.py

from django.shortcuts import render, redirect
from apps.common.decorators import role_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from apps.job.models import Application

User = get_user_model()

@role_required('candidate')
@login_required
def candidate_dashboard(request):
    return render(request, 'candidate/dashboard.html')

@role_required('candidate')
@login_required
def candidate_profile(request):
    user = request.user
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.username = request.POST.get('username')
        user.save()
        messages.success(request, 'Your profile has been updated successfully.')
        return redirect('candidate:candidate_profile')  # Use namespaced URL
    return render(request, 'candidate/profile/myprofile.html', {'user': user})

@role_required('candidate')
@login_required
def my_jobs_status(request):
    candidate = request.user
    # Ensure you filter applications by candidate
    applied_jobs = Application.objects.filter(candidate=candidate).select_related('job')
    
    return render(request, 'candidate/my_jobs_status.html', {'applied_jobs': applied_jobs})