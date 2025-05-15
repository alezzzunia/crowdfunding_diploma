# app/urls.py

from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .forms import CustomAuthenticationForm

urlpatterns = [
    # Головна сторінка
    path('', views.index, name='home'),
    
    # Аутентифікація
    path('login/', LoginView.as_view(
        template_name='app/login.html',
        authentication_form=CustomAuthenticationForm
    ), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    
    # Профіль
    path('profile/', views.profile, name='profile'),
    
    # Проекти
    path('projects/', views.project_catalog, name='project_catalog'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path('projects/<int:project_id>/edit/', views.project_edit, name='project_edit'),
    path('projects/<int:project_id>/delete/', views.project_delete, name='project_delete'),
    
    # Донати
    path('projects/<int:project_id>/donate/', views.make_donation, name='make_donation'),
    
    # Чат
    path('projects/<int:project_id>/chat/', views.project_chat, name='project_chat'),
    
    # Адміністрування
    path('admin/users/', views.admin_users, name='admin_users'),
    path('admin/users/<int:user_id>/ban/', views.admin_ban_user, name='admin_ban_user'),
    path('admin/projects/', views.admin_projects, name='admin_projects'),
]