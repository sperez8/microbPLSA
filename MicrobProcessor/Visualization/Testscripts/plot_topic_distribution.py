'''
Created on 20/11/2013

author: sperez8
'''


study = '1037'
#Z = range(2,19)
Z = [6]
f = '/Users/sperez/git/microbPLSA/MicrobProcessor/Results/study_'+study +'_'

format = 'svg'

if format == 'svg':
    import matplotlib
    matplotlib.use('SVG')
    
    import os,sys
    _cur_dir = os.path.dirname(os.path.realpath(__file__))
    _root_dir = os.path.dirname(_cur_dir)
    sys.path.insert(0, _root_dir)
    from microbPlotter import * #have to import this AFTER selecting SVG usage.
    
    end = '_topics_.txt'
    for z in Z:
        plot = topic_distribution(f+str(z)+end,study)
        plt.savefig('/Users/sperez/Desktop/topic_dist_'+study+'_'+str(z)+'plots.svg')
        print '\n\n\n The topic distribution svg file is ready.'

elif format == 'pdf':

    import os,sys
    _cur_dir = os.path.dirname(os.path.realpath(__file__))
    _root_dir = os.path.dirname(_cur_dir)
    sys.path.insert(0, _root_dir)
    from microbPlotter import *
    
    from matplotlib.backends.backend_pdf import PdfPages
    
    pdf = PdfPages('/Users/sperez/Desktop/topic_dist_'+study+'plots.pdf')
    
    for z in range(2,19):
        plot = topic_distribution(f+str(z)+end,study)
        plot.savefig(pdf, format='pdf')
        
    pdf.close()
    print '\n\n\n The topic distribution pdf file is ready.'



