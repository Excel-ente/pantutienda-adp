# Generated by Django 5.0.7 on 2024-10-01 01:51

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('agenda', '0001_initial'),
        ('configuracion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asientos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now_add=True)),
                ('tipo', models.CharField(choices=[('Patrimonial', 'Patrimonial'), ('Comercial', 'Comercial')], default='Patrimonial', max_length=35)),
                ('detalle', models.CharField(blank=True, max_length=120, null=True)),
                ('estado', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'asiento',
                'verbose_name_plural': '📇 Asientos',
            },
        ),
        migrations.CreateModel(
            name='Cuentas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField(blank=True, null=True, unique=True)),
                ('descripcion', models.CharField(blank=True, max_length=120, null=True)),
                ('tipo_cuenta', models.CharField(choices=[('Personal', 'Personal'), ('Punto de Venta', 'Punto de Venta'), ('Activo', 'Activo'), ('Pasivo', 'Pasivo'), ('Patrimonio', 'Patrimonio')], default='Activo', max_length=20)),
                ('moneda', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='configuracion.monedas')),
            ],
            options={
                'verbose_name': 'cuenta',
                'verbose_name_plural': '💼 Cuentas Patrimoniales',
            },
        ),
        migrations.CreateModel(
            name='CuentasComerciales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField(blank=True, null=True, unique=True)),
                ('descripcion', models.CharField(blank=True, max_length=120, null=True)),
                ('chofer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='agenda.chofer')),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='agenda.cliente')),
                ('moneda', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='configuracion.monedas')),
                ('proveedor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='agenda.proveedor')),
                ('vendedor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='agenda.vendedor')),
            ],
            options={
                'verbose_name': 'cuenta',
                'verbose_name_plural': '🪪 Cuentas comerciales',
            },
        ),
        migrations.CreateModel(
            name='MovimientosCuentaComercial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('debe', models.DecimalField(decimal_places=2, default=0, max_digits=25)),
                ('haber', models.DecimalField(decimal_places=2, default=0, max_digits=25)),
                ('comentarios', models.CharField(blank=True, max_length=255, null=True)),
                ('asiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contabilidad.asientos')),
                ('cuenta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contabilidad.cuentascomerciales')),
            ],
            options={
                'verbose_name': 'movimiento',
                'verbose_name_plural': '📚 Movimientos',
            },
        ),
        migrations.CreateModel(
            name='MovimientosCuentaContable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('debe', models.DecimalField(decimal_places=2, default=0, max_digits=25)),
                ('haber', models.DecimalField(decimal_places=2, default=0, max_digits=25)),
                ('comentarios', models.CharField(blank=True, max_length=255, null=True)),
                ('asiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contabilidad.asientos')),
                ('cuenta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contabilidad.cuentas')),
            ],
            options={
                'verbose_name': 'movimiento',
                'verbose_name_plural': '📚 Movimientos',
            },
        ),
    ]
