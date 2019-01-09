import re

class Search():

    nofood = [0,4,5]

    @staticmethod
    def search(value, data, food, searchFood):
        matching = []
        if(searchFood):
            toSearch = value
        else:
            toSearch ="^" + value

        for k in data['food-items']:
            if(food and not k['liquid']):
                if(re.search(toSearch, k['name'], re.IGNORECASE)):
                    matching.append(k)
                    print(k['name'])

            elif(not food and k['liquid']):
                if(re.search(toSearch, k['name'], re.IGNORECASE)):
                    matching.append(k)
                    print(k['name'])
                    
        return matching