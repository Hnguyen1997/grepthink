# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-05-26 05:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_projectplan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectplan',
            name='duration',
        ),
    ]
