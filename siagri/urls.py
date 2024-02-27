from . import views
from django.urls import path

urlpatterns = [
    path('', views.index_siagri, name='siagri.index'),
    path('pagar', views.siagri_contas_pagar, name='siagri.contas.pagar'),
    path('receber', views.siagri_contas_receber, name='siagri.contas.receber'),

]