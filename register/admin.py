from django.contrib import admin
from .models import Cadastro_Pessoal, Categoria_Cadastro_Pessoal

# Register your models here.
@admin.register(Categoria_Cadastro_Pessoal)
class ProfileAdmin(admin.ModelAdmin):
    list_display =  ('uuid', 'description')

@admin.register(Cadastro_Pessoal)
class ProfileAdmin(admin.ModelAdmin):
    list_display =  ('uuid', 'cpf_cnpj', 'razao_social')
