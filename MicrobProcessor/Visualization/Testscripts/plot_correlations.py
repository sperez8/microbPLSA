'''
Created on 22/01/2014

author: sperez8
'''


import os,sys
_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)
from microbPlotter import *

f = "/Users/sperez/git/microbPLSA/MicrobProcessor/Results/study_"


study = '1037'

f = f + study + '_'
end = '_topics_.txt'

for z in range(4,5):
    topic_correlation(f+str(z)+end)
