# Generated by Django 5.0.7 on 2024-11-01 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0018_landing_clients_logo_1_landing_clients_logo_2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='landing',
            name='banner_1_image',
            field=models.ImageField(blank=True, null=True, upload_to='img/landing/'),
        ),
        migrations.AddField(
            model_name='landing',
            name='banner_1_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='landing',
            name='banner_2_image',
            field=models.ImageField(blank=True, null=True, upload_to='img/landing/'),
        ),
        migrations.AddField(
            model_name='landing',
            name='banner_2_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='landing',
            name='banner_3_image',
            field=models.ImageField(blank=True, null=True, upload_to='img/landing/'),
        ),
        migrations.AddField(
            model_name='landing',
            name='banner_3_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='landing',
            name='section_promo_banners',
            field=models.BooleanField(default=False),
        ),
    ]
