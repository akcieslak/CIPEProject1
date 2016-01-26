#Proposal2 - Using a different textblob than proposal1 and finding polarity of whole sentence
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



class Value:
    def __init__ (self, word, sentenceNum, pol):
        self.word = word
        self.count = 1
        self.sentenceArray = [(sentenceNum, pol)]
        self.avgPol = 0
        self.avgSub = 0

    def update(self, sentenceNum, pol):
        self.count += 1
        self.sentenceArray.append((sentenceNum, pol))

    def getCount(self):
        return self.count

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
    pol = TextBlob(sentences[i].decode('utf-8'), analyzer = NaiveBayesAnalyzer()).sentiment
    line = sentences[i].translate(PUNCTUATION)
    line = line.decode('utf-8')
    speech = partOfSpeech(line)
    for point in speech:
        lword = point[0].lower()
        lword = en.noun.singular(lword)
        if (i == 50 or i == 200 or i == 400):
            print "here"
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
                            DICTIONARY[lword].update(i, pol)
                        else:
                            temp = Value(lword, i, pol)
                            DICTIONARY[lword] = temp
                    

print "here 2"
cmpfun = operator.attrgetter("count")
sortedDict = sorted(DICTIONARY.values(), key=cmpfun, reverse = True)





print "here 3"
topWords = []
j = 0
while j < SIZE:
    topWords.append(sortedDict[j])
    j += 1


k = 0
print "here 4"
with open('proposal8.csv', 'wb') as c:
    writer = csv.writer(c)
    writer.writerow(['Word', 'Count', 'Sentence', 'Classification', 'Polarity Pos', 'Polarity Neg', 'Avg Polarity'])
    while k < SIZE:
        
        for spot in topWords[k].getSentenceArray():
            writer.writerow([str(topWords[k].getWord()), str(topWords[k].getCount()), sentences[spot[0]], spot[1][0],
                             spot[1][1], spot[1][2]])

    

        writer.writerow([" ", " ", " ", " ", " ", " ", " "])
        k += 1
c.close()


