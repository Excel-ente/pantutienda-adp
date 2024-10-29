# Generated by Django 5.0.7 on 2024-10-19 21:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0008_compra_descargas'),
        ('inventario', '0012_movimientoproducto_detalle_movimientoproducto_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimientoproducto',
            name='compra',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='compras.compra'),
        ),
    ]
