from django.conf.urls import patterns, url

from .views import Database

urlpatterns = patterns('',
    # ex: /eventos/
    url(r'^database/$', Database.as_view(), name='database'),
)
