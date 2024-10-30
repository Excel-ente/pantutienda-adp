# Generated by Django 5.0.7 on 2024-10-21 03:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0014_landing_nombre'),
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('landing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='front.landing')),
            ],
        ),
        migrations.AddField(
            model_name='landing',
            name='sections',
            field=models.ManyToManyField(related_name='landings', to='front.section'),
        ),
    ]