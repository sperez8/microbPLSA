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
#study = '1526'
filename  = '/Users/Sarah/Desktop/test_otutable.txt'
name = 'testing'


#file = '/Users/sperez/Desktop/LSTP/LTSP-6site_tags/Bacterial/bac_final.an.0.03.biom'
useC = True
name = 'un_beau_test'
z_i = 2
z_f = 8
z_inc = 2
numRuns = 4

  
m = microbplsa.MicrobPLSA()
m.open_data(filename = filename, name = name, sampling = False)
m.generate_runs(z_i = z_i, z_f = z_f, z_inc = z_inc, numRuns = numRuns, useC = useC)
