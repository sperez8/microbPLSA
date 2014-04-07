'''
Created on 07/04/2014

author: sperez8
'''

import sys, os
import numpy as np
from scipy.stats import spearmanr
import time

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)
import microbplsa

study = '1526'
z = 8

m = microbplsa.MicrobPLSA()
m.open_data(study = study, sampling = False) #get data matrix from the results file
rawdata = m.datamatrix
N, S = rawdata.shape
print rawdata.shape
#remove otus that are in less than X samples
X = 10
for i in range(0,N):
    if np.count_nonzero(rawdata[i,:]) > X:
        rawdata = np.delete(rawdata, i)

print rawdata.shape


# normalize 
rawdata = rawdata.astype(float)
totals = np.sum(rawdata, axis=0).astype(float)
data = rawdata/totals

t0 = time.time()
for i in range(0,N):
    for j in range(0,N):
        break
        if i!= j :
            r,p = spearmanr(data[i,:],data[j,:])
            if (r>0.8 or r<-0.8) and p < 0.01:
                print (i,j), '\t',  r
    
print time.time()-t0