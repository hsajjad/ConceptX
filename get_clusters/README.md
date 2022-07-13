## Get concept clusters
get_clusters/getclusters.sh provides step-by-step commands to create concept clusters. You need to specify path to a sentence file.

### Setting up the environments
```
conda env create --file=env_neuron.yml
```
```
conda env create --file=env_clustering
```

### Run the clustering script
```
sh get_clusters/getclusters.sh
```
The results directory contains the final clustering output.