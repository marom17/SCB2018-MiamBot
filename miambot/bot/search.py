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
        tagged = nltk.pos_tag(tokens) ## (word, type)
        toSearch = []
        p = nltk.PorterStemmer()

        for t in tagged:
            if(t[1] in TOKEEP):
                toSearch.append(p.stem(t[0].lower()))## Remove plurial

        for k in data['food-items']:
            allMatch = False
            ## We search if the food name have all the word that we search
            for w in toSearch:
                if(re.search(w, k['name'], re.IGNORECASE)):
                    allMatch = True
                else:
                    allMatch = False
                    ## We go out of the loop if there is 1 missmatch
                    break
            if(allMatch):
                if(food and not k['liquid']):
                    matching.append(k)

                elif(not food and k['liquid']):
                    matching.append(k)

        return matching