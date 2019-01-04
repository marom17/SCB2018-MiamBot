import aiml
import os

AIML_SET = os.path.join(os.path.dirname(__file__),'aiml_files')

class MiamBot(aiml.Kernel):
    # Create the kernel and learn AIML files
    def __init__(self):
        aiml.Kernel.__init__(self)
        for file in os.listdir(AIML_SET):
            self.learn(os.path.join(AIML_SET,file) )
        self.respond("load aiml b")

    def interact(self, msg):
        print(msg)
        return self.respond(msg)

if __name__ == "__main__":
    bot = MiamBot()
    # Press CTRL-C to break this loop
    while True:
        print(bot.respond(input("Enter your message >> ")))