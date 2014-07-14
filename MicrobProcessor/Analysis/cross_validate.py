'''
Created on 11/07/2014

author: sperez8

Uses cross-validation function and plsa to do k-fold cross-validation on datasets
to find out how many topics minimizes the test set error.
'''

import sys, os
import numpy as np
from sklearn import cross_validation

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)
import microbplsa


#initial input
randomSeed = 2 #seed for reproducible randomization
study = '1526'
name = None
z = 2
z_inc = 1
useC = True

#options
k = 3 #for k-fold validation
fileInfo = '_cross_seed' + str(randomSeed) + '_k' + str(k)
folder = 'CrossValidation'

#load the data
m = microbplsa.MicrobPLSA()
m.open_data(study = study, name = name)
data = m.datamatrix
print data.shape

#First we split the data into k-sub-samples
kFold = cross_validation.KFold(n=data.shape[1], n_folds = k, indices = False, shuffle = True, random_state = randomSeed)
print kFold    

#test that diversity of sub samples are similar

#run plsa on each
i = 1
for trainSamples,testSamples in kFold:
    print sum(trainSamples), sum(testSamples)
    trainData, testData = data[:,trainSamples], data[:,testSamples]
    
    m = microbplsa.MicrobPLSA()
    m.study = study
    m.name = name
    m.datamatrix = trainData
    m.generate_runs(z_i = z, z_f = z, z_inc = z_inc, numRuns = 10, useC = useC, override = False, folder = folder, add_to_file = fileInfo + '(' + str(i) + ')')
    print m.loglikelihood()
    i += 1
    
    # fold-in k-th sample and measure fit
    
    
    

#collect all the data and plot it for all topic numbers










