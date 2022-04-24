import json
import numpy as np
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("--input-file","-i", help="path to the json file")
parser.add_argument("--output-path","-o", default="./", help="output path")
parser.add_argument("--output-vocab-file","-v", default=None, help="output vocab file name")
parser.add_argument("--output-point-file","-p", default=None, help="output points file name")
args = parser.parse_args()

input_file = args.input_file
output_path = args.output_path
output_vocab_file = args.output_vocab_file
output_point_file = args.output_point_file

print("Reading "+input_file)
tokens = []
points = []
with open(input_file,'r') as f:
        dataset = json.load(f)
        for entry in dataset:
            #word, d_wordcount, d_sentencecount, label_idx = entry[0].split('|||')
            #representation = entry[1]
            tokens.append(entry[0])
            points.append(entry[1])

points = np.array(points)

if output_vocab_file == None:
	fname=output_path+"/processed-vocab.npy"
	print("vocab file: {}".format(fname))
	np.save(output_path+"/processed-vocab.npy",tokens)
else:
	print("vocab file: {}".format(output_vocab_file))
	np.save(output_vocab_file,tokens)
if output_point_file == None:
	fname=output_path+"/processed-point.npy"
	print("point file: {}".format(fname))
	np.save(output_path+"/processed-point.npy",points)
else:	
	print("point file: {}".format(output_point_file))
	np.save(output_point_file,points)
print("Written vocab file and point file")	

