from django.conf.urls import url
from . import views

urlpatterns = [
    #render
    url(r'^$', views.index),
    url(r'^main$', views.main),



    #redirect
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout)
]