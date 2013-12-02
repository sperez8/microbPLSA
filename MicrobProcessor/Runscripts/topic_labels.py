'''
Created on 27/11/2013

author: sperez8
'''
import sys, os

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

import microbplsa, time


t0 = time.time()


N=5
biom_data = '/Users/sperez/Documents/PLSAfun/EMPL data/study_1037_closed_reference_otu_table.biom'
f = "/Users/sperez/git/microbPLSA/MicrobProcessor/Results/results_"

m = microbplsa.MicrobPLSA()
m.open_otu_maps(biom_data)

t0 = time.time()
print time.time()-t0



end = '_topics_29Nov.txt'
for z in range(2,8):
    print '\nz = ', z
    labels = m.topic_OTUS(f+str(z)+end,N)
    for label in labels:
        print label
    
end = '_topics_30Nov.txt'
for z in range(8,12):
    print '\nz = ', z
    labels = m.topic_OTUS(f+str(z)+end,N)
    for label in labels:
        print label
        
print time.time()-t0