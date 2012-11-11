comment = "^\n#\n\
# Test case of the introduction of  PITZER phreeqC keyword : to treat Brines\n\
# a modified PITZER phreeqc database is used to treat an evaporation problem"
from chemistry import *

from chemicalmodule import *

from phreeqc import *              # phreeqc importation methods
Phreeqc_file = "pitzer_b.txt"      
ProblemName  = "Pitzer_b"          
#SOLUTION 1
# pH 8.22
# Na 485; K 10.6;    Mn 1.;     Mg 55.1;  Ca 10.7
# Cl 566; Alkalinity 2.4; S(6) 29.3

elementList =  [ElementConcentration ('Alkalinity', 2.400e-03, "mol/l"),\
		ElementConcentration ('Ca', 1.070e-02, "mol/l"),\
		ElementConcentration ('Cl', 5.660e-01, "mol/l"),\
		ElementConcentration ('K',  1.060e-02, "mol/l"),\
		ElementConcentration ('Mg', 5.510e-02, "mol/l"),\
		ElementConcentration ('Mn', 1.000e-03, "mol/l"),\
		ElementConcentration ('Na', 4.850e-01, "mol/l"),\
		ElementConcentration ('S(6)', 2.930e-02, "mol/l")]

clManga = Salt(("Mn+2","Cl-"),b0 = 0.327225,b1 = 1.55025,b2 = 0.0,c0 = 0.0204972)
sulManga = Salt(("Mn+2","SO4-2"),b0 = 0.2065,b1 = 2.9511,b2 = -40.0,c0 = 0.01636)

aqueousSolution_brine  = AqueousSolution (elementConcentrations=elementList,
                                          pH= 8.22)
##	 CO2(g) -3.5 10
##	 Calcite 0 0
##	 Gypsum 0 0
##	     Anhydrite 0 0
##	  Glauberite 0 0
##	  Polyhalite 0 0
##	 Epsomite 0 0
#	   Kieserite 0 0
#	  Hexahydrite 0 0
##	 Halite 0 0
##	     Bischofite 0 0
##	 Carnallite 0 0

mineralPhaseSolution_brine = MineralPhase([MineralConcentration("CO2(g)", 1.E1, "mol/l",saturationIndex = -3.5),\
					   MineralConcentration("Anhydrite", 0., "mol/l"),\
					   MineralConcentration("Bischofite", 0., "mol/l"),\
					   MineralConcentration("Calcite", 0., "mol/l"),\
					   MineralConcentration("Carnallite", 0., "mol/l"),\
					   MineralConcentration("Epsomite", 0., "mol/l"),\
					   MineralConcentration("Glauberite", 0., "mol/l"),\
					   MineralConcentration("Gypsum", 0., "mol/l"),\
					   MineralConcentration("Halite", 0., "mol/l"),\
					   MineralConcentration("Hexahydrite", 0., "mol/l"),\
					   MineralConcentration("Kieserite", 0., "mol/l"),\
					   MineralConcentration("Polyhalite", 0., "mol/l")])
					    
pitzerChemicalState = ChemicalState ("brine",\
				     aqueousSolution_brine,\
				     mineralPhaseSolution_brine)

problem  = ChemicalProblem(name='brine test case',\
                           chemistryDB='pitzer_test',\
                           speciesBaseAddenda=[clManga,sulManga],\
                           chemicalState=pitzerChemicalState)

module  = Chemical()
module.setData(problem)
module.initialise()
module.setParameter('pitzer')
module.setComment(comment)
module.run()
module.outputStateSaving()

module.end()

print " checking results stability"
pH = 7.9373525676e+00
IonicStrength = 7.4905558167e-01
state = module.getOutput()
if abs(pH-state[4]) < 1.e-4:
    if abs(IonicStrength-state[7]) < 1.e-4:
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        print "Results can be considered as stable"
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    else:
        raise Warning, "problem with the Pitzer test case n. on ionic strength"else:
    raise Warning, "problem with the pitzer test case n. on pH"
