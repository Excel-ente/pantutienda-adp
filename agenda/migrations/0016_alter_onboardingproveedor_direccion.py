# Generated by Django 5.0 on 2024-10-12 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0015_onboardingproveedor_pin_maps_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onboardingproveedor',
            name='direccion',
            field=models.CharField(max_length=255, null=True, verbose_name='Dirección'),
        ),
    ]