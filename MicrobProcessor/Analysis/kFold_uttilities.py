'''
Created on 06/08/2014

author: sperez8

Contains all KFold cross-validation methods.
Uses sklearn cross_validation module
'''

import sys, os
import numpy as np
from sklearn import cross_validation

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)
import microbplsa

FOLDER = 'CrossValidation'

def load(study, name):
    m = microbplsa.MicrobPLSA()
    m.open_data(study = study, name = name)
    print 'Data loaded.'
    return m

def create_folds(m, k, z, shuffle = True, seed = None):
    #Create the folds and save the way we partitioned the data
    numSamples = m.dimensions()[1]
    kFolds = cross_validation.KFold(numSamples, n_folds = k, indices = False, shuffle = shuffle, random_state = seed)
    m.save_kFold(kFolds, k, z)
    print 'kFold sample iterator done.'
    return kFolds

def train(k, kFolds, data, study, name, z, numRuns = 1, seed = None, override = False, useC = True, folder = FOLDER):
    i = 1
    for trainSamples,testSamples in kFolds:
        trainData, testData = data[:,trainSamples], data[:,testSamples]
        
        print '\nTraining dataset fold {0} of {1}'.format(i,k)
        m = microbplsa.MicrobPLSA()
        m.study = study
        m.name = name
        m.datamatrix = trainData
        
        if seed is None:
            seed = 'None'
        fileInfo = '_cross_seed' + str(seed) + '_k' + str(k)
        add = fileInfo + '(' + str(i) + ')'
        
        
        m.generate_runs(z_i = z, z_f = z, numRuns = numRuns, useC = useC, override = override, folder = folder, add_to_file = add)
        i += 1
    
    return None

def test(m, kFolds, k, z):
    study = m.study
    name = m.name
    data = m.datamatrix
    
    kFold = m.open_kFold(study, name, k, z)
    
    for trainSamples,testSamples in kFolds:
        trainData, testData = data[:,trainSamples], data[:,testSamples]
        p_d_z_test = m.fold_in(testData, useC =  False)
    
    '''in development'''
        
    return None