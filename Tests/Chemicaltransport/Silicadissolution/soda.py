#!/usr/bin/python
from chemistry import *
from chemicalmodule import *
from phreeqc import *

Phreeqc_file = "soda.txt"      # bounded to Phreeqc
ProblemName  = "soda"          # Phreeqc file 
#~~~~~~~~~~~~~~~~~~~
# Chemical Addenda ~
#~~~~~~~~~~~~~~~~~~~
speciesAddenda = []
Na = AqueousMasterSpecies(symbol = "Na+",\
                          name = "Na",\
                          element = "Na",\
                          molarMass = MolarMass(0.02299,"kg/mol"),\
                          alkalinity = 0)
speciesAddenda.append(Na)
Si = AqueousMasterSpecies(symbol = "H4SiO4",\
                          name = "Si",\
                          element = "SiO2",\
                          molarMass = MolarMass(0.0280843,"kg/mol"),\
                          alkalinity = 0.0)
speciesAddenda.append(Si)
NaSSp = AqueousSecondarySpecies(symbol = "Na+",\
                                formationReaction = [("Na+",1)],\
                                logK25 = 0.0,\
                                name = "Na",)
speciesAddenda.append(NaSSp)
SiSSp = AqueousSecondarySpecies(symbol = "H4SiO4",\
                                formationReaction = [("H4SiO4",1)],\
                                logK25 = 0.0,\
                                name = "Si",)
speciesAddenda.append(SiSSp)
H3SiO4SSp = AqueousSecondarySpecies(symbol = "H3SiO4-",\
                                    formationReaction = [("H4SiO4",1),("H+",-1)],\
                                    logK25 = -9.83,\
                                    name = "H3SiO4",)
speciesAddenda.append(H3SiO4SSp)
QuartzAd = MineralSecondarySpecies(symbol = "SiO2",\
                                   formationReaction = [("H2O",-2),("H4SiO4",1)],\
                                   logK25 = -3.6,\
                                   name = "Quartz",\
                                   density = Density(2648.29,"kg/m**3"))
speciesAddenda.append(QuartzAd)
#~~~~~~~~~~~~~~~~~
# Chemical State ~
#~~~~~~~~~~~~~~~~~
ChemicalStateList = []
sodaAqueousSolution = AqueousSolution (elementConcentrations = [ElementConcentration ("Na",2.e-02,"mol/l")
                                                               ],\
                                       pH = 12.2545,\
                                       pe = 4)
sodaChemicalState = ChemicalState ("soda",sodaAqueousSolution)

#~~~~~~~~~
# Module ~
#~~~~~~~~~
module = Chemical()
problem  = ChemicalProblem(name               = "soda",\
                           chemistryDB        = "phreeqc.dat",\
                           speciesBaseAddenda = speciesAddenda,\
                           chemicalState      = sodaChemicalState)
module.setData(problem)
module.initialise()
module.setParameter("soda.out")
module.run()
module.outputStateSaving()

print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "        End of the soda case ~"
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
