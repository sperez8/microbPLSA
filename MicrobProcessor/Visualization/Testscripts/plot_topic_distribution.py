'''
Created on 20/11/2013

author: sperez8
'''
import numpy as np
from time import time
import sys,os
   
_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
_root_dir = os.path.dirname(_root_dir)
analysis_dir = _root_dir+ '/Analysis'
sys.path.insert(0, analysis_dir)
from clustering import *

t0 = time()
study = '1526'
Z = [8]
useC = False
run = 4
name = None
datafile = '/Users/sperez/Documents/PLSA data/EMPL data/study_'+study+'_split_library_seqs_and_mapping/study_'+study+'_closed_reference_otu_table.biom'

format = 'svg'

order = None
order = makedendrogram(study = study, filename = datafile, showme = False)
order = [int(o) for o in order]
order = np.array(order)

print "Dendogram done!"

if format == 'svg':
    import matplotlib
    matplotlib.use('SVG')
    
    import os,sys
    _cur_dir = os.path.dirname(os.path.realpath(__file__))
    _root_dir = os.path.dirname(_cur_dir)
    sys.path.insert(0, _root_dir)
    from microbPlotter import * #have to import this AFTER selecting SVG usage.
    
    for z in Z:
        plot = topic_distribution(name = name, study = study, order = order, run = run, useC = useC, z = z)
        topicFile = '/Users/sperez/Desktop/topic_dist_'+study+'_'+str(z)+'plots'
        if useC:
            topicFile += '_withC'
        topicFile += '_run'+str(run)+'.svg'
        plot.savefig(topicFile)
        print '\n\n\n The topic distribution svg file is ready.', topicFile

elif format == 'pdf':

    import os,sys
    _cur_dir = os.path.dirname(os.path.realpath(__file__))
    _root_dir = os.path.dirname(_cur_dir)
    sys.path.insert(0, _root_dir)
    from microbPlotter import *
    
    from matplotlib.backends.backend_pdf import PdfPages
    topicFile = '/Users/sperez/Desktop/topic_dist_'+study+'_'+str(z)+'plots_C'
    pdffile = topicFile + '.pdf'
    pdf = PdfPages(pdffile)
    
    for z in Z:
        plot = topic_distribution(name = name, study = study, order = order, run = run, useC = useC, z = z)
        plot.savefig(pdf, format='pdf')
        
    pdf.close()
    print '\n\n\n The topic distribution pdf file is ready.'
    print 'Process took', round(time()-t0,1), 'seconds'
    print pdffile



