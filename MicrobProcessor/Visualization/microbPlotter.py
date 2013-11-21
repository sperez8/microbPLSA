'''
Created on 20/11/2013

author: sperez8

Functions to plot data.
'''
import sys, os
from time import time

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

from utilities import open_model


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
    p_z, p_w_z, p_d_z = open_model(file)
    print p_d_z