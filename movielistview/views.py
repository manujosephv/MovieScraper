# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
import datetime
import json

# Create your views here.
def index(request):
    return render(request, 'movielistview/index.html', {})

def scrape_movies(request):
    if request.method == 'POST':
        scrape_form = request.POST.get('data')
        response_data = {}

        #Actions to be done here


        response_data['result'] = 'Scrape Completed'
        response_data['movie_count'] = "Movie Count"
        response_data['scraped_time'] = datetime.datetime.now().isoformat() #post.created.strftime('%B %d, %Y %I:%M %p')

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )