'''
Created on 22/01/2014

author: sperez8

Shows how to use Labelling class
'''

from labelling import Labelling

study = '722'
simple = False
for Z in range(2,23):
    Lab = Labelling(study, Z, debug = False,ignore_continuous = False)
    if simple:
         labels = Lab.getlabels()
    else:
        Lab.metadata()
        R = Lab.correlate()
        labels = Lab.assignlabels(R,num_labels = 3)
        
    Lab.save_labels(labels) 