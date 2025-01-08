from django.urls import path, include
from . import views
from .views import UploadedFilesView  # Import UploadedFilesView
from djoser.views import TokenDestroyView  # Import TokenDestroyView from djoser

urlpatterns = [
    # Custom Web Views
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('authors-and-sellers/', views.authors_and_sellers_view, name='authors_and_sellers'),
    path('upload-books/', views.upload_books_view, name='upload_books'),
    path('uploaded-files/', views.uploaded_files_view, name='uploaded_files'),
    path('my-books/', views.my_books_view, name='my_books'),  # "My Books" view

    # Custom API Views
    path('api/uploaded-files/', UploadedFilesView.as_view(), name='api_uploaded_files'),  # Custom API for uploaded files
    path('auth/token/logout/', TokenDestroyView.as_view(), name='auth_token_logout'),  # Logout for token-based auth

    # Djoser Routes (Place them last to avoid overriding)
    path('api/auth/', include('djoser.urls')),  # Includes default Djoser routes
    # path('api/auth/token/', include('djoser.urls.authtoken')),  # Routes for token-based authentication
]


