# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-28 01:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_auto_20190130_1856'),
    ]

    operations = [
        migrations.CreateModel(
            name='Techs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tech', models.CharField(default='', max_length=255)),
            ],
            options={
                'verbose_name': 'Tech',
                'verbose_name_plural': 'Techs',
                'ordering': ('tech',),
            },
        ),
    ]