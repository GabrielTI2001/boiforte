from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from sales.models import Venda
from django.db.models import Sum
import requests
import locale

@login_required
def dashboard_index(request):

    return render(request, 'dashboard.html')