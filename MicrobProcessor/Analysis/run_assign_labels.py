'''
Created on 22/01/2014

author: sperez8
'''

from assign_labels import Labelling

study = '1037'
for Z in range(2,14):
     Lab = Labelling(study, Z, debug = True)
     Lab.metadata()
     R = Lab.correlate()
     labels = Lab.assignlabels(R)
     Lab.save_labels(labels) 