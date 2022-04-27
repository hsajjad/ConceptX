# ConceptX
Analyzing Latent Concept in Pre-trained Transformer Models

## Get concept clusters
getclusters.sh provides a step-by-step commands to create concept clusters. You need to specify path to a sentence file.

### Proprocessing
This step invovles tokenizing the input sentences and extracting word-level contextualized embeddings. The setup requires setting up neurox environment using env_neurox.yml.

```conda env create --file=env_neuron.yml
```

### Run clustering
Cluster the word-level contextualized embeddings. This step requires setting up the clustering environment.

```conda env create --file=env_clustering
```

## Get Auto-labels
Label the sentence file with pre-defined tags such as parts-of-speech, suffixes, wordNet, etc.


