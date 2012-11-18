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
Phreeqc_file = "test_geoi.txt"      # bounded to Phreeqc
ProblemName  = "test_geoi"          # Phreeqc file 
mesh = CartesianMesh2D("global","XY")
nx  = 51
ny  = 1
#~~~~~~~~~~~~~~~~~~
#~ Mesh extension ~
#~~~~~~~~~~~~~~~~~~
deltax = []
dx = [0.004/1]*1
deltax.extend(dx)
dx = [0.2/50]*50
deltax.extend(dx)
deltay = []
dy = [1.0/1]*1
deltay.extend(dy)
mesh.setdAxis("X",deltax)
mesh.setdAxis("Y",deltay)
b0Body = CartesianMesh2D("b", "XY")
b0Body.setZone("b",index_min = Index2D (1,1), index_max = Index2D (1,1))
a1Body = CartesianMesh2D("a", "XY")
a1Body.setZone("a",index_min = Index2D (2,1), index_max = Index2D (51,1))
#~~~~~~~~~~~~~
#~ Materials ~
#~~~~~~~~~~~~~
quartzMaterial = Material (name = "quartz",effectiveDiffusion = EffectiveDiffusion (3e-10,unit="m**2/s"),\
permeability = Permeability(value = 1.0),\
porosity = Porosity(value = 1.0),\
kinematicDispersion = KinematicDispersion (0.0,0))

#~~~~~~~~~~~
#~ Regions ~
#~~~~~~~~~~~
b0Region = Region(support=b0Body, material= quartzMaterial)
a1Region = Region(support=a1Body, material= quartzMaterial)
#~~~~~~~~~~~~~~~~~~~
# Chemical Addenda ~
#~~~~~~~~~~~~~~~~~~~
speciesAddenda = []
NaAMS = AqueousMasterSpecies(symbol = "Na+",\
                             name = "Na",\
                             element = "Na",\
                             molarMass = MolarMass(0.02299,"g/mol"),\
                             alkalinity = 0)
speciesAddenda.append(NaAMS)
SiAMS = AqueousMasterSpecies(symbol = "H4SiO4",\
                             name = "Si",\
                             element = "SiO2",\
                             molarMass = MolarMass(0.0280843,"g/mol"),\
                             alkalinity = 0.0)
speciesAddenda.append(SiAMS)
NaSSp = AqueousSecondarySpecies(symbol = "Na+",\
                                formationReaction = [\
                                                     ("Na+",1)],\
                                logK25 = 0.0,\
                                name = "Na")
speciesAddenda.append(NaSSp)
SiSSp = AqueousSecondarySpecies(symbol = "H4SiO4",\
                                formationReaction = [\
                                                     ("H4SiO4",1)],\
                                logK25 = 0.0,\
                                name = "Si")
speciesAddenda.append(SiSSp)
H3SiO4SSp = AqueousSecondarySpecies(symbol = "H3SiO4-",\
                                    formationReaction = [\
                                                         ("H4SiO4",1),("H+",-1)],\
                                    logK25 = -9.83,\
                                    name = "H3SiO4")
speciesAddenda.append(H3SiO4SSp)
QuartzAd = MineralSecondarySpecies(symbol = "SiO2",\
                                   formationReaction = [("H2O",-2),("H4SiO4",1)],\
                                   logK25 = -3.6,\
                                   name = "Quartz",\
                                   density = Density(2648.29,"kg/m**3"))
speciesAddenda.append(QuartzAd)
#~~~~~~~~~~~~~~~~~~
# Chemical States ~
#~~~~~~~~~~~~~~~~~~
ChemicalStateList = []
sodaAqueousSolution = AqueousSolution (elementConcentrations = [ElementConcentration ("Na",2.e-02,"mol/l")
                                                               ],\
                                       pH = 12.2545,\
                                       pe = 4)
sodaChemicalState = ChemicalState ("soda",sodaAqueousSolution)

columnMineralPhase = MineralPhase([MineralTotalConcentration("Quartz",10.0, "mol/l",saturationIndex = 0.0)])
columnAqueousSolution = AqueousSolution (elementConcentrations = [ElementConcentration ("Na",0.0,"mol/l")
                                                                 ],\
                                         pH = 7.0,\
                                         pe = 4)
columnChemicalState = ChemicalState ("column",columnAqueousSolution,mineralPhase = columnMineralPhase)

#~~~~~~~~~~~~~~~~~~~~
# Initial condition ~
#~~~~~~~~~~~~~~~~~~~~
aIC = InitialCondition (body  = a1Body, value = columnChemicalState)
#~~~~~~~~~~~~~~~~~~~~~
# Boundary condition ~
#~~~~~~~~~~~~~~~~~~~~~
bBC = BoundaryCondition (boundary = b0Body, btype="Dirichlet", value = sodaChemicalState)
#~~~~~~~~~~~~~~~~~~~
# Expected outputs ~
#~~~~~~~~~~~~~~~~~~~
expectedOutputs = [ExpectedOutput("Concentration","Na",format="table",name="Na_output"),
ExpectedOutput("pH",format="table",name="pH_output")]
#~~~~~~~~~
# Module ~
#~~~~~~~~~
module = ChemicalTransportModule()
problem  = ChemicalTransportProblem(name               = "test_geoi",\
                                    regions            = [b0Region,a1Region],\
                                    initialConditions  = [aIC],\
                                    boundaryConditions = [bBC],\
                                    calculationTimes   = [0.0,864000.0],\
                                    sources            = None,\
                                    darcyVelocity      = Velocity(Vector([0.0,0.0,0.0])),\
                                    chemistryDB        = "/home/dimier/Wrapper/Phreeqc_dat/water_gui.dat",\
                                    speciesBaseAddenda = speciesAddenda,\
                                    kineticLaws        = None,\
                                    activityLaw        = None,\
                                    outputs            = expectedOutputs)
module.setData (problem, trace = 0, mesh = mesh, algorithm="CC")

module.setComponent("mt3d","phreeqc")
module.setTransportParameters("T.V.D.")
module.setTransportParameters("Jacobi",1e-20)
module.setCouplingParameter(initialTimeStep        = 20000.0,
                            MinTimeStep            = 2.e+2,
                            MaxTimeStep            = 5.e+4,
                            CouplingPrecision      = 1e-08,
                            OptimalIterationNumber = 20,
                            MaxIterationNumber     = 30,
                            CoefDecreaTimeStep     = 0.8,
                            CoefIncreaTimeStep     = 1.1)
module.run()
#~~~~~~~~~~~~~~~~~~
# Post processing ~
#~~~~~~~~~~~~~~~~~~

print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "        End of the test_geoi case ~"
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
