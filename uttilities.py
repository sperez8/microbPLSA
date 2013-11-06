'''
Created on 3/11/2013

author: sperez8

contains a bunch of different utilities to read EMP data

'''
import numpy as np
import json
from pprint import pprint




def find_otu_name(id):
    '''returns the OTU name for an OTU id'''
    id = str(id)
    tax_file = '/Users/sperez/Documents/PLSAfun/gg_otus_4feb2011/taxonomies/greengenes_tax.txt'
    tax_table = open(tax_file,'r')
    
    for line in tax_table:
        if id in line[0:len(id)]:
            return line.replace(id, '')

def import_biom_file(f):
    '''reads a .biom file and extracts OTU count data
    using the json library since .biom is a json file.
    See biom-format.org/documentation/versions/biom-1.0.html for more info'''
    json_data=open(f)
    data = json.load(json_data)
    #pprint(data) #use this command to print the whole file
    json_data.close()
    
    shape = data['shape']
    datamatrix = np.zeros((shape[0], shape[1]))
    
    data_type = data['matrix_type']  #can either be 'sparse' or 'dense'

    
    if data_type == 'sparse':
        for otu, sample, count in data['data']:
            datamatrix[otu][sample] = count
    if data_type == 'dense': #NOT TESTED YET
        row = 0
        for otu_counts in data['data']:
            datamatrix[row] = otu_counts        
    
        
    return datamatrix



#Testing find_otu_name()
import time
t0 = time.time()
id = 89440
print find_otu_name(id)
print time.time() - t0

#testing import_biom_file()
f = '/Users/sperez/Documents/PLSAfun/EMPL data/study_1037_closed_reference_otu_table.biom'
print import_biom_file(f)
