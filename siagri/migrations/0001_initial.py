# Generated by Django 5.0.1 on 2024-03-26 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyAppPermissions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': [('ver_contas_pagar_receber', 'Ver Contas Pagar e Receber')],
                'managed': False,
            },
        ),
    ]