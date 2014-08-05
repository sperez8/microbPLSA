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
study = '1037'
name = None
z = 2
z_inc = 1
useC = True
numRuns = 100
#options
k = 2 #for k-fold validation
fileInfo = '_cross_seed' + str(randomSeed) + '_k' + str(k)
folder = 'CrossValidation'

#load the data
m = microbplsa.MicrobPLSA()
m.open_data(study = study, name = name)
data = m.datamatrix

#First we split the data into k-sub-samples
kFold = cross_validation.KFold(n=data.shape[1], n_folds = k, indices = False, shuffle = True, random_state = randomSeed)
#and save the way we partitioned the data
m.save_kFold(kFold,z,k)

#test that diversity of sub samples are similar
#(in development...)

#run plsa on each and save the "new model"
i = 1
for trainSamples,testSamples in kFold:
    trainData, testData = data[:,trainSamples], data[:,testSamples]
    
    m = microbplsa.MicrobPLSA()
    m.study = study
    m.name = name
    m.datamatrix = trainData
    m.generate_runs(z_i = z, z_f = z, z_inc = z_inc, numRuns = numRuns, useC = useC, override = False, folder = folder, add_to_file = fileInfo + '(' + str(i) + ')')
    i += 1


#Load test data
kFold = m.open_kFold(study, name, k, z)
   
#Fold in
print '\n*'+'-'*25+'Folding'+'-'*25+'*\n'

for trainSamples,testSamples in kFold:
    trainData, testData = data[:,trainSamples], data[:,testSamples]

    p_d_z_test = m.fold_in(testData, useC =  False)
    
    '''
    p_z_d = m.model.p_z * p_d_z_test
    print m.model.p_d_z
    print np.sum(m.model.p_d_z, axis = 0)
    print p_z_d
    print np.sum(p_z_d, axis = 0)  
    

#collect all the data and plot it for all topic numbers

'''








