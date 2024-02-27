from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from register.models import Cadastro_Pessoal
from register.forms import CadastroPessoalForm
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
import os
# Create your views here.
@login_required
@permission_required('register.view_cadastro_pessoal', raise_exception=True)
def index_cadastro_pessoal(request):

    search = request.GET.get('search')

    if search:
        query_search = (Q(razao_social__icontains=search) | Q(cpf_cnpj__icontains=search))
        cadastros = Cadastro_Pessoal.objects.filter(query_search).order_by('-created_at')
        qtd_cadastros = cadastros.count()
        str_registros = f"{qtd_cadastros} {'registros encontrados' if qtd_cadastros > 1 else 'registro encontrado'}"
    else:
        cadastros = Cadastro_Pessoal.objects.all().order_by('-created_at')
        qtd_cadastros = cadastros.count()
        str_registros = f"{qtd_cadastros} {'registros mais recentes' if qtd_cadastros > 1 else 'registro mais recente'}"

    cadastros_pessoais = [{
        'id': cad.id,
        'uuid': cad.uuid,
        'categoria': cad.categoria,
        'razao_social': cad.razao_social,
        'fantasia': cad.nome_fantasia,
        'cpf_cnpj': cad.cpf_cnpj,
        'endereco': cad.endereco or '-',
        'municipio': f"{cad.municipio.nome_municipio} - {cad.municipio.sigla_uf}",
        'natureza_juridica': cad.natureza_juridica
    } for cad in cadastros]

    context = {
        'cadastros': cadastros_pessoais,
        'str_registros': str_registros
    }

    return render(request, 'pessoal/index.html', context)



@login_required
@permission_required('register.view_cadastro_pessoal', raise_exception=True)
def cadastro_pessoal_view(request, uuid):

    try:
        cadastro = Cadastro_Pessoal.objects.get(uuid=uuid)


        context = {
            'cadastro': cadastro
        }
        

        return render(request, 'pessoal/view.html', context)  
    
    except ObjectDoesNotExist:
        return render(request, 'errors/404.html')



     
         


@login_required
@permission_required('register.add_cadastro_pessoal', raise_exception=True)
def cadastro_pessoal_new(request):
    #NOVO CADASTRO PESSOAL
    user = Cadastro_Pessoal(created_by = request.user)

    if request.method == "POST":
        form = CadastroPessoalForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save() #Salva no Banco de Dados
            messages.success(request, 'Cadastro realizado com sucesso.', extra_tags='app_messages')
            return redirect('cadpessoal.index')

        else:
            return render(request, 'pessoal/new.html', {'form': form})
    
    else:
        form = CadastroPessoalForm()
        return render(request, 'pessoal/new.html', {'form': form})


login_required
@permission_required('register.change_cadastro_pessoal', raise_exception=True)
def cadastro_pessoal_edit(request, uuid):

    instance = Cadastro_Pessoal.objects.get(uuid=uuid)

    if request.method == "POST":
        form = CadastroPessoalForm(request.POST, request.FILES, instance=instance)
        avatar_path = instance.avatar.path
        avatar_name = instance.avatar.name

        if form.is_valid():
            if request.FILES and avatar_name != 'avatars/clients/default-avatar.jpeg':
                os.remove(avatar_path)
            form.save()
            messages.success(request, 'Cadastro atualizado com sucesso!', extra_tags='app_messages')

    else:
        form = CadastroPessoalForm(instance=instance)

    context = {
        'form': form,
        'uuid': uuid,
        'fantasia' : instance.nome_fantasia,
        'avatar': instance.avatar
    }

    return render(request, 'pessoal/edit.html', context)

@login_required
@permission_required('register.delete_cadastro_pessoal', raise_exception=True)
def cadastro_pessoal_delete(request, uuid):
    try:
        cadastro = Cadastro_Pessoal.objects.get(uuid=uuid)
        print(cadastro.avatar.name)
        if cadastro.avatar and cadastro.avatar.name != 'avatars/clients/default-avatar.jpeg': #remove o avatar, se houver
            os.remove(cadastro.avatar.path)
        cadastro.delete()
        messages.success(request, 'Cadastro excluído com sucesso!', extra_tags='app_messages')
        return redirect('cadpessoal.index')
    
    except ObjectDoesNotExist:
        return render(request, 'errors/404.html')