from chemistry import *
from chemicalmodule import *
from phreeqc import *

Phreeqc_file = "Acidified_max.txt"      # bounded to Phreeqc
ProblemName  = "Acidified_max"          # Phreeqc file 
#~~~~~~~~~~~~~~~~~~~
# Chemical Addenda ~
#~~~~~~~~~~~~~~~~~~~
speciesAddenda = []
S = AqueousMasterSpecies(symbol = "SO4--",\
                         name = "S",\
                         element = "S04--",\
                         molarMass = MolarMass(32.066,"g/mol"),\
                         alkalinity = 0)
speciesAddenda.append(S)
C = AqueousMasterSpecies(symbol = "HCO3-",\
                         name = "C",\
                         element = "HCO3-",\
                         molarMass = MolarMass(12.011,"g/mol"),\
                         alkalinity = 1)
speciesAddenda.append(C)
C_m3_ = AqueousMasterSpecies(symbol = "C2H6",\
                             name = "C(-3)",\
                             element = "C2H6",\
                             molarMass = MolarMass(12.011,"g/mol"),\
                             alkalinity = 0)
speciesAddenda.append(C_m3_)
C_p4_ = AqueousMasterSpecies(symbol = "HCO3-",\
                             name = "C(+4)",\
                             element = "HCO3-",\
                             molarMass = MolarMass(12.011,"g/mol"),\
                             alkalinity = 0)
speciesAddenda.append(C_p4_)
Na = AqueousMasterSpecies(symbol = "Na+",\
                          name = "Na",\
                          element = "Na+",\
                          molarMass = MolarMass(22.9898,"g/mol"),\
                          alkalinity = 0)
speciesAddenda.append(Na)
Ca = AqueousMasterSpecies(symbol = "Ca++",\
                          name = "Ca",\
                          element = "Ca++",\
                          molarMass = MolarMass(40.078,"g/mol"),\
                          alkalinity = 0)
speciesAddenda.append(Ca)
Cl = AqueousMasterSpecies(symbol = "Cl-",\
                          name = "Cl",\
                          element = "Cl-",\
                          molarMass = MolarMass(35.4527,"g/mol"),\
                          alkalinity = 0)
speciesAddenda.append(Cl)
Al = AqueousMasterSpecies(symbol = "Al+++",\
                          name = "Al",\
                          element = "Al+++",\
                          molarMass = MolarMass(26.9815,"g/mol"),\
                          alkalinity = 0)
speciesAddenda.append(Al)
Fe_p2_ = AqueousMasterSpecies(symbol = "Fe++",\
                              name = "Fe(+2)",\
                              element = "Fe",\
                              molarMass = MolarMass(55.847,"g/mol"),\
                              alkalinity = 0)
speciesAddenda.append(Fe_p2_)
Mg = AqueousMasterSpecies(symbol = "Mg++",\
                          name = "Mg",\
                          element = "Mg++",\
                          molarMass = MolarMass(24.305,"g/mol"),\
                          alkalinity = 0)
speciesAddenda.append(Mg)
Si = AqueousMasterSpecies(symbol = "SiO2",\
                          name = "Si",\
                          element = "SiO2",\
                          molarMass = MolarMass(28.0855,"g/mol"),\
                          alkalinity = 0)
speciesAddenda.append(Si)
Fe_p3_ = AqueousMasterSpecies(symbol = "Fe+3",\
                              name = "Fe(+3)",\
                              element = "Fe",\
                              molarMass = MolarMass(55.847,"g/mol"),\
                              alkalinity = -2)
speciesAddenda.append(Fe_p3_)
S_m2_ = AqueousMasterSpecies(symbol = "HS-",\
                             name = "S(-2)",\
                             element = "S",\
                             molarMass = MolarMass(32.066,"g/mol"),\
                             alkalinity = 1)
speciesAddenda.append(S_m2_)
Fe = AqueousMasterSpecies(symbol = "Fe+2",\
                          name = "Fe",\
                          element = "Fe+2",\
                          molarMass = MolarMass(55.847,"g/mol"),\
                          alkalinity = 0)
speciesAddenda.append(Fe)
S_p6_ = AqueousMasterSpecies(symbol = "SO4-2",\
                             name = "S(+6)",\
                             element = "SO4",\
                             molarMass = MolarMass(32.066,"g/mol"),\
                             alkalinity = 0)
speciesAddenda.append(S_p6_)
K = AqueousMasterSpecies(symbol = "K+",\
                         name = "K",\
                         element = "K+",\
                         molarMass = MolarMass(39.0983,"g/mol"),\
                         alkalinity = 0)
speciesAddenda.append(K)
NaHCO3SSp = AqueousSecondarySpecies(symbol = "NaHCO3",\
                                    formationReaction = [("HCO3-",1),("Na+",1)],\
                                    logK25 = -0.262432112033,\
                                    name = "NaHCO3",)
speciesAddenda.append(NaHCO3SSp)
MgClpSSp = AqueousSecondarySpecies(symbol = "MgCl+",\
                                   formationReaction = [("Mg+2",1),("Cl-",1)],\
                                   logK25 = 0.043022426443,\
                                   name = "MgCl+",)
speciesAddenda.append(MgClpSSp)
FeHCO3pSSp = AqueousSecondarySpecies(symbol = "FeHCO3+",\
                                     formationReaction = [("HCO3-",1),("Fe++",1)],\
                                     logK25 = 2.72,\
                                     name = "FeHCO3+",)
speciesAddenda.append(FeHCO3pSSp)
AlO2H2pSSp = AqueousSecondarySpecies(symbol = "Al(OH)2+",\
                                     formationReaction = [("2.0000H2O",1),("1.0000Al+++",1),("2.0000H+",-1)],\
                                     logK25 = -7.82750693541,\
                                     name = "AlO2H2+",)
speciesAddenda.append(AlO2H2pSSp)
ClmSSp = AqueousSecondarySpecies(symbol = "Cl-",\
                                 formationReaction = [("Cl-",1)],\
                                 logK25 = 0,\
                                 name = "Cl-",)
speciesAddenda.append(ClmSSp)
KpSSp = AqueousSecondarySpecies(symbol = "K+",\
                                formationReaction = [("K+",1)],\
                                logK25 = 0,\
                                name = "K+",)
speciesAddenda.append(KpSSp)
HCO3mSSp = AqueousSecondarySpecies(symbol = "HCO3-",\
                                   formationReaction = [("HCO3-",1)],\
                                   logK25 = 0,\
                                   name = "HCO3-",)
speciesAddenda.append(HCO3mSSp)
HAlO2SSp = AqueousSecondarySpecies(symbol = "HAlO2",\
                                   formationReaction = [("2H2O",1),("Al+3",1),("3H+",-1)],\
                                   logK25 = -12.3935736616,\
                                   name = "HAlO2",)
speciesAddenda.append(HAlO2SSp)
MgCO3SSp = AqueousSecondarySpecies(symbol = "MgCO3",\
                                   formationReaction = [("Mg+2",1),("HCO3-",1),("H+",-1)],\
                                   logK25 = -6.73391939216,\
                                   name = "MgCO3",)
speciesAddenda.append(MgCO3SSp)
MgppSSp = AqueousSecondarySpecies(symbol = "Mg++",\
                                  formationReaction = [("Mg++",1)],\
                                  logK25 = 0,\
                                  name = "Mg++",)
speciesAddenda.append(MgppSSp)
Fep3SSp = AqueousSecondarySpecies(symbol = "Fe+3",\
                                  formationReaction = [("H+",1),("Fe+2",1),("0.25O2",1),("0.5H2O",-1)],\
                                  logK25 = 5.75769296065,\
                                  name = "Fe+3",)
speciesAddenda.append(Fep3SSp)
NaCO3mSSp = AqueousSecondarySpecies(symbol = "NaCO3-",\
                                    formationReaction = [("Na+",1),("HCO3-",1),("H+",-1)],\
                                    logK25 = -10.3336440843,\
                                    name = "NaCO3-",)
speciesAddenda.append(NaCO3mSSp)
NaAlO2SSp = AqueousSecondarySpecies(symbol = "NaAlO2",\
                                    formationReaction = [("2H2O",1),("Na+",1),("Al+3",1),("4H+",-1)],\
                                    logK25 = -18.3804563569,\
                                    name = "NaAlO2",)
speciesAddenda.append(NaAlO2SSp)
FeSO4SSp = AqueousSecondarySpecies(symbol = "FeSO4",\
                                   formationReaction = [("SO4-2",1),("Fe+2",1)],\
                                   logK25 = 2.2,\
                                   name = "FeSO4",)
speciesAddenda.append(FeSO4SSp)
FeCO3SSp = AqueousSecondarySpecies(symbol = "FeCO3",\
                                   formationReaction = [("HCO3-",1),("Fe+2",1),("H+",-1)],\
                                   logK25 = -5.5988,\
                                   name = "FeCO3",)
speciesAddenda.append(FeCO3SSp)
Alp3SSp = AqueousSecondarySpecies(symbol = "Al+3",\
                                  formationReaction = [("Al+3",1)],\
                                  logK25 = 0,\
                                  name = "Al+3",)
speciesAddenda.append(Alp3SSp)
NapSSp = AqueousSecondarySpecies(symbol = "Na+",\
                                 formationReaction = [("Na+",1)],\
                                 logK25 = 0,\
                                 name = "Na+",)
speciesAddenda.append(NapSSp)
SiO2SSp = AqueousSecondarySpecies(symbol = "SiO2",\
                                  formationReaction = [("SiO2",1)],\
                                  logK25 = 0,\
                                  name = "SiO2",)
speciesAddenda.append(SiO2SSp)
CaCO3SSp = AqueousSecondarySpecies(symbol = "CaCO3",\
                                   formationReaction = [("HCO3-",1),("Ca+2",1),("H+",-1)],\
                                   logK25 = -6.19805423401,\
                                   name = "CaCO3",)
speciesAddenda.append(CaCO3SSp)
HSmSSp = AqueousSecondarySpecies(symbol = "HS-",\
                                 formationReaction = [("SO4--",1),("H+",1),("2O2",-1)],\
                                 logK25 = -114.216697752,\
                                 name = "HS-",)
speciesAddenda.append(HSmSSp)
CappSSp = AqueousSecondarySpecies(symbol = "Ca++",\
                                  formationReaction = [("Ca++",1)],\
                                  logK25 = 0,\
                                  name = "Ca++",)
speciesAddenda.append(CappSSp)
MgHCO3pSSp = AqueousSecondarySpecies(symbol = "MgHCO3+",\
                                     formationReaction = [("HCO3-",1),("Mg+2",1)],\
                                     logK25 = 1.28060426324,\
                                     name = "MgHCO3+",)
speciesAddenda.append(MgHCO3pSSp)
C2H6SSp = AqueousSecondarySpecies(symbol = "C2H6",\
                                  formationReaction = [("2H+",1),("2HCO3-",1),("H2O",1),("3.5O2",-1)],\
                                  logK25 = -190.328178147,\
                                  name = "C2H6",)
speciesAddenda.append(C2H6SSp)
CaSO4SSp = AqueousSecondarySpecies(symbol = "CaSO4",\
                                   formationReaction = [("1.0000SO4--",1),("1.0000Ca++",1)],\
                                   logK25 = 2.38766577473,\
                                   name = "CaSO4",)
speciesAddenda.append(CaSO4SSp)
Fep2SSp = AqueousSecondarySpecies(symbol = "Fe+2",\
                                  formationReaction = [("Fe+2",1)],\
                                  logK25 = 0,\
                                  name = "Fe+2",)
speciesAddenda.append(Fep2SSp)
CO3m2SSp = AqueousSecondarySpecies(symbol = "CO3-2",\
                                   formationReaction = [("HCO3-",1),("H+",-1)],\
                                   logK25 = -10.0847264775,\
                                   name = "CO3-2",)
speciesAddenda.append(CO3m2SSp)
CaHCO3pSSp = AqueousSecondarySpecies(symbol = "CaHCO3+",\
                                     formationReaction = [("HCO3-",1),("Ca+2",1)],\
                                     logK25 = 1.27037886237,\
                                     name = "CaHCO3+",)
speciesAddenda.append(CaHCO3pSSp)
FeCO3pSSp = AqueousSecondarySpecies(symbol = "FeCO3+",\
                                    formationReaction = [("HCO3-",1),("Fe+3",1),("H+",-1)],\
                                    logK25 = -1.71081325409,\
                                    name = "FeCO3+",)
speciesAddenda.append(FeCO3pSSp)
CO2SSp = AqueousSecondarySpecies(symbol = "CO2",\
                                 formationReaction = [("HCO3-",1),("H+",1),("H2O",-1)],\
                                 logK25 = 6.30229680369,\
                                 name = "CO2",)
speciesAddenda.append(CO2SSp)
SO4mmSSp = AqueousSecondarySpecies(symbol = "SO4--",\
                                   formationReaction = [("SO4--",1)],\
                                   logK25 = 0,\
                                   name = "SO4--",)
speciesAddenda.append(SO4mmSSp)
MgSO4SSp = AqueousSecondarySpecies(symbol = "MgSO4",\
                                   formationReaction = [("Mg+2",1),("SO4-2",1)],\
                                   logK25 = 3.08132980277,\
                                   name = "MgSO4",)
speciesAddenda.append(MgSO4SSp)
AlO2mSSp = AqueousSecondarySpecies(symbol = "AlO2-",\
                                   formationReaction = [("2H2O",1),("Al+3",1),("4H+",-1)],\
                                   logK25 = -17.9888941868,\
                                   name = "AlO2-",)
speciesAddenda.append(AlO2mSSp)
DolomitemdisAd = MineralSecondarySpecies(symbol = "CaMg(CO3)2",\
                                         formationReaction = [("2H+",-1),("Ca++",1),("Mg++",1),("2HCO3-",1)],\
                                         logK25 = 1.92,\
                                         name = "Dolomite-dis")
speciesAddenda.append(DolomitemdisAd)
AnkeriteAd = MineralSecondarySpecies(symbol = "CaMg0.3Fe0.7C2O6",\
                                     formationReaction = [("4H+",-1),("Ca++",1),("0.3Mg++",1),("0.7Fe++",1),("2H2O",1),("2CO2",1)],\
                                     logK25 = 12.14,\
                                     name = "Ankerite")
speciesAddenda.append(AnkeriteAd)
IlliteAd = MineralSecondarySpecies(symbol = "K0.6Mg0.25Al1.8Al0.5Si3.5O10(OH)2",\
                                   formationReaction = [("8H+",-1),("0.25Mg++",1),("0.6K+",1),("2.3Al+3",1),("3.5SiO2",1),("5H2O",1)],\
                                   logK25 = 3.8,\
                                   name = "Illite")
speciesAddenda.append(IlliteAd)
ChalcedonyAd = MineralSecondarySpecies(symbol = "SiO2",\
                                       formationReaction = [("SiO2",1)],\
                                       logK25 = -3.02,\
                                       name = "Chalcedony")
speciesAddenda.append(ChalcedonyAd)
AnhydriteAd = MineralSecondarySpecies(symbol = "CaSO4",\
                                      formationReaction = [("Ca++",1),("SO4--",1)],\
                                      logK25 = -5.05,\
                                      name = "Anhydrite")
speciesAddenda.append(AnhydriteAd)
KaoliniteAd = MineralSecondarySpecies(symbol = "Al2Si2O5(OH)4",\
                                      formationReaction = [("6H+",-1),("2Al+++",1),("2SiO2",1),("5H2O",1)],\
                                      logK25 = 2.38,\
                                      name = "Kaolinite")
speciesAddenda.append(KaoliniteAd)
CO2_g_Ad = MineralSecondarySpecies(symbol = "CO2",\
                                   formationReaction = [("CO2",1)],\
                                   logK25 = -1.89865961392,\
                                   name = "CO2(g)")
speciesAddenda.append(CO2_g_Ad)
QuartzAd = MineralSecondarySpecies(symbol = "SiO2",\
                                   formationReaction = [("SiO2",1)],\
                                   logK25 = -3.24,\
                                   name = "Quartz")
speciesAddenda.append(QuartzAd)
MontmormCaAd = MineralSecondarySpecies(symbol = "Ca.165Mg.33Al1.67Si4O10(OH)2",\
                                       formationReaction = [("6H+",-1),("0.165Ca+2",1),("0.33Mg+2",1),("1.67Al+3",1),("4H2O",1),("4SiO2",1)],\
                                       logK25 = -0.830933464616,\
                                       name = "Montmor-Ca")
speciesAddenda.append(MontmormCaAd)
CalciteAd = MineralSecondarySpecies(symbol = "CaCO3",\
                                    formationReaction = [("H+",-1),("Ca++",1),("HCO3-",1)],\
                                    logK25 = 1.05,\
                                    name = "Calcite")
speciesAddenda.append(CalciteAd)
SideriteAd = MineralSecondarySpecies(symbol = "FeCO3",\
                                     formationReaction = [("H+",-1),("Fe++",1),("HCO3-",1)],\
                                     logK25 = -1.17,\
                                     name = "Siderite")
speciesAddenda.append(SideriteAd)
MontmormNaAd = MineralSecondarySpecies(symbol = "Na.33Mg.33Al1.67Si4O10(OH)2",\
                                       formationReaction = [("6H+",-1),("0.33Mg++",1),("0.33Na+",1),("1.67Al+++",1),("4H2O",1),("4SiO2",1)],\
                                       logK25 = -0.65,\
                                       name = "Montmor-Na")
speciesAddenda.append(MontmormNaAd)
GoethiteAd = MineralSecondarySpecies(symbol = "FeOOH",\
                                     formationReaction = [("3H+",-1),("Fe+++",1),("2H2O",1)],\
                                     logK25 = -1.13,\
                                     name = "Goethite")
speciesAddenda.append(GoethiteAd)
PyriteAd = MineralSecondarySpecies(symbol = "FeS2",\
                                   formationReaction = [("H2O",-1),("0.25H+",1),("0.25SO4--",1),("Fe++",1),("1.75HS-",1)],\
                                   logK25 = -21.91,\
                                   name = "Pyrite")
speciesAddenda.append(PyriteAd)
#~~~~~~~~~~~~~~~~~
# Chemical State ~
#~~~~~~~~~~~~~~~~~
ChemicalStateList = []
Acidified_maxMineralPhase = MineralPhase([MineralTotalConcentration("CO2(g)",10, "mol/l",saturationIndex = 1.919)])
Acidified_maxAqueousSolution = AqueousSolution (elementConcentrations = [ElementConcentration ("Al",2.18e-8,"mol/l"),
                                                                         ElementConcentration ("C",1.00,"mol/l"),
                                                                         ElementConcentration ("Ca",4.22e-2,"mol/l"),
                                                                         ElementConcentration ("Cl",1.92e-1,"mol/l"),
                                                                         ElementConcentration ("Fe",1.22e-5,"mol/l"),
                                                                         ElementConcentration ("K",1.85e-2,"mol/l"),
                                                                         ElementConcentration ("Mg",1.12e-2,"mol/l"),
                                                                         ElementConcentration ("Na",8.00e-2,"mol/l"),
                                                                         ElementConcentration ("S",6.16e-3,"mol/l"),
                                                                         ElementConcentration ("Si",6.55e-4,"mol/l")
                                                                        ],\
                                                pH = 3.36,\
                                                temperature =80,\
                                                pe = 4)
Acidified_maxChemicalState = ChemicalState ("Acidified_max",Acidified_maxAqueousSolution,mineralPhase = Acidified_maxMineralPhase)

#~~~~~~~~~
# Module ~
#~~~~~~~~~
module = Chemical()
problem  = ChemicalProblem(name               = "Acidified_max",\
                           chemistryDB        = "water_gui.dat",\
                           speciesBaseAddenda = speciesAddenda,\
                           chemicalState      = Acidified_maxChemicalState)
module.setData(problem)
module.initialise()
module.setParameter("Acidified_max.out")
module.run()
module.outputStateSaving()

print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "        End of the Acidified_max case ~"
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
