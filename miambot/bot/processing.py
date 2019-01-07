class Processor():
    
    def proc(self, bot, answer):
        msgType = bot.getPredicate('type')
        print(msgType)
        if(msgType in "answer"):
            return answer
        else:
            food = bot.getPredicate('food')
            drink = bot.getPredicate('drink')
            print(food)
            print(drink)
            return '{"food": '+food+', "drink": '+drink+'}'