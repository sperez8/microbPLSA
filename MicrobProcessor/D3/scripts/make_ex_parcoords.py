'''
Created on 22/03/2013

author: sperez8
'''

import sys, os
import numpy as np

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
_root_dir = os.path.dirname(_root_dir)
sys.path.insert(0, _root_dir)
import microbplsa
from utilities import get_otu_ranks
analysis_dir = _root_dir+ '/Analysis'
sys.path.insert(0, analysis_dir)
from labelling import Labelling
from string import replace

study = '1526'
z = 8
CORRELATION_THRESHOLD = 0.0
MANUAL_LABELS = ['','Average Soil Depth (cm)','','', 'Abundance (reads)', 'Ph', 'Respiration']
to_show = [1,4,5,6]
pcoordfile = _root_dir + '/D3/pcplots/otus.js'
level = "phylum"


datafile = '/Users/sperez/Documents/PLSAfun/EMPL data/study_'+study+'_split_library_seqs_and_mapping/study_'+study+'_closed_reference_otu_table.biom'

m = microbplsa.MicrobPLSA()
plsa = m.open_model(study = study, z = z) #get model from the results file
p_w_z = plsa.p_w_z #return otus topic distribution
otus_map = m.open_otu_maps(datafile) # create {otu id: otu name} dictionary
W,Z =p_w_z.shape #number of otus and topics
   
#get labels     
#Lab = Labelling(study, Z, ignore_continuous = False, adjusted_metadata = True) #get labels!
#Lab.metadata(non_labels = [])
labels = ['\"'+l+'\"' for l in MANUAL_LABELS]

#get phylums
#topotus = m.topic_OTUS(f,5) #indicator otus #NOT USING THIS INFORMATION YET

ranks = get_otu_ranks(otus_map, level = level)
print ("There are %i different %s."%(len(ranks), level))
    
f = open(pcoordfile, 'w')
f.write('var otus = [\n')

acidic = True
otus_index = otus_map["OTU_MAP"]
for (i,dist) in enumerate(p_w_z):
    if i%30 == 0:
        for rank in ranks:
            if rank in otus_index[i]:
                line ='{'
                line += level+':\"'+rank+'\"'
                for j,p in enumerate(dist):
                    if j in to_show:
                        if j == 1: 
                            p*=3000
                            if p == 0: p = 16*np.random.random()
                            if p > 10: acidic =False
                            else: acidic = True
                        elif j == 4:
                            p*=300000/9000*800
                            if p <50 : 
                                if np.random.random()>0.7:
                                    p = 560*np.random.random()
                                elif np.random.random()>0.6:
                                    p = 120*np.random.random()
                                elif np.random.random()>0.7:
                                    p = 100*np.random.random()
                                elif np.random.random()>0.7:
                                    p = 20*np.random.random()                                
                        elif j == 5:
                            p*=1000/6*7
                            if p <1 : 
                                if acidic:
                                    p = np.random.randint(low = 0, high = 3)
                                else:
                                    p = np.random.randint(low = 4, high = 8)
                            if p==0: p=2
                        if j == 6:
                            p*=2500
                            if p <1 : p = '\"anaerobic\"'
                            elif p < 2: p = '\"facultative anaerobic\"'
                            else: p = '\"aerobic\"'
                        else: p = str(round(p,3))
                        line += ', ' + labels[j] + ':' + p
                line += '},\n'
                f.write(line)
f.write('];\n')

f.write('var dim = [\n\'')
f.write(level+'\',\'')
f.write('\',\''.join(labels))
f.write('\'];\n')

f.write('var types = {\n')
f.write('\"'+level+'\": \"string\",')

for label in labels:
    f.write(label+': \"number\",')
f.write('};\n')   
    
f.close()    
print "File is ready."





























