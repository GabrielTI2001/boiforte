from . import views
from django.urls import path, include

urlpatterns = [
    path('sales-ranking', views.dashboard_vendas, name='dashboard.vendas'),
]