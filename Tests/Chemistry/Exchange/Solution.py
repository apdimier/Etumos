from chemistry import *
from chemicalmodule import *
from phreeqc import *

Phreeqc_file = "Solution.txt"      # bounded to Phreeqc
ProblemName  = "Solution"          # Phreeqc file 
#~~~~~~~~~~~~~~~~~~~
# Chemical Addenda ~
#~~~~~~~~~~~~~~~~~~~
speciesAddenda = []
#~~~~~~~~~~~~~~~~~
# Chemical State ~
#~~~~~~~~~~~~~~~~~
ChemicalStateList = []
SolutionIonicExchangers = IonicExchangers([ExchangeBindingSpecies("X-", MolesAmount(3.e-2, "mol"))])
SolutionAqueousSolution = AqueousSolution (elementConcentrations = [ElementConcentration ("Na",1,"mol/l"),
                                                                    ElementConcentration ("K",0.2,"mol/l"),
                                                                    ElementConcentration ("Cl",1.2,"mol/l")
                                                                   ],\
                                           pH = 7.0,\
                                           pe = 4)
SolutionChemicalState = ChemicalState ("Solution",SolutionAqueousSolution ,ionicExchanger = SolutionIonicExchangers)

#~~~~~~~~~
# Module ~
#~~~~~~~~~
module = Chemical()
problem  = ChemicalProblem(name               = "Solution",\
                           chemistryDB                = "phreeqc.dat",\
                           speciesBaseAddenda = speciesAddenda,\
                           chemicalState      = SolutionChemicalState)
module.setData(problem)
module.initialise()
module.setParameter("Solution.out")
module.run()
module.outputStateSaving()
#~~~~~~~~~~~~~~~~~~
# Post processing ~
#~~~~~~~~~~~~~~~~~~
KX = 0.01501
NaX = 0.01498
if abs(KX-module.getOutput()[22][1]) < 1.e-4 and abs(NaX-module.getOutput()[22][1]) < 1.e-4:
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "Results can be considered as stable"
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
else:
    raise Warning, "problem with the exchange test case n. on exchange site distribution"

print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "        End of the Solution case ~"
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
