# Generated by Django 5.0.6 on 2024-06-26 15:43

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_author_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='name',
            field=models.CharField(max_length=20, verbose_name=django.contrib.auth.models.User),
        ),
    ]
