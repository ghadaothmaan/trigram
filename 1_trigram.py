# -*- coding: utf-8 -*-
# encoding=utf8
from __future__ import unicode_literals
import re
from collections import defaultdict

countTwoWords = defaultdict(dict)
countThreeWords = defaultdict(lambda: defaultdict(dict))
probThreeWords = defaultdict(lambda: defaultdict(dict))
probTwoWords = defaultdict(lambda: defaultdict(dict))
countOneWord = defaultdict(dict)
words = []
file = open("output.txt",'w',encoding='utf-8')

def readFile(filename):
    with open(filename) as f:
        lines = f.readlines()
    str = ""
    # ignore lines staring with tags < >
    for line in lines:
        if line[0] != '<' and line[0] != '>':
            str = str + line

    return str

# calculates count
def calculateCount(str):
    # reads file into a set of unique words
    str = re.split('; |, |\*|\n|\s| ', str)
    global words
    global countOneWord
    words = set(str)
    print("words:", words)

    # initializing the dicts first
    for i in range(str.__len__() - 2):
        countThreeWords[str[i]][str[i + 1]][str[i + 2]] = 0
        countTwoWords[str[i]][str[i + 1]] = 0
        countOneWord[str[i]] = 0

    countOneWord[str[str.__len__() - 1]] = 1
    countOneWord[str[str.__len__() - 2]] = 1
    countTwoWords[str[str.__len__() - 2]][str[str.__len__() - 1]] = 1

    # then whenever a sentence is found, increasing its count
    for i in range(str.__len__() - 2):
        countThreeWords[str[i]][str[i + 1]][str[i + 2]] = countThreeWords[str[i]][str[i + 1]][str[i + 2]] + 1
        countTwoWords[str[i]][str[i + 1]] = countTwoWords[str[i]][str[i + 1]] + 1
        countOneWord[str[i]] = countOneWord[str[i]] + 1

    # then calculating probability according to markov trigram assumption, p(z|x,y) = c(x,y,z) / c(x,y)
    for i in range(str.__len__() - 2):
        probThreeWords[str[i]][str[i + 1]][str[i + 2]] = countThreeWords[str[i]][str[i + 1]][str[i + 2]] / \
                                                         countTwoWords[str[i]][str[i + 1]]
    # p(y|x) = c(x,y) / c(x)
    for i in range(str.__len__() - 1):
        probTwoWords[str[i]][str[i + 1]] = countTwoWords[str[i]][str[i + 1]] / countOneWord[str[i]]

    countOneWord = [(k, countOneWord[k]) for k in sorted(countOneWord, key=countOneWord.get, reverse=False)]


# gets probability of a word given two other words
def getTrigramProb(sentence):
    # splits and takes last two words
    *whatever, first, second = sentence.split()
    res = defaultdict(dict)

    for third in countThreeWords[first][second]:
        res[third] = probThreeWords[first][second][third]

    # sorting the dict by probabilities value
    s = [(k, res[k]) for k in sorted(res, key=res.get, reverse=False)]
    res = []

    for key, value in s:
        res.append(key)

    # returns first 5 trigram predictions with highest probability
    return res[0:5]


def getBigramProb(second):
    res = defaultdict(dict)

    for third in countTwoWords[second]:
        res[third] = probTwoWords[second][third]

    s = [(k, res[k]) for k in sorted(res, key=res.get, reverse=False)]
    res = []

    for key, value in s:
        res.append(key)

    # returns first 5 bigram predictions with highest probability
    return res[0:5]


# sorts all words on count desc and returns first 5 results
def getUnigramProb():
    res = countOneWord
    s = sorted(res, key=lambda tup: tup[1])
    res = []

    for key, value in s:
        res.append(key)

    return res[0:5]


# gets probability of all words combinations
def getProbAll():
    for first in words:
        for second in words:
            for third in words:
                try:
                    if probThreeWords[first][second][third] > 0.3:
                        file.write("{} {} {} {}".format(first, second, third, probThreeWords[first][second][third]) + "\n")
                except:
                    x = "{} {} {} {}".format(first, second, third, 0)


calculateCount(readFile('corpus.txt'))
sentence = input("enter your sentence: ")
res = getTrigramProb(sentence)

# if trigram renders no resluts, either bigram or unigram should
if res.__len__() == 0:
    sentence = sentence.split()
    second = sentence[-1]
    res = getBigramProb(second)
if res.__len__() == 0:
    res = getUnigramProb()

for query in res:
    print(query)

# getProbAll()
# file.close()

# جهد عمل ألوان
# جهد عمل جهد