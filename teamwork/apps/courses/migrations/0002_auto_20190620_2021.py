# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-06-20 12:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
        ('courses', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='projects',
            field=models.ManyToManyField(related_name='course', to='projects.Project'),
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(related_name='enrollment', through='courses.Enrollment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='assignment',
            name='subs',
            field=models.ManyToManyField(default='', related_name='ass', to='projects.Tsr'),
        ),
    ]
