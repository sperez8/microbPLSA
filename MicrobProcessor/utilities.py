'''
Created on 3/11/2013

author: sperez8

contains a bunch of different utilities to read EMP data

'''
import numpy as np
import json
#from pprint import pprint
import sys, os
import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


_cur_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, _cur_dir)
import microbplsa

SAMPLE_SIZE = 100
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
        datamatrix = np.zeros((SAMPLE_SIZE+1, shape[1]))
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
            if sampling and row > SAMPLE_SIZE: break #doesn't work/untested
            else: datamatrix[otu][sample] = count
    if data_type == 'dense': #NOT TESTED YET
        row = 0
        for otu_counts in data['data']: 
            datamatrix[row] = otu_counts    
            row += 1   
            if sampling and row > SAMPLE_SIZE: break 
    
        
    return [], datamatrix, []

def import_tab_file(filename, sampling):
    '''imports the date from filename and saves it in numpy array format'''
    file = open(filename,'r')
    table = file.read().splitlines() #read file and split by lines
    samples = table[1].split('\t')  #read column names which are split by tabs
    samples.pop(0)
    otus = []
    datamatrix = np.ndarray((len(table)-2,len(samples)))
    if sampling and len(table)>1000:
        last_line = SAMPLE_SIZE
    else: last_line = len(table)
    for i in range(2,last_line):
        row = table[i].split('\t')
        otus.append(row.pop(0)) 
        datamatrix[i-2] = (row)

    #return datamatrix, otus
    return samples, datamatrix, np.array([int(x) for x in otus])
    
def read_results(file):
    f = open(file, 'r')
    reader = csv.reader(f)
    for row in reader:
        print row
    sys.exit()

def convert_2_R(results_file):
    '''converts the result matrix probabilities into tab delimited files readable by R'''
    dir = os.path.dirname(os.path.realpath(__file__)) + "/Results/"  
    m = microbplsa.MicrobPLSA()
    plsa = m.open_model(dir + results_file) #get model from the results file
    p_z = plsa.p_z
    p_w_z = plsa.p_w_z
    #return document's distribution
    p_z_d = plsa.document_topics()
    
    
    R_file_p_z = open(dir + 'Results_for_R/p_z_' + results_file, 'w')
    for row in p_z:
        R_file_p_z.writelines('\n')
        R_file_p_z.writelines('\t' + str(row))
        R_file_p_z.writelines('\n')
    R_file_p_z.close()   
    
    R_file_p_w_z = open(dir + 'Results_for_R/p_w_z_' + results_file, 'w')
    for row in p_w_z:
        R_file_p_w_z.writelines('\n')
        R_file_p_w_z.writelines('\t' + str(i) for i in row)
        R_file_p_w_z.writelines('\n')
    R_file_p_w_z.close()  
    
    R_file_p_z_d = open(dir + 'Results_for_R/p_z_d_' + results_file, 'w')
    #R_file_p_z_d.writelines('\t topic' + (str(i)) for i in range(1,p_z_d.shape[1]+1))
    for row in p_z_d:
        R_file_p_z_d.writelines('\n')
        R_file_p_z_d.writelines('\t' + str(i) for i in row)
        R_file_p_z_d.writelines('\n')
    R_file_p_z_d.close()      
    
    return None

def make_dictionary(data, k):
    '''from 'rows' dictionary in .biom file, creates a dictionary with two maps:
    OTU_MAP with {index:otu} keys
    and OTU_ID_MAP with {id:otu} keys'''
    otu_map = {}
    otu_id_map = {}
    index = 0
    for item in data:
        otu_id = int(item['id'])
        metadata = item['metadata']
        taxonomy = metadata['taxonomy']
        otu_name = ''
        i=0
        names = 0
        #print 'taxa', taxonomy
        while names < k:
            if 'k__' in taxonomy[-1-i]:
                otu_name = taxonomy[-1-i] +'_'+ otu_name
                break
            level = str(taxonomy[-1-i])
            #print 'level',level
            if level[-1] != '_':
                otu_name = level.replace(' (class)','') +'_'+ otu_name
                names +=1
            i+=1
        #print 'id:', otu_id, otu_name
    
        otu_map[index] = otu_name
        otu_id_map[otu_id] = otu_name
        index +=1

    return {'OTU_MAP': otu_map, 'OTU_ID_MAP':otu_id_map}            

def get_metadata(csvfile):
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
    
    return None



