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
        
        indTable = np.loadtxt(filename, delimiter = '\t', skiprows = 1, usecols = (0,1,2,3,4,6), dtype = {'names':('otus', 'A','B','stat', 'pvalue','group'),'formats':('i4','f  4','f4','f4','f4','i4')})
        
        return indTable
    
    def get_significant_otus(self, cutoff = 0.8):
        '''gets the otus with a p(w|z) > 0.8 for each topic'''
        otusTable = self.m.significant_otus(cutoff = cutoff)
                
        
        return None
    
    def compare(self):
        
        return None
    
    
    
    
    
    