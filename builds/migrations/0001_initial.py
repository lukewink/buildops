# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-26 00:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewBuild',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('application', models.CharField(max_length=200)),
                ('version', models.CharField(max_length=25)),
                ('branch', models.CharField(max_length=200)),
                ('revision', models.CharField(max_length=100)),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Build',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch', models.CharField(max_length=200)),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='Build time')),
                ('revision', models.CharField(max_length=100)),
                ('number', models.IntegerField(default=1)),
            ],
            options={
                'ordering': ('time',),
            },
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=25)),
                ('next_number', models.IntegerField(default=1)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='versions', to='builds.Application')),
            ],
        ),
        migrations.AddField(
            model_name='build',
            name='version',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='builds', to='builds.Version'),
        ),
        migrations.AlterUniqueTogether(
            name='version',
            unique_together=set([('application', 'version')]),
        ),
        migrations.AlterUniqueTogether(
            name='build',
            unique_together=set([('version', 'number')]),
        ),
    ]
