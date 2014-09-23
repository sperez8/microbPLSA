'''
Created on 3/11/2013

author: sperez8

contains a bunch of different utilities to read EMP data

'''
import numpy as np
import json
import sys, os
import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


_cur_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, _cur_dir)
import microbplsa

SAMPLE_SIZE = 100
classes = {'kingdom':'k', 'phylum':'p', 'class':'c', 'order':'o', 'family':'f', 'genus':'g', 'species':'s'}


def extract_data(dataFile,sampling):
    if dataFile[-6:]=='.array':
        return load_array_data(dataFile, sampling)
    elif dataFile[-4:]=='.txt':
        return import_tab_file(dataFile, sampling)
    elif dataFile[-5:]=='.biom':
        return import_biom_file(dataFile, sampling)
    else: 
        try:
            open(dataFile+'.txt.array')
            return load_array_data(dataFile + '.txt.array', sampling)
        except IOError:
            try:
                open(dataFile+'.biom.array')
                return load_array_data(dataFile + '.biom.array', sampling)
            except IOError:
                try:
                    open(dataFile+'.biom')
                    return import_biom_file(dataFile+'.biom', sampling)
                except IOError:
                    try:
                        open(dataFile+'.txt')
                        return import_tab_file(dataFile+'.txt', sampling)
                    except IOError:
                        pass
    print "The file {0} with extension '.array', '.txt' or '.biom' doesn't exist. Please check the study number and name were attributed correctly.".format(dataFile)
    sys.exit()
            
def import_biom_file(f,sampling):
    '''reads a .biom file and extracts OTU count data
    using the json library since .biom is a json file.
    See biom-format.org/documentation/versions/biom-1.0.html for more info'''
    json_data=open(f)
    data = json.load(json_data)
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
    
        
    return datamatrix

def import_tab_file(dataFile, sampling):
    '''imports the date from f and saves it in numpy array format'''
    print 'Loading'
    datamatrix = np.loadtxt(dataFile, delimiter = '\t', dtype = int, skiprows = 1) #skip header of document
    
    if sampling:
        return datamatrix[:,:SAMPLE_SIZE]
    else:
        return datamatrix
    

def pickle_data_matrix(dataFile):
    datamatrix = extract_data(dataFile,None)
    datamatrix.dump(dataFile + '.array')
    return None

def load_array_data(dataFile, sampling):
    datamatrix = np.load(dataFile + '.array', 'r')

    if sampling:
        return datamatrix[:,:SAMPLE_SIZE]
    else:
        return datamatrix

def read_results(dataFile):
    f = open(dataFile, 'r')
    reader = csv.reader(f)
    for row in reader:
        print row
    return None

def convert_2_R(results_file):
    '''converts the result matrix probabilities into tab delimited files readable by R'''
    dir = os.path.dirname(os.path.realpath(__file__)) + "/Results/"  
    m = microbplsa.MicrobPLSA()
    plsa = m.open_model(modelFile = os.path.oin(dir, results_file)) #get model from the results file
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

def get_otu_ranks(otu_map, level = "phylum"):         
    ranks_otus = []
    cut = classes[level]
    for otu in otu_map['OTU_MAP'].values():
        try:
            piece = otu.split(cut+"__")[1]
        except IndexError: #that otu doesn't go down to that rank level so we skip it.
            continue
        rank = piece.split('_')[0]
        ranks_otus.append(str(rank))
    ranks = set(ranks_otus)
    return ranks

def normalize_array(data_array):
    '''normalizes a numpy array along the columns'''
    data = data_array.astype(float)
    totals = np.sum(data, axis=0).astype(float)
    norm_data = data/totals
    return norm_data

def zipper(*args):
    '''a revamped version of zip() method that checks that lists
    to be zipped are the same length'''
    for i,item in enumerate(args):
        if len(item) != len(args[0]):
            raise ValueError('The lists to be zipped aren\'t the same length.')
    
    return zip(*args)