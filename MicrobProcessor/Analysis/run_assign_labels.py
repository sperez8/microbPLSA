'''
Created on 22/01/2014

author: sperez8

Shows how to use Labelling class
'''

from labelling import Labelling

study = '1526'
simple = False
for Z in range(2,39):
    Lab = Labelling(study, Z, debug = False,ignore_continuous = False, adjusted_metadata = True)
    if simple:
         labels = Lab.getlabels()
    else:
        Lab.metadata(non_labels = ['BarcodeSequence'])
        m = list(Lab.metadatamatrix[:,7])
        transf = {'DRY':1, "SAFE":2, "DIPPING":3, "UNDER_ISH":4}
        M = [transf[n] for n in m]
        print M
        if 5 in M: print "DDJDJD        "
        import sys
        sys.exit()
        sys.exit()
        R = Lab.correlate()
        labels = Lab.assignlabels(R,num_labels = 8)
        
    Lab.save_labels(labels) 