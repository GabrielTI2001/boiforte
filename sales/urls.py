from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.index_vendas, name='vendas.index'),
    path('new', views.vendas_new, name='vendas.new'),
    path('edit/<uuid:uuid>', views.vendas_edit, name='vendas.edit'),
    path('delete/<int:id>', views.vendas_delete, name='vendas.delete')
]