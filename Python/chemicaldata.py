from __future__ import division
from phreeqc import Phreeqc
from species import molarMassStringEval
from species import *
import numpy as np
import os
chemistrySolver = Phreeqc()
#
databaseFile = os.getenv("PHREEQCDAT")+"/phreeqc.dat"
molarMassDico = chemistrySolver.getMolarMassList(databaseFile,typ = {})
#
caCl2SSp = AqueousSecondarySpecies(symbol = "CaCl2",\
                                   formationReaction = [("Ca++",1),("2Cl-",1)],\
                                   logK25 = -0.64,\
                                   logK = [1.56212e+03, 2.55796e-01, -8.58012e+04, -5.69819e+02, 5.22119e+06],\
                                   name = "CaCl2",)
molarMassCaCl2 = caCl2SSp.getMolarMass(molarMassDico)
naClSSp = AqueousSecondarySpecies(symbol = "NaCl",\
                                   formationReaction = [("1Cl-",1),("1Na+",1)],\
                                   logK25 = -0.5,\
                                   name = "NaCl",)
molarMassNaCl = naClSSp.getMolarMass(molarMassDico)
#
h2OSSp = AqueousSecondarySpecies(symbol = "H2O",\
                                   formationReaction = [("H+",2),("0--",1)],\
                                   logK25 = 0.0,\
                                   name = "H2O",)
molarMassH2O = h2OSSp.getMolarMass(molarMassDico)
#
kClSSp = AqueousSecondarySpecies(symbol = "KCl",\
                                 formationReaction = [("1Cl-",1),("1K+",1)],\
                                 logK25 = -0.5,\
                                 logK = [7.89547e+02, 1.20470e-01, -4.47224e+04, -2.85535e+02, 2.71764e+06],\
                                 name = "KCl",)
molarMassKCl = kClSSp.getMolarMass(molarMassDico)
#
naHCO3SSp = AqueousSecondarySpecies(symbol = "NaHCO3",\
                                    formationReaction = [("1HCO3-",1),("1Na+",1)],\
                                    logK25 = -0.247,\
                                    logK = [7.69790e+02, 1.14620e-01, -4.14361e+04, -2.79679e+02, 2.38366e+06],\
                                    name = "NaHCO3",)
molarMassNaHCO3 = naHCO3SSp.getMolarMass(molarMassDico)
#
mgCl2SSp = AqueousSecondarySpecies(symbol = "MgCl2",\
                                   formationReaction = [("Ca++",1),("2Cl-",1)],\
                                   logK25 = -0.64,\
                                   logK = [1.56212e+03, 2.55796e-01, -8.58012e+04, -5.69819e+02, 5.22119e+06],\
                                   name = "MgCl2",)
molarMassMgCl2 = mgCl2SSp.getMolarMass(molarMassDico)
#
cO2SSp = AqueousSecondarySpecies(symbol = "CO2",\
                                 formationReaction = [("HCO3-",1),("1H+",1),("1H2O",-1)],\
                                 logK25 = 6.353,\
                                 name = "CO2",)
molarMassCO2 = cO2SSp.getMolarMass(molarMassDico)
#
n2SSp = AqueousSecondarySpecies(symbol = "N2",\
                                formationReaction = [("1.5O2",1),("2NH3",1),("3H2O",-1)],\
                                logK25 = 116.439,\
                                name = "N2",)
molarMassN2 = n2SSp.getMolarMass(molarMassDico)
#
cH4SSp = AqueousSecondarySpecies(symbol = "CH4",\
                                 formationReaction = [("HCO3-",1),("H+",1),("H2O",1),("2O2",-1)],\
                                 logK25 = -144.116,\
                                 name = "CH4",)
molarMassCH4 = cH4SSp.getMolarMass(molarMassDico)
#
h2SSSp = AqueousSecondarySpecies(symbol = "H2S",\
                                 formationReaction = [("1HS-",1),("1H+",1)],\
                                 logK25 = 6.989,\
                                 name = "H2S",)
molarMassH2S = h2SSSp.getMolarMass(molarMassDico)
M0 = molarMassH2O


saltMolarMasses    = np.array([molarMassNaCl, molarMassCaCl2, molarMassKCl, molarMassMgCl2, molarMassNaHCO3])
ionVantHoffFactors = np.array([naClSSp.getVantHoffFactor(), caCl2SSp.getVantHoffFactor(), kClSSp.getVantHoffFactor(), naHCO3SSp.getVantHoffFactor(), mgCl2SSp.getVantHoffFactor()])
gasMolarMasses     = np.array([molarMassCO2, molarMassN2, molarMassCH4, molarMassH2S])


if __name__ == '__main__':

    print (" salt   molar masses: \n")
    print (" NaCl   molar mass %e in kg/mol:"%molarMassNaCl)
    print (" KCl   molar mass %e in kg/mol:"%molarMassKCl)
    print (" CaCl2  molar mass %e in kg/mol:"%molarMassCaCl2)
    print (" CH4    molar mass %e in kg/mol:"%molarMassCH4)
    print (" CO2    molar mass %e in kg/mol:"%molarMassCO2)
    print (" H2S    molar mass %e in kg/mol:"%molarMassH2S)
    print (" MgCl2  molar mass %e in kg/mol:"%molarMassMgCl2)
    print (" N2     molar mass %e in kg/mol:"%molarMassN2)
    print (" NaCl   molar mass %e in kg/mol:"%molarMassCaCl2)
    print (" NaHCO3 molar mass %e in kg/mol:"%molarMassNaHCO3)




