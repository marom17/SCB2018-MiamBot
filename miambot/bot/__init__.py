import aiml
import os
import bot.config as cfg
from bot.processing import Processor


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

    def interact(self, msg, user, usrId):
        self.setPredicate('currentUserName', user)
        self.setPredicate('userId', usrId)
        self.setPredicate('type', 'answer')
        resp = self.respond(msg)
        resp = self.processor.proc(self, resp)
        return resp

if __name__ == "__main__":
    bot = MiamBot()
    # Press CTRL-C to break this loop
    while True:
        print(bot.respond(input("Enter your message >> ")))