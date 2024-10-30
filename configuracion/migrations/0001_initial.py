# Generated by Django 5.0.7 on 2024-10-01 01:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('agenda', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListaDePrecio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'lista',
                'verbose_name_plural': '📒 Listas de Precios',
            },
        ),
        migrations.CreateModel(
            name='medioDeCompra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=200, null=True)),
                ('tipo', models.CharField(choices=[('Efectivo', 'Efectivo'), ('Mercado Pago', 'Mercado Pago'), ('Bancario', 'Bancario'), ('Cuenta Corriente', 'Cuenta Corriente')], default='Efectivo', max_length=50)),
            ],
            options={
                'verbose_name': 'medio de compra',
                'verbose_name_plural': '💸 MDP Compras',
            },
        ),
        migrations.CreateModel(
            name='medioDeVenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=200, null=True)),
                ('tipo', models.CharField(choices=[('Efectivo', 'Efectivo'), ('Mercado Pago', 'Mercado Pago'), ('Bancario', 'Bancario'), ('Cuenta Corriente', 'Cuenta Corriente')], default='Efectivo', max_length=50)),
            ],
            options={
                'verbose_name': 'medio de pago',
                'verbose_name_plural': '🪙 MDP Ventas',
            },
        ),
        migrations.CreateModel(
            name='Monedas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='Pesos', max_length=255, unique=True)),
                ('abreviacion', models.CharField(default='ARS', max_length=3, unique=True)),
                ('signo', models.CharField(blank=True, default='$', max_length=5, null=True)),
                ('principal', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'moneda',
                'verbose_name_plural': '🪙 Monedas',
            },
        ),
        migrations.CreateModel(
            name='TipoCliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name': 'tipo cliente',
                'verbose_name_plural': '💼 Tipo de clientes',
            },
        ),
        migrations.CreateModel(
            name='configuracion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emprendimiento', models.CharField(blank=True, max_length=255, null=True)),
                ('venta_stock_negativo', models.BooleanField(default=False)),
                ('tipo_cambio_1', models.DecimalField(decimal_places=10, default=1, max_digits=25)),
                ('precio_venta_automatico', models.BooleanField(default=False, verbose_name='Precio venta basado en rentabilidad')),
                ('calculo_rentabilidad', models.CharField(choices=[('Sobre costo', 'Sobre costo'), ('Sobre venta', 'Sobre venta')], default='Sobre costo', max_length=50)),
                ('proveedor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='agenda.proveedor')),
            ],
            options={
                'verbose_name': 'configuracion',
                'verbose_name_plural': '⚙️ Configuracion',
            },
        ),
    ]