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
        msg = json_data['message']['text']
        usrName = json_data['message']['from']['first_name']
        usrId = json_data['message']['from']['id']
        resp = chatbot.interact(msg, usrName, usrId)
        return HttpResponse(resp)
    return HttpResponse("Forbidden",status=403)


