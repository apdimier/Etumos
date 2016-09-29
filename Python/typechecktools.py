# -*- coding: utf-8 -*-
"""
Utilities to check the type of elements
"""

from __future__ import absolute_import
from __future__ import print_function
import types

from wrappertools import verifyEqualFloats

def toList(x):
    """
    Used to change a tuple to a list or an item to a list of one element.
    """
    if type(x) in [list,tuple]:
        return list(x)
    else:
        return [x]

def verifyLength(tulist, listLength, message=None):
    """
    If the list is not of length, listLength, an exception is raised
    """
    if len(tulist) != listLength:
        if not message:
            message = "check the length of the list"
            pass
    raise Exception(message)
    pass

def verifyItem(x, objekt):
    """
    Raises an exception if an item is not in a list, a tuple or a dictionary key.
    """
    if objekt.__class__ == list:
        if x not in objekt : raise Exception(x + " not in list argument "+objekt.__str__())
    elif objekt.__class__ == dict:
        if x not in list(objekt.keys()) : raise Exception(x + " not in list argument "+list(objekt.keys()).__str__())
    elif objekt.__class__ == tuple:
        if x not in list(objekt) : raise Exception(x + " not in list argument "+list(objekt).__str__())
    else:
        message = "The argument objekt must be a dictionary, a list or a tuple"
        raise message
    return None

def verifyItemList(dlt, objekt):
    """
    we check that the object is within a dictionary, a list or a tuple.
    Otherwise an exception is Raised.
    """
    for x in dlt:
        verifyItem(x, objekt)
        pass
    return None

def isInRange(x, x_min = None, x_max = None):
    """Return true if  x is in [x_min, x_max], false otherwise."""
    
    if x_min is None and x_max is None :
        return 1
    if x_min is None :
        return x <= x_max
    if x_max is None :
        return x >= x_min
    
    return x >= x_min and x <= x_max

def verifyRange(x, min=None, max=None):
    """Raises an exception if x is not in [min, max]."""
    if not isInRange(x, min, max):
        if min is None :
            str = ']..., ' + repr(max) + ']'
        elif max is None :
            str = '[' + repr(min) + ', ...['
        else:
            str = '[' + repr(min) + ', ' + repr(max) + ']'
            pass
        message = ' '.join(['Quantity', repr(x), 'out of range', str])
        raise message
    pass

def verifyGrowingOrderOfList(l):
    """
    Raises an exception if elements of list are not in growing order
    """
    previous = 0.0
    for item in l:
        verifyRange(item,min=previous)
        previous = item
        pass
    
def isInOpenRange(x, xMin = None, xMax = None):
    """
    Return true if  x is in ]xMin, xMax[, false otherwise.
    """
    if xMin is None and xMax is None :
        return 1
    if xMin is None :
        return x < xMax
    if xMax is None :
        return x > xMin
    
    return x > xMin and x < xMax

def verifyOpenRange(x, min=None, max=None):
    """
    Raises an exception if x is not in ]min, max[.
    """
    if not isInOpenRange(x, min, max):
        if min is None :
            str = ']..., ' + repr(max) + '['
        elif max is None :
            str = ']' + repr(min) + ', ...['
        else:
            str = ']' + repr(min) + ', ' + repr(max) + '['
            pass
        message = ' '.join(['Quantity', repr(x), 'out of range', str])
        raise message
    pass

# type checks

def _w_(liste):
    """Writes a string from a list of 'things' with a __name__ attribute.""" 
    liste = toList(liste)
    return (' '.join([elt.__name__ for elt in liste]))
    

def _typeErrorMessage(string1, string2):
    """
    Error message for type-verifing functions.
    """
    s = ' '.join(['type', string1, "found,", string2, "expected"])
    return s


def isInstance(x, klassenprobe):
    """
    Returns true if x is an instance of one of the classes within the testclasses, false otherwise
    """
    if type(klassenprobe) is not list:
        if isinstance(x, klassenprobe):
            return 1
        else:
            raise Exception(" the x instance is not of the specified type %s"%(klassenprobe.__name__))
    else:
        for klasse in klassenprobe:
            if isinstance(x, klasse):
                return 1
            pass
    return 0

def verifyType(x, someTypes, message = None):
    """
    Raises an exception if the type of a variable is not in some_types
    """
    if type(x) in someTypes:
        return 1
    else:
    #raise Exception("wrong type")
        return 0

def verifyTypeList(alist, someTypes):
    alist = toList(alist)
    for x in alist:
        verifyType(x, someTypes)
        pass
    return None
    
def verifyClass(x, someClass, message=None):
    """
    Raises an exception if x is not an instance of one of some_classes
    """
    try:
        #print "verifyClass",x.__class__,someClass.__class__
        if x.__class__ == someClass.__class__:
            print("verifyClass it is ok")
            return
        pass
    except:
        dir(x)
        pass
    # Temporary
    
    if not isInstance(x, someClass):
##         #""""
##         classes=toList(some_classes)
##         for clas in classes:
##             print x.__class__.__name__,clas.__name__
##         #""""
        if message is None:
            if hasattr(x, "__repr__"): xstr = x.__repr__()
            else: xstr = repr(type(x))
            xstr = repr(type(x))       
            message =_typeErrorMessage(xstr, _w_(someClass))
            pass
        raise TypeError(message)
    return

def verifyClasse(x, someClass, message=None):
    """
    Raises an exception if x is not an instance of one of some_classes
    """
    try:
        if x.__class__ == someClass.__class__:
            return
        pass
    except:
        pass
    # Temporary
    
    if not isInstance(x, someClass):
        if message is None:
            if hasattr(x, "__repr__"):
                xstr = x.__repr__()
            else:
                xstr = repr(type(x))
            xstr = repr(type(x))       
            message = _typeErrorMessage(xstr, _w_(someClass))
            pass
    raise TypeError(message)
    return

def verifyClassList(liste, someClass):
    """
    Raises an exception if an element of the list, liste,  is not an instance of one of some_classes
    """
    liste = list(liste)
    for x in liste:
        #print(" x class name ",x) 
        verifyClass(x, someClass)
        pass
    return

# Type check and return

def checkTypeAndSet(element, someType):
    """
    check the type and then returns the element
    """
    verifyType(element, someType)
    return element

def checkClassAndSet(element, someClass):
    """
    check the appartenance to a class and then returns the element
    """
    verifyClass(element, someClass)
    return element

def verifyExists( *args):
    ind = 0
    for item in args:
        ind += 1
        if not item:
            message = "item number %s of 'args' does not exist."%ind
            raise Exception(message)
