'''
Created on 07/04/2014

author: sperez8
'''

import sys, os
import numpy as np
from scipy.stats import spearmanr

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)
import microbplsa



class NetworkAnalysis():
    ''' Build and analysis network from OTUs abundances '''
    
    def __init__(self, study = None, biomfile = None):
        ''' Opens the probs of a model previously computed and saved in a json file '''
        m = microbplsa.MicrobPLSA()
        m.open_data(study = study, file = biomfile) #get data matrix from the results file
        self.rawdata = m.datamatrix
        self.N,self.S = self.rawdata.shape 
        return None
         
    def remove_rare_otus(self,minSamples = None):
        if minSamples == None:
            minSamples = int(0.1*self.S) #default is that otus must be present in 10 percent of samples 
        newdata = np.append(self.rawdata.T, np.array(range(0,N)),axis=0)###
        print newdata.shape
        for i,row in enumerate(self.rawdata):
            print len(row)
            if np.count_nonzero(row) >= minSamples:
                newdata = 0
        
        return None     
    
    def normalize(self):
        rawdata = self.rawdata.astype(float)
        totals = np.sum(rawdata, axis=0).astype(float)
        self.data = rawdata/totals
        return None
    
    def measure_correlations(self):
        for i in range(0,N):
            for j in range(0,N):
                break
                if i!= j :
                    r,p = spearmanr(data[i,:],data[j,:])
                    if (r>0.8 or r<-0.8) and p < 0.01:
                        print (i,j), '\t',  r













