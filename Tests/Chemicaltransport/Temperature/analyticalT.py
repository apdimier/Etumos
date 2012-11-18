#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Analytical solution for a temperature Dirichlet B.C. 
#
#  C0     = initial concentration of NaOH in the injection mesh
#           expressed in mol/l
#
#  C0 =  1.E-2
#  Kw,Ks,Ka = 1.E-14, pow(10,-3.6), pow(10,-9.8) at  25 de Celcius
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os
from functions import Function
from math import *

from _erffunctions import *



class AnalyticalSolution(Function):
    def __init__(self, time, masse, coords, De, Kw, Ks, Ka, rho, cp, kw, Ti, T0):
        self.time   = time
        self.masse  = masse
        self.coords = coords
        self.De     = De
        self.Kw     = Kw
        self.Ks     = Ks
        self.Ka     = Ka
        self.cp     = cp
        self.kw     = kw
        self.rho    = rho
        self.Ti = Ti
        self.T0 = T0
        pass
    def evalNa(self):
        listNa=[]
        for xp in self.coords:    
            a     =  xp / (2. * sqrt(self.De * self.time))
            Na    = self.masse * (1. - erf(a))
            listNa.append(Na)

        return listNa
    
    def evalPH(self):
        listPh=[]
        for xp in self.coords:    
            a     =  xp / (2. * sqrt(self.De * self.time))
            Na    = self.masse * (1. - erf(a))
            d = (Na*Na)+(4.0*(self.Kw+(self.Ks * self.Ka)))
            d = pow(d,0.5)
            pH = -1.*(log10(0.5*(d-Na)))
            #pH = -1.*(log(0.5*(d-Na)))/(log(10.))
            listPh.append(pH)

        return listPh
    
    def evalT_old(self):
        listT=[]
        print self.kw, self.time
#        raw_input()
        for xp in self.coords:
            a = 2.0 * sqrt(self.kw *  self.time)
##            b     = erf(xp/a)-0.5* erf((xp+L)/a)-0.5* erf((xp-2.*L)/a)
            b     = erf(xp/a)
##            c     = erfc(xp/a)+ erfc((2.*L-xp)/a)
            c     = erfc(xp/a)
            T   = self.Ti*b +self.T0 *c
            listT.append(T)
        return listT
    
    def evalT(self):
        listT=[]
        alpha = self.kw/(self.rho*self.cp)
        print " self.kw",self.kw
        print " self.rho",self.rho
        print " self.cp",self.cp
        print " xp",self.coords[0]
        print " T0",self.T0
        print " Ti",self.Ti
#        raw_input()
        for xp in self.coords:
            a = 2.0 * sqrt(alpha *  self.time)
            T   = self.Ti + (self.T0 - self.Ti)*(erfc(xp/a))
            listT.append(T)
        return listT
    
    def evalFluxT(self):
        listT=[]
        alpha = self.kw/(self.rho*self.cp)
        for xp in self.coords:
            a = 2.0 * sqrt(alpha *  self.time/3.141592654)
            b = 2.0 * sqrt(alpha *  self.time)
            T   = self.Ti + (self.T0 - self.Ti)*( exp (-xp**2/(4*alpha*self.time))-(xp/a)*sqrt(3.141592654)*erfc(xp/b))
            listT.append(T)
        return listT


