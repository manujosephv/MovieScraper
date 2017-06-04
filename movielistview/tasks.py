from __future__ import absolute_import

from celery import task, current_task
from .Utils import Utils
# from some_project import my_intensive_task # need to change
# from my_app.models import my_model # need to change
import random


import time

@task(name='tasks.scrape_movies_task')
def scrape_movies_task():

    # What we return here, will be available as an argument
    # in the success callback function
    print "Scraping Movie Task"
    # time.sleep(20)
    utils = Utils()
    movie_count_added = utils.scrape_and_add_movies()
    print "Scrape Movie Task complete"
    return movie_count_added

@task(name='tasks.update_ratings_task')
def update_ratings_task():

    print "Update Ratings TaskA"
    utils = Utils()
    no_of_rows_updated = utils.update_all_ratings()
    print "Task finished successfully"
    return no_of_rows_updated

@task(name='tasks.delete_read_movies_task')
def delete_read_movies_task():
    print "Delete Task"
    Movie.objects.filter(post_date__lte =timezone.now()-datetime.timedelta(days=10),movie_read = True).delete()

@task(name='tasks.test_task')
def test_task():

    print "in test task"
    n=5
    """
    Brainless number crunching just to have a substantial task:
    """
    for i in range(n):
        
        # if(i%30 == 0):
        #     process_percent = int(100 * float(i) / float(n))
        #     current_task.update_state(state='PROGRESS',
        #                               meta={'process_percent': process_percent})
        time.sleep(1)
    return 32
