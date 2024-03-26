from . import views
from django.urls import path, include

urlpatterns = [
    path('personal', views.index_cadastro_pessoal, name='cadpessoal.index'),
    # path('personal/<uuid:uuid>', views.cadastro_pessoal_view, name='cadpessoal.view'),
    # path('personal/new', views.cadastro_pessoal_new, name='cadpessoal.new'),
    # path('personal/edit/<uuid:uuid>', views.cadastro_pessoal_edit, name='cadpessoal.edit'),
    # path('personal/delete/<uuid:uuid>', views.cadastro_pessoal_delete, name='cadpessoal.delete')
]