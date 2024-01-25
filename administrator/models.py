from django.db import models
import uuid

class Allowed_Emails(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    email = models.CharField(max_length=150, null=True, unique=True, verbose_name='Email')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural = 'Allowed Emails'
    def __str__(self):
        return self.email