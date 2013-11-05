'''
Created on 3/11/2013

author: sperez8

contains a bunch of different utilities to read EMP data

'''

def find_otu_name(id):
    id = str(id)
    tax_file = '/Users/sperez/Documents/PLSAfun/gg_otus_4feb2011/taxonomies/greengenes_tax.txt'
    tax_table = open(tax_file,'r')
    
    for line in tax_table:
        if id in line:
            return line
            
import time
t0 = time.time()
id = 89440
print find_otu_name(id)
print time.time() - t0