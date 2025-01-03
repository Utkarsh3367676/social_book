from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect



def index(request):
    return render(request, 'index.html') 

def login_view(request):
    return render(request, 'accounts/login.html')

def register_view(request):
    return render(request, 'accounts/register.html')


def forgot_password(request):
    return render(request,'accounts/forgot-password.html')

def dashboard(request):
    return render(request,'accounts/dashboard.html')


def logout_view(request):
    # Logout logic
    logout(request)
    return redirect('login')


