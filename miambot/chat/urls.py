from django.urls import path

from . import views

f = open(".token")
token = f.readline()
f.close()

urlpatterns = [
    path('', views.index, name='index'),
    #path('k7g0rrrbdmxwphqt0i7u', views.bot, name='webhook')
    path(token, views.bot, name='webhook')
]