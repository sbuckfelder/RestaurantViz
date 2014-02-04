from django.conf.urls import patterns, include, url
from views import dummyTest

urlpatterns = patterns('',
    url(r'^tester/$', dummyTest),
)
