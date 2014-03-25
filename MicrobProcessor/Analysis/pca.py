'''
Created on 22/01/2014

author: sperez8

Perform PCA using sklearn implementation
'''
import os, sys
_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)
import microbplsa

analysis_dir = _root_dir+ '/Analysis'
sys.path.insert(0, analysis_dir)
from labelling import Labelling

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.font_manager import FontProperties
from sklearn.decomposition import PCA
import numpy as np

study = '1526'
z = 8
MANUAL_LABELS = ['Topic ' + str(k+1) for k in range(0,z)]
print MANUAL_LABELS
datafile = '/Users/sperez/Documents/PLSAfun/EMPL data/study_'+study+'_split_library_seqs_and_mapping/study_'+study+'_closed_reference_otu_table.biom'
resultfile = '/Users/sperez/git/microbPLSA/MicrobProcessor/Results/study_'+study +'_'+str(z)+'_topics_.txt'
num_components = 3

def makePCA(datafile, num_components):
    m = microbplsa.MicrobPLSA()
    m.open_data(datafile) #get data of OTU abundances per sample
    X = m.datamatrix.T
    
    plsa = m.open_model(resultfile) #get model from the results file
    #return document's distribution
    p_d_z = plsa.p_d_z
    N,Z =p_d_z.shape
    
    #get topic labels
    if MANUAL_LABELS:
        labels  = MANUAL_LABELS
    else:
        Lab = Labelling(study, Z, ignore_continuous = False)
        Lab.metadata(non_labels = ['BarcodeSequence'])
        R = Lab.correlate()
        labels_r = Lab.assignlabels(R,num_labels = 1)
        labels, r = zip(*labels_r)
        labels = [l.replace('(','\n(') for l in labels]
    
    #get primary topic per sample
    topics = []
    for i, row in enumerate(p_d_z):
        max_topic_index = np.argmax(row)
        topics.append(max_topic_index)    
    topics = np.array(topics)
    pca = PCA(n_components=num_components, whiten = True)
    pca.fit(X)
    X_r = pca.fit(X).transform(X)
    
    # Percentage of variance explained for each components
    print('Explained variance ratio (first two components): %s'
          % str(pca.explained_variance_ratio_))
    
    #initiate plot and colors
    colors = [float(c)/float(Z) for c in range(0,Z)]
    colors = plt.cm.rainbow(np.linspace(0, 1, Z))
    fig = plt.figure(1, figsize=(4, 3))
    plt.clf()
    ax = plt.subplot(111, projection ='3d')
    if num_components == 2:
        for c, i, l in zip(colors, range(0,Z), labels):
            ax.plot(X_r[topics == i, 0], X_r[topics == i, 1], 'o', color=c, label=l)
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, 0.5, box.height])
    elif num_components == 3:
        for c, i, l in zip(colors, range(0,Z), labels):
            ax.plot(X_r[topics == i, 0], X_r[topics == i, 1], X_r[topics == i, 2], 'o', color=c, label=l)
    fontP = FontProperties()
    if Z > 12: 
        columns = 2
    else: columns = 1
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, 0.5, box.height])
    plt.legend(prop = fontP, loc='center left', bbox_to_anchor=(1, 0.5), ncol = columns)
    plt.title('PCA of Study %s with Z=%s' %(study, str(z)))

    plt.show()
    return None

makePCA(datafile, num_components)