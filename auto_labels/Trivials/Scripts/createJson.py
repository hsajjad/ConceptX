#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
#from tqdm import tqdm
from argparse import ArgumentParser


def readJson(fileName):

	lines = []

	with open(fileName, "r") as read_file:
		data = json.load(read_file)
		for line in data:
			line = line.rstrip('\r\n')
			lines.append(line)
	return lines


parser = ArgumentParser()
parser.add_argument("-t", "--text", dest="t",
                    help="Text File", metavar="FILE")
parser.add_argument("-j", "--json", dest="j",
                    help="Json File", metavar="FILE")



args = parser.parse_args()

textFile = args.t
lines = []
	
with open(textFile) as f1:
	for s in f1:
		s = s.rstrip('\r\n')
		lines.append(s)

with open(args.j, 'w') as outfile:
	json.dump(lines, outfile)


