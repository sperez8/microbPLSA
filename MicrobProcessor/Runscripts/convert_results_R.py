'''
Created on 06/01/2014

author: sperez8
'''

import sys, os
import fnmatch

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

from utilities import *

for study in ['1526']:    
    directory = _root_dir + '/Results/'
    for file in os.listdir(directory):
        if fnmatch.fnmatch(file, 'study_'+study+'*'):
            print file
            convert_2_R(file)