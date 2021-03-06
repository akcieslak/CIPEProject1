#Proposal1 - the comparison between polarity of the splice (4 behind and 4 before) and the whole sentence

import enchant
import nltk
from nltk.corpus import stopwords
from textblob.classifiers import NaiveBayesClassifier
import operator
import re
from textblob import TextBlob
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
#sentences = re.split(r' *[\.\?!][\'"\)\]]* *', text)
sentences = text.split(".")



def findWord(go, writer):
    while go == True:
        word = raw_input("Please enter word: ")
        if word == "exit":
            go = False
            break
        if word in DICTIONARY:
            writer.writerow([word, DICTIONARY[word].getAvgPol(), DICTIONARY[word].getAvgSub()])
    return 

def findGroup(go, writer):
    while go == True:
        group = raw_input("Please enter word/list: ")
        if group == "exit":
            go = False
            break
        group = group.split()
        pol = 0
        sub = 0
        count = 0
        for word in group:
            if word in DICTIONARY:
                count += 1
                pol += DICTIONARY[word].getAvgPol()
                sub += DICTIONARY[word].getAvgSub()
        if count == 0:
            avgPol = 0
            avgSub = 0
        else:
            avgPol = pol/(count)
            avgSub = sub/(count)
        writer.writerow([group, avgPol, avgSub])

    return 
        

def makeString(part):
    string = ""
    for element in part:
        string += " " + element
    return string

def partOfSpeech(text):
    tokenize = nltk.word_tokenize(text)
    return nltk.pos_tag(tokenize)


def getSplice(sentenceTuple): 
    sentenceIndex = sentenceTuple[0]
    wordIndex = sentenceTuple[1] 
    sentence = sentences[sentenceIndex]
    sentence = sentence.split()
    lengthS = len(sentence) - 1
    if (lengthS <= 4):
        splice = sentence
    elif (lengthS - wordIndex >= 4 and wordIndex - 0 >= 4):
        splice = sentence[wordIndex - 4 : wordIndex + 5]
    elif (lengthS - wordIndex >= 4 and wordIndex - 0 < 4):
        splice = sentence[0 : wordIndex + 5]
    else:
        splice = sentence[wordIndex - 4 : lengthS + 1]

    splice = makeString(splice)
    return str(splice)

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
with open('output.csv', 'wb') as c:
    writer = csv.writer(c)
    writer.writerow(['Word', 'Count', 'Sentence', 'Splice', 'Polarity', 'Sentence Pol', 'Subjectivity', 'Avg Polarity', 'Avg Whole Pol', 'Avg Subjectivity','Location'])
    while k < SIZE:
        polarSum = 0
        subjectSum = 0
        wholeSum = 0

        for spot in topWords[k].getSentenceArray():
            splice = getSplice(spot)
            whole = sentences[spot[0]]
            wholePol = TextBlob(whole.decode('utf-8')).polarity
            polarity = TextBlob(splice.decode('utf-8')).polarity
            subjectivity = TextBlob(splice.decode('utf-8')).subjectivity
            polarSum += polarity
            subjectSum += subjectivity
            wholeSum += wholePol
            writer.writerow([str(topWords[k].getWord()), str(topWords[k].getCount()), sentences[spot[0]], str(splice), str(polarity), str(wholePol), str(subjectivity)])


        topWords[k].setAvgPol(polarSum/topWords[k].getCount())
        topWords[k].setAvgSub(subjectSum/topWords[k].getCount())

        writer.writerow([" ", " ", " ", " ", " ", " ", " ", str(polarSum/topWords[k].getCount()),
                         str(wholeSum/topWords[k].getCount()), str(subjectSum/topWords[k].getCount()), str(topWords[k].getSentenceArray())])
        k += 1
c.close()

with open('proposal1.csv', 'wb') as k:
    writer = csv.writer(k)
    writer.writerow(['Word','Average Polarity', 'Average Subjectivity'])
    findGroup(True, writer)

