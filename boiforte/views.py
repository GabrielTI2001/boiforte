from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from datetime import datetime, date
from django.utils.dateformat import format
from sales.models import Venda
from django.db.models import Sum
import locale

@login_required
def home(request):
    current_date = date.today()
    weekdays = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"]

    data_formatada = _("Hoje é %(weekday_name)s, %(dia)d de %(mes)s de %(ano)d") % {
        'weekday_name': weekdays[current_date.weekday()],
        'dia': current_date.day,
        'mes': format(current_date, 'F'),
        'ano': current_date.year,
    }
    
    context = {
        'user_avatar': request.user.profile.avatar,
        'str_today': data_formatada,
    }
    
    return render(request, 'home.html', context)

def handler404(request, exception):
    return render(request, 'errors/404.html', status=404)

def handler403(request, exception):
    return render(request, 'errors/403.html', status=403)

def handler500(request):
    return render(request, 'errors/500.html', status=500)
