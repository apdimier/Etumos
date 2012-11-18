from chemistry import *
from chemicalmodule import *
from phreeqc import *

Phreeqc_file = "azerty.txt"      # bounded to Phreeqc
ProblemName  = "azerty"          # Phreeqc file 
#~~~~~~~~~~~~~~~~~~~
# Chemical Addenda ~
#~~~~~~~~~~~~~~~~~~~
speciesAddenda = []
#~~~~~~~~~~~~~~~~~
# Chemical State ~
#~~~~~~~~~~~~~~~~~
ChemicalStateList = []
azertyMineralPhase = MineralPhase([])
azertyAqueousSolution = AqueousSolution (elementConcentrations = [ElementConcentration ("Na",2.0000000000e-02,"mol/l"),
ElementConcentration ("Si",1.0000000000e-03,"mol/l"),
ElementConcentration ("Ca",1.0000000000e-02,"mol/l"),
                                                                 ],\
                                         pH = 7.0,\
                                         pe = 4)
azertyChemicalState = ChemicalState ("azerty",azertyAqueousSolution,azertyMineralPhase)

#~~~~~~~~~
# Module ~
#~~~~~~~~~
module = Chemical()
problem  = ChemicalProblem(name               = "azerty",\
                           chemistryDB                = "phreeqc.dat",\
                           speciesBaseAddenda = speciesAddenda,\
                           chemicalState      = azertyChemicalState)
module.setData(problem)
module.initialise()
module.setParameter("azerty.out")
module.run()
module.outputStateSaving()

print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "        End of the azerty case ~"
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
