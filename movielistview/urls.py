from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^scrape_movies/$', views.scrape_movies, name='scrape_movies'),
    url(r'^view_movies/$', views.view_movies, name='view_movies'),
    url(r'^filter_movies/$', views.filter_movies, name='filter_movies'),
    url(r'^mark_read_movies/$', views.mark_read_movies, name='mark_read_movies'),
    url(r'^update_ratings/$', views.update_ratings, name='update_ratings'),
    url(r'^poll_state/$', views.poll_state, name='poll_state'),
]

