import re

class Search():

    nofood = [0,4,5]

    @staticmethod
    def search(value, data, food):
        matching = []

        for k in data['food-items']:
            if(food and not k['liquid']):
                if(re.search(value, k['name'], re.IGNORECASE)):
                    matching.append(k)

            elif(not food and k['liquid']):
                if(re.search(value, k['name'], re.IGNORECASE)):
                    matching.append(k)

        return matching