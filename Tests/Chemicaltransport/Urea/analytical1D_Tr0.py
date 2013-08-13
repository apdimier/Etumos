#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  analytical solution for a
#
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os
from functions import Function
from math import exp,pi,sqrt,erfc

#from _erffunctions import erfc
"""
Lapidus and Amundson, 1952 see phreeqC manual p. 61
"""


class AnalyticalFunction1D_Tr:
    def __init__(self, coords, C0, Ci, time, darcyVelocity, De):
        self.time  = time
        self.q = darcyVelocity
        self.De = De
        self.c0         = C0
        self.ci         = Ci
        self.coords     = coords
        print " time q De c0: ",self.time , self.q, self.De, self.c0
        pass

    def eval(self):
        listC=[]
        #
        D0t = sqrt(self.De * self.time)
        print " D0t: ",D0t
        #
        for xl in self.coords:
            ym = (xl-self.q*self.time) / (2.* D0t)
            yp = (xl+self.q*self.time) / (2.* D0t)
            #print " xl, ym, yp: ",xl, ym, yp
            #print " ym: ",erfc(ym)
            #print " ym, yp: ",erfc(yp)
            #print "exp: ",xl, self.De
            #print exp(xl*self.q/self.De)
            conc = self.ci + 0.5*(self.c0 - self.ci) * ( erfc(ym) + exp(xl * self.q / self.De)*erfc(yp))
            listC.append(conc)
            #if ( xl < 0.5): print " xp erfc(ym) erfc(yp) ",xl, erfc(ym), erfc(yp), conc
            if xl < 1.e-2: print " xl conc ",xl, conc

        return listC    
    



