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
from matplotlib.font_manager import FontProperties
from sklearn.decomposition import PCA
import numpy as np

study = '1037'
z = 8
datafile = '/Users/sperez/Documents/PLSAfun/EMPL data/study_'+study+'_split_library_seqs_and_mapping/study_'+study+'_closed_reference_otu_table.biom'
resultfile = '/Users/sperez/git/microbPLSA/MicrobProcessor/Results/study_'+study +'_'+str(z)+'_topics_.txt'


def makePCA(datafile):
    m = microbplsa.MicrobPLSA()
    data = m.open_data(datafile) #get data of OTU abundances per sample
    X = data.T
    print X.shape
    
    plsa = m.open_model(resultfile) #get model from the results file
    #return document's distribution
    p_d_z = plsa.p_d_z
    N,Z =p_d_z.shape
    
    #get topic labels
    Lab = Labelling(study, Z, ignore_continuous = True)
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
    pca = PCA(n_components=2, whiten = True)
    pca.fit(X)
    X_r = pca.fit(X).transform(X)
    
    # Percentage of variance explained for each components
    print('Explained variance ratio (first two components): %s'
          % str(pca.explained_variance_ratio_))
    
    colors = [float(c)/float(Z) for c in range(0,Z)]
    colors = plt.cm.rainbow(np.linspace(0, 1, Z))
    plt.figure()
    for c, i, l in zip(colors, range(0,Z), labels):
        plt.scatter(X_r[topics == i, 0], X_r[topics == i, 1], c=c, cmap = 'rainbow', label=l)
    
    ax = plt.subplot(111)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, 0.5, box.height])
    fontP = FontProperties()
    if Z > 12: 
        columns = 2
    else: columns = 1
    plt.legend(prop = fontP, title = 'Topic Label', loc='center left', bbox_to_anchor=(1, 0.5), ncol = columns)
    plt.title('PCA of Study %s' %study)

    plt.show()
    return None

makePCA(datafile)