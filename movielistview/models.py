# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Movie(models.Model):
    name = models.CharField(max_length = 200)
    year = models.IntegerField()
    genre = models.CharField(max_length = 200)
    imdb_rating = models.FloatField()
    imdb_votes = models.BigIntegerField()
    rt_critics = models.CharField(max_length= 200)
    plot = models.TextField()
    starring = models.CharField(max_length = 500)
    director = models.CharField(max_length = 100)
    imdb_link = models.URLField(max_length = 500)
    rt_link = models.URLField(max_length = 500)
    post_link = models.URLField(max_length = 500)
    release_name = models.CharField(max_length = 300)
    release_date = models.CharField(max_length = 100)
    thumbnail_link = models.URLField(max_length = 500)
    date_time = models.DateTimeField()
    trailer_link = models.URLField(max_length = 500)
    tomatometer = models.FloatField()
    rt_rating = models.FloatField()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name