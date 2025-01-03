# Generated by Django 5.0.7 on 2024-10-19 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0005_rename_direccionentregacliente_pedido_direccion_entrega_cliente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='estado',
            field=models.CharField(choices=[('pendiente', 'Pendiente'), ('en_preparacion', 'En preparacion'), ('listo', 'Listo'), ('en_camino', 'En camino'), ('completado', 'Completado'), ('cancelado', 'Cancelado')], default='pendiente', max_length=20),
        ),
    ]
