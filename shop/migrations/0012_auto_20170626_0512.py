# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-26 05:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_auto_20170626_0449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='store',
            name='description',
            field=models.TextField(),
        ),
    ]
