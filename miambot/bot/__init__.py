import aiml
import os
import bot.config as cfg
from .processing import Processor
import threading
import requests

f = open(".token")
token = f.readline().rstrip()
f.close()

PROD = os.getenv('PROD')

class MiamBot(aiml.Kernel):
    # Create the kernel and learn AIML files
    def __init__(self,properties=cfg.BOT_PROPERTIES):
        aiml.Kernel.__init__(self)
        #if os.path.isfile("bot.brn"):
        #   self.bootstrap(brainFile = "bot.brn")
        #else:
        self.init_bot()
        #   self.saveBrain("bot.brn")
        for p in properties:
            self.setBotPredicate( p, properties[p])

        ## Init the processing engine
        self.processor = Processor()

    def init_bot(self):
        for file in os.listdir(cfg.AIML_SET):
            ## Load all aiml files
            self.learn(os.path.join(cfg.AIML_SET,file))

    ## Function to interact with the bot
    def interact(self, msg, user, usrId, chatId):
        self.setPredicate('currentUserName', user, chatId)
        self.setPredicate('userId', usrId, chatId)
        self.setPredicate('type', 'answer', chatId)
        ## Handle first message from telegram
        if("/start" in msg):
            resp = self.respond("start", chatId)
            if(PROD):
                requests.post("https://api.telegram.org/bot"+token+"/sendMessage",data={"chat_id":chatId, "text":resp, "parse_mode":"HTML"})
        else:
            sessionData = self.getSessionData(chatId)
            resp = self.respond(msg, chatId).replace("/n",'\n')
            if(PROD):
                requests.post("https://api.telegram.org/bot"+token+"/sendMessage",data={"chat_id":chatId, "text":resp, "parse_mode":"HTML"})
            ## Send processing to background process
            t1 = threading.Thread(target=self.processor.proc(self, resp, chatId))
            t1.setDaemon(True)
            t1.start()

if __name__ == "__main__":
    bot = MiamBot()
    # Press CTRL-C to break this loop
    while True:
        print(bot.respond(input("Enter your message >> ")))
