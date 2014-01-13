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

f = "/Users/sperez/git/microbPLSA/MicrobProcessor/Results/results_"


pdf = PdfPages('/Users/sperez/Desktop/loglikelihood_curves.pdf')


for study in ['1037','1526','659','722','864']:
    plot = loglikelihood_curve(study)
    plot.savefig(pdf, format='pdf')
    print "Figure saved for study ", study
    plot.clf()

    
pdf.close()
print 'PDF file is ready to read'