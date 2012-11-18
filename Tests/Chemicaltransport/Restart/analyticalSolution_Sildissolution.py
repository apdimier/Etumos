#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  silica dissolution, analytical solution
#
#  C0     Dirichlet condition aqueous Na concentration
#         unit: mol/l
#
#  C0 =  2.0e-2
#  
#  K_Na,K_silice,K_silicique = pow(10,-14.18), pow(10,-3.6), pow(10,-9.8) 
#
#       Na+ + H2O = NaOH + H+
#                    log_k           -14.180
#
#          SiO2 = H4SiO4 -2H2O
#                    log_k   -3.6000000000e+00
#
#          H4SiO4 -1H+  = H3SiO4-
#                    log_k   -9.8300000000e+00
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os
from functions import Function
from math import *

from _erffunctions import erfc

class analyticalFunction(Function):

    def __init__(self, time, C0, coords, De):
        self.time        = time
        self.C0          = C0
        self.coords      = coords
        self.De          = De
        self.K_Na        = K_Na = pow(10.,-14.18)
        self.K_Silice    = K_Silice = pow(10.,-3.60)
        self.K_Silicique = K_Silicique   = pow(10.,-9.83)
        pass

    def evalNa(self):
        listNa=[]
        for xp in self.coords:    
            a     =  xp / (2.0 * sqrt(self.De * self.time))
            Na    = self.C0 * erfc(a)
            listNa.append(Na)

        return listNa
    
    def evalPH(self):
        listPh=[]
        for xp in self.coords:    
            a     =  xp / (2.0 * sqrt(self.De * self.time))
            Na    = self.C0 * erfc(a)
            d = (Na*Na)+(4.0*(self.K_Na+(self.K_Silice * self.K_Silicique)))
            d = pow(d,0.5)
            pH = -1.*(log10(0.5*(d-Na)))
            #pH = -1.*(log(0.5*(d-Na)))/(log(10.))
            listPh.append(pH)

        return listPh
    



