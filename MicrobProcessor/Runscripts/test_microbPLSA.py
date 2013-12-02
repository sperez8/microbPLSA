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
from math import sqrt
#f = '/Users/sperez/Documents/workspace/myprojects/myplsa/otu_table.txt'

for study in ['659','722','1526','1037']:

    f = '/Users/sperez/Documents/PLSAfun/EMPL data/study_'+study+'_split_library_seqs_and_mapping/study_'+study+'_closed_reference_otu_table.biom'
    
    m = microbplsa.MicrobPLSA()
    (w,d) = m.open_data(f,sampling = True)
    
    print '\n\n\nStudy', study, 'has', w, 'otus and', d, 'samples.'
    
    num_topics = int(2*sqrt(d))
    print 'We will run PLSA with Z = 2 to', num_topics-1 
    
    
    for z in range(2,num_topics):
        print '\n ZZZZZZZzzzz is ',z, '\n' 
        t0 = time()
        model = m.runplsa(z, maxiter=5000, verbatim = False)
        name = f.split('/')[-1].split('_')
        name = name[0]+'_'+name[1] +'_'
        m.saveresults(filename = name+ str(z) + '_topics_', extension =  '.txt')
        print '\n Topic Labels', model.topic_labels(None)
        print 'Time for analysis:', int(time()-t0)