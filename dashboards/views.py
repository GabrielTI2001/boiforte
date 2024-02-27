from django.shortcuts import render
from sales.models import Venda
from django.db.models import Sum
import requests
import locale

def dashboard_vendas(request):
    ranking_clientes = Venda.objects.values('cliente', 'cliente__razao_social', 'cliente__avatar').annotate(total = Sum('valor')).order_by('-total')
    ranking_fornecedores = Venda.objects.values('fornecedor', 'fornecedor__razao_social', 'fornecedor__avatar').annotate(total = Sum('valor')).order_by('-total')

    venda_clientes = [{
        'posicao': f"{i + 1}°",
        'cliente': r['cliente__razao_social'],
        'avatar': r['cliente__avatar'],
        'total': locale.currency(r['total'], grouping=True)
    } for i, r in enumerate(ranking_clientes)]

    venda_fornecedores = [{
        'posicao': f"{i + 1}°",
        'fornecedor': r['fornecedor__razao_social'],
        'avatar': r['fornecedor__avatar'],
        'total': locale.currency(r['total'], grouping=True)
    } for i, r in enumerate(ranking_fornecedores)]

    context = {
        'venda_clientes': venda_clientes,
        'venda_fornecedores': venda_fornecedores
    }

    return render(request, 'vendas.html', context)