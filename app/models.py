# app/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('investor', _('Інвестор')),
        ('author', _('Автор')),
        ('admin', _('Адміністратор')),
    )
    user_type = models.CharField(_('Тип користувача'), max_length=10, choices=USER_TYPES, default='investor')
    profile_image = models.ImageField(_('Зображення профілю'), upload_to='profile_images/', null=True, blank=True)
    
    def is_investor(self):
        return self.user_type == 'investor'
    
    def is_author(self):
        return self.user_type == 'author'
    
    def is_project_admin(self):
        return self.user_type == 'admin'
        
    class Meta:
        verbose_name = _('Користувач')
        verbose_name_plural = _('Користувачі')

class Project(models.Model):
    STATUS_CHOICES = (
        ('active', _('Активний')),
        ('completed', _('Завершений')),
        ('canceled', _('Скасований')),
    )
    
    title = models.CharField(_('Назва'), max_length=200)
    description = models.TextField(_('Опис'))
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='projects', verbose_name=_('Автор'))
    goal_amount = models.DecimalField(_('Цільова сума'), max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(_('Зібрана сума'), max_digits=10, decimal_places=2, default=0)
    status = models.CharField(_('Статус'), max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(_('Дата створення'), auto_now_add=True)
    deadline = models.DateTimeField(_('Дедлайн'))
    category = models.CharField(_('Категорія'), max_length=100)
    
    def progress_percentage(self):
        if self.goal_amount == 0:
            return 0
        return int((self.current_amount / self.goal_amount) * 100)
    
    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name = _('Проект')
        verbose_name_plural = _('Проекти')

class ProjectMedia(models.Model):
    MEDIA_TYPES = (
        ('image', _('Зображення')),
        ('video', _('Відео')),
        ('document', _('Документ')),
    )
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='media', verbose_name=_('Проект'))
    media_type = models.CharField(_('Тип медіа'), max_length=10, choices=MEDIA_TYPES)
    file = models.FileField(_('Файл'), upload_to='project_media/', null=True, blank=True)
    url = models.URLField(_('URL'), null=True, blank=True)
    
    def __str__(self):
        return f"{self.project.title} - {self.get_media_type_display()}"
        
    class Meta:
        verbose_name = _('Медіа проекту')
        verbose_name_plural = _('Медіа проектів')

class Donation(models.Model):
    investor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='donations', verbose_name=_('Інвестор'))
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='donations', verbose_name=_('Проект'))
    amount = models.DecimalField(_('Сума'), max_digits=10, decimal_places=2)
    comment = models.TextField(_('Коментар'), blank=True, null=True)
    created_at = models.DateTimeField(_('Дата донату'), auto_now_add=True)
    
    def __str__(self):
        return f"{self.investor.username} - {self.project.title} - {self.amount}"
        
    class Meta:
        verbose_name = _('Донат')
        verbose_name_plural = _('Донати')

class ChatMessage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='messages', verbose_name=_('Проект'))
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages', verbose_name=_('Відправник'))
    message = models.TextField(_('Повідомлення'))
    created_at = models.DateTimeField(_('Дата створення'), auto_now_add=True)
    
    def __str__(self):
        return f"{self.sender.username} - {self.project.title}"
        
    class Meta:
        verbose_name = _('Повідомлення чату')
        verbose_name_plural = _('Повідомлення чату')