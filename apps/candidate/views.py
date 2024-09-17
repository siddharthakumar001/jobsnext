from django.shortcuts import render
from apps.common.decorators import role_required

@role_required('candidate')
def candidate_dashboard(request):
    return render(request, 'candidate/dashboard.html')