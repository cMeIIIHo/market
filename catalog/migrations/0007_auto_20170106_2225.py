# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-06 19:25
from __future__ import unicode_literals

import catalog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_auto_20170106_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spec_prod',
            name='code',
            field=models.IntegerField(default=catalog.models.get_code),
        ),
    ]
