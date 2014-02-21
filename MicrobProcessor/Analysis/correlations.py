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
import microbplsa

DECIMALPTS = 2


def perform_correlations(realfactors, factors, factors_type, metatable, Z, F, file):
    ''' sorts through all the metadata and calculates all 
        the correlations depending on the type of variable 
        in the metadata'''
    p_z_d = get_topic_proportions(file)
    Rs = np.zeros((Z,F)) # to be filled
    for ftype,metafactors in factors_type.iteritems():
        for metafactor in metafactors:
            if ftype == "continuous":
                factor = metafactor.keys()[0]
                m_index = factors.index(factor)
                r_index = realfactors.index(factor)
                data = list(metatable[:,m_index])
                Y = numericize(data)
                Rs[:,r_index] = correlation_continuous(p_z_d, Y)    
            elif ftype == "dichotomous":
                for factor in metafactor.keys():
                    labels = metafactor[factor]
                    m_index = factors.index(factor)
                    r_index = realfactors.index(factor)
                    Y = np.array([x == labels[0] for x in metatable[:,m_index]])
                    Rs[:,r_index] = correlation_dichotomous(p_z_d, Y)
            elif ftype == "categorical":
                for factor, options in metafactor.iteritems():
                    for opt in options:
                        label = opt[opt.index('(')+1:-1] 
                        m_index = factors.index(factor)
                        r_index = realfactors.index(opt)
                        Y = np.array([x == label for x in metatable[:,m_index]])
                        Rs[:,r_index] = correlation_dichotomous(p_z_d, Y)

    #now we check that we have filled the correlation matrix!     
    zeros = sum(sum(Rs == 0)) #measure how many entries are 0. need to sum twice over both dimensions
    if zeros >= 1:
        index = np.where(Rs == 0.0)
        print '******************'*10
        print 'WARNING: ', str(zeros)+ ' entrie(s) in the correlation matrix remain unfilled at position(s):' + str(index)
        if zeros >= 2:
            strangefactors = []
            for i in index:
                strangefactors.append(realfactors[i[1]])
        else: strangefactors =  realfactors[index[1][0]]
        print 'These positions correspond to following metadata factors:', strangefactors
        print '******************'*10
    
    #We round the double floats to 2 decimal points, but only after checking for zeros.
    R = np.around(Rs, DECIMALPTS)
    return R

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
        R.append(r)
    return np.array(R)
    
def correlation_continuous(p_z_d, Y):
    '''calculates the correlation between all topics
        and a continuous variable'''
    R = []
    for z in range(0,p_z_d.shape[0]):
        X = p_z_d[z]
        r = spearmanr(X, Y)[0]
        R.append(r)
    return np.array(R)
                                                                           
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

def numericize(data):
    ''' Data is a list f strings that need to be turned
    into floats. However sometimes they contain ',' instead of
    '.' and '-' to show ranges. We transform the data here'''
    data1 = [d.replace(',','.') for d in data]
    #check for range variables like '30-39'
    data2=[]
    for d in data1:
        if '-' in d and d.split('-')[0]: #need both statements here in case of neg numbs.
                start_range = float(d.split('-')[0])
                end_range = float(d.split('-')[1])
                middle = (start_range + end_range)/2.0
                data2.append(middle)
        else:
            data2.append(float(d))
    return data2
    




























