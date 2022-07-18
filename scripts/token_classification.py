from argparse import ArgumentParser
from transformers import AutoTokenizer, AutoModelForTokenClassification, TokenClassificationPipeline

def main():
	parser = ArgumentParser()
	parser.add_argument("model_name", help="Model identifier")
	parser.add_argument("sentence_file", help="Path to a file with one sentence per line")
	parser.add_argument("output_file", help="Path to output file with one labels for every token in the sentence_file")

	args = parser.parse_args()

	# Load model and build pipeline
	tokenizer = AutoTokenizer.from_pretrained(args.model_name)
	model = AutoModelForTokenClassification.from_pretrained(args.model_name)
	pipeline = TokenClassificationPipeline(model, tokenizer, ignore_labels=[])

	with open(args.sentence_file) as fp, \
		open(args.output_file, "w") as ofp:
		for line_idx, line in enumerate(fp):
			line = line.strip()
			print(f"Line {line_idx}: {line[:80]}")
			outputs = pipeline(line)

			original_tokens = line.split(" ")

			# Pick first per subword
			idx_to_pick = []
			current_idx = 0
			for token in original_tokens:
				idx_to_pick.append(current_idx)
				current_idx += len(tokenizer.tokenize(token))

			labels = []
			for word_idx, label_idx in enumerate(idx_to_pick):
				token_prediction = outputs[label_idx]
				assert original_tokens[word_idx].startswith(token_prediction["word"]), \
					f"Original word: {original_tokens[word_idx]}, First subword: {token_prediction['word']}"
			
				labels.append(token_prediction["entity"])

			assert len(labels) == len(original_tokens)
			
			ofp.write(" ".join(labels) + "\n")

if __name__ == '__main__':
	main()