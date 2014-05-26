'''
Created on 1/05/2014

author: sperez8
Shows how to save the abundance data from a biom file to  json file
'''
import sys, os

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

import microbplsa
m = microbplsa.MicrobPLSA()

study = '1526'
m.open_data(study = study)
m.save_data(normalize = True)

