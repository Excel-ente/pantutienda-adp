# Generated by Django 5.0 on 2024-10-11 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0005_producto_costo_unitario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productoprecio',
            name='precio_manual',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
    ]
