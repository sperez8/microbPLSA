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

# study = '722'
# z = 22
# datafile = '/Users/sperez/Documents/PLSAfun/EMPL data/study_'+study+'_split_library_seqs_and_mapping/study_'+study+'_closed_reference_otu_table.biom'


def makedendrogram(datafile, show = True):
    m = microbplsa.MicrobPLSA()
    data = m.open_data(datafile)
    X = data.T

    Y = pdist(X, 'euclidean')

    Z = linkage(Y)

    t = 0.7*max(Z[:,2])

    D = dendrogram(Z, color_threshold = t)

    leaves_order = D['ivl']
    if show:
        show()
    else: plt.clf()
    return leaves_order


def makePCA(datafile):
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
    