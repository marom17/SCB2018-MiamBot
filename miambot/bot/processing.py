import os
import json
import bot.search
from .search import Search
import requests
import bot.foodConfig as fcg

f = open(".token")
token = f.readline().rstrip()
f.close()

class Processor():

    def __init__(self):
        ## Put the food data in the memory
        with open(os.path.join(os.path.dirname(__file__),"foodInfo/dataset-en.json"), "r") as read_file:
            self.data = json.load(read_file)

    def proc(self, bot, answer, chatId):
        msgType = bot.getPredicate('type', chatId)
        print(msgType)

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
                    #request.post("https://api.telegram.org/bot"+token+"/sendMessage",data={'chat_id':chatId, 'text':resp, 'parse_mode':'HTML'})
                ## Everything is found
                else:
                    resp = bot.respond("ALLFOUND", chatId)
                    #request.post("https://api.telegram.org/bot"+token+"/sendMessage",data={'chat_id':chatId, 'text':resp, 'parse_mode':'HTML'})

                ## Search the calories of the food
                self.getCalories(selected)
                
            ## Search in the database
            elif(msgType in "search"):
                toSearch = bot.getPredicate('search', chatId)
                matching = Search.search(toSearch, self.data, True)
                matching += Search.search(toSearch, self.data, False)
                ## Not found in database
                if(len(matching) == 0):
                    bot.setPredicate("notFoundList", toSearch, chatId)
                    resp = bot.respond("NOTFOUND", chatId)
                    #request.post("https://api.telegram.org/bot"+token+"/sendMessage",data={'chat_id':chatId, 'text':resp, 'parse_mode':'HTML'})
                ## Found in the database
                else:
                    resp = "Found in database:\n"
                    for f in matching:
                        resp += "* "+f['name']+"\n"
                    print(resp)
                    #request.post("https://api.telegram.org/bot"+token+"/sendMessage",data={'chat_id':chatId, 'text':resp, 'parse_mode':'HTML'})

    ## Select the food that is the most near the search
    def selectFood(self, tab, search, liquid):
        selected = None

        return selected

    def getCalories(self, found):
        for f in found:
            kcal = 0
            fCat = f['categories']
            fkcal = f['composition']['energy-kcal']['value']
            liquid = f['liquid']
            fgr = 0
            if(liquid == 0):
                # Fruit
                if("3/" in fCat):
                    frg = fcg.FRUITGR
                # Vegetables
                elif("7/" in fcat):
                    frg = fcg.VEGEG
                #Meat and Fish
                elif("15/" in fcat or "16/" in fcat):
                    frg = fcg.MEATG
                # Ceral and potatoes
                elif("12/" in fcat):
                    if("12/4" in fcat):
                        frg = fcg.POTG
                    else:
                        frg = fcg.CEREG  
                # Yogurth                  
                elif("6/" in fcat):
                    if("6/5" in fcat)
                        frg = fcg.YOGG
                    else:
                        frg = fcg.CHEESEG
                else:
                    frg = fcg.DEFAULTG
            else:
                fgr = 3.3
            
            kcal = fgr * fkcal
            print("%s of %s: %s kcal", fgr, f['name'], kcal)

        return None
            