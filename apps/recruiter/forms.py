# TALENTNEXT/apps/recruiter/forms.py

from django import forms
from apps.job.models import Job  # Import Job model from the job app
import re

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the job title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Provide a detailed job description', 'rows': 4}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')

        # Check if title contains only alphabetic characters and spaces
        if not re.match(r'^[A-Za-z\s]+$', title):
            raise forms.ValidationError("The title should contain only alphabetic characters and spaces.")
        
        # Ensure the title is between 5 and 100 characters
        if len(title) < 5 or len(title) > 100:
            raise forms.ValidationError("The title must be between 5 and 100 characters.")
        
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description')

        # Ensure the description is between 20 and 1000 characters
        if len(description) < 20 or len(description) > 1000:
            raise forms.ValidationError("The description must be between 20 and 1000 characters.")
        
        return description

    def __init__(self, *args, **kwargs):
        job_status = kwargs.pop('job_status', None)
        super(JobForm, self).__init__(*args, **kwargs)
        if job_status == 'published':
            # If job is published, restrict status options to 'closed' only
            self.fields['status'].choices = [
                ('published', 'Published'),
                ('closed', 'Closed'),
            ]
        else:
            # Allow all status options
            self.fields['status'].choices = [
                ('draft', 'Draft'),
                ('published', 'Published'),
                ('closed', 'Closed'),
            ]