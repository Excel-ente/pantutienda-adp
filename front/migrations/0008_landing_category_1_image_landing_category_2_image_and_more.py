# Generated by Django 5.0.7 on 2024-10-20 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0007_landing_hero_background_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='landing',
            name='category_1_image',
            field=models.ImageField(blank=True, null=True, upload_to='img/landing/'),
        ),
        migrations.AddField(
            model_name='landing',
            name='category_2_image',
            field=models.ImageField(blank=True, null=True, upload_to='img/landing/'),
        ),
        migrations.AddField(
            model_name='landing',
            name='category_3_image',
            field=models.ImageField(blank=True, null=True, upload_to='img/landing/'),
        ),
        migrations.AddField(
            model_name='landing',
            name='category_4_image',
            field=models.ImageField(blank=True, null=True, upload_to='img/landing/'),
        ),
    ]