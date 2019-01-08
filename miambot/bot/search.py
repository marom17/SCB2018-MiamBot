import re

class Search():

    nofood = [0,4,5]

    @staticmethod
    def search(value, data, food):
        matching = []

        for k in data['food-items']:
            if(food and not k['liquid']):

                if(re.search("^"+value, k['name'], re.IGNORECASE)):
                    matching.append(k)
                    print(k['name'])
        print(len(matching))
        #print(matching)
        return 0