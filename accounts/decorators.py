from functools import wraps
from django.shortcuts import redirect
from .models import UploadedFile

def my_books_access_required(view_func):
    """
    Wrapper to check if the user has uploaded files.
    Redirects to 'Upload Books' if no files are found.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return redirect('login')  # Redirect to login if not authenticated

        # Check if user has uploaded files
        if UploadedFile.objects.filter(user=user).exists():
            return view_func(request, *args, **kwargs)  # Allow access
        else:
            return redirect('upload_books')  # Redirect to upload books

    return _wrapped_view
