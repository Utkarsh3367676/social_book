from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from .models import CustomUser  
from django.contrib.auth.decorators import login_required
from .models import UploadedFile
from django.utils.timezone import now
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect




def index(request):
    return render(request, 'index.html') 


def login_view(request):
    next_url = request.GET.get('next', reverse('dashboard'))  # Use 'reverse' to ensure correct URL

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Check if the next URL is valid
            if next_url.startswith('/'):
                return HttpResponseRedirect(next_url)
            else:
                return redirect('dashboard')  # Fallback to dashboard if 'next' URL is invalid
        else:
            context = {
                'error': 'Invalid username or password',
                'next': next_url,
            }
            return render(request, 'accounts/login.html', context)

    return render(request, 'accounts/login.html', {'next': next_url})

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

    
    
    

@login_required
def upload_books_view(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        visibility = request.POST['visibility']
        cost = request.POST.get('cost', None)
        year_published = request.POST['year_published']
        file = request.FILES['file']

        # Save the uploaded file
        UploadedFile.objects.create(
            user=request.user,
            title=title,
            description=description,
            visibility=visibility,
            cost=cost,
            year_published=year_published,
            file=file
        )
        return redirect('uploaded_files')

    return render(request, 'accounts/upload_books.html', {'current_year': now().year})

@login_required
def uploaded_files_view(request):
    # Fetch files uploaded by the logged-in user
    uploaded_files = UploadedFile.objects.filter(user=request.user)
    return render(request, 'accounts/uploaded_files.html', {'uploaded_files': uploaded_files})

