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


study = '1037'
Z = 6
f = "/Users/sperez/git/microbPLSA/MicrobProcessor/Results/study_" + study + '_' + str(Z) +'_topics_.txt'
datafile = '/Users/sperez/Documents/PLSAfun/EMPL data/study_'+study+'_split_library_seqs_and_mapping/study_'+study+'_closed_reference_otu_table.biom'
metadatafile = '/Users/sperez/Documents/PLSAfun/EMPL data/study_'+study+'_split_library_seqs_and_mapping/metadata.csv'

factors, metadata = get_metadata(metadatafile)
metatable = reorder_metadata(datafile,metadata)



ORG = np.array([True if 'ORG' in x else False for x in metatable[:,1]])
REF = np.array([True if 'REF' in x else False for x in metatable[:,1]])
biogeoclimatic_zone = np.array([True if 'Sub-boreal Spruce' in x else False for x in metatable[:,19]])
print biogeoclimatic_zone

R = topic_point_bisectoral_correlation(f, ORG)
print '\n CORRELATIONS ORG:', R
R = topic_point_bisectoral_correlation(f, REF)
print '\n CORRELATIONS REF:', R
R = topic_point_bisectoral_correlation(f, biogeoclimatic_zone)
print '\n CORRELATIONS biogeoclimatic_zone:', R
