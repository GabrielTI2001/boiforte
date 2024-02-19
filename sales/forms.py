from .models import Venda
from register.models import Cadastro_Pessoal
from django import forms

class VendaForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(
        queryset=Cadastro_Pessoal.objects.filter(categoria__description='Cliente'),
        label='Cliente',
        widget=forms.Select(attrs={'class': 'form-control form-control-alt'}))
    
    fornecedor = forms.ModelChoiceField(
        queryset=Cadastro_Pessoal.objects.filter(categoria__description='Fornecedor'),
        label='Fornecedor',
        widget=forms.Select(attrs={'class': 'form-control form-control-alt'}))
    
    class Meta:
        model = Venda
        exclude = ('created_by', 'updated_at', 'created_at')