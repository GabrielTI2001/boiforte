from . import views
from django.urls import path, include

urlpatterns = [
    path('vendas', views.dashboard_vendas, name='dashboard.vendas'),
]