# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-23 16:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movielistview', '0008_auto_20170523_1930'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='show_read',
            new_name='movie_read',
        ),
    ]
