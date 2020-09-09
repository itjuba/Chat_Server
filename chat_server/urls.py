
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url

from . import  views
urlpatterns = [
    path('',views.index,name='index'),
    path('users/',views.get_login_users,name='users'),
    url(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),

]
