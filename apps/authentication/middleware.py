# TALENTNEXT/apps/authentication/middleware.py

from django.shortcuts import redirect
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

class ForcePasswordChangeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.user.role == 'candidate':
            logger.info(f"Middleware: User {request.user.username} is authenticated and is_first_login: {request.user.is_first_login}")
            if request.user.is_first_login:
                logger.info(f"Middleware: Redirecting {request.user.username} to updatepass.")
                if request.path not in [reverse('authentication:updatepass'), reverse('authentication:update_pass_done')]:
                    return redirect('authentication:updatepass')  # Use the correct namespaced URL
        return self.get_response(request)