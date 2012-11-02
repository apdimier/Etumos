from chemistry import *
from chemicalmodule import *
from phreeqc import *

Phreeqc_file = "caprock.txt"      # bounded to Phreeqc
ProblemName  = "caprock"          # Phreeqc file
"""
 The present test case is based on data issued from the IFP journal Vol. 65 (2010), No. 3, pp. 485-502
 
 Integrative Modeling of Caprock Integrity in the Context of CO2 Storage
 
 
"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# molar masses issued from llnl.dat ~
# in g/mol                          ~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Na = 22.9898
Mg = 24.305
Al = 26.9815
Fe = 55.847
S  = 32.066
Si = 28.0855
O  = 15.994
H  = 1.0079
C  = 12.0110
Ca = 40.078
K  = 39.0983

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# calculation of the molar mass of each mineral  ~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

MontmNa     = 0.33*Na + 0.33*Mg + 1.67*Al + 4*Si + 12*O + 2*H
Calcite     = Ca+C+3*O
Ankerite    = Ca + 0.3*Mg + 0.7*Fe + 6*O + 2*C
Kaolinite   = 2*Al + 2*Si + 9*O + 4*H
Illite      = 0.25*Mg + 0.6*K + 2.3*Al + 3.5*Si + 12*O + 2*H
Quartz      = Si + 2*O
Anhydrite   = Ca + S + 4*O
Pyrite      = 2*S + Fe


#~~~~~~~
# Data ~	// for 1L of solution //
#~~~~~~~

#
#  mineralogy[i] = [ "Mineral",  percentage molar mass ]
#

mineralogy   =   [["Calcite",    0.5,   Calcite]]
mineralogy.append(["Ankerite",   0.05,    Ankerite])
mineralogy.append(["Montmor-Na", 0.25,   MontmNa])
mineralogy.append(["Kaolinite",  0.03,    Kaolinite])
mineralogy.append(["Illite",     0.02,    Illite])
mineralogy.append(["Quartz",     0.10,   Quartz])
mineralogy.append(["Anhydrite",  0.03,    Anhydrite])
mineralogy.append(["Pyrite",     0.02,    Pyrite])

totalMassOfMinerals = 50		# total mass of minerals, in g

#~~~~~~~~~~~~~~~~~~~
# Chemical Addenda ~
#~~~~~~~~~~~~~~~~~~~
speciesAddenda = []
Ankerite = MineralSecondarySpecies(symbol = "CaFe0.7Mg0.3(CO3)2 + 4H+",\
                                  formationReaction = [("Ca++",1),\
                                                       ("Fe++",0.7),\
                                                       ("Mg++",0.3),\
                                                       ("H2O",2),\
                                                       ("CO2",2)],\
                                  logK25 = 12.14,\
                                  name = "Ankerite",\
                                  density = Density(3000,"kg/m**3"))
speciesAddenda=[Ankerite]
mineralComposition = []
for mineral in mineralogy:
    mineralComposition.append(MineralTotalConcentration(mineral[0],mineral[1]*totalMassOfMinerals/mineral[2],  "mol/l", saturationIndex = 0.0))
    pass
#~~~~~~~~~~~~~~~~~
# Chemical State ~
#~~~~~~~~~~~~~~~~~
ChemicalStateList = []
#alkaMineralPhase = MineralPhase([MineralTotalConcentration("Calcite", a[0][1]*0.01*mt/a[0][2], "mol/l", saturationIndex = 0.0),
#                                MineralTotalConcentration("Ankerite", a[1][1]*0.01*mt/a[1][2], "mol/l", saturationIndex = 0.0),
#                                MineralTotalConcentration("Montmor-Na", a[2][1]*0.01*mt/a[2][2], "mol/l", saturationIndex = 0.0),
#                                MineralTotalConcentration("Kaolinite", a[3][1]*0.01*mt/a[3][2], "mol/l", saturationIndex = 0.0),
#                                MineralTotalConcentration("Illite", a[4][1]*0.01*mt/a[4][2], "mol/l", saturationIndex = 0.0),
#                                MineralTotalConcentration("Quartz", a[5][1]*0.01*mt/a[5][2], "mol/l", saturationIndex = 0.0),
#                                MineralTotalConcentration("Anhydrite", a[6][1]*0.01*mt/a[6][2], "mol/l", saturationIndex = 0.0),
#                                MineralTotalConcentration("Pyrite", a[7][1]*0.01*mt/a[7][2], "mol/l", saturationIndex = 0.0),
#                                MineralTotalConcentration("Goethite",0.0, "mol/l", saturationIndex = 6e-4),
#                                MineralTotalConcentration("Chalcedony",0.0, "mol/l", saturationIndex = -0.23),
#                                MineralTotalConcentration("Dolomite-dis", 0.0, "mol/l", saturationIndex = -1.24),
#                                MineralTotalConcentration("Siderite",0.0, "mol/l", saturationIndex = -0.8),
#                                ])
mineralComposition+= [MineralTotalConcentration("Goethite",0.0, "mol/l", saturationIndex = 6e-4),
                      MineralTotalConcentration("Chalcedony",0.0, "mol/l", saturationIndex = -0.23),
                      MineralTotalConcentration("Dolomite-dis", 0.0, "mol/l", saturationIndex = -1.24),
                      MineralTotalConcentration("Siderite",0.0, "mol/l", saturationIndex = -0.8),
                     ]
alkaMineralPhase = MineralPhase(mineralComposition)
alkaAqueousSolution = AqueousSolution (elementConcentrations = [ElementConcentration ("Al",1.531e-7,"mol/l"),
                                                                ElementConcentration ("C",2.180e-3,"mol/l"),
                                                                ElementConcentration ("Ca",1.528e-2,"mol/l"),
                                                                ElementConcentration ("Cl",2.601e-1,"mol/l"),
                                                                ElementConcentration ("Fe",1.534e-5,"mol/l"),
                                                                ElementConcentration ("K",1.190e-2,"mol/l"),
                                                                ElementConcentration ("Mg",8.937e-4,"mol/l"),
                                                                ElementConcentration ("Na",2.543e-1,"mol/l"),
                                                                ElementConcentration ("S",1.841e-2,"mol/l"),
                                                                ElementConcentration ("Si",5.371e-4,"mol/l")
                                                               ],\
                                       pH = 6.54,\
                                       pe = 4,\
                                       temperature = 80)
alkaChemicalState = ChemicalState ("caprock",alkaAqueousSolution,mineralPhase = alkaMineralPhase)

#~~~~~~~~~
# Module ~
#~~~~~~~~~
module = Chemical()
problem  = ChemicalProblem(name               = "homogeneousCaprock",\
                           chemistryDB        = "llnl.dat",\
                           speciesBaseAddenda = speciesAddenda,\
                           chemicalState      = alkaChemicalState)
module.setData(problem)
module.initialise()
module.setParameter("caprock.out")
module.run()
module.outputStateSaving()
#~~~~~~~~~~~~~~~~~~
# Post processing ~
#~~~~~~~~~~~~~~~~~~
print " checking results stability"
print module.getOutput()
pH = 6.536
if abs(pH-module.getOutput()[4]) < 1.e-2:
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "Results can be considered as stable"
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
else:
    raise Warning, "problem with the caprock equilibrium test case on pH"

print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "     End of the caprock case ~"
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
