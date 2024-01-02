from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField
import uuid
# Create your models here.
class MyAppPermissions(models.Model):
    class Meta:
        managed = False  # No database table creation or deletion operations will be performed for this model.
        permissions = [
            ("gerenciar_usuarios", "Gerenciar Usuários"),
        ]

class Profile(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    job_function = models.CharField(max_length=255, null=True, verbose_name='Cargo ou Função')
    cpf =  models.CharField(max_length=255, null=True, verbose_name='CPF')
    bio = models.TextField(default=None, null=True, verbose_name='Biografia')
    birthday = models.DateField(null=True, verbose_name='Data Nascimento')
    avatar = ResizedImageField(size=[128, 128], default='avatars/users/default-avatar.jpg', upload_to='avatars/users')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'User Profile'
    def __str__(self):
        return self.user.first_name
