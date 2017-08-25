from django.conf.urls import url , include

from django.contrib import admin

from django.conf import settings

from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^register',views.register , name='register'),
	url(r'^login',views.login , name='login'),
    url(r'^logout',views.logout , name='logout'),
    url(r'^settings/$',views.settings , name='settings'),
    url(r'^settings/picture/$', views.picture, name='picture'),
    url(r'^settings/upload_picture/$', views.upload_picture,
        name='upload_picture'),
    url(r'^settings/password/$', views.password, name='password'),
    url(r'^settings/message/$', views.message, name='message'),
]
