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
pcoordfile = _root_dir +'/D3/pcplots/topics.js'

f = '/Users/sperez/git/microbPLSA/MicrobProcessor/Results/study_'+study +'_'+str(z)+'_topics_.txt'
datafile = '/Users/sperez/Documents/PLSAfun/EMPL data/study_'+study+'_split_library_seqs_and_mapping/study_'+study+'_closed_reference_otu_table.biom'

m = microbplsa.MicrobPLSA()
plsa = m.open_model(f) #get model from the results file
p_z_d = plsa.document_topics() #return document's distribution
Z,N =p_z_d.shape #number of samples
        
Lab = Labelling(study, Z, ignore_continuous = False, adjusted_metadata = True) #get labels!
x,y,z = Lab.metadata(non_labels = [])
print y
R = Lab.correlate()
labels_r = Lab.assignlabels(R,num_labels = 1)
print labels_r
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
samplenames = Lab.metadatamatrix[:,0]
samples = []
if study == '1526' or study == '722': 
    samples = [s.split('.')[0] for s in samplenames] #removes numerical id after sample name
else: samples = samplenames
types = Lab.metadatamatrix[:,1] #column with types for color coding later

    
f = open(pcoordfile, 'w')
f.write('var topics = [\n')

for s,distribution in enumerate(p_z_d.T):
    line ='{'
    #line += '  sample: \"'+samples[s]+'\",'
    line += ' site:\"'+ types[s]+'\"'
    for i,p in enumerate(distribution):
        if oldlabels[i] in goodlabels:
            line += ', ' + labels[i] + ':' + str(round(p,3)) 
    line += '},\n'
    f.write(line)
f.write('];\n')

f.write('var dim = [\n\'')
f.write('type\',\'')
f.write('\',\''.join(labels))
f.write('\'];\n')

f.write('var types = {\n')
f.write('\"samples\": \"string\",')
f.write('\"site\": \"string\",')

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





























