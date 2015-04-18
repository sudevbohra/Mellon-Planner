from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'mellonplanner.views.home', name="home"),
    url(r'^getschedules/', 'mellonplanner.views.getschedules'),
    url(r'^getschedule/(?P<index>\d+)$', 'mellonplanner.views.getschedule', name="getschedule"),
    #url(r'', 'mellonplanner.views.mellon'),
)
