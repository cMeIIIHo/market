# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-05 17:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20170104_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sub_type',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.Sub_type'),
        ),
    ]
