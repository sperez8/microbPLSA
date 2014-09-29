'''
Created on 19/09/2014

author: sperez8

Collection of different methods for analyzing data
'''

import os
import sys
import numpy as np
import re

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
OTU_MAP_NAME = os.path.join(_root_dir, 'Otu_maps', 'OTU_MAP_')
TOP_OTUS_NAME = os.path.join(_root_dir, 'Results', 'Top_otus', 'top_otus_')

HEADER = ['Z', 'Otu #', 'Abundance', 'P(w|z)', 'Kingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species', 'Strain', 'Sub-strain']

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

def get_map(mapFile = None, name = None, study = None):
    if mapFile:
        f = mapFile
    else:
        try:
            f = open(OTU_MAP_NAME + "name_" + str(name) + ".txt", 'r')
            print "Found map:", f 
        except IOError:
            try:
                f = open(OTU_MAP_NAME + "study_" + str(study) + ".txt", 'r')
                print "Found map:", f
            except IOError:
                f = ''
                print "\n***No otu id to otu name map found for this study.***\n"
                return None
    
    if f:
        data = np.loadtxt(f, delimiter = ',', dtype = { 'names':('id','name'), 'formats': ('i16', 'S300') })
        map = {}
        for row in data:
            id, name = row[0], row[1]
            map[id] = name
    return map



def top_otus(m, z, dataFile = None, mapFile = None, n_otus = 5):
    ''' get otu_id: otu_name map and use it to find the top labels per topic in the plsa model.
        Writes the output to a text file or to console if no file found'''
    abundances = measure_abundance(m)
    if dataFile:
        map = m.open_otu_maps(dataFile)['OTU_MAP']
    else:
        map = get_map(mapFile = mapFile, name = m.name, study = m.study)
    
    otu_labels = m.model.topic_labels(N=n_otus)
    
    
    
    #save top_otus
    if m.name:
        topFile = os.path.join(TOP_OTUS_NAME + "name_" + str(m.name) + ".txt")
    elif m.study:
        topFile = os.path.join(TOP_OTUS_NAME + "study_" + str(m.study) + ".txt")
    
    f = open(topFile, 'w')
    
    f.write('\t'.join(HEADER))
    
    for z,tops in otu_labels.iteritems():
        for i in tops.keys():
            f.write('\n')
            f.write(str(z+1))
            f.write('\t')
            f.write(str(i))
            f.write('\t')
            f.write(str(round(abundances[i],3)))
            f.write('\t')
            f.write(str(round(m.model.p_w_z[i,z],4)))
            f.write('\t')
            if map:
                f.write('\t'.join(format_otu_name(map[i])))
            
    f.close() 
    
    print "\nSaved top otus {0} per topic in file: {1}".format(n_otus, f)


def format_otu_name(otu):
    newName = ''
    a = otu.split('unclassified')[0]
    b = re.split('[a-z]__',a)
    [b.pop(i) for i,item in enumerate(b) if item =='']
    length = 9
    c = [b[i] if i<len(b) else 'None' for i in range(0,length)]
    #remove unwanted characers
    d = [i.replace('_','') for i in c]
    newName = [re.sub('\([0-9]+\)','',i) for i in d]
    return newName
    
    
    
    
    
    
    
    
    
    
    
    
