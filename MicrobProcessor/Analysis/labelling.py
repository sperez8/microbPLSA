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
    
    def __init__(self, study, Z, debug = False,  ignore_continuous = False, adjusted_metadata = True, resultfile = None, datafile = None):
        '''handles all the files and calls the right functions
            to create a labeling file.'''
        self.debug = debug
        self.ignore_continuous = ignore_continuous
        self.adjusted_metadata = adjusted_metadata
        self.Z = Z
        self.study = study

        if self.debug:
            print '\n\n\nStudy:', study, 'Z = ', Z
            print 'Files are:'
            print self.datafile
            print self.resultfile
        
        self.m = microbplsa.MicrobPLSA()
        return None

    def getlabels(self):
        self.metadata()
        R = self.correlate()
        return self.assignlabels(R)

    def metadata(self, metadatafile = None, reorder = True, non_labels = []):
        if metadatafile == None:
            metadatafile = '/Users/sperez/Documents/PLSAfun/EMPL data/study_'+self.study+'_split_library_seqs_and_mapping/metadata'+self.study+'.csv'
        
        #store the name of the metadata columns in FACTORS = ['date', 'soil type', ...]
        #store the metadata in a numpy array with row: sample, col: data
        self.factors, self.metadatamatrix = get_metadata(metadatafile, self.adjusted_metadata)
        #sometimes the samples aren't in the same order in the metadata 
        #as in the result files
        if reorder:
            datafile = self.m.open_data(study = self.study)
            json_data=open(datafile)
            alldata = json.load(json_data)
            json_data.close()
            data = alldata['columns']
            self.metadatamatrix = reorder_metadata(data,self.metadatamatrix,self.study)
        
        #test if different metadata factors are dichotomous, continuous
        #or categorical. The embedded dictionaries look like: 
        #factor_types{'categorical':[factorA:{cat1, cat2, cat3...}, factorB...] ....}
        self.factors_type, self.realfactors = organize_metadata(self.metadatamatrix,self.factors, non_labels)
        return self.metadatamatrix, self.factors_type, self.factors
        
    def correlate(self):
        '''measure the correlation between each topic and each metadata factor
            store these in a numpy array where row: topic, col: factor'''
               
        # get document's distribution for each topic
        model= self.m.open_model(self.study,self.Z) #get model from the results file
        p_z_d = model.document_topics()  
        R = perform_correlations(self.realfactors, self.factors, self.factors_type, self.metadatamatrix, self.Z, self.study, p_z_d, self.ignore_continuous)
        
        if self.debug:
            print '\nThe correlation matrix is:\n', R
            print "\nDone assigning labels!"
        return R

    def assignlabels(self, R, num_labels = 1):
        '''for each topic, find the factor to which it is correlated
            the most and assign it the corresponding label'''
        
        labels = []
        for i, row in enumerate(R):
            rowabs = np.absolute(row) #want to find the highest neg or pos correlation value
            topic_label = []
            n = 0
            while n != num_labels:
                max_r_index = np.argmax(rowabs)
                max_r = row[max_r_index]
                if num_labels == 1:
                    topic_label = (self.realfactors[max_r_index], max_r)
                else: topic_label.append((self.realfactors[max_r_index], max_r))
                rowabs[max_r_index]=0.0
                n+=1
            labels.append(topic_label) 
        return labels
    
    def save_labels(self, labels, labelfile = None):
        '''Given the labels of each topic, they are saved in a 
            text file for further analysis'''
        if labelfile == None:
            labelfile = '/Users/sperez/Documents/PLSAfun/EMPL data/study_'+self.study+'_split_library_seqs_and_mapping/topic'+str(self.Z)+'labels'+self.study+'.txt'
     
        f = open(labelfile, 'w')
        z = 1
        num_labels = len(labels[0])
        f.write('\t'.join(['Topic'] +['Label', 'Correlation']*num_labels))
        for topic_labels in labels:
            f.write('\n')
            line = str(z)
            for (label, r) in topic_labels:
                line += '\t' + label + '\t' + str(r)
            f.write(line)
            z+=1
        f.close()
        return None








