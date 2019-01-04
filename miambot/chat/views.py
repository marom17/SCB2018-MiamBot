from django.shortcuts import render
from django.http import HttpResponse

from miambot.urls import chatbot

def index(request):
    return HttpResponse("Hello, world. You're at the chat index.")

def bot(request):
    resp = chatbot.respond('hello')
    return HttpResponse(resp)


