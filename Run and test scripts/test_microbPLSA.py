import sys, os
from time import time

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

import microbplsa

f = '/Users/sperez/Documents/PLSAfun/EMPL data/study_1037_closed_reference_otu_table.biom'
#f = '/Users/sperez/Documents/workspace/myprojects/myplsa/otu_table.txt'

m = microbplsa.MicrobPLSA(f,sampling = False)

t0 = time()
model = m.runplsa(5, verbatim = True)
m.saveresults('results')

print '\n\n\n Topic Labels', model.topic_labels(None)
print 'Time for analysis:', int(time()-t0)