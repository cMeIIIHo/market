# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-17 18:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_auto_20170117_2032'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sale_card',
            old_name='pictute',
            new_name='picture',
        ),
    ]