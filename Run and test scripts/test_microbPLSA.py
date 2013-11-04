import sys

sys.path.append('/Users/sperez/git/microbPLSA') 

import microbplsa

f = 'otu_table.txt'
m = microbplsa.MicrobPLSA(f)
