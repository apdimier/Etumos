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
Phreeqc_file = "title.txt"      # bounded to Phreeqc
ProblemName  = "title"          # Phreeqc file 
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
boundary0Zone = CartesianMesh2D("boundary", "XY")
boundary0Zone.setZone("boundary",index_min = Index2D (1,1), index_max = Index2D (1,1))
column1Zone = CartesianMesh2D("column", "XY")
column1Zone.setZone("column",index_min = Index2D (2,1), index_max = Index2D (101,1))
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
boundary0Region = Region(support=boundary0Zone, material= columnMaterial)
column1Region = Region(support=column1Zone, material= columnMaterial)
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
T = AqueousMasterSpecies(symbol = "T+",\
                         name = "T",\
                         element = "T",\
                         molarMass = MolarMass(1.008,"kg/mol"),\
                         alkalinity = 0.0)
speciesAddenda.append(T)
CsSSp = AqueousSecondarySpecies(symbol = "Cs+",\
                                formationReaction = [("Cs+",1)],\
                                logK25 = 0.0,\
                                name = "Cs")
speciesAddenda.append(CsSSp)
TSSp = AqueousSecondarySpecies(symbol = "T+",\
                               formationReaction = [("T+",1)],\
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
columnMineralPhase = MineralPhase([])
columnIonicExchangers = IonicExchangers([ExchangeBindingSpecies("NaZ", MolesAmount(0.0018, "mol"))])
columnAqueousSolution = AqueousSolution (elementConcentrations = [ElementConcentration ("Na",1.e-2,"mol/l")
                                                                 ],\
                                         pH = 7.0,\
                                         pe = 4)
columnChemicalState = ChemicalState ("column",columnAqueousSolution,columnMineralPhase)

boundaryMineralPhase = MineralPhase([])
boundaryIonicExchangers = IonicExchangers([ExchangeBindingSpecies("NaZ", MolesAmount(0.0, "mol"))])
boundaryAqueousSolution = AqueousSolution (elementConcentrations = [ElementConcentration ("Cs",1.e-6,"mol/l"),
                                                                    ElementConcentration ("Na",1.e-2,"mol/l"),
                                                                    ElementConcentration ("T",1.e-6,"mol/l")
                                                                   ],\
                                           pH = 7.0,\
                                           pe = 4)
boundaryChemicalState = ChemicalState ("boundary",boundaryAqueousSolution,boundaryMineralPhase)

#~~~~~~~~~~~~~~~~~~~~
# Initial condition ~
#~~~~~~~~~~~~~~~~~~~~
columnIC = InitialCondition (zone  = column1Zone, value = columnChemicalState)
#~~~~~~~~~~~~~~~~~~~~~
# Boundary condition ~
#~~~~~~~~~~~~~~~~~~~~~
boundaryBC = BoundaryCondition (boundary = boundary0Zone, btype="Dirichlet", value = boundaryChemicalState)
#~~~~~~~~~~~~~~~~~~~
# Expected outputs ~
#~~~~~~~~~~~~~~~~~~~
expectedOutputs = []
#~~~~~~~~~
# Module ~
#~~~~~~~~~
module = ChemicalTransportModule()
problem  = ChemicalTransportProblem(name               = "title",\
                                    regions            = [boundary0Region,column1Region],\
                                    initialConditions  = [columnIC],\
                                    boundaryConditions = [boundaryBC],\
                                    calculationTimes   = [0.0,32400.0],\
                                    sources            = None,\
                                    darcyVelocity      = Velocity(Vector([3.5e-7,0.0,0.0])),\
                                    bdd                = "/home/dimier/Wrapper/Phreeqc_dat/phreeqc.dat",\
                                    speciesBaseAddenda = speciesAddenda,\
                                    kineticLaws        = None,\
                                    activityLaw        = None,\
                                    outputs            = expectedOutputs)
module.setData (problem, trace = 0, mesh = mesh, algorithm="NI")

module.setComponent("mt3d","phreeqc")
module.setTransportParameters("T.V.D.")
module.setTransportParameters("Jacobi",1e-15)
module.setCouplingParameter(InitialTimeStep        = 200.0,
                            MaxTimeStep            = 200.0,
                            MinTimeStep            = 200.0,
                            CouplingPrecision      = 1e-05,
                            MaxCouplingStep        = 30,
                            ObjectiveCouplingStep  = 20,
                            CoefIncreaTimeStep     = 1.05,
                            CoefDecreaTimeStep     = 0.5)
module.run()

print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "        End of the title case ~"
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
