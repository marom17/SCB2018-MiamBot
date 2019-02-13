from django.urls import path

from . import views

f = open(".token")
token = f.readline().rstrip()
f.close()

urlpatterns = [
    path('', views.index, name='index'),
    path(token, views.bot, name='webhook')
]
