# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-19 21:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_auto_20170217_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='name',
            field=models.CharField(max_length=50, verbose_name='\u6559\u5e08\u540d'),
        ),
    ]
