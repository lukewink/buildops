# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-22 06:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0003_auto_20170222_0344'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='build',
            options={'ordering': ('time',)},
        ),
        migrations.AlterField(
            model_name='build',
            name='time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Build time'),
        ),
    ]