# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-20 23:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_auto_20170219_2123'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='image',
            field=models.ImageField(default=None, upload_to='teacher/%Y/%m', verbose_name='\u8bb2\u5e08\u5934\u50cf'),
        ),
    ]