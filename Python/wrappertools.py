#!/usr/bin/env python
from __future__ import absolute_import
from constant import epsf
from numpy import allclose
from types import FloatType,\
                  IntType,\
                  StringType
from six.moves import range
class Whoops(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)
        
def verifyEqualFloats(f1, f2, eps=0.):
##    if len(args)<2:
##        msg='Not enough arguments to compare.'
##        raise ValueError(msg)
    args=[f1,f2]
    verifyTypeList(args,[FloatType,IntType])
    if not eps:
        for f in args:
            if f:
                eps=f/epsf
                break
            pass
        pass
    for i in range(len(args)-1):
        f1=args[i]
        f2=args[i+1]
        allclose(f1,f2,rtol = 0,atol =eps)
        pass
    return

def checkFloatEquality(x, y, eps = epsf, msg = None):
   if not msg: msg='|x-y|>eps cf. values'%(x,y,eps)
   if not allclose(x,y,rtol = 0.,atol=eps):
        raise ValueError(msg)

def areClose(x, y, atol = epsf, kind = None, msg = None):
    eps = atol
    if type(x) not in [FloatType,IntType]:
        raise Exception("x: %s should be a float"%x)
    if type(y) not in [FloatType,IntType]:
        raise Exception("y: %s should be a float"%y)
    if kind.Lower().startswith('r'):
        if x !=0.:
            eps = epsf/x
            pass
        elif y !=0:
            eps = epsf/y
            pass
        pass
    if msg == None:
        return allclose(x,y,0.,eps)
    elif allclose(x,y,0.,eps):
        return True
    else:
        raise Warning(" x and y distance is greater than %s"%eps)
    



