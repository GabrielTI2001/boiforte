from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.dashboard_index, name='dashboard.index'),
]