'''
Created on 19/09/2014

author: sperez8

Collection of different methods for analyzing data
'''

import os
import sys
import numpy as np

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
OTU_MAP_NAME = os.path.join(_root_dir, 'Otu_maps', 'OTU_MAP_')
TOP_OTUS_NAME = os.path.join(_root_dir, 'Results', 'Top_otus', 'top_otus_')

HEADER = ['Z','Otu #', 'Name', 'Abundance', 'P(w|z)']

def measure_abundance(m):
    '''calculates the proportion of samples an OTU occurs in (ie. its abundance) and returns it
        as a {otu index : abundance}'''
    if not m.datamatrix:
        m.open_data()
    otutable = m.datamatrix
    N = float(m.dimensions()[1])
    otu_abundances = {}
    
    for otu, abundances in enumerate(otutable):
        otu_abundances[otu] = float(np.count_nonzero(abundances))/N
    
    return otu_abundances


def top_otus(m, z, dataFile = None, mapFile = None, n_otus = 5):
    ''' get otu_id: otu_name map and use it to find the top labels per topic in the plsa model.
        Writes the output to a text file or to console if no file found'''
    map = None
    abundances = measure_abundance(m)
    
    if dataFile:
        map = m.open_otu_maps(dataFile)['OTU_MAP']
    elif mapFile:
        f = mapFile
    else:
        try:
            f = open(OTU_MAP_NAME + "name_" + str(m.name) + ".txt", 'r')
            print "Found map:", f 
        except IOError:
            try:
                f = open(OTU_MAP_NAME + "study_" + str(m.study) + ".txt", 'r')
                print "Found map:", f
            except IOError:
                f = ''
                print "No otu id to otu name map found for this study."
    
    if f:
        data = np.loadtxt(f, delimiter = ',', dtype = { 'names':('id','name'), 'formats': ('i16', 'S300') })
        map = {}
        for row in data:
            id, name = row[0], row[1]
            map[id] = name
    
    otu_labels = m.model.topic_labels(map, n_otus, abundances)
    
    if m.name:
        topFile = os.path.join(TOP_OTUS_NAME + "name_" + str(m.name) + ".txt")
    elif m.study:
        topFile = os.path.join(TOP_OTUS_NAME + "name_" + str(m.name) + ".txt")
    
    f = open(topFile, 'w')
    
    f.write('\t'.join(HEADER))
    
    for label in otu_labels:
        for row in label:
            f.write('\n')
            f.write('\t'.join([str(r) for r in row]))
        
    f.close()
    
    #np.savetxt(f, np.asarray(otu_labels), delimiter = ',', fmt="%s")
    
    print "\nSaved top otus {0} per topic in file: {1}".format(n_otus, f)
    
    return None





