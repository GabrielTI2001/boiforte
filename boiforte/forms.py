from django import forms
from allauth.account.forms import LoginForm, ChangePasswordForm, SignupForm, ResetPasswordForm, ResetPasswordKeyForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from administrator.models import Allowed_Emails

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget = forms.TextInput(attrs={'type': 'email', 'class': 'form-control form-control-alt', 'placeholder': 'Seu e-mail'})
        self.fields['login'].label = 'E-mail'
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control form-control-alt', 'placeholder': 'Sua senha'})
        self.fields['password'].label = 'Senha'


class CustomSignupForm(SignupForm):

    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control form-control-alt', 'placeholder': 'Seu nome'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control form-control-alt', 'placeholder': 'Seu sobrenome'}))
    
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control form-control-alt', 'placeholder': 'Seu nome de usuário'})
        self.fields['email'].widget = forms.TextInput(attrs={'class': 'form-control form-control-alt', 'placeholder': 'Seu e-mail'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control form-control-alt', 'placeholder': 'Sua senha'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control form-control-alt', 'placeholder': 'Sua senha novamente'})
        self.fields['first_name'].label = 'Nome'
        self.fields['last_name'].label = 'Sobrenome'
        self.fields['username'].label = 'Nome de usuário'
        self.fields['email'].label = 'E-mail'
        self.fields['password1'].label = 'Senha'
        self.fields['password2'].label = 'Senha (novamente)'
    
    def clean_email(self):
        #somente e-mails autorizados podem se registrar.
        email = self.cleaned_data.get('email')

        #verifica se o email informado está na lista de emails autorizados
        if not Allowed_Emails.objects.filter(email=email).exists():
            raise ValidationError("Domínio de e-mail não autorizado.")
        
        #verifica se o email informado já existe no cadastro de usuários
        if User.objects.filter(email=email).exists():
            raise ValidationError("Endereço de e-mail já cadastrado.")
        
        return email
    
    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        return user
