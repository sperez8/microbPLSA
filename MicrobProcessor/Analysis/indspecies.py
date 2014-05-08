'''
Created on 22/01/2014

author: sperez8

Performs indicator species analysis
'''
import os, sys
import numpy as np
from scipy import stats

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)
import microbplsa   
            
class IndSpecies():
    '''A class to obtain indicator species from the indspecies R package 
        and compare them to PLSA dominant otus'''

    def __init__(self, study, z):
        '''selects study and creates MicrobPLSA instance for that study'''
        self.study = study
        self.z = z
        self.m = microbplsa.MicrobPLSA()
        self.plsa = self.m.open_model(study = self.study, z = self.z)
        return None
    
    def find_indspecies(self):
        ''' Obtains indicator species table resulting from
            analysis in R using the indspecies package '''
        
        folder =  '/Users/sperez/Documents/PLSAfun/EMPL data/study_'+self.study+'_split_library_seqs_and_mapping/'
        filename = folder + "indspecies_study_" + self.study + ".txt"
        
        indTable = np.loadtxt(filename, delimiter = '\t', skiprows = 1, usecols = [0,1,2,3,4,6]) #, dtype = {'names':['otus', 'A','B','stat', 'pvalue','group'],'formats':['i4','f  4','f4','f4','f4','i4']})
        self.indTable = np.array(indTable)
        return None
    
    def get_significant_otus(self, cutoff = 0.8):
        '''gets the otus with a p(w|z) > 0.8 for each topic'''
        otusTable = self.m.significant_otus(cutoff = cutoff)
        self.otusTable = otusTable
        return otusTable 
        
    def compare(self):
        inds = self.indTable
        otus = self.otusTable
        
        groups = {}
        for ind, A,B, stat, pvalue, group in inds:
            group = int(group)  
            if group not in groups.keys():
                groups[group] = [0 for x in range(0,self.z+1)]
                groups[group][0] = np.sum([inds[:,5]==group]) #gets total number of indicator otus for group
                
            #now we find if the otu is a topic indicator:
            #CAN BE MORE EFFICIENT using np.where()
            for otu, p_w_z, z in otus:
                
                if ind == otu:
                    groups[group][int(z)] += 1
        return groups
    
    
    
    
    