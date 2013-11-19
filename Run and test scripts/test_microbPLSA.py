'''
Created on 16/09/2013

author: sperez8
'''

import sys, os
from time import time

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

import microbplsa

f = '/Users/sperez/Documents/PLSAfun/EMPL data/study_1037_closed_reference_otu_table.biom'
#f = '/Users/sperez/Documents/workspace/myprojects/myplsa/otu_table.txt'

m = microbplsa.MicrobPLSA(f,sampling = False)

for z in [2,3,4,6,7,8,9,10,11,12]:
    print '\n\n\n ZZZZZZZzzzz is ',z, '\n\n\n' 
    t0 = time()
    model = m.runplsa(z, verbatim = True)
    m.saveresults('results' + z + 'topics')
    print '\n\n\n Topic Labels', model.topic_labels(None)
    print 'Time for analysis:', int(time()-t0)