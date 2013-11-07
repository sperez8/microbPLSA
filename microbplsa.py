'''
Created on 16/09/2013

author: sperez8
'''
import numpy as np
import csv
from time import time, gmtime, strftime
import sys
sys.path.append('/Users/sperez/Documents/workspace/PLSA/') #Mathieu Blondel's PLSA package
from plsa import pLSA
from utilities import *

class MicrobPLSA():
    '''A class to handle metagenomic data from in particular the Earth Microbiome Project
    and apply statistical tools such as Probabilistic Latent Semantic Analysis.
    This class is actually a wrapper on Mathieu Blondel's PLSA package'''

    def __init__(self, file, sampling = False):
        self.file = file
        self.sampling = sampling #boolean tells us to use full dataset or not
        self.columns, self.datamatrix, self.otus = extract_data(self.file, self.sampling)
        
    def runplsa(self, topic_number, maxiter, verbatim = True):
        '''runs plsa on sample data in filename'''
        columns, datamatrix, otus = self.columns, self.datamatrix, self.otus
        Z = topic_number #number of topics
        if verbatim: 
            print '\nData in matrix form:\n', datamatrix, '\n'
            print len(otus), 'Otus:',otus
            print len(columns), 'Samples:', columns
            print Z, 'Topics.'
            
        plsa = pLSA()
        plsa.debug = verbatim
        plsa.random_init(Z, len(otus), len(columns))
        print "\n Running PLSA...\n"
        plsa.train(datamatrix, Z, maxiter)   #runs plsa!
        self.model = plsa
        return self.model
        
    def saveresults(self, filename = 'Results/results'):
        ''' functions saves plsa probabilities into a .csv file'''
        filename = self.formatfile(filename)
        f = open(filename,'w')
        writer = csv.writer(f)
        p_z,p_w_z,p_d_z = self.model.get_model()
        
        writer.writerow(['p_z', p_z.shape])
        writer.writerow(p_z)
        writer.writerow(['p_d_z', p_d_z.shape])
        for value in p_d_z:
            writer.writerow(value)    
        writer.writerow(['p_w_z', p_w_z.shape])
        for value in p_w_z:
            writer.writerow(value)
            
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
    def formatfile(filename):
        '''formats name of file to get correct file format and avoid conflicts'''
        if 'results' in filename:
            timestamp = strftime("%d%b%H:%M", gmtime()) #add date to filename to avoid conflicts
            filename = filename + timestamp
        if filename[-4:] != '.csv':
            filename = filename +'.csv'
        if 'Results/' not in filename:
            filename = 'Results/'+filename
        return filename
    





