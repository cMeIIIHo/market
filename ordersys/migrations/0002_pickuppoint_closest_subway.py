# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-09-14 20:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordersys', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pickuppoint',
            name='closest_subway',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
