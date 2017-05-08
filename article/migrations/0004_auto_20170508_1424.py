# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-08 06:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_remove_classification_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='classification',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.Classification'),
        ),
    ]
