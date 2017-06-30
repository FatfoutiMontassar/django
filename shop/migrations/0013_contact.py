# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-26 15:20
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_auto_20170626_0512'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('subject', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
    ]