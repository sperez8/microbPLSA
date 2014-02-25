'''
Created on 18/02/2014

author: sperez8

Uses functions from correlations.py and 
metdata_tools to assign labels to topics
'''

from metadata_tools import *
from correlations import *
import sys,os
_cur_dir = os.path.dirname(os.path.realpath(__file__))
_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)
import microbplsa

class Labelling():
    '''A class to handle the labelling of topics using metadata'''
    
    def __init__(self, study, Z, debug = False,  ignore_continuous = False, resultfile = None, datafile = None):
        '''handles all the files and calls the right functions
            to create a labeling file.'''
        self.debug = debug
        self.ignore_continuous = ignore_continuous
        self.Z = Z
        self.study = study
        
        if resultfile == None:
            self.resultfile = "/Users/sperez/git/microbPLSA/MicrobProcessor/Results/study_" + self.study + '_' + str(self.Z) +'_topics_.txt'
        if datafile == None:
            self.datafile = '/Users/sperez/Documents/PLSAfun/EMPL data/study_'+self.study+'_split_library_seqs_and_mapping/study_'+self.study+'_closed_reference_otu_table.biom'
   
        if self.debug:
            print '\n\n\nStudy:', study, 'Z = ', Z
            print 'Files are:'
            print self.datafile
            print self.resultfile
        
        return None

    def getlabels(self):
        self.metadata()
        R = self.correlate()
        return self.assignlabels(R)

    def metadata(self, metadatafile = None, reorder = True):
        if metadatafile == None:
            metadatafile = '/Users/sperez/Documents/PLSAfun/EMPL data/study_'+self.study+'_split_library_seqs_and_mapping/metadata'+self.study+'.csv'
        
        #store the name of the metadata columns in FACTORS = ['date', 'soil type', ...]
        #store the metadata in a numpy array with row: sample, col: data
        self.factors, self.metadata = get_metadata(metadatafile)
        #sometimes the samples aren't in the same order in the metadata 
        #as in the result files
        if reorder:
            self.metadata = reorder_metadata(self.datafile,self.metadata,self.study)
        
        #test if different metadata factors are dichotomous, continuous
        #or categorical. The embedded dictionaries look like: 
        #factor_types{'categorical':[factorA:{cat1, cat2, cat3...}, factorB...] ....}
        self.factors_type, self.realfactors = organize_metadata(self.metadata,self.factors)
        return self.metadata, self.factors_type, self.factors
        
    def correlate(self):
    #measure the correlation between each topic and each metadata factor
    #store these in a numpy array where row: topic, col: factor
        R = perform_correlations(self.realfactors, self.factors, self.factors_type, self.metadata, self.Z, self.resultfile, self.ignore_continuous)
        
        if self.debug:
            print '\nThe correlation matrix is:\n', R
            print "\nDone assigning labels!"
        return R

    def assignlabels(self, R):
        '''for each topic, find the factor to which it is correlated
            the most and assign it the corresponding label'''
        
        labels = []
        for row in R:
            rowabs = np.absolute(row) #want to find the highest neg or pos correlation value
            max_r_index = np.argmax(rowabs)
            max_r = row[max_r_index]
            label = self.realfactors[max_r_index]
            labels.append((label, max_r)) 
        return labels
    
    def save_labels(self, labels, labelfile = None):
        '''Given the labels of each topic, they are saved in a 
            text file for further analysis'''
        if labelfile == None:
            labelfile = '/Users/sperez/Documents/PLSAfun/EMPL data/study_'+self.study+'_split_library_seqs_and_mapping/topic'+str(self.Z)+'labels'+self.study+'.txt'
     
        f = open(labelfile, 'w')
        z = 1
        f.write('\t'.join(['Topic','Label', 'Correlation']))
        for (label, r) in labels:
            f.write('\n')
            f.write('\t'.join([str(z),label,str(r)]))
            z+=1
        f.close()
        return None








