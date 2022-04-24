import argparse
import json



def get_pieces(line):
    pieces = []
    end_idx = len(line)
    for _ in range(3):
        sep_idx = line[:end_idx].rfind("|||")
        pieces.append(line[sep_idx+3:end_idx])
        end_idx = sep_idx
    pieces.append(line[:end_idx])
    return list(reversed(pieces))

parser = argparse.ArgumentParser()
parser.add_argument('--input-file', type=str, required=True)
parser.add_argument('--frequency-file', type=str, required=True)
parser.add_argument('--sentence-file', type=str, required=True)
parser.add_argument('--minimum-frequency', type=int, default=5)
parser.add_argument('--maximum-frequency', type=int, default=50)
parser.add_argument('--delete-frequency', type=int, default=500000)
parser.add_argument('--output-file', type=str, default="output_activatons.json")

args = parser.parse_args()

datasetfiles = (args.input_file).split(',')
min_freq = args.minimum_frequency
max_freq = args.maximum_frequency
del_freq = args.delete_frequency

print ("Min: ", min_freq, " Max: ", max_freq, " Del: ", del_freq)

wordCount = {}
with open(args.frequency_file) as f:
    print ("Loading frequency")
    wordCount = json.load(f)
print("Len of word dict: {}".format(len(wordCount)))
currCount = {}
output = []
maxskip = 0
maxskips = set()
minskip = 0
minskips = set()
delskip = 0
delskips = set()

dataset_wordcount = {}
dataset_sentencecount = 0

files_size = {}
# concatenate all sentence files
files = (args.sentence_file).split(',')
sentences = []
for idx,file in enumerate(files):
    f = open(file)
    filesize = 0
    data= json.load(f)
    for line in data:
        sentences.append(line.strip())
        filesize +=1
    files_size[idx] = filesize
print ("file sizes", files_size)

with open(args.output_file+"_min_"+str(min_freq)+"_max_"+str(max_freq)+'-sentences.json', 'w') as fp:
    json.dump(sentences, fp, ensure_ascii=False)

for idx, file in enumerate(datasetfiles):
    print ("Loading ", file)
    with open(file) as f:
        dataset = json.load(f)
        for entry in dataset:
            #print ("Old entry", entry[0])
            word, d_wordcount, d_sentencecount, label_idx = get_pieces(entry[0])
            #word, d_wordcount, d_sentencecount, label_idx = entry[0].split('|||')
            d_sentencecount = int(d_sentencecount)
            #print (word, d_wordcount, d_sentencecount, label_idx)
            if word in dataset_wordcount:
                dataset_wordcount[word] +=1
            else:
                dataset_wordcount[word] = 1
            d_sentencecount += dataset_sentencecount
            entry = (word+"|||"+str(dataset_wordcount[word])+"|||"+str(d_sentencecount)+"|||"+label_idx, entry[1])
            #print ("New entry", entry)
            if word in wordCount and wordCount[word] > del_freq: # skipping most frequent words
                print("Delete word {}".format(word))
                delskip +=1
                delskips.add(word)
                continue
            if word in wordCount and wordCount[word] >= min_freq:
                if word in currCount:
                    if currCount[word] <max_freq:
                        output.append(entry)
                        currCount[word] += 1
                    else:
                        print ("Crossed max frequency :", entry[0])
                        maxskip +=1
                        maxskips.add(word)
                else:
                    currCount[word] = 1
                    output.append(entry)
            else:
                print ("Skipping word with low frequency: ", entry[0])
                minskip +=1
                minskips.add(word)
    dataset_sentencecount += files_size[idx]

print("Writing datasets...")
with open(args.output_file+"_min_"+str(min_freq)+"_max_"+str(max_freq)+"_del_"+str(del_freq)+"-dataset.json", 'w') as fp:
    json.dump(output, fp, ensure_ascii=False)


print ("Limit Max types: ", maxskips)
print ("Skipped Min types: ", minskips)
print ("Skipped frequent types: ", delskips)

print ("Total word types before dropping: ", len(wordCount))
print ("Total word tokens before dropping: ", sum(wordCount.values()))

print ("Tokens skipped based on Max freq: ", maxskip)
print ("Tokens skipped based on Min freq: ", minskip)
print ("Tokens skipped based on Del freq: ", delskip)
print ("Types skipped based on Max freq: ", len(maxskips))
print ("Types skipped based on Min freq: ", len(minskips))
print ("Types skipped based on Del freq: ", len(delskips))

print ("Remaining Tokens: ", sum(wordCount.values()) - maxskip - minskip - delskip)
print ("Remaining Types: ", len(wordCount) - len(minskips) - len(delskips))
