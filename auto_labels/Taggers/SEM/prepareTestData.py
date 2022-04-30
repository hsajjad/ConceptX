#!/usr/bin/env python
import os
import sys
import json
import operator
from transformers import AutoTokenizer
from pathlib import Path
import re

#from tqdm import tqdm
from argparse import ArgumentParser

def remove_confusing_tokens(ds_file, target_file):
    '''
    Ensures that strange control characters are removed and that there are breaks
    between lines ensuring that the sequence is not longer than 128 tokens
    '''
    tokenizer = AutoTokenizer.from_pretrained(BERT_MODEL)
    subword_len_counter = 0
    with open(ds_file, "rt") as f_p, open(target_file, 'w') as t:
        for line in f_p:
            line = line.rstrip()

            if not line:
                t.write(f'{line}\n')
                subword_len_counter = 0
                continue

            token = line.split()[0]

            current_subwords_len = len(tokenizer.tokenize(token))

            # Token contains strange control characters like \x96 or \x95
            # Just filter out the complete line
            if current_subwords_len == 0:
                continue

            if (subword_len_counter + current_subwords_len) > MAX_LENGTH:
                t.write("\n")
                t.write(f'{line}\n')
                subword_len_counter = current_subwords_len
                continue

            subword_len_counter += current_subwords_len

            t.write(f'{line}\n')


parser = ArgumentParser()
parser.add_argument("-f", "--files", dest="f",
                    help="files to be decoded", metavar="FILE")

args = parser.parse_args()
str = args.f
files = str.split()
MAX_LENGTH=250
BERT_MODEL='bert-base-multilingual-cased'

for i in files:
    TEST_FILE = 'Data/' +  i
    print (TEST_FILE)
    str = "python3 changeFormatTest.py -s " + TEST_FILE + "> " + i
    os.system(str)
    remove_confusing_tokens(i, (i+".tst"))
