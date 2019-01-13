import os
import json
import bot.search
from .search import Search
import requests
import bot.foodConfig as fcg
import re

import bot.db as db

f = open(".token")
token = f.readline().rstrip()
f.close()

PROD = os.getenv('PROD')

class Processor():

    def __init__(self):
        ## Put the food data in the memory
        with open(os.path.join(os.path.dirname(__file__),"foodInfo/dataset-en.json"), "r") as read_file:
            self.data = json.load(read_file)

    def proc(self, bot, answer, chatId):
        msgType = bot.getPredicate('type', chatId)

        ## If the repsond is not an answer, we do some processing
        if(msgType not in "answer"):
            ## Search for food and drink for 
            if(msgType in ["food", "drink", "fooddrink"]):
                food = bot.getPredicate('food', chatId).split(',')
                drink = bot.getPredicate('drink', chatId).split(',')
                ## Remove the space at the begining of a string
                i = 0
                for f in food:
                    food[i] = f.lstrip()
                    i = i + 1
                i = 0
                for d in drink:
                    drink[i] = d.lstrip()
                    i = i + 1

                matching = []
                notFound = []
                selected = []

                if(msgType in "food"):
                    for f in food:
                        found = Search.search(f, self.data, True)
                        if(len(found) == 0):
                            notFound.append(f)
                        else:
                            matching.append(found)
                        selected.append(self.selectFood(found, food, False))
                elif(msgType in "drink"):
                    for d in drink:
                        found = Search.search(d, self.data, False)
                        if(len(found) == 0):
                            notFound.append(d)
                        else:
                            matching.append(found)
                        selected.append(self.selectFood(found, drink, True))
                else:
                    for f in food:
                        found = Search.search(f, self.data, True)
                        if(len(found) == 0):
                            notFound.append(f)
                        else:
                            matching.append(found)
                        selected.append(self.selectFood(found, food, False))
                    for d in drink :
                        found = Search.search(d, self.data, False)
                        if(len(found) == 0):
                            notFound.append(d)
                        else:
                            matching.append(found)
                        selected.append(self.selectFood(found, drink, True))

                ## Some food are not found
                if(len(notFound) != 0):
                    string = ""
                    for nf in notFound:
                        string+= nf+", "
                    string = string[:-2] # Remove the last coma space of the list
                    bot.setPredicate("notFoundList", string, chatId)
                    resp = bot.respond("NOTFOUND", chatId)
                    if(PROD):
                        requests.post("https://api.telegram.org/bot"+token+"/sendMessage",data={"chat_id":chatId, "text":resp, "parse_mode":"HTML"})
                ## Everything is found
                else:
                    resp = bot.respond("ALLFOUND", chatId)
                    if(PROD):
                        requests.post("https://api.telegram.org/bot"+token+"/sendMessage",data={"chat_id":chatId, "text":resp, "parse_mode":"HTML"})
                ## Search the calories of the food
                self.getCalories(selected, chatId)
                
            ## Search in the database
            elif(msgType in "search"):
                toSearch = bot.getPredicate('search', chatId)
                matching = Search.search(toSearch, self.data, True)
                matching += Search.search(toSearch, self.data, False)
                ## Not found in database
                if(len(matching) == 0):
                    bot.setPredicate("notFoundList", toSearch, chatId)
                    resp = bot.respond("NOTFOUND", chatId)
                    if(PROD):
                        requests.post("https://api.telegram.org/bot"+token+"/sendMessage",data={"chat_id":chatId, "text":resp, "parse_mode":"HTML"})
                ## Found in the database
                else:
                    resp = "Found in database:\n"
                    for f in matching:
                        resp += "* "+f['name']+"\n"
                    if(PROD):
                        requests.post("https://api.telegram.org/bot"+token+"/sendMessage",data={"chat_id":chatId, "text":resp, "parse_mode":"HTML"})

            elif(msgType in "tcal"):
                resp = "Your today consumption is " + str(db.DB.getCalories(chatId))
                print(resp)
                if(PROD):
                    requests.post("https://api.telegram.org/bot"+token+"/sendMessage",data={"chat_id":chatId, "text":resp, "parse_mode":"HTML"})
            
            elif(msgType in "7cal"):
                resp = "Your last days consumption is:\n"
                days = db.DB.getLast7Calories(chatId)
                if(PROD):
                    requests.post("https://api.telegram.org/bot"+token+"/sendMessage",data={"chat_id":chatId, "text":resp, "parse_mode":"HTML"})
                

    ## Select the food that is the most near the search
    def selectFood(self, tab, search, liquid):
        selected = None
        maxOccurence = 0
        percent = 0.0
        for f in tab:
            split = f['name'].split(',')
            first = split[0]
            occurence = 0.0
            for s in search:
                if(s.lower() in first.lower()):
                    occurence += len(s)
            percent = occurence/len(first)
            if(percent >= maxOccurence):
                maxOccurence = percent
                selected = f

        return selected

    ## Get the number of calories a product have
    ## We only search in the first part of a product name
    def getCalories(self, found, chatId):
        for f in found:
            kcal = 0
            fcat = f['categories']
            fkcal = float(f['composition']['energy-kcal']['value'])
            liquid = int(f['liquid'])
            fgr = 0
            ## Find the number of grams of a portion
            if(liquid == 0):
                # Fruit
                if(self.inCat('3/', fcat)):
                    fgr = fcg.FRUITGR
                # Vegetables
                elif(self.inCat('7/', fcat)):
                    fgr = fcg.VEGEG
                #Meat and Fish
                elif(self.inCat('15/', fcat) or self.inCat('16/', fcat)):
                    fgr = fcg.MEATG
                # Ceral and potatoes
                elif(self.inCat('12/', fcat)):
                    if(self.inCat('12/4', fcat)):
                        fgr = fcg.POTG
                    else:
                        fgr = fcg.CEREG  
                # Yogurth                  
                elif(self.inCat('6/', fcat)):
                    if(self.inCat('6/5', fcat)):
                        fgr = fcg.YOGG
                    else:
                        fgr = fcg.CHEESEG
                else:
                    fgr = fcg.DEFAULTG
            else:
                fgr = fcg.LIQDL
            kcal = (fgr/100.0) * fkcal
            db.DB.enterCalories(chatId, kcal)

        return None

    ## Find a food belong to a specific category or subcategory
    def inCat(self, toSearch, listCat):
        for cat in listCat:
            if(re.search(toSearch,cat,re.IGNORECASE)):
                return True
        return False
            
