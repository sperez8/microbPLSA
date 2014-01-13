'''
Created on 20/11/2013

author: sperez8

Functions to plot data.
'''
import sys, os
import fnmatch
from time import time
import re

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

import microbplsa


def data_count(file):
    samples, datamatrix, otus = extract_data(file, False)
    #matrix with boolean values representing if OTU occurs or not
    binary_data = datamatrix > np.zeros(datamatrix.shape)
    
    #Measure the number of OTUs in each sample
    otu_count = np.sum(binary_data, axis = 0)
    #Measure the number of samples in which an OTU occurs
    otu_presence = np.sum(binary_data, axis = 1)
    #Measure number of reads per sample
    tags = np.sum(datamatrix, axis = 0)
    
    plt.subplot(1,3,1)
    bins = np.sort(tags)
    n = np.arange(bins.shape[0])
    plt.bar(n,bins,width = 0.8, color = 'green')
    plt.xlabel('Sample #')
    plt.ylabel('Tag or read count')
    plt.title('Sorted read count per sample.')
    
    
    #Make plot for sample diversity
    plt.subplot(1,3,2)
    bins = np.sort(otu_count)
    n = np.arange(bins.shape[0])
    plt.bar(n,bins,width = 0.8, color = 'blue')
    plt.xlabel('Sample #')
    plt.ylabel('OTU diversity count')
    plt.title('Sorted read count per sample.')
    
    #Make plot for OTU's presence in samples
    plt.subplot(1,3,3)
    plt.hist(otu_presence, bins=datamatrix.shape[1], normed=1, facecolor='purple')
    plt.xlabel('Number of samples')
    plt.ylabel('Proportion of OTUs in given number of samples')
    plt.title('Histogram of OTUs\'s number in count')
    plt.show()
    return None


def topic_distribution(file):
    '''Given a model p_z,p_w_z,p_d_z, we can plot the document's distribution
    using p(z|d) = normalized((p(d|z)*p(z))) '''
    
    m = microbplsa.MicrobPLSA()
    plsa = m.open_model(file) #get model from the results file
    
    #return document's distribution
    p_z_d = plsa.document_topics()
    
    Z,N =p_z_d.shape #number of samples
    n = np.arange(N)
    width = 10.0/float(N) #scale width of bars by number of samples
    p = [] #list of plots
    colors = plt.cm.rainbow(np.linspace(0, 1, Z))
    p.append(plt.bar(n, p_z_d[0,:], width, color=colors[0]))
    height = p_z_d[0,:]
    for z in range(1,Z):
        height
        p.append(plt.bar(n, p_z_d[z,:], width, color=colors[z], bottom=height))
        height += p_z_d[z,:]
    
    
    plt.ylabel('Probability')
    plt.title('Sample\'s topic distribution')
    #plt.xticks(np.arange(0,width/2.0,N*width), ['S'+str(n) for n in range(1,N)])
    plt.legend(p, ['Topic'+str(z) for z in range(1,Z+1)] )
    
    return plt

def loglikelihood_curve(study):
    '''Given a dataset we can find the models p_z,p_w_z,p_d_z for 
    different number of topics Z and can plot the loglikelihood vs. Z curve'''
    logl = []
    topic = []

    for file in os.listdir(_root_dir+'/Results/'):
        if fnmatch.fnmatch(file, 'study_'+study+'*.txt'):
            Z = int(re.findall(r'\d+', file)[1])
            f = '/Users/sperez/Documents/PLSAfun/EMPL data/study_'+study+'_split_library_seqs_and_mapping/study_'+study+'_closed_reference_otu_table.biom'
            m = microbplsa.MicrobPLSA()
            (w,d) = m.open_data(f,sampling = False)
            td = m.datamatrix
            plsa = m.open_model(_root_dir+'/Results/'+file) #get model from the results file
            L = m.loglikelihood()
            
            topic.append(Z)
            logl.append(L)
    
    plt.plot(topic,logl,'.')
    plt.ylabel('LogLikelihood')
    plt.title('Loglikelihood versus number of topics for study '+study)
    plt.xlabel('Z, number of topics')
    
    return plt
    
    
    