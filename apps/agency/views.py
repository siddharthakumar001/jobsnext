from django.shortcuts import render

# Create your views here.


@role_required('admin')
def admin_dashboard(request):
    return render(request, 'admin/dashboard.html')
