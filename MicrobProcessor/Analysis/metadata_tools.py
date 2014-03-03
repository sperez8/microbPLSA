'''
Created on 18/02/2014

author: sperez8

contains a bunch of different utilities to read and organize metadata
'''

import csv
import json
import numpy as np
import string
from collections import Counter


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
    
    #First get the sample order
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


def organize_metadata(metatable, factors, non_labels):
    '''organizes the metadata by type in a dictionary of the form:
        {factor_type: {factor: values}} where factor_type is 
        dichotomous, continuous, categorical. All 'constant' or
        invariable factors are ignored'''
    N = metatable.shape[0] #number of samples
    factor_types = {"dichotomous":[], "continuous":[], "categorical":[]}
    #F is the number of dichotomous and continuous factors + 
    #the number of categories for the categorical factors
    F = 0
    #we save the names of the factors we will actually test
    #including all the categorical labels
    real_factors =[] 
    #we first create a dictionary of {factor: possible types}
    for index, factor in enumerate(factors):
        if factor not in non_labels:
            column = metatable[:,index]
            options = []
            ftype = None
            all_cont_values = True
            for value in column:
                if is_numerical(value):
                    ftype = 'continuous'
                else:
                    all_cont_values = False
                if value not in options:
                        options.append(value)
                        
            
            if not all_cont_values:
                if len(options) == N or len(options) == 1:
                    continue #these are invariable factors and we ignore them               
                elif len(options)==2:
                    ftype = 'dichotomous'
                    F += 1
                    real_factors.append(options[0])
                elif len(options) > 2:
                    ftype = 'categorical'
                    F += len(options)
                    options = [factor + ' (' + opt + ')' for opt in options]
                    real_factors.extend(options)
            if ftype == 'continuous': 
                #check if all the value are the same, if
                constant_value = (np.unique(options).shape == (1,))
                if not constant_value:
                    real_factors.append(factor)
                    F += 1
                    factor_types[ftype].append(factor)
                else:
                    continue
            else:
                factor_types[ftype].append({factor:options})

    return factor_types, real_factors

def sort_metadate_types(factors):
    factors_sorted = {}
    return factors_sorted

def is_numerical(value):
    '''return True if a metadata value is numerical.
        if it's 'none' then we can't tell
        if it has punctuation such as '-' or '/' 
        then it might be a range or a date'''
    
    #if str.lower(value) == 'none': #chekc for 'none', 'None', 'NONE', etc...
    #    return True
    if any((char in string.letters) for char in value):
        return False
    else:
        for p in string.punctuation:
            if p in value:
                if p =='.': #probably have a float
                    pass
                elif p == '/': pass #value = value.split(p)[-1] #probably a date...
                elif p == '-': value = value.split(p)[-1]
                else: print "I don't know how to deal with this punctuation: ", p
        try:
            v = float(value)
            return v
        except ValueError:
            return None
    
    
    
    
    
    
    