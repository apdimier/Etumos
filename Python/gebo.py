"""
The "gebo"-database extension must be used in combination with "pitzer.dat"
The inserted data are taken from literature and various thermodynamic databases.
The references of the data are given behind their input.
THE USER IS RESPONSIBLE FOR THE RESULTS OF MODELLING!

Pitzer parameters: B0, B1, B2, C0 are introduced via the saltSpecies function applied on instances of the Salt class.

THETA, PSI and LAMBDA are introduced via a "copy/paste" like method.
Developping a specific data model for Pitzer is too time consuming.

Reference for the extension is :

        Grundwasser - Zeitschrift der Fachsektion Hydrogeologie (2013) 18:93:98
        
        Prozessmodellierung hochsalinarer Waesser mit einer erweiterten PHREEQC-Datensatz
        
        E. Bozau
        
        The phreeqc database addon is linked to the article

"""
from __future__ import absolute_import
from chemistry import *
from chemicalmodule import *
from phreeqc import *

speciesAddenda = []
#
Fe = AqueousMasterSpecies(symbol = "Fe++",\
                          name = "Fe",\
                          element = "Fe",\
                          molarMass = MolarMass(55.845,"g/mol"),\
                          alkalinity = 0.0)
speciesAddenda.append(Fe)
#
Fe_p2_ = AqueousMasterSpecies(symbol = "Fe++",\
                              name = "Fe(+2)",\
                              element = "Fe",\
                              molarMass = MolarMass(55.845,"g/mol"),\
                              alkalinity = 0.0)
speciesAddenda.append(Fe_p2_)
#
Fe_p3_ = AqueousMasterSpecies(symbol = "Fe+++",\
                              name = "Fe(+3)",\
                              element = "Fe",\
                              molarMass = MolarMass(55.845,"g/mol"),\
                              alkalinity = 0.0)
speciesAddenda.append(Fe_p3_)
#
S_m2_ = AqueousMasterSpecies(symbol = "HS-",\
                             name = "S(-2)",\
                             element = "S",\
                             molarMass = MolarMass(32.064,"g/mol"),\
                             alkalinity = 1.0)
speciesAddenda.append(S_m2_)
#
# N
#
N = AqueousMasterSpecies(symbol = "NO3-",\
                             name = "N",\
                             element = "N",\
                             molarMass = MolarMass(14.0067,"g/mol"),\
                             alkalinity = 0.0)
speciesAddenda.append(N)
#
# N(+5)
#
Np5 = AqueousMasterSpecies(symbol = "NO3-",\
                             name = "N(+5)",\
                             element = "NO3",\
                             molarMass = MolarMass(14.0067,"g/mol"),\
                             alkalinity = 0.0)
speciesAddenda.append(Np5)
#
# N(+3)
#
Np3 = AqueousMasterSpecies(symbol = "NO2-",\
                             name = "N(+3)",\
                             element = "NO2",\
                             molarMass = MolarMass(14.0067,"g/mol"),\
                             alkalinity = 0.0)
speciesAddenda.append(Np3)
#
# N(0)
#
N0 = AqueousMasterSpecies(symbol = "N2",\
                             name = "N(0)",\
                             element = "N",\
                             molarMass = MolarMass(14.0067,"g/mol"),\
                             alkalinity = 0.0)
speciesAddenda.append(N0)
#
# N(-3)
#
Nm3 = AqueousMasterSpecies(symbol = "NH4+",\
                             name = "N(-3)",\
                             element = "NH4",\
                             molarMass = MolarMass(14.0067,"g/mol"),\
                             alkalinity = 0.0)
speciesAddenda.append(Nm3)
#
# C(-4)
#
C_m4_ = AqueousMasterSpecies(symbol = "CH4",\
                             name = "C(-4)",\
                             element = "CH4",\
                             molarMass = MolarMass(12.0107,"g/mol"),\
                             alkalinity = 0)
speciesAddenda.append(C_m4_)
#
# Si
#
Si = AqueousMasterSpecies(symbol = "SiO2",\
                          name = "Si",\
                          element = "Si",\
                          molarMass = MolarMass(28.0855,"g/mol"),\
                          alkalinity = 0)
speciesAddenda.append(Si)
#
# Zn
#
Zn = AqueousMasterSpecies(symbol = "Zn+2",\
                          name = "Zn",\
                          element = "Zn",\
                          molarMass = MolarMass(65.37,"g/mol"),\
                          alkalinity = 0)
speciesAddenda.append(Zn)





#
# Pb
#
Pb = AqueousMasterSpecies(symbol = "Pb+2",\
                          name = "Pb",\
                          element = "Pb",\
                          molarMass = MolarMass(207.20,"g/mol"),\
                          alkalinity = 0)
speciesAddenda.append(Pb)
#
# Al
#
Al = AqueousMasterSpecies(symbol = "Al+++",\
                          name = "Al",\
                          element = "Al",\
                          molarMass = MolarMass(26.981538,"g/mol"),\
                          alkalinity = 0)
speciesAddenda.append(Al)
                                                                                            #
                                                                                            # Now secondary species declaration
                                                                                            #
#
# H2O = OH- + H+
#
OHm = AqueousSecondarySpecies(symbol = "OH-",\
                                  formationReaction = [("H2O",1),("H+",-1)],\
                                  logK25 = -13.898,\
                                  logK = [-283.971,-0.05069842, 13323.0, 102.24447, -1119669.0],
                                  #activity_law = Davies(6.0),\
                                  name = "OH-",)
speciesAddenda.append(OHm)
#
# 2 H2O = O2 + 4 H+ + 4 e-
#
O2 = AqueousSecondarySpecies(symbol = "O2",\
                                  formationReaction = [("H2O",2),("4H+",-1),("4e-",-1)],\
                                  logK25 = -86.08,\
                                  #activity_law = Davies(6.0),\
                                  name = "O2",)
speciesAddenda.append(O2)
#
# 2 H+ + 2 e- = H2
#
H2 = AqueousSecondarySpecies(symbol = "H2",\
                                  formationReaction = [("H+",2),("e-",2)],\
                                  logK25 = -3.15,\
                                  #activity_law = Davies(6.0),\
                                  name = "H2",)
speciesAddenda.append(H2)
#
# Fe+2 = Fe+3 + e-
#
Feppp = AqueousSecondarySpecies(symbol = "Fe+++",\
                                  formationReaction = [("Fe++",1),("e-",-1)],\
                                  logK25 = -13.02,\
                                  coefA = 9.0, coefB = 0.0,
                                  name = "Fe+++",)
speciesAddenda.append(Feppp)
#
# Ferric
#
#
# Fe+3 + H2O = FeOH+2 + H+
#
FeOHpp = AqueousSecondarySpecies(symbol = "FeOH+2",\
                                  formationReaction = [("Fe+++",1),("H2O",1),("H+",-1)],\
                                  logK25 = -2.19,\
                                  #activity_law = Davies(6.0),\
                                  name = "FeOH+2",)
speciesAddenda.append(FeOHpp)
#
# Fe+3 + 2 H2O = Fe(OH)2+ + 2 H+
#
FeOH2p = AqueousSecondarySpecies(symbol = "Fe(OH)2+",\
                                  formationReaction = [("Fe+++",1),("H2O",2),("H+",-2)],\
                                  logK25 = -5.67,\
                                  #activity_law = Davies(6.0),\
                                  name = "Fe(OH)2+",)
speciesAddenda.append(FeOH2p)
#
# Fe+3 + 3 H2O = Fe(OH)3 + 3 H+
#
FeOH3 = AqueousSecondarySpecies(symbol = "Fe(OH)3",\
                                  formationReaction = [("Fe+++",1),("H2O",3),("H+",-3)],\
                                  logK25 = -12.56,\
                                  #activity_law = Davies(6.0),\
                                  name = "Fe(OH)3",)
speciesAddenda.append(FeOH3)
#
# Fe+3 + 4 H2O = Fe(OH)4- + 4 H+
#
FeOH4m = AqueousSecondarySpecies(symbol = "Fe(OH)4-",\
                                  formationReaction = [("Fe+++",1),("H2O",4),("H+",-4)],\
                                  logK25 = -21.6,\
                                  #activity_law = Davies(6.0),\
                                  name = "Fe(OH)4-",)
speciesAddenda.append(FeOH4m)
#
# 2 Fe+3 + 2 H2O = Fe2(OH)2+4 + 2 H+
#
Fe2OH2pppp = AqueousSecondarySpecies(symbol = "Fe2(OH)2+4",\
                                  formationReaction = [("Fe+++",2),("H2O",2),("H+",-2)],\
                                  logK25 = -2.95,\
                                  #activity_law = Davies(6.0),\
                                  name = "Fe2(OH)2+4",)
speciesAddenda.append(Fe2OH2pppp)
#
# 3 Fe+3 + 4 H2O = Fe3(OH)4+5 + 4 H+
#
Fe3OH4ppppp = AqueousSecondarySpecies(symbol = "Fe3(OH)4+5",\
                                  formationReaction = [("Fe+++",3),("H2O",4),("H+",-4)],\
                                  logK25 = -6.3,\
                                  #activity_law = Davies(6.0),\
                                  name = "Fe3(OH)4+5",)
speciesAddenda.append(Fe3OH4ppppp)
#
# Fe+3 + Cl- = FeCl+2
#
FeClpp = AqueousSecondarySpecies(symbol = "FeCl+2",\
                                  formationReaction = [("Fe+++",1),("Cl-",1)],\
                                  logK25 = 1.48,\
                                  #activity_law = Davies(6.0),\
                                  name = "FeCl+2",)
speciesAddenda.append(FeClpp)
#
# Fe+3 + 2 Cl- = FeCl2+
#
FeCl2p = AqueousSecondarySpecies(symbol = "FeCl2+",\
                                  formationReaction = [("Fe+++",1),("Cl-",2)],\
                                  logK25 = 2.13,\
                                  #activity_law = Davies(6.0),\
                                  name = "FeCl2+",)
speciesAddenda.append(FeCl2p)
#
# Fe+3 + 3 Cl- = FeCl3
#
FeCl3 = AqueousSecondarySpecies(symbol = "FeCl3",\
                                  formationReaction = [("Fe+++",1),("Cl-",3)],\
                                  logK25 = 1.13,\
                                  #activity_law = Davies(6.0),\
                                  name = "FeCl3",)
speciesAddenda.append(FeCl3)
#
# Fe+3 + SO4-2 = FeSO4+ 
#
FeSO4p = AqueousSecondarySpecies(symbol = "FeSO4+",\
                                  formationReaction = [("Fe+++",1),("SO4-2",1)],\
                                  logK25 = 4.04,\
                                  #activity_law = Davies(6.0),\
                                  name = "FeSO4+",)
speciesAddenda.append(FeSO4p)
#
# Fe+3 + HSO4- = FeHSO4+2 
#
FeHSO4p2 = AqueousSecondarySpecies(symbol = "FeHSO4+2",\
                                  formationReaction = [("Fe+++",1),("HSO4-",1)],\
                                  logK25 = 2.48,\
                                  #activity_law = Davies(6.0),\
                                  name = "FeHSO4+2",)
speciesAddenda.append(FeHSO4p2)
#
# Fe+3 + 2SO4-2 = Fe(SO4)2- 
#
Fe_2SO4m = AqueousSecondarySpecies(symbol = "Fe(SO4)2-",\
                                  formationReaction = [("Fe+++",1),("SO4-2",2)],\
                                  logK25 = 5.38,\
                                  #activity_law = Davies(6.0),\
                                  name = "Fe(SO4)2-",)
speciesAddenda.append(Fe_2SO4m)
#
# SO4-2 + 9 H+ + 8 e- = HS- + 4 H2O
#
HS = AqueousSecondarySpecies(symbol = "HS-",\
                                  formationReaction = [("SO4-2",1),("H+",9),("e-",8),("H2O",-4)],\
                                  logK25 = 33.65,\
                                  #activity_law = Davies(6.0),\
                                  coefA = 3.5, coefB = 0.0,
                                  name = "HS-",)
speciesAddenda.append(HS)
#
# HS- + H+ = H2S
#
H2S = AqueousSecondarySpecies(symbol = "H2S",\
                                  formationReaction = [("HS-",1),("H+",1)],\
                                  logK25 = 6.994,\
                                  logK = [-11.17, 0.02386, 3279.0],
                                  name = "H2S",)
speciesAddenda.append(H2S)
#
# HS- = S-2 + H+
#
Sm2 = AqueousSecondarySpecies(symbol = "S-2",\
                                  formationReaction = [("HS-",1),("H+",-1)],\
                                  logK25 = -12.918,\
                                  coefA = 5.0, coefB = 0.0,
                                  name = "S-2",)
speciesAddenda.append(Sm2)
#
# NH4+ ss
#
NH4SSp = AqueousSecondarySpecies(symbol = "NH4+",\
                                  formationReaction = [("NH4+",1)],\
                                  logK25 = 0.0,\
                                  coefA = 2.5, coefB = 0.0,
                                  name = "NH4+",)
speciesAddenda.append(NH4SSp)
#
# NO3- ss
#
NO3mSSp = AqueousSecondarySpecies(symbol = "NO3-",\
                                  formationReaction = [("NO3-",1)],\
                                  logK25 = 0.0,\
                                  coefA = 3.0, coefB = 0.0,
                                  name = "NO3-",)
speciesAddenda.append(NO3mSSp)
#
# NO3- + 2 H+ + 2 e- = NO2- + H2O
#
NO2m = AqueousSecondarySpecies(symbol = "NO2-",\
                                  formationReaction = [("NO3-",1),("H+",2),("e-",2),("H2O",-1),],\
                                  logK25 = 28.570,\
                                  coefA = 3.0, coefB = 0.0,
                                  name = "NO2-",)
speciesAddenda.append(NO2m)
#
# 2 NO3- + 12 H+ + 10 e- = N2 + 6 H2O
#
N2 = AqueousSecondarySpecies(symbol = "N2",\
                                  formationReaction = [("NO3-",2),("H+",12),("e-",10),("H2O",-6),],\
                                  logK25 = 207.08,\
                                  name = "N2",)
speciesAddenda.append(N2)
#
# NH4+ = NH3 + H+
#
NH3 = AqueousSecondarySpecies(symbol = "NH3",\
                                  formationReaction = [("NH4+",1),("H+",-1)],\
                                  logK25 = -9.252,\
                                  logK = [0.6322, -0.001225, -2835.76],
                                  name = "NH3",)
speciesAddenda.append(NH3)
#
# NO3- + 10H+ + 8e- = NH4+ + 3H2O ss
#
NH4p = AqueousSecondarySpecies(symbol = "NH4+",\
                                  formationReaction = [("NO3-",1),("H+",10),("e-",8),("H2O",-3)],\
                                  logK25 = 119.077,\
                                  name = "NH4+",)
speciesAddenda.append(NH4p)




#
# CO3-2 + 10 H+ + 8 e- = CH4 + 3 H2O
#
CH4 = AqueousSecondarySpecies(symbol = "CH4",\
                                  formationReaction = [("CO3-2",1),("H+",10),("e-",8),("H2O",-3)],\
                                  logK25 = 41.071,\
                                  name = "CH4",)
speciesAddenda.append(CH4)
#
# SiO2 ss
#
SiO2 = AqueousSecondarySpecies(symbol = "SiO2",\
                               formationReaction = [("SiO2",1)],\
                               logK25 = 0,\
                               name = "SiO2",)
speciesAddenda.append(SiO2)
                                                                                            #
                                                                                            # Zn
                                                                                            #
#
# Zn+2 ss
#
Znp2 = AqueousSecondarySpecies(symbol = "Zn+2",\
                               formationReaction = [("Zn+2",1)],\
                               logK25 = 0,\
                               coefA = 5.0, coefB = 0.0,\
                               name = "Zn+2",)
speciesAddenda.append(Znp2)
#
# Zn+2 + H2O = ZnOH+ + H+ ss
#
ZnOHp = AqueousSecondarySpecies(symbol = "ZnOH+",\
                                  formationReaction = [("Zn+2",1),("H2O",1),("H+",-1)],\
                                  logK25 = -8.96,\
                                  name = "ZnOH+",)
speciesAddenda.append(ZnOHp)
#
# Zn+2 + 2 H2O = Zn(OH)2 + 2 H+ ss
#
Zn_OH_2 = AqueousSecondarySpecies(symbol = "Zn(OH)2",\
                                  formationReaction = [("Zn+2",1),("H2O",2),("H+",-2)],\
                                  logK25 = -16.9,\
                                  name = "Zn(OH)2",)
speciesAddenda.append(Zn_OH_2)
#
# Zn+2 + 3 H2O = Zn(OH)3- + 3 H+ ss
#
Zn_OH_3 = AqueousSecondarySpecies(symbol = "Zn(OH)3-",\
                                  formationReaction = [("Zn+2",1),("H2O",3),("H+",-3)],\
                                  logK25 = -28.4,\
                                  name = "Zn(OH)3-",)
speciesAddenda.append(Zn_OH_3)
#
# Zn+2 + 4 H2O = Zn(OH)4-2 + 4 H+ ss
#
Zn_OH_4 = AqueousSecondarySpecies(symbol = "Zn(OH)4-2",\
                                  formationReaction = [("Zn+2",1),("H2O",4),("H+",-4)],\
                                  logK25 = -41.2,\
                                  name = "Zn(OH)4-2",)
speciesAddenda.append(Zn_OH_4)
#
# Zn+2 + Cl- = ZnCl+ ss
#
ZnClp = AqueousSecondarySpecies(symbol = "ZnCl+",\
                                  formationReaction = [("Zn+2",1),("Cl-",1)],\
                                  logK25 = 0.43,\
                                  name = "ZnCl+",)
speciesAddenda.append(ZnClp)
#
# Zn+2 + 2 Cl- = ZnCl2 ss
#
ZnCl2 = AqueousSecondarySpecies(symbol = "ZnCl2",\
                                  formationReaction = [("Zn+2",1),("Cl-",2)],\
                                  logK25 = 0.45,\
                                  name = "ZnCl2",)
speciesAddenda.append(ZnCl2)
#
# Zn+2 + 3Cl- = ZnCl3- ss
#
ZnCl3m = AqueousSecondarySpecies(symbol = "ZnCl3-",\
                                  formationReaction = [("Zn+2",1),("Cl-",3)],\
                                  logK25 = 0.5,\
                                  name = "ZnCl3-",)
speciesAddenda.append(ZnCl3m)
#
# Zn+2 + 3Cl- = ZnCl3- ss
#
ZnCl4mm = AqueousSecondarySpecies(symbol = "ZnCl4--",\
                                  formationReaction = [("Zn+2",1),("Cl-",4)],\
                                  logK25 = 0.2,\
                                  name = "ZnCl4--",)
speciesAddenda.append(ZnCl4mm)
#
# Zn+2 + CO3-2 = ZnCO3 ss
#
ZnCO3 = AqueousSecondarySpecies(symbol = "ZnCO3",\
                                  formationReaction = [("Zn+2",1),("CO3-2",1)],\
                                  logK25 = 5.3,\
                                  name = "ZnCO3",)
speciesAddenda.append(ZnCO3)
#
# Zn+2 + CO3-2 = ZnCO3 ss
#
Zn_CO3_2mm = AqueousSecondarySpecies(symbol = "Zn(CO3)2-2",\
                                  formationReaction = [("Zn+2",1),("CO3-2",2)],\
                                  logK25 = 9.63,\
                                  name = "Zn(CO3)2-2",)
speciesAddenda.append(Zn_CO3_2mm)
#
# Zn+2 + HCO3- = ZnHCO3+  ss
#
ZnHCO3p = AqueousSecondarySpecies(symbol = "ZnHCO3+",\
                                  formationReaction = [("Zn+2",1),("HCO3-",1)],\
                                  logK25 = 2.1,\
                                  name = "ZnHCO3+",)
speciesAddenda.append(ZnHCO3p)
#
# Zn+2 + SO4-2 = ZnSO4  ss
#
ZnSO4 = AqueousSecondarySpecies(symbol = "ZnSO4",\
                                  formationReaction = [("Zn+2",1),("SO4-2",1)],\
                                  logK25 = 2.37,\
                                  name = "ZnSO4",)
speciesAddenda.append(ZnSO4)
#
# Zn+2 + 2SO4-2 = Zn(SO4)2-2   ss
#
Zn_SO4_2mm = AqueousSecondarySpecies(symbol = "Zn(SO4)2-2",\
                                  formationReaction = [("Zn+2",1),("SO4-2",2)],\
                                  logK25 = 3.28,\
                                  name = "Zn(SO4)2-2",)
speciesAddenda.append(Zn_SO4_2mm)
                                                                                            #
                                                                                            # Pb
                                                                                            #
#
# Pb+2 ss
#
Pbp2 = AqueousSecondarySpecies(symbol = "Pb+2",\
                               formationReaction = [("Pb+2",1)],\
                               logK25 = 0,\
                               name = "Pb+2",)
speciesAddenda.append(Pbp2)
#
# 1.0000 Pb++ + 1.0000 HCO3-  =  PbCO3 +1.0000 H+  ss
#
PbCO3 = AqueousSecondarySpecies(symbol = "PbCO3",\
                                  formationReaction = [("Pb+2",1),("HCO3-",1),("H+",-1)],\
                                  logK25 = -3.7488,\
                                  activity_law = Davies(3.0),\
                                  name = "PbCO3",)
speciesAddenda.append(PbCO3)
#
# 1.0000 Pb++ + 1.0000 Cl-  =  PbCl+  ss
#
PbClp = AqueousSecondarySpecies(symbol = "PbCl+",\
                                  formationReaction = [("Pb+2",1),("Cl-",1)],\
                                  logK25 = 1.4374,\
                                  activity_law = Davies(4.0),\
                                  logK = [1.1948e+002, 4.3527e-002, -2.7666e+003, -4.9190e+001, -4.3206e+001],\
                                  name = "PbCl+",)
speciesAddenda.append(PbClp)
#
# 2.0000 Cl- + 1.0000 Pb++  =  PbCl2  ss
#
PbCl2 = AqueousSecondarySpecies(symbol = "PbCl2",\
                                  formationReaction = [("Pb+2",1),("Cl-",2)],\
                                  logK25 = 2.0026,\
                                  activity_law = Davies(3.0),\
                                  logK = [2.2537e+002, 7.7574e-002, -5.5112e+003, -9.2131e+001, -8.6064e+001],\
                                  name = "PbCl2",)
speciesAddenda.append(PbCl2)
#
# 3.0000 Cl- + 1.0000 Pb++  =  PbCl3-  ss
#
PbCl3m = AqueousSecondarySpecies(symbol = "PbCl3-",\
                                  formationReaction = [("Pb+2",1),("Cl-",3)],\
                                  logK25 = 1.6881,\
                                  activity_law = Davies(4.0),\
                                  logK = [2.5254e+002, 8.9159e-002, -6.0116e+003, -1.0395e+002, -9.3880e+001],\
                                  name = "PbCl3-",)
speciesAddenda.append(PbCl3m)
#
# 4.0000 Cl- + 1.0000 Pb++  =  PbCl4--  ss
#
PbCl4mm = AqueousSecondarySpecies(symbol = "PbCl4--",\
                                  formationReaction = [("Pb+2",1),("Cl-",4)],\
                                  logK25 = 1.4909,\
                                  activity_law = Davies(4.0),\
                                  logK = [1.4048e+002, 7.6332e-002, -1.1507e+003, -6.3786e+001, -1.7997e+001],\
                                  name = "PbCl4--",)
speciesAddenda.append(PbCl4mm)
                                                                                            #
                                                                                            # Al
                                                                                            #
#
# Al ss
#
AlpppSSp = AqueousSecondarySpecies(symbol = "Al+++",\
                                   formationReaction = [("Al+++",1)],\
                                   logK25 = 0,\
                                   name = "Al+++",)
speciesAddenda.append(AlpppSSp)
#
# Al+3 + H2O = AlOH+2 + H+
#
AlOHpp = AqueousSecondarySpecies(symbol = "AlOH+2",\
                                   formationReaction = [("Al+++",1),("H2O",1),("H+",-1),],\
                                   logK25 = -5,\
                                   logK = [-38.253, 0.0, -656.27, 14.327, 0.0],\
                                   name = "AlOH+2",)
speciesAddenda.append(AlOHpp)
#
# Al+3 + 2H2O = Al(OH)2+ + 2H+
#
Al_2OH_p = AqueousSecondarySpecies(symbol = "Al(OH)2+",\
                                   formationReaction = [("Al+++",1),("H2O",2),("H+",-2),],\
                                   logK25 = -10.1,\
                                   logK = [88.5, 0.0, -9391.6, -27.121, 0.0],\
                                   name = "Al(OH)2+",)
speciesAddenda.append(Al_2OH_p)
#
# Al+3 + 3H2O = Al(OH)3 + 3H+
#
AlOH3 = AqueousSecondarySpecies(symbol = "Al(OH)3",\
                                   formationReaction = [("Al+++",1),("H2O",3),("H+",-3),],\
                                   logK25 = -16.9,\
                                   logK = [226.374, 0.0, -18247.8, -73.597, 0.0],\
                                   name = "Al(OH)3",)
speciesAddenda.append(AlOH3)
#
# Al+3 + 4H2O = Al(OH)4- + 4H+
#
AlOH4 = AqueousSecondarySpecies(symbol = "Al(OH)4-",\
                                   formationReaction = [("Al+++",1),("H2O",4),("H+",-4),],\
                                   logK25 = -22.7,\
                                   logK = [51.578, 0.0, -11168.9, -14.865, 0.0],\
                                   name = "Al(OH)4-",)
speciesAddenda.append(AlOH4)
                                                                                            #
                                                                                            # Na
                                                                                            #
#
# Na+ + H2O = NaOH + H+
#
NaOH = AqueousSecondarySpecies(symbol = "NaOH",\
                                   formationReaction = [("Na+",1),("H2O",1),("H+",-1),],\
                                   logK25 = -14.18,\
                                   name = "NaOH",)
speciesAddenda.append(NaOH)
#
# Na+ + CO3-2 = NaCO3-
#
NaCO3m = AqueousSecondarySpecies(symbol = "NaCO3-",\
                                   formationReaction = [("Na+",1),("CO3-2",1)],\
                                   logK25 = 1.27,\
                                   name = "NaCO3-")
speciesAddenda.append(NaCO3m)
#
# Na+ + HCO3- = NaHCO3
#
NaHCO3 = AqueousSecondarySpecies(symbol = "NaHCO3",\
                                   formationReaction = [("Na+",1),("HCO3-1",1)],\
                                   logK25 = -0.25,\
                                   name = "NaHCO3",)
speciesAddenda.append(NaHCO3)
#
# Na+ + SO4-2 = NaSO4-
#
NaSO4m = AqueousSecondarySpecies(symbol = "NaSO4-",\
                                   formationReaction = [("Na+",1),("SO4-2",1)],\
                                   logK25 = 0.7,\
                                   name = "NaSO4-",)
speciesAddenda.append(NaSO4m)
                                                                                            #
                                                                                            # Ca
                                                                                            #
#
# Ca+2 + H2O = CaOH+ + H+
#
CaOHp = AqueousSecondarySpecies(symbol = "CaOH+",\
                                   formationReaction = [("Ca+2",1),("H2O",1),("H+",-1)],\
                                   logK25 = -12.78,\
                                   name = "CaOH+",)
speciesAddenda.append(CaOHp)
#
# Cl- +  Ca+2  =  CaCl+
#
CaClp = AqueousSecondarySpecies(symbol = "CaCl+",\
                                   formationReaction = [("Cl-",1),("Ca+2",1)],\
                                   logK25 = -0.6956,\
                                   logK = [8.1498e+001, 3.8387e-002, -1.3763e+003, -3.5968e+001, -2.1501e+001],\
                                   activity_law = Davies(4.0),\
                                   name = "CaCl+",)
speciesAddenda.append(CaClp)
#
# 2Cl- + Ca+2  =  CaCl2
#
CaCl2 = AqueousSecondarySpecies(symbol = "CaCl2",\
                                   formationReaction = [("Cl-",2),("Ca+2",1)],\
                                   logK25 = -0.6436,\
                                   logK = [1.8178e+002, 7.6910e-002, -3.1088e+003, -7.8760e+001, -4.8563e+001],\
                                   activity_law = Davies(3.0),\
                                   name = "CaCl2",)
speciesAddenda.append(CaCl2)
                                                                                            #
                                                                                            # Ba
                                                                                            #
#
# Ba+2 + SO4-2 = BaSO4
#
BaSO4 = AqueousSecondarySpecies(symbol = "BaSO4",\
                                   formationReaction = [("Ba+2",1),("SO4-2",1)],\
                                   logK25 = 2.7,\
                                   name = "BaSO4",)
speciesAddenda.append(BaSO4)
#
# Cl- +  Ba+2  =  BaCl+
#
BaClp = AqueousSecondarySpecies(symbol = "BaCl+",\
                                   formationReaction = [("Ba+2",1),("Cl-",1)],\
                                   logK25 = -0.6956,\
                                   logK = [8.1498e+001, 3.8387e-002, -1.3763e+003, -3.5968e+001, -2.1501e+001],\
                                   activity_law = Davies(4.0),\
                                   name = "BaCl+",)
speciesAddenda.append(BaClp)
#
# 2Cl- + Ba+2  =  BaCl2
#
BaCl2 = AqueousSecondarySpecies(symbol = "BaCl2",\
                                   formationReaction = [("Ba+2",1),("Cl-",2)],\
                                   logK25 = -0.6436,\
                                   logK = [1.8178e+002, 7.6910e-002, -3.1088e+003, -7.8760e+001, -4.8563e+001],\
                                   activity_law = Davies(3.0),\
                                   name = "BaCl2",)
speciesAddenda.append(BaCl2)
                                                                                            #
                                                                                            # mineral phases
                                                                                            #
#
# Siderite
#
siderite = MineralSecondarySpecies(symbol = "FeCO3",\
                               formationReaction = [("Fe+2",1),("CO3-2",1)],\
                               logK25 = -10.89,\
                               name = "Siderite",)
speciesAddenda.append(siderite)
#
# Hematite
#
hematite = MineralSecondarySpecies(symbol = "Fe2O3",\
                               formationReaction = [("Fe+3",2),("H2O",3),("H+",-6)],\
                               logK25 = -4.008,\
                               name = "Hematite",)
speciesAddenda.append(hematite)                                                                                            
#
# Goethite
#
goethite = MineralSecondarySpecies(symbol = "FeOOH",\
                               formationReaction = [("Fe+3",1),("H2O",2),("H+",-3)],\
                               logK25 = -1.0,\
                               name = "Goethite",)
speciesAddenda.append(goethite)                                                                                            
#
# Hematite
#
hydrous_ferric_oxide = MineralSecondarySpecies(symbol = "Fe(OH)3",\
                               formationReaction = [("Fe+3",1),("H2O",3),("H+",-3)],\
                               logK25 = 4.891,\
                               name = "Fe(OH)3(a)",)
speciesAddenda.append(hydrous_ferric_oxide)                                                                                            
#
# Pyrite
#
pyrite = MineralSecondarySpecies(symbol = "FeS2",\
                               formationReaction = [("Fe+2",1),("HS-",2),("e-",-2),("H+",-2)],\
                               logK25 = -18.479,\
                               name = "Pyrite",)
speciesAddenda.append(pyrite)                                                                                            
#
# FeS(ppt)
#
troilite = MineralSecondarySpecies(symbol = "FeS",\
                               formationReaction = [("Fe+2",1),("HS-",1),("H+",-1)],\
                               logK25 = -3.915,\
                               name = "FeS(ppt)",)
speciesAddenda.append(troilite)                                                                                            
#
# Pyrrhotite
#
pyrrhotite = MineralSecondarySpecies(symbol = "FeS",\
                               formationReaction = [("Fe+2",1),("HS-",1),("H+",-1)],\
                               logK25 = -3.7193,\
                               logK = [-1.5785e+002, -5.2258e-002, 3.9711e+003, 6.3195e+001, 6.2012e+001],\
                               name = "Pyrrhotite",)
speciesAddenda.append(pyrrhotite)                                                                                            
#
# Magnetite
#
magnetite = MineralSecondarySpecies(symbol = "Fe3O4",\
                               formationReaction = [("Fe+2",1),("Fe+3",2),("H2O",4),("H+",-8)],\
                               logK25 = 10.4724,\
                               logK = [-3.0510e+002, -7.9919e-002, 1.8709e+004, 1.1178e+002, 2.9203e+002],\
                               name = "Magnetite",)
speciesAddenda.append(magnetite)
#
# Mackinawite
#
mackinawite = MineralSecondarySpecies(symbol = "FeS",\
                               formationReaction = [("Fe+2",1),("HS-",1),("H+",-1)],\
                               logK25 = -4.648,\
                               name = "Mackinawite",)
speciesAddenda.append(mackinawite)
#
# FeMetal
#
feMetal = MineralSecondarySpecies(symbol = "Fe",\
                               formationReaction = [("Fe+2",1),("e-",2)],\
                               logK25 = 14.9,\
                               name = "FeMetal",)
speciesAddenda.append(feMetal)
#
# Sulfur
#
sulfur = MineralSecondarySpecies(symbol = "S",\
                               formationReaction = [("H2S",1),("e-",-2),("H+",-2)],\
                               logK25 = 4.882,\
                               name = "Sulfur",)
speciesAddenda.append(sulfur)
#
# Quartz
#
quartz = MineralSecondarySpecies(symbol = "SiO2",\
                               formationReaction = [("SiO2",1)],\
                               logK25 = -3.9993,\
                               logK = [7.7698e-002, 1.0612e-002, 3.4651e+003, -4.3551e+000, -7.2138e+005],\
                               name = "Quartz",)
speciesAddenda.append(quartz)
#
# Sphalerite
#
sphalerite = MineralSecondarySpecies(symbol = "ZnS",\
                               formationReaction = [("Zn+2",1),("HS-",1),("H+",-1)],\
                               logK25 = -11.618,\
                               name = "Sphalerite",)
speciesAddenda.append(sphalerite)
#
# Galena
#
galena = MineralSecondarySpecies(symbol = "PbS",\
                               formationReaction = [("Pb+2",1),("HS-",1),("H+",-1)],\
                               logK25 = -14.8544,\
                               logK = [-1.2124e+002, -4.3477e-002, -1.6463e+003, 5.0454e+001, -2.5654e+001],\
                               name = "Galena",)
speciesAddenda.append(galena)
#
# Pb
#
pb = MineralSecondarySpecies(symbol = "Pb",\
                               formationReaction = [("Pb+2",1),("H2O",1),("O2",-0.5),("H+",-2)],\
                               logK25 = 47.1871,\
                               logK = [-3.1784e+001, -1.4816e-002, 1.4984e+004, 1.3383e+001, 2.3381e+002],\
                               name = "Pb",)
speciesAddenda.append(pb)
#
# Anglesite
#
anglesite = MineralSecondarySpecies(symbol = "PbSO4",\
                               formationReaction = [("Pb+2",1),("SO4-2",1)],\
                               logK25 = -7.79,\
                               name = "Anglesite",)
speciesAddenda.append(anglesite)
#
# Plattnerite
#
plattnerite = MineralSecondarySpecies(symbol = "PbO2",\
                               formationReaction = [("Pb+2",1),("H2O",2),("e-",-2),("H+",-4)],\
                               logK25 = 49.3,\
                               name = "Plattnerite",)
speciesAddenda.append(plattnerite)
#
# Pb2O3
#
pb2O3 = MineralSecondarySpecies(symbol = "Pb2O3",\
                               formationReaction = [("Pb+2",2),("H2O",3),("e-",-2),("H+",-6)],\
                               logK25 = 61.04,\
                               name = "Pb2O3",)
speciesAddenda.append(pb2O3)
#
# Minium
#
minium = MineralSecondarySpecies(symbol = "Pb3O4",\
                               formationReaction = [("Pb+2",3),("H2O",4),("e-",-2),("H+",-8)],\
                               logK25 = 73.69,\
                               name = "Minium",)
speciesAddenda.append(minium)
#
# Pb(OH)2
#
Pb_OH_2 = MineralSecondarySpecies(symbol = "Pb(OH)2",\
                               formationReaction = [("Pb+2",1),("H2O",2),("H+",-2)],\
                               logK25 = 8.15,\
                               name = "Pb(OH)2",)
speciesAddenda.append(Pb_OH_2)
#
# Laurionite
#
laurionite = MineralSecondarySpecies(symbol = "PbOHCl",\
                               formationReaction = [("Pb+2",1),("Cl-",1),("H2O",1),("H+",-1)],\
                               logK25 = 0.623,\
                               name = "Laurionite",)
speciesAddenda.append(laurionite)
#
# Pb2(OH)3Cl
#
Pb2_OH_3Cl = MineralSecondarySpecies(symbol = "Pb2(OH)3Cl",\
                               formationReaction = [("Pb+2",2),("H2O",3),("Cl-",1),("H+",-3)],\
                               logK25 = 8.793,\
                               name = "Pb2(OH)3Cl",)
speciesAddenda.append(Pb2_OH_3Cl)
#
# Hydrocerrusite
#
hydrocerrusite = MineralSecondarySpecies(symbol = "Pb(OH)2:2PbCO3",\
                               formationReaction = [("Pb+2",3),("CO3-2",2),("H2O",2),("H+",-2)],\
                               logK25 = -17.460,\
                               name = "Hydrocerrusite",)
speciesAddenda.append(hydrocerrusite)
#
# Pb2O(OH)2
#
Pb2O_OH_2 = MineralSecondarySpecies(symbol = "PbO:Pb(OH)2",\
                               formationReaction = [("Pb+2",2),("H2O",3),("H+",-4)],\
                               logK25 = 26.2,\
                               name = "Pb2O(OH)2",)
speciesAddenda.append(Pb2O_OH_2)
#
# Pb4(OH)6SO4
#
Pb4_OH_6SO4 = MineralSecondarySpecies(symbol = "Pb4(OH)6SO4",\
                               formationReaction = [("Pb+2",4),("SO4-2",1),("H2O",6),("H+",-6)],\
                               logK25 = 21.1,\
                               name = "Pb4(OH)6SO4",)
speciesAddenda.append(Pb4_OH_6SO4)
#
# Alamosite
#
alamosite = MineralSecondarySpecies(symbol = "PbSiO3",\
                               formationReaction = [("Pb+2",1),("SiO2",1),("H2O",1),("H+",-2)],\
                               logK25 = 5.6733,\
                               logK = [2.9941e+002, 6.7871e-002, -8.1706e+003, -1.1582e+002, -1.3885e+002],\
                               name = "Alamosite",)
speciesAddenda.append(alamosite)
#
# Pb2SiO4
#
Pb2SiO4 = MineralSecondarySpecies(symbol = "Pb2SiO4",\
                               formationReaction = [("Pb+2",2),("SiO2",1),("H2O",2),("H+",-4)],\
                               logK25 = 18.0370,\
                               logK = [2.7287e+002, 6.3875e-002, -3.7001e+003, -1.0568e+002, -6.2927e+001],\
                               name = "Pb2SiO4",)
speciesAddenda.append(Pb2SiO4)








#
# Kaolinite
#
kaolinite = MineralSecondarySpecies(symbol = "Al2Si2O5(OH)4",\
                               formationReaction = [("Al+++",2),("SiO2",2),("H2O",5),("H+",-6)],\
                               logK25 = 6.8101,\
                               logK = [1.6835e+001, -7.8939e-003, 7.7636e+003, -1.2190e+001, -3.2354e+005],\
                               name = "Kaolinite",)
speciesAddenda.append(kaolinite)
#
# Illite
#
illite = MineralSecondarySpecies(symbol = "K0.6Mg0.25Al1.8Al0.5Si3.5O10(OH)2",\
                               formationReaction = [("Mg++",0.25),("K+",0.6),("Al+++",2.3),("SiO2",3.5),("H2O",5),("H+",-8)],\
                               logK25 = 9.0260,\
                               logK = [2.6069e+001, -1.2553e-003, 1.3670e+004, -2.0232e+001, -1.1204e+006],\
                               name = "Illite",)
speciesAddenda.append(illite)
#
# Albite
#
albite = MineralSecondarySpecies(symbol = "NaAlSi3O8",\
                               formationReaction = [("Al+++",1),("Na+",1),("SiO2",3),("H2O",2),("H+",-4)],\
                               logK25 = 2.7645,\
                               logK = [-1.1694e+001, 1.4429e-002, 1.3784e+004, -7.2866e+000, -1.6136e+006],\
                               name = "Albite",)
speciesAddenda.append(albite)
#
# Anorthite
#
anorthite = MineralSecondarySpecies(symbol = "CaAl2(SiO4)2",\
                               formationReaction = [("Ca++",1),("Al+++",2),("SiO2",2),("H2O",4),("H+",-8)],\
                               logK25 = 26.5780,\
                               logK = [3.9717e-001, -1.8751e-002, 1.4897e+004, -6.3078e+000, -2.3885e+005],\
                               name = "Anorthite",)
speciesAddenda.append(anorthite)
#
# Gibbsite
#
gibbsite = MineralSecondarySpecies(symbol = "Al(OH)3",\
                               formationReaction = [("Al+3",1),("H2O",3),("H+",-3)],\
                               logK25 = 8.11,\
                               name = "Gibbsite",)
speciesAddenda.append(gibbsite)
#
# Al(OH)3(a)
#
hydrargillite = MineralSecondarySpecies(symbol = "Al(OH)3",\
                               formationReaction = [("Al+3",1),("H2O",3),("H+",-3)],\
                               logK25 = 10.8,\
                               name = "Al(OH)3(a)",)
speciesAddenda.append(hydrargillite)
#
# Barite
#
barite = MineralSecondarySpecies(symbol = "BaSO4",\
                               formationReaction = [("Ba+2",1),("SO4--",1)],\
                               logK25 = -9.9711,\
                               logK = [-1.8747e+002, -7.5521e-002, 2.0790e+003, 7.7998e+001, 3.2497e+001],\
                               name = "Barite",)
speciesAddenda.append(barite)
#
# Anhydrite
#
anhydrite = MineralSecondarySpecies(symbol = "CaSO4",\
                               formationReaction = [("Ca+2",1),("SO4--",1)],\
                               logK25 = -4.362,\
                               logK = [-2.0986e+002, -7.8823e-002, 5.0969e+003, 8.5642e+001, 7.9594e+001],\
                               name = "Anhydrite",)
speciesAddenda.append(anhydrite)
#
# Gypsum
#
gypsum = MineralSecondarySpecies(symbol = "CaSO4:2H2O",\
                               formationReaction = [("Ca+2",1),("SO4--",1),("H2O",2)],\
                               logK25 = -4.4823,\
                               logK = [-2.4417e+002, -8.3329e-002, 5.5958e+003, 9.9301e+001, 8.7389e+001],\
                               name = "Gypsum",)
speciesAddenda.append(gypsum)
                                                                                            #
                                                                                            # gases
                                                                                            #
#
# O2(g)
#
o2g = MineralSecondarySpecies(symbol = "O2",\
                               formationReaction = [("O2",1)],\
                               logK25 = -2.8983,\
                               logK = [-7.5001, 7.8981e-003, 0.0, 0.0, 2.0027e+005],\
                               name = "O2(g)",)
speciesAddenda.append(o2g)
#
# H2(g)
#
h2g = MineralSecondarySpecies(symbol = "H2",\
                               formationReaction = [("H2O",1),("O2",-0.5)],\
                               logK25 = 43.0016,\
                               logK = [-1.1609e+001, -3.7580e-003, 1.5068e+004, 2.4198e+000, -7.0997e+004],\
                               name = "H2(g)",)
speciesAddenda.append(h2g)
#
# N2(g)
#
n2g = MineralSecondarySpecies(symbol = "N2",\
                               formationReaction = [("N2",1)],\
                               logK25 = -3.1864,\
                               logK = [-58.453, 1.81800E-03,  3199,  17.909, -27460],\
                               name = "N2(g)",)
speciesAddenda.append(n2g)
#
# H2S(g)
#
h2Sg = MineralSecondarySpecies(symbol = "H2S",\
                               formationReaction = [("H+",1),("HS-",1)],\
                               logK25 = -7.9759,\
                               logK = [-9.7354e+001, -3.1576e-002, 1.8285e+003, 3.7440e+001, 2.8560e+001],\
                               name = "H2S(g)",)
speciesAddenda.append(h2Sg)
#
# CH4(g)
#
CH4g = MineralSecondarySpecies(symbol = "CH4",\
                               formationReaction = [("CH4",1)],\
                               logK25 = -2.964,\
                               name = "CH4(g)",)
speciesAddenda.append(CH4g)
#
# NH3(g)
#
NH3g = MineralSecondarySpecies(symbol = "NH3",\
                                 formationReaction = [("NH3",1)],\
                                 logK25 = 1.770,\
                                 name = "NH3(g)")
speciesAddenda.append(NH3g)
#
# CO2(g)
#
CO2g = MineralSecondarySpecies(symbol = "CO2",\
                                 formationReaction = [("CO2",1)],\
                                 logK25 = -1.468,\
                                 logK = [108.3865, 0.01985076, -6919.53, -40.45154, 669365],\
                                 name = "CO2(g)")
speciesAddenda.append(CO2g)
#
# and now salts
#
#
# HS-
#
speciesAddenda.append(Salt(("HS-","Na+" ), b0 = -0.103, b1 = 0.884, description = "Millero 1986"))
speciesAddenda.append(Salt(("HS-","K+"  ), b0 = -0.337, b1 = 0.884, description = "Millero 1986"))
speciesAddenda.append(Salt(("HS-","Mg+2"), b0 =  0.466, b1 = 2.264, description = "Millero 1986"))
speciesAddenda.append(Salt(("HS-","Ca+2"), b0 =  0.069, b1 = 2.264, description = "Millero 1986"))
#
# Ba+2
#
speciesAddenda.append(Salt(("Ba+2","SO4-2" ), b0 = 0.22,   b1 = 2.88, b2 = -41.8, c0 = 0.19, description = "From Pitzer 91, Reardon 90"))
speciesAddenda.append(Salt(("Ba+2","HSO4-" ), b0 = 0.2145, b1 = 2.53, b2 =   0.0, c0 = 0.0 , description = "From Harvie et al.84 (Ca) "))


