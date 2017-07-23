# -*- coding: utf-8 -*-
"""
Created on Fri May 19 07:24:06 2017

@author: manuj
"""
import datetime
from django.utils import timezone
from dateutil.parser import parse
import datefinder
import difflib

import time
import numpy as np
import pandas as pd

from MovieScraper import MovieScraper
from MovieListCleaner import MovieListCleaner
from .models import Movie
from django.db.models import Max
from django.db.models import Min
from django.utils import timezone
import imdb
import re
from imdb._exceptions import IMDbDataAccessError, IMDbParserError



class Utils:
    
    MAX_SCRAP_PAGES = 100
    INIT_SCRAP_TIME = 30 #days

    @classmethod
    def convert_timezone_aware(self,x):
        if isinstance(x,datetime.datetime):
            return timezone.make_aware(x)
        else:
            return x

    # @transaction.atomic
    @classmethod
    def scrape_and_add_movies(self):
        #Actions to be done here
        if Movie.objects.all().count()>0:
            post_max_date = timezone.make_naive(Movie.objects.latest('post_date').post_date)
        else:
            post_max_date = datetime.datetime.now() - datetime.timedelta(self.INIT_SCRAP_TIME)
        movie_scraped = MovieScraper()
        movie_scraped.scrape_site(self.MAX_SCRAP_PAGES, post_max_date)
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
            movie_df['release_date'] = movie_df['release_date'].map(self.convert_timezone_aware, na_action = 'ignore')
            movie_df['date_time'] = movie_df['date_time'].map(self.convert_timezone_aware, na_action = 'ignore')
            movie_df['post_date'] = movie_df['post_date'].map(self.convert_timezone_aware, na_action = 'ignore')
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
        counter = 0
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
                        counter = counter+1
                else:
                    m = Movie(**movie)
                    m.save()
                    counter = counter+1

        return counter

    # def update_all_ratings():
    #     #for debug only
    #     movies = Movie.objects.filter(movie_read = False)
    #     # Create the object that will be used to access the IMDb's database.
    #     ia = imdb.IMDb() # by default access the web.
    #     counter = 0
    #     for movie in movies:
    #         print("movie name: {}".format(movie.name))
    #         print("movie link: {}".format(movie.imdb_link))
    #         movie_info, imdb_link_present = get_imdb_info(movie.imdb_link,movie.name,ia)
    #         if movie_info:
    #             if 'rating' in movie_info.keys():
    #                 print ("new rating: {} <--- old rating: {}".format(movie_info['rating'],movie.imdb_rating))
    #             else:
    #                 print("no ratings")
    #             if 'votes' in movie_info.keys():
    #                 print ("new votes: {} <--- old votes: {}".format(movie_info['votes'],movie.imdb_votes))
    #             else:
    #                 print ("no votes")
    #             counter = counter +1
    #             #For Debug only
    #             # movie.movie_read = True
    #             # movie.save()
    #     return counter

    # @transaction.atomic
    @classmethod
    def update_all_ratings(self):
        movies = Movie.objects.filter(movie_read = False)
        print("in update: count of movie {}".format(movies.count()))
        # Create the object that will be used to access the IMDb's database.
        ia = imdb.IMDb() # by default access the web.
        counter = 0
        for movie in movies:
            print("movie name: {}".format(u''.join(movie.name).encode('utf-8').strip()))
            print("movie link: {}".format(u''.join(movie.imdb_link).encode('utf-8').strip()))
            movie_info, imdb_link_present = self.get_imdb_info(movie.imdb_link,movie.name,ia)
            if movie_info:
                if 'rating' in movie_info.keys():
                    movie.imdb_rating = movie_info['rating']
                if 'votes' in movie_info.keys():
                    movie.imdb_votes = movie_info['votes']
                if 'plot' in movie_info.keys():
                    movie.plot = movie_info['plot']
                if not imdb_link_present:
                    movie.imdb_link = ia.get_imdbURL(movie_info)
                movie.datetime = timezone.make_aware(datetime.datetime.now())
                movie.save()
                print ("movie rating: {}".format(movie.imdb_rating))
                print ("movie votes: {}".format(movie.imdb_votes))
                counter = counter +1
        return counter

    @classmethod
    def get_imdb_info(self,imdb_link,imdb_name,ia):
        match = re.search(r'^https?://[^\s]+/[^\s]+/tt([^\s]+)$', imdb_link.strip('/'))
        if match is not None:
            id = match.group(1)
            try:
                movie = ia.get_movie(id)
                return movie, True
            except IMDbParserError as e:
                result_set = ia.search_movie(imdb_name)
                if len(result_set)>0:
                    return ia.search_movie(imdb_name)[0], False
                else:
                    return False, False 
        else:
            result_set = ia.search_movie(imdb_name)
            if len(result_set)>0:
                return ia.search_movie(imdb_name)[0], False
            else:
                return False, False

    @classmethod
    def remove_duplicates_in_db(self):
        df = pd.DataFrame(list(Movie.objects.all().values()))
        movie_cleaner = MovieListCleaner(df)
        df = movie_cleaner.remove_duplicates_model(df)
        id_list = df.id.tolist()
        duplicates = Movie.objects.exclude(id__in = id_list).delete()
        #Movie query to delete all ids which are not in this list
        # print(df.id)
        return duplicates[0]

    # @commit_on_success
    @classmethod
    def update_release_type(self):
        movies = Movie.objects.filter(release_type="")
        movie_scraper = MovieScraper()
        for movie in movies:
            movie.release_type = movie_scraper.find_release_type_from_name(movie.release_name)
            movie.save()
        return movies.count()

