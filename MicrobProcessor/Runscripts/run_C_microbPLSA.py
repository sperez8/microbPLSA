'''
Created on 16/09/2013

author: sperez8
'''

import sys, os
from time import time
from math import sqrt
import numpy as np

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

import microbplsa

_root_dir = os.path.dirname(_root_dir)
sys.path.insert(0, _root_dir+'/PLSA/')

import _plsa as plsa # the C module

study = '1526'
z = 2


  
m = microbplsa.MicrobPLSA()
m.open_data(study = study, sampling = False)
(w,d) = m.dimensions()
print '\n\n\nStudy', study, 'has', w, 'otus and', d, 'samples.'

matrix = m.datamatrix

print matrix

ext = '.txt'
resultsfilename = 'C_test_study_' + study + '_' + str(z) + '_topics_'


t0 = time()

model = m.runplsa(z, verbatim = True, use_C = False)   ##change to use C code
m.saveresults(filename = resultsfilename, extension =  '.txt')
print 'Topic Labels', model.topic_labels(None)
print 'Time for analysis:', int(time()-t0)
    
