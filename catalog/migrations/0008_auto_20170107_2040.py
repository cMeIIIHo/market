# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-07 17:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_auto_20170106_2225'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='float_opt',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='int_opt',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='option_name',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='text_opt',
            options={'ordering': ['name']},
        ),
    ]
