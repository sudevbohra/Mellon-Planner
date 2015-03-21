from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'mellonplanner.views.home'),
    url(r'^login', 'django.contrib.auth.views.login', {'template_name':'Login_Page.html'}),
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login'),
    url(r'^register/$', 'mellonplanner.views.register'),
    url(r'^myschedule/', 'mellonplanner.views.home'),
    url(r'^login/', 'mellonplanner.views.home'),                   
    #url(r'', 'mellonplanner.views.mellon'),
)
