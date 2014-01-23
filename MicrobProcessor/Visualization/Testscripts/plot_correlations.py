'''
Created on 22/01/2014

author: sperez8
'''

import os,sys
_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)
from microbPlotter import *

f = "/Users/sperez/git/microbPLSA/MicrobProcessor/Results/study_"
study = '1037'
Z = 8
f = f + study + '_' + str(Z) +'_topics_.txt'

factors, data = metadata('/Users/sperez/Documents/PLSAfun/EMPL data/study_'+study+'_split_library_seqs_and_mapping/metadata.csv')

ORG = np.array([True if 'ORG' in x else False for x in data[:,1]])
REF = np.array([True if 'REF' in x else False for x in data[:,1]])


R = topic_correlation(f, ORG)
print '\n CORRELATIONS:', R
R = topic_correlation(f, REF)
print '\n CORRELATIONS:', R
