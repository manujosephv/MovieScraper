# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
import datetime
import json
from .forms import ScrapeForm
from .models import Movie
from MovieScraper import MovieScraper
from MovieListCleaner import MovieListCleaner
import pandas as pd
import numpy as np
from django.db import transaction


# Create your views here.
def index(request):
    return render(request, 'movielistview/index.html', {"movie_count":Movie.objects.count()})

@transaction.atomic
def scrape_movies(request):
    if request.method == 'POST':
        scrape_form = ScrapeForm(request.POST)
        response_data = {}
        if scrape_form.is_valid():
            #Actions to be done here
            scrape_pages = scrape_form.cleaned_data['scrape_pages']
            min_rating = scrape_form.cleaned_data['min_rating']
            min_votes = scrape_form.cleaned_data['min_votes']
            print('about to scrape' + str(scrape_pages) +" pages")
            movie_scraped = MovieScraper()
            movie_scraped.scrape_site(scrape_pages)
            movie_clean = MovieListCleaner(movie_scraped.movieScraped, min_rating,min_votes)
            movie_clean.clean_movie()
            movie_df = movie_clean.cleanMovieList
            print("scrape complete")
            #Deleting all existing entries
            Movie.objects.all().delete()
            #rename dataframe to match model
            cols = [ 'name','year', 'genre', 'imdb_rating', 'imdb_votes','rt_critics','plot', 'starring','director', 
                'imdb_link','rt_link', 'post_link','release_name', 'release_date','thumbnail_link',
                'date_time','trailer_link', 'tomatometer','rt_rating']
            movie_df.columns = cols
            print(movie_df.name)
            movie_df.replace(r'^\s+$', np.nan, regex=True, inplace=True)
            print(movie_df.name)
            movie_dict = movie_df.to_dict('records')
            #replacing empty strings with None

            for movie in movie_dict:
                m = Movie(**movie)
                m.save()

            response_data['no_of_rows'] = Movie.objects.count()
            response_data['result'] = 'Scrape Completed'
            response_data['movie_count'] = len(movie_df.index)
            response_data['scraped_time'] = datetime.datetime.now().isoformat() #post.created.strftime('%B %d, %Y %I:%M %p')

            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        else:
            return HttpResponse(
            json.dumps({"result": "invalid form"}),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"result": "this isn't happening"}),
            content_type="application/json"
        )

def view_movies(request):
    movies = Movie.objects.all()
    print(movies)
    return render(request, 'movielistview/view_movies.html', {'movies': movies})
#    return render(request, 'movielistview/page1.html', {})