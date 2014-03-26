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
study = '1037'
biom_data = '/Users/sperez/Documents/PLSAfun/EMPL data/study_1037_closed_reference_otu_table.biom'
f = "/Users/sperez/git/microbPLSA/MicrobProcessor/Results/study_"+study+"_"
end = "_topics_.txt"

m = microbplsa.MicrobPLSA()
m.open_otu_maps(biom_data)


print time.time()-t0
t0 = time.time()


for z in range(2,10):
    print '\nz = ', z
    labels = m.topic_OTUS(f+str(z)+end,N)
    for label in labels:
        print label