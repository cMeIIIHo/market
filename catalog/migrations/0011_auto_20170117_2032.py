# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-17 17:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_sale_card'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale_card',
            name='pictute',
            field=models.ImageField(blank=True, upload_to='sale_cards/'),
        ),
    ]
