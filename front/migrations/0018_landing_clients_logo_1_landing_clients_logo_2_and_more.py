# Generated by Django 5.0 on 2024-10-31 11:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0017_remove_landing_category_1_image_and_more'),
        ('inventario', '0019_alter_categoria_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='landing',
            name='clients_logo_1',
            field=models.ImageField(blank=True, null=True, upload_to='img/landing/'),
        ),
        migrations.AddField(
            model_name='landing',
            name='clients_logo_2',
            field=models.ImageField(blank=True, null=True, upload_to='img/landing/'),
        ),
        migrations.AddField(
            model_name='landing',
            name='clients_logo_3',
            field=models.ImageField(blank=True, null=True, upload_to='img/landing/'),
        ),
        migrations.AddField(
            model_name='landing',
            name='clients_logo_4',
            field=models.ImageField(blank=True, null=True, upload_to='img/landing/'),
        ),
        migrations.AddField(
            model_name='landing',
            name='clients_text',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='landing',
            name='clients_title',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='landing',
            name='footer_icon',
            field=models.ImageField(blank=True, null=True, upload_to='img/landing/'),
        ),
        migrations.AddField(
            model_name='landing',
            name='footer_section',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='landing',
            name='footer_text',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='landing',
            name='section_clients',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='section',
            name='name',
            field=models.CharField(choices=[('section_hero', 'Hero Section'), ('section_category', 'Category Section'), ('section_gallery', 'Gallery Section'), ('about_us', 'About Us Section'), ('testimonials', 'Testimonials Section'), ('features', 'Features Section'), ('cta_section', 'Call to Action Section'), ('newsletter', 'Newsletter Section'), ('section_clients', 'Nuestros Clientes Section'), ('footer', 'Footer Section')], max_length=255),
        ),
        migrations.CreateModel(
            name='CategoryOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(default=0)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventario.categoria')),
                ('landing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_order_set', to='front.landing')),
            ],
            options={
                'verbose_name': 'orden de categoría',
                'verbose_name_plural': 'Orden de Categorías',
                'ordering': ['order'],
            },
        ),
    ]