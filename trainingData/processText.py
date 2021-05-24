import re
import sys

inputName = sys.argv[1]
outputName = sys.argv[2]

f = open(inputName, "r")
text = f.read();
f.close()
text = text.replace('\n', ' ')
sentences = re.split(r'[ \s]{2,}|\W*\.\s+\W*|\W*\!\s+\W*|\W*\:\W*|\W*\;\W*|\W*\(\W*|\W*\)\W*|\W*\"\W*', text);

f2 = open(outputName,"w")
for s in sentences:
    if len(s.split(' ')) < 2:
        continue
    f2.write(s + "\n")