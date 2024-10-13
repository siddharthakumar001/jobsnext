import dramatiq
from django.core.mail import send_mail
from django.conf import settings
import os
from dramatiq.brokers.rabbitmq import RabbitmqBroker

# No need to initialize broker here, global broker url is set in settings.py
broker = RabbitmqBroker(url=os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/%2F"))
# Set the broker to be used globally
dramatiq.set_broker(broker)
@dramatiq.actor
def send_email_task(subject, message, recipient_list):
    """
    Sends an email to the specified recipients.
    """
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            fail_silently=False,
        )
        print(f"Email sent to: {recipient_list}")
    except Exception as e:
        print(f"Failed to send email: {e}")
