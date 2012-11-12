from chemistry import *
from chemicalmodule import *
from phreeqc import *

Phreeqc_file = "boundary.txt"      # bounded to Phreeqc
ProblemName  = "boundary"          # Phreeqc file 
#~~~~~~~~~~~~~~~~~~~
# Chemical Addenda ~
#~~~~~~~~~~~~~~~~~~~
speciesAddenda = []
T = AqueousMasterSpecies(symbol = "T+",\
                         name = "T",\
                         element = "T",\
                         molarMass = MolarMass(35,"kg/mol"),\
                         alkalinity = 0)
speciesAddenda.append(T)
TESp = SorbedSecondarySpecies(symbol = "T+",\
                              formationReaction = [("T+",1)],\
                              logK25 = 0.0,\
                              name = "T",)
speciesAddenda.append(TESp)
#~~~~~~~~~~~~~~~~~
# Chemical State ~
#~~~~~~~~~~~~~~~~~
ChemicalStateList = []
boundaryIonicExchangers = IonicExchangers([ExchangeBindingSpecies("NaX", MolesAmount(2.e-6, "mol"))])
boundaryAqueousSolution = AqueousSolution (elementConcentrations = [ElementConcentration ("Na",1.e-2,"mol/l"),
                                                                    ElementConcentration ("Cl",1.e-2,"mol/l")
                                                                   ],\
                                           pH = 7.0,\
                                           pe = 4)
boundaryChemicalState = ChemicalState ("boundary",boundaryAqueousSolution ,ionicExchanger = boundaryIonicExchangers)

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
