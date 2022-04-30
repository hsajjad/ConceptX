#!/usr/bin/env python
import sys
import json
#from tqdm import tqdm
from argparse import ArgumentParser


def firstWord(lines):

	output = []
	for line in lines:
		words = line.split()
		length = len(words)

		#print ("FW",  end='')
		string = "FW"

		for i in range(len(words)-1):
			#print (" NO_UNK",  end='')
			string = string + " NO_UNK"
		#print()
		output.append(string)

	with open('labels_FirstWord.json', 'w') as outfile:
		json.dump(output, outfile)

def lastWord(lines):

	output = []
	for line in lines:
		words = line.split()
		length = len(words)

		string = ""
		for i in range(len(words)-1):
			string = string + "NO_UNK "
		
		string = string + "LW"
		output.append(string)

	with open('labels_LastWord.json', 'w') as outfile:
		json.dump(output, outfile)

def casing(lines):

	output = []
	for line in lines:
		words = line.split()
		length = len(words)

		string = ""
		for i in range(len(words)):

			if (words[i].islower()):
				string = string + "LC "
			elif(words[i].isupper()):
				string = string + "UC "
			else:
				if (words[i].isalpha()):
					string = string + "MC "
				else:
					string = string + "NO_UNK "
		string = string[:-1]
		output.append(string)

	with open('labels_Casing.json', 'w') as outfile:
		json.dump(output, outfile)

def suffixes(lines):

	wordMap = {}
	output = []
	suffixes = {}

	with open("SuffixList") as f1:
		for s in f1:
			s = s.rstrip('\r\n')
			ss = s.split()
			suffixes[ss[0]] = ss[1]

	
	for line in lines:
		words = line.split()
		length = len(words)

		string = ""
		for i in range(len(words)):

			flag = 0
			if (words[i] in wordMap):
				string = string + wordMap[words[i]] + " "
			else:
				for j in suffixes:
					if (words[i].endswith(suffixes[j]) and words[i] != suffixes[j] ):
						if i in wordMap:
							if len(suffixes[j]) > len(wordMap[words[i]]):
								wordMap[words[i]] = j
						else:
							wordMap[words[i]] = suffixes[j]
							flag = 1
				if (flag ==0):
					string = string + "NO_UNK" + " "
				else:
					string = string + wordMap[words[i]] + " " 

		string = string[:-1]
		output.append(string)

	with open('labels_Suffixes.json', 'w') as outfile:
		json.dump(output, outfile)

def prefixes(lines):

	wordMap = {}
	output = []
	suffixes = {}

	with open("PrefixList") as f1:
		for s in f1:
			s = s.rstrip('\r\n')
			ss = s.split()
			suffixes[ss[0]] = ss[1]

	
	for line in lines:
		words = line.split()
		length = len(words)

		string = ""
		for i in range(len(words)):

			flag = 0
			if (words[i] in wordMap):
				string = string + wordMap[words[i]] + " "
			else:
				for j in suffixes:
					lowerCasedStr = words[i].lower() 
					if (lowerCasedStr.startswith(suffixes[j]) and lowerCasedStr != suffixes[j] ):
						if i in wordMap:
							if len(suffixes[j]) > len(wordMap[words[i]]):
								wordMap[words[i]] = j
						else:
							wordMap[words[i]] = suffixes[j]
							flag = 1
				if (flag ==0):
					string = string + "NO_UNK" + " "
				else:
					string = string + wordMap[words[i]] + " " 

		string = string[:-1]
		output.append(string)

	with open('labels_Prefixes.json', 'w') as outfile:
		json.dump(output, outfile)


def multiple(lines):

	fileList = ["Food", "Animal", "Body", "Plant", "Substance", "Event"]
	counts = [0] * len(fileList)
	labelDB = []
	output = []

	for i in fileList:
		thisLabel = {}
		with open(i) as f1:
			for s in f1:
				s = s.rstrip('\r\n')
				s = s.lower()
				thisLabel[s] = 1
		labelDB.append(thisLabel)

	for line in lines:
		words = line.split()
		length = len(words)

		string = ""
		for i in range(len(words)):

			flag = 0

			for k in range(len(fileList)):
				thisLabel = labelDB[k]

				if (words[i].lower() in thisLabel):
					string = string + fileList[k] + " "
					flag = 1
					counts[k] = counts[k] + 1
					print (line)
					print (words[i].lower(), fileList[k], counts[k])
					break

			if (flag == 0):
				string = string + "NO_UNK "

		string = string[:-1]
		output.append(string)


	with open('labels_multiple.json', 'w') as outfile:
		json.dump(output, outfile)

	for i in range(len(counts)):
		print (fileList[i], counts[i])


def strSorting(lst):
    lst.sort(key=len)
    return lst

def propaganda(lines, PropagandaFile):

	propagandaDictionary = {}
	output = []
	output2 = []
	
	with open(PropagandaFile) as f1:
		for s in f1:
			s = s.rstrip('\r\n')
			words = s.split("\t")
			propagandaDictionary[words[1]] = words[0]

	for line in lines:

		matches = []

		for k, v in propagandaDictionary.items():

			if (k in line and len(k) > 5):
				matches.append(k)
			
		matches = strSorting(matches)
		origLine = line

		print (line)
		print (matches)

		for j in reversed(matches):
			subwords = j.split()
			string = propagandaDictionary[j]
			dup = " [[[ "
			dup2 = " [[[ "

			for k in subwords:
				dup = dup + string + " "
				dup2 = dup2 + k + " "

			dup = dup + "]]] "
			dup2 = dup2 + "]]] "

			lineX = line.replace(j, dup)
			if (lineX != line):
				origLine = origLine.replace(j, dup2)
				line = lineX
		line = line.replace ("  ", " ")
		origLine = origLine.replace ("  ", " ")
		words = line.split()
		words2 = origLine.split()
		print (line)
		print (origLine)
		string = ""
		inputString = ""
		flag = 0

		for l in range(len(words)):

			if (words[l] == "[[["):
				flag = 1
				continue

			if (words[l] == "]]]"):
				flag = 0
				continue

			if (flag == 0):
				string = string + "NO_UNK "
				inputString = inputString + words2[l] + " "
			if (flag == 1):
				string = string + words[l] + " "
				inputString = inputString + words2[l] + " "

			#print (flag, words[l])
			#print (string)
			#print (inputString)
			#input()
		string = string[:-1]
		inputString = inputString[:-1]
		output.append(string)
		output2.append(inputString)

		# w = string.split()
		# ww = inputString.split()
		# print (string, len(w))
		# print (inputString, len(ww))

		# input ()


	string = "labels_" + args.l + ".json"
	inputString = "input_" + args.l + ".json"

	with open(string, 'w') as outfile:
		json.dump(output, outfile)
	outfile.close()

	with open(inputString, 'w') as outfile:
		json.dump(output2, outfile)
	outfile.close()



def countries(lines):

	countries = {}
	output = []
	
	with open("CountryList") as f1:
		for s in f1:
			s = s.rstrip('\r\n')
			countries[s] = 1

	
	for line in lines:
		words = line.split()
		length = len(words)

		string = ""
		for i in range(len(words)):

			flag = 0
			if (words[i] in countries):
				string = string + "Country "
			else:
				string = string + "NO_UNK "
				
		string = string[:-1]
		output.append(string)

	with open('labels_Countries.json', 'w') as outfile:
		json.dump(output, outfile)

def cities(lines):

	countries = {}
	output = []
	
	with open("CityList") as f1:
		for s in f1:
			s = s.rstrip('\r\n')
			countries[s] = 1

	
	for line in lines:
		words = line.split()
		length = len(words)

		string = ""
		for i in range(len(words)):

			flag = 0
			if (words[i] in countries):
				string = string + "City "
			else:
				string = string + "NO_UNK "
				
		string = string[:-1]
		output.append(string)

	with open('labels_Cities.json', 'w') as outfile:
		json.dump(output, outfile)


def sports(lines):

	countries = {}
	output = []
	
	with open("SportsList") as f1:
		for s in f1:
			s = s.rstrip('\r\n')
			countries[s] = 1

	
	for line in lines:
		words = line.split()
		length = len(words)

		string = ""
		for i in range(len(words)):

			flag = 0
			if (words[i] in countries):
				string = string + "Sports "
			else:
				string = string + "NO_UNK "
				
		string = string[:-1]
		output.append(string)

	with open('labels_Sports.json', 'w') as outfile:
		json.dump(output, outfile)

def bpe(lines, vocabFile):

	vocab = {}
	bpeDictionary = {}
	output = []
	
	with open(vocabFile) as f1:
		for s in f1:
			s = s.rstrip('\r\n')
			vocab[s] = 1

	
	#count = 0
	for line in lines:
		words = line.split()
		length = len(words)
		thisSent = ""

		#print (count)
		#count = count+1
		for i in range(len(words)):
			
			string = words[i] + "|||"
			if (words[i] in bpeDictionary):
				string = bpeDictionary[words[i]]
				thisSent = thisSent + string + " "
			else:
				for key in vocab:
					if (key in words[i] and key != "" and key != words[i]):
						string = string +  key + "|||"
						#print (string)
				string = string[:-3]
				#print (string)
				thisSent = thisSent + string + " "
				bpeDictionary[words[i]] = string
		
			
		thisSent = thisSent[:-1]
		#print (thisSent)
		#input()
		output.append(thisSent)

	jsonOutput = "labels_" + args.m + ".json" 
	with open(jsonOutput, 'w') as outfile:
		json.dump(output, outfile)

def brownClusters(lines, vocabFile):
	wordToCluster = {}
	clusterName = {}
	clusterToName = {}
	cN = {}
	output = []

	with open(vocabFile) as f1:
		for s in f1:
			s = s.rstrip('\r\n')
			words = s.split()
			wordToCluster[words[1]] = words[0]

			if words[0] in clusterName.keys():
				freqArray = clusterName[words[0]]
				tup = (words[1], int(words[2]))
				
				freqArray.append(tup)
				clusterName[words[0]] = freqArray
			else:
				tup = (words[1], int(words[2]))
				freqArray = []
				freqArray.append(tup)
				clusterName[words[0]] = freqArray

	for keys in clusterName:
		freqArray = clusterName[keys]
		freqArray.sort(key = lambda x: x[1], reverse=True)
		
		string = ""
		for i in range (5):
			a, b = freqArray[i]
			string = string + a + "_"
		string = string[:-1]
		cN [keys] = string
		
		#print (keys, string)
	
	for line in lines:
		words = line.split()

		length = len(words)
		thisSent = ""

		for i in range(len(words)):
			cluster = wordToCluster[words[i]]
			thisSent = thisSent + cluster + ":::" + cN[cluster] + " "

		thisSent = thisSent[:-1]
		#print (thisSent)
		#input()
		output.append(thisSent)

	jsonOutput = "labels_" + vocabFile + ".json" 
	with open(jsonOutput, 'w') as outfile:
		json.dump(output, outfile)

def latentClusters(lines, vocabFile):

	vocab = {}
	output = []
	with open(vocabFile) as f1:
		for s in f1:
			s = s.rstrip('\r\n')
			words = s.split ("||||||")
			vocab[words[0]] = words[1]

	for line in lines:
		words = line.split()

		length = len(words)
		thisSent = ""
		for i in range(len(words)):
			if (words[i] in vocab):
				string = vocab[words[i]]
				thisSent = thisSent + string + " "
			else:
				thisSent = thisSent + "NO_UNK "
		
		thisSent = thisSent[:-1]
		output.append(thisSent)

	jsonOutput = "clusters_" + args.m + ".json" 
	with open(jsonOutput, 'w') as outfile:
		json.dump(output, outfile)




parser = ArgumentParser()
parser.add_argument("-j", "--jsonFile", dest="j",
                    help="JsonFile", metavar="FILE")
parser.add_argument("-l", "--label", dest="l",
                    help="Label Type", metavar="FILE")
parser.add_argument("-m", "--model", dest="m",
                    help="Model", metavar="FILE", default="BERT")
parser.add_argument("-c", "--clusters", dest="c",
                    help="Number of Clusters", metavar="FILE", default="50")


args = parser.parse_args()

with open(args.j, "r") as read_file:
	data = json.load(read_file)

	lines = []  
	for line in data:
		line = line.rstrip('\r\n')
		lines.append(line)
read_file.close()

if (args.l == "FirstWord"):
	firstWord(lines)

if (args.l == "LastWord"):
	lastWord(lines)

if (args.l == "Casing"):
	casing (lines)

if (args.l == "Suffix"):
	suffixes (lines)

if (args.l == "Prefix"):
	prefixes (lines)

if (args.l == "Country"):
	countries (lines)

if (args.l == "City"):
	cities (lines)

if (args.l == "Sports"):
	sports (lines)

if (args.l == "Multiple"):
	multiple (lines)

if (args.l == "BPE"):
	vocab = args.m + ".vocab"
	bpe (lines, vocab)
if (args.l == "Brown"):
	vocab = "brownClusters" + args.c
	brownClusters(lines, vocab)
if (args.l == "Latent"):
	vocab = args.m + ".clusterMap"
	latentClusters (lines, vocab)
if (args.l == "Propaganda"):
	propertyFile = args.l + "Labels"
	propaganda (lines, propertyFile)
