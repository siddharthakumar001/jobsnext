# TALENTNEXT/apps/candidate/views.py

from apps.common.decorators import role_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from apps.job.models import Application  # Assuming Document is a model for storing uploaded docs
from apps.candidate.models import Document 
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import logging



User = get_user_model()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@role_required('candidate')
@login_required
def candidate_dashboard(request):
    return render(request, 'candidate/dashboard.html')

@role_required('candidate')
@login_required
def candidate_profile(request):
    user = request.user
    if request.method == 'POST':
        # Update candidate details
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.username = request.POST.get('username')
        user.save()

        # Handle multiple file uploads (CVs and IDs)
        files = request.FILES.getlist('cvs') + request.FILES.getlist('ids')
        for file in files:
            # Ensure file is either CV or ID
            doc_type = 'cv' if file.name.endswith(('.pdf', '.doc', '.docx')) else 'id'
            # Limit to 10 documents for CVs and IDs
            if Document.objects.filter(user=user, doc_type=doc_type).count() >= 10:
                messages.error(request, f'You can only upload up to 10 {doc_type.upper()} documents.')
                continue
            
            # Check for existing document with the same file name
            if Document.objects.filter(user=user, file=file.name, doc_type=doc_type).exists():
                messages.warning(request, f'Document "{file.name}" is already uploaded.')
                continue
            
            doc = Document(user=user, file=file, doc_type=doc_type)
            doc.save()
        
        messages.success(request, 'Profile updated successfully.')
        return redirect('candidate:candidate_profile')
    
    # Fetch uploaded documents from the Document model
    uploaded_docs = Document.objects.filter(user=user)

    # Fetch applications and their associated resumes
    applications = Application.objects.filter(candidate=user)
    for application in applications:
        if application.resume:
            # Check if the resume is already uploaded
            if not uploaded_docs.filter(file=application.resume.name).exists():
                # Create a new Document entry if it doesn't exist
                uploaded_docs = uploaded_docs | Document.objects.filter(user=user, file=application.resume.name)
    
    logger.debug(f"Uploaded Documents: {list(uploaded_docs.values_list('file', flat=True))}")

    return render(request, 'candidate/profile/myprofile.html', {'user': user, 'uploaded_docs': uploaded_docs})

# Function to delete a document
@role_required('candidate')
@login_required
def delete_document(request, doc_id):
    doc = get_object_or_404(Document, id=doc_id, user=request.user)
    doc.delete()
    messages.success(request, 'Document deleted successfully.')
    return redirect('candidate:candidate_profile')

@role_required('candidate')
@login_required
def my_jobs_status(request):
    candidate = request.user
    # Ensure you filter applications by candidate
    applied_jobs = Application.objects.filter(candidate=candidate).select_related('job')
    
    return render(request, 'candidate/my_jobs_status.html', {'applied_jobs': applied_jobs})