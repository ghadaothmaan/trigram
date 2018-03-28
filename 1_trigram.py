import re
from collections import defaultdict

countTwoWords = defaultdict(dict)
countThreeWords = defaultdict(lambda: defaultdict(dict))
probThreeWords = defaultdict(lambda: defaultdict(dict))


def readFile(filename):
    with open(filename) as f:
        lines = f.readlines()
    str = ""

    # ignore lines staring with tags < >
    for line in lines:
        if line[0] != '<' and line[0] != '>':
            str = str + line

    return str

# dog cat bird fish

# calculates count
def calculateCount(str):
    str = re.split('; |, |\*|\n|\s| ', str)

    # initializing the dicts first
    for i in range(str.__len__() - 2):
        countThreeWords[str[i]][str[i + 1]][str[i + 2]] = 0
        countTwoWords[str[i]][str[i + 1]] = 0

    # then whenever a sentence is found, increasing its count
    for i in range(str.__len__() - 2):
        countThreeWords[str[i]][str[i + 1]][str[i + 2]] = countThreeWords[str[i]][str[i + 1]][str[i + 2]] + 1
        countTwoWords[str[i]][str[i + 1]] = countTwoWords[str[i]][str[i + 1]] + 1

    # then calculating probability according to markov trigram assumption
    # p(z|x,y) = c(x,y,z) / c(x,y)
    for i in range(str.__len__() - 2):
        probThreeWords[str[i]][str[i + 1]][str[i + 2]] = countThreeWords[str[i]][str[i + 1]][str[i + 2]] / countTwoWords[str[i]][str[i + 1]]


# gets probability of a word given two other words
def getProb(first, second):
    res = defaultdict(dict)

    for third in countThreeWords[first][second]:
        res[third] = probThreeWords[first][second][third]

    # sorting the dict by probabilities value
    s = [(k, res[k]) for k in sorted(res, key=res.get, reverse=False)]
    res = []
    print(s)

    for key, value in s:
        res.append(key)

    return res


calculateCount(readFile('/Users/gee/PycharmProjects/nlp_project/spacetoon.txt'))

try:
    res = getProb('لن', 'نستسلم')
    for query in res:
        print(query)
except:
    print("NO RESULTS")
