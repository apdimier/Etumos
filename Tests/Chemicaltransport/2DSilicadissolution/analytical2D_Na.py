#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  analytical solution for silica dissolution
#
#  alphaL = longitudinal dispersion
#  alphaT = transversal  dispersion
#  Ux     = Darcy velocity along the x-axis
#  x0, y0 = coordinates of the injection point
#  S      = surface of the injection mesh
#  C0     = initial concentration of NaOH in the injection mesh
#           expressed in mol/l
#
#  alphaL,alphaT,Ux,S,C0,x0,y0 = 0.2, 0.05, 5.7E-7, 4.E-4, 1.E-2, 1., 1.75
#  Kw,Ks,Ka = 1.E-14, pow(10,-3.6), pow(10,-9.8)
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os
from math import *

class AnalyticalFunction2D_Na:
    def __init__(self, time, mass):
        self.time  = time
        self.mass = mass
        pass
    def eval(self,coords):
        x = coords[0]
        y = coords[1]
        # != par init
        alphaL,alphaT,Ux,x0,y0 = 0.2, 0.05, 5.7E-7, 1., 1.75
        # Na theoretical concentration
        a = (((x-x0)-(Ux*self.time))*((x-x0)-(Ux*self.time)))/(4.0*alphaL*Ux*self.time)
        b = ((y-y0)*(y-y0))/(4.0*alphaT*Ux*self.time)
#        c = (self.mass)/(4.0*pi*Ux*pow(alphaL*alphaT,0.5))
        c = (self.mass)/(4.0*pi*Ux*self.time*pow(alphaL*alphaT,0.5))
        res1 = c*(exp(-1.*(a+b)))
##        # pH theoretical concentration
##        Kw,Ks,Ka = 1.E-14, pow(10,-3.6), pow(10,-9.8)
##        d = (res1*res1)+(4.0*(Kw+(Ks*Ka)))
##        d = pow(d,0.5)
##        res2 = -1.*log(0.5*(d-res1))/(log(10.))

        return res1
    



