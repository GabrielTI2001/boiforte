from django.db import models

# Create your models here.
class MyAppPermissions(models.Model):
    class Meta:
        managed = False  # No database table creation or deletion operations will be performed for this model.
        permissions = [
            ("ver_contas_pagar_receber", "Ver Contas Pagar e Receber"),

        ]

