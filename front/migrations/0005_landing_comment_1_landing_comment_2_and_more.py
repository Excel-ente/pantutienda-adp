# Generated by Django 5.0.7 on 2024-10-20 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0004_landing_about_us_landing_cta_section_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='landing',
            name='comment_1',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='landing',
            name='comment_2',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='landing',
            name='comment_3',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='landing',
            name='name_comment_1',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='landing',
            name='name_comment_2',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='landing',
            name='name_comment_3',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='landing',
            name='testimonials_title',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
