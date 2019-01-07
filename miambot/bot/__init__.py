import aiml
import os
import bot.config as cfg


class MiamBot(aiml.Kernel):
    # Create the kernel and learn AIML files
    def __init__(self,properties=cfg.BOT_PROPERTIES):
        aiml.Kernel.__init__(self)
        #if os.path.isfile("bot.brn"):
        #   self.bootstrap(brainFile = "bot.brn")
        #else:
        self.init_bot()
        self.respond("load aiml b")
        #   self.saveBrain("bot.brn")
        for p in properties:
            self.setBotPredicate( p, properties[p])
    def interact(self, msg):
        return self.respond(msg)

    def init_bot(self):
        for file in os.listdir(cfg.AIML_SET):
            self.learn(os.path.join(cfg.AIML_SET,file))

if __name__ == "__main__":
    bot = MiamBot()
    # Press CTRL-C to break this loop
    while True:
        print(bot.respond(input("Enter your message >> ")))