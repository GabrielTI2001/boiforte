from register.models import Cadastro_Pessoal, Cadastro_Municipios, Categoria_Cadastro_Pessoal
from django import forms
from PIL import Image
from django.core.validators import RegexValidator
import uuid, os

class CadastroPessoalForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(
        queryset=Categoria_Cadastro_Pessoal.objects.all(),
        label='Categoria',
        widget=forms.Select(attrs={'class': 'form-control form-control-alt'}))
    
    razao_social = forms.CharField(
        label='Nome ou Razão Social', min_length=3, max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-alt'}))
    
    nome_fantasia = forms.CharField(
        label='Nome Fantasia', min_length=3, max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-alt'}))
    
    natureza_juridica = forms.ChoiceField(
        label='Natureza Jurídica',
        choices=[('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')],
        widget=forms.Select(attrs={'type': 'select', 'class': 'form-control form-control-alt'}))

    cpf_cnpj = forms.CharField(
        label='CPF/CNPJ', min_length=3, max_length=100,
        validators=[RegexValidator(r'(^\d{3}\.\d{3}\.\d{3}\-\d{2}$)|(^\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}$)', message='Formato CPF ou CNPJ inválido!')],
        widget=forms.TextInput(attrs={'class': 'form-control form-control-alt'}))
    
    numero_rg = forms.CharField(
        label='N° RG', min_length=3, max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-alt'}))
    
    endereco = forms.CharField(
        label='Endereço', max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-alt'}))
    
    municipio = forms.ModelChoiceField(
        queryset=Cadastro_Municipios.objects.all().order_by('nome_municipio'),
        label='Município',
        widget=forms.Select(attrs={'class': 'form-control form-control-alt'}))
    
    cep_endereco = forms.CharField(
        label='CEP Endereço', max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-alt'}))

    data_nascimento = forms.DateField(
        label='Data Nascimento',
        required=False,
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control form-control-alt'}))
    
    contato_01 = forms.CharField(
        label='Contato (1)', max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-alt'}))
    
    contato_02 = forms.CharField(
        label='Contato (2)', max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-alt'}))
 
    email_01 = forms.CharField(
        label='E-mail (1)', max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-alt'}))
    
    email_02 = forms.CharField(
        label='E-mail (2)', max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-alt'}))
    
    profissao = forms.CharField(
        label='Profissão', max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-alt'}))
    
    description = forms.CharField(
        label='Descrição', min_length=3,
        required=False,
        widget=forms.Textarea(attrs={'cols': 6, 'rows': 3, 'class': 'form-control form-control-alt'}))

    avatar = forms.FileField(
        label='Avatar',
        required=False,
        widget=forms.FileInput(attrs={'type': 'file', 'class': 'form-control form-control-alt'}))
    
    def clean_nome_fantasia(self):
        nome_fantasia_input = self.cleaned_data['nome_fantasia']
        razao_social = self.cleaned_data['razao_social']
        if not nome_fantasia_input:
            name_parts = razao_social.split()
            if len(name_parts) >= 2:
                first_name = name_parts[0]
                last_name = name_parts[-1]
            else:
                first_name = name_parts[0]
                last_name = ""

            nome_fantasia = f"{first_name} {last_name}"

        else:
            nome_fantasia = nome_fantasia_input

        return nome_fantasia
    
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

    def clean(self):
        cleaned_data = super().clean()
        for field in self.fields:
            if self.fields[field].required == False and cleaned_data.get(field) == "":
                cleaned_data[field] = None
        return cleaned_data

    class Meta:
        model = Cadastro_Pessoal
        exclude = ('created_by', 'is_active')