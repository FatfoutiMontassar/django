# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-08-23 07:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20170821_1353'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='message',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
