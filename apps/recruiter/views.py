from django.shortcuts import render
from apps.common.decorators import role_required  # Import the decorator

def recruiter_dashboard(request):
    return render(request, 'recruiter/dashboard.html')

@role_required('recruiter')
def recruiter_dashboard(request):
    return render(request, 'recruiter/dashboard.html')


