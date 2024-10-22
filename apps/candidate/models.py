# TALENTNEXT/apps/candidate/models.py
from django.db import models
from apps.authentication.models import User

class Document(models.Model):
    DOC_TYPE_CHOICES = [
        ('cv', 'CV'),
        ('id', 'ID'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/')
    doc_type = models.CharField(max_length=2, choices=DOC_TYPE_CHOICES)
    
    def __str__(self):
        return f"{self.user.username} - {self.doc_type} - {self.file.name}"