from constant import epspH
from datamodel import *
import fields
from listtools import normMaxListComparison, subtractLists
from chemicaltransport import *
from chemicaltransportmodule import *
from mt3d import Mt3d              # mt3d
from cartesianmesh import *        # Cartesian mesh
from phreeqc import *              # phreeqc

import os
Phreeqc_file = "guitest.txt"      # bounded to Phreeqc
ProblemName  = "guitest"          # Phreeqc file 
mesh = CartesianMesh2D("global","XY")
nx  = 101
ny  = 1
#~~~~~~~~~~~~~~~~~~
#~ Mesh extension ~
#~~~~~~~~~~~~~~~~~~
deltax = []
dx = [0.0001/1]*1
deltax.extend(dx)
dx = [0.1/100]*100
deltax.extend(dx)
deltay = []
dy = [1.0/1]*1
deltay.extend(dy)
mesh.setdAxis("X",deltax)
mesh.setdAxis("Y",deltay)
boundary0Body = CartesianMesh2D("boundary", "XY")
boundary0Body.setZone("boundary",index_min = Index2D (1,1), index_max = Index2D (1,1))
column1Body = CartesianMesh2D("column", "XY")
column1Body.setZone("column",index_min = Index2D (2,1), index_max = Index2D (101,1))
#~~~~~~~~~~~~~
#~ Materials ~
#~~~~~~~~~~~~~
columnMaterial = Material (name = "column",effectiveDiffusion = EffectiveDiffusion (0.0,unit="m**2/s"),\
permeability = Permeability(value = 1.0),\
porosity = Porosity(value = 0.25),\
kinematicDispersion = KinematicDispersion (0.002,1))

#~~~~~~~~~~~
#~ Regions ~
#~~~~~~~~~~~
boundary0Region = Region(support=boundary0Body, material= columnMaterial)
column1Region = Region(support=column1Body, material= columnMaterial)
#~~~~~~~~~~~~~~~~~~~
# Chemical Addenda ~
#~~~~~~~~~~~~~~~~~~~
speciesAddenda = []
CsAMS = AqueousMasterSpecies(symbol = "Cs+",\
                             name = "Cs",\
                             element = "Cs",\
                             molarMass = MolarMass(135,"g/mol"),\
                             alkalinity = 0.0)
speciesAddenda.append(CsAMS)
TAMS = AqueousMasterSpecies(symbol = "T+",\
                            name = "T",\
                            element = "T",\
                            molarMass = MolarMass(1.008,"g/mol"),\
                            alkalinity = 0.0)
speciesAddenda.append(TAMS)
CsSSp = AqueousSecondarySpecies(symbol = "Cs+",\
                                formationReaction = [\
                                                     ("Cs+",1)],\
                                logK25 = 0.0,\
                                name = "Cs")
speciesAddenda.append(CsSSp)
TSSp = AqueousSecondarySpecies(symbol = "T+",\
                               formationReaction = [\
                                                    ("T+",1)],\
                               logK25 = 0.0,\
                               name = "T")
speciesAddenda.append(TSSp)
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
columnIC = InitialCondition (body  = column1Body, value = columnChemicalState)
#~~~~~~~~~~~~~~~~~~~~~
# Boundary condition ~
#~~~~~~~~~~~~~~~~~~~~~
boundaryBC = BoundaryCondition (boundary = boundary0Body, btype="Dirichlet", value = boundaryChemicalState)
#~~~~~~~~~~~~~~~~~~~
# Expected outputs ~
#~~~~~~~~~~~~~~~~~~~
expectedOutputs = [ExpectedOutput("Concentration","Cs",format="table",name="CsOutput")]
#~~~~~~~~~
# Module ~
#~~~~~~~~~
module = ChemicalTransportModule()
problem  = ChemicalTransportProblem(name               = "guitest",\
                                    regions            = [boundary0Region,column1Region],\
                                    initialConditions  = [columnIC],\
                                    boundaryConditions = [boundaryBC],\
                                    calculationTimes   = [0.0,32400.0],\
                                    sources            = None,\
                                    darcyVelocity      = Velocity(Vector([3.5e-7,0.0,0.0])),\
                                    chemistryDB        = "/home/dimier/Wrapper/Phreeqc_dat/phreeqc.dat",\
                                    speciesBaseAddenda = speciesAddenda,\
                                    kineticLaws        = None,\
                                    activityLaw        = None,\
                                    outputs            = expectedOutputs)
module.setData (problem, trace = 0, mesh = mesh, algorithm="CC")

module.setComponent("mt3d","phreeqc")
module.setTransportParameters("T.V.D.")
module.setTransportParameters("Jacobi",1e-20)
module.setCouplingParameter(initialTimeStep        = 200.0,
                            minTimeStep            = 200.0,
                            maxTimeStep            = 200.0,
                            couplingPrecision      = 1e-05,
                            optimalIterationNumber = 20,
                            maxIterationNumber     = 30,
                            decreaTimeStepCoef     = 0.5,
                            increaTimeStepCoef     = 1.05)
module.run()
#~~~~~~~~~~~~~~~~~~
# Post processing ~
#~~~~~~~~~~~~~~~~~~
#=========================
# sauvegarde des tables 
#=========================
res_cs     = module.getOutput('CsOutput')
tab = []

CsdeX      = res_cs[-1][1]

#=========================
# dx0 translation
#=========================
liste_X   = CsdeX.getColumn(0)
dx0 = dx [0]
liste_dx0 = [dx0] * (len(liste_X))
liste_decalX = subtractLists(liste_X,liste_dx0)

from posttables import Table

resTable = Table(name="TabCs")
resTable.addColumn("X",liste_decalX)
resTable.addColumn("Y",CsdeX.getColumn(1))
resTable.addColumn("Cs",CsdeX.getColumn(2))
CsdeX = resTable
print 'len(CsdeX.getColumn(2)) =',len(CsdeX.getColumn(2))

CsdeX. writeToFile('CsdeX_10j.tab')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Comparison to analytical concentration ~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "       compared to analytical solution"
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

table_Cs_numeric = CsdeX

table_Cs_analytic = Table(name="analytical_solution")
f_name = "CsdeX_ana.tab"
table_Cs_analytic.readFromFile(f_name,nbcolumns = 2,columnsNames = 'no',name = 'no')

Cs_analytic = table_Cs_analytic.getColumn(1)
print 'Cs_analytic',Cs_analytic[0:50]
Cs_numeric  = table_Cs_numeric.getColumn(2)
print 'Cs_numeric',Cs_numeric[0:50]

list1 = []
print 'len(Cs_numeric)',len(Cs_numeric)
print 'len(Cs_analytic)',len(Cs_analytic)
for i in range(len(Cs_analytic)):
        list1.append(Cs_analytic[i])
Cs_analytic = list1[0:50]
Cs_numeric = Cs_numeric[0:50]
CsNorm = normMaxListComparison(Cs_numeric,Cs_analytic)
print 'Cs norm = ',CsNorm
epsilon_Cs = 10.E-2
if CsNorm > epsilon_Cs:
    OKConc = 0
    message = "Error on the Cs concentration higher than 10% and equal to: "+str(CsNorm)
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
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "        End of the guitest case ~"
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

module.end()
