#!/usr/bin/env python
"""A collection of useful containers:

- Set
- OrderedSet
""" 
from __future__ import absolute_import
from copy import deepcopy 


class Set(list): 
    """Without repetitions"""

    def append(self, item):
        """Return the item already there or the new."""
        try:
            i = self.index(item)
            return self[i]
        except ValueError:
            list.append(self, item)
            return item

    def extend(self, a_list):
        ret = []
        for item in a_list:
            ret.append(self.append(item))
            pass
        return ret

    def delete(self, item):
        self.remove(item)

    def tolist(self):
        return self


class OrderedSet(Set):

    def append(self, item):
        list = self
        lo = 0
        hi = len(list)
        while lo < hi: # bisection loop
            mid = (lo+hi)//2        
            if item < list[mid]: 
                hi = mid
                pass
            else: lo = mid+1
            pass
        try:
            previous = list[lo-1]
        except IndexError: # smallest (and therefore new) item
            list.insert(0, item)
            return item
        if item != previous: # new item
            list.insert(lo, item)
            return item
        else: # already there
            item = previous
            return previous


class DictOfContainers(dict):
    def __init__(self, container=None):
        self.dict = {}
        if container == None:
            self.container_proto = []
            pass
        else:
            self.container_proto = container
            pass

    def __getitem__(self, key):
        return self.dict[key]

    def __len__(self):
        nn = 0
        for key in self.dict.keys():
            nn += len(self.dict[key])
            pass
        return nn

    def keys(self):
        keys = list(self.dict.keys())
        keys.sort()
        return keys

    def getContainer(self, key):
        dict = self.dict
        try:
            return dict[key]
        except KeyError:
            dict[key] = deepcopy(self.container_proto)
            return dict[key]

    def append(self, key_and_item):
        key, item = key_and_item
        cont = self.getContainer(key)
        return cont.append(item)

    def delete(self,key_and_item):
        key, item = key_and_item
        cont = self.getContainer(key)
        return cont.delete(item)

    def extend(self, key, items):
        cont = self.getContainer(key)
        return cont.extend(items)

    def __iter__(self):
        return DictOfContainersIterator(self)


class DictOfContainersIterator:
    def __init__(self, dict):
        self.dict = dict
        self.keys = list(dict.keys())
        self.key = self.keys[0]
        self.ikey = 0
        self.iter = iter(dict[self.key])

    def __iter__(self):
        return self

    def nextKey(self):
        self.ikey += 1
        try:
            self.key = self.keys[self.ikey]
        except IndexError: # end of dict
            raise StopIteration
        self.iter = iter(self.dict[self.key])
        return

    def next(self):
        try:
            return next(self.iter)
        except StopIteration: # end of container
            self.nextKey()
            return next(self.iter)

