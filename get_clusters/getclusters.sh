#!/bin/bash

scriptDir=../scripts/
inputPath=../data/ # path to a sentence file
input=text.in #name of the sentence file
# model name or path to a finetuned model
model="bert-base-cased"

# maximum sentence length
sentence_length=300

# analyze latent concepts of layer 12
layer=12

working_file=$input.tok.sent_len #do not change this

#1. Tokenize text with moses tokenizer
perl ${scriptDir}/tokenizer/tokenizer.perl -l en -no-escape < ${inputPath}/$input > $input.tok

#2. Do sentence length filtering and keep sentences max length of 300
python ${scriptDir}/sentence_length.py --text-file $input.tok --length ${sentence_length} --output-file $input.tok.sent_len

#Optional step. if sentence file is larger than 50k sentences, split it into smaller chunks for easy loading of activations

source activate neurox_pip
#3. Extract layer-wise activations
python -m neurox.data.extraction.transformers_extractor --decompose_layers --filter_layers ${layer} --output_type json ${model} ${working_file} ${working_file}.activations.json

#4. Create a dataset file with word and sentence indexes
python ${scriptDir}/create_data_single_layer.py --text-file ${working_file} --activation-file ${working_file}.activations-layer${layer}.json --output-prefix ${working_file}

#5. Calculate vocabulary size
python ${scriptDir}/frequency_count.py --input-file ${working_file} --output-file ${working_file}.words_freq

#6. Filter number of tokens to fit in the memory for clustering. Input file will be from step 4. minfreq sets the minimum frequency. If a word type appears is coming less than minfreq, it will be dropped. if a word comes 
minfreq=0
maxfreq=1000000
delfreq=1000000
python ${scriptDir}/frequency_filter_data.py --input-file ${working_file}-dataset.json --frequency-file ${working_file}.words_freq --sentence-file ${working_file}-sentences.json --minimum-frequency $minfreq --maximum-frequency $maxfreq --delete-frequency ${delfreq} --output-file ${working_file}

#7. Run clustering 

conda activate clustering

mkdir results
DATASETPATH=${working_file}_min_${minfreq}_max_${maxfreq}_del_${delfreq}-dataset.json
VOCABFILE=processed-vocab.npy
POINTFILE=processed-point.npy
RESULTPATH=./results
CLUSTERS=50,100,50  #Comma separated for multiple values or three values to define a range
# first number is number of clusters to start with, second is number of clusters to stop at and third one is the increment from the first value
# 600 1000 200 means [600,800,1000] number of clusters
		
#echo "Extracting Data!"
python -u ${scriptDir}/extract_data.py --input-file $DATASETPATH

echo "Creating Clusters!"
python -u ${scriptDir}/get_agglomerative_clusters.py --vocab-file $VOCABFILE --point-file $POINTFILE --output-path $RESULTPATH  --cluster $CLUSTERS --range 1
echo "DONE!"