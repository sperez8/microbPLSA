'''
Created on 12/09/2014

author: sperez8
'''

import sys, os
import argparse

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

import microbplsa

FOLDER = 'Models'

#analysis_dir = os.path.join(_root_dir, 'Analysis')
#sys.path.insert(0, analysis_dir)

#import top_otus as top

def main(*argv):
    '''handles user input and runs different analysis functions using plsa model'''

    parser = argparse.ArgumentParser(description='This scripts runs plsa for a range of topic numbers.')
    parser.add_argument('-s','--study', help='The study number', default = None)
    parser.add_argument('-n','--name', help='The name of the dataset')
    parser.add_argument('-z','--topics', help='The range of topics to be run [z_start, z_end]', nargs = '+', type = int, required = True)
    parser.add_argument('-z_inc','--increment', help='Increment of topic numbers', type = int, default = 1)
    parser.add_argument('-useC', help='use C code to run plsa', action = 'store_true')
    parser.add_argument('-run', help='Specify the run number', type = int, default = 1)
    parser.add_argument('-topotus', help='Specify to calculate the top otus', action = 'store_true')
    parser.add_argument('-n_otus', help='Specify the number of top otus to return per topic', type = int, default = 5)
    parser.add_argument('-calculateX', help='Specify to calculate X', action = 'store_true')
    
    args = parser.parse_args()
    
    if args.study is None and args.name is None:
        print "***Study number or a data name must be specified.***\n"
        parser.print_help()
        sys.exit()
    
    if not args.calculateX and not args.topotus:
        print "***Please specify an action to perform from the following: 'topotus', 'calculateX' "
        parser.print_help()
        sys.exit()
    
    if args.study:
        study = str(args.study)
    else: study = None
    name = args.name
    if len(args.topics) == 1:
        z_i = args.topics[0]
        z_f = args.topics[0]
    elif len(args.topics) == 2: 
        z_i = min(args.topics)
        if z_i < 2: 
            z_i = 2
        z_f = max(args.topics)
    else:
        print "\n***Too many arguments specified for number of topics***\n"
        parser.print_help()
        sys.exit()
    z_inc = args.increment
    run = args.run
    useC = args.useC
    topotus = args.topotus
    n_otus = args.n_otus
    calculateX = args.calculateX

    print ("    Study: %s" % study)
    print ("    Name: %s" % name)
    if z_i != z_f:
        print ("    Topics range: [{0} - {1}] in increments of {2}".format(z_i, z_f, z_inc))
    else:
        print ("    Topic number used: {0}".format(z_i))
    print ("    Using C: %s" % args.useC)
    print ("    Run number: %s" % args.run)

    m = microbplsa.MicrobPLSA(study = study, name = name)
    #m.open_data()
    
    for z in range(z_i, z_f+1, z_inc): 
        if topotus:
            print "Finding top otus per each topic"
            #dataFile = m.open_data(study = study, name = name)
            m.open_model(z = z, run = run, useC = True, folder = FOLDER)
            m.top_otus_labels(z, n_otus = n_otus)
        if calculateX:
            pass
            #do something...
        

if __name__ == "__main__":
    main(*sys.argv[1:])