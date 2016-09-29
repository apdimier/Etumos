"""Algebraic Operations with List of FLoats."""

import math

import numpy as npy

from operator import __and__ as AND

from operator import add as addition

from operator import mul as multiplication

from types import ListType,TupleType

def toList(x):
    """
    Direkt von der ZauberFloete 
    returns a list type object made of x element or elements
    """
    if type(x) in [ListType,TupleType]:
        return list(x)
    else:
        return [x]

def _checkListLength(lst1, lst2):
    if len(lst1) != len(lst2):
        raise Exception, "check arguments length"

def isListOfLists(x):
    if not isinstance(x, ListType): return False
    return reduce(AND, map(lambda z: isinstance(z, ListType), x))

def printList(lst,str):
    """print a list"""
    ind=0
    for i in lst : 
        print str,ind,i
        ind+=1
        pass
    print "end of printlist ",len(lst)
    return None

def _add(x, y):
    return x + y
def _sub(x, y):
    return x - y

def addLists(lst1, lst2):
    return map(_add, lst1, lst2)

def subtractLists(lst1, lst2):
     return map(_sub, lst1, lst2)

def amultList(a, lst1):
    return map(lambda x: a*x , lst1)

def dot( a, b ):
    return reduce(addition, map( multiplication, a, b))

def normMaxList(liste):
    return max(abs(min(liste)), abs(max(liste)))

def normL1List(list):
    return npy.sum(npy.absolute(list))
    
normL1 = normL1List

def norm2List(list):
    return (npy.sum(npy.absolute(list)**2))**0.5

norm2L = norm2List

def normMaxListComparison(lst1, lst2):
    """
    Returns normMax(lst1 - lst2) / normMax(lst2).
    """
    return normMaxList(subtractLists(lst1, lst2)) / normMaxList(lst2)

def norm2ListComparison(lst1, lst2):
    """
    Returns norm2(l1 - l2) / norm2(l2).
    """
    return norm2L(subtractLists(lst1, lst2)) / norm2L(lst2)

def elimCommonElementsInList(liste,epsilon):
    """returns a new list made of all single elements in list liste (single test is made at epsilon)"""
    liste.sort()
    l_temp = [liste[0]]
    li = range(len(liste))
    for i in li[1:]:
        time = liste[i]
        if type(time) != TupleType:
            if abs(time - l_temp[-1]) > epsilon:
                l_temp.append(time)
                pass
            pass
        else:
            # if element is a tuple, we keep it!
            l_temp.append(time)
            pass
        pass
    return l_temp

def toFloatList(l):
    """ convert int list to float list """
    return map(float,l)

def extractIndex(l,index):
    """
    Extract from the list l the value corrresponding to list index
    """
    new_l = []
    len_l = len(l)
    for i in index:
        if i<=len_l:
            new_l.append(l[i])
            pass
        else:
            mess = "index %i output of range of list l"%i
            raise IncorrectValue(mess)
        pass
    return new_l
