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
Nabis = AqueousSecondarySpecies (symbol="Na+",
                               formationReaction = [("Na+", 1)],
			       coefA = 4.0,\
			       coefB = 0.1,\
                               logK25 =0.0,
                               name ="Na")
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
speciesAddenda = [Na,H4SiO4,Nabis,H4SiO4bis,H3SiO4,Quartz]

############################################################
#  Definition of all non attached variables : Velocity, ChemicalState ...
############################################################

AqueousSolution_soude  = AqueousSolution (elementConcentrations=[ElementConcentration ('Na', 2.0e-02, "mol/l")],
                                          pH= 12.2545 ,
                                          pe =  4.0)
chemical_state_soude   = ChemicalState ("soude", AqueousSolution_soude)

AqueousSolution_column = AqueousSolution (elementConcentrations=[ElementConcentration ('Na', 0.0e-02, "mol/l")],
                                          pH= 7.0 , pe =  4.0)
MineralPhaseSolution_column = MineralPhase([TotalConcentration("Quartz", 1.E1, "mol/l")])
chemical_state_quartz = ChemicalState ("quartz", AqueousSolution_column, MineralPhaseSolution_column)

############################################################
#  Definition of Problem: Insert all previous variables in the problem
############################################################

problem_soude  = ChemicalProblem(name = 'Test physico-numerique chimie 2 soude',
                                 chemistryDB = 'phreeqc',
                                 speciesBaseAddenda = speciesAddenda,
                                 chemicalState = chemical_state_soude)
problem_quartz = ChemicalProblem(name='Test physico-numerique chimie 2 quartz',
                                 chemistryDB = 'phreeqc',
                                 speciesBaseAddenda = speciesAddenda,
                                 chemicalState = chemical_state_quartz)
############################################################
#  Define the calculation module and set problem data
############################################################
#
# ok init
#
ok = 0
#
chem_soude  = Chemical()
chem_soude.setData(problem_soude)
chem_soude.initialise()
chem_soude.setParameter("chemicalmodule_phreeqc_cas2_soude")
############################################################
#  Run computations 
############################################################

chem_soude.run()
chem_soude.outputStateSaving()
result0 = chem_soude.getOutput()
pH = 12.2545
if abs(pH-result0[4]) < 1.e-4:
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "Results can be considered as stable"
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    ok = 1
else:
    raise Warning, "problem with the soude test case n. on pH"

chem_quartz  = Chemical()
chem_quartz.setData(problem_quartz)
chem_quartz.initialise()
chem_quartz.setParameter("chemicalmodule_phreeqc_cas2_quartz")

chem_quartz.run()
chem_quartz.outputStateSaving()
pH = 6.65139813427
result1 = chem_quartz.getOutput()
if abs(pH-result1[4]) < 1.e-4:
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "Results can be considered as stable"
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    ok = 1
else:
    raise Warning, "problem with the soude test case n. on pH"

############################################################
#  End
############################################################

chem_soude.end()
chem_quartz.end()

print " end of the test case"
