'''
Created on 22/01/2014

author: sperez8
'''

import os,sys
from assign_labels import labeling

study = '1037'
for Z in range(2,14):
     labeling(study, Z)