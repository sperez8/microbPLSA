import sys

sys.path.append('/Users/sperez/git/microbPLSA') 

import microbplsa

f = '/Users/sperez/Documents/workspace/myprojects/myplsa/otu_table.txt'
m = microbplsa.MicrobPLSA(f,sampling = True)

model = m.runplsa(5, verbatim = True, maxiter= 100)
m.saveresults('test')

print 'Topic Labels', model.topic_labels(None)