# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-05 15:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0021_auto_20170203_0045'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='float_opt',
            name='active_in',
        ),
        migrations.RemoveField(
            model_name='int_opt',
            name='active_in',
        ),
        migrations.RemoveField(
            model_name='text_opt',
            name='active_in',
        ),
    ]
