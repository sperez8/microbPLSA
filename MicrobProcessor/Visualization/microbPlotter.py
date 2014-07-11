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
import math
from matplotlib.font_manager import FontProperties
   
_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)
from microbplsa import *
from utilities import zipper

analysis_dir = os.path.join(_root_dir, 'Analysis')
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

def topic_distribution(name = None, study = None, order = None, **options):
    '''Given a model p_z,p_w_z,p_d_z, we can plot the document's distribution
    using p(z|d) = normalized((p(d|z)*p(z))) '''
    
    m = microbplsa.MicrobPLSA()
    m.open_model(name = name, study = study, **options) #get model from the results file
    #return document's distribution
    p_z_d = m.model.document_topics()
    
    Z,N =p_z_d.shape #number of samples
    if order is not None:
        p_z_d = p_z_d[:,order]
    n = np.arange(N)
    width = 25.0/float(N) #scale width of bars by number of samples
    p = [] #list of plots
    colors = plt.cm.rainbow(np.linspace(0, 1, Z))    
    
    Lab = Labelling(m, ignore_continuous = False)
    Lab.metadata(non_labels = ['BarcodeSequence'])
    R = Lab.correlate()
    labels_r = Lab.assignlabels(R,num_labels = 1)
    labels, r = zip(*labels_r)
    labels = [l.replace('(','\n(') for l in labels]
    
    #sort and organize labels and topics so they are always plotted in the same order
    labelsUnsorted = zipper(labels,range(0,Z))
    labelsUnsorted.sort()
    labels, Zrange = zip(*labelsUnsorted)
    Zrange = list(Zrange)
    p.append(plt.bar(n, p_z_d[Zrange[0],:], width, color=colors[0], linewidth = 0))
    height = p_z_d[Zrange[0],:]
    for i,z in enumerate(Zrange[1:]):
        p.append(plt.bar(n, p_z_d[z,:], width, color=colors[i+1], bottom=height, linewidth = 0))
        height += p_z_d[z,:]
    
    
    plt.ylabel('Probability P(z|d)')
    plt.xlabel('Sample')
    plt.title('Sample\'s topic distribution')
    #plt.xticks(np.arange(0,width/2.0,N*width), ['S'+str(n) for n in range(1,N)])

    topiclegend = ['Topic' + str(Zrange[labels.index(l)]+1) + ': '+ l + '\n ('+ str(r[Zrange[labels.index(l)]]) + ')' for l in labels]
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
    plt.figure(1, figsize=(8,8))
    
    labelset = list(set(colorlabel))
    #print labelset
    colors = plt.cm.rainbow(np.linspace(0, 1,len(labelset)+1))
    #colors = ['r','b','y','m']
    
    for x,y,c in zipper(X,Y,colorlabel):
        plt.scatter(x,y, color=colors[labelset.index(c)])
    
    
    plt.ylabel(factor)
    plt.xlabel('Topic proportion')
    plt.title('Scatter plot of proportion of Topic ' + str(z+1) + ' and ' + factor)
     
    plt.legend(labelset)
    return plt


def loglikelihood_curve(study = None, name = None, run = 'all', useC = False, save = False):
    '''Given a dataset we can find the models p_z,p_w_z,p_d_z for 
    different number of topics Z and can plot the loglikelihood vs. Z curve'''
    logl = []
    topic = []
    
    files_found = False
    if type(run) == int : run = "_run" + str(run)
    elif run == 'all': run = "_*"
    add = ''
    if useC:
        add = '_with_C'
    if study is not None:
        study = str(study)
        RESULT_FILE_TEMPLATE = 'study_' + study + '*_topics' + add + run + '.txt' #what a result file looks like
    else:
        RESULT_FILE_TEMPLATE = 'study_' + name + '*_topics' + add + run + '.txt' #what a result file looks like
        
    m = microbplsa.MicrobPLSA()
    m.open_data(study = study, name = name)
    
    for file in os.listdir(os.path.join(_root_dir, RESULTS_LOCATION)):        
        if fnmatch.fnmatch(file, RESULT_FILE_TEMPLATE):
            print 'Calculating LogLikelihood of model from the file: ', file
            files_found = True
            Z = int(re.findall(r'\d+_topic', file)[0].split('_')[0])
            print 'Getting model...'
            m.open_model(modelFile = os.path.join(_root_dir, RESULTS_LOCATION, file)) #get model from the results file
            print 'Calculating...'
            L = m.loglikelihood()
            
            if Z in topic:
                logl[topic.index(Z)].append(L)
            else:
                topic.append(Z)
                logl.append([L])
            print "Z = {0}, L = {1}".format(Z,L)
                
    logl_std = [np.std(x) for x in logl]
    log_count = [len(x) for x in logl]
    logl = [np.mean(x) for x in logl]
    if not files_found: 
        print "There were no files found using the template:" + RESULT_FILE_TEMPLATE
        sys.exit()
    
    topic.sort()
    logl, logl_std = zip(*sorted(zipper(logl,logl_std)))
    plt.plot(topic,logl,'b-')
    #plt.plot(topic,logl,'m.')
    plt.errorbar(topic, logl, yerr=logl_std, fmt='m.')
    plt.ylabel('LogLikelihood')
    if study:
        plt.title('Loglikelihood versus number of topics for study ' + study )
    else: 
        plt.title('Loglikelihood versus number of topics for study ' + str(name) )
    plt.xlabel('Z, number of topics')
    
    if save:
        topic = [str(round(t,2)) for t in topic]
        count = [str(t) for t in log_count]
        logl = [str(round(t,2)) for t in logl]
        logl_std = [str(round(t,1)) for t in logl_std]
        if study:
            logfile = open(os.path.join(_root_dir, RESULTS_LOCATION, 'Loglikelihoods', 'logs_' + study + '.txt'), 'w')
        elif name:
            logfile = open(os.path.join(_root_dir, RESULTS_LOCATION, 'Loglikelihoods', 'logs_' + str(name) + '.txt'), 'w')
        logfile.write('\t'.join(topic))
        logfile.write('\n')
        logfile.write('\t'.join(count))
        logfile.write('\n')
        logfile.write('\t'.join(logl))
        logfile.write('\n')
        logfile.write('\t'.join(logl_std))
        
    return plt
    

def piechart(z, groups):
    '''gets the indicator species values, compares them
        to the top otus per topic and plots a pie chart to show the
        representation of otus in each category'''
    labels = ["topic" + str(z) for z in range(1,z+1)]
    labels.insert(0,"Not associated\n to topics")

    for group, values in groups.items():
        plt.close('all')
        
        total = float(values[0])
        sum = float(np.sum(values[1:]))
        sizes = [float(x)/total*100 for x in values[1:]]
        sizes.insert(0,(1- sum/total)*100)
        
        colors = plt.cm.rainbow(np.linspace(0, 1, z+1))
        explode = [0 for x in range(0,z)]
        explode.insert(0,0.1)
        
        plt.pie(sizes, labels=labels, colors = colors, explode = explode,
                autopct='%1.1f%%', shadow=True, startangle=90)
        # Set aspect ratio to be equal so that pie is drawn as a circle.
        plt.axis('equal')
        plt.title("Indicator Otus for Group" + str(group) + " with "+str(int(total))+" OTUs", verticalalignment = 'bottom', horizontalalignment = 'right')
        yield group, plt





