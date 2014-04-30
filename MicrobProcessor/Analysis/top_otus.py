'''
Created on 27/11/2013

author: sperez8
'''
import sys, os

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

import microbplsa


z = 8
study = '1526'
N = 5

m = microbplsa.MicrobPLSA()
m.top_otus(study,  z, N_otus = N)