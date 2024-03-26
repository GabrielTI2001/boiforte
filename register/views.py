from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from register.models import Cadastro_Pessoal
from register.forms import CadastroPessoalForm
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from boiforte.settings import BOIFORTE_DB_HOST, BOIFORTE_DB_PASS, BOIFORTE_DB_PORT, BOIFORTE_DB_USER, BOIFORTE_DB_SID, ORACLE_CLIENT
import os, cx_Oracle

@login_required
@permission_required('register.view_cadastro_pessoal', raise_exception=True)
def index_cadastro_pessoal(request):
    dsn_tns = cx_Oracle.makedsn(BOIFORTE_DB_HOST, BOIFORTE_DB_PORT, BOIFORTE_DB_SID)
    search = request.GET.get('search')

    if search:
        conexao = cx_Oracle.connect(BOIFORTE_DB_USER, BOIFORTE_DB_PASS, dsn_tns)

        # Criar um cursor
        cursor = conexao.cursor()
        
        # Consulta SQL
        consulta_sql = f"""SELECT A.CODI_TRA, A.CODI_MUN, A.RAZA_TRA, A.CGC_TRA, A.ENDE_TRA, B.DESC_MUN, B.ESTA_MUN FROM TRANSAC A
            INNER JOIN MUNICIPIO B ON (B.CODI_MUN = A.CODI_MUN)
            WHERE A.RAZA_TRA LIKE '%{search.upper()}%'"""
                
        # Executar a consulta
        cursor.execute(consulta_sql)
        
        # Recuperar os resultados como uma lista de dicionários
        #colunas = ["nome", "cgc"]
        colunas = [col[0] for col in cursor.description]
        cadastros = [dict(zip(colunas, row)) for row in cursor.fetchall()]
        
        # Fechar o cursor e a conexão
        cursor.close()
        conexao.close()

        return render(request, 'pessoal/index.html', {'cadastros': cadastros})
    else:
        return render(request, 'pessoal/index.html')



# @login_required
# @permission_required('register.view_cadastro_pessoal', raise_exception=True)
# def cadastro_pessoal_view(request, uuid):

#     try:
#         cadastro = Cadastro_Pessoal.objects.get(uuid=uuid)


#         context = {
#             'cadastro': cadastro
#         }
        

#         return render(request, 'pessoal/view.html', context)  
    
#     except ObjectDoesNotExist:
#         return render(request, 'errors/404.html')


# @login_required
# @permission_required('register.add_cadastro_pessoal', raise_exception=True)
# def cadastro_pessoal_new(request):
#     #NOVO CADASTRO PESSOAL
#     user = Cadastro_Pessoal(created_by = request.user)

#     if request.method == "POST":
#         form = CadastroPessoalForm(request.POST, request.FILES, instance=user)
#         if form.is_valid():
#             form.save() #Salva no Banco de Dados
#             messages.success(request, 'Cadastro realizado com sucesso.', extra_tags='app_messages')
#             return redirect('cadpessoal.index')

#         else:
#             return render(request, 'pessoal/new.html', {'form': form})
    
#     else:
#         form = CadastroPessoalForm()
#         return render(request, 'pessoal/new.html', {'form': form})


# login_required
# @permission_required('register.change_cadastro_pessoal', raise_exception=True)
# def cadastro_pessoal_edit(request, uuid):

#     instance = Cadastro_Pessoal.objects.get(uuid=uuid)

#     if request.method == "POST":
#         form = CadastroPessoalForm(request.POST, request.FILES, instance=instance)
#         avatar_path = instance.avatar.path
#         avatar_name = instance.avatar.name

#         if form.is_valid():
#             if request.FILES and avatar_name != 'avatars/clients/default-avatar.jpeg':
#                 os.remove(avatar_path)
#             form.save()
#             messages.success(request, 'Cadastro atualizado com sucesso!', extra_tags='app_messages')

#     else:
#         form = CadastroPessoalForm(instance=instance)

#     context = {
#         'form': form,
#         'uuid': uuid,
#         'fantasia' : instance.nome_fantasia,
#         'avatar': instance.avatar
#     }

#     return render(request, 'pessoal/edit.html', context)

# @login_required
# @permission_required('register.delete_cadastro_pessoal', raise_exception=True)
# def cadastro_pessoal_delete(request, uuid):
#     try:
#         cadastro = Cadastro_Pessoal.objects.get(uuid=uuid)
#         print(cadastro.avatar.name)
#         if cadastro.avatar and cadastro.avatar.name != 'avatars/clients/default-avatar.jpeg': #remove o avatar, se houver
#             os.remove(cadastro.avatar.path)
#         cadastro.delete()
#         messages.success(request, 'Cadastro excluído com sucesso!', extra_tags='app_messages')
#         return redirect('cadpessoal.index')
    
#     except ObjectDoesNotExist:
#         return render(request, 'errors/404.html')