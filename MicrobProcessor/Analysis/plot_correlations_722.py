'''
Created on 22/01/2014

author: sperez8
'''

import os,sys
from correlations import *
_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)
from utilities import *


study = '722'
Z = 5
f = "/Users/sperez/git/microbPLSA/MicrobProcessor/Results/study_" + study + '_' + str(Z) +'_topics_.txt'
datafile = '/Users/sperez/Documents/PLSAfun/EMPL data/study_'+study+'_split_library_seqs_and_mapping/study_'+study+'_closed_reference_otu_table.biom'
metadatafile = '/Users/sperez/Documents/PLSAfun/EMPL data/study_'+study+'_split_library_seqs_and_mapping/metadata'+study+'.csv'

factors, metadata = get_metadata(metadatafile)

for i,factor in enumerate(factors):
    print i, factor
metatable = reorder_metadata(datafile,metadata,study)


human = np.array([True if 'human' in x else False for x in metatable[:,12]])

R = topic_point_bisectoral_correlation(f, human)
print '\n CORRELATIONS human:', R

