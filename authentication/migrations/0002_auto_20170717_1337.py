# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-07-17 12:37
from __future__ import unicode_literals

import authentication.models
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='profile',
            name='picture',
            field=models.ImageField(null=True, upload_to=authentication.models.rename),
        ),
    ]