# app/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser, Project, ProjectMedia, Donation, ChatMessage

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_active')
    list_filter = ('user_type', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Особиста інформація'), {'fields': ('first_name', 'last_name', 'email', 'profile_image')}),
        (_('Права доступу'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_type', 'groups', 'user_permissions')}),
        (_('Важливі дати'), {'fields': ('last_login', 'date_joined')}),
    )
    
class ProjectMediaInline(admin.TabularInline):
    model = ProjectMedia
    extra = 0

class DonationInline(admin.TabularInline):
    model = Donation
    extra = 0
    readonly_fields = ('created_at',)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'goal_amount', 'current_amount', 'status', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'description', 'author__username')
    readonly_fields = ('current_amount',)
    inlines = [ProjectMediaInline, DonationInline]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('author')

class ProjectMediaAdmin(admin.ModelAdmin):
    list_display = ('project', 'media_type', 'file', 'url')
    list_filter = ('media_type',)
    search_fields = ('project__title',)

class DonationAdmin(admin.ModelAdmin):
    list_display = ('investor', 'project', 'amount', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('investor__username', 'project__title', 'comment')
    readonly_fields = ('created_at',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('investor', 'project')

class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'project', 'created_at', 'message_preview')
    list_filter = ('created_at',)
    search_fields = ('sender__username', 'project__title', 'message')
    readonly_fields = ('created_at',)
    
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = _('Повідомлення')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('sender', 'project')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectMedia, ProjectMediaAdmin)
admin.site.register(Donation, DonationAdmin)
admin.site.register(ChatMessage, ChatMessageAdmin)