#!/usr/bin/env python
import sys
import json
import random
#from tqdm import tqdm
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument("-f", "--labelFile", dest="f",
                    help="Label File", metavar="FILE")
parser.add_argument("-l", "--labelType", dest="l",
                    help="Label Type", metavar="FILE")

args = parser.parse_args()
output = []
with open(args.f) as f1:
		for s in f1:
			s = s.rstrip('\r\n')
			output.append(s)


args = parser.parse_args()
outputFile = args.l + ".json"

with open(outputFile, 'w') as outfile:
	json.dump(output, outfile)