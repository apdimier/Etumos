from chemistry import *
from chemicalmodule import *
from phreeqc import *

Phreeqc_file = "column.txt"      # bounded to Phreeqc
ProblemName  = "column"          # Phreeqc file 
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
K = AqueousMasterSpecies(symbol = "K+",\
                         name = "K",\
                         element = "K",\
                         molarMass = MolarMass(39.102,"g/mol"),\
                         alkalinity = 0.0)
speciesAddenda.append(K)
T = AqueousMasterSpecies(symbol = "T+",\
                         name = "T",\
                         element = "T",\
                         molarMass = MolarMass(35,"g/mol"),\
                         alkalinity = 0)
speciesAddenda.append(T)
Cl = AqueousMasterSpecies(symbol = "Cl-",\
                          name = "Cl",\
                          element = "Cl",\
                          molarMass = MolarMass(35.453,"g/mol"),\
                          alkalinity = 0.0)
speciesAddenda.append(Cl)
NaSSp = AqueousSecondarySpecies(symbol = "Na+",\
                                formationReaction = [("Na+",1)],\
                                logK25 = 0.0,\
                                name = "Na",)
speciesAddenda.append(NaSSp)
KSSp = AqueousSecondarySpecies(symbol = "K+",\
                               formationReaction = [("K+",1)],\
                               logK25 = 0.0,\
                               name = "K",)
speciesAddenda.append(KSSp)
TSSp = AqueousSecondarySpecies(symbol = "T+",\
                               formationReaction = [("T+",1)],\
                               logK25 = 0.0,\
                               name = "T",)
speciesAddenda.append(TSSp)
ClSSp = AqueousSecondarySpecies(symbol = "Cl-",\
                                formationReaction = [("Cl-",1)],\
                                logK25 = 0.0,\
                                name = "Cl",)
speciesAddenda.append(ClSSp)
NaXESp = SorbedSecondarySpecies(symbol = "NaX",\
                                formationReaction = [("Na+",1),("X-",1)],\
                                logK25 = 0.0,\
                                name = "NaX",)
speciesAddenda.append(NaXESp)
KXESp = SorbedSecondarySpecies(symbol = "KX",\
                               formationReaction = [("K+",1),("X-",1)],\
                               logK25 = 0.301,\
                               name = "KX",)
speciesAddenda.append(KXESp)
#~~~~~~~~~~~~~~~~~
# Chemical State ~
#~~~~~~~~~~~~~~~~~
ChemicalStateList = []
columnIonicExchangers = IonicExchangers([ExchangeBindingSpecies("X-", MolesAmount(0.01, "mol"))])
columnAqueousSolution = AqueousSolution (elementConcentrations = [ElementConcentration ("Na",1.e-2,"mol/l"),
                                                                  ElementConcentration ("Cl",1.e-2,"mol/l"),
                                                                  ElementConcentration ("K",1.e-10,"mol/l")
                                                                 ],\
                                         pH = 7.0,\
                                         pe = 4)
columnChemicalState = ChemicalState ("column",columnAqueousSolution ,ionicExchanger = columnIonicExchangers)

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

print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "        End of the column case ~"
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
