# apps/job/forms.py

from django import forms
from .models import Application
from apps.authentication.models import User  # Assuming your custom User model is in authentication
from .choices import COUNTRY_CODE_CHOICES

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            'first_name',
            'last_name',
            'email',
            'mobile_number',
            'country_code',
            'resume',
            'cover_letter',
            'interested_in_account'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Mobile Number'}),
            'country_code': forms.Select(choices=COUNTRY_CODE_CHOICES, attrs={'class': 'form-control'}),
            'resume': forms.FileInput(attrs={'class': 'form-control'}),
            'cover_letter': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Optional: Your Cover Letter'}),
            'interested_in_account': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        self.job = kwargs.pop('job', None)  # Pass the job when initializing the form
        super(ApplicationForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Check if the email has already applied for this specific job
        if Application.objects.filter(job=self.job, email=email).exists():
            raise forms.ValidationError("You have already applied for this job with this email.")
        return email

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get('mobile_number')
        # Check if the mobile number has already applied for this specific job
        if Application.objects.filter(job=self.job, mobile_number=mobile_number).exists():
            raise forms.ValidationError("You have already applied for this job with this mobile number.")
        return mobile_number