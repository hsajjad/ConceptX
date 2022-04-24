# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 21:04:13 2022

@author: Devi
"""
#!/usr/bin/python

import sys
import pandas as pd
import warnings


warnings.filterwarnings('ignore')

def read(file):
    
    #file_name = sys.argv[1]
    #read the file into a dataframe df
    df = pd.read_csv(file, sep='\|\|\|', header=None,
                    names=['word','occurrence_in_the_corpus','sentence_id',
                          'word_id','cluster_id'])
    df.to_csv(r'clusters-400-csv.csv', index=False)
    
    #Average size of clusters (avg_tokens)
    print()
    print("Average cluster size is ",round(df.shape[0]/df.cluster_id.nunique(),2))
    
    df_cluster_unique_words = df.groupby('cluster_id',as_index=True)['word'].agg(**{'unique_words':lambda x:set(x), 
                                                                                    'frequency':lambda x:len(x),
                                                                                   'unique_word_freq': lambda x:len(set(x))}).reset_index()
    print("Average size of clusters based on unique words ",
          round(df_cluster_unique_words.unique_word_freq.sum()/df.cluster_id.nunique(),2))
    
    max_tokens = df_cluster_unique_words[df_cluster_unique_words.frequency==df_cluster_unique_words.frequency.max()]
    print("Size of the largest cluster in terms of words (max_tokens)",",".join(map(str,set(max_tokens['frequency']))))
    min_tokens = df_cluster_unique_words[df_cluster_unique_words.frequency==df_cluster_unique_words.frequency.min()]
    print("Size of the smallest cluster in terms of words (min_tokens)",",".join(map(str,set(min_tokens['frequency']))))
    
    max_types = df_cluster_unique_words[df_cluster_unique_words.unique_word_freq==df_cluster_unique_words.unique_word_freq.max()].reset_index(drop=True)
    print("Size of the largest cluster in terms of unique words (max_types)",",".join(map(str,set(max_types['unique_word_freq']))))
    
    min_types = df_cluster_unique_words[df_cluster_unique_words.unique_word_freq==df_cluster_unique_words.unique_word_freq.min()]
    print("Size of the smallest cluster in terms of unique words (min_types)",",".join(map(str,set(min_types['unique_word_freq']))))
    
    print ("Variance in cluster sizes (var_tokens)", round(df_cluster_unique_words.frequency.to_numpy().var(),2))
    #print("Variance in cluster sizes (var_tokens)", round(df_cluster_unique_words.frequency.var(),2))
    print ("Variance in cluster sizes based on unique words (var_types)", round(df_cluster_unique_words.unique_word_freq.to_numpy().var(),2))
    #print("Variance in cluster sizes based on unique words (var_types)", round(df_cluster_unique_words.unique_word_freq.var(),2))
    
    return


if __name__ == "__main__":
    if len(sys.argv)>1 and len(sys.argv)<3:
        read(str(sys.argv[1]))
    else:
        print("Wrong format, the correct usage: python cluster.py inputfilename")