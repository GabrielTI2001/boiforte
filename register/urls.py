"""
URL configuration for boiforte project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.urls import path, include

urlpatterns = [
    path('pessoal/', views.index_cadastro_pessoal, name='cadpessoal.index'),
    path('pessoal/new', views.cadastro_pessoal_new, name='cadpessoal.new'),
    path('pessoal/edit/<uuid:uuid>', views.cadastro_pessoal_edit, name='cadpessoal.edit'),
    path('pessoal/delete/<uuid:uuid>', views.cadastro_pessoal_delete, name='cadpessoal.delete')
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)