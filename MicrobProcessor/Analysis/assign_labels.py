'''
Created on 18/02/2014

author: sperez8

Uses functions from correlations.py and 
metdata_tools to assign labels to topics
'''

from metadata_tools import *
from correlations import *


def labeling(study, Z, resultfile = None,
              datafile = None, metadatafile = None):
    '''handles all the files and calls the right functions
        to create a labeling file.'''
    if resultfile == None:
        resultfile = "/Users/sperez/git/microbPLSA/MicrobProcessor/Results/study_" + study + '_' + str(Z) +'_topics_.txt'
    if datafile == None:
        datafile = '/Users/sperez/Documents/PLSAfun/EMPL data/study_'+study+'_split_library_seqs_and_mapping/study_'+study+'_closed_reference_otu_table.biom'
    if metadatafile == None:
        metadatafile = '/Users/sperez/Documents/PLSAfun/EMPL data/study_'+study+'_split_library_seqs_and_mapping/metadata.csv'

    #store the name of the metadata columns in FACTORS
    #store the metadata in a numpy array with row: sample, col: data
    factors, metadata = get_metadata(metadatafile)
    #sometimes the samples aren't in the metadata 
    #as in the result files
    metatable = reorder_metadata(datafile,metadata,study)

    factors_type = organize_metadata(metatable,factors)
    
    R = perform_correlations(factors, factors_type, metatable, Z, resultfile)
    
    
    
    return None