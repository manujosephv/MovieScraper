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
from .MovieScraper import MovieScraper
from .MovieListCleaner import MovieListCleaner
from .Utils import Utils
import pandas as pd
import numpy as np
from django.db import transaction
from django.db.models import Max
from django.db.models import Min
from django.utils import timezone
import imdb
import re
from imdb._exceptions import IMDbDataAccessError, IMDbParserError

from .tasks import scrape_movies_task, update_ratings_task, test_task

from celery.result import AsyncResult
from django.views.decorators.csrf import csrf_exempt

MAX_SCRAP_PAGES = 100
INIT_SCRAP_TIME = 30 #days

# Create your views here.
def index(request):
    # return render(request, 'movielistview/index.html', {})
    return render(request, 'movielistview/index.html', {"movie_count_unread":Movie.objects.filter(movie_read = False).count(),
                                                        "last_scrape_time" : timezone.make_naive(Movie.objects.latest('date_time').date_time)
        })

@transaction.atomic
def scrape_movies(request):
    if request.method == 'POST':
        
        # utils = Utils()
        # movie_count_added = utils.scrape_and_add_movies()
        res = scrape_movies_task.delay()
        # res = test_task.delay()
        response_data = {}
        # response_data['no_of_rows'] = Movie.objects.count()
        # response_data['no_of_unread_rows'] = Movie.objects.filter(movie_read = False).count()
        response_data['result'] = 'Scrape Started'
        # response_data['movie_count_added'] = movie_count_added
        # response_data['scraped_time'] = datetime.datetime.now().isoformat() #post.created.strftime('%B %d, %Y %I:%M %p')
        # response_data['last_scrape_time'] = timezone.make_naive(Movie.objects.latest('date_time').date_time).isoformat() #post.created.strftime('%B %d, %Y %I:%M %p')
        response_data['task_id'] = res.id

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
def poll_state(request):
    """ A view to report the progress to the user """
    data = 'Fail'
    if request.is_ajax():
        print('task_id' in request.POST.keys())
        if 'task_id' in request.POST.keys() and request.POST['task_id']:
            task_id = request.POST['task_id']
            task = AsyncResult(task_id)
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
            response_data = 'No task_id in the request'
    else:
        response_data = 'This is not an ajax request'

    json_data = json.dumps(response_data)
    return HttpResponse(json_data, content_type='application/json')


def view_movies(request):
    movies = Movie.objects.all().order_by('-post_date')
    #print(movies)
    return render(request, 'movielistview/view_movies.html', {'movies': movies})
#    return render(request, 'movielistview/page1.html', {})

def filter_movies(request):
    print(request)
    print(request.method)
    if not request.method == 'POST':
        print("not POST")
        print('filter-params' in request.session)
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
            if show_read:
                # show_read = True
                movies = Movie.objects.filter(imdb_rating__gte = min_rating, imdb_votes__gte = min_votes).order_by('-post_date')
            else:
                # show_read = False
                movies = Movie.objects.filter(imdb_rating__gte = min_rating, imdb_votes__gte = min_votes, movie_read = show_read ).order_by('-post_date')
            response_data = {'movies':movies, 'show_read':show_read, 'min_rating':min_rating, 'min_votes':min_votes}
        else:
            movie = Movie()
            response_data = {'movies':movie}
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

@transaction.atomic
def update_ratings(request):
    if request.method == 'GET':
        # scrape_form = ScrapeForm(request.POST)
        #Deleting all existing entries
        #Movie.objects.all().delete()
        # no_of_rows_updated = update_all_ratings()
        # utils = Utils()
        # no_of_rows_updated = utils.update_all_ratings()
        no_of_rows_updated = update_ratings_task.delay()
        # movie_count_added = 0
        response_data = {}
        response_data['no_of_rows'] = Movie.objects.count()
        # response_data['no_of_rows_updated'] = no_of_rows_updated
        response_data['result'] = 'Update Completed'
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




def test_view(request):
    if request.method == 'GET':
        
        # Configure Task and Callbacks
        s = run_task.s()
        s.link(on_success_task.s())
        s.link_error(on_error_task.s())

        # Start Task asynchronously
        task_id = s.apply_async()



        response_data = {}
        response_data['result'] = 'Update Completed'
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"result": "this isn't happening"}),
            content_type="application/json"
        )





# def convert_timezone_aware(x):
#     if isinstance(x,datetime.datetime):
#         return timezone.make_aware(x)
#     else:
#         return x

# def scrape_and_add_movies():
#     #Actions to be done here
#     if Movie.objects.all().count()>0:
#         post_max_date = timezone.make_naive(Movie.objects.latest('post_date').post_date)
#     else:
#         post_max_date = datetime.datetime.now() - datetime.timedelta(INIT_SCRAP_TIME)
#     movie_scraped = MovieScraper()
#     movie_scraped.scrape_site(MAX_SCRAP_PAGES, post_max_date)
#     if len(movie_scraped.movieScraped.index) >0 :
#         movie_clean = MovieListCleaner(movie_scraped.movieScraped)
#         movie_clean.clean_movie()
#         movie_df = movie_clean.cleanMovieList
#         print("scrape complete")
#         #rename dataframe to match model
#         cols = [ 'name','year', 'genre', 'imdb_rating', 'imdb_votes','rt_critics','plot', 'starring','director', 
#             'imdb_link','rt_link', 'post_link','release_name', 'release_type', 'release_date','thumbnail_link',
#             'date_time','trailer_link', 'tomatometer','rt_rating','post_date']
#         movie_df.columns = cols
#         #print(movie_df.name)
#         movie_df.replace(r'^\s+$', np.nan, regex=True, inplace=True)
#         #Making Date-time Timezone aware
#         movie_df['release_date'] = movie_df['release_date'].map(convert_timezone_aware, na_action = 'ignore')
#         movie_df['date_time'] = movie_df['date_time'].map(convert_timezone_aware, na_action = 'ignore')
#         movie_df['post_date'] = movie_df['post_date'].map(convert_timezone_aware, na_action = 'ignore')
#         #Make Key
#         movie_df['key'] = movie_df[['name','year', 'genre', 'imdb_rating', 'imdb_votes','rt_critics','plot', 'starring','director', 
#             'imdb_link','rt_link', 'post_link','release_name', 'release_type', 'release_date','thumbnail_link',
#             'trailer_link', 'tomatometer','rt_rating','post_date']].apply(lambda row: ','.join(map(str, row)), axis=1)
#         #print(movie_df.name)
#         # print(movie_df.key.count())
#         # print(len(movie_df.key.unique()))
#     else:
#         movie_df = pd.Dataframe()
#     movie_dict = movie_df.to_dict('records')
#     #replacing empty strings with None

#     for movie in movie_dict:
#         # print(timezone.make_naive(movie['post_date']))
#         # print(timezone.make_naive(movie['post_date']) <= post_max_date)
#         if isinstance(movie['post_date'], datetime.datetime):
#             if timezone.make_naive(movie['post_date']) <= post_max_date:
#                 # print("Max post date")
#                 if not(Movie.objects.filter(key=movie['key']).exists()):
#                     # print("new-saving")
#                     m = Movie(**movie)
#                     m.save()
#             else:
#                 m = Movie(**movie)
#                 m.save()

#     return len(movie_df.index)

# # def update_all_ratings():
# #     #for debug only
# #     movies = Movie.objects.filter(movie_read = False)
# #     # Create the object that will be used to access the IMDb's database.
# #     ia = imdb.IMDb() # by default access the web.
# #     counter = 0
# #     for movie in movies:
# #         print("movie name: {}".format(movie.name))
# #         print("movie link: {}".format(movie.imdb_link))
# #         movie_info, imdb_link_present = get_imdb_info(movie.imdb_link,movie.name,ia)
# #         if movie_info:
# #             if 'rating' in movie_info.keys():
# #                 print ("new rating: {} <--- old rating: {}".format(movie_info['rating'],movie.imdb_rating))
# #             else:
# #                 print("no ratings")
# #             if 'votes' in movie_info.keys():
# #                 print ("new votes: {} <--- old votes: {}".format(movie_info['votes'],movie.imdb_votes))
# #             else:
# #                 print ("no votes")
# #             counter = counter +1
# #             #For Debug only
# #             # movie.movie_read = True
# #             # movie.save()
# #     return counter


# def update_all_ratings():
#     movies = Movie.objects.all()
#     # Create the object that will be used to access the IMDb's database.
#     ia = imdb.IMDb() # by default access the web.
#     counter = 0
#     for movie in movies:
#         movie_info, imdb_link_present = get_imdb_info(movie.imdb_link,movie.name,ia)
#         if movie_info:
#             if 'rating' in movie_info.keys():
#                 movie.imdb_rating = movie_info['rating']
#             if 'votes' in movie_info.keys():
#                 movie.imdb_votes = movie_info['votes']
#             if 'plot' in movie_info.keys():
#                 movie.plot = movie_info['plot']
#             if not imdb_link_present:
#                 movie.imdb_link = ia.get_imdbURL(movie_info)
#             movie.save()
#             counter = counter +1
#     return counter

# def get_imdb_info(imdb_link,imdb_name,ia):
#     match = re.search(r'^https?://[^\s]+/[^\s]+/tt([^\s]+)$', imdb_link.strip('/'))
#     if match is not None:
#         id = match.group(1)
#         try:
#             movie = ia.get_movie(id)
#             return movie, True
#         except IMDbParserError as e:
#             result_set = ia.search_movie(imdb_name)
#             if len(result_set)>0:
#                 return ia.search_movie(imdb_name)[0], False
#             else:
#                 return False, False 
#     else:
#         result_set = ia.search_movie(imdb_name)
#         if len(result_set)>0:
#             return ia.search_movie(imdb_name)[0], False
#         else:
#             return False, False
