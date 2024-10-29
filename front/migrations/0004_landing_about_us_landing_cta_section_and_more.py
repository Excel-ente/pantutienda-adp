# Generated by Django 5.0.7 on 2024-10-20 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0003_landing_section_gallery'),
    ]

    operations = [
        migrations.AddField(
            model_name='landing',
            name='about_us',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='landing',
            name='cta_section',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='landing',
            name='features',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='landing',
            name='newsletter',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='landing',
            name='testimonials',
            field=models.BooleanField(default=False),
        ),
    ]
