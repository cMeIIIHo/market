# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-02 21:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0020_auto_20170128_0510'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='pictute',
            new_name='picture',
        ),
        migrations.AlterField(
            model_name='spec_prod',
            name='amount',
            field=models.PositiveIntegerField(),
        ),
    ]
