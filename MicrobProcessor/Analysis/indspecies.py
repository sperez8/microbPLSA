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
            
class IndicatorSpecies():
    '''A class to obtain indicator species from the indspecies R package 
        and comapre them to PLSA dominant otus'''

    def __init__(self, study):
        self.study = study
        return None
    
    def find_indspecies(study):
        ''' Obtains indicator species table resulting from
            analysis in R using the indspecies package '''
        
        folder =  '/Users/sperez/Documents/PLSAfun/EMPL data/study_'+study+'_split_library_seqs_and_mapping/'
        filename = folder + "indspecies_study_" + study + ".txt"
        
        indTable = np.loadtxt(filename, delimiter = '\t', skiprows = 1, usecols = (0,1,2,3,4,6), dtype = {'names':('otus', 'A','B','stat', 'pvalue','group'),'formats':('i4','f  4','f4','f4','f4','i4')})
        
        return indTable