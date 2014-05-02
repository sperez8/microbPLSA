'''
Created on 20/11/2013

author: sperez8

Functions to plot data.
'''
import sys, os
from os.path import join
import fnmatch
from time import time
import re
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from math import sqrt
from matplotlib.font_manager import FontProperties
   
_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)
import microbplsa

analysis_dir = _root_dir+ '/Analysis'
sys.path.insert(0, analysis_dir)
from labelling import Labelling

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

def topic_distribution(file,study, order = None):
    '''Given a model p_z,p_w_z,p_d_z, we can plot the document's distribution
    using p(z|d) = normalized((p(d|z)*p(z))) '''
    
    m = microbplsa.MicrobPLSA()
    plsa = m.open_model(file) #get model from the results file
    
    #return document's distribution
    p_z_d = plsa.document_topics()
    
    Z,N =p_z_d.shape #number of samples
    if order is not None:
        p_z_d = p_z_d[:,order]
    n = np.arange(N)
    width = 20.0/float(N) #scale width of bars by number of samples
    p = [] #list of plots
    colors = plt.cm.rainbow(np.linspace(0, 1, Z))
    p.append(plt.bar(n, p_z_d[0,:], width, color=colors[0], linewidth = 0))
    height = p_z_d[0,:]
    for z in range(1,Z):
        p.append(plt.bar(n, p_z_d[z,:], width, color=colors[z], bottom=height, linewidth = 0))
        height += p_z_d[z,:]
    
    
    plt.ylabel('Probability P(z|d)')
    plt.xlabel('Sample')
    plt.title('Sample\'s topic distribution')
    #plt.xticks(np.arange(0,width/2.0,N*width), ['S'+str(n) for n in range(1,N)])
    
    Lab = Labelling(study, Z, ignore_continuous = True)
    Lab.metadata(non_labels = ['BarcodeSequence'])
    R = Lab.correlate()
    labels_r = Lab.assignlabels(R,num_labels = 1)
    labels, r = zip(*labels_r)
    labels = [l.replace('(','\n(') for l in labels]

    topiclegend = ['Topic' + str(z+1) + ': '+ str(labels[z]) + '\n ('+ str(r[z]) + ')' for z in range(0,Z)]
    fontP = FontProperties()
    if N >60:
        fontP.set_size('xx-small')
    else: fontP.set_size('small')
    ax = plt.subplot(111)
    ratio = float(N)*0.5
    ax.set_aspect(ratio)
    ax.tick_params(axis = 'x', colors='w') #remove tick labels by setting them the same color as background
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, 0.5, box.height])

    if order is not None:
        plt.xticks(n, order, size = 'xx-small')
    if Z > 12: 
        columns = 2
    else: columns = 1
    plt.legend(p, topiclegend, prop = fontP, title = 'Topic Label', loc='center left', bbox_to_anchor=(1, 0.5), ncol = columns)
    return plt

def topiclabel_scatter(X,Y,factor,z, colorlabel):
    '''Given a study, a topic and a label we make scatter plot'''
    print 'x', X
    print Y
    plt.figure(1, figsize=(8,8))
    
    labelset = list(set(colorlabel))
    #print labelset
    colors = plt.cm.rainbow(np.linspace(0, 1,len(labelset)+1))
    #colors = ['r','b','y','m']
    
    for x,y,c in zip(X,Y,colorlabel):
        plt.scatter(x,y, color=colors[labelset.index(c)])
    
    
    plt.ylabel(factor)
    plt.xlabel('Topic proportion')
    plt.title('Scatter plot of proportion of Topic ' + str(z+1) + ' and ' + factor)
     
    plt.legend(labelset)
    return plt


def loglikelihood_curve(study, run = 'all', save = False):
    '''Given a dataset we can find the models p_z,p_w_z,p_d_z for 
    different number of topics Z and can plot the loglikelihood vs. Z curve'''
    logl = []
    topic = []
    
    files_found = False
    if run == 1: run  = '_'
    elif type(run) == int : run = "_run" + str(run)
    elif run == 'all': run = "_*"
    RESULT_FILE_TEMPLATE = 'study_'+study+'*_topics'+run+'.txt' #what a result file looks like
    
    f = '/Users/sperez/Documents/PLSAfun/EMPL data/study_'+study+'_split_library_seqs_and_mapping/study_'+study+'_closed_reference_otu_table.biom'
    m = microbplsa.MicrobPLSA()
    m.open_data(study = study)
    
    for file in os.listdir(_root_dir+'/Results/'):        
        if fnmatch.fnmatch(file, RESULT_FILE_TEMPLATE):
            print file
            files_found = True
            Z = int(re.findall(r'\d+', file)[1])
            plsa = m.open_model(file = _root_dir+'/Results/'+file) #get model from the results file
            L = m.loglikelihood()
            
            if Z in topic:
                logl[topic.index(Z)].append(L)
            else:
                topic.append(Z)
                logl.append([L])
    print topic
    print logl
    logl_std = [np.std(x) for x in logl]
    log_count = [len(x) for x in logl]
    logl = [np.mean(x) for x in logl]
    print logl_std
    if not files_found: 
        print "There were no files found using the template:" + RESULT_FILE_TEMPLATE
        sys.exit()
    
    topic.sort()
    logl, logl_std = zip(*sorted(zip(logl,logl_std)))
    plt.plot(topic,logl,'b-')
    #plt.plot(topic,logl,'m.')
    plt.errorbar(topic, logl, yerr=logl_std, fmt='m.')
    plt.ylabel('LogLikelihood')
    plt.title('Loglikelihood versus number of topics for study '+study)
    plt.xlabel('Z, number of topics')
    
    if save:
        topic = [str(round(t,2)) for t in topic]
        count = [str(t) for t in log_count]
        logl = [str(round(t,2)) for t in logl]
        logl_std = [str(round(t,1)) for t in logl_std]
        logfile = open(_root_dir+'/Results/'+'Loglikelihoods/logs_'+study+'.txt', 'w')
        logfile.write('\t'.join(topic))
        logfile.write('\n')
        logfile.write('\t'.join(count))
        logfile.write('\n')
        logfile.write('\t'.join(logl))
        logfile.write('\n')
        logfile.write('\t'.join(logl_std))
        
    return plt
    


