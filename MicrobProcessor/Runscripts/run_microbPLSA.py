'''
Created on 16/09/2013

author: sperez8
'''

import sys, os

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

import microbplsa

#use file below to test this script
study = '1526'
filename = None
#filename = '/Users/sperez/Desktop/LSTP/LTSP-6site_tags/Bacterial/bac_final0.03.otutable_GOODSAMPLES.txt'
useC = True
z_i = 8
z_f = 10
z_inc = 1
numRuns = 1
  
m = microbplsa.MicrobPLSA()
m.open_data(filename = filename, study = study)
m.generate_runs(z_i = z_i, z_f = z_f, z_inc = z_inc, numRuns = numRuns, useC = useC)