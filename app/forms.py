# app/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Project, Donation, ProjectMedia, ChatMessage

class CustomUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(
        choices=CustomUser.USER_TYPES,
        label=_('Тип користувача'),
        widget=forms.RadioSelect
    )
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'user_type', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Логін')})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Пароль')})

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'description', 'goal_amount', 'deadline', 'category')
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class ProjectMediaForm(forms.ModelForm):
    class Meta:
        model = ProjectMedia
        fields = ('media_type', 'file', 'url')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['media_type'].widget.attrs.update({'class': 'form-control'})
        self.fields['file'].widget.attrs.update({'class': 'form-control'})
        self.fields['url'].widget.attrs.update({'class': 'form-control'})
        
    def clean(self):
        cleaned_data = super().clean()
        media_type = cleaned_data.get('media_type')
        file = cleaned_data.get('file')
        url = cleaned_data.get('url')
        
        if media_type == 'document' and not file:
            self.add_error('file', _('Для документів необхідно додати файл.'))
            
        if media_type == 'video' and not (file or url):
            self.add_error('url', _('Для відео потрібно додати URL або файл.'))
            
        if media_type == 'image' and not (file or url):
            self.add_error('file', _('Для зображень потрібно додати файл або URL.'))
            
        return cleaned_data

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ('amount', 'comment')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].widget.attrs.update({'class': 'form-control', 'min': '0.01', 'step': '0.01'})
        self.fields['comment'].widget.attrs.update({'class': 'form-control', 'rows': '3'})

class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ('message',)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message'].widget.attrs.update({'class': 'form-control', 'rows': '2', 'placeholder': _('Напишіть повідомлення...')})