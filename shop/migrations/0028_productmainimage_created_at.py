# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-03 11:05
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0027_storeimage_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='productmainimage',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]