from chemistry import *
from chemicalmodule import *
from phreeqc import *

Phreeqc_file = "clay.txt"      # bounded to Phreeqc
ProblemName  = "clay"          # Phreeqc file 
#~~~~~~~~~~~~~~~~~~~
# Chemical Addenda ~
#~~~~~~~~~~~~~~~~~~~
speciesAddenda = []
Na = AqueousMasterSpecies(symbol = "Na+",\
                          name = "Na",\
                          element = "Na",\
                          molarMass = MolarMass(22.9898,"g/mol"),\
                          alkalinity = 0.0)
speciesAddenda.append(Na)
C = AqueousMasterSpecies(symbol = "CO3-2",\
                         name = "C",\
                         element = "HCO3",\
                         molarMass = MolarMass(12.0111,"g/mol"),\
                         alkalinity = 2.0)
speciesAddenda.append(C)
Tr = AqueousMasterSpecies(symbol = "Tr",\
                          name = "Tr",\
                          element = "Tr",\
                          molarMass = MolarMass(1.008,"g/mol"),\
                          alkalinity = 0.0)
speciesAddenda.append(Tr)
Ca = AqueousMasterSpecies(symbol = "Ca++",\
                          name = "Ca",\
                          element = "Ca",\
                          molarMass = MolarMass(40.08,"g/mol"),\
                          alkalinity = 0.0)
speciesAddenda.append(Ca)
Cl = AqueousMasterSpecies(symbol = "Cl-",\
                          name = "Cl",\
                          element = "Cl",\
                          molarMass = MolarMass(35.453,"g/mol"),\
                          alkalinity = 0.0)
speciesAddenda.append(Cl)
NaHCO3SSp = AqueousSecondarySpecies(symbol = "NaHCO3",\
                                    formationReaction = [("Na+",1),("CO3-2",1),("H+",1)],\
                                    logK25 = 10.079,\
                                    name = "NaHCO3",)
speciesAddenda.append(NaHCO3SSp)
CSSp = AqueousSecondarySpecies(symbol = "CO3-2",\
                               formationReaction = [("CO3-2",1)],\
                               logK25 = 0.0,\
                               name = "C",)
speciesAddenda.append(CSSp)
CO2SSp = AqueousSecondarySpecies(symbol = "CO2",\
                                 formationReaction = [("CO3-2",1),("H+",2),("H2O",-1)],\
                                 logK25 = 16.6807,\
                                 name = "CO2",)
speciesAddenda.append(CO2SSp)
NaCO3minSSp = AqueousSecondarySpecies(symbol = "NaCO3-",\
                                      formationReaction = [("Na+",1),("CO3--",1)],\
                                      logK25 = 1.27,\
                                      name = "NaCO3min",)
speciesAddenda.append(NaCO3minSSp)
NaOHSSp = AqueousSecondarySpecies(symbol = "NaOH",\
                                  formationReaction = [("Na+",1),("H2O",1),("H+",-1)],\
                                  logK25 = -14.18,\
                                  name = "NaOH",)
speciesAddenda.append(NaOHSSp)
ClSSp = AqueousSecondarySpecies(symbol = "Cl-",\
                                formationReaction = [("Cl-",1)],\
                                logK25 = 0.0,\
                                name = "Cl",)
speciesAddenda.append(ClSSp)
HCO3minSSp = AqueousSecondarySpecies(symbol = "HCO3-",\
                                     formationReaction = [("CO3-2",1),("H+",1)],\
                                     logK25 = 10.3289,\
                                     name = "HCO3min",)
speciesAddenda.append(HCO3minSSp)
NaSSp = AqueousSecondarySpecies(symbol = "Na+",\
                                formationReaction = [("Na+",1)],\
                                logK25 = 0.0,\
                                name = "Na",)
speciesAddenda.append(NaSSp)
CaSSp = AqueousSecondarySpecies(symbol = "Ca++",\
                                formationReaction = [("Ca++",1)],\
                                logK25 = 0.0,\
                                name = "Ca",)
speciesAddenda.append(CaSSp)
CaHCO3SSp = AqueousSecondarySpecies(symbol = "CaHCO3+",\
                                    formationReaction = [("Ca++",1),("CO3--",1),("H+",1)],\
                                    logK25 = 11.4347,\
                                    name = "CaHCO3",)
speciesAddenda.append(CaHCO3SSp)
CaCO3SSp = AqueousSecondarySpecies(symbol = "CaCO3",\
                                   formationReaction = [("Ca++",1),("CO3--",1)],\
                                   logK25 = 3.22528,\
                                   name = "CaCO3",)
speciesAddenda.append(CaCO3SSp)
HCO3SSp = AqueousSecondarySpecies(symbol = "CO3-2",\
                                  formationReaction = [("CO3-2",1)],\
                                  logK25 = 0.0,\
                                  name = "HCO3",)
speciesAddenda.append(HCO3SSp)
TrSSp = AqueousSecondarySpecies(symbol = "Tr",\
                                formationReaction = [("Tr",1)],\
                                logK25 = 0.0,\
                                name = "Tr",)
speciesAddenda.append(TrSSp)
CaOHpSSp = AqueousSecondarySpecies(symbol = "CaOH+",\
                                   formationReaction = [("Ca++",1),("H2O",1),("H+",-1)],\
                                   logK25 = -12.78,\
                                   name = "CaOH+",)
speciesAddenda.append(CaOHpSSp)
Fix_HpAd = MineralSecondarySpecies(symbol = "H+",\
                                   formationReaction = [("H+",1)],\
                                   logK25 = 0.0,\
                                   name = "Fix_H+")
speciesAddenda.append(Fix_HpAd)
H2gAd = MineralSecondarySpecies(symbol = "H2",\
                                formationReaction = [("H2",1)],\
                                logK25 = -3.15,\
                                name = "H2(g)")
speciesAddenda.append(H2gAd)
O2gAd = MineralSecondarySpecies(symbol = "O2",\
                                formationReaction = [("O2",1)],\
                                logK25 = -2.96,\
                                name = "O2(g)")
speciesAddenda.append(O2gAd)
H2OgAd = MineralSecondarySpecies(symbol = "H2O",\
                                 formationReaction = [("H2O",1)],\
                                 logK25 = 1.51,\
                                 name = "H2O(g)")
speciesAddenda.append(H2OgAd)
AragoniteAd = MineralSecondarySpecies(symbol = "CaCO3",\
                                      formationReaction = [("Ca+2",1),("CO3-2",1)],\
                                      logK25 = -8.33606,\
                                      name = "Aragonite")
speciesAddenda.append(AragoniteAd)
CO2gAd = MineralSecondarySpecies(symbol = "CO2",\
                                 formationReaction = [("H2O",-1),("CO3--",1),("H+",2)],\
                                 logK25 = -18.1487,\
                                 name = "CO2(g)")
speciesAddenda.append(CO2gAd)
HaliteAd = MineralSecondarySpecies(symbol = "NaCl",\
                                   formationReaction = [("Na+",1),("Cl-",1)],\
                                   logK25 = 1.582,\
                                   name = "Halite")
speciesAddenda.append(HaliteAd)
PortlanditeAd = MineralSecondarySpecies(symbol = "Ca(OH)2",\
                                        formationReaction = [("Ca+2",1),("OH-",2)],\
                                        logK25 = -5.4448,\
                                        name = "Portlandite")
speciesAddenda.append(PortlanditeAd)
CalciteAd = MineralSecondarySpecies(symbol = "CaCO3",\
                                    formationReaction = [("Ca+2",1),("CO3-2",1)],\
                                    logK25 = -8.47983,\
                                    name = "Calcite")
speciesAddenda.append(CalciteAd)
#~~~~~~~~~~~~~~~~~
# Chemical State ~
#~~~~~~~~~~~~~~~~~
ChemicalStateList = []
clayMineralPhase = MineralPhase([MineralTotalConcentration("Calcite",2.8954e-3, "mol/l",saturationIndex = 0.0),
                                MineralTotalConcentration("Portlandite",0.0, "mol/l",saturationIndex = 0.0),
                                MineralTotalConcentration("Aragonite",0.0, "mol/l",saturationIndex = 0.0),
                                MineralTotalConcentration("Halite",0.0, "mol/l",saturationIndex = 0.0),
                                MineralTotalConcentration("CO2(g)",1.0, "mol/l",saturationIndex = -2.54),
                                MineralTotalConcentration("H2O(g)",1.0, "mol/l",saturationIndex = -1.4)])
clayAqueousSolution = AqueousSolution (elementConcentrations = [ElementConcentration ("Ca",2.7e-3,"mol/l"),
                                                                ElementConcentration ("Cl",1.e-2,"mol/l"),
                                                                ElementConcentration ("C",4.5e-3,"mol/l"),
                                                                ElementConcentration ("Na",8.e-3,"mol/l"),
                                                                ElementConcentration ("Tr",1.e-2,"mol/l")
                                                               ],\
                                       pH = 7.5,\
                                       pe = 4)
clayChemicalState = ChemicalState ("clay",clayAqueousSolution,mineralPhase = clayMineralPhase,phFixed = ("HCl",7.5))

#~~~~~~~~~
# Module ~
#~~~~~~~~~
module = Chemical()
problem  = ChemicalProblem(name               = "clay",\
                           chemistryDB        = "phreeqc.dat",\
                           speciesBaseAddenda = speciesAddenda,\
                           chemicalState      = clayChemicalState)
module.setData(problem)
module.initialise()
module.setParameter("clay.out")
module.run()
module.outputStateSaving()

print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "        End of the clay case ~"
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
