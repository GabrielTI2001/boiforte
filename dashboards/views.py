from django.shortcuts import render
from sales.models import Venda
from django.db.models import Sum
import requests

def dashboard_vendas(request):
    ranking = Venda.objects.values('cliente', 'cliente__razao_social').annotate(
        total = Sum('valor')
    ).order_by('-total')
    dados = [{
        'cliente': r['cliente__razao_social'],
        'total': r['total']
    } for r in ranking]
    return render(request, 'vendas.html', {'dados':dados})