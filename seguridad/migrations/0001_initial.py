# Generated by Django 5.0.7 on 2024-10-28 23:53

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FailedLoginAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField()),
                ('attempt_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('ciudad', models.CharField(blank=True, max_length=100, null=True)),
                ('region', models.CharField(blank=True, max_length=100, null=True)),
                ('pais', models.CharField(blank=True, max_length=100, null=True)),
                ('organizacion', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
