'''
Created on 22/01/2014

author: sperez8

Performs clustering on raw otu counts
'''
from scipy.cluster.vq import kmeans
import os, sys

from matplotlib.pyplot import show
import numpy as np
from scipy.cluster.hierarchy import fclusterdata
from scipy.cluster.hierarchy import linkage
from scipy.cluster.hierarchy import dendrogram
from scipy.spatial.distance import pdist
import matplotlib.pylab as plt


_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)
import microbplsa

study = '1037'
z = 8

f = '/Users/sperez/git/microbPLSA/MicrobProcessor/Results/study_'+study +'_'
end = '_topics_.txt'
file = f+str(z)+end


m = microbplsa.MicrobPLSA()
plsa = m.open_model(file) #get model from the results file'
X = plsa.p_d_z

print X.shape

Y = pdist(X, 'euclidean')

Z = linkage(Y)

dendrogram(Z)
show()

