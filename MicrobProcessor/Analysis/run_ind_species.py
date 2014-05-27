'''
Created on 06/05/2014

author: sperez8

Shows how to use IndSpecies class
'''

from indspecies import IndSpecies

study = '1526'
z = 8

indspecies = IndSpecies(study, z)
group_names = '_metadata_dryness'


table = indspecies.find_indspecies(group_names)
indspecies.get_significant_otus(cutoff = 0.9)
groups = indspecies.compare()
print groups



