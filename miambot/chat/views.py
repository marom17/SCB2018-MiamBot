from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from miambot.urls import chatbot

def index(request):
    return HttpResponse("Hello, world. You're at the chat index.")

@csrf_exempt
def bot(request):
    ## Accept only POST methods
    if request.method == 'POST':
        ## Get all information needed from telegram POST
        json_data = json.loads(request.body.decode('utf-8'))
        msg = json_data['message']['text']
        usrName = json_data['message']['from']['first_name']
        usrId = json_data['message']['from']['id']
        chatId = json_data['message']['chat']['id']
        chatbot.interact(msg, usrName, usrId, chatId)
        ## Return imediatly a respond to telegram
        return HttpResponse(status=200)
    return HttpResponse("Forbidden",status=403)


