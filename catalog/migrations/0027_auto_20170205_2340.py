# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-05 20:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0026_auto_20170205_2335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='option_name',
            name='data_type',
            field=models.CharField(blank=True, choices=[('int', 'Целое число'), ('float', 'Десятичная дробь'), ('text', 'Текст')], max_length=10),
        ),
    ]
