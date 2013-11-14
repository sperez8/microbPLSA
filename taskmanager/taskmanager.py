# -*- coding: utf-8 -*-

# Copyright (c) 2009 Mathieu Blondel
# BSD license

import hashlib
from functools import wraps, update_wrapper
from types import FunctionType
import cPickle as pickle
from glob import glob
import os
import time
from gzip import GzipFile
import logging
import sys
import tempfile
import sqlite3
import shutil
import base64
import datetime

import numpy as np

HASH_METHOD = "sha1"

NOT_COMPRESSED = 0
GZIP_COMPRESSED = 1

FLAG_DEFAULT = 0
FLAG_NOCACHE = 1
FLAG_SHOWRESULT = 2

PICKLE_PROTOCOL = pickle.HIGHEST_PROTOCOL

########################################
# List utils...
########################################

def remove_duplicates(l, func=lambda x:x):
    """
    Remove duplicates from a list and preserve order.
    Elements from the list must be hashable.
    """
    d = {}
    ret = []
    for e in l:
        k = func(e)
        if not k in d:
            ret.append(e)
            d[k] = 1
    return ret

def pair_list_to_dict(pl, func=lambda x:x):
    d = {}

    for e in pl:
        if len(e) == 2:
            d[func(e[0])] = e[1]
        else:
            d[func(e[0])] = e[1:]

    return d

def list_split(seq, p):
    """ split seq in p lists of about the same size """
    newseq = []
    n = len(seq) / p    # min items per subsequence
    r = len(seq) % p    # remaindered items
    b,e = 0, n + min(1, r)  # first split
    for i in range(p):
        newseq.append(seq[b:e])
        r = max(0, r-1)  # use up remainders
        b,e = e, e + n + min(1, r)  # min(1,r) is always 0 or 1

    return newseq

########################################
# Misc utils...
########################################

def separator(sep="-", size=80):
    return sep * size

########################################
# Hash utils...
########################################

def get_str_hash(s):
    m = hashlib.new(HASH_METHOD)
    m.update(s)
    return m.hexdigest()

def get_file_hash(f):
    offs = f.tell()
    f.seek(0)
    res = get_str_hash(f.read())
    f.seek(offs)
    return res

def get_general_hash(obj):
    tmpfile = tempfile.TemporaryFile("w+")
    save_object(tmpfile, obj)
    return get_file_hash(tmpfile)

def get_pickle_hash(obj):
    tmpfile = tempfile.TemporaryFile("w+")
    pickle.dump(obj, tmpfile, PICKLE_PROTOCOL)
    return get_file_hash(tmpfile)

HASH_CACHE = {} # object-id => hash

def get_hash_key(obj):
    #return (id(obj), repr(obj))
    return id(obj)

def set_hash_cache(obj, hashvalue):
    HASH_CACHE[get_hash_key(obj)] = hashvalue

def has_hash_cache(obj):
    return get_hash_key(obj) in HASH_CACHE

def get_hash_cache(obj):
    return HASH_CACHE[get_hash_key(obj)]

def get_hash(obj):
    if has_hash_cache(obj):
        return get_hash_cache(obj)
    elif hasattr(obj, "hash"):
        # __hash__ returns ints and serves another purpose
        return obj.hash()
    elif isinstance(obj, file):
        return get_file_hash(obj)
    elif isinstance(obj, str):
        return get_str_hash(obj)
    else:
        return get_general_hash(obj)

########################################
# Object load/save utils...
########################################

def read_file(path):
    f = open(path)
    ret = f.read()
    f.close()
    return ret

def save_file(path, s, mode="w"):
    f = open(path, mode)
    f.write(s)
    f.close()

def load_object(path):
    def cache_hash(obj):
        set_hash_cache(obj, get_file_hash(open(path)))
        return obj

    # FIXME: create a system to add custom object loader,saver and hasher.

    if path.endswith(".lst"):
        store = ListStore()
        store.open(path)
        return cache_hash(store)
    elif path.endswith(".klst"):
        store = KeyListStore()
        store.open(path)
        return cache_hash(store)
    elif path.endswith(".npy"):
        return cache_hash(np.load(path))
    elif path.endswith(".npz"):
        npz = np.load(path)
        return cache_hash(npz[npz.files[0]])
    elif path.endswith(".pp"):
        f = open(path)
        try:
            return cache_hash(pickle.load(f))
        finally:
            f.close()
    elif path.endswith(".ppz"):
        f = GzipFile(path)
        try:
            return cache_hash(pickle.load(f))
        finally:
            f.close()
    else:
        raise ValueError, "Unknown file extension"

def save_object(f, obj, compression=NOT_COMPRESSED):
    """f can be either a string or a file"""
    def append_ext(p, ext):
        if not p.endswith(ext):
            p += ext
        return p

    if isinstance(f, file):
        path = None
    else:
        make_path_dirname(f)

        if isinstance(obj, ListStore):
            path = append_ext(f, ".lst")
        elif isinstance(obj, KeyListStore):
            path = append_ext(f, ".klst")

        elif isinstance(obj, np.ndarray):
            if compression == NOT_COMPRESSED:
                path = append_ext(f, ".npy")
            else:
                path = append_ext(f, ".npz")
        else:
            if compression == NOT_COMPRESSED:
                path = append_ext(f, ".pp") # python pickle
            else:
                path = append_ext(f, ".ppz")

        f = open(path, "w+")


    if isinstance(obj, Store):
        obj.save(f.name)
    elif isinstance(obj, np.ndarray):
        if compression == NOT_COMPRESSED:
            np.save(f, obj)
        else:
            np.savez(f, obj)
    else:
        if compression == NOT_COMPRESSED:
            pickle.dump(obj, f, PICKLE_PROTOCOL)
        else:
            gz = GzipFile(mode="w", fileobj=f)
            pickle.dump(obj, gz, PICKLE_PROTOCOL)
            gz.close()

    set_hash_cache(obj, get_file_hash(f))

    if path is not None:
        f.close()

    return path

########################################
# Path utils...
########################################

def touch(path):
    """ Like UNIX command """
    f = open(path, "w")
    f.close()

def make_path_dirname(path):
    dirname = os.path.dirname(path)

    if not os.path.exists(dirname):
        os.makedirs(dirname)

def wait_until_released(path, check_time=5):
    """ Wait until the file is released by other programs using it"""

    # FIXME: rewrite using inotify or kqueue?
    #        how about Windows?
    f = os.popen("lsof +r %d %s" % (check_time, path))
    return f.read()

def recursive_glob(path):
    def getdirs(d):
        return [p for p in glob(d) if os.path.isdir(p)]

    ret = []

    dirname = os.path.dirname(path)
    basename = os.path.basename(path)

    for d in getdirs(dirname):
        for d2 in getdirs(os.path.join(d, "*")):
            ret += recursive_glob(os.path.join(d2, basename))

        for f in glob(os.path.join(d, basename)):
            ret.append(f)

    return remove_duplicates(ret)

########################################
# Function/Class utils...
########################################

#import inspect
#import ast
#def get_inlined_source(func, obj=None):
#    src = inspect.getsource(func)
#    tree = ast.parse(src)
#    print ast.dump(tree)

def get_func_source(func):
    # FIXME: use the ast to inline functions used by func (when possible)
    return func.func_code.co_code

def get_func_args(func):
    n_args = func.func_code.co_argcount
    func_args = func.func_code.co_varnames
    return func_args[0:n_args]

def get_all_func_args(obj, func, *args, **kw):
    """
    Return the full list of arguments and their values.
    Arguments and named arguments can be mixed.
    Missing arguments are replaced by their default values.

    obj: the original object ("self") func was called on or None if function
    """
    name = func.func_name
    n_args = func.func_code.co_argcount

    func_args = func.func_code.co_varnames[0:n_args]

    if obj is not None:
    #if len(func_args) > 0 and func_args[0] == "self":
        # skip self
        func_args = func_args[1:]

    dflt_args = func.func_defaults

    mykw = {}

    # process *args
    if len(args) > len(func_args):
        raise TypeError, "Too many arguments to %s" % name

    for i, arg in enumerate(args):
        mykw[func_args[i]] = arg

    # use default args if there are missing args
    if len(mykw) < n_args and dflt_args:
        for i, arg in enumerate(reversed(dflt_args)):
            k = func_args[-(i+1)]
            if not k in mykw:
                mykw[k] = arg

    # process **kw
    mykw.update(kw)

    try:
        return [(arg, mykw[arg]) for arg in func_args]
    except KeyError, e:
        raise TypeError, "Missing argument (%s)" % str(e)

def get_class_defining_attr(obj, attr):
    for klass in obj.__class__.__mro__:
        if attr in klass.__dict__:
            return klass
    return None

def proxy_method(obj, method):
    def wrapper(*args, **kw):
        return getattr(obj, method)(*args[1:], **kw)
    return wrapper

########################################
# Types...
########################################

def directory(ext="*", recursive=True):
    class Directory(object):
        EXT = ext
        RECURSIVE = recursive

        def __init__(self, path):
            self._path = path

        def get_files(self):
            if not self.RECURSIVE:
                return glob(os.path.join(self._path, self.EXT))
            else:
                return recursive_glob(os.path.join(self._path, self.EXT))

        def hash(self):
            digest = ""
            for f in self.get_files():
                digest += get_hash(file(f))
            return get_hash(digest)

    return Directory

def boolean(s):
    try:
        return bool(int(s))
    except:
        return True

########################################
# Stores...
########################################

def adapt_object(obj):
    return base64.b64encode(pickle.dumps(obj))

def convert_object(data):
    return pickle.loads(base64.b64decode(data))

def unpickle_store(cls, data):
    f = tempfile.NamedTemporaryFile()
    f.write(base64.b64decode(data))
    store = cls()
    store.open(f.name)
    return store

class Store(object):

    def __init__(self):
        self._f = tempfile.NamedTemporaryFile()
        self.open()

    def open(self, path=None):
        if path is not None:
            shutil.copy(path, self._f.name)

        self._con = sqlite3.connect(self._f.name)
        self._con.text_factory = str
        self._c = self._con.cursor()

        if not self._has_tables():
            self._create_tables()

    def _e(self, req, *a, **kw):
        #print req, a, kw
        return self._c.execute(req, *a, **kw)

    def _em(self, req, *a, **kw):
        #print req, a, kw
        return self._c.executemany(req, *a, **kw)

    def _fo(self):
        return self._c.fetchone()

    def _fa(self):
        return self._c.fetchall()

    def _efo(self, req, *a, **kw):
        self._e(req, *a, **kw)
        return self._fo()

    def _efa(self, req, *a, **kw):
        self._e(req, *a, **kw)
        return self._fa()

    def _has_tables(self):
        self._e("SELECT count(type) FROM sqlite_master WHERE type = 'table'")
        return self._fo()[0] > 0

    def save(self, path):
        self._con.commit()
        shutil.copy(self._f.name, path)

    def __reduce__(self):
        self._con.commit()
        f = open(self._f.name)
        data = base64.b64encode(f.read())
        f.close()
        return (unpickle_store, (self.__class__, data))

class KeyListStore(Store):

    """
    Efficient persistent storage of key/list pairs.
    """

    def __init__(self, *args, **kw):
        Store.__init__(self)

        self._KEY_IDS = {}

        if len(args) == 1 and isinstance(args[0], dict):
            initial_dict = args[0]
        else:
            initial_dict = kw

        # FIXME: can be done without a loop
        for key, items in initial_dict.items():
            if not isinstance(items, list):
                raise ValueError, "KeyListStore takes lists as values"
            self[key] = items

    def _create_tables(self):
        self._c.executescript("""
CREATE TABLE keys(
  keyid    INTEGER PRIMARY KEY,
  key      TEXT
);

CREATE TABLE items(
  itemid     INTEGER PRIMARY KEY,
  keyid      INTEGER REFERENCES keys,
  item       BLOB
);

CREATE INDEX items_keyid_index ON items(keyid);
""")

    def _update_key_ids(self):
        self._KEY_IDS = {}
        for row in self._efa("SELECT * FROM keys ORDER BY keyid"):
            self._KEY_IDS[row[1]] = row[0]

    def open(self, *args, **kw):
        Store.open(self, *args, **kw)
        self._update_key_ids()

    def __getitem__(self, key):
        return list(self.get_item_gen(key))

    def get_item_gen(self, key):
        keyid = self._KEY_IDS[key]

        c = self._con.cursor()
        c.execute("SELECT item FROM items WHERE keyid=? ORDER BY itemid",
                  (keyid,))

        return (convert_object(r[0]) for r in c)

    def __len__(self):
        return len(self._KEY_IDS)

    def __setitem__(self, key, items):
        try:
            keyid = self._KEY_IDS[key]
        except KeyError:
            self._e("INSERT INTO keys (key) VALUES (?)", (key,))
            keyid = self._c.lastrowid
            self._KEY_IDS[key] = keyid

        self._e("DELETE FROM items WHERE keyid=?", (keyid,))

        items = ((keyid, adapt_object(item)) for item in items)
        self._em("INSERT INTO items (keyid,item) VALUES(?,?)", items)

    def __delitem__(self, key):
        keyid = self._KEY_IDS[key]
        self._e("DELETE FROM items WHERE keyid=?", (keyid,))
        self._e("DELETE FROM keys WHERE keyid=?", (keyid,))
        del self._KEY_IDS[key]

    def keys(self):
        return self._KEY_IDS.keys()

    def values(self):
        return [self[k] for k in self.keys()]

    def items(self):
        return zip(self.keys(), self.values())

    def __iter__(self):
        return iter(self._KEY_IDS)

    def _get_item_id(self, key, idx):
        keyid = self._KEY_IDS[key]

        l = self.get_n_items(key)

        if idx > l - 1:
            raise IndexError

        return self._efo("""SELECT itemid FROM items
WHERE keyid=? ORDER BY itemid LIMIT 1 OFFSET ?""", (keyid, idx,))[0]

    def get_item(self, key, idx):
        keyid = self._KEY_IDS[key]

        d = self._efo("""SELECT item FROM items
WHERE keyid=? ORDER BY itemid LIMIT 1 OFFSET ?""", (keyid,idx))

        if d is None: raise IndexError

        return convert_object(d[0])

    def get_item_slice(self, key, sliceobj):
        if sliceobj.stop is None or sliceobj.stop < 0:
            size = self.get_n_items(key)
        else:
            size = sliceobj.stop

        start, stop, step = sliceobj.indices(size)
        limit = stop - start

        keyid = self._KEY_IDS[key]

        rows = self._efa("""SELECT item FROM items
WHERE keyid=? ORDER BY itemid LIMIT ? OFFSET ?""", (keyid,limit,start))

        if step > 1:
            rows = rows[::step]

        return [convert_object(r[0]) for r in rows]

    def set_item(self, key, idx, item):
        idx = self._get_item_id(key, idx)

        d = adapt_object(item)
        self._e("UPDATE items SET item=? WHERE itemid=?", (d, idx))

    def get_n_items(self, key):
        k = self._KEY_IDS[key]
        return self._efo("SELECT COUNT(*) FROM items WHERE keyid=?", (k,))[0]

    def del_item(self, key, idx):
        idx = self._get_item_id(key, idx)
        self._e("DELETE FROM items WHERE itemid=?", (idx,))

    def append_item(self, key, item):
        self.append_items(key, [item])

    def append_items(self, key, items):
        keyid = self._KEY_IDS[key]
        items = [(keyid, adapt_object(item)) for item in items]
        self._em("INSERT INTO items (keyid,item) VALUES (?,?)", items)

    def __eq__(self, othr):
        return dict(self) == dict(othr)

    def __ne__(self, othr):
        return not(self == othr)


class ListStore(KeyListStore):

    """
    Efficient persistent storage of arbitrary list of objects.
    """

    def __init__(self, *args):
        KeyListStore.__init__(self)

        if len(args) == 0:
            initial_list = []
        elif len(args) == 1 and (isinstance(args[0], list) or
                                 isinstance(args[0], list)):

            initial_list = args[0]
        else:
            initial_list = args

        KeyListStore.__setitem__(self, "store", initial_list)

    def __getitem__(self, idx):
        if isinstance(idx, slice):
            return self.get_item_slice("store", idx)
        else:
            return self.get_item("store", idx)

    def __len__(self):
        return self.get_n_items("store")

    def __setitem__(self, idx, item):
        self.set_item("store", idx, item)

    def __delitem__(self, idx):
        self.del_item("store", idx)

    def __iter__(self):
        return self.get_item_gen("store")

    def append(self, item):
        KeyListStore.append_items(self, "store", [item])

    def append_items(self, items):
        KeyListStore.append_items(self, "store", items)

    def __add__(self, othr):
        l = ListStore()
        l.append_items(list(self))
        l.append_items(list(othr))
        return l

    def __eq__(self, othr):
        return list(self) == list(othr)

    def __ne__(self, othr):
        return not(self == othr)

########################################
# Task...
########################################

def task(*args):
    if len(args) == 0:
        raise TaskManagerError, "Too few arguments to task"

    # @task
    if isinstance(args[0], FunctionType):
        func = args[0]
        return Task(func)

    # @task(arg1, arg2, ...)
    else:
        def wrapper(func):
           return Task(func, args)
        return wrapper

# @task
# @nocache
# is equivalent to task(nocache())
def nocache(func):
    func.nocache = True
    return func

def show(func):
    func.show = True
    return func

def inputs(*filenames):
    def wrapper(func):
        func.inputs = filenames
        return func
    return wrapper

def output(filename):
    def wrapper(func):
        func.output = filename
        return func
    return wrapper

class Task(object):

    def __init__(self, func, args=[]):
        self._func = func # the original function
        self._args = args # the decorator arguments (e.g. [Task(), int, int])
        self._obj = None
        self.nocache = func.nocache if hasattr(func, "nocache") else False
        self.inputs = func.inputs if hasattr(func, "inputs") else []
        self.output = func.output if hasattr(func, "output") else None
        self.show = func.show if hasattr(func, "show") else False

    def filter_args(self, args):
        def apply_filter(filt, arg):
            try:
                return filt(arg)
            except ValueError:
                raise TaskError, "Argument %s is not compatible with %s" % \
                                    (arg, filt)

        ret_args = []

        for i, arg in enumerate(args):
            try:
                filt = self._args[i]
            except IndexError:
                break

            if filt == any or filt is None or isinstance(filt, Task):
                ret_args.append(arg)
            else:
                ret_args.append(apply_filter(filt, arg))

        return ret_args

    def get_filename(self, *argvalues):
        """
        Return a unique filename given the task and the arguments
        (we assume the function is deterministic)
        """

        m = hashlib.new(HASH_METHOD)

        # the filename is based on the function source code
        m.update(get_hash(get_func_source(self._func)))

        # the class of the object the task is called on
        #if self._obj:
        #    m.update(get_hash(self._obj.__class__.__name__))

        # and its arguments
        for value in argvalues:
            m.update(get_hash(value))

        if self._obj:
            # task was defined as a method
            klass = get_class_defining_attr(self._obj, self.get_name())
            klass = klass.__name__ + "_"
        else:
            # task was defined as a function
            klass = ""

        return klass + self.get_name() + "_" + m.hexdigest()

    def __call__(self, *args, **kw):
        # manually specified input arguments with @inputs
        if self.inputs:
            def _load(inp):
                inps = glob(inp + "*")
                if len(inps) == 0:
                    raise Exception, "Couldn't find input file %s" % inp
                elif len(inps) > 1:
                    raise Exception, "More than one file found for %s" % inp
                inp = inps[0]
                self.info("Loading inputs %s..." % inp)
                return load_object(inp)

            inputs = map(_load, self.inputs)
            args = tuple(list(inputs) + list(args))

         # retrieve args and keywords as a list of (arg, value) pairs
        allargs = get_all_func_args(self._obj, self._func, *args, **kw)

        # keep only values and apply filters
        argvalues = self.filter_args([a[1] for a in allargs])

        if self.output is not None:
            # a filename was specified, no cache handling
            res = self.run_with_timer(*argvalues)
            fullpath = save_object(self.output, res)
            self.LOGGER.info("File saved to %s." % fullpath)
            return res

        # basepath doesn't contain the extension (.npy, .pp etc) yet
        basepath = os.path.join(TaskManager.OUTPUT_FOLDER,
                                self.get_filename(*argvalues))

        if not self.nocache and os.path.exists(basepath):
            # another process is working on the same task with the same inputs
            # let's wait for it to finish
            self.info("Waiting for other process to finish...")
            wait_until_released(basepath)
            self.info("Other process done!")

        # retrieve the filename with its extension
        match = glob(basepath + ".*")

        if not self.nocache and len(match) > 0 and os.path.exists(match[0]):
            self.info("Cache found!")
            self.LOGGER.info("Cache loaded from %s." % match[0])
            return load_object(match[0])
        else:
            # write this file to let other processes know that
            # this process is already working on the current task
            make_path_dirname(basepath)
            lock = open(basepath, "w")

            res = self.run(*argvalues)

            self.info("Saving result!")
            fullpath = save_object(basepath, res)
            self.LOGGER.info("Cache saved to %s." % fullpath)
            lock.close()
            os.unlink(basepath)

            return res

    def run(self, *args, **kw):
        if self._obj is not None:
            res = self._func(self._obj, *args)
        else:
            res = self._func(*args)
        if self.show:
            print str(res)
        return res

    def run_with_timer(self, *args, **kw):
        self.info("Executing!")
        start = time.time()

        res = self.run(*args)

        diff = time.time() - start
        self.info("Done in %d second(s)." % diff)

        return res

    def __get__(self, obj, type=None):
        # a hack to be able to call func with the self it's bound to
        self._obj = obj
        return self

    #def __call__(self, *args, **kw):
        #return self._func(*args, **kw)

    #def __get__(self, obj, type=None):
        #if obj is None:
            #return self
        ## convert unbound function to method
        #new_func = self._func.__get__(obj, type)
        #return self.__class__(new_func, self._args)

    def __repr__(self):
        return "<Task \"%s\">" % self.get_name()

    #def __eq__(self, othr):
        #return self.get_name() == othr.get_name()

    def get_func(self):
        """ The original function used by the task """
        return self._func

    def get_args(self):
        """ The arguments used in @task(...) """
        return self._args

    def get_name(self):
        return self._func.func_name

    def get_task_dependencies(self, recursive=True):
        if recursive:
            tasks = []
            for task in self.get_task_dependencies(recursive=False):
                tasks += task.get_task_dependencies(recursive=True)
                tasks += [task]
            return remove_duplicates(tasks, lambda x: x.get_name())
        else:
            return [t for t in self._args if isinstance(t, Task)]

########################################
# Task Manager...
########################################

class TaskManager(object):

    OUTPUT_FOLDER = "/tmp/taskmanager/"

    def parse_tasks(self, args, tasksep=":", paramsep=","):
        """
        Returns a list of pairs (task, args)

        where task is the Task object to run
              args are the arguments passed to the command line
        """
        tasks = []

        for arg in args:
            arr = arg.split(tasksep)
            task = arr[0]

            flag = FLAG_DEFAULT
            if task[-1] == "]":
                i = task.index("[")
                options = task[i+1:-1].split(paramsep)
                options = [o.strip().lower() for o in options]
                task = task[0:i]

                if "f" in options:
                    flag |= FLAG_NOCACHE

                if "s" in options:
                    flag |= FLAG_SHOWRESULT

            if len(arr) > 1 and arr[1]:
                params = arr[1].split(paramsep)
            else:
                params = []

            tasks.append((task, params, flag))

        return remove_duplicates(tasks, lambda x: x[0])

    def check_tasks_exist(self, tasks):
        for task_str, args, nocache in tasks:
            if not hasattr(self, task_str):
                raise TaskManagerError, "Task %s doesn't exist" % task_str

    def get_task(self, task_str):
        if not hasattr(self, task_str):
            raise TaskManagerError, "Task %s doesn't exist" % task_str

        task = getattr(self, task_str)

        if not isinstance(task, Task):
            raise TaskManagerError, "%s is not a Task" % task_str

        return task

    def get_task_list(self):
        tasks = []
        for attr in dir(self):
            try:
                tasks.append(self.get_task(attr))
            except TaskManagerError:
                continue
        return tasks

    def get_name(self):
        return self.__class__.__name__

    def do_clear(self, args):
        if len(args) == 0:
            raise TaskManagerError, "Clear needs a task argument " \
                        "(e.g. clear:mytask)"

        pat = "%s_*%s*" % (self.get_name(), args[0])

        for f in glob(os.path.join(self.OUTPUT_FOLDER, pat)):
            os.unlink(f)

    def do_clearall(self):
        pat = "%s_**" % self.get_name()

        for f in glob(os.path.join(self.OUTPUT_FOLDER, pat)):
            os.unlink(f)

    def do_help(self):
        tasks = self.get_task_list()

        if len(tasks) > 0:
            print "Available tasks are:"
            for task in tasks:
                print "- %s" % task.get_name()
            print "\nEnter help:taskname for more help."
        else:
            print "No task available"

        print """
Syntax examples for a project with a task "task2" which depends on "task1":

task2                          # execute task2 and task1 implicitly
task1 task2                    # same as above but run task1 explicitly
task1:param1,param2 task2      # run task1 with specific parameters
task1:param1,param2 task2[F]   # force to re-execute task2 (nocache)
task1:param1,param2 task2[S]   # display the result of task2 when it's done
task1:param1,param2 task2[F,S] # nocache and show result combined

"""

    def do_help_task(self, task):
        task = self.get_task(task)
        print "Task: " + task.get_name() + "\n"
        print "Arguments:"
        for arg in get_func_args(task.get_func()):
            print "- %s" % arg
        doc = task.get_func().__doc__
        if doc:
            print "\nDocumentation:"
            print doc.strip()

    def process_builtin_commands(self, tasks):
        if tasks[0][0] == "clear":
            self.do_clear(tasks[0][1])
            raise StopIteration
        elif tasks[0][0] == "clearall":
            self.do_clearall()
            raise StopIteration
        elif tasks[0][0] == "help":
            if len(tasks[0][1]) == 0:
                self.do_help()
            else:
                self.do_help_task(tasks[0][1][0])
            raise StopIteration

    def process_options(self, tasks):
        to_remove = []

        for i, task in enumerate(tasks):
            if task[0] == "--debug":
                self.LOGGER.setLevel(logging.DEBUG)
                to_remove.append(i)

        for i in to_remove:
            del tasks[i]

    def run_command_gen(self, args):
        tasks = self.parse_tasks(args)
        return self.run_tasks_gen(tasks)

    def run_tasks_gen(self, tasks):
        self.get_task_list()

        if len(tasks) == 0:
            raise TaskManagerError, "No Task to perform"

        self.process_options(tasks)
        self.process_builtin_commands(tasks)

        self.check_tasks_exist(tasks)
        task_dict = pair_list_to_dict(tasks)

        def task_args(task):
            try:
                return task_dict[task.get_name()][0]
            except KeyError:
                return []

        def task_nocache(task):
            try:
                return bool(task_dict[task.get_name()][1] & FLAG_NOCACHE)
            except KeyError:
                return False

        def task_showresult(task):
            try:
                return bool(task_dict[task.get_name()][1] & FLAG_SHOWRESULT)
            except KeyError:
                return False

        cache = {}

        def runtask(task):
            name = task.get_name()

            if not name in cache:
                # required tasks
                needed_tasks = []

                for needed_task in task.get_task_dependencies(recursive=False):
                    needed_tasks.append(cache[needed_task.get_name()])

                # command line arguments
                cmd_args = task_args(task)

                dflt_nocache = task.nocache
                nocache = task_nocache(task)

                if nocache: task.nocache = nocache

                self.info(separator())
                self.info("Running %s..." % task.get_name())
                cache[name] = task(*(needed_tasks + cmd_args))

                task.nocache = dflt_nocache

            if task_showresult(task):
                print str(cache[name])

            return cache[name]

        last_task = self.get_task(tasks[-1][0])
        deps = last_task.get_task_dependencies()

        self.info("Target task: %s" % last_task.get_name())

        if len(deps) > 0:
            self.info("Required tasks: %s" % \
                                    ", ".join([t.get_name() for t in deps]))

        total_start = time.time()

        for task in deps:
           yield runtask(task)

        yield runtask(last_task)

        diff = time.time() - total_start
        self.info(separator())
        self.info("Total elapsed time: %d seconds\n\n" % diff)

    def run_tasks(self, tasks):
        return list(self.run_tasks_gen(tasks))

    def run_command(self, args):
        self.log_history("started: " + " ".join(args))
        ret = list(self.run_command_gen(args))
        self.log_history("completed: " + " ".join(args))
        return ret

    def log_history(self, s):
        m = "[%s] %s\n" % \
            (datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
             s)
        if not os.path.exists(TaskManager.OUTPUT_FOLDER):
            os.makedirs(TaskManager.OUTPUT_FOLDER)
        save_file(os.path.join(TaskManager.OUTPUT_FOLDER, "HISTORY"),
                  m, mode="a")


def get_tasks_in_main():
    import __main__
    tasks = []
    for attr in dir(__main__):
        attr = getattr(__main__, attr)
        if isinstance(attr, Task):
            tasks.append(attr)
    return tasks

def _get_task_manager(task_list):
    if task_list is None: task_list = get_tasks_in_main()
    manager = TaskManager()
    for task in task_list:
        #method = new.instancemethod(func, None, TaskManager)
        #if not method_name: method_name=func.__name__
        #clas.__dict__[method_name]=method
        setattr(manager, task.get_name(), task)
    return manager

def run_command(args, task_list=None):
    manager = _get_task_manager(task_list)
    return manager.run_command(args)

def run_tasks(tasks, task_list=None):
    manager = _get_task_manager(task_list)
    return manager.run_tasks(tasks)

########################################
# Logging utils...
########################################

class StreamHandler(logging.StreamHandler):

    def emit(self, *args, **kw):
        logging.StreamHandler.emit(self, *args, **kw)
        self.flush()

LOGGER = logging.getLogger('TaskManagerLogger')
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(StreamHandler(sys.stdout))

TaskManager.LOGGER = LOGGER
Task.LOGGER = LOGGER

# logging proxy methods to save some typing
for meth in ("debug", "info", "warning", "error", "critical"):
    setattr(TaskManager, meth, proxy_method(LOGGER, meth))
    setattr(Task, meth, proxy_method(LOGGER, meth))

########################################
# Parallel computing...
########################################

def pool_map_seq(func, iterable, chunksize=None, njobs=None):
    return map(func, iterable)

def pool_zipped_map_seq(func, iterable, chunksize=None, njobs=None):
    ret = []
    for args in iterable:
        if not isinstance(args, list) and not isinstance(args, tuple):
            args = (args, )
        ret.append(func(*args))
    return ret

def pool_sequentialize(iterable, chunksize=None, njobs=None):
    ret = []
    for func, args, kw in iterable:
        ret.append(func(*args, **kw))
    return ret

try:
    import multiprocessing

    def pool_map(func, iterable, chunksize=None, njobs=None):
        """
        func must be an unary function
        """
        pool = multiprocessing.Pool(njobs)
        return pool.map(func, iterable, chunksize)

    def pool_zipped_map(func, iterable, chunksize=None, njobs=None):
        """
        func can be of variable arity and each element in iterable should
        be a tuple of the same length as func's arity
        """
        if chunksize is not None and njobs is None:
            njobs = chunksize

        pool = multiprocessing.Pool(njobs)

        jobs = []

        if chunksize is not None and chunksize > 1:
            chunks = list_split(list(iterable), chunksize)
            iterable = [(func, it) for it in chunks]
            res = pool_zipped_map(pool_zipped_map_seq, iterable, njobs=njobs)
            return reduce(lambda x,y: x+y, res)
        else:
            for args in iterable:
                if not isinstance(args, list) and not isinstance(args, tuple):
                    args = (args, )
                jobs.append(pool.apply_async(func, args))

            return [job.get() for job in jobs]

    def pool_parallelize(iterable, chunksize=None, njobs=None):
        if chunksize is not None and njobs is None:
            njobs = chunksize

        pool = multiprocessing.Pool(njobs)

        jobs = []

        if chunksize is not None and chunksize > 1:
            chunks = list_split(list(iterable), chunksize)
            res = pool_map(pool_sequentialize, chunks, njobs=njobs)
            return reduce(lambda x,y: x+y, res)
        else:
            for func, args, kw in iterable:
                jobs.append(pool.apply_async(func, args, kw))
            return [job.get() for job in jobs]

    def pool_cpu_count():
        try:
            return multiprocessing.cpu_count()
        except NotImplementedError:
            return 1

except ImportError:
    pool_map = pool_map_seq
    pool_zipped_map = pool_zipped_map_seq
    pool_parallelize = pool_sequentialize
    pool_cpu_count = lambda : 1


def delayed(func):
    @wraps(func)
    def delayed_function(*args, **kw):
        return func, args, kw
    return delayed_function

def parallelized(func):
    @wraps(func)
    def wrapper(iterable, chunksize=None, njobs=None):
        return pool_zipped_map(func, iterable, chunksize, njobs)
    return wrapper

########################################
# Exceptions...
########################################

class TaskError(Exception):
    pass

class TaskManagerError(Exception):
    pass
