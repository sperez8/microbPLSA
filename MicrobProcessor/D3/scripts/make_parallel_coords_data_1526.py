'''
Created on 14/03/2013

author: sperez8
'''

import sys, os
import numpy

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
_root_dir = os.path.dirname(_root_dir)
sys.path.insert(0, _root_dir)
import microbplsa
analysis_dir = _root_dir+ '/Analysis'
sys.path.insert(0, analysis_dir)
from labelling import Labelling
from string import replace

study = '1526'
z = 8
CORRELATION_THRESHOLD = 0.0
MANUAL_LABELS = ['Topic 1', 'Topic 2', 'Year Last submerged', 'Under water', 'Topic 5', 'Topic 6', 'Submerged between 2002-1999', 'Moki Camp']
pcoordfile = _root_dir +'/D3/pcplots/topics.js'

f = '/Users/sperez/git/microbPLSA/MicrobProcessor/Results/Models/study_'+study +'_'+str(z)+'_topics_.txt'
datafile = '/Users/sperez/Documents/PLSAfun/EMPL data/study_'+study+'_split_library_seqs_and_mapping/study_'+study+'_closed_reference_otu_table.biom'

m = microbplsa.MicrobPLSA()
m.open_model(modelFile = f, study = '1526') #get model from the results file
plsa = m.model
p_z_d = plsa.document_topics() #return document's distribution
Z,N =p_z_d.shape #number of samples

Lab = Labelling(m, Z, ignore_continuous = False, adjusted_metadata = True) #get labels!
Lab.metadata(non_labels = [])
samplenames = Lab.metadatamatrix[:,0]
samples = [s.split('.')[0] for s in samplenames] #removes numerical id after sample name
types = Lab.metadatamatrix[:,1] #column with types for color coding later

year = Lab.metadatamatrix[:,6]
if len(MANUAL_LABELS) == Z:
    labels = ['\"'+l+'\"' for l in MANUAL_LABELS]
else: 
    labels = ['\"Topic '+str(i)+'\"' for i in range(0,Z)]
    
f = open(pcoordfile, 'w')
f.write('var topics = [\n')

for s,distribution in enumerate(p_z_d.T):
    line ='{'
    #line += '  sample: \"'+samples[s]+'\",'
    line += ' site:\"'+ types[s]+'\"'
    line += ', \"Year last submerged\":\"'+ year[s]+'\"'
    for i,p in enumerate(distribution):
        line += ', ' + labels[i] + ':' + str(round(p,3)) 
    line += '},\n'
    f.write(line)
f.write('];\n')

f.write('var dim = [\n\'')
f.write('site\',\'')
f.write('\"Year last submerged\"\',\'')
f.write('\',\''.join(labels))
f.write('\'];\n')

f.write('var types = {\n')
f.write('\'samples\': \'string\',')
f.write('\'site\': \'string\',')
f.write('\"Year last submerged\" : \'string\',')

for label in labels:
    f.write( label + ': \'number\',')
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





























