#!/usr/bin/env python
import sys
import json
from tqdm import tqdm
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument("-s", "--sjsonFile", dest="s",
                    help="Source Json File", metavar="FILE")
parser.add_argument("-m", "--modelFile", dest="m",
                    help="Model File", metavar="FILE")

args = parser.parse_args()

lines = []  
labels = []

with open(args.s, "r") as read_file:
	data = json.load(read_file)
	for line in data:
		line = line.rstrip('\r\n')
		lines.append(line)
read_file.close()


for i in range(len(lines)):

	if(args.m == "BERT"):
		if (lines[i].startswith("##")):
			lines[i] = lines[i].replace("##", "")
		print (lines[i]) ## Prefixes

	elif (args.m == "RoBERTa"):
		bChar = '\u0120'
		if (lines[i].startswith(bChar)):
			lines[i] =  lines[i].replace(bChar, "")
		print (lines[i])
	elif (args.m == "XLNet" or args.m == "AlBERT" or args.m == "XLM-R"):
		bChar = '\u2581'
		if (lines[i].startswith(bChar)):
			lines[i] =  lines[i].replace(bChar, "")
		print (lines[i])
	




	