import pandas as pd
import sys
import re

csvName = sys.argv[1]
outputName = sys.argv[2]

sentences = pd.read_csv(csvName, header=None, usecols=[0]).values.tolist()

words = set()

for sentence in sentences:
    for word in sentence[0].split():
        words.add(re.sub(r'[^\w\-\']|\-$|.*[0-9].*', '', word).lower())

words.remove('')

outputFile = open(outputName,"w")

for word in words:
    outputFile.write(word + "\n")
