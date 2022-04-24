import codecs
import argparse
import json

parser = argparse.ArgumentParser()

parser.add_argument('--input-file', type=str, required=True)
parser.add_argument('--output-file', type=str, default="output_activatons.json")

args = parser.parse_args()

files = (args.input_file).split(',')

wordCount = {}

for file in files:
    f = codecs.open(file, encoding="utf-8")
    print ("Reading file: ", file)
    for line in f.readlines():
        words = line.strip().split(' ')
        for word in words:
            if word in wordCount:
                wordCount[word] += 1

            else:
                wordCount[word] = 1

print ("Saving output file")        
with open(args.output_file, 'w') as fp:
    json.dump(wordCount, fp)

print ("######### Singletons #############")

print ([k for k,v in wordCount.items() if v < 2])

print ("#####################################")

print ("Types in vocab: ", len(wordCount))
print ("Tokens in vocab: ", sum(wordCount.values()))

lessthan5=0
lessthan4=0
lessthan3=0
lessthan2=0

for k,v in wordCount.items():
    if v < 2:
        lessthan5+=1
        lessthan4+=1
        lessthan3+=1
        lessthan2+=1
    elif v < 3:
        lessthan5+=1
        lessthan4+=1
        lessthan3+=1
    elif v < 4:
        lessthan5+=1
        lessthan4+=1
    elif v < 5:
        lessthan5+=1
       
print ("Types less than 2: ", lessthan2) 
print ("Types less than 3: ", lessthan3)
print ("Types less than 4: ", lessthan4)
print ("Types less than 5: ", lessthan5)
