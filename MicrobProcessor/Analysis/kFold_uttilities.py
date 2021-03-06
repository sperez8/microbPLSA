'''
Created on 06/08/2014

author: sperez8

Contains all KFold cross-validation methods.
Uses sklearn cross_validation module
'''

import sys, os
import numpy as np
from sklearn import cross_validation
from sklearn.metrics import mean_squared_error
from math import sqrt
import pickle

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)
import microbplsa

#lower the difference in log likelihood for folding in documents
EPS = 0.001

FOLDER = 'CrossValidation'
CROSS_VAL_LOCATION = os.path.join('Results',FOLDER)

def create_folds(m, k, z, shuffle = True, seed = None):
    #Create the folds and save the way we partitioned the data
    numSamples = m.dimensions()[1]
    kFolds = cross_validation.KFold(numSamples, n_folds = k, indices = False, shuffle = shuffle, random_state = seed)
    save_kFold(kFolds, k, z, m.study, m.name)
    print 'kFold sample iterator done.'
    return kFolds
    
def save_kFold(kFold, k, z, study = None, name = None):
    '''Save the k fold cross validation sample assignment'''
    kPartitions = []
    for train,test in kFold:
        a,b = list(train), list(test)
        kPartitions.append([a,b])
    
    kFoldFile = get_file_name(k,z, study, name, folded = False)
    f = open(kFoldFile,'w')
    pickle.dump(kPartitions, f)
    return None

def save_folded_data(foldedData, k, z, study = None, name = None):
    '''Save the folded in test data'''
    foldedFile = get_file_name(k, z, study, name, folded = True)
    f = open(foldedFile,'w')
    pickle.dump(foldedData, f)
    return None

def open_kFold(study, name, k, z, folded = False):
    '''Open the k fold cross validation folds'''
    kFoldFile = get_file_name(k,z, study, name, folded)
    f = open(kFoldFile,'r')
    data = pickle.load(f)
    return data

def train(k, kFolds, data, study, name, z, numRuns = 1, seed = 'None', override = False, useC = True, folder = FOLDER):
    i = 1
    for trainSamples,testSamples in kFolds:
        trainData, testData = data[:,trainSamples], data[:,testSamples]
        
        print '\nTraining dataset fold {0} of {1}'.format(i,k)
        m = microbplsa.MicrobPLSA()
        m.study = study
        m.name = name
        m.datamatrix = trainData
        
        add = '_cross_seed' + str(seed) + '_k' + str(k) + '(' + str(i) + ')'
        
        
        m.generate_runs(z_i = z, z_f = z, numRuns = numRuns, useC = useC, override = override, folder = folder, add_to_file = add)
        i += 1
    
    return None

def test(m, kFolds, k, z, run = 1, useC = True, seed = None, folder = FOLDER):
    study = m.study
    name = m.name
    data = m.datamatrix

    #i denotes the fold currently being tested
    i = 1
    foldedData = []
    for trainSamples,testSamples in kFolds:
        trainSamples = np.array(trainSamples)
        testSamples = np.array(testSamples)
        trainData, testData = data[:,trainSamples], data[:,testSamples]
        
        #open the right cross validation model file
        add = '_cross_seed' + str(seed) + '_k' + str(k) + '(' + str(i) + ')'
        i += 1
        m.open_model(z = z, run = run, useC = True, folder = folder, add_to_file = add)
        p_d_z_fold = m.model.p_d_z
        #fold in
        print "Folding in"
        p_d_z_test = m.fold_in(testData, eps = EPS, useC =  useC)
        
        #Check that folding indeed occurred
        if p_d_z_test == p_d_z_fold:
            print "Folding in didn't work!"
            
        foldedData.append(p_d_z_test)
        
    save_folded_data(foldedData, k, z, study, name) 
        
    return None

def measure_error(m, kFolds, k, z):
    '''Compare the p_d_z_test and p_d_z_train for the folded in documents'''
    study = m.study
    name = m.name
    
    #Get model for when the fold is included.
    m.open_model(z = z, run = 1, useC = True, folder = 'Models', add_to_file = None)
    p_d_z = m.model.p_d_z
    p_z_train = m.model.p_z
    #print 'train', p_z_train
    
    #get folded in data
    p_d_z_test_all = open_kFold(study, name, k, z, folded = True) 
        
    mse = []
    i=0
    for trainSamples,testSamples in kFolds:
        trainSamples = np.array(trainSamples)
        testSamples = np.array(testSamples)
        
        #open folds
        seed = 2
        add = '_cross_seed' + str(seed) + '_k' + str(k) + '(' + str(i+1) + ')'
        m.open_model(z = z, run = 1, useC = True, folder = FOLDER, add_to_file = add)
        p_z_fold = m.model.p_z
        #print 'fold', p_z_fold
        
        
        p_d_z_train = p_d_z[testSamples,:]
        p_d_z_test = p_d_z_test_all[i]
        
        #need to reorder p_d_z_train and p_d_z_test in order of the dominant topics so they line up!
        p_d_z_train_sorted = p_d_z_train[:,np.argsort(p_z_train)]
        p_d_z_test_sorted = p_d_z_test[:,np.argsort(p_z_fold)]
        
        mse.append(mean_squared_error(p_d_z_train_sorted, p_d_z_test_sorted))
        i+=1
        
    return mse

def save_mse(mse, k, z, study = None, name = None, seed = 2, run = 1):
    '''Save the folded in test data'''
    mseFile = get_file_name(k, z, study, name, mse = True)
    np.savetxt(mseFile, mse, delimiter=",")
    return None


def get_file_name(k, z, study = None, name = None, folded = False, mse = False):
    '''finds the path of the file with the dataset cross validation
        partitions for the current study, number of folds (k) and topic number (z)'''
    ext = '.txt'
    
    if study:
        fileName = 'study_' + study + '_z=' + str(z) + '_kFold_' + str(k)
    elif name:
        fileName = 'study_' + name + '_z=' + str(z) + '_kFold_' + str(k)
    else:
        print "please provide a name or a study for this kfold"
    
    if folded:
        fileName += '_folded'
        
    if mse:
        fileName += '_mse'
        ext = '.csv'
    
    kFoldFile = os.path.join(_root_dir, CROSS_VAL_LOCATION, fileName + ext)
    return kFoldFile












