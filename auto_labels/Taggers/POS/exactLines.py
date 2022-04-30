#!/usr/bin/env python
import sys
from tqdm import tqdm
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument("-o", "--oIndex", dest="o",
                    help="Original", metavar="FILE")
parser.add_argument("-m", "--mIndex", dest="m",
                    help="Original", metavar="FILE")
parser.add_argument("-l", "--lIndex", dest="l",
                    help="label Index", metavar="FILE")

args = parser.parse_args()

oFile = []
with open(args.o) as f1:
	for line in f1:
		line = line.rstrip('\r\n')
		oFile.append(line)
f1.close()

with open(args.o) as f1, open(args.m) as f2, open(args.l) as f3:
	count = 0
	while count <= len(oFile):

		line = f1.readline()
		count = count+1
		line2 = f2.readline()
		line3 = f3.readline()
		line = line.rstrip('\r\n')
		line2 = line2.rstrip('\r\n')
		line3 = line3.rstrip('\r\n')
		one = line.split()
		two = line2.split()
		three = line3.split()

		if (line != ""):
			while (line != line2 and f1):
				line2 = f2.readline()
				line3 = f3.readline()
				line2 = line2.rstrip('\r\n')
				line3 = line3.rstrip('\r\n')
				tags = line2.split()
				two = line2.split()
				three = line3.split()

			#print ("Bakwas", count, line, line2, line3)
			if (one[0] == two[0]):
				
				if (line3 != ""):
					if (three[0] == two[0]):
							print (line3)
					else:
						input()
				else: #space
					line3 = f3.readline()
					line3 = line3.rstrip('\r\n')
					three = line3.split()
 
					while (len(line) != 0):
						#print (count, len(line), line, line3)
						#input()
						print (line)
						line = f1.readline()
						count = count+1
						line2 = f2.readline()
						line = line.rstrip('\r\n')
						line2 = line2.rstrip('\r\n')
						one = line.split()
						two = line2.split()
					print (line)		
					line = f1.readline()
					count = count+1
					line2 = f2.readline()
					line = line.rstrip('\r\n')
					line2 = line2.rstrip('\r\n')
					one = line.split()
					two = line2.split()

					if (three[0] == one[0] and three[0]== two[0]):
						print (line3)
					else:
						print (count, line, line2, line3)
						input()			
		else:
			print (line)
		

f1.close()
f2.close()
f3.close()
