# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-18 11:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('year', models.IntegerField()),
                ('genre', models.CharField(max_length=200)),
                ('imdb_rating', models.FloatField()),
                ('imdb_votes', models.BigIntegerField()),
                ('rt_critics', models.CharField(max_length=200)),
                ('plot', models.TextField()),
                ('starring', models.CharField(max_length=500)),
                ('director', models.CharField(max_length=100)),
                ('imdb_link', models.URLField(max_length=500)),
                ('rt_link', models.URLField(max_length=500)),
                ('post_link', models.URLField(max_length=500)),
                ('release_name', models.CharField(max_length=300)),
                ('release_date', models.CharField(max_length=100)),
                ('thumbnail_link', models.URLField(max_length=500)),
                ('date_time', models.DateTimeField()),
                ('trailer_link', models.URLField(max_length=500)),
                ('tomatometer', models.FloatField()),
                ('rt_rating', models.FloatField()),
            ],
        ),
    ]
