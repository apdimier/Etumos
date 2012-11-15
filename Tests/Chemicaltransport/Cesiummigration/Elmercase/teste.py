#
# Runfile: this file has been generated through the Interface.
#
from constant import epspH
import os                  # for file path
from mesh import *         # for Meshes treatment 
from datamodel import * 
import sys
from chemicaltransportmodule import *
from listtools import normMaxListComparison, subtractLists

setProblemType("ChemicalTransport")
dico = { 'MethodChoice' : 'FE'}

Phreeqc_file = "guitest.txt"      # bounded to Phreeqc
ProblemName  = "guitest"          # Phreeqc file 
PhreeqcDB = "phreeqc.dat"

#~~~~~~~~~~~~~~~~~~
#~ Mesh extension ~
#~~~~~~~~~~~~~~~~~~
meshFileName = "cesium.msh"
mesh = Mesh2D(meshFileName)
numberOfVertices = mesh._getNumberOfVertices()
columnBody      = mesh.getBody('domain')
inletBoundary   = mesh.getBody('inlet')
outletBoundary  = mesh.getBody('outlet')
#~~~~~~~~~~~~~
#~ Materials ~
#~~~~~~~~~~~~~
#medium = Material (name = "medium",effectiveDiffusion = EffectiveDiffusion (0.002*3.5e-7/0.25,unit="m**2/s"),\
medium = Material (name = "medium",effectiveDiffusion = EffectiveDiffusion (0.0,unit="m**2/s"),\
                                permeability = Permeability(value = 1.0),\
                                porosity = Porosity(value = 0.25),
                                kinematicDispersion = KinematicDispersion (0.002,0))

#~~~~~~~~~~~
#~ Regions ~
#~~~~~~~~~~~
inletRegion     = Region(support = inletBoundary,       material = medium)
outletRegion    = Region(support = outletBoundary,      material = medium)
columnRegion    = Region(support = columnBody,          material = medium)
#~~~~~~~~~~~~~~~~~~~
# Chemical Addenda ~
#~~~~~~~~~~~~~~~~~~~
speciesAddenda = []
Cs = AqueousMasterSpecies(symbol = "Cs+",\
                          name = "Cs",\
                          element = "Cs",\
                          molarMass = MolarMass(135,"kg/mol"),\
                          alkalinity = 0.0)
speciesAddenda.append(Cs)
Tr = AqueousMasterSpecies(symbol = "Tr+",\
                         name = "Tr",\
                         element = "Tr",\
                         molarMass = MolarMass(1.008,"kg/mol"),\
                         alkalinity = 0.0)
speciesAddenda.append(Tr)
CsSSp = AqueousSecondarySpecies(symbol = "Cs+",\
                                formationReaction = [("Cs+",1)],\
                                logK25 = 0.0,\
                                name = "Cs")
speciesAddenda.append(CsSSp)
TrSSp = AqueousSecondarySpecies(symbol = "Tr+",\
                               formationReaction = [("Tr+",1)],\
                               logK25 = 0.0,\
                               name = "Tr")
speciesAddenda.append(TrSSp)
Z = SorbingSiteMasterSpecies(symbol = "Z-",name   = "Z")
speciesAddenda.append(Z)
ZESp = SorbedSecondarySpecies(symbol = "Z-",\
                              formationReaction = [("Z-",1)],\
                              logK25 = 0.0,\
                              name = "Z",)
speciesAddenda.append(ZESp)
HZESp = SorbedSecondarySpecies(symbol = "HZ",\
                               formationReaction = [("H+",1),("Z-",1)],\
                               logK25 = -99.0,\
                               name = "HZ",)
speciesAddenda.append(HZESp)
NaZESp = SorbedSecondarySpecies(symbol = "NaZ",\
                                formationReaction = [("Na+",1),("Z-",1)],\
                                logK25 = 0.0,\
                                name = "NaZ",)
speciesAddenda.append(NaZESp)
CsZESp = SorbedSecondarySpecies(symbol = "CsZ",\
                                formationReaction = [("Cs+",1),("Z-",1)],\
                                logK25 = 0.5,\
                                name = "CsZ",)
speciesAddenda.append(CsZESp)
#~~~~~~~~~~~~~~~~~~
# Chemical States ~
#~~~~~~~~~~~~~~~~~~
ChemicalStateList = []
columnIonicExchangers = IonicExchangers([ExchangeBindingSpecies("NaZ", MolesAmount(0.0018, "mol"))])
columnAqueousSolution = AqueousSolution (elementConcentrations = [ElementConcentration ("Na",1.e-2,"mol/l")
                                                                 ],\
                                         pH = 7.0,\
                                         pe = 4)
columnChemicalState = ChemicalState ("column",columnAqueousSolution ,ionicExchanger = columnIonicExchangers)

boundaryIonicExchangers = IonicExchangers([ExchangeBindingSpecies("NaZ", MolesAmount(0.0, "mol"))])
boundaryAqueousSolution = AqueousSolution (elementConcentrations = [ElementConcentration ("Cs",1.e-6,"mol/l"),
                                                                    ElementConcentration ("Na",1.e-2,"mol/l"),
                                                                    ElementConcentration ("T",1.e-6,"mol/l")
                                                                   ],\
                                           pH = 7.0,\
                                           pe = 4)
boundaryChemicalState = ChemicalState ("boundary",boundaryAqueousSolution ,ionicExchanger = boundaryIonicExchangers)

#~~~~~~~~~~~~~~~~~~~~
# Initial condition ~
#~~~~~~~~~~~~~~~~~~~~
columnIC = InitialCondition (body  = columnBody, value = columnChemicalState)
#~~~~~~~~~~~~~~~~~~~~~
# Boundary condition ~
#~~~~~~~~~~~~~~~~~~~~~
inletBC  = BoundaryCondition (boundary = inletBoundary, btype="Dirichlet", value = boundaryChemicalState)
#
outletBC = BoundaryCondition (boundary = outletBoundary, btype="Dirichlet", value = columnChemicalState)
#~~~~~~~~~~~~~~~~~~~
# Expected outputs ~
#~~~~~~~~~~~~~~~~~~~
expectedOutputs = [ExpectedOutput('Concentration','Cs',format='table',name='CsOutput')]
#~~~~~~~~~
# Module ~
#~~~~~~~~~
#                                    darcyVelocity      = Velocity(Vector([3.5e-7/0.25,0.0,0.0])),\
module = ChemicalTransportModule()
problem  = ChemicalTransportProblem(name               = "guitest",\
                                    regions            = [inletRegion,outletRegion,columnRegion],\
                                    initialConditions  = [columnIC],\
                                    boundaryConditions = [inletBC,outletBC],\
                                    calculationTimes   = [0.0,32400.0],\
                                    sources            = None,\
                                    darcyVelocity      = Velocity(Vector([3.5e-7, 0.0, 0.0])),\
                                    chemistryDB        = "phreeqc.dat",\
                                    speciesBaseAddenda = speciesAddenda,\
                                    kineticLaws        = None,\
                                    activityLaw        = None,\
                                    outputs            = expectedOutputs)
module.setData (problem, trace = 0, mesh = mesh, algorithm="CC")

module.setComponent('Elmer','Phreeqc')
module.transport.setTransportParameter(convSolver = 1.e-9,\
                                       iterSolver = 600,\
                                       indMemory = 0,\
                                       discretisation = dico['MethodChoice'],\
                                       algebraicResolution = 'Iterative',\
                                       timeSteppingMethod = "BDF",BDFOrder = "1",
# possible values are CG CGS BiCGStab TFQMR GMRES
                                       preconditioner='ILU0',accelerator="GMRES")
module.setCouplingParameter(initialTimeStep        = 1,
                            maxTimeStep            = 100.0,
                            minTimeStep            = 0.1,
                            couplingPrecision      = 5.e-05,
                            optimalIterationNumber = 20,
                            maxIterationNumber     = 30,
                            increaTimeStepCoef     = 1.025,
                            decreaTimeStepCoef     = 0.5,
                            chat		   = True)
#                            
module.run()
#
#~~~~~~~~~~~~~~~~~
#  Getting Outputs
#~~~~~~~~~~~~~~~~~

#=========================
# sauvegarde des tables 
#=========================
res_cs     = module.getOutput('CsOutput')
tab = []

CsdeX      = res_cs[-1][1]
print CsdeX.getColumn(0)
print CsdeX.getColumn(1)
print CsdeX.getColumn(2)
print CsdeX.getColumn(3)
#raw_input("column 3")
#=========================
# dx0 translation
#=========================

from posttables import Table

resTable = Table(name="TabCs")
resTable.addColumn("X",CsdeX.getColumn(0))
resTable.addColumn("Y",CsdeX.getColumn(1))
resTable.addColumn("Cs",CsdeX.getColumn(3))
CsdeX = resTable
print 'len(CsdeX.getColumn(2)) =',len(CsdeX.getColumn(2))

CsdeX. writeToFile('CsdeX_10j.tab')
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Comparison to analytical concentration ~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "      compared to analytical solution "
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
#
table_Cs_numeric = CsdeX
#
table_Cs_analytic = Table(name="analytical_solution")
f_name = "../CsdeX_ana.tab"
table_Cs_analytic.readFromFile(f_name,nbcolumns = 2,columnsNames = 'no',name = 'no')
#
Cs_analytic = table_Cs_analytic.getColumn(1)
print 'Cs_analytic',Cs_analytic[0:50]
Cs_numeric  = table_Cs_numeric.getColumn(2)
print type(table_Cs_numeric)
print 'Cs_numeric',Cs_numeric[:]
list1 = []
print 'len(Cs_numeric)',len(Cs_numeric)
print 'len(Cs_analytic)',len(Cs_analytic)
for i in range(len(Cs_analytic)):
    list1.append(Cs_analytic[i])
Cs_analytic = list1[0:20]
#ind = 0
#Cs_numeric2 = []
#for i in range(2,52):
#    if ind%2 == 0:
#        Cs_numeric2.append(Cs_numeric[i])
#    ind+=1
#print Cs_numeric2
print Cs_numeric
CsNorm = normMaxListComparison(Cs_numeric[2:22],Cs_analytic)
print 'Cs norm = ',CsNorm
epsilon_Cs = 10.e-2
if CsNorm > epsilon_Cs:
    OKConc = 0
    message = "Error on the Cs concentration higher than 5% and equal to: "+str(CsNorm)
    raise Warning, message
else :
    OKConc = 1
    print "Good agreement between numerical and analytical results for the Cs concentration, error equal to ", CsNorm
print ' '

print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "        End of the Cesium case ~"
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
#~~~~~~
# END ~
#~~~~~~
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "        End of the teste case ~"
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
