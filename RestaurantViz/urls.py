from django.conf.urls import patterns, include, url
from views import restVizApp, testhtml

urlpatterns = patterns('',
    url(r'^RestaurantViz$', restVizApp),
    url(r'^test$', testhtml),
)
