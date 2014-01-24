'''
Created on 20/11/2013

author: sperez8
'''

from matplotlib.backends.backend_pdf import PdfPages
import os,sys
_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)
from microbPlotter import *

study = '1037'
f = '/Users/sperez/git/microbPLSA/MicrobProcessor/Results/study_'+study+'_'


pdf = PdfPages('/Users/sperez/Desktop/topic_dist_plots.pdf')

end = '_topics_.txt'
for z in range(2,7):
    plot = topic_distribution(f+str(z)+end)
    plot.savefig(pdf, format='pdf')
    
end = '_topics_.txt'
for z in range(7,13):
    plot = topic_distribution(f+str(z)+end)
    plot.savefig(pdf, format='pdf')
    
pdf.close()
print 'file is ready.'