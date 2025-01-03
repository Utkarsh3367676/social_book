from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), 
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('forgot-password/',views.forgot_password,name='forgot_password'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('authors-and-sellers/', views.authors_and_sellers_view, name='authors_and_sellers'),

]
