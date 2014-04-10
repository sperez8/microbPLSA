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
    
    def __init__(self, study = None, biomFile = None):
        ''' Opens the probs of a model previously computed and saved in a json file '''
        m = microbplsa.MicrobPLSA()
        m.open_data(study = study, file = biomFile) #get data matrix from the results file
        self.rawData = m.datamatrix
        self.N,self.S = self.rawData.shape 
        return None
         
    def remove_rare_otus(self,minSamples = None):
        if minSamples == None:
            minSamples = int(0.1*self.S) #default is that otus must be present in 10 percent of samples 
        if minSamples <=1: 
            newData = np.copy(self.rawData)
            return None
        newData = np.copy(self.rawData)
        
        
        print newData.shape
        newData = newData[np.all(np.count_nonzero(newData) >= minSamples, axis = 0)]
        print np.all(np.count_nonzero(newData) >= minSamples, axis = 0)
        
        print newData
        return None     
    
    def normalize(self):
        rawdata = self.rawdata.astype(float)
        totals = np.sum(rawdata, axis=0).astype(float)
        self.data = rawdata/totals
        return None
    
    def measure_correlations(self):
        for i in range(0,self.N):
            for j in range(0,self.N):
                break
                if i!= j :
                    r,p = spearmanr(data[i,:],data[j,:])
                    if (r>0.8 or r<-0.8) and p < 0.01:
                        print (i,j), '\t',  r













