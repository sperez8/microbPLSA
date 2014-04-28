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

study = '1526'
z = 8
CORRELATION_THRESHOLD = 0.0
pcoordfile = _root_dir + '/D3/pcplots/otus.js'
level = "phylum"

datafile = '/Users/sperez/Documents/PLSAfun/EMPL data/study_'+study+'_split_library_seqs_and_mapping/study_'+study+'_closed_reference_otu_table.biom'

m = microbplsa.MicrobPLSA()
plsa = m.open_model(study = study, z = z) #get model from the results file
p_z_w = plsa.word_topics() #return otus topic distribution
otus_map = m.open_otu_maps(datafile) # create {otu id: otu name} dictionary
Z,W =p_z_w.shape #number of otus and topics
print W,Z
   
#get labels     
Lab = Labelling(study, Z, ignore_continuous = False, adjusted_metadata = True) #get labels!
Lab.metadata(non_labels = [])
R = Lab.correlate()
labels_r = Lab.assignlabels(R,num_labels = 1)
oldlabels, r = zip(*labels_r)
goodlabels = []
for lab, r in labels_r:
    if r > CORRELATION_THRESHOLD or r < -CORRELATION_THRESHOLD:
        goodlabels.append(lab)
print ("Only %i/%i passed the correlation threshold of %1.1f"%(len(goodlabels), len(oldlabels), CORRELATION_THRESHOLD))

labels = [replace(l,' (', '_') for l in oldlabels]
labels = [replace(l,' ', '_') for l in labels]
labels = [replace(l,')','') for l in labels]
labels = [replace(l,':', '_') for l in labels]
labels = [replace(l,'.', '_') for l in labels]
labels = [replace(l,'-', '_') for l in labels]

#get phylums
ranks = get_otu_ranks(otus_map, level = level)
print ("There are %i different %s."%(len(ranks), level))
    
f = open(pcoordfile, 'w')
f.write('var otus = [\n')

otus_index = otus_map["OTU_MAP"]
for (i,dist) in enumerate(p_z_w.T):
    for rank in ranks:
        if rank in otus_index[i]:
            line ='{'
            line += level+':\"'+rank+'\"'
            for j,p in enumerate(dist):
                line += ', ' + labels[j] + ':' + str(round(p,3)) 
            line += '},\n'
            f.write(line)
f.write('];\n')

f.write('var dim = [\n\'')
f.write(level+'\',\'')
f.write('\',\''.join(labels))
f.write('\'];\n')

f.write('var types = {\n')
f.write('\"'+level+'\": \"string\",')

for label in labels:
    f.write('\"'+label+'\": \"number\",')
#unfortunately we have to iter through all possible factors
#to find the ones that are labels
#could be more efficient but it would mean changing the way
#the factor type is stored.
#         for ftype,factors in Lab.factors_type.iteritems():
#             for factor in factors:
#                 if ftype == "continuous":
#                     if factor in labels:
#                         f.write('\"'+factor+'\": \"number\",')
#                 elif ftype == "dichotomous" or ftype == "categorical":
#                     for key, options in factor.iteritems():
#                         for option in options:
#                             if option in labels:
#                                 f.write('\"'+option+'\": \"string\",')
f.write('};\n')   
    
f.close()    
print "File is ready."





























