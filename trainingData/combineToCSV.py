#! /usr//bin/python

import csv
import sys

originFileName = sys.argv[1]
translatedFileName = sys.argv[2]
outputFileName = sys.argv[3]

csvFile = open(outputFileName, 'w', newline='');

originFile = open(originFileName, 'r');
translatedFile = open(translatedFileName, 'r');
writer = csv.writer(csvFile)


while True:
    originLine = originFile.readline()

    if not originLine:
        break

    translatedLine = translatedFile.readline()

    writer.writerow([originLine.strip('\n'), translatedLine.strip('\n')])
