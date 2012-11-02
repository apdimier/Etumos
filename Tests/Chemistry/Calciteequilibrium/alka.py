from chemistry import *
from chemicalmodule import *
from phreeqc import *

Phreeqc_file = "alka.txt"      # bounded to Phreeqc
ProblemName  = "alka"          # Phreeqc file 
#~~~~~~~~~~~~~~~~~~~
# Chemical Addenda ~
#~~~~~~~~~~~~~~~~~~~
speciesAddenda = []
#~~~~~~~~~~~~~~~~~
# Chemical State ~
#~~~~~~~~~~~~~~~~~
ChemicalStateList = []
alkaMineralPhase = MineralPhase([MineralTotalConcentration("Calcite",10.0, "mol/l",saturationIndex = 0.0),
                                MineralTotalConcentration("CO2(g)",10.0, "mol/l",saturationIndex = 0.01)])
alkaAqueousSolution = AqueousSolution (elementConcentrations = [ElementConcentration ("Alkalinity",4.0,"mol/l"),
                                                                ElementConcentration ("S(6)",1.0,"mol/l"),
                                                                ElementConcentration ("Ca",3.0,"mol/l")
                                                               ],\
                                       pH = 7.0,\
                                       pe = 4)
alkaChemicalState = ChemicalState ("alka",alkaAqueousSolution,mineralPhase = alkaMineralPhase)

#~~~~~~~~~
# Module ~
#~~~~~~~~~
module = Chemical()
problem  = ChemicalProblem(name               = "alka",\
                           chemistryDB                = "phreeqc.dat",\
                           speciesBaseAddenda = speciesAddenda,\
                           chemicalState      = alkaChemicalState)
module.setData(problem)
module.initialise()
module.setParameter("alka.out")
module.run()
module.outputStateSaving()
#~~~~~~~~~~~~~~~~~~
# Post processing ~
#~~~~~~~~~~~~~~~~~~
print " checking results stability"
pH = 5.2440
if abs(pH-module.getOutput()[4]) < 1.e-4:
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "Results can be considered as stable"
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
else:
    raise Warning, "problem with the Calcite equilibrium test case n. on pH"

print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "        End of the alka case ~"
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
