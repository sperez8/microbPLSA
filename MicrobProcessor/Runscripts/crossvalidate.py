'''
Created on 09/09/2013

author: sperez8
'''

import sys, os
import argparse
import numpy as np

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

import microbplsa

analysis_dir = os.path.join(_root_dir, 'Analysis')
sys.path.insert(0, analysis_dir)

import kFold_uttilities as kf


def main(*argv):
    '''handles user input and runs plsa'''

    parser = argparse.ArgumentParser(description='This scripts runs cross validations to determine the optimal number of topics.')
    parser.add_argument('-action', help='Action to perform from "all", "train", "test", "mse"', required = True)
    parser.add_argument('-k', help='Number of folds in kFold cross validation', type = int, default = 5)
    parser.add_argument('-s','--study', help='The study number', default = None)
    parser.add_argument('-n','--name', help='The name of the dataset')
    parser.add_argument('-z','--topics', help='The range of topics to be run [z_start, z_end]', nargs = '+', type = int, required = True)
    parser.add_argument('-z_inc','--increment', help='Increment of topic numbers', type = int, default = 1)
    parser.add_argument('-useC', help='use C code to run plsa', action = 'store_true')
    parser.add_argument('-run', help='Specify the number of the run', type = int, default = 1)
    parser.add_argument('-seed', help='Random seed for kFold generator', type = int, default = 2)
    args = parser.parse_args()
    
    if args.action not in ['all', 'train', 'test', 'mse']:
        print "***The specified action is not recognized.***\n"
        parser.print_help()
        sys.exit()
    else:
        action = str(args.action)
        
    k = args.k
    
    if args.study is None and args.name is None:
        print "***Study number or a data name must be specified.***\n"
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
    seed = args.seed
    

    print ("    Study: %s" % study)
    print ("    Name: %s" % name)
    if z_i != z_f:
        print ("    Topics tested will be from {0} to {1} in increments of {2}".format(z_i, z_f, z_inc))
    else:
        print ("    Number of topics: {0}".format(z_i))
    print ("    Using C: %s" % args.useC)
    print ("    Number of run used: %s" % args.run)
    print ("    Action performed: %s" % action)
    print ("    Number of folds, k= : %s" % k)

    m = microbplsa.MicrobPLSA(study = study, name = name)
    mseAll = []
    if action == 'train' or action == 'test' or action == 'all':
        m.open_data()
        print 'Data loaded.'
        
    for z in range(z_i, z_f+1, z_inc): 
        if action == 'train' or action == 'all':
            kFolds = kf.create_folds(m, k, z, shuffle = True, seed = seed)
            data = m.datamatrix
            kf.train(k, kFolds, data, study, name, z, numRuns = run, seed = seed, useC = useC, override = False)
        if action == 'test' or action == 'all':
            kFolds = kf.open_kFold(study, name, k, z)
            kf.test(m, kFolds, k, z, useC = useC, seed = seed)
        if action == 'mse' or action == 'all':
            kFolds = kf.open_kFold(study, name, k, z)
            mse = kf.measure_error(m, kFolds, k, z)
            print "\n The cross validation error for study {0} with {1} topics and {2} folds is:     {3} +/-{4}\n".format(study, z, k, round(np.mean(mse),5), round(np.std(mse),5))
            mse.insert(0,z)
            mseAll.append(mse)
    
    if mseAll:
        kf.save_mse(mseAll, k, z, study, name, seed, run)
    
if __name__ == "__main__":
    main(*sys.argv[1:])
    
    
    