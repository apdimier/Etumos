#
# For elmer, the order of bodies must be conserved for initial conditions
#
#
from constant import epspH
import os                  # for file path
from mesh import *         # for the mesh treatment 
from datamodel import * 
import sys
from chemicaltransportmodule import *
from listtools import normMaxListComparison, subtractLists
from chemistry import FreeKineticLaw
from analytical1D_Tr0 import *
from listtools import normMaxListComparison
#
dico = { 'MethodChoice' : 'FE'}

import os
ProblemName  = "1Dexample"          # Phreeqc file 
setProblemType("ChemicalTransport")
#~~~~~~~~~~~~~~~~~~
#~ Mesh extension ~
#~~~~~~~~~~~~~~~~~~
meshFileName = "mesh.msh"
mesh = Mesh1D(meshFileName)
numberOfVertices = mesh._getNumberOfVertices()
print " within script numberOfVertices",numberOfVertices
#raw_input()

dom1Body      = mesh.getBody('domain')
inlet1Boundary   = mesh.getBody('inlet')
#~~~~~~~~~~~~~
#~ Materials ~
#~~~~~~~~~~~~~
De = 0.0
alpha = 0.02
porosity = 1.0
dom1Material = Material (name = "dom1",\
                         effectiveDiffusion = EffectiveDiffusion (De,unit="m**2/s"),\
                         porosity = Porosity(value = porosity),\
                         kinematicDispersion = KinematicDispersion (alpha,0.0,0.0))
print " within script quartzmaterial"
#~~~~~~~~~~~
#~ Regions ~
#~~~~~~~~~~~
dom1Region = Region (support = dom1Body, material=dom1Material)

#~~~~~~~~~~~~~~~~~~~
# Chemical Addenda ~
#~~~~~~~~~~~~~~~~~~~
speciesAddenda = []
# Tr
Tr = AqueousMasterSpecies("Tr", "Tr", element = "Tr", molarMass=MolarMass(1.0,'kg/mol'), alkalinity = .0)
speciesAddenda.append(Tr)
#
# Traceur
#
Tracer = AqueousSecondarySpecies ("Tr", [("Tr", 1)], logK25 = 0.0, name = "Tr")
speciesAddenda.append (Tracer)
#~~~~~~~~~~~~~~~~~~
# Chemical States ~
#~~~~~~~~~~~~~~~~~~
ChemicalStateList = []
inletMineralPhase = []
C0 = 1.e-3
inletAqueousSolution = AqueousSolution   (elementConcentrations = [ElementConcentration ("Ca",1.e-3,"mol/l"),\
                                                            ElementConcentration ("C",3.75e-3,"mol/l"),\
                                                            ElementConcentration ("Cl",3e-3,"mol/l"),\
                                                            ElementConcentration ("Amm",2e-5,"mol/l"),\
                                                            ElementConcentration ("Na",3.e-3,"mol/l"),\
                                                            ElementConcentration ("Tr",C0,"mol/l"),\
                                                            ElementConcentration ("Z",2e-5,"mol/l"),\
                                                            ElementConcentration ("Sulfate",0.2e-3,"mol/l"),\
                                                            ElementConcentration ("Urea",10e-3,"mol/l")],\
                                   pH = 7.75,pe = 4)

inletChemicalState = ChemicalState       ("inlet", inletAqueousSolution, inletMineralPhase)
#
ColumnIonicExchangers = IonicExchangers([ExchangeBindingSpecies("X-", MolesAmount(.0005, "mol"))])

columnMineralPhase = MineralPhase ([ MineralConcentration("Calcite",  3.e-3, "mol/l", saturationIndex = 0.0)])

columnAqueousSolution = AqueousSolution (elementConcentrations = [ElementConcentration ("Ca",1e-3,"mol/l"),\
                                                                  ElementConcentration ("C",3.5e-3,"mol/l"),\
                                                                  ElementConcentration ("Cl",2e-3,"mol/l"),\
                                                                  ElementConcentration ("Na",1.75e-3,"mol/l"),\
                                                                  ElementConcentration ("Z",2e-5,"mol/l"),\
                                                                  ElementConcentration ("Sulfate",0.2e-3,"mol/l")],\
                                         pH = 7.33,pe = 4)
#
columnChemicalState = ChemicalState     ("column",      columnAqueousSolution,  ionicExchanger = ColumnIonicExchangers, mineralPhase = columnMineralPhase)

kineticLaws = [ FreeKineticLaw ("Calcite",\
                                lawParameter = [50, 0.6],
                                m0 = 0.3
                               ),
                FreeKineticLaw ("ureolysis",\
                                formula = "Urea  -1.0   H2O -2  AmmH+  2  CO3-2  1",\
                                lawParameter = [3.21e-3, 1.22e-2, 1.83e-2])
	      ]
#kineticLaws = []
#~~~~~~~~~~~~~~~~~~~~
# Initial condition ~
#~~~~~~~~~~~~~~~~~~~~
initial_condition1        = InitialCondition (body  = dom1Body, value = columnChemicalState)

#~~~~~~~~~~~~~~~~~~~~~
# Boundary condition ~
#~~~~~~~~~~~~~~~~~~~~~
inlet1Boundary = BoundaryCondition (boundary = inlet1Boundary, btype='Dirichlet', value = inletChemicalState)
#outletBoundary = BoundaryCondition (boundary = outletBoundary, btype='Dirichlet', value = columnChemicalState)

# On doit rajouter une condition de symetrie dans le systeme pour traiter correctement le passage volumes finis elements finis
#
#symmetryBoundary = BoundaryCondition (boundary = symmetryBoundary, btype="Dirichlet", value = columnChemicalState)

#~~~~~~~~~~~~~~~~~~~
# Expected outputs ~
#~~~~~~~~~~~~~~~~~~~
finalTime = 32400*1.0
expectedOutputs = [     ExpectedOutput("pH", format = "table",name = "pH",timeSpecification = TimeSpecification(times=[finalTime])),\
                        ExpectedOutput("Concentration","Amm",format="table",name="Amm",timeSpecification=TimeSpecification(times=[finalTime])),\
                        ExpectedOutput("Concentration","Calcite",format="table",name="Calcite",timeSpecification=TimeSpecification(times=[finalTime])),\
                        ExpectedOutput("Concentration","C",format="table",name="C",timeSpecification=TimeSpecification(times=[finalTime])),\
                        ExpectedOutput("Concentration","Ca",format="table",name="Ca",timeSpecification=TimeSpecification(times=[finalTime])),\
                        ExpectedOutput("Concentration","Amm",format="table",name="Amm",timeSpecification=TimeSpecification(times=[finalTime])),\
                        ExpectedOutput(quantity='Concentration',unknown="Tr",format='table',unit='molal',name="Tr",\
                        timeSpecification=TimeSpecification(times=[finalTime])),\
                        ExpectedOutput("Concentration","ureolysis",format="table",name="ureolysis",timeSpecification=TimeSpecification(times=[finalTime]))]
#raw_input(" expected outputs")

# Module ~
#~~~~~~~~~
darcy = 3.5e-7
#
module = ChemicalTransportModule()
problem  = ChemicalTransportProblem(name               = "1Dexample",\
                                    regions            = [dom1Region],\
                                    initialConditions  = [initial_condition1],\
                                    boundaryConditions = [inlet1Boundary],\
                                    calculationTimes   = [0.0,finalTime],\
                                    sources            = None,\
                                    darcyVelocity      = Velocity(Vector([darcy, 0.0, 0.0])),\
                                    chemistryDB        = "phrqc_calcite1.dat",\
                                    speciesBaseAddenda = speciesAddenda,\
                                    kineticLaws        = kineticLaws,\
                                    activityLaw        = None,\
                                    outputs            = expectedOutputs)
#raw_input(" module set data")
module.setData(problem,unstructured=1,mesh=mesh,trace=0,algorithm="CC")
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Define the Component and its solver parameters
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
module.setComponent('Elmer','Phreeqc')
#
module.setCouplingParameter(initialTimeStep          = 1.0,
                            minTimeStep              = 1.0e+1,
                            maxTimeStep              = 3.e+02,
                            couplingPrecision        = 1e-02,
                            maxIterationNumber       = 40,
                            optimalIterationNumber   = 20,
                            increaTimeStepCoef       = 1.05,
                            decreaTimeStepCoef       = 0.75)

module.transport.setTransportParameter(convSolver = 1.e-10,
				       iterSolver = 600,
				       indMemory = 0,
                                       discretisation = dico['MethodChoice'],
				       algebraicResolution = 'Iterative',
# possible values are CG CGS BiCGStab TFQMR GMRES
                                       timeSteppingMethod = "BDF",BDFOrder = "1",
				       preconditioner='ILU0',
				       accelerator="GMRES")
#module.setVtkOutputsParameters(["Ca","pH","Urea","Calcite","C","Amm","ureolysis","Tr"],"s",10800)
#module.setVtkOutputsParameters(["Ca","pH","ureolysis","Tr"],"s",10800)
#list_of_species_toplot = ["Ca","pH","ureolysis","Tr"]
#pointtoplot = 5
#if list_of_species_toplot !=[]:
#module.setInteractivePlot(" module ",list_of_species_toplot,pointtoplot,plotfrequency=30)
#module.setInteractiveSpatialPlot([ExpectedOutput('Concentration','Cl',format='table',unit='molal',                              name='Cl')])

module.run()
outTr = module.getOutput("Tr")
coordinates = outTr[-1][1].getColumn(0)
#print "coordinates", outTr[-1][1].getColumn(0)
#print "values", outTr[-1][1].getColumn(-1)
numericalSolution = outTr[-1][1].getColumn(-1)
analFunction = AnalyticalFunction1D_Tr(outTr[-1][1].getColumn(0)[0:100], C0, 0.0, finalTime, darcy, De + alpha*darcy)
analyticalSolution = analFunction.eval()
#print analyticalSolution
epsilonT = 3.E-2
normTr = normMaxListComparison(numericalSolution[1:15],analyticalSolution[1:15])
#for i in range(1,20):
#    print i,numericalSolution[i],analyticalSolution[i]
#print " norm max ",normTr
#print  "~~~~~~~~~~~~~~~"
#print " Calcite outputs~"
#print "~~~~~~~~~~~~~~~~"
#outCalcite = module.getOutput("Calcite")[-1][1].getColumn(-1)
#
#for ind in range (1,20):
#    print coordinates[ind],outCalcite[ind]
#
ok = 1
if normTr < epsilonT:
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "~    End of the stable sample case    ~"
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
else:
    raise Exception, " The test case is not stable"
module.end()
#http://www.youtube.com/watch?v=vf9boOR1KXA&list=RD02ckSgSiFf6K8
