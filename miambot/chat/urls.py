from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('k7g0rrrbdmxwphqt0i7u'+'/test', views.bot, name='index')
]