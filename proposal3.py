#Proposal3 - using the exp equation with the original textblob from Proposal1
import enchant
import nltk
from nltk.corpus import stopwords
import operator
import re
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import string
import csv
import en
import math

SIZE = 50
d = enchant.Dict("en_US")
f = open('allText.txt', 'r')
CACHEDSTOPWORDS = stopwords.words('english')
PUNCTUATION = string.maketrans(string.punctuation, ' ' * len(string.punctuation))

DICTIONARY = {}
POSITION = 0
           

splitFile = []
text = f.read()
sentences = text.split(".")

        

def makeString(part):
    string = ""
    for element in part:
        string += " " + element
    return string

def partOfSpeech(text):
    tokenize = nltk.word_tokenize(text)
    return nltk.pos_tag(tokenize)


def getWeightedPol(sentence, n, index):
    sentence = sentence.split()
    lengthS = len(sentence) - 1
    

    polSum = 0 
    i = 1
    while i <= n and i <= lengthS:
        pol = 0
        try: 
            splice = makeString(sentence[index - i : index + i])
            pol = TextBlob(splice.decode('utf-8')).polarity
        except Exception:
            pass
            print splice
            break
        work = math.exp((-i/3)) * pol 
        polSum += work
        i += 1
        
    return polSum
    
    

class Value:
    def __init__ (self, word, position, sentenceNum, sentenceInd):
        self.word = word
        self.count = 1
        self.positionArray = [position]
        self.sentenceArray = [(sentenceNum, sentenceInd)]
        self.avgPol = 0
        self.avgSub = 0

    def update(self, position, sentenceNum, sentenceInd):
        self.count += 1
        self.positionArray.append(position)
        self.sentenceArray.append((sentenceNum, sentenceInd))

    def getCount(self):
        return self.count

    def getPositionArray(self):
        return self.positionArray

    def getWord(self):
        return self.word

    def getSentenceArray(self):
        return self.sentenceArray

    def setAvgPol(self, avg):
        self.avgPol = avg

    def getAvgPol(self):
        return self.avgPol

    def setAvgSub(self, avg):
        self.avgSub = avg

    def getAvgSub(self):
        return self.avgSub


for i in range(len(sentences) - 1):
    line = sentences[i].translate(PUNCTUATION)
    line = line.decode('utf-8')
    speech = partOfSpeech(line)
    r = 0
    for point in speech:
        lword = point[0].lower()
        POSITION += 1
        lword = en.noun.singular(lword)
        if lword not in CACHEDSTOPWORDS:
            if lword != '' and lword != "re":
                if (d.check(lword) and len(lword) > 1):
                    if ('VB' in point[1] and point[1] != 'VBP' or 'NN' in point[1] ):
                        try:
                            lword = en.verb.present(lword)
                            lword = en.verb.infinitive(lword)
                        except Exception:
                            pass
                        if (lword in DICTIONARY):
                            DICTIONARY[lword].update(POSITION, i, r)
                        else:
                            temp = Value(lword, POSITION, i, r)
                            DICTIONARY[lword] = temp
                    
        r += 1


cmpfun = operator.attrgetter("count")
sortedDict = sorted(DICTIONARY.values(), key=cmpfun, reverse = True)






topWords = []
j = 0
while j < SIZE:
    topWords.append(sortedDict[j])
    j += 1


k = 0
with open('proposal3.csv', 'wb') as c:
    writer = csv.writer(c)
    writer.writerow(['Word', 'Count', 'Sentence', 'Polarity', 'Avg Polarity'])
    while k < SIZE:
        polarSum = 0

        for spot in topWords[k].getSentenceArray():
            index = spot[1] #This will give the sentence index
            sentence = sentences[spot[0]]
            pol = getWeightedPol(sentence, 5, index)
            
            polarSum += pol
            writer.writerow([str(topWords[k].getWord()), str(topWords[k].getCount()), sentences[spot[0]], str(pol)])

        topWords[k].setAvgPol(polarSum/topWords[k].getCount())

        writer.writerow([" ", " ", " ", " ", str(polarSum/topWords[k].getCount())])
        k += 1
        
c.close()


