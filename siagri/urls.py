from . import views
from django.urls import path

urlpatterns = [
    path('accounts', views.siagri_contas_pagar_receber, name='siagri.contas.pagar.receber'),
    path('accounts/payments', views.siagri_contas_pagar, name='siagri.contas.pagar'),
    path('accounts/revenues', views.siagri_contas_receber, name='siagri.contas.receber'),




    path('test', views.siagri_test, name='siagri.test'),
    

]