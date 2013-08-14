#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# That test case is issued from the phreeqC examples. The 
# same physical behavior is stated, but due to the dis.
# of the advection scheme, no direct comparison to
# phreeqc results can be made
#
# see the Ex11 of the phreeqC manual for a description of the case
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
nx  = 51
ny  = 1
#~~~~~~~~~~~~~~~~~~
#~ Mesh extension ~
#~~~~~~~~~~~~~~~~~~
deltax = []
dx = [0.01/1]*1
deltax.extend(dx)
dx = [0.1/(nx-1)]*(nx-1)
deltax.extend(dx)
deltay = []
dy = [0.1/1]*1
deltay.extend(dy)
mesh.setdAxis("X",deltax)
mesh.setdAxis("Y",deltay)
column0Body = CartesianMesh2D("column", "XY")
column0Body.setZone("column",index_min = Index2D (2,1), index_max = Index2D (nx,1))
boundary1Body = CartesianMesh2D("boundary", "XY")
boundary1Body.setZone("boundary",index_min = Index2D (1,1), index_max = Index2D (1,1))
#~~~~~~~~~~~~~
#~ Materials ~
#~~~~~~~~~~~~~
materialMaterial = Material (name = "material",effectiveDiffusion = EffectiveDiffusion (3.0e-9,unit="m**2/s"),\
permeability = Permeability(value = 1.0),\
porosity = Porosity(value = 1.0),\
kinematicDispersion = KinematicDispersion (0.0,0))

#~~~~~~~~~~~
#~ Regions ~
#~~~~~~~~~~~
column0Region = Region(support=column0Body, material= materialMaterial)
boundary1Region = Region(support=boundary1Body, material= materialMaterial)
#~~~~~~~~~~~~~~~~~~~
# Chemical Addenda ~
#~~~~~~~~~~~~~~~~~~~
speciesAddenda = []
ClAMS = AqueousMasterSpecies(symbol = "Cl-",\
                             name = "Cl",\
                             element = "Cl",\
                             molarMass = MolarMass(35.4532,"g/mol"),\
                             alkalinity = 0.0)
speciesAddenda.append(ClAMS)
NaAMS = AqueousMasterSpecies(symbol = "Na+",\
                             name = "Na",\
                             element = "Na",\
                             molarMass = MolarMass(22.9898,"g/mol"),\
                             alkalinity = 0.0)
speciesAddenda.append(NaAMS)
CaAMS = AqueousMasterSpecies(symbol = "Ca++",\
                             name = "Ca",\
                             element = "Ca",\
                             molarMass = MolarMass(40.08,"g/mol"),\
                             alkalinity = 0.0)
speciesAddenda.append(CaAMS)
Nm3AMS = AqueousMasterSpecies(symbol = "NH4+",\
                              name = "N(-3)",\
                              element = "N",\
                              molarMass = MolarMass(14.067,"g/mol"),\
                              alkalinity = 0.0)
speciesAddenda.append(Nm3AMS)
NAMS = AqueousMasterSpecies(symbol = "NO3-",\
                            name = "N",\
                            element = "N",\
                            molarMass = MolarMass(14.067,"g/mol"),\
                            alkalinity = 0.0)
speciesAddenda.append(NAMS)
Np3AMS = AqueousMasterSpecies(symbol = "N2",\
                              name = "N(+3)",\
                              element = "N",\
                              molarMass = MolarMass(14.067,"g/mol"),\
                              alkalinity = 0)
speciesAddenda.append(Np3AMS)
Np5AMS = AqueousMasterSpecies(symbol = "NO3-",\
                              name = "N(+5)",\
                              element = "N",\
                              molarMass = MolarMass(14.067,"g/mol"),\
                              alkalinity = 0.0)
speciesAddenda.append(Np5AMS)
N0AMS = AqueousMasterSpecies(symbol = "N2",\
                             name = "N(0)",\
                             element = "N",\
                             molarMass = MolarMass(14.0067,"g/mol"),\
                             alkalinity = 0.0)
speciesAddenda.append(N0AMS)
KAMS = AqueousMasterSpecies(symbol = "K+",\
                            name = "K",\
                            element = "K",\
                            molarMass = MolarMass(39.102,"g/mol"),\
                            alkalinity = 0.0)
speciesAddenda.append(KAMS)
ClSSp = AqueousSecondarySpecies(symbol = "Cl-",\
                                formationReaction = [\
                                                     ("Cl-",1)],\
                                logK25 = 0.0,\
                                name = "Cl")
speciesAddenda.append(ClSSp)
NaSSp = AqueousSecondarySpecies(symbol = "Na+",\
                                formationReaction = [\
                                                     ("Na+",1)],\
                                logK25 = 0.0,\
                                name = "Na")
speciesAddenda.append(NaSSp)
CaSSp = AqueousSecondarySpecies(symbol = "Ca++",\
                                formationReaction = [\
                                                     ("Ca++",1)],\
                                logK25 = 0.0,\
                                name = "Ca")
speciesAddenda.append(CaSSp)
NSSp = AqueousSecondarySpecies(symbol = "NO3-",\
                               formationReaction = [\
                                                    ("NO3-",1)],\
                               logK25 = 0.0,\
                               name = "N")
speciesAddenda.append(NSSp)
NH3SSp = AqueousSecondarySpecies(symbol = "NH3",\
                                 formationReaction = [\
                                                      ("NH4+",1),("H+",-1)],\
                                 logK25 = -9.252,\
                                 name = "NH3")
speciesAddenda.append(NH3SSp)
NH4pSSp = AqueousSecondarySpecies(symbol = "NH4+",\
                                  formationReaction = [\
                                                       ("NO3-",1),("H+",10),("e-",8),("H2O",-3)],\
                                  logK25 = 119.077,\
                                  name = "NH4+")
speciesAddenda.append(NH4pSSp)
N2SSp = AqueousSecondarySpecies(symbol = "N2",\
                                formationReaction = [\
                                                     ("NO3-",2),("H+",12),("e-",10),("H2O",-6)],\
                                logK25 = 207.08,\
                                name = "N2")
speciesAddenda.append(N2SSp)
KSSp = AqueousSecondarySpecies(symbol = "K+",\
                               formationReaction = [\
                                                    ("K+",1)],\
                               logK25 = 0.0,\
                               name = "K")
speciesAddenda.append(KSSp)
NO2mSSp = AqueousSecondarySpecies(symbol = "NO2-",\
                                  formationReaction = [\
                                                       ("NO3-",1),("H+",2),("e-",2),("H2O",-1)],\
                                  logK25 = 28.57,\
                                  name = "NO2-")
speciesAddenda.append(NO2mSSp)
X = SorbingSiteMasterSpecies(symbol = "X-",name   = "X")
speciesAddenda.append(X)
XESp = SorbedSecondarySpecies(symbol = "X-",\
                              formationReaction = [("X-",1)],\
                              logK25 = 0.0,\
                              name = "X",)
speciesAddenda.append(XESp)
NaXESp = SorbedSecondarySpecies(symbol = "NaX",\
                                formationReaction = [("Na+",1),("X-",1)],\
                                logK25 = 0.0,\
                                name = "NaX",)
speciesAddenda.append(NaXESp)
KXESp = SorbedSecondarySpecies(symbol = "KX",\
                               formationReaction = [("K+",1),("X-",1)],\
                               logK25 = 0.7,\
                               name = "KX",)
speciesAddenda.append(KXESp)
CaX2ESp = SorbedSecondarySpecies(symbol = "CaX2",\
                                 formationReaction = [("Ca++",1),("2X-",1)],\
                                 logK25 = 0.8,\
                                 name = "CaX2",)
speciesAddenda.append(CaX2ESp)
#~~~~~~~~~~~~~~~~~~
# Chemical States ~
#~~~~~~~~~~~~~~~~~~
ChemicalStateList = []
boundaryAqueousSolution = AqueousSolution (elementConcentrations = [ElementConcentration ("Ca",6.e-4,"mol/l"),
                                                                    ElementConcentration ("Cl",1.2e-3,"mol/l")
                                                                   ],\
                                           pH = 7,\
                                           pe = 12.5)
boundaryChemicalState = ChemicalState ("boundary",boundaryAqueousSolution)

columnIonicExchangers = IonicExchangers([ExchangeBindingSpecies("X", MolesAmount(1.1e-3, "mol"))])
columnAqueousSolution = AqueousSolution (elementConcentrations = [ElementConcentration ("K",2.e-4,"mol/l"),
                                                                  ElementConcentration ("Na",1.e-3,"mol/l"),
                                                                  ElementConcentration ("N(5)",1.2e-3,"mol/l")
                                                                 ],\
                                         pH = 7.0,\
                                         pe = 12.5)
columnChemicalState = ChemicalState ("column",columnAqueousSolution ,ionicExchanger = columnIonicExchangers)

totoAqueousSolution = AqueousSolution (elementConcentrations = [ElementConcentration ("Na",1.e-2,"mol/l")
                                                               ],\
                                       pH = 7.0,\
                                       pe = 4)
totoChemicalState = ChemicalState ("toto",totoAqueousSolution)

#~~~~~~~~~~~~~~~~~~~~
# Initial condition ~
#~~~~~~~~~~~~~~~~~~~~
columnIC = InitialCondition (body  = column0Body, value = columnChemicalState)
#~~~~~~~~~~~~~~~~~~~~~
# Boundary condition ~
#~~~~~~~~~~~~~~~~~~~~~
boundaryBC = BoundaryCondition (boundary = boundary1Body, btype="Dirichlet", value = boundaryChemicalState)
#~~~~~~~~~~~~~~~~~~~
# Expected outputs ~
#~~~~~~~~~~~~~~~~~~~
finalTime = 3600.
expectedOutputs = [ExpectedOutput("Concentration","K",format = "table",name = "K_output",timeSpecification=TimeSpecification(times=[finalTime]))]
#~~~~~~~~~
# Module ~
#~~~~~~~~~
module = ChemicalTransportModule()
problem  = ChemicalTransportProblem(name               = "guitest",\
                                    regions            = [column0Region,boundary1Region],\
                                    initialConditions  = [columnIC],\
                                    boundaryConditions = [boundaryBC],\
                                    calculationTimes   = [0.0,finalTime],\
                                    sources            = None,\
                                    darcyVelocity      = Velocity(Vector([0.002/720.0, 0.0, 0.0])),\
                                    chemistryDB        = "water_gui_cv.dat",\
                                    speciesBaseAddenda = speciesAddenda,\
                                    kineticLaws        = None,\
                                    activityLaw        = None,\
                                    outputs            = expectedOutputs)
module.setData (problem, trace = 0, mesh = mesh, algorithm="CC")
intimestep = 1.e-1
module.setComponent("mt3d","phreeqc")
module.setTransportParameters("T.V.D.")
module.setTransportParameters("Jacobi",1e-20)
module.setCouplingParameter(initialTimeStep        = intimestep,
                            minTimeStep            = intimestep,
                            maxTimeStep            = 5.,
                            couplingPrecision      = 8.e-04,
                            optimalIterationNumber = 20,
                            maxIterationNumber     = 30,
                            decreaTimeStepCoef     = 0.75,
                            increaTimeStepCoef     = 1.025)
module.run()
#~~~~~~~~~~~~~~~~~~
# Post processing ~
#~~~~~~~~~~~~~~~~~~
#
#       Comparison to reference solution issued from phreeqC
#
refSolution = [\
6.8114e-05,\
1.6401e-04,\
3.1388e-04,\
4.8294e-04,\
3.1468e-04,\
2.3243e-04,\
2.0708e-04, 2.0124e-04, 2.0018e-04, 2.0002e-04, 2.0000e-04, 2.0000e-04, 2.0000e-04, 2.0000e-04, 2.0000e-04, 2.0000e-04,
2.0000e-04, 2.0000e-04, 2.0000e-04, 2.0000e-04, 2.0000e-04, 2.0000e-04, 2.0000e-04, 2.0000e-04, 2.0000e-04, 2.0000e-04,
2.0000e-04, 2.0000e-04, 2.0000e-04, 2.0000e-04, 2.0000e-04, 2.0000e-04, 2.0000e-04, 2.0000e-04, 2.0000e-04, 2.0000e-04,
2.0000e-04, 2.0000e-04, 2.0000e-04, 2.0004e-0]

K_num     = module.getOutput('K_output')
print "K =",K_num[-1][-1].getColumn(2)[0:]
errorNorm = normMaxListComparison(K_num[-1][1].getColumn(2)[1:30],refSolution[1:30])
#
# The front is sharp, so the error control (0.05) is relatively large
#
print 'error norm = ',errorNorm
if errorNorm < 0.15 :
    print "~~~~~~~~~~~~~~~\nThe results are stable\n~~~~~~~~~~~~~~~\n"
else:
    raise Exception, "~~~~~~~~~~~~~~~\nThe results have significantely changed, check the case\n~~~~~~~~~~~~~~~\n"
#print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
#print "        End of the guitest case ~"
#print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

module.end()
