from . import views
from django.urls import path, include

urlpatterns = [
    path('pessoal/', views.index_cadastro_pessoal, name='cadpessoal.index'),
    path('pessoal/new', views.cadastro_pessoal_new, name='cadpessoal.new'),
    path('pessoal/edit/<uuid:uuid>', views.cadastro_pessoal_edit, name='cadpessoal.edit'),
    path('pessoal/delete/<uuid:uuid>', views.cadastro_pessoal_delete, name='cadpessoal.delete')
]