from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^scrape_movies/$', views.scrape_movies, name='scrape_movies'),
    url(r'^view_movies/$', views.view_movies, name='view_movies'),
]