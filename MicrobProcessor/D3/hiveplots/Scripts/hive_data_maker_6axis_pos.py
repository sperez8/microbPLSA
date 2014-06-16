'''
created 25/02/2014
modified 13/05/2014

by sperez

Makes positive edges network
'''
import os
import sys
import csv
import numpy as np
import json

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

#global variables
NUM_AXIS = 6
AXIS_INDEX = [0,2,4]
LOW_DEG = 1
HIGH_DEG = 15
delimiter = ","
modulenames = {1:'1',2:'2',3:'3',4:'4'} #numbers in str encode for four components modules


outnodesfile = _root_dir + '/WebContent/nodesmod' + str(NUM_AXIS) + 'pos' + '.js'
outlinksfile = _root_dir + '/WebContent/linksmod' + str(NUM_AXIS) + 'pos' + '.js'
innodesfile = _root_dir + '/Data/WL_Nodes_ALL.csv'
inlinksfile = _root_dir + '/Data/WL_Pos_Edges_Ensemble.csv'

def get_nodes(file):
	'''returns node data from csv file'''
	data = np.loadtxt(file, delimiter=delimiter, skiprows = 1, usecols = (0,2,3,4,5))
	nodes = list(data[:,0])
	nodesa = [str(n)+'a' for n in nodes]
	nodesb = [str(n)+'b' for n in nodes]
	nodes = nodesa+nodesb
	depths = list(data[:,2])*2
	modules = list(data[:,1])*2
	degrees = list(data[:,4])*2
	return nodes, depths, modules, degrees
    
def get_links(file):
	'''returns link data from csv file'''
	data = np.loadtxt(file, delimiter=delimiter, skiprows=1, usecols = (0,1))
	sources = list(data[:,0])
	#sa = [str(s)+'a' for s in sources]
	#sb = [str(s)+'b' for s in sources]
	#sources = sa + sb
	targets = list(data[:,1])
	#ta = [str(t)+'a' for t in targets]
	#tb = [str(t)+'b' for t in targets]
	#targets = ta + tb
	return sources, targets
	
def axis_assignment(nodes, sources, targets, degrees, low, high):
	'''assigns nodes to axis number given 
		a variable such as degree'''
	degrees = [int(d) for d in degrees]
	axis = {}
	a,b,c = 0,0,0
	for n,degree in zip(nodes,degrees):
		if degree <= low: #low degree nodes
			axis[n] = AXIS_INDEX[0]
			a+=1
		elif degree <= high: #medium degree nodes
			axis[n] = AXIS_INDEX[1]
			b+=1
		else: #high degree nodes
			axis[n] = AXIS_INDEX[2]
			c+=1
		if 'b' in n:
			if NUM_AXIS == 6:
				axis[n]+=1 #populate all 0-5 axis
			elif axis[n] != 0 :
				axis[n]+=1 #populate all 0-4 axis
	#print 'number of nodes in degree categories', a,b,c
	return axis

def doublelinks(degrees, sources, targets, axis):
	'''fixes links to accomodate for the doubling the axis'''
	newsources = []
	newtargets = []
	for s,t in zip(sources, targets):
		sa = str(s) + 'a'
		ta = str(t) + 'a'
		sb = str(s) + 'b'
		tb = str(t) + 'b'
		#if not (degrees[nodes.index(sa)] == 1 and degrees[nodes.index(ta)] == 1):
		if NUM_AXIS == 6:
			if sa not in axis:
				print "s", s
				continue
			if ta not in axis:
				print "t", t
				continue
			if (axis[sa] == 0 and axis [tb] == 1):
				newsources.append(sa)
				newtargets.append(tb)
				#need to double within doubled axis links for symmetry
				newsources.append(sb)
				newtargets.append(ta)
			elif (axis[sa] == 2 and axis [tb] == 3):
				newsources.append(sa)
				newtargets.append(tb)
				#need to double within doubled axis links for symmetry
				newsources.append(sb)
				newtargets.append(ta)
			elif (axis[sa] == 4 and axis [tb] == 5):
				newsources.append(sa)
				newtargets.append(tb)
				#need to double within doubled axis links for symmetry
				newsources.append(sb)
				newtargets.append(ta)
			elif (axis[sb] == 1 and axis [ta] == 2):
				newsources.append(sb)
				newtargets.append(ta)
			elif (axis[sb] == 3 and axis [ta] == 4):
				newsources.append(sb)
				newtargets.append(ta)
			elif (axis[sb] == 5 and axis [ta] == 0):
				newsources.append(sb)
				newtargets.append(ta)
			#same thing but with source and target switched
			elif (axis[tb] == 1 and axis [sa] == 2):
				newsources.append(sa)
				newtargets.append(tb)
			elif (axis[tb] == 3 and axis [sa] == 4):
				newsources.append(sa)
				newtargets.append(tb)
			elif (axis[tb] == 5 and axis [sa] == 0):
				newsources.append(sa)
				newtargets.append(tb)	
	return newsources, newtargets


def axis_position(nodes, depths):
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

	newdepths_dict = {}
	for n, d in zip(nodes, newdepths):
		newdepths_dict[n]=d
	return newdepths_dict


def module_assignment(nodes, modules, modulenames):
	'''assignes numbers to the nodes depending on which module
		they belong too, give the dictionary modulename. The nodes
		will then be colored given their module group number'''
	modulegroups = {}
	for m, n in zip(modules,nodes):
		if m in modulenames.keys(): 
			modulegroups[n] = modulenames[m]
		else:
			modulegroups[n] = 0
	return modulegroups


def write_nodes(file, nodes, positions, axis, modulegroup):
	'''outputs node info to a text file
		in a javascript variable format'''
	f = open(file, 'w')
	f.write('var nodes = [\n')

	for n in nodes:
		f.write('  {axis: '+str(axis[n])+', pos: '+str(positions[n])+', mod: '+str(modulegroup[n])+'},\n')
	f.write('];')
	
def write_links(file, nodes, sources, targets):
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
positions = axis_position(nodes, depths)
axis = axis_assignment(nodes, sources, targets, degrees,  LOW_DEG, HIGH_DEG)
modulegroup = module_assignment(nodes, modules, modulenames)
write_nodes(outnodesfile, nodes, positions, axis, modulegroup)
sources, targets = doublelinks(degrees, sources, targets, axis)
write_links(outlinksfile, nodes, sources, targets)
print "All done :)"
























