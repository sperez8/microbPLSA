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

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)
from microbplsa import MicrobPLSA


def perform_correlations(factors, factors_type, metatable, Z, F, file):
    ''' sorts through all the metadata and calculates all 
        the correlations depending on the type of variable 
        in the metadata'''
    p_z_d = get_topic_proportions(file)
    Rs = np.zeros((Z,F)) # to be filled
    for type,metafactors in factors_type.iteritems():
        for metafactor in metafactors:
            if type == "constant":
                #we skip these since they irrelevant
                pass
            elif type == "continuous":
                index = factors.index(metafactor)
                data = list(metatable[:,index])
                Y = [0 if y == 'none' else float(y) for y in data]
                Rs[:,index] = correlation_continuous(p_z_d, Y)       
            elif type == "dichotomous":
                for factor in metafactor.keys():
                    labels = metfactor[factor]
                    index = factors.index(factor)
                    Y = np.array([True if labels[0] in x else False for x in metatable[:,index]])
                    Rs[:,index] = correlation_dichotomous(p_z_d, Y)
            elif type == "categorical":
                for factor, labels in metafactor.iteritems():
                    for label in labels:
                        index = factors.index(factor) ###not right...
                        Y = np.array([True if label in x else False for x in metatable[:,index]])
                        Rs[:,index] = correlation_dichotomous(p_z_d, Y)         
    #now we check that we have file the correlation matrix!       
    #zeroes = sum(Rs == 0)
    #if zeroes >= 1: raise CorrelationProblem('Some entries, in the correlation matrix remain unfilled.')
    
    
    #### NOTE: currently the order of factors and columns and Rs dont correspond!!!!
    
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
    
def correlation_continous(p_z_d, Y):
    '''calculates the correlation between all topics
        and a continuous variable'''
    R = []
    for z in range(0,p_z_d.shape[0]):
        X = p_z_d[z]
        r = spearmanr(X, Y)
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