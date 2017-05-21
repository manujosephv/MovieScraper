# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Movie(models.Model):
    name = models.CharField(max_length = 200)
    year = models.IntegerField()
    genre = models.CharField(max_length = 200)
    imdb_rating = models.FloatField(null=True, blank=True)
    imdb_votes = models.BigIntegerField(null=True, blank=True)
    rt_critics = models.CharField(max_length= 200, null=True, blank=True)
    plot = models.TextField(null=True, blank=True)
    starring = models.CharField(max_length = 500, null=True, blank=True)
    director = models.CharField(max_length = 100, null=True, blank=True)
    imdb_link = models.URLField(max_length = 500, null=True, blank=True)
    rt_link = models.URLField(max_length = 500, null=True, blank=True)
    post_link = models.URLField(max_length = 500, null=True, blank=True)
    release_name = models.CharField(max_length = 300)
    release_type = models.CharField(max_length = 300)
    release_date = models.CharField(max_length = 100, null=True, blank=True)
    thumbnail_link = models.URLField(max_length = 500)
    date_time = models.DateTimeField()
    post_date = models.DateTimeField()
    trailer_link = models.URLField(max_length = 500, null=True, blank=True)
    tomatometer = models.CharField(max_length = 5,null=True, blank=True)
    rt_rating = models.FloatField(null=True, blank=True)


    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name