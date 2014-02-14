'''
Created on 16/09/2013

author: sperez8
'''

import sys, os
from time import time
import datetime

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

import microbplsa
from math import sqrt
#f = '/Users/sperez/Documents/workspace/myprojects/myplsa/otu_table.txt'


for study in ['1526','659','864','1037','722','1043','1702', '1642','1692','1579','1578','1526','1289','1034','990']:

    f = '/Users/sperez/Documents/PLSAfun/EMPL data/study_'+study+'_split_library_seqs_and_mapping/study_'+study+'_closed_reference_otu_table.biom'
    
    m = microbplsa.MicrobPLSA()
    (w,d) = m.open_data(f,sampling = False)
    
    print '\n\n\nStudy', study, 'has', w, 'otus and', d, 'samples.'
    
    num_topics = int(3*sqrt(d))
    print 'We will run PLSA with Z = 2 to', num_topics-1 
    
    
    for z in range(2,num_topics):
        name = f.split('/')[-1].split('_')
        name = name[0]+'_'+name[1] +'_'
        resultsfilename = name + str(z) + '_topics_.txt'
        try:
            open(_root_dir + '/Results/' + resultsfilename, "r")
            print "The results file already exists for study", study, "and ", z, "topics."
            continue #if result files already exists, we don't overide
        except IOError:
            #plsa has not been run with that topic nubmer and study so we run it!
            today = datetime.datetime.today()
            print '\n', today.strftime('%b %d, %Y @ %I:%M%p')
            print 'ZZZZZZZzzzz is ',z, '\n' 

            t0 = time()
            model = m.runplsa(z, maxiter=5000, verbatim = False)        
            m.saveresults(filename = resultsfilename, extension =  '.txt')
            print 'Topic Labels', model.topic_labels(None)
            print 'Time for analysis:', int(time()-t0)
            