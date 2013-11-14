# -*- coding: utf-8 -*-

# Copyright (c) 2009 Mathieu Blondel
# BSD license

import unittest
from types import FunctionType, InstanceType, MethodType, ClassType
import shutil
import os
import random
from math import sqrt
import pickle

import numpy as np

from taskmanager import *

TEST_FOLDER = "/tmp/taskmanagertests/"

TEST_LOGGER = logging.getLogger('TaskManagerTestLogger')
TEST_LOGGER.addHandler(logging.FileHandler("/dev/null"))

class MyStr(str):

    def twice(self):
        return self + self

class MyProject(TaskManager):

    @task(int, int)
    def task1(self, param1=10, param2=15):
        return param1 + param2

    @task(task1)
    def task2(self, task1_inp):
        return task1_inp / 2

    @task(task2)
    def task3(self, task2_inp):
        return task2_inp * 3

    @task
    def task4(self):
        return 10.0

    @task(task4, task3, float)
    def task5(self, task4_inp, task3_inp, epsilon=0.001):
        arr = np.random.random((int(task4_inp), int(task3_inp)))
        arr -= epsilon
        return arr

    # task2 ends up being required twice
    @task(task5, task2)
    def task6(self, task5_inp, task2_inp):
        arr = task5_inp * task2_inp
        return np.linalg.svd(arr) # returns a tuple

    @task
    @nocache
    def task7(self):
        return random.randint(0,1000000000)

    @nocache
    @task(any)
    def task8(self, somearg):
        return random.randint(0,1000000000)

    @task(directory("t*.py"))
    def task9(self, mydir):
        assert(mydir.__class__.__name__ == "Directory")
        return (sorted(mydir.get_files())[0], random.randint(0,1000000000))

    @task(file)
    def task10(self, myfile):
        assert(isinstance(myfile, file))
        return (myfile.readlines()[0], random.randint(0,1000000000))

    def task11_utility(self):
        return "MyProject"

    @task
    def task11(self):
        return self.task11_utility()

    @task(MyStr)
    def task12(self, s="blabla"):
        return s.twice()

class MyProject2(MyProject):

    @task(MyProject.task2)
    def task3(self, task2_inp):
        return task2_inp * 2

    def task11_utility(self):
        return "MyProject2"

@task
def functask1():
    return 10

@task(functask1)
def functask2(functask1_inp):
    return np.random.random((10, functask1_inp))

@task(functask1)
@nocache
def functask3(functask1_inp):
    return np.random.random((10, functask1_inp))

class TaskManagerTest(unittest.TestCase):

    def setUp(self):
        TaskManager.OUTPUT_FOLDER = TEST_FOLDER
        TaskManager.LOGGER.setLevel(logging.WARNING)
        self.p = MyProject()
        self.p2 = MyProject2()

    def tearDown(self):
        if os.path.exists(TaskManager.OUTPUT_FOLDER):
            shutil.rmtree(TaskManager.OUTPUT_FOLDER)

    def reset(self):
        self.tearDown(); self.setUp()

    def testParseTasks(self):
        def check_parse(s, expected):
            got = self.p.parse_tasks(s.split(" "))
            self.p.check_tasks_exist(got)
            self.assertEquals(got, expected)            

        F = FLAG_DEFAULT
        T = FLAG_NOCACHE
        S = FLAG_SHOWRESULT
        NS = FLAG_NOCACHE | FLAG_SHOWRESULT

        check_parse("task1 task2 task3",
                    [("task1", [], F), ("task2", [], F), ("task3", [], F)])

        # F means force ("no cache")
        check_parse("task1 task2[F] task3",
                    [("task1", [], F), ("task2", [], T), ("task3", [], F)])

        # S means "show results to stdout"
        check_parse("task1 task2[S] task3",
                    [("task1", [], F), ("task2", [], S), ("task3", [], F)])

        check_parse("task1 task2[F,S] task3",
                    [("task1", [], F), ("task2", [], NS), ("task3", [], F)])

        check_parse("task1:10,15 task2 task3",
                    [("task1", ['10','15'], F), ("task2", [], F), 
                     ("task3", [], F)])

        check_parse("task1[S,F]:10,15 task2 task3",
                    [("task1", ['10','15'], NS), ("task2", [], F), 
                     ("task3", [], F)])

        check_parse("task1: task2 task3",
                    [("task1", [], F), ("task2", [], F), ("task3", [], F)])

        self.assertRaises(TaskManagerError, check_parse, 
                         "task1 toto task3", [])

    def testRun(self):
        def run(command):
            """ 
            Run all tasks (implicit and explicit) and return
            the results in a list
            """
            return list(self.p.run_command(command.split(" ")))

        self.assertRaises(TaskManagerError, run, "toto titi")

        self.assertEqual(run("task1"), [25])
        self.assertEqual(run("task1:11"), [26])
        self.assertEqual(run("task1:11,12"), [23])
        self.assertRaises(TaskError, run, "task1:blabla")
        # duplicates are not allowed
        self.assertEqual(run("task1 task1"), [25])

        self.assertEqual(run("task2"), [25, 12])
        self.assertEqual(run("task1 task2"), [25, 12])
        self.assertEqual(run("task1:11 task2"), [26, 13])
        self.assertEqual(run("task1:11,12 task2"), [23, 11])

        self.assertEqual(run("task3"), [25, 12, 36])
        self.assertEqual(run("task2 task3"), [25, 12, 36])
        self.assertEqual(run("task1 task2 task3"), [25, 12, 36])
        self.assertEqual(run("task1:11 task2 task3"), [26, 13, 39])
        self.assertEqual(run("task1:11,12 task2 task3"), [23, 11, 33])
        self.assertEqual(run("task1 task3"), [25, 12, 36])
        self.assertEqual(run("task1:11 task3"), [26, 13, 39])
        self.assertEqual(run("task1:11,12 task3"), [23, 11, 33])

        self.assertEqual(run("task4"), [10.0])
        self.assertRaises(TypeError, run, "task4:blabla")
        
        # FIXME: this test should pass but is not supported currently
        # self.assertEqual(run("task1 task4 task3"), [25, 10.0, 12, 36])

        t5res = run("task5")[-1]
        self.assertEqual(t5res.__class__, np.ndarray)
        # cache
        self.assertTrue(np.array_equal(t5res, run("task5")[-1])) 
        # nocache
        self.assertFalse(np.array_equal(t5res, run("task5[F]")[-1]))

        res = run("task6")[-1]
        self.assertEqual(res.__class__, tuple)
        self.assertEqual(len(res), 3)

        t7res = run("task7")[0]
        self.assertTrue(isinstance(t7res, int))
        self.assertNotEqual(t7res, run("task7")[0]) # test nocache

        t8res = run("task8:str")[0]
        self.assertTrue(isinstance(t8res, int))

        t9res = run("task9:.")[0]
        self.assertEquals(t9res[0], './taskmanager.py')
        self.assertEquals(t9res, run("task9:.")[0]) # test cache
        self.assertNotEqual(t9res, run("task9[F]:.")[0]) # test nocache

        t10res = run("task10:tests.py")[0]
        self.assertEquals(t10res[0].strip(), "# -*- coding: utf-8 -*-")
        self.assertEquals(t10res, run("task10:tests.py")[0])
        self.assertNotEqual(t10res, run("task10[F]:tests.py")[0])

        self.assertEqual(run("task11"), ["MyProject"])
        self.p.get_task("task11").task11_utility = lambda x: "NewResult"
        # FIXME: the following test should pass (need inlining)
        # self.assertEqual(run("task11"), ["NewResult"])

    def testRunWithInheritance(self):
        def run(proj, command):
            return list(proj.run_command(command.split(" ")))

        # results are different even though inputs are the same because
        # task3 was redefined in MyProject2
        self.assertEqual(run(self.p, "task3"), [25, 12, 36])
        self.assertEqual(run(self.p2, "task3"), [25, 12, 24])

        t5res = run(self.p, "task5")[-1]
        self.assertEqual(t5res.__class__, np.ndarray)
        t5res2 = run(self.p2, "task5")[-1]
        self.assertEqual(t5res2.__class__, np.ndarray)

        # task5 was not implemented in MyProject2 so MyProject's one
        self.assertTrue(np.array_equal(t5res, t5res2))

        self.assertEqual(run(self.p, "task11"), ["MyProject"])
        # FIXME: the following test should pass (need inlining)
        # self.assertEqual(run(self.p2, "task11"), ["MyProject2"])

    def testRunWithoutClass(self):
        self.assertEqual(functask1(), 10)
        res = functask2(10)
        self.assertTrue(np.array_equal(res, functask2(10)))
        res = functask3(10)
        self.assertFalse(np.array_equal(res, functask3(10)))

    def testRunTasks(self):
        def run(command, tasks):
            return run_command(command.split(" "), tasks)        

        self.assertEquals(run("functask1", [functask1, functask2]), [10])
        res = run("functask2", [functask1, functask2])
        res2 = run("functask2", [functask1, functask2])
        self.assertTrue(np.array_equal(res[-1], res2[-1]))

    def testTaskList(self):
        self.assertEquals(len(self.p.get_task_list()), 12)
        self.assertEquals(len(self.p2.get_task_list()), 12)

class TaskTest(unittest.TestCase):
    def setUp(self):
        TaskManager.OUTPUT_FOLDER = TEST_FOLDER
        TaskManager.LOGGER.setLevel(logging.WARNING)
        self.p = MyProject()
        self.p2 = MyProject2()

    def tearDown(self):
        if os.path.exists(TaskManager.OUTPUT_FOLDER):
            shutil.rmtree(TaskManager.OUTPUT_FOLDER)
        
    def testTaskFuncs(self):
        for task in ("task1", "task2", "task3", "task4"):
            taskobj = self.p.get_task(task)
            self.assertTrue(isinstance(taskobj, Task))
            #self.assertTrue(isinstance(taskobj.get_func(), MethodType))

    def testTaskNames(self):
        for task in ("task1", "task2", "task3", "task4"):
            taskobj = self.p.get_task(task)
            self.assertEquals(taskobj.get_name(), task)

    def testGetTaskDependencies(self):
        t1 = self.p.get_task("task1")
        t2 = self.p.get_task("task2")        
        t3 = self.p.get_task("task3")
        t4 = self.p.get_task("task4")
        t5 = self.p.get_task("task5")
        t6 = self.p.get_task("task6")

        self.assertEquals(t1.get_task_dependencies(recursive=False), [])
        self.assertEquals(t2.get_task_dependencies(recursive=False), [t1])
        self.assertEquals(t3.get_task_dependencies(recursive=False), [t2])
        self.assertEquals(t4.get_task_dependencies(recursive=False), [])
        self.assertEquals(t5.get_task_dependencies(recursive=False), [t4, t3])
        self.assertEquals(t6.get_task_dependencies(recursive=False), [t5, t2])
      
        self.assertEquals(t1.get_task_dependencies(), [])
        self.assertEquals(t2.get_task_dependencies(), [t1])
        self.assertEquals(t3.get_task_dependencies(), [t1, t2])
        self.assertEquals(t4.get_task_dependencies(), [])
        self.assertEquals(t5.get_task_dependencies(), [t4, t1, t2, t3])
        self.assertEquals(t6.get_task_dependencies(), [t4, t1, t2, t3, t5])

    def testFilterArgs(self):
        t1 = self.p.get_task("task1")
        self.assertEquals(t1.filter_args(["10", "11"]), [10, 11])

        t4 = self.p.get_task("task4")
        self.assertEquals(t4.filter_args([]), [])

        t5 = self.p.get_task("task5")
        o1 = object(); o2 = object()
        self.assertEquals(t5.filter_args([o1, o2]), [o1, o2])
        self.assertEquals(t5.filter_args([o1, o2, "0.2"]), [o1, o2, 0.2])

    def testExecuteTasksSeparetely(self):
        task1 = self.p.get_task("task1")
        self.assertEquals(task1(), 25)
        self.assertEquals(task1(30, 10), 40)
        self.assertEquals(task1(param1=30, param2=10), 40)

    def testGetFileName(self):
        t2 = self.p.get_task("task2")
        t1 = self.p.get_task("task1")
        t4 = self.p.get_task("task4")

        # check that filenames remain unique
        self.assertEquals(t2.get_filename("test"), t2.get_filename("test"))
        self.assertEquals(t2.get_filename(5), t2.get_filename(5))
        self.assertEquals(t2.get_filename(5), t2.get_filename(5))
        self.assertNotEqual(t2.get_filename(5, "test"), t2.get_filename(5))
        self.assertEquals(t2.get_filename(5, "test"), t2.get_filename(5,"test"))
        self.assertNotEqual(t2.get_filename(5, "test"), t2.get_filename(5))
        
        arr1 = np.array([1,2,3,4])
        arr2 = np.array([1,2,3,4])
        self.assertEquals(t2.get_filename(arr1), t2.get_filename(arr2))
        self.assertNotEqual(t1.get_filename(arr1), t2.get_filename(arr2))

        # test for task with no arguments
        self.assertEquals(t4.get_filename(), t4.get_filename())

    def testCache(self):
        t5 = self.p.get_task("task5")
        t7 = self.p.get_task("task7")
        t8 = self.p.get_task("task8")

        # task5 generates a matrix with random contents so if cache works
        # we should get twice the sames matrix
        self.assertTrue(np.array_equal(t5(10, 4), t5(10, 4)))

        self.assertTrue(t7.nocache)
        self.assertTrue(t8.nocache)
        self.assertNotEqual(t7(), t7())
        self.assertNotEqual(t8(10), t8(10))

    def testCustomFiler(self):
        t12 = self.p.get_task("task12")
        self.assertEquals(t12("test"), "testtest")
        self.assertEquals(t12(), "blablablabla")

class UtilsTest(unittest.TestCase):
    def setUp(self):
        TaskManager.OUTPUT_FOLDER = TEST_FOLDER
        TaskManager.LOGGER.setLevel(logging.WARNING)
        self.p = MyProject()
        self.p2 = MyProject2()

    def tearDown(self):
        if os.path.exists(TaskManager.OUTPUT_FOLDER):
            shutil.rmtree(TaskManager.OUTPUT_FOLDER)
        
    def testRemoveDuplicates(self):
        t1 = self.p.get_task("task1")
        t2 = self.p.get_task("task2")        
        t3 = self.p.get_task("task3")
        t4 = self.p.get_task("task4")
        t5 = self.p.get_task("task5")
        t6 = self.p.get_task("task6")

        f = lambda x: x.get_name()

        self.assertEquals(remove_duplicates([t2, t4, t3, t1, t4, t3], f),
                          [t2, t4, t3, t1])

        self.assertEquals(remove_duplicates([2, 4, 3, 1, 4, 3]),
                          [2, 4, 3, 1])

    def testExecuteTasksSeparetely(self):
        t1 = self.p.get_task("task1")
        self.assertEquals(t1(), 25)
        self.assertEquals(t1(30, 10), 40)
        self.assertEquals(t1(param1=30, param2=10), 40)
        self.assertEquals(t1(0), 15)
        self.assertEquals(t1(param2=0), 10)
        self.assertRaises(TypeError, t1, 30, 10, 40) # incorrect num of args    
  

    def testGetAllFuncArgs(self):
        t1 = self.p.get_task("task1")
        t1func = t1.get_func()

        self.assertEquals(get_all_func_args(self.p, t1func), 
                          [("param1", 10), ("param2", 15)])

        self.assertEquals(get_all_func_args(self.p, t1func, 12), 
                          [("param1", 12), ("param2", 15)])

        self.assertEquals(get_all_func_args(self.p, t1func, 12, 13), 
                          [("param1", 12), ("param2", 13)])

        self.assertEquals(get_all_func_args(self.p, t1func, 
                                            param1=12, param2=13), 
                          [("param1", 12), ("param2", 13)])

        self.assertEquals(get_all_func_args(self.p, t1func, 
                                            param2=12, param1=13), 
                          [("param1", 13), ("param2", 12)])

        self.assertEquals(get_all_func_args(self.p, t1func, 12, param2=13), 
                          [("param1", 12), ("param2", 13)])

        t2 = self.p.get_task("task2")
        t2func = t2.get_func()
        # missing args
        self.assertRaises(TypeError, get_all_func_args, self.p, t2func)

    def testPairListToDict(self):
        d = pair_list_to_dict([(1,2), (3,4)])
        self.assertEquals(len(d), 2)
        self.assertEquals(d[1], 2)
        self.assertEquals(d[3], 4)

        self.assertEquals(pair_list_to_dict([]), {})

        t1 = self.p.get_task("task1")
        t2 = self.p.get_task("task2")        
        t3 = self.p.get_task("task3")

        d = pair_list_to_dict([(t1, 1), (t2, 2), (t3, 3)],
                              lambda x: x.get_name())
        self.assertEquals(len(d), 3)
        self.assertEquals(d["task1"], 1)
        self.assertEquals(d["task2"], 2)
        self.assertEquals(d["task3"], 3)
        

    def testDirectory(self):
        d = directory("t*.py")
        d2 = directory("te*.py")

        self.assertTrue(d != d2)
        self.assertEquals(sorted(d(".").get_files()), 
                         sorted(['./taskmanager.py', './tests.py']))
        self.assertEquals(d2(".").get_files(),
                          ['./tests.py'])

        self.assertEquals(d(".").hash(), d(".").hash())
        self.assertEquals(d2(".").hash(), d2(".").hash())

    def testSaveLoadObject(self):
        arr = [1,2,3,4,5]
        arrpath = os.path.join(TEST_FOLDER, "test")

        # test not compressed pickle
        arrpathext = save_object(arrpath, arr)
        self.assertEquals(arr, load_object(arrpathext))

        # test compressed pickle
        arrpathext = save_object(arrpath, arr, GZIP_COMPRESSED)
        self.assertEquals(arr, load_object(arrpathext))

        arr = np.array(arr)

        # test not compressed numpy
        arrpathext = save_object(arrpath, arr)
        self.assertTrue(np.array_equal(arr, load_object(arrpathext)))

        # test compressed numpy
        arrpathext = save_object(arrpath, arr, GZIP_COMPRESSED)
        self.assertTrue(np.array_equal(arr, load_object(arrpathext)))

        # test list store
        arr = ListStore(range(1000))
        arrpathext = save_object(arrpath, arr)
        self.assertEquals(arr, load_object(arrpathext))
        

    def testGetClassDefiningAttr(self):
        self.assertEquals(get_class_defining_attr(self.p2, "task3"), MyProject2)
        self.assertEquals(get_class_defining_attr(self.p2, "task5"), MyProject)

    def testListSplit(self):
        self.assertEquals(list_split(range(10), 2), 
                          [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]])
        self.assertEquals(list_split(range(10), 3), 
                          [[0, 1, 2, 3], [4, 5, 6], [7, 8, 9]])
        self.assertEquals(list_split(range(10), 1), [range(10)])

def mysqrt(i):
    return sqrt(i)

def mypow(a, b):
    return pow(a, b)

mysqrt_delayed = delayed(mysqrt)
mypow_delayed = delayed(mypow)

mysqrt_parallel = parallelized(mysqrt)
mypow_parallel = parallelized(mypow)

class ParallelTest(unittest.TestCase):

    SQRT = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
    POW = [0, 1, 8, 27, 64, 125, 216, 343, 512, 729]

    def _s(self, value):
        self.assertEquals(value, self.SQRT)

    def _p(self, value):
        self.assertEquals(value, self.POW)    

    def testPoolMap(self):
        # with list
        self._s(pool_map(mysqrt, [i**2 for i in range(10)], njobs=4))
        self._s(pool_map_seq(mysqrt, [i**2 for i in range(10)], njobs=4))
        # with generator
        self._s(pool_map(mysqrt, (i**2 for i in range(10)), njobs=4))
        self._s(pool_map_seq(mysqrt, (i**2 for i in range(10)), njobs=4))

    def testPoolZippedMap(self):
        # with list
        self._p(pool_zipped_map(mypow, [(i,3) for i in range(10)], njobs=4))
        self._p(pool_zipped_map_seq(mypow, [(i,3) for i in range(10)], njobs=4))
        # with generator
        self._p(pool_zipped_map(mypow, ((i,3) for i in range(10)), njobs=4))
        self._p(pool_zipped_map_seq(mypow, ((i,3) for i in range(10)), njobs=4))

    def testPoolParallelize(self):
        # with list
        self._s(pool_parallelize([mysqrt_delayed(i**2) for i in range(10)],
                                 njobs=4))
        self._p(pool_parallelize([mypow_delayed(i, 3) for i in range(10)],
                                 njobs=4))
        self._s(pool_sequentialize([mysqrt_delayed(i**2) for i in range(10)],
                                   njobs=4))
        self._p(pool_sequentialize([mypow_delayed(i, 3) for i in range(10)],
                                   njobs=4))
        # with generator
        self._s(pool_parallelize((mysqrt_delayed(i**2) for i in range(10)),
                                 njobs=4))
        self._p(pool_parallelize((mypow_delayed(i, 3) for i in range(10)),
                                 njobs=4))
        # with chunksize
        self._s(pool_parallelize([mysqrt_delayed(i**2) for i in range(10)],
                                  chunksize=4, njobs=4))
        self._p(pool_parallelize([mypow_delayed(i, 3) for i in range(10)],
                                  chunksize=4, njobs=4))


    def testParallelized(self):
        # with list
        self._s(mysqrt_parallel([i**2 for i in range(10)], njobs=4))
        self._s(mysqrt_parallel([(i**2,) for i in range(10)], njobs=4))
        self._p(mypow_parallel([(i, 3) for i in range(10)], njobs=4))
        # with generator
        self._s(mysqrt_parallel((i**2 for i in range(10)), njobs=4))
        self._s(mysqrt_parallel(((i**2,) for i in range(10)), njobs=4))
        self._p(mypow_parallel(((i, 3) for i in range(10)), njobs=4))
        # with chunksize
        self._s(mysqrt_parallel([i**2 for i in range(10)],chunksize=2,njobs=4))
        self._p(mypow_parallel([(i, 3) for i in range(10)],
                               chunksize=2,njobs=4))

class TestListStore(unittest.TestCase):

    def testListStore(self):
        l = ListStore()
        
        # append
        l.append(1)
        l.append(2)

        self.assertEquals(l[0], 1)
        self.assertEquals(l[1], 2)
        self.assertEquals(list(l), [1,2])

        # setitem
        l[1] = 3

        self.assertEquals(l[0], 1)
        self.assertEquals(l[1], 3)
        self.assertEquals(list(l), [1,3])

        # len
        self.assertEquals(len(l), 2)

        # IndexError
        self.assertRaises(IndexError, l.__getitem__, 2)
        self.assertRaises(IndexError, l.__setitem__, 2, 4)
        self.assertRaises(IndexError, l.__delitem__, 2)

        # delitem
        del l[1]
        self.assertEquals(len(l), 1)
        self.assertEquals(l[0], 1)

    def testEmpty(self):
        l = ListStore()
        self.assertEquals(list(l), [])

    def testFromOtherList(self):
        for l in (ListStore([1,2]), ListStore(1,2)):
            self.assertEquals(l[0], 1)
            self.assertEquals(l[1], 2)
            self.assertEquals(list(l), [1,2])
            self.assertEquals(len(l), 2)

    def testLoadSave(self):
        l = ListStore([1,2])

        if not os.path.exists(TEST_FOLDER): os.makedirs(TEST_FOLDER)

        path = os.path.join(TEST_FOLDER, "test.lst")

        l.save(path)
        
        l2 = ListStore()
        l2.open(path)

        self.assertEquals(l, l2)
        self.assertEquals(list(l2), [1,2])

    def testAdd(self):
        l = ListStore([1,2,3])
        l2 = ListStore([4,5,6])
        self.assertEquals(ListStore([1,2,3,4,5,6]), l+l2)

    def testPickle(self):
        l = ListStore([1,2,3])
        data = pickle.dumps(l)
        l2 = pickle.loads(data)
        self.assertEquals(l, l2)

    def testSlice(self):
        l = ListStore(range(10))
        self.assertEquals(l[0:3], range(10)[0:3])
        self.assertEquals(l[:3], range(10)[:3])
        self.assertEquals(l[0:], range(10)[0:])
        self.assertEquals(l[:-2], range(10)[:-2])
        self.assertEquals(l[:-2:2], range(10)[:-2:2])
        self.assertEquals(l[2:8:2], range(10)[2:8:2])

    def testToList(self):
        l = ListStore(range(10))
        l2 = list(l)
        self.assertEquals(l, l2)

class TestKeyListStore(unittest.TestCase):

    def testKeyListStore(self):
        l = KeyListStore()
        
        l['toto'] = [1, 2, 3]
        l['titi'] = [2, 3, 4]
        l['tutu'] = []

        self.assertEquals(l['toto'], [1, 2, 3])
        self.assertEquals(l['titi'], [2, 3, 4])
        self.assertEquals(l['tutu'], [])    

        self.assertEquals(len(l), 3)

        l['titi'] = [5, 6, 7, 8]
        self.assertEquals(l['titi'], [5, 6, 7, 8])

        keys = sorted(l.keys())
        self.assertEquals(keys, ["titi", "toto", "tutu"])

        values = l.values()
        for v in values:
            self.assertTrue(v in [[1, 2, 3], [5, 6, 7, 8], []])

        del l['tutu']
        del l['titi']

        self.assertRaises(KeyError, l.__getitem__, 'tutu')
        self.assertRaises(KeyError, l.__getitem__, 'titi')
        self.assertEquals(['toto'], l.keys())

        l.append_item('toto', 4)
        self.assertEquals(l['toto'], [1, 2, 3, 4])

        self.assertEquals(l.get_item('toto', 1), 2)
        self.assertRaises(IndexError, l.get_item, 'toto', 4)

        self.assertEquals(l.get_n_items("toto"), 4)

        l.del_item("toto", 3)

        l.set_item('toto', 1, 3)
        self.assertEquals(l.get_item('toto', 1), 3)
       

    def testFromOtherDict(self):
        for l in (KeyListStore({"test": [1,2,3]}), 
                  KeyListStore(test=[1,2,3])):

            self.assertEquals(l.keys(), ["test"])
            self.assertEquals(l["test"], [1,2,3])

    def testLoadSave(self):
        l = KeyListStore({"test": [1,2,3]})

        if not os.path.exists(TEST_FOLDER): os.makedirs(TEST_FOLDER)

        path = os.path.join(TEST_FOLDER, "test.klst")

        l.save(path)
        
        l2 = KeyListStore()
        l2.open(path)

        self.assertEquals(l, l2)

    def testPickle(self):
        l = KeyListStore({"toto":[1,2,3]})
        data = pickle.dumps(l)
        l2 = pickle.loads(data)
        self.assertEquals(l, l2)

    def testToDict(self):
        l = KeyListStore({"test": [1,2,3]})
        l2 = dict(l)
        self.assertEquals(l, l2)

        

if __name__ == "__main__":
    unittest.main()