comment = "^\n#\n\
# Test case for the SOLIDSOLUTION phreeqC keyword : see page 236 of the phreeqC manual\n\
# See the SOLID_SOLUTION  keyword definition p. 144 and 192 of the phreeqC manual\n\
#"
# Import common Necessary modules(python)
#
from chemistry import *

#
#   Import Module depending on Problem Type:
#        Chemical              : from chemicalmodule import *
#        Chemical Transport    : from chemicaltransportmodule import *
#

from chemicalmodule import *

from phreeqc import *              # phreeqc importation methods
Phreeqc_file = "solidsolution.txt"      
ProblemName  = "solidsolution"          

elementList =  [ElementConcentration ('Ca', 3.932e-3, "mol/l"),\
		ElementConcentration ('C', 7.864e-3, "mol/l")]

AqueousSolution_solidsolution  = AqueousSolution (elementConcentrations=elementList,
                                          pH= 5.93 ,
                                          pe =  4.0)
MineralPhaseSolution_solidsolution = MineralPhase([MineralTotalConcentration("CO2(g)", 1.E1, "mol/l"),\
					           MineralTotalConcentration("Aragonite", 0., "mol/l")])
					    
SolidSolutionList = SolidSolution (name = "Ca(x)Sr(1-x)CO3",\
			minerals=[MineralTotalConcentration("Aragonite",	0.0, "mol/l"),
				  MineralTotalConcentration("Strontianite",	0.0, "mol/l")],\
				  temperature= 25.,\
				  gugg =  [0.,0.])					    
chemical_state_solidsolution = ChemicalState ("Solid Solution of Strontianite and Aragonite",\
						   AqueousSolution_solidsolution,\
						   MineralPhaseSolution_solidsolution,\
						   solidSolution = SolidSolutionList,\
						   charge="ok")

problem_solidsolution  = ChemicalProblem(name='solid solution test case',
                                         chemistryDB='phreeqc',
                                         speciesBaseAddenda=[],
                                         chemicalState=chemical_state_solidsolution)

module  = Chemical()
module.setData(problem_solidsolution)
module.initialise()
module.setParameter('chemicalmodule_phreeqc_solidsolution')
module.setComment(comment)
module.run()
module.outputStateSaving()

module.end()

print " checking results stability"
pH = 5.6572
IonicStrength = 1.13318e-02
state = module.getOutput()
if abs(pH-state[4]) < 1.e-4:
    if abs(IonicStrength-state[7]) < 1.e-4:
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        print "Results can be considered as stable"
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    else:
        raise Warning, "problem with the solid solution test case"else:
    raise Warning, "problem with the solid solution test case"
