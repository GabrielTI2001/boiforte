from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from .models import Venda
from .forms import *

@login_required
@permission_required('sales.view_venda', raise_exception=True)
def index_vendas(request):
    search = request.GET.get('search')
    if search:
        query_search = (Q(cliente__razao_social__icontains=search) | Q(fornecedor__razao_social__icontains=search))
        cadastros = Venda.objects.filter(query_search).order_by('-created_at')
        qtd_cadastros = cadastros.count()
        str_registros = f"{qtd_cadastros} {'registros encontrados' if qtd_cadastros > 1 else 'registro encontrado'}"
    else:
        cadastros = Venda.objects.all().order_by('-created_at')
        qtd_cadastros = cadastros.count()
        str_registros = f"{qtd_cadastros} {'registros mais recentes' if qtd_cadastros > 1 else 'registro mais recente'}"

    contexto = {
        'cadastros': cadastros,
        'str_registros': str_registros
    }
    return render(request, 'index.html', contexto)

@login_required
@permission_required('sales.add_venda', raise_exception=True)
def vendas_new(request):
    venda = Venda(created_by = request.user)
    if request.method == "POST":
        form = VendaForm(request.POST, instance=venda)
        if form.is_valid():
            form.save()
            form = VendaForm()
            messages.success(request, 'Cadastro efetuado com sucesso!', extra_tags='app_messages') 
    form = VendaForm()
    return render(request, 'new.html', {'form':form})

@login_required
@permission_required('sales.change_venda', raise_exception=True)
def vendas_edit(request, uuid):
    venda = Venda.objects.get(uuid=uuid)
    form = VendaForm(instance=venda)
    if request.method == "POST":
        form = VendaForm(request.POST, instance=venda)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro atualizado com sucesso!', extra_tags='app_messages') 
    return render(request, 'edit.html', {'form':form})

@login_required
@permission_required('sales.delete_venda', raise_exception=True)
def vendas_delete(request, id):
    try:
        cadastro = Venda.objects.get(id=id)
        cadastro.delete()
        messages.success(request, 'Cadastro excluído com sucesso!', extra_tags='app_messages')
        return redirect('vendas.index')
    except ObjectDoesNotExist:
        return render(request, 'errors/404.html')