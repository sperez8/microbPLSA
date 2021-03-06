'''
Created on 22/03/2013

author: sperez8
'''

import sys, os
import numpy as np

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
_root_dir = os.path.dirname(_root_dir)
sys.path.insert(0, _root_dir)
import microbplsa
from utilities import get_otu_ranks
analysis_dir = _root_dir+ '/Analysis'
sys.path.insert(0, analysis_dir)
from labelling import Labelling
from string import replace
from math import log
study = '1526'
z = 8
CORRELATION_THRESHOLD = 0.0
MANUAL_LABELS = ['Topic 1', 'Topic 2', 'Year Last submerged', 'Under water', 'Topic 5', 'Topic 6', 'Submerged between 2002-1999', 'Moki Camp']
pcoordfile = _root_dir + '/D3/pcplots/otus.js'
level = "phylum"

datafile = '/Users/sperez/Documents/PLSAfun/EMPL data/study_'+study+'_split_library_seqs_and_mapping/study_'+study+'_closed_reference_otu_table.biom'

m = microbplsa.MicrobPLSA()
plsa = m.open_model(study = study, z = z) #get model from the results file
#p_w_z = plsa.p_w_z #return otus topic distribution
p_w_z = plsa.word_topics().T
otus_map = m.open_otu_maps(datafile) # create {otu id: otu name} dictionary
W,Z =p_w_z.shape #number of otus and topics

#get labels     
#Lab = Labelling(study, Z, ignore_continuous = False, adjusted_metadata = True) #get labels!
#Lab.metadata(non_labels = [])
labels = ['\"'+l+'\"' for l in MANUAL_LABELS]

#get the average abundance of otus
m.open_data(study = study)
abundances = m.measure_abundance()


#get phylum of otus to color them appropriately
ranks = get_otu_ranks(otus_map, level = level)
print ("There are %i different %s."%(len(ranks), level))
    
f = open(pcoordfile, 'w')
f.write('var otus = [\n')


otus_index = otus_map["OTU_MAP"]
for (i,dist) in enumerate(p_w_z):
    for rank in ranks:
        if rank in otus_index[i]:
            line ='{'
            line += level+':\"'+rank+'\"'
            if abundances:
                line += ', abundances:'+ str(abundances[i]) 
            for j,p in enumerate(dist):
                line += ', ' + labels[j] + ':' + str(round(p,3))
            line += '},\n'
            f.write(line)
f.write('];\n')

f.write('var dim = [\n\'')
f.write(level+'\',\'')
f.write('abundances\',\'')
f.write('\',\''.join(labels))
f.write('\'];\n')

f.write('var types = {\n')
f.write('\"'+level+'\": \"string\",')
f.write('\"abundances\": \"number\",')

for label in labels:
    f.write(label+': \"number\",')
f.write('};\n')   
    
f.close()    
print "File is ready."





























