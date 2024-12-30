# auth/middleware.py
from django.shortcuts import redirect

class AppwriteAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if there's an Appwrite session
        appwrite_session = request.session.get('appwrite_session')
        request.user_authenticated = appwrite_session is not None

        response = self.get_response(request)
        return response
