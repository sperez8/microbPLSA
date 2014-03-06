'''
Created on 22/01/2014

author: sperez8

Performs clustering on raw otu counts
PCA stuff from http://scikit-learn.org/stable/auto_examples/decomposition/plot_pca_3d.html
'''
from sklearn.decomposition import PCA

from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pylab as pl
from scipy import stats


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

study = '722'
z = 22



f = '/Users/sperez/git/microbPLSA/MicrobProcessor/Results/study_'+study +'_'
end = '_topics_.txt'
file = f+str(z)+end

def makedendrogram(file):
    m = microbplsa.MicrobPLSA()
    plsa = m.open_model(file) #get model from the results file'
    X = plsa.p_d_z
    
    Y = pdist(X, 'euclidean')
    
    Z = linkage(Y)
    
    D = dendrogram(Z)
    print D['ivl']
    show()
    return None


def makePCA(file):
    m = microbplsa.MicrobPLSA()
    plsa = m.open_model(file) #get model from the results file'
    X = plsa.p_d_z    
    
    
    pca = PCA(n_components=2, whiten = True, )
    pca.fit(X)
    pca_score = pca.explained_variance_ratio_
    V = pca.components_
    print V.shape
    print V
    print pca_score* V.T

    x_pca_axis, y_pca_axis = V
    pcaplot = plt.scatter(x_pca_axis, y_pca_axis)
    show()

    return None
    
makePCA(file)
    
    