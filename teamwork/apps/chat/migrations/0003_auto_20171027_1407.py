# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-27 21:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_auto_20171026_2034'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chatroom',
            options={'ordering': ('name',)},
        ),
        migrations.RenameField(
            model_name='chatroom',
            old_name='room_name',
            new_name='name',
        ),
    ]
