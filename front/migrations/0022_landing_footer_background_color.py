# Generated by Django 5.0.7 on 2024-11-01 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0021_landing_background_color_hww'),
    ]

    operations = [
        migrations.AddField(
            model_name='landing',
            name='footer_background_color',
            field=models.CharField(default='#ffffff', help_text='Color de fondo en formato hexadecimal (ej. #ffffff para blanco)', max_length=7),
        ),
    ]
