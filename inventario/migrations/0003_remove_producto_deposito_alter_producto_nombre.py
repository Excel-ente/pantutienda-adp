# Generated by Django 5.0 on 2024-10-11 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0002_remove_deposito_contactos_remove_deposito_cuit_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='deposito',
        ),
        migrations.AlterField(
            model_name='producto',
            name='nombre',
            field=models.CharField(max_length=100),
        ),
    ]