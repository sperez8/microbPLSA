'''
Created on 08/05/2014

author: sperez8
'''
import math

from matplotlib.backends.backend_pdf import PdfPages
import os,sys
_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)
from microbPlotter import piechart

_root_dir = os.path.dirname(_root_dir)
sys.path.insert(0, _root_dir + "/Analysis")
from indspecies import IndSpecies

from matplotlib.backends.backend_pdf import PdfPages


study = '1526'
z = 8
#group_names = '_metadata_dryness'
group_names = '_kmeans5'

for c in [0.5,0.6,0.7,0.8,0.9,0.97,0.99]:
    pdffile = '/Users/sperez/Desktop/pie_chart_'+study+'_plots'+group_names+str(c)+'.pdf'
    pdf = PdfPages(pdffile)

    indspecies = IndSpecies(study, z)
    indspecies.find_indspecies(group_names)
    indspecies.get_significant_otus(cutoff = c)
    groups = indspecies.compare()
    
    indspecies.get_stats_report()
    
    for group, plot in piechart(z, groups):
        if group < 100:
            plot.savefig(pdf, format='pdf')
        else: pass
            
    pdf.close()
    print '\n\n\n The pdf file with pie charts is ready.'
    print pdffile

