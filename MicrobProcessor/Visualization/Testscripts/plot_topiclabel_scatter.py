'''
Created on 20/11/2013

author: sperez8
'''
import os,sys
_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
_root_dir = os.path.dirname(_root_dir)
sys.path.insert(0, _root_dir)
import microbplsa
analysis_dir = _root_dir+ '/Analysis'
sys.path.insert(0, analysis_dir)
from labelling import Labelling
from correlations import numericize

study = '1037'
Z = 8

f = '/Users/sperez/git/microbPLSA/MicrobProcessor/Results/study_'+study +'_'
end = '_topics_.txt'

datafile = f+str(Z)+end

format = 'svg'



Lab = Labelling(study, Z)
metatable, factor_types, factors = Lab.metadata()
R = Lab.correlate()
labels_r = Lab.assignlabels(R)
labels, r = zip(*labels_r)
labels = [l.replace('(','\n(') for l in labels]


m = microbplsa.MicrobPLSA()
plsa = m.open_model(datafile) #get model from the results file

#return document's distribution
p_z_d = plsa.document_topics()


if format == 'svg':
    import matplotlib
    matplotlib.use('SVG')
else:
    from matplotlib.backends.backend_pdf import PdfPages
    pdf = PdfPages('/Users/sperez/Desktop/topic_scatter_'+study+'_plots.pdf')

import os,sys
_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)
from microbPlotter import *
    

for z in range(0,8):
    factor = labels[z]
    if factor in factor_types['continuous']:
        print factor
        i = factors.index(factor)
        data = list(metatable[:,i])
        Y = numericize(data)
        X = p_z_d[z,:]
        if format == 'svg':    
            plot = topiclabel_scatter(X,Y,factor,z)
            plot.savefig('/Users/sperez/Desktop/topic_scatter_'+study+'_'+factor+'plots.svg')
            plot.clf()
        elif format == 'pdf':
            plot = topiclabel_scatter(X,Y,factor,z)
            plot.savefig(pdf, format='pdf')
            plot.clf()
                            
if format == 'pdf':
    pdf.close()