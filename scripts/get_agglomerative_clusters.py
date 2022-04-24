import numpy as np
from sklearn.cluster import AgglomerativeClustering
from collections import defaultdict
from sklearn.decomposition import PCA
from sklearn import manifold
import time
import codecs
import argparse
import dill as pickle

parser = argparse.ArgumentParser()
parser.add_argument("--vocab-file","-v", help="output vocab file with complete path")
parser.add_argument("--point-file","-p", help="output point file with complete path")
parser.add_argument("--output-path","-o", help="output path clustering model and result files")
parser.add_argument("--cluster","-k", help="cluster numbers comma separated (e.g. 5,10,15)")
parser.add_argument("--range","-r", type=bool, default=False, help="whether cluster option provides a range or cluster numbers (e.g. in case of range: 5,50,10 start with k=5 increment by 10 till reach k=50)")

args = parser.parse_args()

vocab_file = args.vocab_file
point_file = args.point_file
outputpath = args.output_path

Ks = [int(k) for k in args.cluster.split(',')]
print ("Cluster input ",Ks)
if range:
	tmp = list(range(Ks[0], Ks[1]+1, Ks[2]))
	Ks = tmp

print ("Run for the following cluster sizes", Ks)

vocab = np.load(vocab_file)
points = np.load(point_file)
			
for K in Ks:
	starttime = time.time()
	print("Perform "+str(K)+" Clustering!")
	clustering = AgglomerativeClustering(n_clusters=K,compute_distances=True).fit(points)

	fn = outputpath+'/model-'+str(K)+'-agglomerative-clustering.pkl'
	with open(f"{fn}", "wb") as fp:
		pickle.dump(clustering,fp)
		#np.save(fn,clustering)
				
	clusters = defaultdict(list)
	for i,label in enumerate(clustering.labels_):
		clusters[clustering.labels_[i]].append(vocab[i])

	print("Write "+str(K)+" Clusters!")	
	target = open(outputpath+'/clusters-'+str(K)+'.txt','w')
				
	#Write Clusters	 (Word|||WordID|||SentID|||TokenID|||ClusterID)
	for key in clusters.keys():
		for word in clusters[key]:
			target.write(word+"|||"+str(key)+"\n")
	target.close()
				
	endtime = time.time()
	diff = endtime-starttime
	print(str(K)+": Time-taken: "+str(diff)+" sec")
