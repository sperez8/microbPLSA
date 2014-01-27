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
f = "/Users/sperez/git/microbPLSA/MicrobProcessor/Results/results_"


t0 = time()

for study in ['722']:
    file = '/Users/sperez/Desktop/loglikelihood_curves'+study+'_.pdf'
    pdf = PdfPages(file)
    plot = loglikelihood_curve(study)
    plot.savefig(pdf, format='pdf')
    print "Figure saved for study ", study
    plot.clf() 
    pdf.close()
    
print 'Process took', time()-t0
print 'PDF file is ready to read: ', file