# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
import datetime
import json
from .forms import ScrapeForm, FilterForm, MarkReadForm, SearchMovieForm
from .models import Movie
from .MovieScraper import MovieScraper
from .MovieListCleaner import MovieListCleaner
from .Utils import Utils
import pandas as pd
import numpy as np
from django.db import transaction
from django.db.models import Max
from django.db.models import Min
from django.utils import timezone
from django.db.models import Q
import imdb
import re
from imdb._exceptions import IMDbDataAccessError, IMDbParserError

from .tasks import scrape_movies_task, update_ratings_task, test_task, remove_duplicates_task

from celery.result import AsyncResult
from django.views.decorators.csrf import csrf_exempt

MAX_SCRAP_PAGES = 100
INIT_SCRAP_TIME = 30 #days

color_dict = {1: "Red",
                2: "Pink",
                3: "Purple",
                4: "Deep-Purple",
                5: "Indigo",
                6: "Blue",
                7: "Light-Blue",
                8: "Cyan",
                9: "Teal",
                10: "Green",
                11: "Light-Green",
                12: "Lime",
                # 13: "Yellow",
                # 14: "Amber",
                # 15: "Orange",
                13: "Deep-Orange",
                14: "Brown",
                15: "Grey",
                16: "Blue-Grey"
}

# Create your views here.

'''
Landing page and it's actions
'''
def index(request):
    movie_list_id = (Movie.objects.filter(post_date__lte =timezone.now()-datetime.timedelta(days=30),movie_read = False, imdb_votes__gte = 3000)
                                    .order_by('-imdb_rating','-rt_rating','-post_date')
                                        .values_list('id', flat=True))
    print movie_list_id
    
    spot_light_movies = (Movie.objects.order_by('-imdb_rating','-rt_rating','-post_date').filter(id__in=list(movie_list_id[:4])))

    print spot_light_movies

    return render(request, 'movielistview/index.html', {"movie_count_unread":Movie.objects.filter(movie_read = False).count(),
                                                        "last_scrape_time" : timezone.make_naive(Movie.objects.latest('date_time').date_time),
                                                        "spotlight" : spot_light_movies
        })

@transaction.atomic
def scrape_movies(request):
    if request.method == 'POST':
        res = scrape_movies_task.delay()
        response_data = {}
        response_data['result'] = 'Scrape Started'
        response_data['task_id_scrape'] = res.id
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"result": "this isn't happening"}),
            content_type="application/json"
        )


@csrf_exempt
def poll_state_scrape(request):
    """ A view to report the progress to the user """
    data = 'Fail'
    if request.is_ajax():
        print('task_id_scrape' in request.POST.keys())
        if 'task_id_scrape' in request.POST.keys() and request.POST['task_id_scrape']:
            task_id_scrape = request.POST['task_id_scrape']
            task = AsyncResult(task_id_scrape)
            data = task.result or task.state
            print(task.result)
            print(task.state)
            response_data = {}
            # response_data['no_of_rows'] = Movie.objects.count()
            # response_data['no_of_unread_rows'] = Movie.objects.filter(movie_read = False).count()
            response_data['result'] = 'Scrape Completed'
            response_data['movie_count_added'] = task.result
            response_data['state'] = task.state
            # response_data['movie_count_added'] = movie_count_added
            # response_data['scraped_time'] = datetime.datetime.now().isoformat() #post.created.strftime('%B %d, %Y %I:%M %p')
            response_data['last_scrape_time'] = timezone.make_naive(Movie.objects.latest('date_time').date_time).isoformat() #post.created.strftime('%B %d, %Y %I:%M %p')
        else:
            response_data = 'No task_id_scrape in the request'
    else:
        response_data = 'This is not an ajax request'

    json_data = json.dumps(response_data)
    return HttpResponse(json_data, content_type='application/json')

@csrf_exempt
def update_ratings(request):
    if request.method == 'GET':
        res = update_ratings_task.delay()
        # res = test_task.delay()
        response_data = {}
        response_data['task_id_rating'] = res.id
        # response_data['no_of_rows_updated'] = no_of_rows_updated
        response_data['result'] = 'Update Started'
        # response_data['scraped_time'] = datetime.datetime.now().isoformat() #post.created.strftime('%B %d, %Y %I:%M %p')
        # response_data['last_scrap_time'] = timezone.make_naive(Movie.objects.latest('date_time').date_time).isoformat() #post.created.strftime('%B %d, %Y %I:%M %p')
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


@csrf_exempt
def poll_state_rating(request):
    """ A view to report the progress to the user """
    data = 'Fail'
    if request.is_ajax():
        print('task_id_rating' in request.POST.keys())
        if 'task_id_rating' in request.POST.keys() and request.POST['task_id_rating']:
            task_id_rating = request.POST['task_id_rating']
            task = AsyncResult(task_id_rating)
            data = task.result or task.state
            print(task.result)
            print(task.state)
            response_data = {}
            # response_data['no_of_rows'] = Movie.objects.count()
            # response_data['no_of_unread_rows'] = Movie.objects.filter(movie_read = False).count()
            response_data['result'] = 'Rating Completed'
            response_data['movie_rating_updated'] = task.result
            response_data['state'] = task.state
        else:
            response_data = 'No task_id_scrape in the request'
    else:
        response_data = 'This is not an ajax request'

    json_data = json.dumps(response_data)
    return HttpResponse(json_data, content_type='application/json')


@csrf_exempt
def remove_duplicates(request):
    if request.method == 'GET':
        res = remove_duplicates_task.delay()
        # res = test_task.delay()
        response_data = {}
        response_data['task_id_duplicate'] = res.id
        response_data['result'] = 'Removing Duplicates'

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"result": "this isn't happening"}),
            content_type="application/json"
        )


@csrf_exempt
def poll_state_duplicates(request):
    """ A view to report the progress to the user """
    data = 'Fail'
    if request.is_ajax():
        print('task_id_duplicate' in request.POST.keys())
        if 'task_id_duplicate' in request.POST.keys() and request.POST['task_id_duplicate']:
            task_id_duplicate = request.POST['task_id_duplicate']
            task = AsyncResult(task_id_duplicate)
            data = task.result or task.state
            print(task.result)
            print(task.state)
            response_data = {}
            # response_data['no_of_rows'] = Movie.objects.count()
            # response_data['no_of_unread_rows'] = Movie.objects.filter(movie_read = False).count()
            response_data['result'] = 'Removed Duplicates'
            response_data['duplicates_removed'] = task.result
            response_data['state'] = task.state
        else:
            response_data = 'No task_id_scrape in the request'
    else:
        response_data = 'This is not an ajax request'

    json_data = json.dumps(response_data)
    return HttpResponse(json_data, content_type='application/json')

def search_movies(request):
    if request.method == 'POST':
        search_movies_form = SearchMovieForm(request.POST)
        response_data = {}
        if search_movies_form.is_valid():
            
            condition_name = search_movies_form.cleaned_data['condition_name']
            movie_name = search_movies_form.cleaned_data['movie_name']
            condition_rating = search_movies_form.cleaned_data['condition_rating']
            rating = search_movies_form.cleaned_data['rating']
            condition_votes = search_movies_form.cleaned_data['condition_votes']
            votes = search_movies_form.cleaned_data['votes']
            condition_date = search_movies_form.cleaned_data['condition_date']
            date = search_movies_form.cleaned_data['date']
            
            print("name is {}".format(movie_name))
            print("rating is {}".format(rating))
            print("votes is {}").format(votes)
            print("date is {}").format(date)
            queryset = Movie.objects.all()
            print("count before filtering: {}".format(queryset.count()))
            if movie_name:
                if condition_name == "contains":
                    queryset = queryset.filter(name__icontains = movie_name)
                elif condition_name == "does not contain":
                    queryset = queryset.filter(~Q(name__icontains = movie_name))
            print("count after name: {}".format(queryset.count()))
            if rating:
                if condition_rating == "equal to":
                    queryset= queryset.filter(imdb_rating = rating)
                elif condition_rating == "less than":
                    queryset= queryset.filter(imdb_rating__lte = rating)
                elif condition_rating == "greater than":
                    queryset= queryset.filter(imdb_rating__gte = rating)
            print("count after rating: {}".format(queryset.count()))
            if votes:
                if condition_votes == "less than":
                    queryset = queryset.filter(imdb_votes__lte = votes)
                if condition_votes == "greater than":
                    queryset = queryset.filter(imdb_votes__gte = votes)
            print("count after votes: {}".format(queryset.count()))
            if date:
                if condition_date == "before":
                    queryset= queryset.filter(post_date__lte = timezone.now()-datetime.timedelta(days=date))

            response_data['result'] = queryset.count()
            response_data['search_id_array'] = list(queryset.values_list('id',flat=True))
            response_data['movie_list_name'] = list(queryset.values_list('name',flat=True))
            request.session['search_id_array'] = list(queryset.values_list('id',flat=True))
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


@csrf_exempt
def mark_read_bulk(request):
    if request.method == 'POST':
        id_array = request.session['search_id_array']
        response_data = {}
        print("search_id_array is {}".format(id_array))
        q = Movie.objects.filter(id__in = id_array).update(movie_read = True)

        response_data['result'] = 'mark read success'
        response_data['count'] = q
        # response_data['id_array'] = queryset.values_list('id',flat=True)
        # request.session['id_array'] = queryset.values_list('id',flat=True)
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

    else:
        return HttpResponse(
            json.dumps({"result": "this isn't happening"}),
            content_type="application/json"
        )

@csrf_exempt
def delete_bulk(request):
    if request.method == 'POST':
        id_array = request.session['search_id_array']
        response_data = {}

        print("search_id_array is {}".format(id_array))
        f = Movie.objects.filter(id__in = id_array).delete()
        print(f)
        response_data['result'] = 'delete success'
        response_data['count'] = f[0]
        # response_data['id_array'] = queryset.values_list('id',flat=True)
        # request.session['id_array'] = queryset.values_list('id',flat=True)
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

    else:
        return HttpResponse(
            json.dumps({"result": "this isn't happening"}),
            content_type="application/json"
        )

'''
View Movies Section

'''

def view_movies(request):
    movies = Movie.objects.all().order_by('-post_date')
    return render(request, 'movielistview/view_movies.html', {'movies': movies,'color_dict':color_dict})

def filter_movies(request):
    print(request)
    print(request.method)
    if not request.method == 'POST':
        # print("not POST")
        # print('filter-params' in request.session)
        if 'filter-params' in request.session:
            request.POST = request.session['filter-params']
            request.method = 'POST'


    if request.method == 'POST':
        filter_form = FilterForm(data=request.POST or None)
        request.session['filter-params'] = request.POST
        print("form initialised")
        print(filter_form)
        print(filter_form.is_valid())
        response_data = {'movies':''}
        if filter_form.is_valid():
            show_read = filter_form.cleaned_data['show_read']
            min_rating = filter_form.cleaned_data['min_rating']
            min_votes = filter_form.cleaned_data['min_votes']
            if show_read:
                # show_read = True
                movies = Movie.objects.filter(imdb_rating__gte = min_rating, imdb_votes__gte = min_votes).order_by('-post_date')
            else:
                # show_read = False
                movies = Movie.objects.filter(imdb_rating__gte = min_rating, imdb_votes__gte = min_votes, movie_read = show_read ).order_by('-post_date')
            response_data = {'movies':movies, 'show_read':show_read, 'min_rating':min_rating, 'min_votes':min_votes, 'color_dict':color_dict}
        else:
            movie = Movie()
            response_data = {'movies':movie,'color_dict':color_dict}
        return render(request, 'movielistview/view_movies.html', response_data)

def mark_read_movies(request):
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

