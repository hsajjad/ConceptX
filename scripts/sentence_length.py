"""
Utility function to remove sentences of length longer than the specified length
Input
Author: Hassan Sajjad
Creation: 9 Feb 2022

Parameters
----------
text-file : str, 
    sentence file
length : int, optional
    Maximum sentence length

Yields
------
output : sentence file
"""

# sample command
# python /alt/neurox/concept-pool/data/scripts/sentence_length.py --text-file sample_data/test_inp --output-file sample_data/test_inp.sent_len --length 30

import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--text-file', type=str, required=True)
parser.add_argument('--length', type=int, required=False, default=300)
parser.add_argument('--output-file', type=str, required=True)

args = parser.parse_args()

out = open(args.output_file, "w")

print("Loading text file...")
print("Removing lines with length greater than ", args.length)

count = 0

with open(args.text_file) as f:
    for line in f.readlines():
        if len((line.strip()).split()) < args.length:
            out.write(line)
        else:
            print ("Skipped line: ", line)
            count +=1

print ("File saved as ", args.output_file)
print ("Number of lines skipped: ", count)


