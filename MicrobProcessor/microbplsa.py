'''
Created on 16/09/2013

author: sperez8
'''
import numpy as np
import csv
from time import time, localtime, strftime
from utilities import *
import sys, os

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir + os.sep + "PLSA")
from plsa import pLSA

class MicrobPLSA():
    '''A class to handle metagenomic data from in particular the Earth Microbiome Project
    and apply statistical tools such as Probabilistic Latent Semantic Analysis.
    This class is actually a wrapper on Mathieu Blondel's PLSA package'''

    def __init__(self):
        return None
        
    def open_model(self, file):
        ''' Opens the probs of a model previously computed and saved in a json file '''
        f = open(file,'r')
        data = json.load(f)
        p_z = np.array(data['p_z'])
        p_w_z = np.array(data['p_w_z'])
        p_d_z = np.array(data['p_d_z'])
        model = p_z, p_w_z, p_d_z
        plsa = pLSA()
        plsa.set_model(model)
        return plsa

    def runplsa(self, file, topic_number, maxiter=500, verbatim = True, sampling = False):
        '''runs plsa on sample data in filename'''
        self.columns, self.datamatrix, self.otus = extract_data(file, sampling)
        samples, datamatrix, otus = self.columns, self.datamatrix, self.otus
        Z = topic_number #number of topics
#         if verbatim: 
#             print '\nData in matrix form:\n', datamatrix.shape, '\n'
#             print datamatrix
#             print len(otus), 'Otus:',otus
#             print len(samples), 'Samples:', samples
#             print Z, 'Topics.'
            
        plsa = pLSA()
        plsa.debug = verbatim
        print "\n Running PLSA...\n"
        plsa.train(datamatrix, Z, maxiter)   #runs plsa!
        self.model = plsa
        return plsa
    
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
    
    
    @staticmethod
    def formatfile(filename, extension):
        '''formats name of file to get correct file format and avoid conflicts'''
        if 'results' in filename:
            timestamp = strftime("%d%b%H:%M", localtime()) #add date to filename to avoid conflicts
            filename = filename + timestamp
        if filename[-4:] != extension:
            filename = filename + extension
        if 'Results/' not in filename:
            filename = 'Results/'+filename
        return filename







