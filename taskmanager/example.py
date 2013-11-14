#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009 Mathieu Blondel
# BSD license

import numpy as np
from scipy.cluster.vq import kmeans2

from taskmanager import TaskManager, TaskManagerError, task, nocache, directory

class MyProject(TaskManager):

    @task(int, int)
    def genmatrix(self, rows=1000, cols=1000):
        return np.random.random((rows, cols))

    @task(genmatrix, int)
    def dot(self, mat, n=3):
        """
        Performs matrix multiplication on mat with itself, n times.
        """
        for i in range(n):
            mat = np.dot(mat, mat)
        return mat

    @task(dot)
    @nocache
    def length(self, mat):
        print mat.shape

    #@task(dot, int)
    #def kmeans(self, mat, k=5):
        #return kmeans2(mat, k)

    #@task(genmatrix, kmeans)
    #def averages(self, mat, kmeans_res):
        #centroids, codebook = kmeans_res


if __name__ == "__main__":
    import sys
    try:
        import sys
        TaskManager.OUTPUT_FOLDER = "./tmp"
        p = MyProject()
        p.run(sys.argv[1:])
    except TaskManagerError, m:
        print >>sys.stderr, m