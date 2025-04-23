from django.shortcuts import redirect
from django.contrib import messages

class UserTypeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.path.startswith('/buyer/') and request.user.user_type != 'buyer':
                messages.error(request, "You do not have permission to access this page.")
                return redirect('home')  # Or another suitable redirect
            elif request.path.startswith('/farmer/') and request.user.user_type != 'farmer':  # Corrected path
                messages.error(request, "You do not have permission to access this page.")
                return redirect('home')  # Or another suitable redirect
        response = self.get_response(request)
        return response