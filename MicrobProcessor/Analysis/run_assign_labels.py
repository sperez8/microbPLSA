'''
Created on 22/01/2014

author: sperez8

Shows how to use Labelling class
'''

from labelling import Labelling

study = '1037'
simple = True
for Z in range(2,14):
    Lab = Labelling(study, Z, debug = True)
    if simple:
         labels = Lab.getlabels()
    else:
        Lab.metadata()
        R = Lab.correlate()
        labels = Lab.assignlabels(R)
        
    Lab.save_labels(labels) 