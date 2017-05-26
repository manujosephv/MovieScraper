# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import models
from django.contrib import admin

class MovieAdmin(admin.ModelAdmin):
	list_display = ('name', 'year', 'release_type', 'post_date', 'movie_read')
	ordering = ('-post_date',) # The negative sign indicate descendent order
	 
	# def view_homepage_link(self, obj):
	# 	return '<a href="%s" target="_blank">%s</a>' % (obj.homepage, obj.homepage,)
	#   	view_homepage_link.allow_tags = True
	#   	view_homepage_link.short_description = 'Homepage' # Optional

# Register your models here.
# admin.site.register(models.Movie)
admin.site.register(models.Movie,MovieAdmin)