#!/usr/bin/env python
import sys
from tqdm import tqdm
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument("-s", "--sIndex", dest="s",
                    help="source Index", metavar="FILE")

args = parser.parse_args()

with open(args.s) as f1:
	for line in f1:
		line = line.rstrip('\r\n')
		words = line.split()

		for i in range(len(words)):
			print (words[i] + " LOC" )
		print ()

f1.close()

