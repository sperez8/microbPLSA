'''
Created on 22/01/2014

author: sperez8

Performs clustering on raw otu counts
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
    m.open_data(datafile)
    data = m.datamatrix
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
    