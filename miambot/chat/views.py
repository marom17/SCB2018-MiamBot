from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from miambot.urls import chatbot

def index(request):
    return HttpResponse("Hello, world. You're at the chat index.")

@csrf_exempt
def bot(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        resp = chatbot.interact(json_data['message']['text'])
        return HttpResponse(resp)
    return HttpResponse("Forbidden",status=403)


