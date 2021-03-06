# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-05 05:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_date', models.DateTimeField(blank=True, null=True)),
                ('source', models.URLField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Classification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='article.Classification')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commenter', models.CharField(max_length=60)),
                ('text', models.TextField()),
                ('comment_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('belong_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.Article')),
                ('comment_on', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='article.Comment')),
            ],
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('html_tag', models.CharField(choices=[('1', 'h1'), ('2', 'h2'), ('3', 'h3'), ('4', 'h4'), ('5', 'h5'), ('6', 'h6'), ('7', 'a'), ('8', 'p'), ('9', 'img')], default='8', max_length=1)),
                ('text', models.TextField(default='new content')),
                ('html_class', models.CharField(blank=True, max_length=200, null=True)),
                ('href', models.CharField(blank=True, max_length=200, null=True)),
                ('src', models.CharField(blank=True, max_length=200, null=True)),
                ('alt', models.CharField(blank=True, max_length=200, null=True)),
                ('belong_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content', to='article.Article')),
                ('previous_content', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='previous', to='article.Content')),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='classification',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='article.Classification'),
        ),
    ]
