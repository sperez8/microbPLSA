'''
Created on 27/11/2013

author: sperez8
'''
import sys, os

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

import microbplsa

N=5
reference = '/Users/sperez/Documents/PLSAfun/EMPL data/study_1037_closed_reference_otu_table.biom'
f = "/Users/sperez/git/microbPLSA/MicrobProcessor/Results/results_"

m = microbplsa.MicrobPLSA()


end = '_topics_26Nov.txt'
for z in range(2,7):
    m.topic_OTUS(reference, f+str(z)+end,N)
    
# end = '_topics_27Nov.txt'
# for z in range(7,13):
#     topic_labels(f+str(z)+end)