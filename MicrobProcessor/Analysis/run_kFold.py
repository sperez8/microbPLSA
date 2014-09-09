'''
Created on 11/07/2014

author: sperez8

Uses kFold cross-validation methods in kFold_uttilities.py to perform cross-validation on datasets
to find out how many topics minimizes the test set error.
This script generates the k-fold models to be used by perform_kfold_cv.py
'''

import kFold_uttilities as kf

#parameters
randomSeed = 2

study = None
name = 'bac_final0.03.otutable_GOODSAMPLES'
#study = '1037'
#name = None
useC = True
numRuns = 10
k = 5
fileInfo = '_cross_seed' + str(randomSeed) + '_k' + str(k)

#load the data
m = kf.load(study, name)
    
for z in [8,12,15,17,22,27,32,39,42,47,55,65,75,85]:
    kFolds = kf.create_folds(m, k, z, shuffle = True, seed = randomSeed)
    data = m.datamatrix
    
    #run plsa on each and save the "new model"
    kf.train(k, kFolds, data, study, name, z, numRuns = numRuns, seed = randomSeed, override = False)




