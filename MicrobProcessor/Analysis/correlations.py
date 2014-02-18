'''
Created on 29/01/2014

author: sperez8

contains a bunch of different utilities to read EMP data

'''
import numpy as np
import json
import sys, os
from math import sqrt
from scipy.stats import spearmanr
from scipy.stats import chisquare


_cur_dir = os.path.dirname(os.path.realpath(__file__))
_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)
import microbplsa


def perform_correlations(factors, factors_type, metatable, Z, file):
    ''' sorts through all the metadata and calculates all 
        the correlations depending on the type of variable 
        in the metadata'''
    p_z_d = get_topic_proportions(file)
    Rs = np.zeros((Z,len(factors)))
    for type,metafactors in factors_type.iteritems():
        if type == "constant":
            pass
        elif type == "continuous":
            pass        
        elif type == "dichotomous":
            for metafactor in metafactors:
                for factor, labels in metafactor.iteritems():
                    index = factors.index(factor)
                    Y = np.array([True if labels[0] in x else False for x in metatable[:,index]])
                    Rs[:,index] = correlation_dichotomous(p_z_d, Y)
        elif type == "categorical":
            pass        
    return Rs

def get_topic_proportions(file):
    '''Given a model p_z,p_w_z,p_d_z, stored in a result file, 
        we can find the topic distributions'''
    m = microbplsa.MicrobPLSA()
    plsa = m.open_model(file) #get model from the results file
    #return document's distribution for each topic
    return plsa.document_topics()  
    
def correlation_dichotomous(p_z_d, Y):
    '''calculates the correlation between all topics
        and a dichotomous variable'''
    R = []
    for z in range(0,p_z_d.shape[0]):
        X = p_z_d[z]
        r = pbcorrelation(X, Y)
        R.append(round(r,3))
    return np.array(R)
    
def assign_topic_labels(R):
    '''for each topic, find the factor to which it is correlated 
        best and assign it the corresponding label'''
    
    labels = {}
    return labels

def save_labels(labels, filename):
    '''Given the labels of each topic, they are saved in a 
        text file for further analysis'''
    
    f = open(filename, 'w')
    for label in labels:
        f.write(label)
    f.close()
                                                                           
def pbcorrelation(X, Y):
    ''' calculates point bisectoral correlation given two variable X and Y:
        X is a vector with the continuous variables, and
        Y is a vector with the True or False dichotomous statements'''
    M1 = X[Y]
    n1 = float(len(M1))
    M1 = np.mean(M1)
    M0 = X[np.logical_not(Y)]
    n0 = float(len(M0))
    M0 = np.mean(M0)
    s_n = np.std(X)
    r = ((M1-M0)/s_n)*sqrt((n1*n0)/((n1+n0)**2))
    return r


def topic_point_bisectoral_correlation(file,Y):
    '''Given a model p_z,p_w_z,p_d_z, and sample metadata boolean vector Y,
         we can calculate the correlation between the topic distributions 
         and dichotomous factors'''
    
    m = microbplsa.MicrobPLSA()
    plsa = m.open_model(file) #get model from the results file
    
    #return document's distribution
    p_z_d = plsa.document_topics()    
    Z,N =p_z_d.shape #number of samples
    R = []
    N
    for z in range (0,Z):
        X = p_z_d[z]
        r = pbcorrelation(X,Y)
        R.append(round(r,2))
   
    return R
    
def topic_spearman_correlation(file,Y):
    '''Given a model p_z,p_w_z,p_d_z, and sample metadata boolean vector Y,
         we can calculate the correlation between the topic distributions 
         and continuous factors'''
    
    m = microbplsa.MicrobPLSA()
    plsa = m.open_model(file) #get model from the results file
    
    #return document's distribution
    p_z_d = plsa.document_topics()    
    Z,N =p_z_d.shape #number of sampless
    R = []
    for z in range (0,Z):
        X = p_z_d[z]
        R.append([round(x,3) for x in spearmanr(X,Y)])
   
    return R

def topic_category_correlation(file, Y):
    '''FIX ME!!!'''
    
    
    '''Given a model p_z,p_w_z,p_d_z, and sample metadata with 
        categorical options stored in Y, we can calculate the correlation
        between the topic distributions and categorical factors'''
    
    m = microbplsa.MicrobPLSA()
    plsa = m.open_model(file) #get model from the results file
    p_z = plsa.p_z
    
    #return document's distribution
    p_z_d = plsa.document_topics()    
    Z,N =p_z_d.shape #number of sampless
    R = []
    for z in range(0,Z):
        R = 0
    
    return R