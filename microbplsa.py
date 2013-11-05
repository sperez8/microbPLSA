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

class MicrobPLSA():
    '''A class to handle metagenomic data from in particular the Earth Microbiome Project
    and apply statistical tools such as Probabilistic Latent Semantic Analysis.
    This class is actually a wrapper on Mathieu Blondel's PLSA package'''

    def __init__(self, file):
        self.file = file
    
    def runplsa(self, topic_number, maxiter, verbatim = True):
        '''runs plsa on sample data in filename'''
        columns, datamatrix, otus = self.importdata(self.file)
        Z = topic_number #number of topics
        if verbatim: 
            print '\nData in matrix form:\n', datamatrix
            print len(otus), 'Otus:',otus
            print len(columns), 'Sample names:', columns
            print Z, 'topics.'
            
        plsa = pLSA()
        plsa.debug = verbatim
        plsa.random_init(Z, len(otus), len(columns))
        print "\n Running PLSA.\n"
        plsa.train(datamatrix, Z, maxiter)   #runs plsa!
        self.model = plsa
        return self.model
        
    def saveresults(self, filename = 'results'):
        ''' functions saves plsa probabilities into a .csv file'''
        filename = self.formatfile(filename)
        f = open(filename,'w')
        writer = csv.writer(f)
        p_z,p_w_z,p_d_z = self.model.get_model()
        
        writer.writerow(['p_z', p_z.shape])
        for value in p_z:
            writer.writerow(value)
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
        if filename == 'test' or 'results' or 'results.csv':
            timestamp = strftime("%d%b%H:%M", gmtime()) #add date to filename to avoid conflicts
            filename = 'results' + timestamp + '.csv'
        if filename[-4:] != '.csv':
            filename = filename +'.csv'
        return filename
    
    @staticmethod
    def importdata(self, filename):
        '''imports the date from filename and saves it in numpy array format'''
        file = open(filename,'r')
        table = file.read().splitlines() #read file and split by lines
        columns = table[1].split('\t')  #read column names which are split by tabs
        columns.pop(0)
        otus = []
        datamatrix = np.ndarray((len(table)-2,len(columns)))
        for i in range(2,len(table)):
            row = table[i].split('\t')
            otus.append(row.pop(0)) 
            datamatrix[i-2] = (row)
    
        #return datamatrix, otus
        return columns, datamatrix, np.array([int(x) for x in otus])






