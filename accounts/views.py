from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from .models import CustomUser  # Import your CustomUser model


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


from django.shortcuts import render
from .models import CustomUser
from django_filters import FilterSet, BooleanFilter  # Import specific classes

# Then modify your filter class to use these imports:
class CustomUserFilter(FilterSet):
    public_visibility = BooleanFilter(field_name="public_visibility", label="Public Visibility", lookup_expr='exact')

    class Meta:
        model = CustomUser
        fields = ['public_visibility']
        
        
def authors_and_sellers_view(request):
    # Apply the filter based on GET parameters
    user_filter = CustomUserFilter(request.GET, queryset=CustomUser.objects.all())
    
    # Pass the filtered users to the template
    return render(request, 'accounts/authors_and_sellers.html', {'filter': user_filter})

    
