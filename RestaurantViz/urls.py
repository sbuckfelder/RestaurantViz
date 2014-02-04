from django.conf.urls import patterns, include, url
from views import restVizApp

urlpatterns = patterns('',
    url(r'^RestaurantViz/$', restVizApp),
)
