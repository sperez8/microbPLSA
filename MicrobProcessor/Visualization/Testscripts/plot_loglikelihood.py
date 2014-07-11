'''
Created on 13/01/2014

author: sperez8
'''

from matplotlib.backends.backend_pdf import PdfPages
import os,sys
_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)
from microbPlotter import *
from time import time


study = None
name = 'bac_final0.03.otutable_GOODSAMPLES'
run = 1
#run = 'all'
useC = True
t0 = time()

file = '/Users/sperez/Desktop/loglikelihood_curves'+name+'_run_'+str(run)+'.pdf'
print "Plotting log likelihood curve for study ", name
pdf = PdfPages(file)
plot = loglikelihood_curve(study = study, name = name, run = run, useC = useC, save = True)
plot.savefig(pdf, format='pdf')
print "Figure saved for study ", study
plot.clf() 
pdf.close()
    
print 'Process took', time()-t0
print 'PDF file is ready to read: ', file