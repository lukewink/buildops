# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-22 03:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0002_auto_20170222_0337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='build',
            name='number',
            field=models.IntegerField(default=1),
        ),
    ]
