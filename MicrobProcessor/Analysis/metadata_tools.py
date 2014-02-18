'''
Created on 18/02/2014

author: sperez8

contains a bunch of different utilities to read and organize metadata
'''

import csv
import json


def get_metadata(csvfile):
    '''returns metadata from csv file as an array'''
    with open(csvfile, 'rU') as file:
        spamreader = csv.reader(file, delimiter=',', quotechar='|')
        header = spamreader.next()
        x = [spamreader.next(),spamreader.next()]
        x = np.array(x)
        for row in spamreader:
            x = np.append(x,[row], axis = 0)
    return header, x

def reorder_metadata(datafile,metadata,study):
    '''gets the order of the sample names in the .biom data file. 
    Reorders the metadata in the table according to that sample order.'''
    
    #FIrst get the sample order
    json_data=open(datafile)
    data = json.load(json_data)
    json_data.close()
    columns = data['columns']
    samples = {}
    i=0
    for item in columns:
        sample_name = item['id']
        if study == '1037':
            s = str(sample_name).split('.')
            s.pop() #remove numerical id with pop()
            sample_name = '.'.join(s) 
        samples[sample_name] = i
        i+=1
    #Now we reconstruct the metadata numpy array by putting the rows in the right order.
    metatable = np.ndarray(shape=metadata.shape, dtype='S40')
    i = 0
    for x in metadata[:,0]:
        j = samples[x]
        metatable[j,:] = metadata[i,:]
        i+=1
    return metatable


def organize_metadata(metadata_column):
    options = {}
    for item in metadata_column:
        if item not in options:
            options[item] = 1
        else: options[item] +=1
    return options

def sort_metadate_types(factors):
    factors_sorted = {}
    return factors_sorted

