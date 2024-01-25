from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.contrib.auth.models import User
from administrator.models import Allowed_Emails
from users.models import Profile
from django.contrib.auth.forms import PasswordChangeForm
from .forms import Profileform, Userform, formEmails
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, ExpressionWrapper, DateTimeField, Sum, Q
from boiforte.forms import CustomSignupForm, SignupForm
import os, requests, json

@login_required
@permission_required('users.gerenciar_usuarios', raise_exception=True)
def users_index(request):
    #INDEX CADASTRO USUÁRIOS
    search = request.GET.get('search')

    if search:
        query_search = (Q(user__first_name__icontains=search) | Q(user__last_name__icontains=search) | Q(user__email__icontains=search) | Q(user__username__icontains=search))
        query_users = Profile.objects.filter(query_search)
        qtd_cadastros = query_users.count()
        str_usuarios = f"{qtd_cadastros} {'usuários encontrados' if qtd_cadastros > 1 else 'usuário encontrado'}"
    else:
        query_users = Profile.objects.all()
        qtd_cadastros = query_users.count()
        str_usuarios = f"{qtd_cadastros} {'usuários mais recentes' if qtd_cadastros > 1 else 'usuário mais recente'}"

    users = [{
        'id': user.id,
        'first_name': user.user.first_name,
        'last_name': user.user.last_name,
        'avatar': user.avatar,
        'last_login': user.user.last_login.strftime("%d/%m/%Y às %H:%M") if  user.user.last_login != None else 'Nunca Fez Login',
        'email': user.user.email,
        'username': user.user.username,
        'is_active': 'Ativo' if user.user.is_active else 'Desativado',
        'is_active_color': 'success' if user.user.is_active else 'warning',
    }for user in query_users]

    context = {
        'users': users,
        'str_usuarios': str_usuarios
    }

    return render(request, 'index_users.html', context)



@login_required
@permission_required('users.view_profile', raise_exception=True)
def user_view(request, id):
    usuario = User.objects.get(pk=request.user.id)
    try:
        profile = Profile.objects.get(user=usuario, pk=id)

        context = {
            'first_name': profile.user.first_name,
            'last_name': profile.user.last_name,
            'user_job': profile.job_function if profile.job_function else profile.user.email,
            'user_avatar': profile.avatar
        }

        return render(request, 'view_profile.html', context)
    
    except ObjectDoesNotExist:
        return render(request, 'errors/403.html')

    

@login_required
@permission_required('users.change_profile', raise_exception=True)
def user_edit(request, id):
    usuario = User.objects.get(pk=request.user.id)
    
    try:
        profile = Profile.objects.get(user=usuario, pk=id)
        if request.method == 'POST':
            formuser = Userform(request.POST, instance=usuario)
            formprofile = Profileform(request.POST, request.FILES, instance=profile)
            file_path = profile.avatar.path
            file_name = profile.avatar.name

            if formuser.is_valid():
                formuser.save()
            if formprofile.is_valid():
                if request.FILES and file_name != 'avatars/users/default-avatar.jpg':
                   os.remove(file_path)
                formprofile.save()  
                messages.success(request, 'Perfil atualizado com sucesso!', extra_tags='app_messages')
        else:
            formuser = Userform(instance=usuario)
            formprofile = Profileform(instance=profile)

        context = {
            'formusuario': formuser, 
            'formprofile': formprofile,
            'email': usuario.email,
            'user_job': profile.job_function if profile.job_function else usuario.email,
            'first_name': usuario.first_name,
            'last_name': usuario.last_name
        }

        return render(request, 'edit_profile.html', context)
    
    except ObjectDoesNotExist:
        return render(request, 'errors/403.html')
    

@login_required
@permission_required('users.gerenciar_usuarios', raise_exception=True)
def user_new(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            form.save(request)
            messages.success(request, 'Usuário cadastrado. Será necessário confirmar e-mail.', extra_tags='app_messages')
            return redirect('users.index')  # Ou redirecione para a página desejada
    else:
        form = CustomSignupForm()
    return render(request, 'new_user.html', {'form': form})

@login_required
@permission_required('users.gerenciar_usuarios', raise_exception=True)
def users_emails(request):
    emails = Allowed_Emails.objects.all()
    if request.method == 'POST':
        form = formEmails(request.POST)
        if form.is_valid():
            # Faça algo com o formulário válido
            form.save()
            messages.success(request, 'E-mail autorizado com sucesso.', extra_tags='app_messages')
            return render(request, 'users_emails.html', {'emails': emails, 'form':formEmails})
        else:
            form = formEmails(request.POST)
            return render(request, 'users_emails.html', {'emails': emails, 'form':form})

    else:
        return render(request, 'users_emails.html', {'emails': emails, 'form':formEmails})