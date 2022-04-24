import argparse
import json
import sys

from collections import Counter
from tqdm import tqdm

sys.path.append("/export/work/hsajjad/software/NeuroX/")

import neurox.data.loader as data_loader
#from aux_classifier import data_loader

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--text-file', type=str, required=True)
    parser.add_argument('--activation-file', type=str, required=True)
    parser.add_argument('--output-prefix', type=str, required=True)

    args = parser.parse_args()

    print("Loading activations...")
    activations, num_layers = data_loader.load_activations(f'{args.activation_file}', num_neurons_per_layer=768)
    print("Loading tokens...")
    tokens = data_loader.load_data(
        f'{args.text_file}',
        f'{args.text_file}',
        activations,
        1000
    )

    print("Preparing dataset...")
    sentences = []
    labels = []
    selected_tokens = Counter()
    token_dataset = []

    for line_idx, label_line in tqdm(enumerate(tokens['target'])):
        sentences.append(" ".join(tokens['source'][line_idx]))
        labels.append(" ".join(label_line))
        for label_idx, label in enumerate(label_line):
            token = tokens['source'][line_idx][label_idx]
            selected_tokens[token] += 1
            token_acts = activations[line_idx][label_idx, :]
            token_acts = token_acts.tolist()
            
            final_tok_rep = f'{token}|||{selected_tokens[token]}|||{len(sentences)-1}|||{label_idx}'
            token_dataset.append((final_tok_rep, token_acts))
    
    print("Writing datasets...")
    with open(f'{args.output_prefix}-sentences.json', 'w', encoding='utf-8') as fp:
        json.dump(sentences, fp, ensure_ascii=False)
    
    with open(f'{args.output_prefix}-labels.json', 'w') as fp:
        json.dump(labels, fp)
  
    with open(f'{args.output_prefix}-dataset.json', 'w') as fp:
        json.dump(token_dataset, fp)

if __name__ == '__main__':
    main()
