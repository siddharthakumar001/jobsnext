#TALENTNEXT/apps/job/tasks.py

import dramatiq
from django.core.mail import send_mail
from django.conf import settings
import requests
import os
from dramatiq.brokers.rabbitmq import RabbitmqBroker

# No need to initialize broker here, global broker url is set in settings.py

broker = RabbitmqBroker(url=os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/%2F"))
# Set the broker to be used globally
dramatiq.set_broker(broker)
@dramatiq.actor
def process_job_document_task(document_path):
    """
    Processes a job document (e.g., Word or PDF) using the OpenAI API to create a job.
    """
    try:
        # Example: Read the document content
        with open(document_path, 'rb') as file:
            content = file.read()

        # Call OpenAI API (replace with actual API call)
        headers = {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "model": "text-davinci-003",
            "prompt": f"Create a job posting from the following document:\n\n{content.decode('utf-8')}",
            "max_tokens": 150,
        }
        response = requests.post("https://api.openai.com/v1/completions", headers=headers, json=data)
        response.raise_for_status()
        job_description = response.json()['choices'][0]['text'].strip()

        # Save the generated job description to the database
        from .models import Job

        # Create a new job
        job = Job.objects.create(
            title="Generated Job Title",  # Replace with dynamic title if available
            description=job_description,
            recruiter_id=1,  # Replace with actual recruiter ID or logic
            status='draft',
        )
        print(f"Job created: {job.title}")

    except Exception as e:
        print(f"Failed to process document {document_path}: {e}")
