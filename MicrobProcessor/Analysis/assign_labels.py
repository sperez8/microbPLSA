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

def labeling(study, Z, resultfile = None,
              datafile = None, metadatafile = None):
    '''handles all the files and calls the right functions
        to create a labeling file.'''
    if resultfile == None:
        resultfile = "/Users/sperez/git/microbPLSA/MicrobProcessor/Results/study_" + study + '_' + str(Z) +'_topics_.txt'
    if datafile == None:
        datafile = '/Users/sperez/Documents/PLSAfun/EMPL data/study_'+study+'_split_library_seqs_and_mapping/study_'+study+'_closed_reference_otu_table.biom'
    if metadatafile == None:
        metadatafile = '/Users/sperez/Documents/PLSAfun/EMPL data/study_'+study+'_split_library_seqs_and_mapping/metadata'+study+'.csv'

    print 'Study:', study, 'Z = ', Z
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
        
    return R









