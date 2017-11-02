# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-11-02 18:58
from __future__ import unicode_literals

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('ordersys', '0008_auto_20171030_2357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, verbose_name='телефон'),
        ),
    ]
