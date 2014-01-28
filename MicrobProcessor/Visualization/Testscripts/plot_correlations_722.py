'''
Created on 22/01/2014

author: sperez8
'''

import os,sys
_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
_root_dir = os.path.dirname(_root_dir)
sys.path.insert(0, _root_dir)
from utilities import *


study = '722'
Z = 12
f = "/Users/sperez/git/microbPLSA/MicrobProcessor/Results/study_" + study + '_' + str(Z) +'_topics_.txt'
datafile = '/Users/sperez/Documents/PLSAfun/EMPL data/study_'+study+'_split_library_seqs_and_mapping/study_'+study+'_closed_reference_otu_table.biom'
metadatafile = '/Users/sperez/Documents/PLSAfun/EMPL data/study_'+study+'_split_library_seqs_and_mapping/metadata'+study+'.csv'

factors, metadata = get_metadata(metadatafile)

metatable = reorder_metadata(datafile,metadata)



ORG = np.array([True if 'human' in x else False for x in metatable[:,1]])



R = topic_point_bisectoral_correlation(f, ORG)
print '\n CORRELATIONS ORG:', R

