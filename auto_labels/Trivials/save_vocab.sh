#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: ./save_vocab.sh <model-name>"
    exit
fi

python -c "import json;from transformers import AutoTokenizer; json.dump(AutoTokenizer.from_pretrained('$1').get_vocab(), open('$1_vocab.json', 'w'))"
