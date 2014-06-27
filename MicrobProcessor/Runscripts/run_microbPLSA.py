'''
Created on 16/09/2013

author: sperez8
'''

import sys, os
from time import time
import datetime
import itertools

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

import microbplsa
from math import sqrt
#f = '/Users/sperez/Documents/workspace/myprojects/myplsa/otu_table.txt'

#for study in ['1526'] #, '1037','722','1043','864', '1702', '1642','1692','1579','1578','1526','1289','1034','990']:

#study = '1526'
#Z = 40
#max_runs = 4


file = '/Users/sperez/Desktop/LSTP/LTSP-6site_tags/Bacterial/bac_final.an.0.03.otutable.txt'
#file = '/Users/sperez/Desktop/sample.txt'
Z = 100
study = None
max_runs = 1


  
m = microbplsa.MicrobPLSA()
m.open_data(study = study, file = file, sampling = False)
(w,d) = m.dimensions()
print '\n\n\nStudy', study, 'has', w, 'otus and', d, 'samples.'

if Z is not None: 
    num_topics = Z
else: 
    num_topics = int(3*sqrt(d))
print 'We will run PLSA with Z = 2 to', num_topics


for z in range(5,num_topics,5):
    ext = '.txt'
    if study:
        resultsfilename = 'study_' + study + '_' + str(z) + '_topics_'
    else:
        name = file.split('/')[-1][:-4]
        resultsfilename = 'study_' + name + '_' + str(z) + '_topics_'
        

    run = ''
    while True:
        print 'looping'
        if run == '' : 
            filename = _root_dir + '/Results/' + resultsfilename + ext
        else: 
            filename = _root_dir + '/Results/' + resultsfilename + 'run' +str(run) + ext
        print filename, run
        try:
            open(filename, "r")
            if study:
                name = study
            print "The results file already exists for study", name, "and", z, "topics and run "+ str(run) +"."
            if run  == "": 
                run = 2
            else: 
                run += 1
            continue #if result files already exists, we don't override
        except IOError:
            #found a file not yet written so we run PLSA with those parameters.
            break
        
    if run != '' and run >= max_runs: 
        continue   #only want to compute plsa for each z a certain max number of times
    print "\nSaving plsa to file:", filename
    #plsa has not been run with that topic number and study so we run it!
    today = datetime.datetime.today()
    print '\n', today.strftime('%b %d, %Y @ %I:%M%p')
    print 'ZZZZZZZzzzz is ',z, '\n' 

    t0 = time()
    model = m.runplsa(z, verbatim = True)        
    m.saveresults(filename = filename, extension =  '.txt')
    print 'Topic Labels', model.topic_labels(None)
    print 'Time for analysis:', int(time()-t0)
    
