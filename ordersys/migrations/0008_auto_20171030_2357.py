# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-10-30 20:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ordersys', '0007_auto_20171017_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='pickup_point',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='ordersys.PickupPoint', verbose_name='пункт самовывоза'),
        ),
    ]