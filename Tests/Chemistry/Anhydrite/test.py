comment = "#     Na+    : 2. E-2\
#     OH-    : 2. E-2\
#  pour la zone quartz: \
#     quartz mineral : 10. molal"

from chemistry import *

from chemicalmodule import *

from phreeqc import *              # phreeqc importation methods
Phreeqc_file = "cas2_NaOH_runfile.txt"      # necessary for Phreeqc
ProblemName  = "cas2_NaOH_runfile"          # necessary for Phreeqc

Na = AqueousMasterSpecies(symbol='Na+',\
                             name='Na',\
                             element = 'Na',\
                             molarMass=MolarMass(22.9898E-3,'kg/mol'),\
                             alkalinity = 0.0)
S = AqueousMasterSpecies(symbol='SO4-2',\
                             name='S',\
                             element = 'SO4',\
                             molarMass=MolarMass(32.064E-3,'kg/mol'),\
                             alkalinity = 0.0)
Nabis = AqueousSecondarySpecies (symbol="Na+",
                               formationReaction = [("Na+", 1)],
                               logK25 =0.0,
                               name ="Na")
Sbis = AqueousSecondarySpecies (symbol="SO4-2",
                               formationReaction = [("SO4-2", 1)],
                               logK25 =0.0,
                               name ="SO4-2")

Ca = AqueousMasterSpecies(symbol='Ca+2',\
                             name='Ca',\
                             element = 'Ca',\
                             molarMass=MolarMass(40.08E-3,'kg/mol'),\
                             alkalinity = 0.0)
Cabis = AqueousSecondarySpecies (symbol="Ca+2",
                               formationReaction = [("Ca+2", 1)],
                               logK25 =0.0,
                               name ="Ca")

Cl = AqueousMasterSpecies(symbol='Cl-',\
                             name='Cl',\
                             element = 'Cl',\
                             molarMass=MolarMass(35.453E-3,'kg/mol'),\
                             alkalinity = 0.0)
Clbis = AqueousSecondarySpecies (symbol="Cl-",
                               formationReaction = [("Cl-", 1)],
                               logK25 =0.0,
                               name ="Cl")
H4SiO4  = AqueousMasterSpecies(symbol='H4SiO4',
                                  name = 'Si',
                                  element = 'SiO2',
                                  molarMass=MolarMass(96.1163E-3,'kg/mol'),
                                  alkalinity = 0.0)
H4SiO4bis = AqueousSecondarySpecies (symbol="H4SiO4",
                                     formationReaction = [("H4SiO4", 1)],
                                     logK25 =0.0,
                                     name ="Si")
H3SiO4 = AqueousSecondarySpecies (symbol='H3SiO4-',
                                  formationReaction = [('H4SiO4', 1),('H+', -1)],
                                  logK25 =-9.8,
                                  name ='H3SiO4')
Quartz = MineralSecondarySpecies(symbol='SiO2',
                                 formationReaction = [('H4SiO4', 1),('H2O', -2)],
                                 logK25 = -3.6,
                                 name ='Quartz',
                                 density  = Density(2648.29,'kg/m**3'))
Anhydrite = MineralSecondarySpecies(symbol='CaSO4',
                                 formationReaction = [('Ca+2', 1),('SO4-2', 1)],
                                 logK25 = -4.360,
                                 name ='Anhydrite',
                                 density  = Density(2648.29,'kg/m**3'))

Tr = AqueousMasterSpecies(symbol="Tr",  name="Tr", element = "Tr", molarMass=MolarMass(1.0,'kg/mol'), alkalinity = .0)
Tracer = AqueousSecondarySpecies (symbol="Tr", formationReaction = [("Tr", 1)], logK25 = 0.0, name = "Tr")

speciesAddenda = [S, Sbis, Tr, Tracer, Na, H4SiO4, Nabis, Ca, Cabis, Cl, Clbis, H4SiO4bis, H3SiO4, Quartz,Anhydrite]

############################################################
#  Definition of all non attached variables : Velocity, ChemicalState ...
############################################################

AqueousSolution_soda  = AqueousSolution (elementConcentrations=[ElementConcentration ('Na', 2.0e-02, "mol/l")],
                                          pH= 12.2545 ,
                                          pe =  4.0)
chemical_sodaState   = ChemicalState ("soda", AqueousSolution_soda)

AqueousSolution_column = AqueousSolution (elementConcentrations=[ElementConcentration ('Na', 1, "mol/l"),ElementConcentration ('Cl', 1, "mol/l")],
                                          pH= 7.0 , pe =  4.0)
MineralPhaseSolution_column = MineralPhase([TotalConcentration("Quartz", 1.E1, "mol/l"),TotalConcentration("Anhydrite", 0.15, "mol/l")])
chemical_quartzState = ChemicalState ("quartz", AqueousSolution_column, MineralPhaseSolution_column)

############################################################
#  Definition of Problem: Insert all previous variables in the problem
############################################################

#problem_soda  = ChemicalProblem(name = 'Anhydrite_test_without_quartz',
#                                 chemistryDB = 'water',
#                                 speciesBaseAddenda = speciesAddenda,
#                                 chemicalState = chemical_sodaState)
problem_quartz = ChemicalProblem(name='Anhydrite_test_with_quartz',
                                 chemistryDB = 'water',
                                 speciesBaseAddenda = speciesAddenda,
                                 chemicalState = chemical_quartzState)
############################################################
#  Define the calculation module and set problem data
############################################################

#chem_soda  = Chemical()
#chem_soda.setData(problem_soda)
#chem_soda.initialise()
#chem_soda.setParameter("chemicalmodule_phreeqc_cas2_soda")

chem_quartz  = Chemical()
chem_quartz.setData(problem_quartz)
chem_quartz.initialise()
chem_quartz.setParameter("chemicalmodule_phreeqc_cas2_quartz")

############################################################
#  Run computations 
############################################################

#chem_soda.run()
#chem_soda.outputStateSaving()
chem_quartz.run()
chem_quartz.outputStateSaving()

############################################################
#  End
############################################################

#chem_soda.end()
chem_quartz.end()

print " end of the test case"
