'''
Created on 27/11/2013

author: sperez8
'''
import sys, os

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

import microbplsa


Z = 8
study = '1526'
N_otus = 5

m = microbplsa.MicrobPLSA()
biom_data =m.open_data(study = study)
map = m.open_otu_maps(biom_data)['OTU_MAP']
m.open_model(study = study, z = Z)

print map

otu_labels = m.model.topic_labels(None, N_otus)
for label in otu_labels:
    print label
    print [map[o] for o in label]