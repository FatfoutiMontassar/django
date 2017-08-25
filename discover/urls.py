from django.conf.urls import url , include

from django.contrib import admin

from django.conf import settings

from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.discover , name='discover' ),
    url(r'^discover/$', views.discover , name='discover' ),
	url(r'^discover/(?P<idC>\w{0,50})/(?P<idP>\w{0,50})/$', views.discover , name='discover' ),
	url(r'^search/$', views.search , name='search' ),
    url(r'^addToWishList/$', views.addToWishList , name='addToWishList' ),
]
