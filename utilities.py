'''
Created on 3/11/2013

author: sperez8

contains a bunch of different utilities to read EMP data

'''
import numpy as np
import json
from pprint import pprint
import sys
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


def find_otu_name(id):
    '''returns the OTU name for an OTU id'''
    id = str(id)
    tax_file = '/Users/sperez/Documents/PLSAfun/gg_otus_4feb2011/taxonomies/greengenes_tax.txt'
    tax_table = open(tax_file,'r')
    
    for line in tax_table:
        if id in line[0:len(id)]:
            return line.replace(id, '')

def extract_data(file,sampling):
    if file[-4:]=='.txt':
        return import_tab_file(file, sampling)
    elif file[-5:]=='.biom':
        return import_biom_file(file, sampling)
    else: 
        print "File name:", file
        print "Incorrect file extension."
        sys.exit()
            
def import_biom_file(f,sampling):
    '''reads a .biom file and extracts OTU count data
    using the json library since .biom is a json file.
    See biom-format.org/documentation/versions/biom-1.0.html for more info'''
    json_data=open(f)
    data = json.load(json_data)
    #pprint(data) #use this command to print the whole file
    json_data.close()
    
    shape = data['shape']
    if sampling:
        datamatrix = np.zeros((501, shape[1]))
    else: 
        datamatrix = np.zeros((shape[0], shape[1]))
                 
    data_type = data['matrix_type']  #can either be 'sparse' or 'dense'

    
    if data_type == 'sparse':
        row_otu = 0
        row = 0
        for otu, sample, count in data['data']:
            if otu != row_otu:
                row_otu = otu
                row += 1
            if sampling and row > 500: break #doesn't work/untested
            else: datamatrix[otu][sample] = count
    if data_type == 'dense': #NOT TESTED YET
        row = 0
        for otu_counts in data['data']:
            datamatrix[row] = otu_counts    
            row += 1   
            if sampling and row > 500: break 
    
        
    return [], datamatrix, []

def import_tab_file(filename, sampling):
    '''imports the date from filename and saves it in numpy array format'''
    file = open(filename,'r')
    table = file.read().splitlines() #read file and split by lines
    columns = table[1].split('\t')  #read column names which are split by tabs
    columns.pop(0)
    otus = []
    datamatrix = np.ndarray((len(table)-2,len(columns)))
    if sampling and len(table)>1000:
        last_line = 500
    else: last_line = len(table)
    for i in range(2,last_line):
        row = table[i].split('\t')
        otus.append(row.pop(0)) 
        datamatrix[i-2] = (row)

    #return datamatrix, otus
    return columns, datamatrix, np.array([int(x) for x in otus])


def data_count(file):
    columns, datamatrix, otus = extract_data(file, False)
    #matrix with boolean values representing if OTU occurs or not
    binary_data = datamatrix > np.zeros(datamatrix.shape)
    
    #Measure the number of OTUs in each sample
    otu_count = np.sum(binary_data, axis = 0)
    #Measure the number of samples in which an OTU occurs
    otu_presence = np.sum(binary_data, axis = 1)
    #Measure number of reads per sample
    tags = np.sum(datamatrix, axis = 0)
    
    plt.subplot(1,3,1)
    bins = np.sort(tags)
    n = np.arange(bins.shape[0])
    plt.bar(n,bins,width = 0.8, color = 'green')
    plt.xlabel('Sample #')
    plt.ylabel('Tag or read count')
    plt.title('Sorted read count per sample.')
    
    
    #Make plot for sample diversity
    plt.subplot(1,3,2)
    bins = np.sort(otu_count)
    n = np.arange(bins.shape[0])
    plt.bar(n,bins,width = 0.8, color = 'blue')
    plt.xlabel('Sample #')
    plt.ylabel('OTU diversity count')
    plt.title('Sorted read count per sample.')
    
    #Make plot for OTU's presence in samples
    plt.subplot(1,3,3)
    plt.hist(otu_presence, bins=datamatrix.shape[1], normed=1, facecolor='purple')
    plt.xlabel('Number of samples')
    plt.ylabel('Proportion of OTUs')
    plt.title('Counts of OTUs in different number of samples')
    plt.show()
    return None

f = '/Users/sperez/Documents/PLSAfun/EMPL data/study_1037_closed_reference_otu_table.biom'
data_count(f)

#Testing find_otu_name()
# import time
# t0 = time.time()
# id = 89440
# print find_otu_name(id)
# print time.time() - t0