'''
Created on 11/07/2014

author: sperez8

Uses kFold cross-validation methods in kFold_uttilities.py to perform cross-validation on datasets
to find out how many topics minimizes the test set error.
This script uses the k-fold models generated using run_kfold.py
'''

import kFold_uttilities as kf

#parameters
randomSeed = 2

#study = None
#name = 'bac_final0.03.otutable_GOODSAMPLES'
study = '1037'
name = None
useC = False
k = 5

#load the data
m = kf.load(study, name)
    
for z in [2]:
    #load k-fold partition of samples
    kFolds = kf.open_kFold(study, name, k, z)
    kf.test(m, kFolds, k, z, useC = useC, seed = randomSeed)
