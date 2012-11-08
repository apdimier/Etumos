from chemistry import *
from chemicalmodule import *
from phreeqc import *

Phreeqc_file = "gasphase.txt"   # bounded to Phreeqc
ProblemName  = "gasephase"      # Phreeqc file 
#~~~~~~~~~~~~~~~~~~~
# Chemical Addenda ~
#~~~~~~~~~~~~~~~~~~~
speciesAddenda = []
#~~~~~~~~~~~~~~~~~
# Chemical State ~
#~~~~~~~~~~~~~~~~~
ChemicalStateList = []
stateMineralPhase = MineralPhase([MineralTotalConcentration("Calcite", 10.0, "mol/l", saturationIndex = 0.0)])
#
stateAqueousPhase = AqueousSolution (elementConcentrations = [ElementConcentration ("C(4)",2.0,"mol/l"),
                                                                 ElementConcentration ("S(6)",1.0,"mol/l"),
                                                                 ElementConcentration ("N(0)",2.0,"mol/l")
                                                                ],\
                                                                pH = 7.0,\
                                                                pe = 4)
#
print " fugacity definition "
stateGasPhase = []
stateGasPhase.append(Fugacity ("CH4(g)", 0.0))
stateGasPhase.append(Fugacity ("H2S(g)", 0.0))
stateGasPhase.append(Fugacity ("CO2(g)", 0.005))
stateGasPhase.append(Fugacity ("N2(g)", 0.995))
stateGasPhase = GasPhase(stateGasPhase)
#print " fugacity definition over "
#print stateGasPhase
#raw_input("stateGasPhase")
#                                                                
gasChemicalState = ChemicalState ("gasphase",   stateAqueousPhase,\
                                                mineralPhase = stateMineralPhase,\
                                                gasPhase = stateGasPhase,\
                                                charge = "ok",
                                                gasMassBalance = "ok")

#~~~~~~~~~
# Module ~
#~~~~~~~~~
module = Chemical()
problem  = ChemicalProblem(name               = "gasphase",\
                           chemistryDB        = "phreeqc.dat",\
                           speciesBaseAddenda = speciesAddenda,\
                           chemicalState      = gasChemicalState)
module.setData(problem)
module.initialise()
module.setParameter("gas.out")
module.run()
module.outputStateSaving()
#~~~~~~~~~~~~~~~~~~
# Post processing ~
#~~~~~~~~~~~~~~~~~~
print " checking results stability"
pH = 5.36290438242
if abs(pH-module.getOutput()[4]) < 1.e-4:
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "Results can be considered as stable"
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
else:
    raise Warning, "problem with the CO2 gas phase test case n. on pH"

print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "        End of the gas case ~"
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
