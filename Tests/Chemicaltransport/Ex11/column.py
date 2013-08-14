from chemistry import *
from chemicalmodule import *
from phreeqc import *

Phreeqc_file = "column.txt"      # bounded to Phreeqc
ProblemName  = "column"          # Phreeqc file 
#~~~~~~~~~~~~~~~~~~~
# Chemical Addenda ~
#~~~~~~~~~~~~~~~~~~~
speciesAddenda = []
Cl = AqueousMasterSpecies(symbol = "Cl-",\
                          name = "Cl",\
                          element = "Cl",\
                          molarMass = MolarMass(35.4532,"g/mol"),\
                          alkalinity = 0.0)
speciesAddenda.append(Cl)
Na = AqueousMasterSpecies(symbol = "Na+",\
                          name = "Na",\
                          element = "Na",\
                          molarMass = MolarMass(22.9898,"g/mol"),\
                          alkalinity = 0.0)
speciesAddenda.append(Na)
Ca = AqueousMasterSpecies(symbol = "Ca++",\
                          name = "Ca",\
                          element = "Ca",\
                          molarMass = MolarMass(40.08,"g/mol"),\
                          alkalinity = 0.0)
speciesAddenda.append(Ca)
N = AqueousMasterSpecies(symbol = "NO3-",\
                         name = "N",\
                         element = "N",\
                         molarMass = MolarMass(14.067,"g/mol"),\
                         alkalinity = 0.0)
speciesAddenda.append(N)
NAMS = AqueousMasterSpecies(symbol = "N2",\
                             name = "N(+3)",\
                             element = "N",\
                             molarMass = MolarMass(14.067,"g/mol"),\
                             alkalinity = 0)
speciesAddenda.append(NAMS)
K = AqueousMasterSpecies(symbol = "K+",\
                         name = "K",\
                         element = "K",\
                         molarMass = MolarMass(39.102,"g/mol"),\
                         alkalinity = 0.0)
speciesAddenda.append(K)
Np5AMS = AqueousMasterSpecies(symbol = "NO3-",\
                             name = "N(+5)",\
                             element = "N",\
                             molarMass = MolarMass(14.067,"g/mol"),\
                             alkalinity = 0.0)
speciesAddenda.append(Np5AMS)
NZ = AqueousMasterSpecies(symbol = "N2",\
                            name = "N(0)",\
                            element = "N",\
                            molarMass = MolarMass(14.0067,"g/mol"),\
                            alkalinity = 0.0)
speciesAddenda.append(NZ)
Nm3 = AqueousMasterSpecies(symbol = "NH4+",\
                             name = "N(-3)",\
                             element = "N",\
                             molarMass = MolarMass(14.067,"g/mol"),\
                             alkalinity = 0.0)
speciesAddenda.append(Nm3)
ClSSp = AqueousSecondarySpecies(symbol = "Cl-",\
                                formationReaction = [("Cl-",1)],\
                                logK25 = 0.0,\
                                name = "Cl",)
speciesAddenda.append(ClSSp)
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
NSSp = AqueousSecondarySpecies(symbol = "NO3-",\
                               formationReaction = [("NO3-",1)],\
                               logK25 = 0.0,\
                               name = "N",)
speciesAddenda.append(NSSp)
NH3SSp = AqueousSecondarySpecies(symbol = "NH3",\
                                 formationReaction = [("NH4+",1),("H+",-1)],\
                                 logK25 = -9.252,\
                                 name = "NH3",)
speciesAddenda.append(NH3SSp)
NH4pSSp = AqueousSecondarySpecies(symbol = "NH4+",\
                                  formationReaction = [("NO3-",1),("H+",10),("e-",8),("H2O",-3)],\
                                  logK25 = 119.077,\
                                  name = "NH4+",)
speciesAddenda.append(NH4pSSp)
N2SSp = AqueousSecondarySpecies(symbol = "N2",\
                                formationReaction = [("NO3-",2),("H+",12),("e-",10),("H2O",-6)],\
                                logK25 = 207.08,\
                                name = "N2",)
speciesAddenda.append(N2SSp)
KSSp = AqueousSecondarySpecies(symbol = "K+",\
                               formationReaction = [("K+",1)],\
                               logK25 = 0.0,\
                               name = "K",)
speciesAddenda.append(KSSp)
NO2mSSp = AqueousSecondarySpecies(symbol = "NO2-",\
                                  formationReaction = [("NO3-",1),("H+",2),("e-",2),("H2O",-1)],\
                                  logK25 = 28.57,\
                                  name = "NO2-",)
speciesAddenda.append(NO2mSSp)
X = SorbingSiteMasterSpecies(symbol = "X-",name   = "X")
speciesAddenda.append(X)
XESp = SorbedSecondarySpecies(symbol = "X-",\
                              formationReaction = [("X-",1)],\
                              logK25 = 0.0,\
                              name = "X",)
speciesAddenda.append(XESp)
NaXESp = SorbedSecondarySpecies(symbol = "NaX",\
                                formationReaction = [("Na+",1),("X-",1)],\
                                logK25 = 0.0,\
                                name = "NaX",)
speciesAddenda.append(NaXESp)
KXESp = SorbedSecondarySpecies(symbol = "KX",\
                               formationReaction = [("K+",1),("X-",1)],\
                               logK25 = 0.7,\
                               name = "KX",)
speciesAddenda.append(KXESp)
CaX2ESp = SorbedSecondarySpecies(symbol = "CaX2",\
                                 formationReaction = [("Ca++",1),("2X-",1)],\
                                 logK25 = 0.8,\
                                 name = "CaX2",)
speciesAddenda.append(CaX2ESp)
#~~~~~~~~~~~~~~~~~
# Chemical State ~
#~~~~~~~~~~~~~~~~~
ChemicalStateList = []
columnIonicExchangers = IonicExchangers([ExchangeBindingSpecies("X", MolesAmount(1.1e-3, "mol"))])
columnAqueousSolution = AqueousSolution (elementConcentrations = [ElementConcentration ("K",2.e-4,"mol/l"),
                                                                  ElementConcentration ("Na",1.e-3,"mol/l"),
                                                                  ElementConcentration ("N(5)",1.2e-3,"mol/l")
                                                                 ],\
                                         pH = 7.0,\
                                         pe = 12.5)
columnChemicalState = ChemicalState ("column",columnAqueousSolution ,ionicExchanger = columnIonicExchangers,charge=True)

#~~~~~~~~~
# Module ~
#~~~~~~~~~
module = Chemical()
problem  = ChemicalProblem(name               = "column",\
                           chemistryDB        = "phreeqc.dat",\
                           speciesBaseAddenda = speciesAddenda,\
                           chemicalState      = columnChemicalState)
module.setData(problem)
module.initialise()
module.setParameter("column.out")
module.run()
module.outputStateSaving()
#~~~~~~~~~~~~~~~~~~
# Post processing ~
#~~~~~~~~~~~~~~~~~~
print "ok"
a = 10
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "        End of the column case ~"
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
