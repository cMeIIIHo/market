# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-28 01:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0018_auto_20170128_0425'),
    ]

    operations = [
        migrations.RenameField(
            model_name='float_opt',
            old_name='is_filter_for_category',
            new_name='active_in',
        ),
        migrations.RenameField(
            model_name='int_opt',
            old_name='is_filter_for_category',
            new_name='active_in',
        ),
        migrations.RenameField(
            model_name='text_opt',
            old_name='is_filter_for_category',
            new_name='active_in',
        ),
    ]