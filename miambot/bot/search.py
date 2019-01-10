import os
import re
import nltk

TOKEEP = ["JJ", "JJR", "JJS", "NN", "NNS", "NNP", "NNPS"]

## Import the folder where are the data
nltk.data.path.append(os.path.join(os.path.dirname(__file__),"nltk_data"))

class Search():

    nofood = [0,4,5]

    @staticmethod
    def search(value, data, food):
        matching = []
        tokens = nltk.word_tokenize(value)
        tagged = nltk.pos_tag(tokens)
        toSearch = []

        for t in tagged:
            if(t[1] in TOKEEP):
                toSearch.append(t[0])
        print(toSearch)

        for k in data['food-items']:
            if(food and not k['liquid']):
                if(re.search(value, k['name'], re.IGNORECASE)):
                    matching.append(k)

            elif(not food and k['liquid']):
                if(re.search(value, k['name'], re.IGNORECASE)):
                    matching.append(k)

        return matching