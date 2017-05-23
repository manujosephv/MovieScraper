# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-22 04:53
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movielistview', '0003_auto_20170519_1859'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='key',
            field=models.CharField(default='*', max_length=5000),
        ),
        migrations.AddField(
            model_name='movie',
            name='movie_read',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='movie',
            name='movie_read_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='movie',
            name='post_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='movie',
            name='release_type',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='movie',
            name='genre',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='movie',
            name='name',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='movie',
            name='release_name',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='movie',
            name='year',
            field=models.IntegerField(default=0),
        ),
    ]