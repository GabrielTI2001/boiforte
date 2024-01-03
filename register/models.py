from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField
import uuid
# Create your models here.
class Cadastro_Municipios(models.Model):
    id = models.BigIntegerField(primary_key=True, verbose_name='Código Município')
    cod_uf = models.IntegerField(verbose_name='Código UF')
    sigla_uf = models.CharField(max_length=2, null=True, verbose_name='Sigla UF')
    nome_uf = models.CharField(max_length=255, null=True, verbose_name='Nome UF')
    nome_municipio = models.CharField(max_length=255, null=True, verbose_name='Nome Município')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural = 'Cadastro Municípios'
    def __str__(self):
        return f"{self.nome_municipio} - {self.sigla_uf}"


class Categoria_Cadastro_Pessoal(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    description = models.CharField(max_length=255, null=True, verbose_name='Descrição Categoria')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural = 'Categoria Cadastro Pessoal'
    def __str__(self):
        return self.description


class Cadastro_Pessoal(models.Model):
    NATUREZA_CHOICES = (
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica')
    )

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    categoria = models.ForeignKey(Categoria_Cadastro_Pessoal, on_delete=models.SET_NULL, null=True, verbose_name='Categoria Cadastro')
    razao_social = models.CharField(verbose_name='Nome ou Razão Social', max_length=255, null=True)
    natureza_juridica = models.CharField(verbose_name='Natureza Jurídica', max_length=2, choices=NATUREZA_CHOICES, null=True)
    nome_fantasia = models.CharField(max_length=255, null=True, blank=True, verbose_name='Nome Fantasia')
    cpf_cnpj = models.CharField(verbose_name='CPF/CNPJ', max_length=40, null=True, unique=True, error_messages={'unique':'CPF ou CNPJ já cadastrado!'})
    numero_rg = models.CharField(max_length=255, null=True, blank=True, verbose_name='Endereço')
    endereco = models.CharField(max_length=255, null=True, blank=True, verbose_name='Endereço')
    municipio = models.ForeignKey(Cadastro_Municipios, null=True, on_delete=models.CASCADE, verbose_name='Município')
    cep_endereco = models.CharField(max_length=50, null=True, blank=True, verbose_name='CEP')
    data_nascimento = models.DateField(verbose_name='Data Nascimento', null=True, blank=True)
    contato_01 = models.CharField(max_length=100, null=True, blank=True, verbose_name='Contato 01')
    contato_02 = models.CharField(max_length=100, null=True, blank=True, verbose_name='Contato 02')
    email_01 = models.CharField(max_length=100, null=True, blank=True, verbose_name='Email 01')
    email_02 = models.CharField(max_length=100, null=True, blank=True, verbose_name='Email 02')
    profissao = models.CharField(max_length=100, null=True, blank=True, verbose_name='Profissão')
    description = models.TextField(null=True, blank=True, verbose_name='Descrição')
    avatar = ResizedImageField(size=[128, 128], default='avatars/clients/default-avatar.jpeg', upload_to='avatars/clients')
    is_active = models.BooleanField(default=1, null=True, verbose_name='Ativo')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural = 'Cadastro Pessoal'
    def __str__(self):
        return self.razao_social