from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django_filters import FilterSet, BooleanFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from .models import CustomUser, UploadedFile
from .serializers import UploadedFileSerializer
from social_book.db.queries import get_uploaded_files
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods


def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


@ensure_csrf_cookie
def login_view(request):
    next_url = request.GET.get('next', reverse('dashboard'))
    if not next_url.startswith('/'):
        next_url = reverse('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['auth_token'] = str(Token.objects.get_or_create(user=user)[0])

            # Handle AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'redirect_url': next_url})

            return redirect(next_url)
        else:
            error_message = 'Invalid username or password'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': error_message}, status=400)
            return render(request, 'accounts/login.html', {'error': error_message, 'next': next_url})

    if request.user.is_authenticated:
        return redirect('dashboard')

    return render(request, 'accounts/login.html', {'next': next_url})


@login_required
@require_http_methods(["POST"])
def logout_view(request):
    try:
        Token.objects.filter(user=request.user).delete()
    except Exception as e:
        print(f"Error deleting token: {e}")
    finally:
        request.session.flush()

    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html', {'user': request.user})


def register_view(request):
    return render(request, 'accounts/register.html')


def forgot_password(request):
    return render(request, 'accounts/forgot-password.html')


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
    uploaded_files = get_uploaded_files(user_id=request.user.id)
    return render(request, 'accounts/uploaded_files.html', {'uploaded_files': uploaded_files})


# ----------------- API Endpoints -----------------


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_token_view(request):
    """
    API to generate an authentication token for the logged-in user.
    """
    token, _ = Token.objects.get_or_create(user=request.user)
    return Response({'token': token.key}, status=200)


class UploadedFilesView(APIView):
    """
    API to fetch user-uploaded files using token-based authentication.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        files = UploadedFile.objects.filter(user=user)
        serializer = UploadedFileSerializer(files, many=True)
        return Response(serializer.data)


# ----------------- Filters -----------------


class CustomUserFilter(FilterSet):
    public_visibility = BooleanFilter(field_name="public_visibility", label="Public Visibility", lookup_expr='exact')

    class Meta:
        model = CustomUser
        fields = ['public_visibility']


def authors_and_sellers_view(request):
    user_filter = CustomUserFilter(request.GET, queryset=CustomUser.objects.all())
    return render(request, 'accounts/authors_and_sellers.html', {'filter': user_filter})


from django.shortcuts import render
from .models import UploadedFile
from .decorators import my_books_access_required

@my_books_access_required
def my_books_view(request):
    """
    View for 'My Books' where users can view their uploaded files.
    """
    user = request.user
    uploaded_files = UploadedFile.objects.filter(user=user)
    return render(request, 'accounts/my_books.html', {'uploaded_files': uploaded_files})
