import sys

sys.path.append('/Users/sperez/git/microbPLSA') 

import microbplsa

f = '/Users/sperez/Documents/workspace/myprojects/myplsa/otu_table.txt'
m = microbplsa.MicrobPLSA(f)

m.runplsa(10, verbatim = True, maxiter= 100)
m.saveresults('test')