# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
import datetime
import json
from .forms import ScrapeForm
from .forms import FilterForm
from .forms import MarkReadForm
from .models import Movie
from MovieScraper import MovieScraper
from MovieListCleaner import MovieListCleaner
import pandas as pd
import numpy as np
from django.db import transaction
from django.db.models import Max
from django.db.models import Min
from django.utils import timezone

MAX_SCRAP_PAGES = 100
INIT_SCRAP_TIME = 30 #days

# Create your views here.
def index(request):
    return render(request, 'movielistview/index.html', {"movie_count_unread":Movie.objects.filter(movie_read = False).count(),
                                                        "last_scrap_time" : timezone.make_naive(Movie.objects.latest('date_time').date_time)
        })

@transaction.atomic
def scrape_movies(request):
    if request.method == 'POST':
        # scrape_form = ScrapeForm(request.POST)
        #Deleting all existing entries
        #Movie.objects.all().delete()
        movie_count_added = scrape_and_add_movies()
        # movie_count_added = 0
        response_data = {}
        response_data['no_of_rows'] = Movie.objects.count()
        response_data['no_of_unread_rows'] = Movie.objects.filter(movie_read = False).count()
        response_data['result'] = 'Scrape Completed'
        response_data['movie_count_added'] = movie_count_added
        response_data['scraped_time'] = datetime.datetime.now().isoformat() #post.created.strftime('%B %d, %Y %I:%M %p')
        response_data['last_scrap_time'] = timezone.make_naive(Movie.objects.latest('date_time').date_time).isoformat() #post.created.strftime('%B %d, %Y %I:%M %p')
        #response_data['debug_info2'] = Movie.objects.all().latest('post_date')

        return HttpResponse(
            json.dumps(response_data),
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
    if request.method == 'POST':
        filter_form = FilterForm(data=request.POST)
        print("form initialised")
        # print(filter_form.errors())
        print(filter_form.is_valid())
        response_data = {'movies':''}
        if filter_form.is_valid():
            #Actions to be done here
            #post_max_date = Movies.objects.all().aggregate(Max('post_date'))
            #post_max_date = datetime.datetime.now()- datetime.timedelta(days=40)
            #Scraping last x pages checking for new entries only
            show_read = filter_form.cleaned_data['show_read']
            min_rating = filter_form.cleaned_data['min_rating']
            min_votes = filter_form.cleaned_data['min_votes']

            print(show_read)
            print(min_rating)
            print(min_votes)
            #min_rating = filter_form.cleaned_data['min_rating']
            #min_votes = filter_form.cleaned_data['min_votes']
            # movies = Movie.objects.all().order_by('-post_date')
            # print(movies)
            #movies = Movie.objects.all().order_by('-post_date')
            if show_read == "Y":
                # show_read = True
                movies = Movie.objects.filter(imdb_rating__gte = min_rating, imdb_votes__gte = min_votes).order_by('-post_date')
            elif show_read == "N":
                show_read = False
                movies = Movie.objects.filter(imdb_rating__gte = min_rating, imdb_votes__gte = min_votes, movie_read = show_read ).order_by('-post_date')
            else:
                movies = Movie()
            
            response_data = {'movies':movies}
        return render(request, 'movielistview/view_movies.html', response_data)

def mark_read_movies(request):
    # print("in mark read")
    if request.method == 'POST':
        mark_read_form = MarkReadForm(request.POST)
        response_data = {}
        if mark_read_form.is_valid():
            
            post_id = mark_read_form.cleaned_data['post_id']
            checked = mark_read_form.cleaned_data['checked']
            print("Selected post id is {}".format(post_id))
            print("And it is checked? {}".format(checked))
            print("model before update: {}").format(Movie.objects.filter(id = post_id))
            if checked=="Y":
                movie_read = True
            else:
                movie_read = False
            Movie.objects.filter(id = post_id).update(movie_read = movie_read)
            # print("model before update: {}").format(Movie.objects.filter(id = post_id))
            response_data['result'] = 'Marked Read'

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

def convert_timezone_aware(x):
    if isinstance(x,datetime.datetime):
        return timezone.make_aware(x)
    else:
        return x

def scrape_and_add_movies():
    #Actions to be done here
    if Movie.objects.all().count()>0:
        post_max_date = timezone.make_naive(Movie.objects.latest('post_date').post_date)
    else:
        post_max_date = datetime.datetime.now() - datetime.timedelta(INIT_SCRAP_TIME)
    movie_scraped = MovieScraper()
    movie_scraped.scrape_site(MAX_SCRAP_PAGES, post_max_date)
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
        movie_df['release_date'] = movie_df['release_date'].map(convert_timezone_aware, na_action = 'ignore')
        movie_df['date_time'] = movie_df['date_time'].map(convert_timezone_aware, na_action = 'ignore')
        movie_df['post_date'] = movie_df['post_date'].map(convert_timezone_aware, na_action = 'ignore')
        #Make Key
        movie_df['key'] = movie_df[['name','year', 'genre', 'imdb_rating', 'imdb_votes','rt_critics','plot', 'starring','director', 
            'imdb_link','rt_link', 'post_link','release_name', 'release_type', 'release_date','thumbnail_link',
            'trailer_link', 'tomatometer','rt_rating','post_date']].apply(lambda row: ','.join(map(str, row)), axis=1)
        #print(movie_df.name)
        # print(movie_df.key.count())
        # print(len(movie_df.key.unique()))
    else:
        movie_df = pd.Dataframe()
    movie_dict = movie_df.to_dict('records')
    #replacing empty strings with None

    for movie in movie_dict:
        # print(timezone.make_naive(movie['post_date']))
        # print(timezone.make_naive(movie['post_date']) <= post_max_date)
        if isinstance(movie['post_date'], datetime.datetime):
            if timezone.make_naive(movie['post_date']) <= post_max_date:
                # print("Max post date")
                if not(Movie.objects.filter(key=movie['key']).exists()):
                    # print("new-saving")
                    m = Movie(**movie)
                    m.save()
            else:
                m = Movie(**movie)
                m.save()

    return len(movie_df.index)