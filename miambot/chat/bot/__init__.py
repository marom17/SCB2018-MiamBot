import aiml

class MiamBot(aiml.Kernel):
    # Create the kernel and learn AIML files
    def __init__(self):
        aiml.Kernel.__init__(self)
        self.learn("aiml_files/startup.xml")
        self.respond("LOAD AIML B")

if __name__ == "__main__":
    bot = MiamBot()
    # Press CTRL-C to break this loop
    while True:
        print(bot.respond(input("Enter your message >> ")))