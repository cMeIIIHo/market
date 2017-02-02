# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-27 21:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0014_auto_20170128_0011'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('opt_list', models.ManyToManyField(blank=True, to='catalog.Option_name')),
                ('parent_category', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.Category')),
            ],
        ),
    ]