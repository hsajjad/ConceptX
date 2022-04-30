# ConceptX
Analyzing Latent Concept in Pre-trained Transformer Models

The code has been split into three parts. 1) get concept clusters, 2) generate auto-labels data, 3) calculate the alignment between auto-labels and concepts.

## Get concept clusters
getclusters.sh provides step-by-step commands to create concept clusters. You need to specify path to a sentence file.

### Proprocessing
This step invovles tokenizing the input sentences and extracting word-level contextualized embeddings. The setup requires setting up neurox environment using env_neurox.yml.

```
conda env create --file=env_neuron.yml
```

### Run clustering
Cluster the word-level contextualized embeddings. This step requires setting up the clustering environment.

```
conda env create --file=env_clustering
```

## Generate Auto-labels
Label the sentence file with pre-defined concepts such as parts-of-speech, suffixes, wordNet, etc. The directory auto_labels contain all the relevant scripts of this step. We have divided the auto-labels into trivial labels and supervised labels. The former consists of labels that do not require training data and are simply based on a list of words, ngrams, or pattern matches such as words ending with "ed". The latter consists of labels with supervised data such as parts-of-speech. For these labels, we have provided a trained tagger for each concept task.

### Trivial labels
auto-labels/Trivial/README provides step by step instructions to create trivial labels for the input sentence file.

### Supervised labels
This step will run a trained tagger and annotate each word in the input sentences. It requires setting up the environment provided in auto-labels/Taggers/environment.yml. Each task directory e.g. POS contains as README file that describes a step by step process to label the input sentences.

## Calculate alignment
This step calculates the alignment score between a given label file and the concept clusters. 

```
python scripts/align_with_single_auto_tag.py label_file sentence_file cluster_file
```




