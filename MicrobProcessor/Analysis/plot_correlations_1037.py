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
Z = 7
f = "/Users/sperez/git/microbPLSA/MicrobProcessor/Results/study_" + study + '_' + str(Z) +'_topics_.txt'
datafile = '/Users/sperez/Documents/PLSAfun/EMPL data/study_'+study+'_split_library_seqs_and_mapping/study_'+study+'_closed_reference_otu_table.biom'
metadatafile = '/Users/sperez/Documents/PLSAfun/EMPL data/study_'+study+'_split_library_seqs_and_mapping/metadata.csv'

factors, metadata = get_metadata(metadatafile)
metatable = reorder_metadata(datafile,metadata,study)



ORG = np.array([True if 'ORG' in x else False for x in metatable[:,0]])
REF = np.array([True if 'REF' in x else False for x in metatable[:,0]])
biogeoclimatic_zone = np.array([True if 'Sub-boreal Spruce' in x else False for x in metatable[:,18]])
annual_season_precpt = [int(x) for x in metatable[:,5]]
annual_season_temp = [float(x) for x in metatable[:,6]]
elevation = [int(x) for x in metatable[:,7]]
extreme_event = [int(x) for x in metatable[:,16]]
collection_date =[int(x) for x in metatable[:,17]]
mean_coldest = [float(x) for x in metatable[:,22]]
mean_warmest = [float(x) for x in metatable[:,23]]
print mean_coldest


R = topic_point_bisectoral_correlation(f, ORG)
print '\n CORRELATIONS ORG:', R
R = topic_point_bisectoral_correlation(f, REF)
print '\n CORRELATIONS REF:', R
R = topic_point_bisectoral_correlation(f, biogeoclimatic_zone)
print '\n CORRELATIONS biogeoclimatic_zone:', R

R = topic_spearman_correlation(f, annual_season_precpt)
print '\n CORRELATIONS annual_season_precpt:', R
R = topic_spearman_correlation(f, annual_season_temp)
print '\n CORRELATIONS annual_season_temp:', R
R = topic_spearman_correlation(f, elevation)
print '\n CORRELATIONS elevation:', R
R = topic_spearman_correlation(f, extreme_event)
print '\n CORRELATIONS extreme_event:', R
R = topic_spearman_correlation(f, collection_date)
print '\n CORRELATIONS collection_date:', R
R = topic_spearman_correlation(f, mean_coldest)
print '\n CORRELATIONS mean_coldest:', R
R = topic_spearman_correlation(f, mean_warmest)
print '\n CORRELATIONS mean_warmest:', R
