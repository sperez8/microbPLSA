'''
Created on 09/04/2014

author: sperez8

Shows how to use NetworkAnalysis class
'''

from network import NetworkAnalysis

study = 1526

network = NetworkAnalysis(study = study)
network.remove_rare_otus()