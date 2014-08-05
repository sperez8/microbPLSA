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

OTU_MAP_NAME = os.path.join('JsonData', 'OTU_MAP_')
RESULTS_LOCATION = 'Results'
CROSS_VAL_LOCATION = os.path.join('Results','CrossValidation')
MAX_ITER_PLSA = 100000
LEVELS = 10 #default number of levels to add to name of OTU in OTU_MAP


class MicrobPLSA():
    '''A class to handle metagenomic data in particular from the Earth Microbiome Project
    and apply statistical tools such as Probabilistic Latent Semantic Analysis.
    This class is actually a wrapper on Mathieu Blondel's PLSA package'''

    def __init__(self):
        self.study = None
        self.name = None
        self.run = ''
        self.useC = None
        self.model = None
        self.modelFile = None
        return None
        
    def open_model(self, study = None, z = 0, name = None, modelFile = None, run = '', useC = False):
        ''' Opens the probs of a model previously computed and saved in a json file '''
        if self.study is None:
            self.study = study
        if self.name is None:
            self.name = name
        if self.run == '':
            self.run = run
        if self.useC is None:
            self.useC = useC
            
        
        if modelFile is not None:
            self.modelFile = modelFile
        else:
            self.modelFile = self.get_result_filename(z, self.run, self.useC)
        
        f = open(self.modelFile,'r')
        print 'Using the following result file:', self.modelFile
        data = json.load(f)
        p_z = np.array(data['p_z'])
        p_w_z = np.array(data['p_w_z'])
        p_d_z = np.array(data['p_d_z'])
        model = p_z, p_w_z, p_d_z
        plsa = pLSA()
        plsa.set_model(model)
        self.z = z
        self.model = plsa
        return self.modelFile
    
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

    def open_data(self, study = None, dataFile = None, name = None, sampling = False):
        '''gets the otu table from a .biom or .txt file and saves the otu table as a numpy matrix.'''
        if self.study is None:
            self.study = study
        if self.name is None:
            self.name = name
        
        def get_otu_data_file():
            if self.name is None and dataFile is not None:
                self.name = dataFile.split('/')[-1][:-4]
                    
            if dataFile is not None:
                return dataFile
            elif self.study is not None:
                self.study = str(self.study)
                return '/Users/sperez/Documents/PLSA data/EMPL data/study_'+self.study+'_split_library_seqs_and_mapping/study_'+self.study+'_closed_reference_otu_table'
            elif self.name is not None: 
                return '/Users/sperez/Documents/PLSA data/EMPL data/study_'+self.name+'/'+self.name
            else:
                print "Need study number or the name of the data file to access the data."

        dataFile = get_otu_data_file()
        self.datamatrix = extract_data(dataFile, sampling)
        return dataFile
    
    def dimensions(self):
        return self.datamatrix.shape

    def generate_runs(self, z_i = 1, z_f = None, z_inc = 1, numRuns = 1, useC = True, override = False, folder = None, add_to_file = ''):
        '''runs plsa mutliple time for a range of topics'''
        print '\nStudy', self.study, 'has', self.dimensions()[0], 'otus and', self.dimensions()[1], 'samples.'
        if z_f is None:
            z_f = int(3*sqrt(self.dimensions()[1]))
        print 'We will run PLSA with Z = {0} to {1}.'.format(z_i, z_f)
        if useC:
            print "Running PLSA using C code."
        if override:
            print "Overriding result files if necessary."

        if z_f == z_i:
            z_f += 1
        filesCreated = False
        for z in range(z_i, z_f, z_inc): 
            run = 1
            while True:
                filename = self.get_result_filename(z, run, useC, folder = folder, add_to_file = add_to_file)
                try:
                    open(filename, "r")
                    print "The results file already exists for study {0}, {1} topics and run #{2}:\n    {3}".format(self.study, z, run, filename)
                    if override:
                        print 'Overriding...'
                        break #override
                    else:
                        run += 1
                        continue #if result files already exists, we don't override
                except IOError:
                    break
            if run > numRuns: 
                print "Reached the maximum number of runs ({0}).".format(numRuns)
                continue #only want to compute plsa for each z a certain max number of times
            elif override:
                run += 1
            else:
                print "The results file DOES NOT exist for study {0}, {1} topics and run #{2} so we run plsa and create it: \n    {3}".format(self.study, z, run, filename)  
            today = datetime.datetime.today()
            print '\n', today.strftime('%b %d, %Y @ %I:%M%p')
            print 'ZZZZZZZzzzz is ',z 
        
            t0 = time()
            model = self.run_plsa(z, useC = useC, verbatim = True)
            print '\nSaving plsa to file {0}.'.format(filename)
            self.save_results(filename = filename, extension =  '.txt')
            print 'Time for analysis:', round(time()-t0,1)
            filesCreated = True
        
        if not filesCreated:
            print '\n    No files were created. Exiting...\n'
            sys.exit()
        
        return None
            
    def run_plsa(self, Z, maxiter=MAX_ITER_PLSA, verbatim = True, useC = True):
        '''runs plsa on sample data in filename'''

        plsa = pLSA()
        plsa.debug = verbatim
        print "\n Running ...\n"
        plsa.train(self.datamatrix, Z, maxiter = maxiter, useC = useC)   #runs plsa!
        self.model = plsa
        return plsa        

    def save_data(self, normalize = False):
        ''' functions saves original abundance data to a csv or txt file'''
        filename = os.path.join(_cur_dir, RESULTS_LOCATION, 'data_study_'+self.study+'.txt')
        f = open(filename,'w')
        data = self.datamatrix
        if normalize:
            data = self.normalize_array(data)
        d = [list(row) for row in data]
        json.dump(d,f)
        f.write('\n')
        f.close()
        return None
        
    def save_results(self, filename = os.path.join(RESULTS_LOCATION,'results'), extension = '.txt'):
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

    def fold_in(self, testData, useC = True):
        """
        Compute the log-likelihood that the model generated the data.
        """
        p_d_z_test = self.model.folding_in(testData, useC = useC)
        return p_d_z_test
    
    def save_kFold(self, kFold, study, z, k):
        '''Save the k fold cross validation sample assignment'''
        kPartitions = []
        for train,test in kFold:
            a,b = list(train), list(test)
            kPartitions.append([a,b])
               
        fileName = 'study_' + self.study + '_z=' + str(z) + '_kFold_' + str(k) + '.txt'
        kFoldFile = os.path.join(_cur_dir, CROSS_VAL_LOCATION, fileName)
        f = open(kFoldFile,'w')
        pickle.dump(kPartitions, f)
        return None
    
    def top_otus_labels(self, z, study = None, name = None, N_otus = 5):
        biom_data =self.open_data(study = study, name = name)
        map = self.open_otu_maps(biom_data)['OTU_MAP']
        self.open_model(study = study, name = name, z = z)
        
        otu_labels = self.model.topic_labels(map, N_otus)
        labels = []
        for label in otu_labels:
            labels.append(label)
        
        print 'Top OTUs :\n', labels
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

    def get_result_filename(self, z, run, useC, folder = None, add_to_file = ''):
        if useC:
            addC = 'with_C_'
        else: addC = ''
        
        if add_to_file is None:
            add_to_file = ''

        if self.study:
            resultsfilename = 'study_' + self.study + '_' + str(z) + '_topics_'
        elif self.name:
            resultsfilename = 'study_' + self.name + '_' + str(z) + '_topics_'
        else:
            print 'Please provide the study number or name.'
            
        ext = '.txt'

        resultsfilename += addC
        
        if run != '':
            resultsfilename += 'run' +str(run)

        resultsfilename += add_to_file    
        if folder:
            filename = os.path.join(_cur_dir, RESULTS_LOCATION, folder, resultsfilename + ext)
        else:
            filename = os.path.join(_cur_dir, RESULTS_LOCATION, resultsfilename + ext)
        return filename
