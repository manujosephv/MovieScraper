from __future__ import absolute_import

from celery import task
from .Utils import Utils
# from some_project import my_intensive_task # need to change
# from my_app.models import my_model # need to change

import time

@task(name='tasks.scrape_movies_task')
def scrape_movies_task():

    # What we return here, will be available as an argument
    # in the success callback function
    print "doing task"
    time.sleep(20)
    utils = Utils()
    movie_count_added = utils.scrape_and_add_movies()
    print "finished task"
    return movie_count_added

@task(name='tasks.update_ratings_task')
def update_ratings_task():

    
    utils = Utils()
    no_of_rows_updated = utils.update_all_ratings()
    print "Task finished successfully"
    return no_of_rows_updated

@task(name='tasks.delete_read_movies_task')
def delete_read_movies_task():
    print "Task finished with error"