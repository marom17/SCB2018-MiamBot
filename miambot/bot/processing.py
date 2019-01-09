import os
import json
from .search import Search

class Processor():

    def __init__(self):

        with open(os.path.join(os.path.dirname(__file__),"foodInfo/dataset-en.json"), "r") as read_file:
            self.data = json.load(read_file)

    def proc(self, bot, answer, chatId):
        msgType = bot.getPredicate('type', chatId)
        print(msgType)
        if(msgType not in "answer"):
            food = bot.getPredicate('food', chatId)
            drink = bot.getPredicate('drink', chatId)
            Search.search('apple', self.data, True, False)
            print(food)
            print(drink)