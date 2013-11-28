'''
Created on 20/11/2013

author: sperez8
'''
import os,sys
_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)
from microbPlotter import *

f = "/Users/sperez/git/microbPLSA/MicrobProcessor/Results/results_"


end = '_topics_26Nov.txt'
for z in range(2,7):
    topic_distribution(f+str(z)+end)
    
end = '_topics_27Nov.txt'
for z in range(7,13):
    topic_distribution(f+str(z)+end)