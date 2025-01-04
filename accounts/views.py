from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from .models import CustomUser, UploadedFile
from django_filters import FilterSet, BooleanFilter
from social_book.db.queries import get_uploaded_files

def index(request):
    return render(request, 'index.html')


def login_view(request):
    next_url = request.GET.get('next', reverse('dashboard'))

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if next_url.startswith('/'):
                return HttpResponseRedirect(next_url)
            else:
                return redirect('dashboard')  # Fallback if 'next' is invalid
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
    return render(request, 'accounts/forgot-password.html')


@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')


def logout_view(request):
    logout(request)
    return redirect('login')


class CustomUserFilter(FilterSet):
    public_visibility = BooleanFilter(field_name="public_visibility", label="Public Visibility", lookup_expr='exact')

    class Meta:
        model = CustomUser
        fields = ['public_visibility']


def authors_and_sellers_view(request):
    user_filter = CustomUserFilter(request.GET, queryset=CustomUser.objects.all())
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
    # Fetch files for the logged-in user using SQLAlchemy
    uploaded_files = get_uploaded_files(user_id=request.user.id)  # Pass the logged-in user's ID to the function
    return render(request, 'accounts/uploaded_files.html', {'uploaded_files': uploaded_files})
