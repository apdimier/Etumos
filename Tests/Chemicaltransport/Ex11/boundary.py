from chemistry import *
from chemicalmodule import *
from phreeqc import *

Phreeqc_file = "boundary.txt"      # bounded to Phreeqc
ProblemName  = "boundary"          # Phreeqc file 
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
Ca = AqueousMasterSpecies(symbol = "Ca++",\
                          name = "Ca",\
                          element = "Ca",\
                          molarMass = MolarMass(40.08,"g/mol"),\
                          alkalinity = 0.0)
speciesAddenda.append(Ca)
K = AqueousMasterSpecies(symbol = "K+",\
                         name = "K",\
                         element = "K",\
                         molarMass = MolarMass(39.102,"g/mol"),\
                         alkalinity = 0.0)
speciesAddenda.append(K)
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
KSSp = AqueousSecondarySpecies(symbol = "K+",\
                               formationReaction = [("K+",1)],\
                               logK25 = 0.0,\
                               name = "K",)
speciesAddenda.append(KSSp)
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
boundaryAqueousSolution = AqueousSolution (elementConcentrations = [ElementConcentration ("Ca",6.e-4,"mol/l"),
                                                                    ElementConcentration ("Cl",1.2e-3,"mol/l")
                                                                   ],\
                                           pH = 7,\
                                           temperature =25.0,\
                                           pe = 4)
boundaryChemicalState = ChemicalState ("boundary",boundaryAqueousSolution,charge=True)

#~~~~~~~~~
# Module ~
#~~~~~~~~~
module = Chemical()
problem  = ChemicalProblem(name               = "boundary",\
                           chemistryDB        = "phreeqc.dat",\
                           speciesBaseAddenda = speciesAddenda,\
                           chemicalState      = boundaryChemicalState)
module.setData(problem)
module.initialise()
module.setParameter("boundary.out")
module.run()
module.outputStateSaving()

print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "        End of the boundary case ~"
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
