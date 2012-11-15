from chemistry import *
from chemicalmodule import *
from phreeqc import *

Phreeqc_file = "boundary.txt"      # bounded to Phreeqc
ProblemName  = "boundary"          # Phreeqc file 
#~~~~~~~~~~~~~~~~~~~
# Chemical Addenda ~
#~~~~~~~~~~~~~~~~~~~
speciesAddenda = []
Cs = AqueousMasterSpecies(symbol = "Cs+",\
                          name = "Cs",\
                          element = "Cs+ = Cs+",\
                          molarMass = MolarMass(135,"kg/mol"),\
                          alkalinity = 0.0)
speciesAddenda.append(Cs)
T = AqueousMasterSpecies(symbol = "T+",\
                         name = "T",\
                         element = "T+ = T+",\
                         molarMass = MolarMass(1.008,"kg/mol"),\
                         alkalinity = -1.0)
speciesAddenda.append(T)
CsSSp = AqueousSecondarySpecies(symbol = "Cs+",\
                                formationReaction = [("Cs+",1)],\
                                logK25 = 0.0,\
                                name = "Cs",)
speciesAddenda.append(CsSSp)
TSSp = AqueousSecondarySpecies(symbol = "T+",\
                               formationReaction = [("T+",1)],\
                               logK25 = 0.0,\
                               name = "T",)
speciesAddenda.append(TSSp)
Z = SorbingSiteMasterSpecies(symbol = "Z-",name   = "Z")
speciesAddenda.append(Z)
HZESp = SorbedSecondarySpecies(symbol = "HZ",\
                               formationReaction = [("H+",1),("Z-",1)],\
                               logK25 = -99.0,\
                               name = "HZ",)
speciesAddenda.append(HZESp)
NaZESp = SorbedSecondarySpecies(symbol = "NaZ",\
                                formationReaction = [("Na+",1),("Z-",1)],\
                                logK25 = 0.0,\
                                name = "NaZ",)
speciesAddenda.append(NaZESp)
ZESp = SorbedSecondarySpecies(symbol = "Z-",\
                              formationReaction = [("Z-",1)],\
                              logK25 = 0.0,\
                              name = "Z",)
speciesAddenda.append(ZESp)
CsZESp = SorbedSecondarySpecies(symbol = "CsZ",\
                                formationReaction = [("Cs+",1),("Z-",1)],\
                                logK25 = 0.5,\
                                name = "CsZ",)
speciesAddenda.append(CsZESp)
#~~~~~~~~~~~~~~~~~
# Chemical State ~
#~~~~~~~~~~~~~~~~~
ChemicalStateList = []
boundaryAqueousSolution = AqueousSolution (elementConcentrations = [ElementConcentration ("Cs",1.e-6,"mol/l"),
                                                                    ElementConcentration ("Na",1.e-2,"mol/l"),
                                                                    ElementConcentration ("T",1.e-6,"mol/l")
                                                                   ],\
                                           pH = 7.0,\
                                           pe = 4)
boundaryChemicalState = ChemicalState ("boundary",boundaryAqueousSolution)

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
