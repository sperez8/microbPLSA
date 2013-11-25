'''
Created on 20/11/2013

author: sperez8
'''
import os,sys
_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)
from microbPlotter import *

#f = "/Users/sperez/git/microbPLSA/MicrobProcessor/Results/results_3topics_20Nov17:48.txt"
f= "/Users/Sarah/git/microbPLSA/Visualization/Testscripts/test_results.txt"
topic_distribution(f)