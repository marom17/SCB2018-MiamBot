import aiml
import os
import bot.config as cfg
from .processing import Processor
import threading



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

        self.processor = Processor()

    def init_bot(self):
        for file in os.listdir(cfg.AIML_SET):
            self.learn(os.path.join(cfg.AIML_SET,file))

    def interact(self, msg, user, usrId, chatId):
        sessionData = self.getSessionData(chatId)
        self.setPredicate('currentUserName', user, chatId)
        self.setPredicate('userId', usrId, chatId)
        self.setPredicate('type', 'answer', chatId)
        resp = self.respond(msg, chatId)
        t1 = threading.Thread(target=self.processor.proc(self, resp, chatId))
        t1.setDaemon(True)
        t1.start()
        return resp

if __name__ == "__main__":
    bot = MiamBot()
    # Press CTRL-C to break this loop
    while True:
        print(bot.respond(input("Enter your message >> ")))