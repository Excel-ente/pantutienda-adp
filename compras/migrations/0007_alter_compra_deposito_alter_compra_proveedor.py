# Generated by Django 5.0 on 2024-10-13 22:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0017_direccionentregacliente_pin_maps'),
        ('compras', '0006_compra_detalle_alter_detallecompra_detalle'),
        ('inventario', '0009_deposito_pin_maps'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='deposito',
            field=models.ForeignKey(default=1, help_text='Seleccione el deposito donde ingresará la mercadería.', on_delete=django.db.models.deletion.PROTECT, to='inventario.deposito', verbose_name='Deposito ingreso'),
        ),
        migrations.AlterField(
            model_name='compra',
            name='proveedor',
            field=models.ForeignKey(blank=True, help_text='Si no selecciona proveedor, la compra se mostrará como "Proveedores Generales"', null=True, on_delete=django.db.models.deletion.PROTECT, to='agenda.proveedor'),
        ),
    ]
