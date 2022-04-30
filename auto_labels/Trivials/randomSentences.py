#!/usr/bin/env python
import sys
import json
import random
#from tqdm import tqdm
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument("-j", "--jsonFile", dest="j",
                    help="JsonFile", metavar="FILE")

args = parser.parse_args()

with open(args.j, "r") as read_file:
	data = json.load(read_file)

	lines = []  
	for line in data:
		line = line.rstrip('\r\n')
		lines.append(line)
read_file.close()

output = []
for i in range(0,1000):
	output.append(random.choice(lines))
	print (random.choice(lines))

with open('smallSet.json', 'w') as outfile:
	json.dump(output, outfile)