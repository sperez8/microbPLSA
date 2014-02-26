'''
Created on 22/01/2014

author: sperez8

Shows how to use Labelling class
'''

from labelling import Labelling

study = '864'
simple = True
for Z in range(2,14):
    Lab = Labelling(study, Z, debug = True,ignore_continuous = False)
    if simple:
         labels = Lab.getlabels()
    else:
        Lab.metadata()
        R = Lab.correlate(ignore_continuous = False)
        labels = Lab.assignlabels(R)
        
    Lab.save_labels(labels) 