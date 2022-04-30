#!/usr/bin/env python
import sys
#from tqdm import tqdm
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument("-s", "--sIndex", dest="s",
                    help="source Index", metavar="FILE")
parser.add_argument("-l", "--lIndex", dest="l",
                    help="label Index", metavar="FILE")

args = parser.parse_args()

with open(args.s) as f1, open(args.l) as f2:
	for line in f1:
		line2 = f2.readline()
		line = line.rstrip('\r\n')
		words = line.split()
		line2 = line2.rstrip('\r\n')
		tags = line2.split()

		for i in range(len(words)):
			print (words[i] + " " + tags[i])
		print ()

f1.close()
f2.close()
