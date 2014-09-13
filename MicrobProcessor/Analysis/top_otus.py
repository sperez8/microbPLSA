'''
Created on 27/11/2013

author: sperez8
'''
import sys, os

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

import microbplsa


z = 2
study = None
name = 'bac_final0.03.otutable_GOODSAMPLES'
N = 2

dataFile = os.path.join('C:/Users/Sarah/Desktop/bac_final0.03.otutable_GOODSAMPLES.txt')

m = microbplsa.MicrobPLSA()

m.open_data(study = study, name = name, dataFile = dataFile)

m.open_model(z = z, run = run, useC = True, folder = folder, add_to_file = add)

m.top_otus_labels(z, dataFile,  study = study, name = name, N_otus = N)