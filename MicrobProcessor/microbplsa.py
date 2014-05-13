'''
Created on 16/09/2013

author: sperez8
'''
import numpy as np
import csv
from time import time, localtime, strftime
from utilities import *
import sys, os
import pickle

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir + os.sep + "PLSA")
from plsa import pLSA
from plsa import loglikelihood

OTU_MAP_NAME = 'JsonData/' + 'OTU_MAP_'
RESULTS_LOCATION = '/Results/'
MAX_ITER_PLSA = 10000
LEVELS = 10 #default number of levels to add to name of OTU in OTU_MAP
K_DEFAULT = 1 #default number of samples to leave out when cross validating


class MicrobPLSA():
    '''A class to handle metagenomic data in particular from the Earth Microbiome Project
    and apply statistical tools such as Probabilistic Latent Semantic Analysis.
    This class is actually a wrapper on Mathieu Blondel's PLSA package'''

    def __init__(self):
        return None
        
    def open_model(self, study = None, z = 0, file = None):
        ''' Opens the probs of a model previously computed and saved in a json file '''
        if file:
            f = open(file,'r')
        elif study and z:
            file = _cur_dir + RESULTS_LOCATION + 'study_'+study +'_'+str(z)+'_topics_.txt'
            f = open(file,'r')
        else: print "Need study and topic input for this function."
        data = json.load(f)
        p_z = np.array(data['p_z'])
        p_w_z = np.array(data['p_w_z'])
        p_d_z = np.array(data['p_d_z'])
        model = p_z, p_w_z, p_d_z
        plsa = pLSA()
        plsa.set_model(model)
        self.study = study
        self.z = z
        self.model = plsa
        return plsa
    
    def open_otu_maps(self,biom_data):
        '''Opens a file in the .biom format and opens or creates an {id:otu} dictionary 
        if not already created'''
 
        reference = OTU_MAP_NAME + biom_data.split('/')[-1] +'.txt'
        reference = os.path.join(_cur_dir,reference)
        try:
            with open(reference) as ref: #read the json file if it exists
                pickled_map=open(reference)
                otu_maps = pickle.load(pickled_map)
                pickled_map.close()
        except IOError: #create the json file if it doesn't exist yet
            json_data=open(biom_data)
            data = json.load(json_data)
            json_data.close()
            otu_maps = make_dictionary(data['rows'],LEVELS) #translate the json row data into a {otu_id: otu_name} dictionary
            ref = open(os.path.join(_cur_dir,reference), 'w')
            pickle.dump(otu_maps,ref)
            ref.close()
            
        self.otu_map = otu_maps
        return otu_maps

    def open_data(self, study = None, file = None,sampling = False):
        self.study = study
        
        if file:
            f = open(file,'r')
        elif study:
            study = str(study)
            file = '/Users/sperez/Documents/PLSAfun/EMPL data/study_'+study+'_split_library_seqs_and_mapping/study_'+study+'_closed_reference_otu_table.biom'
            f = open(file,'r')
        else: print "Need study and topic input for this function."      
        self.datamatrix= extract_data(file, sampling)
        return file
    
    def dimensions(self):
        return self.datamatrix.shape

    def runplsa(self, topic_number, maxiter=MAX_ITER_PLSA, verbatim = True):
        '''runs plsa on sample data in filename'''
        datamatrix = self.datamatrix
        Z = topic_number #number of topics

        plsa = pLSA()
        plsa.debug = verbatim
        print "\n Running PLSA...\n"
        plsa.train(datamatrix, Z, maxiter)   #runs plsa!
        self.model = plsa
        return plsa        

    def save_data(self, normalize = False):
        ''' functions saves original abundance data to a csv or txt file'''
        filename = _cur_dir + '/Results/data_study_'+self.study+'.txt'
        f = open(filename,'w')
        data = self.datamatrix
        if normalize:
            data = self.normalizeArray(data)
        d = [list(row) for row in data]
        json.dump(d,f)
        f.write('\n')
        f.close()
        return None
        
    def saveresults(self, filename = 'Results/results', extension = '.txt'):
        ''' functions saves plsa probabilities into a csv or txt file'''
        filename = self.formatfile(filename, extension)
        f = open(filename,'w')
        p_z,p_w_z,p_d_z = self.model.get_model()
        
        if extension == '.csv':
            writer = csv.writer(f)
            writer.writerow(['p_z', p_z.shape])
            writer.writerow(p_z)
            writer.writerow(['p_d_z', p_d_z.shape])
            for value in p_d_z:
                writer.writerow(value)    
            writer.writerow(['p_w_z', p_w_z.shape])
            for value in p_w_z:
                writer.writerow(value)
        elif extension == '.txt':
            data = {}
            data['p_z'] = list(p_z)
            data['p_w_z'] = [list(row) for row in p_w_z] #convert the numpy array in a list of lists  
            data['p_d_z'] = [list(row) for row in p_d_z]
            json.dump(data,f)
        else: print "Error: the extension given is not valid"     
        f.close()
        return None
    
    def svd(self, columns, datamatrix, otus):
        '''performs svd on data. NEEDS TESTING'''
        print '\nData in matrix form:\n', datamatrix
        print '\nOtus:',otus
        print columns
        
        print 'The matrix dimensions are', datamatrix.shape
        
        t0 = time.time() 
        U, s, V = np.linalg.svd(datamatrix, full_matrices=True)
        print '\nSVD took ', time.time(), 'seconds'
        print 's', s
        print 'U is', U.shape, 'V is ', V.shape
        
        #Let's reduce the dimensionality/rank by 50%
        k = int(datamatrix.shape[1]/2)
        print 'k=', k
        for i in range(k,s.shape[0]):
            s[i]=0
        print s
        
        #NON FUNCTIONAL
        #new_data = np.dot(np.dot(U, np.diag(s)), np.conjugate(V))
        #print new_data
        
    def loglikelihood(self):
        """
        Compute the log-likelihood that the model generated the data.
        """
        p_z, p_w_z, p_d_z = self.model.get_model()
        L = loglikelihood(self.datamatrix, p_z, p_w_z, p_d_z)
        return L 

    def top_otus_labels(self, study, z, N_otus = 5):
        biom_data =self.open_data(study = study)
        map = self.open_otu_maps(biom_data)['OTU_MAP']
        self.open_model(study = study, z = z)
        
        otu_labels = self.model.topic_labels(map, N_otus)
        for label in otu_labels:
            print label
        
        return None

    def significant_otus(self, cutoff = 0.8):
        self.open_model(study = self.study, z = self.z)
        
        p_z_w = self.model.word_topics()
        
        table = []
        for z,w in enumerate(p_z_w):
            ind_otus = np.array(np.where(w>cutoff))
            for otu in ind_otus[0]:
                table.append([otu, p_z_w[z,otu], z+1])
        return np.array(table) # usecols = (0,1,2), dtype = {'name':('otus','score','topics'), 'format':('f4','f8','f4')})


    def cross_validate(self, k=K_DEFAULT):
        score = 0
        
        
        return score

    @staticmethod
    def formatfile(filename, extension):
        '''formats name of file to get correct file format and avoid conflicts'''
        if 'results' in filename:
            timestamp = strftime("%d%b", localtime()) #add date to filename to avoid conflicts
            filename = filename + timestamp
        if filename[-4:] != extension:
            filename = filename + extension
        if 'Results/' not in filename:
            _cur_dir = os.path.dirname(os.path.realpath(__file__))
            filename = _cur_dir +'/Results/'+filename
        return filename

    @staticmethod
    def normalizeArray(data_array):
        '''normalizes a numpy array along the columns'''
        data = data_array.astype(float)
        totals = np.sum(data, axis=0).astype(float)
        norm_data = data/totals
        return norm_data 
    



