# Generated by Django 5.0.7 on 2024-10-17 17:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0002_itempedido_precio_unitario_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pedido',
            options={'verbose_name': 'pedido', 'verbose_name_plural': '📲 Pedidos'},
        ),
    ]