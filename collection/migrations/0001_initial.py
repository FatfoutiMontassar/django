# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-08-10 09:25
from __future__ import unicode_literals

import collection.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0037_auto_20170717_1531'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('image', models.ImageField(null=True, upload_to=collection.models.renameC)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('isActive', models.NullBooleanField(choices=[(None, 'I do not know now'), (True, 'Yes I acknowledge this'), (False, 'No, I do not like this')], default=True)),
                ('products', models.ManyToManyField(blank=True, related_name='collecstions_products', to='shop.Product')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
