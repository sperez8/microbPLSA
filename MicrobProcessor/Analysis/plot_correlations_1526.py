'''
Created on 29/01/2014

author: sperez8
'''

import os,sys
_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)
from utilities import *
from correlations import *

study = '1526'
Z = 5
f = "/Users/sperez/git/microbPLSA/MicrobProcessor/Results/study_" + study + '_' + str(Z) +'_topics_.txt'
datafile = '/Users/sperez/Documents/PLSAfun/EMPL data/study_'+study+'_split_library_seqs_and_mapping/study_'+study+'_closed_reference_otu_table.biom'
metadatafile = '/Users/sperez/Documents/PLSAfun/EMPL data/study_'+study+'_split_library_seqs_and_mapping/metadata'+study+'.csv'

factors, metadata = get_metadata(metadatafile)

for i,factor in enumerate(factors):
    #print i, factor
    continue
metatable = reorder_metadata(datafile,metadata,study)

#print metatable

for x in [3,6,14,17]:
    variable_options = organize_metadata(metatable[:,x])
    print "\n\n\nOptions", variable_options
    for variable in variable_options.keys():
        category = np.array([True if variable in i else False for i in metatable[:,x]])
        R = topic_category_correlation(f, variable)
        i = 0
        for chi,p in R:
            #print chi, p
            #if p<0.9995:
            print 'CORRELATION ', variable, ':', chi,p, i
            i+=1

