# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-10-09 17:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordersys', '0004_auto_20170917_1841'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProxyUser',
        ),
    ]
