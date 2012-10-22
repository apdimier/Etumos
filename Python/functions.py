"""
Some tools to define functions
"""
from generictools import listTypeCheck, memberShip, SET_NUMBER
from listtools import toList

import types

from typechecktools import verifyType

from posttables import Table
from math import pow

class Function:
    """
    Function:
    A function is made of a list of coefficients.
    These coefficients must be integers or reals
    """
    
    def __init__(self, coefList = None, timeCoef = None):
        """
        - coefList : list of real or integer
        - the timecoeff is a table
        """
        if coefList:
#            print coefList,type(coefList)
            verifyType(coefList, [types.ListType])
            for coef in coefList:
#                print " c ",c
                verifyType(coef, [types.FloatType,types.IntType])
            self.coefList = coefList
        else:
            self.coefList =[]
            
        if timeCoef:
            memberShip(timeCoef, Table)
            pass
        self.timecoeff = timeCoef
        return

    def copy(self):
        return Function(self.coefList,self.timecoeff)
    
    def getNbCoefficients(self):
        """
        To get the number of coefficients
        """
        return len(self.coefList)
    
    def getNbTimeCoefficients(self):
        """
        To get the number of time coefficients
        """
        if self.timecoeff:
            return self.timecoeff.getNbRows()
        else:
            return None
    
    def getCoefficient(self, i):
        """
        get ith coefficient
        """
        verifyType(i, types.IntType)
        return self.coefList[i]

    def getCoefficients(self):
        """get coefficients list"""
        return self.coefList
    
    def getTimeCoefficient(self):
        "get time table"
        return self.timecoeff

    def amult(self,mult):
        newFunc=self.copy()
        if self.getTimeCoefficient():
            newFunc.timecoeff=self.timecoeff.amult(mult)
        else:
            newFunc.coefList=[c*mult for c in self.coefList]
            pass
        return newFunc
    
    def getNbComponents(self):
        """
        Gets the number of functions (1)
        """
        return 1

    def tolist(self):
        """Returns a list containing the function"""
        return [self]

class TimeTabulatedFunction(Function):
    """Time Tabulated Function"""
    def __init__(self,  timecoeff=None):
        if not timecoeff:
            from exceptions import Exception
            raise Exception("For a tabulated function,\ngive the coefficients.")
        coefList=None
        Function.__init__(self, coefList, timecoeff)

    def copy(self):
        return TimeTabulatedFunction(self.timecoeff)

class SpaceAndTimeTabulatedFunction(Function):
    """Function f(x)*g(t)"""
    def __init__(self,  spacefunction,timecoeff):
        if spacefunction.getTimeCoefficient():
            raise Exception("You initialize a SpaceAndTimeTabulatedFunction with a space function depending on time")
        self.spacefunction = spacefunction
        Function.__init__(self,spacefunction.getCoefficients(),timecoeff)

    def eval(self,coords):
        return self.spacefunction.eval(coords)
    
        
class LinearFunction(Function):
    """
    LinearFunctions:
    
    For a*x + b*y + c*z + d, coefficients are given in a list as [d, a, b, c]

    For a*x + b*y + c*z + d + e*t, coefficients are given as [d, a, b, c, e]
    
    Introducing d as first coefficient, you can introduce 2, 3 or four coefficients 
    depending on the boundary to be treated. But, you have to keep the order: a: 1, b: 2 c: 3
    
    For a timeLinearFunction, you must introduce the 5 coefficients
    """
    
    def eval(self, coords):
        """evaluate function at point of coordinates coords"""
        coefList = self.coefList
        value=coefList[-1]
        for i in range(len(coords)):
            value+=coefList[i]*coords[i]
#            print " i ",i, coefList[i], coords[i]
        return value

class TimeFunction(Function):
    """ Define different types of function of time
        Input are: coef = a list coeficients of the function
                   timeInterval =  (to,tmax)
                   type = type of the function, by default linear function 
    """
    def __init__(self,coef,timeInterval,typeFunction='linear'):
        if typeFunction not in ['linear','exponential','logarithmic','polynomial','power']: raise Exception, "check the time function"
        verifyType(coef, types.ListType)
        verifyType(timeInterval,types.TupleType)
        self.coef=coef
        self.timeInterval=timeInterval
        self.typeFunction=typeFunction
            
    def copy(self):
        return TimeFunction(self.coef,self.timeInterval,self.typeFunction)

    def getTypeFunction(self):
        return self.typeFunction

    def getFunctionCoefficients(self):
        return self.coef

    def getTimeInterval(self):
        return self.timeInterval

    def amult(self,mult):
        newFunc=self.copy()
        newFunc.coef=[x*mult for x in self.coef]
        return newFunc
 
class PolynomialFunction(Function):
    """
    PolynomialFunction:
    
     For a function     anx^n + an-1x^n-1 + ... + a1x + a0 + 
                        bny^n + bn-1y^n-1 + ... + b1y + b0 +
                        cnz^n + cn-1z^n-1 + ... + c1z + c0,

        coefficients should be entered as a list of tuple of same length :
     
        a 3 dimensional list [(an,an-1,...,a1,a0),(bn,bn-1,...,b1,b0),(cn,cn-1,...,c1,c0)]
     """
    def __init__(self,coefList):
        """constructor"""
        verifyType(coefList, types.ListType)
        length = len(coefList)
        if length !=3:
            raise Exception, "wrong dimension:\n"+\
            "the coefList for a polynomial function should be:"+\
            "[(an,an-1,...,a1,a0),(bn,bn-1,...,b1,b0),(cn,cn-1,...,c1,c0)] "
        coefList_x = coefList[0]
        coefList_y = coefList[1]
        coefList_z = coefList[2]
        len_coefList = len(coefList_x)
        if ((len_coefList != len(coefList_y)) or
            (len_coefList != len(coefList_z))):
            raise Exception, "check the coefList length for the PolynomialFunction"
        self.coefList_x = coefList_x
        self.coefList_y = coefList_y
        self.coefList_z = coefList_z
        self.coefList = coefList_x + coefList_y + coefList_z
        return

    def getCoefficientsX(self):
        return self.coefList_x
    
    def getCoefficientsY(self):
        return self.coefList_y
    
    def getCoefficientsZ(self):
        return self.coefList_z
    
    def copy(self):
        return PolynomialFunction([self.coefList_x,self.coefList_y,self.coefList_z])

    def amult(self,mult):
        c=[]
        newcoeff=[]
        for x in self.coefList_x:
            newcoeff.append(x*mult)
            pass
        c.append(tuple(newcoeff))
        newcoeff=[]
        for x in self.coefList_y:
            newcoeff.append(x*mult)
            pass
        c.append(tuple(newcoeff))
        newcoeff=[]
        for x in self.coefList_z:
            newcoeff.append(x*mult)
            pass
        c.append(tuple(newcoeff))
        return PolynomialFunction(c)
##         newFunc=self.copy()
##         Function.amult(newFunc,mult)
##         if not self.getTimeCoefficient():
##             newFunc.coefList_x=self.coefList_x*mult
##             newFunc.coefList_y=self.coefList_y*mult
##             newFunc.coefList_z=self.coefList_z*mult
##         return newFunc

    def eval(self, coords):
        """evaluate function at point of coordinates coords"""
        coefList_x = self.coefList_x
        coefList_y = self.coefList_y
        coefList_z = self.coefList_z
        value = coefList_x[-1] + coefList_y[-1] + coefList_z[-1]
        length = len(coefList_x)
        dim = length - 1
        value = 0.
        x = coords[0]
        y = coords[1]
        if len(coords) >2:
            z = coords[2]
        else:
            z = 0.
        
        for i in range(length):
            value += coefList_x[i]*pow(x,dim -i) + coefList_y[i]*pow(y,dim -i) + coefList_z[i]*pow(z,dim -i)
            pass
        return value        
                                              
class LinearFunction1D(LinearFunction):
    """ 
    ax + b
    """
    pass

class LinearFunction2D(LinearFunction):
    """
    ax + by + c
    """
    pass

class LinearFunction3D(LinearFunction):
    """ 
    ax + by + cz + d
    """
    pass

def makeLinearFunction(coefList):
    """method to construct LinearFunction1D, 2D or 3D
    For a function ax + by + cz + d, coefficients are given in
    a list in order [d,a,b,c]"""
    len1 = len(coefList)
    if len1 == 2:
        return LinearFunction1D(coefList)
    elif len1 == 3:
        return LinearFunction2D(coefList)
    elif len1 == 4:
        return LinearFunction3D(coefList)
    else:
        raise "A linear function must have 2-4 coefficients, not " + `len1`
    return


class Interval:
    """
    points de calculs d une fonction
    """

    def __init__(self, debut, fin, pas):
        self.debut = SET_NUMBER(debut)
        self.fin = SET_NUMBER(fin)
        self.pas = SET_NUMBER(pas)
        if( self.fin < self.debut):
            raise "La fin de l'intervalle doit etre au moins egale au debut"
    def getDebut(self):
        return self.debut
    def getFin(self):
        return self.fin
    def getPas(self):
        return self.pas

class DerivableFunction(Function):
    def __init__(self,fonction,derivee=None,interval=None):
        if isinstance(fonction,types.FunctionType) or isinstance(fonction,types.FloatType) or isinstance(fonction,types.IntType) :
            self.fonction = fonction
        else:
            raise "Foncthd, fonction doit etre de type Function, Float ou Int"
        if derivee <> None:
            if isinstance(derivee,types.FunctionType) or isinstance(derivee,types.FloatType) or isinstance(derivee,types.IntType):
                self.derivee = derivee
        self.derivee = derivee
        if interval == None:
            print "Attention interval nul, les fonctions seront evaluees en zero"
        self.interval = interval
        #
        if type(fonction) == types.FunctionType:
            self.nom=fonction.func_name
        else:
            self.nom='const'
    def eval(self,x):
        if isinstance(self.fonction,types.FunctionType):
            return self.fonction(x)
        elif isinstance(self.fonction,types.FloatType) or isinstance(self.fonction,types.IntType):
            return self.fonction
        else:
            return None
    def deriv_eval(self,x):
        if self.derivee <> None:
            if isinstance(self.derivee,types.FunctionType):
                return self.derivee(x)
            elif isinstance(self.derivee,types.FloatType) or isinstance(self.derivee,types.IntType):
                return self.derivee
        else:
            return None
    #
    def getValue(self):
        return self
    def getName(self):
        return self.nom
    def getInterval(self):
        return self.interval
    
#    
class DerivableFunctionconst(DerivableFunction):
    def __init__(self,constante):
        DerivableFunction.__init__(self,constante)
        self.constante = constante
    def eval(self,x):
        return self.constante  

