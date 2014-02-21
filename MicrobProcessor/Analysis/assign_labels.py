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

def labeling(study, Z, resultfile = None, datafile = None, 
             metadatafile = None, labelfile = None):
    '''handles all the files and calls the right functions
        to create a labeling file.'''
    if resultfile == None:
        resultfile = "/Users/sperez/git/microbPLSA/MicrobProcessor/Results/study_" + study + '_' + str(Z) +'_topics_.txt'
    if datafile == None:
        datafile = '/Users/sperez/Documents/PLSAfun/EMPL data/study_'+study+'_split_library_seqs_and_mapping/study_'+study+'_closed_reference_otu_table.biom'
    if metadatafile == None:
        metadatafile = '/Users/sperez/Documents/PLSAfun/EMPL data/study_'+study+'_split_library_seqs_and_mapping/metadata'+study+'.csv'
    if labelfile == None:
        labelfile = '/Users/sperez/Documents/PLSAfun/EMPL data/study_'+study+'_split_library_seqs_and_mapping/topic'+str(Z)+'labels'+study+'.txt'

    print '\n\n\nStudy:', study, 'Z = ', Z
    print 'Files are:'
    print datafile
    print metadatafile
    print resultfile

    #store the name of the metadata columns in FACTORS = ['date', 'soil type', ...]
    #store the metadata in a numpy array with row: sample, col: data
    factors, metadata = get_metadata(metadatafile)
    #sometimes the samples aren't in the same order in the metadata 
    #as in the result files
    metatable = reorder_metadata(datafile,metadata,study)
    
    #test if different metadata factors are dichotomous, continuous
    #or categorical. The embedded dictionaries look like: 
    #factor_types{'categorical':[factorA:{cat1, cat2, cat3...}, factorB...] ....}
    factors_type, real_factors, F = organize_metadata(metatable,factors)
    
    #measure the correlation between each topic and each metadata factor
    #store these in a numpy array where row: topic, col: factor
    R = perform_correlations(real_factors, factors, factors_type, metatable, Z, F, resultfile)
    
    topiclabels = assign_topic_labels(R, real_factors)
    
    save_labels(topiclabels, labelfile)    
        
    print "Done assigning labels!"
    return R

def assign_topic_labels(R, factorlabels):
    '''for each topic, find the factor to which it is correlated
        the most and assign it the corresponding label'''
    labels = []
    for row in R:
        rowabs = np.absolute(row) #want to find the highest neg or pos correlation value
        max_r_index = np.argmax(rowabs)
        max_r = row[max_r_index]
        label = factorlabels[max_r_index]
        labels.append([label, max_r]) 
    return labels

def save_labels(labels, filename):
    '''Given the labels of each topic, they are saved in a 
        text file for further analysis'''
    
    f = open(filename, 'w')
    z = 1
    f.write('\t'.join(['Topic','Label', 'Correlation']))
    for (label, r) in labels:
        f.write('\n')
        f.write('\t'.join([str(z),label,str(r)]))
        z+=1
    f.close()
    return None








