# Generated by Django 5.0.7 on 2024-10-29 02:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0016_alter_landing_options_alter_section_options_and_more'),
        ('inventario', '0018_alter_recetaproducto_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='landing',
            name='category_1_image',
        ),
        migrations.RemoveField(
            model_name='landing',
            name='category_2_image',
        ),
        migrations.RemoveField(
            model_name='landing',
            name='category_3_image',
        ),
        migrations.RemoveField(
            model_name='landing',
            name='category_4_image',
        ),
        migrations.AlterField(
            model_name='landing',
            name='category_1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='landing_category_1', to='inventario.categoria'),
        ),
        migrations.AlterField(
            model_name='landing',
            name='category_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='landing_category_2', to='inventario.categoria'),
        ),
        migrations.AlterField(
            model_name='landing',
            name='category_3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='landing_category_3', to='inventario.categoria'),
        ),
        migrations.AlterField(
            model_name='landing',
            name='category_4',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='landing_category_4', to='inventario.categoria'),
        ),
    ]
