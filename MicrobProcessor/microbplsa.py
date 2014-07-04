'''
Created on 16/09/2013

author: sperez8
'''
import numpy as np
import csv
from time import time, localtime, strftime
import datetime
from utilities import *
import sys, os
import pickle
from math import sqrt

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir + os.sep + "PLSA")
from plsa import pLSA
from plsa import loglikelihood

OTU_MAP_NAME = 'JsonData/' + 'OTU_MAP_'
RESULTS_LOCATION = '/Results/'
MAX_ITER_PLSA = 10000
LEVELS = 10 #default number of levels to add to name of OTU in OTU_MAP


class MicrobPLSA():
    '''A class to handle metagenomic data in particular from the Earth Microbiome Project
    and apply statistical tools such as Probabilistic Latent Semantic Analysis.
    This class is actually a wrapper on Mathieu Blondel's PLSA package'''

    def __init__(self):
        return None
        
    def open_model(self, study = None, z = 0, filename = None):
        ''' Opens the probs of a model previously computed and saved in a json file '''
        if filename:
            f = open(filename,'r')
        elif study and z:
            filename = _cur_dir + RESULTS_LOCATION + 'study_'+study +'_'+str(z)+'_topics_.txt'
            f = open(filename,'r')
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

    def open_data(self, study = None, filename = None, name = None, sampling = False):
        self.study = study
        self.name = name
        if not self.name:
            self.name = filename.split('/')[-1][:-4]
                
        if filename:
            pass
        elif study:
            study = str(study)
            filename = '/Users/sperez/Documents/PLSA data/EMPL data/study_'+study+'_split_library_seqs_and_mapping/study_'+study+'_closed_reference_otu_table.biom'
        else: 
            print "Need study number or filename to access the data."
        f = open(filename,'r')
        self.datamatrix= extract_data(filename, sampling)
        return filename
    
    def dimensions(self):
        return self.datamatrix.shape

    def generate_runs(self, z_i = 1, z_f = None, z_inc = 1, numRuns = 1, useC = True):
        '''runs plsa mutliple time for a range of topics'''
        print '\n\n\nStudy', self.study, 'has', self.dimensions()[0], 'otus and', self.dimensions()[1], 'samples.'
        if z_f is None:
            z_f = int(3*sqrt(self.dimensions()[1]))
        print 'We will run PLSA with Z = {0} to {1}.\n\n'.format(z_i, z_f)

        for z in range(z_i, z_f, z_inc): 
            run = 1
            while True:
                filename = self.get_result_filename(z, run, useC)

                try:
                    open(filename, "r")
                    print "The results file already exists for study {0}, {1} topics and run #{2}".format(self.study, z, run)
                    run += 1
                    continue #if result files already exists, we don't override
                except IOError:
                    #found a file not yet written so we run PLSA with those parameters.
                    break
            if run > numRuns: 
                continue   #only want to compute plsa for each z a certain max number of times

            today = datetime.datetime.today()
            print '\n', today.strftime('%b %d, %Y @ %I:%M%p')
            print 'ZZZZZZZzzzz is ',z 
        
            t0 = time()
            model = self.run_plsa(z, verbatim = True)
            print 'Saving plsa to file {0}.'.format(filename)

            self.save_results(filename = filename, extension =  '.txt')
            print 'Time for analysis:', round(time()-t0,1)
            
        return None

    def run_plsa(self, Z, maxiter=MAX_ITER_PLSA, verbatim = True, useC = True):
        '''runs plsa on sample data in filename'''

        plsa = pLSA()
        plsa.debug = verbatim
        print "\n Running PLSA...\n"
        plsa.train(self.datamatrix, Z, maxiter = maxiter, useC = useC)   #runs plsa!
        self.model = plsa
        return plsa        

    def save_data(self, normalize = False):
        ''' functions saves original abundance data to a csv or txt file'''
        filename = _cur_dir + '/Results/data_study_'+self.study+'.txt'
        f = open(filename,'w')
        data = self.datamatrix
        if normalize:
            data = self.normalize_array(data)
        d = [list(row) for row in data]
        json.dump(d,f)
        f.write('\n')
        f.close()
        return None
        
    def save_results(self, filename = 'Results/results', extension = '.txt'):
        ''' functions saves plsa probabilities into a csv or txt file'''
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

    def measure_abundance(self):
        '''calculates the proportion of samples an OTU occurs in (ie. its abundance) and returns it
            as a {otu index : abundance}'''
        otutable = self.datamatrix
        otu_abundances = {}
        for otu, abundances in enumerate(otutable):
            otu_abundances[otu] = round(float(np.count_nonzero(abundances))/float(otutable.shape[1]),2)
        return otu_abundances

    def get_result_filename(self, z, run, useC):
        if useC:
            add = 'with_C_'
        else: add = ''
        
        if self.study:
            resultsfilename = 'study_' + self.study + '_' + str(z) + '_topics_' + add
        else:
            resultsfilename = 'study_' + self.name + '_' + str(z) + '_topics_' + add
        ext = '.txt'
        
        finalName = resultsfilename + 'run' +str(run) + ext
        filename = os.path.join(_root_dir, 'MicrobProcessor', 'Results', finalName)
        return filename

    @staticmethod
    def normalize_array(data_array):
        '''normalizes a numpy array along the columns'''
        data = data_array.astype(float)
        totals = np.sum(data, axis=0).astype(float)
        norm_data = data/totals
        return norm_data


