# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-19 22:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_course_coures_org'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='degree',
            field=models.CharField(choices=[('cj', '\u521d\u7ea7'), ('zj', '\u4e2d\u7ea7'), ('gj', '\u9ad8\u7ea7'), ('dy', '\u5669\u68a6')], max_length=2, verbose_name='\u96be\u5ea6'),
        ),
    ]
