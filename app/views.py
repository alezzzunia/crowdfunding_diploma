# app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Q, Sum
from django.contrib import messages
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden, JsonResponse
from django.urls import reverse

from .models import Project, CustomUser, Donation, ProjectMedia, ChatMessage
from .forms import (
    CustomUserCreationForm, ProjectForm, ProjectMediaForm, 
    DonationForm, ChatMessageForm
)

def index(request):
    """Головна сторінка з популярними проектами"""
    latest_projects = Project.objects.filter(status='active').order_by('-created_at')[:6]
    return render(request, 'app/index.html', {
        'latest_projects': latest_projects,
        'title': _('Головна сторінка')
    })

def register(request):
    """Реєстрація нового користувача"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, _('Реєстрація успішна!'))
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'app/register.html', {
        'form': form,
        'title': _('Реєстрація')
    })

@login_required
def profile(request):
    """Профіль користувача"""
    user_projects = Project.objects.filter(author=request.user)
    user_donations = Donation.objects.filter(investor=request.user)
    
    return render(request, 'app/profile.html', {
        'user_projects': user_projects,
        'user_donations': user_donations,
        'title': _('Мій профіль')
    })

def project_catalog(request):
    """Каталог проектів з пошуком та фільтрацією"""
    projects = Project.objects.all()
    
    # Пошук
    search_query = request.GET.get('search', '')
    if search_query:
        projects = projects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__icontains=search_query)
        )
    
    # Фільтрація за статусом
    status_filter = request.GET.get('status', '')
    if status_filter:
        projects = projects.filter(status=status_filter)
    
    # Фільтрація за категорією
    category_filter = request.GET.get('category', '')
    if category_filter:
        projects = projects.filter(category=category_filter)
    
    # Сортування
    sort_by = request.GET.get('sort_by', '-created_at')
    projects = projects.order_by(sort_by)
    
    # Пагінація
    paginator = Paginator(projects, 12)  # 12 проектів на сторінку
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Унікальні категорії для фільтра
    categories = Project.objects.values_list('category', flat=True).distinct()
    
    return render(request, 'app/projects/catalog.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'category_filter': category_filter,
        'sort_by': sort_by,
        'categories': categories,
        'title': _('Каталог проектів')
    })

def project_detail(request, project_id):
    """Детальна сторінка проекту"""
    project = get_object_or_404(Project, id=project_id)
    
    # Отримання всіх медіа-файлів проекту
    media_items = project.media.all()
    
    # Отримання донатів
    donations = project.donations.all().order_by('-created_at')
    
    # Пошук та фільтрація донатів
    search_query = request.GET.get('donor_search', '')
    if search_query:
        donations = donations.filter(
            Q(investor__username__icontains=search_query) |
            Q(investor__first_name__icontains=search_query) |
            Q(investor__last_name__icontains=search_query)
        )
    
    # Сортування донатів
    sort_by = request.GET.get('donor_sort', '-created_at')
    donations = donations.order_by(sort_by)
    
    # Пагінація донатів
    paginator = Paginator(donations, 10)  # 10 донатів на сторінку
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Форма для донату
    donation_form = DonationForm()
    
    return render(request, 'app/projects/detail.html', {
        'project': project,
        'media_items': media_items,
        'page_obj': page_obj,
        'donation_form': donation_form,
        'search_query': search_query,
        'sort_by': sort_by,
        'title': project.title
    })

@login_required
def project_create(request):
    """Створення нового проекту"""
    if not request.user.is_author() and not request.user.is_project_admin():
        messages.error(request, _('Тільки автори можуть створювати проекти.'))
        return redirect('home')
    
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        media_form = ProjectMediaForm(request.POST, request.FILES)
        
        if project_form.is_valid():
            project = project_form.save(commit=False)
            project.author = request.user
            project.save()
            
            # Збереження медіа-файлів
            if 'media_type' in request.POST and request.POST.get('media_type'):
                for i in range(len(request.POST.getlist('media_type'))):
                    media_type = request.POST.getlist('media_type')[i]
                    url = request.POST.getlist('url')[i] if 'url' in request.POST and i < len(request.POST.getlist('url')) else None
                    
                    # Перевірка, чи є файл у запиті
                    file = None
                    if 'file' in request.FILES and i < len(request.FILES.getlist('file')):
                        file = request.FILES.getlist('file')[i]
                    
                    if media_type or url or file:
                        ProjectMedia.objects.create(
                            project=project,
                            media_type=media_type,
                            url=url,
                            file=file
                        )
            
            messages.success(request, _('Проект успішно створено!'))
            return redirect('project_detail', project_id=project.id)
    else:
        project_form = ProjectForm()
        media_form = ProjectMediaForm()
    
    return render(request, 'app/projects/create.html', {
        'project_form': project_form,
        'media_form': media_form,
        'title': _('Створення проекту')
    })

@login_required
def project_edit(request, project_id):
    """Редагування проекту"""
    project = get_object_or_404(Project, id=project_id)
    
    # Перевірка прав доступу
    if project.author != request.user and not request.user.is_project_admin():
        messages.error(request, _('Ви не маєте прав для редагування цього проекту.'))
        return redirect('project_detail', project_id=project.id)
    
    if request.method == 'POST':
        project_form = ProjectForm(request.POST, instance=project)
        
        if project_form.is_valid():
            project_form.save()
            
            # Видалення медіа, якщо потрібно
            if 'delete_media' in request.POST:
                for media_id in request.POST.getlist('delete_media'):
                    try:
                        media = ProjectMedia.objects.get(id=media_id)
                        media.delete()
                    except ProjectMedia.DoesNotExist:
                        pass
            
            # Додавання нових медіа
            if 'media_type' in request.POST and request.POST.get('media_type'):
                for i in range(len(request.POST.getlist('media_type'))):
                    media_type = request.POST.getlist('media_type')[i]
                    url = request.POST.getlist('url')[i] if 'url' in request.POST and i < len(request.POST.getlist('url')) else None
                    
                    # Перевірка, чи є файл у запиті
                    file = None
                    if 'file' in request.FILES and i < len(request.FILES.getlist('file')):
                        file = request.FILES.getlist('file')[i]
                    
                    if media_type or url or file:
                        ProjectMedia.objects.create(
                            project=project,
                            media_type=media_type,
                            url=url,
                            file=file
                        )
            
            messages.success(request, _('Проект успішно оновлено!'))
            return redirect('project_detail', project_id=project.id)
    else:
        project_form = ProjectForm(instance=project)
    
    # Отримання всіх медіа-файлів проекту
    media_items = project.media.all()
    
    return render(request, 'app/projects/edit.html', {
        'project': project,
        'project_form': project_form,
        'media_items': media_items,
        'title': _('Редагування проекту')
    })

@login_required
def project_delete(request, project_id):
    """Видалення проекту"""
    project = get_object_or_404(Project, id=project_id)
    
    # Перевірка прав доступу
    if project.author != request.user and not request.user.is_project_admin():
        messages.error(request, _('Ви не маєте прав для видалення цього проекту.'))
        return redirect('project_detail', project_id=project.id)
    
    if request.method == 'POST':
        project.delete()
        messages.success(request, _('Проект успішно видалено!'))
        return redirect('project_catalog')
    
    return render(request, 'app/projects/delete.html', {
        'project': project,
        'title': _('Видалення проекту')
    })

@login_required
def make_donation(request, project_id):
    """Зробити донат на проект"""
    project = get_object_or_404(Project, id=project_id)
    
    # Перевірка, чи може користувач донатити
    if not request.user.is_investor() and not request.user.is_project_admin():
        messages.error(request, _('Тільки інвестори можуть робити донати.'))
        return redirect('project_detail', project_id=project.id)
    
    if request.method == 'POST':
        donation_form = DonationForm(request.POST)
        
        if donation_form.is_valid():
            donation = donation_form.save(commit=False)
            donation.investor = request.user
            donation.project = project
            donation.save()
            
            # Оновлення суми проекту
            project.current_amount += donation.amount
            project.save()
            
            messages.success(request, _('Дякуємо за вашу підтримку!'))
            return redirect('project_detail', project_id=project.id)
    else:
        donation_form = DonationForm()
    
    return render(request, 'app/projects/donate.html', {
        'project': project,
        'donation_form': donation_form,
        'title': _('Підтримати проект')
    })

@login_required
def project_chat(request, project_id):
    """Чат проекту"""
    project = get_object_or_404(Project, id=project_id)
    
    # Перевірка прав доступу (автор проекту може спілкуватися з інвесторами)
    is_author = (project.author == request.user)
    is_investor = Donation.objects.filter(project=project, investor=request.user).exists()
    
    if not (is_author or is_investor or request.user.is_project_admin()):
        messages.error(request, _('Тільки автор та інвестори можуть брати участь у чаті.'))
        return redirect('project_detail', project_id=project.id)
    
    # Отримання повідомлень
    messages_list = ChatMessage.objects.filter(project=project).order_by('created_at')
    
    if request.method == 'POST':
        chat_form = ChatMessageForm(request.POST)
        
        if chat_form.is_valid():
            chat_message = chat_form.save(commit=False)
            chat_message.sender = request.user
            chat_message.project = project
            chat_message.save()
            
            return redirect('project_chat', project_id=project.id)
    else:
        chat_form = ChatMessageForm()
    
    return render(request, 'app/chat/messages.html', {
        'project': project,
        'messages_list': messages_list,
        'chat_form': chat_form,
        'is_author': is_author,
        'title': _('Чат проекту')
    })

@login_required
def admin_users(request):
    """Адміністрування користувачів"""
    if not request.user.is_project_admin():
        return HttpResponseForbidden(_('Доступ заборонено'))
    
    users = CustomUser.objects.all()
    
    # Пошук
    search_query = request.GET.get('search', '')
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    # Фільтрація за типом
    user_type = request.GET.get('user_type', '')
    if user_type:
        users = users.filter(user_type=user_type)
    
    # Сортування
    sort_by = request.GET.get('sort_by', 'username')
    users = users.order_by(sort_by)
    
    # Пагінація
    paginator = Paginator(users, 20)  # 20 користувачів на сторінку
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'app/admin/users.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'user_type': user_type,
        'sort_by': sort_by,
        'title': _('Адміністрування користувачів')
    })

@login_required
def admin_ban_user(request, user_id):
    """Заблокувати/розблокувати користувача"""
    if not request.user.is_project_admin():
        return HttpResponseForbidden(_('Доступ заборонено'))
    
    user = get_object_or_404(CustomUser, id=user_id)
    
    # Не можна заблокувати самого себе
    if user == request.user:
        messages.error(request, _('Ви не можете заблокувати самого себе!'))
        return redirect('admin_users')
    
    user.is_active = not user.is_active
    user.save()
    
    if user.is_active:
        messages.success(request, _(f'Користувача {user.username} розблоковано.'))
    else:
        messages.success(request, _(f'Користувача {user.username} заблоковано.'))
    
    return redirect('admin_users')

@login_required
def make_donation(request, project_id):
    """Зробити донат на проект"""
    project = get_object_or_404(Project, id=project_id)
    
    # Перевірка, чи може користувач донатити
    if not request.user.is_investor() and not request.user.is_project_admin():
        messages.error(request, _('Тільки інвестори можуть робити донати.'))
        return redirect('project_detail', project_id=project.id)
    
    if request.method == 'POST':
        donation_form = DonationForm(request.POST)
        
        if donation_form.is_valid():
            donation = donation_form.save(commit=False)
            donation.investor = request.user
            donation.project = project
            donation.save()
            
            # Оновлення суми проекту
            project.current_amount += donation.amount
            project.save()
            
            messages.success(request, _('Дякуємо за вашу підтримку!'))
            return redirect('project_detail', project_id=project.id)
    else:
        donation_form = DonationForm()
    
    return render(request, 'app/projects/donate.html', {
        'project': project,
        'donation_form': donation_form,
        'title': _('Підтримати проект')
    })

@login_required
def admin_projects(request):
    """Адміністрування проектів"""
    if not request.user.is_project_admin():
        return HttpResponseForbidden(_('Доступ заборонено'))
    
    projects = Project.objects.all()
    
    # Пошук
    search_query = request.GET.get('search', '')
    if search_query:
        projects = projects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(author__username__icontains=search_query)
        )
    
    # Фільтрація за статусом
    status_filter = request.GET.get('status', '')
    if status_filter:
        projects = projects.filter(status=status_filter)
    
    # Сортування
    sort_by = request.GET.get('sort_by', '-created_at')
    projects = projects.order_by(sort_by)
    
    # Пагінація
    paginator = Paginator(projects, 15)  # 15 проектів на сторінку
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'app/admin/projects.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'sort_by': sort_by,
        'title': _('Адміністрування проектів')
    })