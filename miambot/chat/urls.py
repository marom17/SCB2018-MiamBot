from django.urls import path

from . import views

f = open('.token')
token = f.read()
f.close()

urlpatterns = [
    path('', views.index, name='index'),
    path(token+'/test', views.bot, name='index')
]