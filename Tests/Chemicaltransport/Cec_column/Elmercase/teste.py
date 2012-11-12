from constant import epspH
import os                  # for file path
from mesh import *         # for Meshes treatment 
from datamodel import *   
import sys
from chemicaltransportmodule import *
from listtools import normMaxListComparison, subtractLists

dico = { 'MethodChoice' : 'FE'}

ProblemName  = "guitest1_e"          # Phreeqc file 
setProblemType("ChemicalTransport")

meshFileName = "essai.msh"
mesh = MeshReader(meshFileName)
numberOfVertices = mesh._getNumberOfVertices()
print "numberOfVertices",numberOfVertices

columnBody    = mesh.getBody('domain')
#print columnBody
inletBoundary = mesh.getBody('inlet')
#print " script outletBoundary ",inletBoundary.getBodyName()
#print inletBoundary.getBodyNodesList()
#raw_input()

#~~~~~~~~~~~~~
#~ Materials ~
#~~~~~~~~~~~~~
darcy = 0. # 1.e-3/3600
##columnMaterial = Material (name = "column",effectiveDiffusion = EffectiveDiffusion ((3.0e-10+0.0006670*darcy),unit="m**2/s"),\
##                                           permeability = Permeability(value = 1.0),\
##                                           porosity = Porosity(value = 1.0))
                                           #,\
                                           #kinematicDispersion = KinematicDispersion (0.000667,0))
columnMaterial = Material (name = "column",effectiveDiffusion = EffectiveDiffusion ((3.0e-10),unit="m**2/s"),\
                                           permeability = Permeability(value = 1.0),\
                                           porosity = Porosity(value = 1.0),kinematicDispersion = KinematicDispersion (0.000667,0))

#~~~~~~~~~~~~~~~~~~~
# Chemical Addenda ~
#~~~~~~~~~~~~~~~~~~~
speciesAddenda = []
TAMS = AqueousMasterSpecies(symbol = "T+",\
                            name = "T",\
                            element = "T",\
                            molarMass = MolarMass(35,"g/mol"),\
                            alkalinity = 0)
speciesAddenda.append(TAMS)
TSSp = AqueousSecondarySpecies(symbol = "T+",\
                               formationReaction = [\
                               ("T+",1)],\
                               logK25 = 0.0,\
                               name = "T")
speciesAddenda.append(TSSp)
Na = AqueousMasterSpecies(symbol = "Na+",\
                          name = "Na",\
                          element = "Na",\
                          molarMass = MolarMass(22.9898,"g/mol"),\
                          alkalinity = 0.0)
speciesAddenda.append(Na)
K = AqueousMasterSpecies(symbol = "K+",\
                         name = "K",\
                         element = "K",\
                         molarMass = MolarMass(39.102,"g/mol"),\
                         alkalinity = 0.0)
speciesAddenda.append(K)
Cl = AqueousMasterSpecies(symbol = "Cl-",\
                          name = "Cl",\
                          element = "Cl",\
                          molarMass = MolarMass(35.453,"g/mol"),\
                          alkalinity = 0.0)
speciesAddenda.append(Cl)
NaSSp = AqueousSecondarySpecies(symbol = "Na+",\
                                formationReaction = [("Na+",1)],\
                                logK25 = 0.0,\
                                name = "Na",)
speciesAddenda.append(NaSSp)
KSSp = AqueousSecondarySpecies(symbol = "K+",\
                               formationReaction = [("K+",1)],\
                               logK25 = 0.0,\
                               name = "K",)
speciesAddenda.append(KSSp)
ClSSp = AqueousSecondarySpecies(symbol = "Cl-",\
                                formationReaction = [("Cl-",1)],\
                                logK25 = 0.0,\
                                name = "Cl",)
X = SorbingSiteMasterSpecies(symbol = "X-",name   = "X")
speciesAddenda.append(X)
XESp = SorbedSecondarySpecies(symbol = "X-",\
                              formationReaction = [("X-",1)],\
                              logK25 = 0.0,\
                              name = "X",)
speciesAddenda.append(XESp)
speciesAddenda.append(ClSSp)
NaXESp = SorbedSecondarySpecies(symbol = "NaX",\
                                formationReaction = [("Na+",1),("X-",1)],\
                                logK25 = 0.0,\
                                name = "NaX",)
speciesAddenda.append(NaXESp)
KXESp = SorbedSecondarySpecies(symbol = "KX",\
                               formationReaction = [("K+",1),("X-",1)],\
                               logK25 = 0.0,\
                               name = "KX",)
speciesAddenda.append(KXESp)
HXESp = SorbedSecondarySpecies(symbol = "HX",\
                               formationReaction = [("H+",1),("X-",1)],\
                               logK25 = -99.,\
                               name = "HX",)
speciesAddenda.append(HXESp)
#~~~~~~~~~~~~~~~~~~
# Chemical States ~
#~~~~~~~~~~~~~~~~~~
ChemicalStateList = []
columnIonicExchangers = IonicExchangers([ExchangeBindingSpecies("X", MolesAmount(2.0e-3, "mol"))])
columnAqueousSolution = AqueousSolution (elementConcentrations = [ElementConcentration ("Na",2.0e-3,"mol/l"),\
                                                                  ElementConcentration ("Cl",2.e-3,"mol/l"),\
                                                                  ElementConcentration ("K",0.e-0,"mol/l")\
                                                                 ],\
                                         pH = 7.0,\
                                         pe = 4)
columnChemicalState = ChemicalState ("column",columnAqueousSolution ,ionicExchanger = columnIonicExchangers)

boundaryAqueousSolution = AqueousSolution (elementConcentrations = [ElementConcentration ("K",1.e-3,"mol/l"),\
                                                                    ElementConcentration ("T",1.e-3,"mol/l"),\
                                                                    ElementConcentration ("Na",1.e-15,"mol/l"),\
                                                                    ElementConcentration ("Cl",1.e-3,"mol/l")\
                                                                   ],\
                                           pH = 7.0,\
                                           pe = 4)
boundaryChemicalState = ChemicalState ("boundary",boundaryAqueousSolution)
#~~~~~~~~~~~
#~ Regions ~
#~~~~~~~~~~~
columnRegion = Region (support = columnBody, material = columnMaterial)

inletRegion  = Region (support = inletBoundary, material = columnMaterial)

#~~~~~~~~~~~~~~~~~~~~
# Initial condition ~
#~~~~~~~~~~~~~~~~~~~~
columnIC = InitialCondition (body  = columnBody, value = columnChemicalState)
#~~~~~~~~~~~~~~~~~~~~~
# Boundary condition ~
#~~~~~~~~~~~~~~~~~~~~~
inletBC  = BoundaryCondition (boundary = inletBoundary, btype="Dirichlet", value = boundaryChemicalState)
#~~~~~~~~~~~~~~~~~~~
# Expected outputs ~
#~~~~~~~~~~~~~~~~~~~
expectedOutputs = [ExpectedOutput("Concentration","T",format="table",name="T_output"),\
ExpectedOutput("Concentration","KX",format="table",name="KX_output"),\
ExpectedOutput("Concentration","NaX",format="table",name="NaX_output"),\
ExpectedOutput("Concentration","K",format="table",name="K_output")]
#~~~~~~~~~
# Module ~
#~~~~~~~~~
module = ChemicalTransportModule()
problem  = ChemicalTransportProblem(name               = "guiteste",\
                                    regions            = [columnRegion, inletRegion],\
                                    initialConditions  = [columnIC],\
                                    boundaryConditions = [inletBC],\
                                    calculationTimes   = [0.0,24000.],\
                                    sources            = None,\
                                    darcyVelocity      = Velocity(Vector([darcy,0.0,0.0])),\
                                    chemistryDB        = "water_gui.dat",\
                                    speciesBaseAddenda = speciesAddenda,\
                                    kineticLaws        = None,\
                                    activityLaw        = None,\
                                    outputs            = expectedOutputs)
module.setData (problem, mesh=mesh, trace=0, algorithm="CC")
module.setComponent('Elmer','Phreeqc')
# possible values are CG CGS BiCGStab TFQMR GMRES

#module.transport.setTransportParameter(convSolver = 1.e-8,\
#				       iterSolver = 400,\
#				       indMemory = 0,\
#                                       discretisation = dico['MethodChoice'],\
#				       algebraicResolution = 'Iterative',\
#				       timeSteppingMethod = "BDF",BDFOrder = "1",\
#				       preconditioner='ILU1',accelerator="CG")
#				       timeSteppingMethod = "BDF",\
#				       preconditioner='ILU0',accelerator="TFQMR",thetaScheme=0.0)
				       
module.setCouplingParameter(couplingPrecision      = 2e-03,
                            initialTimeStep        = 1,
                            minTimeStep            = 0.1,
                            maxTimeStep            = 150,
                            optimalIterationNumber = 20,
                            maxIterationNumber     = 30,
                            increaTimeStepCoef     = (0.5)**(-0.2),
                            decreaTimeStepCoef     = 0.5)
module.setVtkOutputsParameters(["Na"],"s",150)
module.launch()
#print module.transport.getPermutation()
#raw_input()
while (module.simulatedTime < module.times[-1]):
    module.oneTimeStep()
    pass
#~~~~~~~~~~~~~~~~~~
# Post processing ~
#~~~~~~~~~~~~~~~~~~
K_unk     = module.getOutput('K_output')
KX_unk     = module.getOutput('KX_output')
print "KX =",KX_unk[-1][1].getColumn(3)[0:30]
T_unk     = module.getOutput('T_output')
print "tracor =",T_unk[-1][1].getColumn(3)[0:30]
time        = K_unk[-1][0]
print "time = ",time
KY      = K_unk[-1][1]
TY      = T_unk[-1][1]

XListe   = KY.getColumn(0)
dx0 = 0.04/100
dxListe = [dx0] * 100

from posttables import Table

tab1  = Table(name='KY')
tab1.addColumn('X',XListe)
tab1.addColumn('Y',KY.getColumn(1))
tab1.addColumn('K',KY.getColumn(3))
KY = tab1
tab2  = Table(name='KT')
tab2.addColumn('X',XListe)
tab2.addColumn('Y',TY.getColumn(1))
tab2.addColumn('K',TY.getColumn(3))
TY = tab2

from _erffunctions import *

C0 = 1.0e-03
porosity = 1.0
darcy = 1.e-3/3600
darcy = 0.
R = 1.  #Retardation factor for the tracer
longDis = 3.e-10 + 6.670e-4*darcy
AnalT = []
from math import exp
den = 1./(2.*sqrt(longDis*time/(porosity*R)))
C1 = darcy*time/(porosity*R)
x = 0.0004
for dx in dxListe:
    value = erfc((x-C1)*den)
    value1 = exp(x*darcy/longDis)*erfc((x+C1)*den)
    value = 0.5*C0*(value+value1)
    AnalT.append(value)
    x+=dx
TCompare = []
for i in range(40):
    if i%2 != 0:
        TCompare.append(TY.getColumn(-1)[i])
    
tracerNorm = normMaxListComparison(TCompare,AnalT[0:20])
print " AnalT =",AnalT[0:30]
print 'tracer norm  = ',tracerNorm
#
# R = 1 + Kd*2500*(1-porosity)/porosity (pho = 1 here)
#
R = 3. #Retardation factor = 1 + dq/dc = cec*(fraction of exchangeable ion )/aqueous
AnalK = []
den = 1./(2.*sqrt(longDis*time/(porosity*R)))
C1 = darcy*time/(porosity*R)
x = 0.0004
for dx in dxListe:
    value = erfc((x-C1)*den)
    value1 = exp(x*darcy/longDis)*erfc((x+C1)*den)
    value = 0.5*C0*(value+value1)
    AnalK.append(value)
    x+=dx
#    print " k x ",x,value
print "K      =",KY.getColumn(-1)[0:40]
print " AnalK =",x,AnalK[0:40]
KCompare = []
for i in range(40):
    if i%2 != 0:
        KCompare.append(KY.getColumn(-1)[i])

sorptionNorm = normMaxListComparison(KCompare,AnalK[0:20])
print 'sorption norm = ',sorptionNorm
if sorptionNorm < 0.1 and tracerNorm < 0.1 : # if you want a better precision work on time step or increase the simulated time
    print "~~~~~~~~~~~~~~~\nThe Kd test is OK\n~~~~~~~~~~~~~~~\n"
else:
    print "~~~~~~~~~~~~~~~\nThe Kd test is KO\n~~~~~~~~~~~~~~~\n"
module.end()
