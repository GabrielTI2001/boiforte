from django.db import models
from register.models import Cadastro_Pessoal
from django.contrib.auth.models import User
import uuid

class Venda(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    fornecedor = models.ForeignKey(Cadastro_Pessoal, null=True, on_delete=models.CASCADE, related_name="fornecedor")
    cliente = models.ForeignKey(Cadastro_Pessoal, null=True, on_delete=models.CASCADE, related_name="cliente")
    valor = models.DecimalField(max_digits=15, decimal_places=2, null=True, verbose_name="Valor (R$)")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)