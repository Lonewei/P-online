# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-03 23:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coursecomments',
            old_name='coures',
            new_name='course',
        ),
    ]
