import pandas as pd
import sys
import re

inputName = sys.argv[1]
outputName = sys.argv[2]

df = pd.read_csv(inputName, header=None, usecols=[0,1])

wordsDict = {}

for index, row in df.iterrows():

    sourceWords = list(filter(lambda x: x != "", re.split('\W+', row[0])))
    targetWords = list(filter(lambda x: x != "", re.split('\W+', row[1])))

    for word in sourceWords:
        if not word in wordsDict:
            wordsDict[word] = {}

        subDict = wordsDict[word]
        for tw in targetWords:
            if tw in subDict:
                subDict[tw] += 1
            else:
                subDict[tw] = 1

finalDict = {}

for key, value in wordsDict.items():
    mostProbableTranslation = []
    mostProbableFrequency = 0
    for translation, frequency in value.items():
        if mostProbableFrequency < frequency:
            if mostProbableFrequency < frequency * 0.9:
                mostProbableTranslation = [translation]
            else:
                mostProbableTranslation.append(translation)
            mostProbableFrequency = frequency
        else:
            if frequency > mostProbableFrequency * 0.9:
                mostProbableTranslation.append(translation)
    finalDict[key] = ' '.join(mostProbableTranslation)

pd.DataFrame.from_dict(finalDict, orient='index').to_csv(outputName, header=False)

