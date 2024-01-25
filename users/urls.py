from django.urls import path
from . import views

urlpatterns = [
    path('', views.users_index, name='users.index'),
    path('view/<int:id>', views.user_view, name='user.view'),
    path('edit/<int:id>', views.user_edit, name='user.edit'),
    path('new', views.user_new, name='user.new'),
    path('emails', views.users_emails, name='users.emails'),
]