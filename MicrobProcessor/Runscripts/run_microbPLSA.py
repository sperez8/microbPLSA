'''
Created on 16/09/2013

author: sperez8
'''

import sys, os
import argparse

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

import microbplsa


def main(*argv):
    '''handles user input and runs plsa'''

    parser = argparse.ArgumentParser(description='This scripts runs plsa for a range of topic numbers.')
    parser.add_argument('-s','--study', help='The study number')
    parser.add_argument('-n','--name', help='The name of the dataset')
    parser.add_argument('-z','--topics', help='The range of topics to be run [z_start, z_end]', nargs = '+', type = int, required = True)
    parser.add_argument('-z_inc','--increment', help='Increment of topic numbers', type = int, default = 1)
    parser.add_argument('-useC', help='use C code to run plsa', action = 'store_true')
    parser.add_argument('-runs','-numruns', help='Specify the number of runs', type = int, default = 1)
    
    args = parser.parse_args()
    
    if args.study is None and args.name is None:
        print "***Study number or a data name must be specified.***\n"
        parser.print_help()
        sys.exit()
    
    study = str(args.study)
    name = args.name
    if len(args.topics) == 1:
        z_i = 2
        z_f = args.topics
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
    numRuns = args.runs
    useC = args.useC

    print ("    Study: %s" % study)
    print ("    Name: %s" % name)
    print ("    Topics will be run from {0} to {1} in increments of {2}".format(z_i, z_f, z_inc))
    print ("    Using C: %s" % args.useC)
    print ("    Number of runs: %s" % args.runs)


    m = microbplsa.MicrobPLSA()
    m.open_data(study = study)
    m.generate_runs(z_i = z_i, z_f = z_f, z_inc = z_inc, numRuns = numRuns, useC = useC)

if __name__ == "__main__":
    main(*sys.argv[1:])