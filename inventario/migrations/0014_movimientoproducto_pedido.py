# Generated by Django 5.0.7 on 2024-10-19 21:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0013_movimientoproducto_compra'),
        ('pedidos', '0006_alter_pedido_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimientoproducto',
            name='pedido',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pedidos.pedido'),
        ),
    ]
