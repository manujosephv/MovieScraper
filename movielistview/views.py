# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
import datetime
import json
from .forms import ScrapeForm
from .forms import FilterForm
from .models import Movie
from MovieScraper import MovieScraper
from MovieListCleaner import MovieListCleaner
import pandas as pd
import numpy as np
from django.db import transaction
from django.db.models import Max
from django.db.models import Min
from django.utils import timezone


# Create your views here.
def index(request):
    return render(request, 'movielistview/index.html', {"movie_count":Movie.objects.count()})

@transaction.atomic
def scrape_movies(request):
    if request.method == 'POST':
        scrape_form = ScrapeForm(request.POST)
        response_data = {}
        if scrape_form.is_valid():
            #Deleting all existing entries
            Movie.objects.all().delete()

            #Actions to be done here
            if Movie.objects.all().count()>0:
                post_max_date = timezone.make_naive(Movie.objects.latest('post_date').post_date)
            else:
                post_max_date = datetime.datetime.now() - datetime.timedelta(30)
            #Scraping last x pages checking for new entries only
            scrape_pages = scrape_form.cleaned_data['scrape_pages']
            #min_rating = scrape_form.cleaned_data['min_rating']
            #min_votes = scrape_form.cleaned_data['min_votes']
            print('about to scrape' + str(scrape_pages) +" pages")
            movie_scraped = MovieScraper()
            movie_scraped.scrape_site(scrape_pages, post_max_date)
            if len(movie_scraped.movieScraped.index) >0 :
                movie_clean = MovieListCleaner(movie_scraped.movieScraped)
                movie_clean.clean_movie()
                movie_df = movie_clean.cleanMovieList
                print("scrape complete")
                #rename dataframe to match model
                cols = [ 'name','year', 'genre', 'imdb_rating', 'imdb_votes','rt_critics','plot', 'starring','director', 
                    'imdb_link','rt_link', 'post_link','release_name', 'release_type', 'release_date','thumbnail_link',
                    'date_time','trailer_link', 'tomatometer','rt_rating','post_date']
                movie_df.columns = cols
                #print(movie_df.name)
                movie_df.replace(r'^\s+$', np.nan, regex=True, inplace=True)
                #Making Date-time Timezone aware
                movie_df['release_date'] = movie_df['release_date'].map(lambda x: timezone.make_aware(x))
                movie_df['date_time'] = movie_df['date_time'].map(lambda x: timezone.make_aware(x))
                movie_df['post_date'] = movie_df['post_date'].map(lambda x: timezone.make_aware(x))
                #Make Key
                movie_df['key'] = movie_df[['name','year', 'genre', 'imdb_rating', 'imdb_votes','rt_critics','plot', 'starring','director', 
                    'imdb_link','rt_link', 'post_link','release_name', 'release_type', 'release_date','thumbnail_link',
                    'trailer_link', 'tomatometer','rt_rating','post_date']].apply(lambda row: ','.join(map(str, row)), axis=1)
                #print(movie_df.name)
                print(movie_df.key.count())
                print(len(movie_df.key.unique()))
            else:
                movie_df = pd.Dataframe()
            movie_dict = movie_df.to_dict('records')
            #replacing empty strings with None

            for movie in movie_dict:
                m = Movie(**movie)
                m.save()

            response_data['no_of_rows'] = Movie.objects.count()
            response_data['result'] = 'Scrape Completed'
            response_data['movie_count_added'] = len(movie_df.index)
            response_data['scraped_time'] = datetime.datetime.now().isoformat() #post.created.strftime('%B %d, %Y %I:%M %p')
            response_data['debug_info1'] = Movie.objects.latest('post_date').post_date.isoformat()
            #response_data['debug_info2'] = Movie.objects.all().latest('post_date')

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
    movies = Movie.objects.all().order_by('-post_date')
    #print(movies)
    return render(request, 'movielistview/view_movies.html', {'movies': movies})
#    return render(request, 'movielistview/page1.html', {})

def filter_movies(request):
    print("Duplicate Removing")
    movies = Movie.objects.all().order_by('-post_date')
    #print(movies)
    
    for row in Movie.objects.all():
        if Movie.objects.filter(key=row.key).count()>1:
             print(row)
    return render(request, 'movielistview/view_movies.html', {'movies': movies})
    # if request.method == 'POST':
    #     filter_form = FilterForm(request.POST)
    #     response_data = {}
    #     if scrape_form.is_valid():
    #         #Actions to be done here
    #         #post_max_date = Movies.objects.all().aggregate(Max('post_date'))
    #         post_max_date = datetime.datetime.now()- datetime.timedelta(days=40)
    #         #Scraping last x pages checking for new entries only
    #         show_read = scrape_form.cleaned_data['show_read']
    #         min_rating = scrape_form.cleaned_data['min_rating']
    #         min_votes = scrape_form.cleaned_data['min_votes']

    #         print(show_read)
    #         print(min_rating)
    #         print(min_votes)
    #         #min_rating = scrape_form.cleaned_data['min_rating']
    #         #min_votes = scrape_form.cleaned_data['min_votes']
    #         # movies = Movie.objects.all().order_by('-post_date')
    #         # print(movies)
    #         movies = Movie.objects.all().order_by('-post_date')
    #         return render(request, 'movielistview/view_movies.html', {'movies': movies})

