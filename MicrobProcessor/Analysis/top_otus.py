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
study = '1526'
name = 'C_test_study_1526_2_topics_'
N = 5

m = microbplsa.MicrobPLSA()

m.top_otus_labels(z, study = study, name = name, N_otus = N)