'''
created 25/02/2014

by sperez

parses tab delimited files
and creates text output for hive.html
'''

import csv
import numpy as np
import json

outnodesfile = '/Users/sperez/D3/hiveplots/WebContent/nodes.js'
outlinksfile = '/Users/sperez/D3/hiveplots/WebContent/links.js'
innodesfile = '/Users/sperez/D3/hiveplots/Data/nodes_mod.txt'
inlinksfile = '/Users/sperez/D3/hiveplots/Data/links.txt'

def get_nodes(file):
	'''returns node data from csv file'''
	data = np.loadtxt(file, delimiter="\t", skiprows = 1)
	nodes = list(data[:,0])
	depths = data[:,1]
	modules = data[:,2]
	degrees = list(data[:,3])
	return nodes, depths, modules, degrees
    
def get_links(file):
	'''returns link data from csv file'''
	data = np.loadtxt(file, delimiter="\t")
	sources = data[:,0]
	targets = data[:,1]
	
	return sources, targets
	
def axis_assignment(degrees, low, high):
	'''assigns nodes to axis number given 
		a variable such as degree'''
	degrees = [int(d) for d in degrees]
	axis = []
	for degree in degrees:
		if degree <= low: #low degree nodes
			axis.append(0)
		elif degree <= high: #medium degree nodes
			axis.append(1)
		else: #high degree nodes
			axis.append(2)
	return axis


def axis_position(depths, ngroups):
	'''scales some variable to assign an axis position
		to the nodes. For example, average depths is normalized
	 	here to fit on axis'''
	depths = [float(d) for d in depths]
	maxd = max(depths)
	newdepths = [round(d/maxd, 2) for d in depths]

##Uncomment below to assign each node to a group number depending 
## on its depth. to be used for node colouring	
# depth.sort()
#	depthgroup = []
# 	if ngroups == 3:
# 		low = depths[int(float(len(depths))/3.0)]
# 		high = depths[int(float(len(depths))*2.0/3.0)]
# 
# 		for d in depths:
# 			if d <= low:
# 				depthgroup.append(0)
# 			elif d <= high:
# 				depthgroup.append(1)
# 			else:
# 				depthgroup.append(2)
	return newdepths


def module_assignment(modules, modulenames):
	'''assignes numbers to the nodes depending on which module
		they belong too, give the dictionary modulename. The nodes
		will then be colored given their module group number'''
	modulegroups = []
	for m in modules:
		if m in modulenames.keys(): 
			modulegroups.append(modulenames[m])
		else:
			modulegroups.append(0)	
	return modulegroups


def write_nodes(file, positions, axis, modulegroup):
	'''outputs node info to a text file
		in a javascript variable format'''
	f = open(file, 'w')
	f.write('var nodes = [\n')
	for a, p, m in zip(axis, positions, modulegroup):
		f.write('  {x: '+str(a)+', y: '+str(p)+', z: '+str(m)+'},\n')
	f.write('];')
	
def write_links(file, nodes):
	'''outputs node info to a text file
		in a javascript variable format'''
	f = open(file, 'w')
	f.write('var links = [\n')
	for s, t in zip(sources, targets):
		f.write('  {source: nodes['+str(nodes.index(s))+'], target: nodes['+str(nodes.index(t))+']},\n')
	f.write('];')
    
    
#What to run
nodes, depths, modules, degrees = get_nodes(innodesfile)
sources, targets = get_links(inlinksfile)
positions = axis_position(depths, 5)
axis = axis_assignment(degrees, 2, 16)
modulenames = {1:'4', 2:'2', 9:'3', 4:'1', 11:'5'} #numbers in str encode for the A,B,C,D,E modules
modulegroup = module_assignment(modules, modulenames)
write_nodes(outnodesfile, positions, axis, modulegroup)
write_links(outlinksfile, nodes)

























