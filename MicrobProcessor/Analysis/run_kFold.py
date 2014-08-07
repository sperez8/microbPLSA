'''
Created on 11/07/2014

author: sperez8

Uses kFold cross-validation methods in kFold_uttilities.py to perform cross-validation on datasets
to find out how many topics minimizes the test set error.
'''

import kFold_uttilities as kf

#parameters
randomSeed = 2

study = '1037'
name = None
#study = None
#name = 'bac_final0.03.otutable_GOODSAMPLES'

z = 2
useC = True
numRuns = 10
k = 2
fileInfo = '_cross_seed' + str(randomSeed) + '_k' + str(k)





#load the data and we split the data into k-sub-samples
m = kf.load(study, name)
kFolds = kf.create_folds(m, k, z, shuffle = True, seed = randomSeed)
data = m.datamatrix

#run plsa on each and save the "new model"
kf.train(k, kFolds, data, study, name, z, numRuns = numRuns, seed = randomSeed, override = False)

#now we test the left out data
kf.test(m, kFolds, k, z)




