from django.db import models
from apps.authentication.models import User  # Import User model

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'recruiter'})  # Limit to users with recruiter role
    is_internal = models.BooleanField(default=True)
    status = models.CharField(max_length=10, choices=[('draft', 'Draft'), ('published', 'Published'), ('closed', 'Closed'), ('archived', 'Archived')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

