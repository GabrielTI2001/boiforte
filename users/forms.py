from django import forms
from django.db import models
from administrator.models import Allowed_Emails
from .models import Profile
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, EmailValidator
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
import uuid, os
from PIL import Image

class Profileform(forms.ModelForm): 
    job_function = forms.CharField(
        label='Função', max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-alt'}))
        
    cpf =  forms.CharField(
        label='CPF',
        validators=[RegexValidator(r'(^\d{3}\.\d{3}\.\d{3}\-\d{2}$)', message='Formato CPF inválido!')],
        widget=forms.TextInput(attrs={'class': 'form-control form-control-alt'}))
    
    bio = forms.CharField(
        label='Bio',
        required=False,
        widget=forms.Textarea(attrs={'cols': 6, 'rows': 4, 'class': 'form-control form-control-alt'}))
    
    birthday = forms.DateField(
        label='Data Nascimento',
        required=False,
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control form-control-alt'}))
        
    avatar = forms.FileField(
        label='Escolha seu novo avatar', required=False,
        widget=forms.FileInput(attrs={'class': 'form-control form-control-alt'}))
    
    def clean_avatar(self):
        if 'avatar' in self.files:
            avatar = self.cleaned_data.get('avatar')

            try:
                img = Image.open(avatar)
                img.verify()  # This verifies that it's an image
            except:
                raise forms.ValidationError('Arquivo não é uma imagem válida!')
            
            extension = os.path.splitext(avatar.name)[1]
            avatar.name = f"avatar-{str(uuid.uuid4()).replace('-', '')}{extension}"
            return avatar
        else:
            return None
    
    class Meta:
        model = Profile
        exclude = ('user', 'created_at', 'updated_at')


class Userform(forms.ModelForm):
    first_name = forms.CharField(
        label='Nome', max_length=50, min_length=3,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-alt'}))
    
    last_name = forms.CharField(
        label='Sobrenome', max_length=50, min_length=3,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-alt'}))
    
    username = forms.CharField(
        label='Usuário', max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-alt'}))
    
    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'username')


class formEmails(forms.ModelForm):
    email = forms.EmailField(
        max_length=254, required=True, label='Novo E-mail Autorizado',
        widget= forms.TextInput(attrs={'placeholder': 'Email'}))
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if Allowed_Emails.objects.filter(email=email).exists():
            raise forms.ValidationError('E-mail já autorizado!')
        else:
            return email

    class Meta:
        model = Allowed_Emails
        fields = ('email',)
