comment = "^\n#\n\
# Test case for the introduction of  PITZER phreeqC keyword in order to treat Brines\n\
# a modified PITZER phreeqc database is used to treat an evaporation problem\n\
# via the introduction of the species addenda, see the gebo module."
from chemistry import *

from chemicalmodule import *

from phreeqc import *              # phreeqc importation methods

from gebo import speciesAddenda  
Phreeqc_file = "pitzer_b.txt"      
ProblemName  = "Pitzer_b"          
#SOLUTION 1
# pH 8.22
# Na 485; K 10.6;    Mn 1.;     Mg 55.1;  Ca 10.7
# Cl 566; Alkalinity 2.4; S(6) 29.3
CalciteMS = MineralSecondarySpecies(symbol            = "CaCO3",\
                                    formationReaction = [('CO3-2', 1), ('Ca+2', 1)],\
                                    logK25            = -8.480000e+00,\
                                    logK              = [-2.3704000000e+02, -1.0770000000e-01, 0.0000000000e+03, 1.0225000000e+02, 6.7900000000e+05, ],\
                                    name              = "Calcite")
speciesAddenda.append(CalciteMS)
SiO2aqueousMS = MineralSecondarySpecies(symbol            = "SiO2",\
                                    formationReaction = [('SiO2', 1)],\
                                    logK25            = -2.71,\
                                    logK              = [-2.3704000000e+02, -1.0770000000e-01, 0.0000000000e+03, 1.0225000000e+02, 6.7900000000e+05, ],\
                                    name              = "SiO2(a)")
speciesAddenda.append(SiO2aqueousMS)
speciesAddenda.append(Salt(("Pb+2",  "Cl-" ),     b0 = 0.26,  b1 = 1.64,  c0 = 0.088, description = "Millero and Byrne"))
speciesAddenda.append(Salt(("PbCl+", "Cl-" ),     b0 = 0.15,                          description = "Millero and Byrne"))
speciesAddenda.append(Salt(("H+",    "PbCl3-" ),  b0 = 0.27,  b1 = 0.63,              description = "Felmy"))
speciesAddenda.append(Salt(("H+",    "PbCl4-2" ), b0 = 0.7 ,                          description = "Felmy"))
speciesAddenda.append(Salt(("Na+",   "PbCl3-" ),  b0 = 0.092, b1 = 0.65,              description = "Felmy"))
speciesAddenda.append(Salt(("Na+",   "PbCl4-2" ), c0 = 0.424,                         description = "Felmy 00"))

elementList =  [ElementConcentration ('Ba',   0.00063, "mol/l"),\
                ElementConcentration ('Ca',   1.403,   "mol/l"),\
                ElementConcentration ('Cl',   4.707,   "mol/l"),\
                ElementConcentration ('K',    0.074,   "mol/l"),\
                ElementConcentration ('Mg',   0.02,    "mol/l"),\
                ElementConcentration ('Na',   1.737,   "mol/l"),\
                ElementConcentration ('Pb',   0.0006,  "mol/l"),\
                ElementConcentration ('S(6)', 0.0009,  "mol/l"),\
                ElementConcentration ('Si',   0.0006,  "mol/l"),\
               ]

aqueousSolution_brine  = AqueousSolution (elementConcentrations=elementList,
                                          temperature = 150,
                                          pH= 7.0,
                                          units = "mol/kgw")

mineralPhaseSolution_brine = MineralPhase([MineralConcentration("Halite", 0., "mol/l")])
                        
pitzerChemicalState = ChemicalState ("brine",\
                     aqueousSolution_brine,\
                     mineralPhaseSolution_brine)

problem  = ChemicalProblem(name='soultz 2 test case',\
                           chemistryDB='pitzer.dat',\
                           speciesBaseAddenda = speciesAddenda,\
                           chemicalState=pitzerChemicalState)

module  = Chemical()
module.setData(problem)
module.initialise()
module.setParameter('soultz2.out')
module.setComment(comment)
module.run()
module.outputStateSaving()

module.end()

print " checking results stability"
pH = 7.0
ionicStrength = 4.2196715096e+00
state = module.getOutput()
comment = "Results for the soultz2 test case can be considered as stable"
if abs(pH-state[4]) < 1.e-4:
    if abs(ionicStrength-state[7]) < 1.e-4:
        print "~"*len(comment)
        print comment
        print "~"*len(comment)
    else:
        raise Warning, "problem with the Soultz2 Pitzer test case on ionic strength"
else:
    raise Warning, "problem with the Soultz2 Pitzer test case on pH"
