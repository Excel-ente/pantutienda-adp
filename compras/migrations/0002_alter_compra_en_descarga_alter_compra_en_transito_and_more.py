# Generated by Django 5.0 on 2024-10-11 17:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0013_alter_chofer_usuario'),
        ('compras', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='en_descarga',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='compra',
            name='en_transito',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='compra',
            name='proveedor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='agenda.proveedor'),
        ),
        migrations.AlterField(
            model_name='compra',
            name='vendedor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='agenda.vendedor'),
        ),
    ]
