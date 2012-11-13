from chemistry import *
from chemicalmodule import *
from phreeqc import *

Phreeqc_file = "toto.txt"      # bounded to Phreeqc
ProblemName  = "toto"          # Phreeqc file 
#~~~~~~~~~~~~~~~~~~~
# Chemical Addenda ~
#~~~~~~~~~~~~~~~~~~~
speciesAddenda = []
#~~~~~~~~~~~~~~~~~
# Chemical State ~
#~~~~~~~~~~~~~~~~~
ChemicalStateList = []
totoAqueousSolution = AqueousSolution (elementConcentrations = [ElementConcentration ("Si",1.31e-4,"mol/l")
                                                               ],\
                                       pH = 10.4,\
                                       pe = 4)
totoChemicalState = ChemicalState ("toto",totoAqueousSolution,phFixed = ("Cl",1.e-3))

#~~~~~~~~~
# Module ~
#~~~~~~~~~
module = Chemical()
problem  = ChemicalProblem(name               = "toto",\
                           chemistryDB        = "phreeqc.dat",\
                           speciesBaseAddenda = speciesAddenda,\
                           chemicalState      = totoChemicalState)
module.setData(problem)
module.initialise()
module.setParameter("toto.out")
module.run()
module.outputStateSaving()

print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "        End of the toto case ~"
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
