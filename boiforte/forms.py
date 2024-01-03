from django import forms
from allauth.account.forms import LoginForm

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget = forms.TextInput(attrs={'type': 'email', 'class': 'form-control form-control-alt', 'placeholder': 'Seu e-mail'})
        self.fields['login'].label = 'E-mail'
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control form-control-alt', 'placeholder': 'Sua senha'})
        self.fields['password'].label = 'Senha'