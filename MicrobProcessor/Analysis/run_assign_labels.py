'''
Created on 22/01/2014

author: sperez8
'''

from assign_labels import labeling, save_labels

study = '1037'
for Z in range(2,14):
     topiclabels  = labeling(study, Z)
     save_labels(topiclabels, labelfile) 