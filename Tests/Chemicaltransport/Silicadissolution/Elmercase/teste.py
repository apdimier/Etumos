from constant import epspH
import os                  # for file path
from mesh import *         # for Meshes treatment 
from datamodel import *
import sys
from chemicaltransportmodule import *
from listtools import normMaxListComparison, subtractLists
############################################################
#   Import Module depending on the Problem Type:
#        Saturated Hydraulic   : from saturatedhydraulicmodule import *
#        Unsaturated Hydraulic : from unsaturatedhydraulicmodule import *
#        Transient Hydraulic   : from transienthydraulicmodule import *
#        Extended Transport    : from extendedtransportmodule import *
#        Simple Transport      : from simpletransportmodule import *
#        Chemical              : from chemicalmodule import *
#        Chemical Transport    : from chemicaltransportmodule import *
############################################################
#
#                Parser Implementation
#
from analyticalSolution_Sildissolution import *
dico = { 'MethodChoice' : 'FE'}

Phreeqc_file = "cas2_NaOH_runfile.txt"      # necessary for Phreeqc
ProblemName  = "cas2_NaOH_runfile"          # necessary for Phreeqc
# contruct list of argument
listarg = []
for m in dico:
    cle = m+"="
    listarg.append(cle)
# get the list of argument from system

setProblemType("ChemicalTransport")
 
ChemicalStateList = []
newSpeciesList=[]

meshFileName = "alkaline.msh"
mesh = Mesh2D(meshFileName)
numberOfVertices = mesh._getNumberOfVertices()

#nodesList = mesh.getData(meshFileName,dimensions = 2)
#
# Les mailles sont de 0.04
#
quartzBody    = mesh.getBody('domain')
print quartzBody
boundary_soude = mesh.getBody('inlet')
boundary_quartz = mesh.getBody('outlet')

print " mesh ok"
#
# Base Addenda
#

Na = AqueousMasterSpecies(symbol='Na+',\
                          name='Na',\
                          element = 'Na',\
                          molarMass=MolarMass(22.9898E-3,"kg/mol"),\
                          alkalinity = 0.0)
                              
Nabis = AqueousSecondarySpecies (symbol="Na+",
                                 formationReaction = [("Na+", 1)],
                                 logK25 =0.0,
                                 name ="Na")
H4SiO4  = AqueousMasterSpecies(symbol='H4SiO4',
                               name = 'Si',\
                               element = 'SiO2',\
                               molarMass=MolarMass(28.0843E-3,'kg/mol'),\
                               alkalinity = 0.0)
H4SiO4bis = AqueousSecondarySpecies (symbol="H4SiO4",
                                     formationReaction = [("H4SiO4", 1)],\
                                     logK25 =0.0,\
                                     name ="Si")
H3SiO4 = AqueousSecondarySpecies (symbol='H3SiO4-',
                                  formationReaction = [('H4SiO4', 1),('H+', -1)],\
                                  logK25 =-9.83,\
                                  name ='H3SiO4')
Quartz = MineralSecondarySpecies(symbol='SiO2',
                                 formationReaction = [('H4SiO4', 1),('H2O', -2)],\
                                 logK25 = -3.6,\
                                 name ='Quartz',\
                                 density  = Density(2648.29,'kg/m**3'))
speciesAddenda = [Na,H4SiO4,Nabis,H4SiO4bis,H3SiO4,Quartz]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Definition of Material and Regions associated
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
solidThermalConductivity = 1.e-3
quartzMaterial = Material (name = "quartz",
                            porosity = Porosity (value = 1.0),\
                            effectiveDiffusion = EffectiveDiffusion (3.e-10),\
			    specificHeat = SpecificHeat(1.,'J/g/K'),\
			    thermalConductivity = ThermalConductivity (solidThermalConductivity,unit = "W/mK"))

region_quartz = Region (support = quartzBody, material=quartzMaterial)

region_soude  = Region (support = boundary_soude, material=quartzMaterial)

region_quartz2  = Region (support = boundary_quartz, material=quartzMaterial)

############################################################
#  Definition of all non attached variables : Velocity, ChemicalState ...
############################################################

#velocity = Velocity(Vector(0.,0.))
ChemicalStateList = []

# =========================================================
# Chemical State definition
# =========================================================

AqueousSolution_soude  = AqueousSolution (elementConcentrations=[ElementConcentration ('Na', 2.0e-02, "mol/l"),
                                                ElementConcentration ('Si', 0.0e-04, "mol/l")],
                                          pH= 12.2545 ,
                                          pe =  4.0)
chemical_state_soude   = ChemicalState ("soda", AqueousSolution_soude)

columnAqueousSolution = AqueousSolution (elementConcentrations = [ElementConcentration ("Na",0.0,"mmol/l")
                                                                 ],\
                                         pH = 7.0,\
                                         pe = 4)

columnMineralPhase = MineralPhase([MineralTotalConcentration("Quartz",10.0, "mol/l",saturationIndex = 0.0)])
columnChemicalState = ChemicalState ("column", columnAqueousSolution, columnMineralPhase)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Definition of Initial Conditions (if required)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

initial_condition_quartz = InitialCondition (body  = quartzBody, value = columnChemicalState)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Definition of Boundary Conditions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

boundary_condition_soude = BoundaryCondition (boundary = boundary_soude, btype='Dirichlet', value = chemical_state_soude)

boundary_condition_quartz = BoundaryCondition (boundary=boundary_quartz, btype='Dirichlet', value = columnChemicalState)

############################################################
#  Definition of Calculation times (if required)
############################################################

temps_initial = 0.0
#
#                       the simulation is conducted over 10 days
#
finalTime   = 3600.*24.*10

############################################################
#  Definition of Expected Outputs
############################################################

expected_outputs = [ExpectedOutput('pH',format='table',name='pH_table'),
                    ExpectedOutput('Concentration','Na',format='table',name='Na_table')]
	   
############################################################
#  Definition of Problem: Insert all previous variables in the problem
############################################################
#
# regions are associated to volumic domains
#
problem  = ChemicalTransportProblem(name               = "cas2_NaOH_runfile",
                                    regions            = [region_quartz],
                                    initialConditions  = [initial_condition_quartz],
                                    boundaryConditions = [boundary_condition_soude,boundary_condition_quartz],
                                    calculationTimes   = [temps_initial, finalTime],
                                    sources            = None,
                                    darcyVelocity=Velocity(Vector([0.0, 0.0, 0.0])),
                                    chemistryDB        = "water.dat",
                                    speciesBaseAddenda = speciesAddenda,
                                    kineticLaws        = None,
                                    activityLaw        = None,
                                    outputs            = expected_outputs)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Define the calculation module and set problem data
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

module = ChemicalTransportModule()
module.setData(problem,mesh=mesh,trace=0,algorithm="CC")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Define the Component and its solver parameters
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
module.setComponent('Elmer','Phreeqc')

module.setCouplingParameter(initialTimeStep        = 6.e+2,
                            minTimeStep            = 1.e+2,
                            maxTimeStep            = 3.5e+3,
                            couplingPrecision      = 5.e-5,
                            optimalIterationNumber = 20,
                            maxIterationNumber     = 30,
                            increaTimeStepCoef     = 1.05,
                            decreaTimeStepCoef     = 0.5)

module.transport.setTransportParameter(convSolver = 1.e-8,\
				       iterSolver = 400,\
				       indMemory = 0,\
                                       discretisation = dico['MethodChoice'],\
				       algebraicResolution = 'Iterative',\
				       timeSteppingMethod = "BDF",
# possible values are CG CGS BiCGStab TFQMR GMRES
				       preconditioner='ILU2',accelerator="GMRES")

module.run()

#~~~~~~~~~~~~~~~~~
#  Getting Outputs
#~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~
# sauvegarde des tables 
#~~~~~~~~~~~~~~~~~~~~~~
res_ph     = module.getOutput('pH_table')
res_na     = module.getOutput('Na_table')
print res_ph[-1][1]
dir(res_ph[-1][1])
print res_ph[-1][1].name
print res_ph[-1][1].column_names
print res_ph[-1][1].values[-1]

NadeX      = res_na[-1][-1]
pHdeX      = res_ph[-1][-1]
tps        = res_ph[-1][0]

liste_X   = NadeX.getColumn(0)
dx0 = liste_X[0]
liste_dx0 = [dx0] * (len(liste_X))
print len(liste_dx0)
liste_decalX = subtractLists(liste_X,liste_dx0)
print len(liste_decalX)
from posttables import Table

tab1  = Table(name='TabNa')
tab1.addColumn('X',liste_decalX)
print "dbg0 ",len(liste_decalX),len(NadeX.getColumn(1))
tab1.addColumn('Y',NadeX.getColumn(1))
print "dbg1 ",len(NadeX.getColumn(2))
tab1.addColumn('Na',NadeX.getColumn(3))
NadeX = tab1

tab2  = Table(name='TabpH')
tab2.addColumn('X',liste_decalX)
tab2.addColumn('Y',pHdeX.getColumn(1))
tab2.addColumn('pH',pHdeX.getColumn(3))
pHdeX = tab2

print 'Times = ',tps,' secondes'
print ''

pHdeX. writeToFile('pHdeX_10j.tab')
NadeX. writeToFile('NadeX_10j.tab')

############################################################
#  Comparison to analytical concentration
############################################################
dx = [0.004]

for i in range(1,30):
    dx.append(dx[0]+dx[i-1])
analFunction = analyticalFunction(finalTime, 0.02, dx, 3.e-10)
print '================================================= '
print '       comparison to the analytic solution'
print '================================================= '

table_Na_numeric = NadeX


list_Na_analytic = analFunction.evalNa()
list_Na_numeric  = table_Na_numeric.getColumn(2)
print " ana: ",list_Na_analytic[0:20]
print " num: ",list_Na_numeric[0:20]

norme_Na = normMaxListComparison(list_Na_numeric[0:30],list_Na_analytic[0:30])
print 'norme_Na = ',norme_Na
epsilon_Na = 10.E-2
if norme_Na > epsilon_Na:
    OKConc = 0
    print 'Be carefull: error on the Na concentration higher than 10% and equal to ',norme_Na*100,"%"
else :
    OKConc = 1
    print 'Good agreement between numerical and analytical results for the Na concentration, error equal to ',norme_Na*100,"%"
print ' '

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Comparison to analytical pH
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

table_pH_numeric = pHdeX

list_pH_analytic = analFunction.evalPH()
list_pH_numeric  = table_pH_numeric.getColumn(2)
print "num: ",list_pH_numeric[0:]
print "anal:",list_pH_analytic[0:20]
# on tronque la liste de la solution analytique si elle est trop longue


pHinf = normMaxListComparison(list_pH_numeric[0:30],list_pH_analytic[0:30])

print 'pH max norm is ',pHinf
if pHinf > epspH:
    OKpH = 0
    print 'Be carefull: error on the pH higher than 10% and equal to: ', pHinf*100,"%"
else :
    OKpH = 1
    print 'Good agreement between numerical and analytical results for pH, error equal to: ',pHinf*100,"%"

if (OKpH):    
    print "\n \n -- Silicate dissolution test PHREEQC/ELMER coupling OK --\n \n"
    pass
else:
    raise Warning, " Problem for the Silicate Dissolution 1D test with PHREEQC/ELMER coupling"
module.end()
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "        End of the Silicate dissolution test case "
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
