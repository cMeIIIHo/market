# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-24 15:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0027_auto_20170205_2340'),
    ]

    operations = [
        migrations.AddField(
            model_name='option_name',
            name='appearance_in_filters',
            field=models.CharField(blank=True, choices=[('1 col', 'значения в один столбец'), ('2 col', 'значения в два столбца'), ('interval', 'интервал от мин до макс')], max_length=70),
        ),
        migrations.AlterField(
            model_name='option_name',
            name='data_type',
            field=models.CharField(blank=True, choices=[('int', 'Целое число'), ('float', 'Десятичная дробь'), ('text', 'Текст')], max_length=20),
        ),
    ]
