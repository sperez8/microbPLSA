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

FOLDER = 'Models'




name = 'bac_final0.03.otutable_GOODSAMPLES'
z = 20
run = 1
pcoordfile = os.path.join(_root_dir, 'D3', 'pcplots', 'paracoords_LTSP_topics'+'.js')

   

m = microbplsa.MicrobPLSA(name = name)
m.open_model(z = z, run = run, useC = True, folder = FOLDER) #get model from the results file
plsa = m.model
p_z_d = plsa.document_topics() #return document's distribution
Z,N =p_z_d.shape #number of samples

print Z,N

samples = ['Sample'+str(i) for i in range(1,N+1)]
labels = ['Topic '+str(i) for i in range(1,Z+1)]

f = open(pcoordfile, 'w')
f.write('var topics = [\n')

for s,distribution in enumerate(p_z_d.T):
    line ='{'
    for i,p in enumerate(distribution):
        line += '"' + labels[i] + '":' + str(round(p,3)) + ',' 
    line = line[:-1]
    line += '},\n'
    f.write(line)
f.write('];\n')

f.write('var dim = [\n\'"')
f.write('"\',\'"'.join(labels))
f.write('"\'];\n')

f.write('var types = {\n')
f.write('\"samples\": \"string\",')

for label in labels:
    f.write('\"'+label+'\": \"number\",')
f.write('};\n')   
    
f.close()    
print "File is ready."





























