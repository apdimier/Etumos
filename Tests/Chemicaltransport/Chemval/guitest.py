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
nx  = 41
ny  = 1
#~~~~~~~~~~~~~~~~~~
#~ Mesh extension ~
#~~~~~~~~~~~~~~~~~~
deltax = []
dx = [0.125/1]*1
deltax.extend(dx)
dx = [10.0/40]*40
deltax.extend(dx)
deltay = []
dy = [1.0/1]*1
deltay.extend(dy)
mesh.setdAxis("X",deltax)
mesh.setdAxis("Y",deltay)
boundary0Zone = CartesianMesh2D("boundary", "XY")
boundary0Zone.setZone("boundary",index_min = Index2D (1,1), index_max = Index2D (1,1))
concrete1Zone = CartesianMesh2D("concrete", "XY")
concrete1Zone.setZone("concrete",index_min = Index2D (2,1), index_max = Index2D (38,1))
concreteb2Zone = CartesianMesh2D("concreteb", "XY")
concreteb2Zone.setZone("concreteb",index_min = Index2D (39,1), index_max = Index2D (41,1))
#~~~~~~~~~~~~~
#~ Materials ~
#~~~~~~~~~~~~~
concretebMaterial = Material (name = "concreteb",effectiveDiffusion = EffectiveDiffusion (3.0e-10,unit="m**2/s"),\
permeability = Permeability(value = 1.0),\
porosity = Porosity(value = 1.0),\
kinematicDispersion = KinematicDispersion (0.0,0))
concreteMaterial = Material (name = "concrete",effectiveDiffusion = EffectiveDiffusion (3.0e-10,unit="m**2/s"),\
permeability = Permeability(value = 1.0),\
porosity = Porosity(value = 1.0),\
kinematicDispersion = KinematicDispersion (1.0,0))

#~~~~~~~~~~~
#~ Regions ~
#~~~~~~~~~~~
boundary0Region = Region(support=boundary0Zone, material= concretebMaterial)
concrete1Region = Region(support=concrete1Zone, material= concreteMaterial)
concreteb2Region = Region(support=concreteb2Zone, material= concretebMaterial)
#~~~~~~~~~~~~~~~~~~~
# Chemical Addenda ~
#~~~~~~~~~~~~~~~~~~~
speciesAddenda = []
NaAMS = AqueousMasterSpecies(symbol = "Na+",\
                             name = "Na",\
                             element = "Na",\
                             molarMass = MolarMass(22.9898,"g/mol"),\
                             alkalinity = 0.0)
speciesAddenda.append(NaAMS)
CAMS = AqueousMasterSpecies(symbol = "CO3-2",\
                            name = "C",\
                            element = "HCO3",\
                            molarMass = MolarMass(12.0111,"g/mol"),\
                            alkalinity = 2.0)
speciesAddenda.append(CAMS)
TrAMS = AqueousMasterSpecies(symbol = "Tr",\
                             name = "Tr",\
                             element = "Tr",\
                             molarMass = MolarMass(1.008,"g/mol"),\
                             alkalinity = 0.0)
speciesAddenda.append(TrAMS)
CaAMS = AqueousMasterSpecies(symbol = "Ca++",\
                             name = "Ca",\
                             element = "Ca",\
                             molarMass = MolarMass(40.08,"g/mol"),\
                             alkalinity = 0.0)
speciesAddenda.append(CaAMS)
ClAMS = AqueousMasterSpecies(symbol = "Cl-",\
                             name = "Cl",\
                             element = "Cl",\
                             molarMass = MolarMass(35.453,"g/mol"),\
                             alkalinity = 0.0)
speciesAddenda.append(ClAMS)
NaHCO3SSp = AqueousSecondarySpecies(symbol = "NaHCO3",\
                                    formationReaction = [\
                                                         ("Na+",1),("CO3-2",1),("H+",1)],\
                                    logK25 = 10.079,\
                                    name = "NaHCO3")
speciesAddenda.append(NaHCO3SSp)
CSSp = AqueousSecondarySpecies(symbol = "CO3-2",\
                               formationReaction = [\
                                                    ("CO3-2",1)],\
                               logK25 = 0.0,\
                               name = "C")
speciesAddenda.append(CSSp)
CO2SSp = AqueousSecondarySpecies(symbol = "CO2",\
                                 formationReaction = [\
                                                      ("CO3-2",1),("H+",2),("H2O",-1)],\
                                 logK25 = 16.6807,\
                                 name = "CO2")
speciesAddenda.append(CO2SSp)
NaCO3minSSp = AqueousSecondarySpecies(symbol = "NaCO3-",\
                                      formationReaction = [\
                                                           ("Na+",1),("CO3--",1)],\
                                      logK25 = 1.27,\
                                      name = "NaCO3min")
speciesAddenda.append(NaCO3minSSp)
NaOHSSp = AqueousSecondarySpecies(symbol = "NaOH",\
                                  formationReaction = [\
                                                       ("Na+",1),("H2O",1),("H+",-1)],\
                                  logK25 = -14.18,\
                                  name = "NaOH")
speciesAddenda.append(NaOHSSp)
ClSSp = AqueousSecondarySpecies(symbol = "Cl-",\
                                formationReaction = [\
                                                     ("Cl-",1)],\
                                logK25 = 0.0,\
                                name = "Cl")
speciesAddenda.append(ClSSp)
HCO3minSSp = AqueousSecondarySpecies(symbol = "HCO3-",\
                                     formationReaction = [\
                                                          ("CO3-2",1),("H+",1)],\
                                     logK25 = 10.3289,\
                                     name = "HCO3min")
speciesAddenda.append(HCO3minSSp)
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
CaHCO3SSp = AqueousSecondarySpecies(symbol = "CaHCO3+",\
                                    formationReaction = [\
                                                         ("Ca++",1),("CO3--",1),("H+",1)],\
                                    logK25 = 11.4347,\
                                    name = "CaHCO3")
speciesAddenda.append(CaHCO3SSp)
CaCO3SSp = AqueousSecondarySpecies(symbol = "CaCO3",\
                                   formationReaction = [\
                                                        ("Ca++",1),("CO3--",1)],\
                                   logK25 = 3.22528,\
                                   name = "CaCO3")
speciesAddenda.append(CaCO3SSp)
HCO3SSp = AqueousSecondarySpecies(symbol = "CO3-2",\
                                  formationReaction = [\
                                                       ("CO3-2",1)],\
                                  logK25 = 0.0,\
                                  name = "HCO3")
speciesAddenda.append(HCO3SSp)
TrSSp = AqueousSecondarySpecies(symbol = "Tr",\
                                formationReaction = [\
                                                     ("Tr",1)],\
                                logK25 = 0.0,\
                                name = "Tr")
speciesAddenda.append(TrSSp)
CaOHpSSp = AqueousSecondarySpecies(symbol = "CaOH+",\
                                   formationReaction = [\
                                                        ("Ca++",1),("H2O",1),("H+",-1)],\
                                   logK25 = -12.78,\
                                   name = "CaOH+")
speciesAddenda.append(CaOHpSSp)
Fix_HpAd = MineralSecondarySpecies(symbol = "H+",\
                                   formationReaction = [("H+",1)],\
                                   logK25 = 0.0,\
                                   name = "Fix_H+")
speciesAddenda.append(Fix_HpAd)
H2gAd = MineralSecondarySpecies(symbol = "H2",\
                                formationReaction = [("H2",1)],\
                                logK25 = -3.15,\
                                name = "H2(g)")
speciesAddenda.append(H2gAd)
O2gAd = MineralSecondarySpecies(symbol = "O2",\
                                formationReaction = [("O2",1)],\
                                logK25 = -2.96,\
                                name = "O2(g)")
speciesAddenda.append(O2gAd)
H2OgAd = MineralSecondarySpecies(symbol = "H2O",\
                                 formationReaction = [("H2O",1)],\
                                 logK25 = 1.51,\
                                 name = "H2O(g)")
speciesAddenda.append(H2OgAd)
AragoniteAd = MineralSecondarySpecies(symbol = "CaCO3",\
                                      formationReaction = [("Ca+2",1),("CO3-2",1)],\
                                      logK25 = -8.33606,\
                                      name = "Aragonite")
speciesAddenda.append(AragoniteAd)
CO2gAd = MineralSecondarySpecies(symbol = "CO2",\
                                 formationReaction = [("H2O",-1),("CO3--",1),("H+",2)],\
                                 logK25 = -18.1487,\
                                 name = "CO2(g)")
speciesAddenda.append(CO2gAd)
HaliteAd = MineralSecondarySpecies(symbol = "NaCl",\
                                   formationReaction = [("Na+",1),("Cl-",1)],\
                                   logK25 = 1.582,\
                                   name = "Halite")
speciesAddenda.append(HaliteAd)
PortlanditeAd = MineralSecondarySpecies(symbol = "Ca(OH)2",\
                                        formationReaction = [("Ca+2",1),("OH-",2)],\
                                        logK25 = -5.4448,\
                                        name = "Portlandite")
speciesAddenda.append(PortlanditeAd)
CalciteAd = MineralSecondarySpecies(symbol = "CaCO3",\
                                    formationReaction = [("Ca+2",1),("CO3-2",1)],\
                                    logK25 = -8.47983,\
                                    name = "Calcite")
speciesAddenda.append(CalciteAd)
#~~~~~~~~~~~~~~~~~~
# Chemical States ~
#~~~~~~~~~~~~~~~~~~
ChemicalStateList = []
clayMineralPhase = MineralPhase([MineralTotalConcentration("Calcite",2.8954e-3, "mol/l",saturationIndex = 0.0),
                                MineralTotalConcentration("Portlandite",0.0, "mol/l",saturationIndex = 0.0),
                                MineralTotalConcentration("Aragonite",0.0, "mol/l",saturationIndex = 0.0),
                                MineralTotalConcentration("Halite",0.0, "mol/l",saturationIndex = 0.0),
                                MineralTotalConcentration("CO2(g)",1.0, "mol/l",saturationIndex = -2.54),
                                MineralTotalConcentration("H2O(g)",1.0, "mol/l",saturationIndex = -1.4)])
                                
clayAqueousSolution = AqueousSolution (elementConcentrations = [ElementConcentration ("Ca",2.7e-3,"mol/l"),
                                                                ElementConcentration ("Cl",1.e-2,"mol/l"),
                                                                ElementConcentration ("C",4.5e-3,"mol/l"),
                                                                ElementConcentration ("Na",8.e-3,"mol/l"),
                                                                ElementConcentration ("Tr",1.e-2,"mol/l")
                                                               ],\
                                       pH = 7.5,\
                                       pe = 4)
clayChemicalState = ChemicalState ("clay",clayAqueousSolution,mineralPhase = clayMineralPhase,phFixed=("HCl",7.5))

concreteMineralPhase = MineralPhase([MineralTotalConcentration("Portlandite",9.767e-3, "mol/l",saturationIndex = 0.0),
                                    MineralTotalConcentration("Calcite",0.0, "mol/l",saturationIndex = 0.0),
                                    MineralTotalConcentration("Halite",0.0, "mol/l",saturationIndex = 0.0),
                                    MineralTotalConcentration("Aragonite",0.0, "mol/l",saturationIndex = 0.0)])
concreteAqueousSolution = AqueousSolution (elementConcentrations = [ElementConcentration ("Cl",4.e-2,"mol/l"),
                                                                    ElementConcentration ("C",1.e-10,"mol/l"),
                                                                    ElementConcentration ("Na",8.e-3,"mol/l"),
                                                                    ElementConcentration ("O(0)",0.0,"mol/l"),
                                                                  
                                                                   ],\
                                           pH = 12.5,\
                                           pe = 4)
concreteChemicalState = ChemicalState ("concrete",concreteAqueousSolution,mineralPhase = concreteMineralPhase,mineralEquilibrium = [("Ca","Portlandite",2.e-2)])

#~~~~~~~~~~~~~~~~~~~~
# Initial condition ~
#~~~~~~~~~~~~~~~~~~~~
concreteIC = InitialCondition (body  = concrete1Zone, value = concreteChemicalState)
concretebIC = InitialCondition (body  = concreteb2Zone, value = concreteChemicalState)
#~~~~~~~~~~~~~~~~~~~~~
# Boundary condition ~
#~~~~~~~~~~~~~~~~~~~~~
boundaryBC = BoundaryCondition (boundary = boundary0Zone, btype="Dirichlet", value = clayChemicalState)
#~~~~~~~~~~~~~~~~~~~
# Expected outputs ~
#~~~~~~~~~~~~~~~~~~~
unan = 3.15576e+7
temps_final = unan*100.
tf = temps_final
expectedOutputs = []
expectedOutputs = [ExpectedOutput(quantity='pH',
                                   format='table',
                                   timeSpecification=TimeSpecification(times=[tf])),
                    ExpectedOutput('Concentration',unknown='Tr',
                                   format='table',
                                   timeSpecification=TimeSpecification(times=[tf])),
                    ExpectedOutput(quantity='Concentration',unknown='Na',name = 'Na',
                                   format='table',
                                   timeSpecification=TimeSpecification(times=[tf])),
                    ExpectedOutput(quantity='Concentration',unknown='Ca',name = 'Ca',
                                   format='table',
                                   timeSpecification=TimeSpecification(times=[tf])),
                    ExpectedOutput(quantity='Concentration',unknown='Portlandite',name = 'Portlandite',
                                   format='table',
                                   timeSpecification=TimeSpecification(times=[tf])),
                    ExpectedOutput(quantity='Concentration',unknown='Calcite',name='Calcite',
                                   format='table',
                                   timeSpecification=TimeSpecification(times=[tf]))]
#~~~~~~~~~
# Module ~
#~~~~~~~~~
module = ChemicalTransportModule()
problem  = ChemicalTransportProblem(name               = "guitest",\
                                    regions            = [boundary0Region,concrete1Region,concreteb2Region],\
                                    initialConditions  = [concreteIC,concretebIC],\
                                    boundaryConditions = [boundaryBC],\
                                    calculationTimes   = [0.0,3.15576e+9],\
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
module.setCouplingParameter(initialTimeStep        = 1577880.0/2.,
                            maxTimeStep            = 15778800.0,
                            minTimeStep            = 577880.0,
                            couplingPrecision      = 1e-10,
                            optimalIterationNumber = 20,
                            maxIterationNumber     = 30,
                            increaTimeStepCoef     = 1.05,
                            decreaTimeStepCoef     = 0.5)


module.launch()
while (module.simulatedTime < module.times[-1]):
    module.oneTimeStep()
    pass
#~~~~~~~~~~~~~~~~~~
# Post processing ~
#~~~~~~~~~~~~~~~~~~
from posttables import Table
res_pH     = module.getOutput('pH')
print " res_pH",res_pH[-1][-1]
pHdeX      = res_pH[-1][1]
time        = res_pH[-1][0]
print pHdeX
OKpH = None
OKNa = None
print pHdeX.values[2]
pH_w = pHdeX.values[2]
pHref = 11.99854766
if abs(pH_w[1]-pHref)>1.e-3 and abs(time-unan*100)<1.e-7 :
    OKpH = 0
    print 'Be carefull: error on pH differs from previous ones ',pH_w[1],pHref
    
elif abs(time-unan*100)>1.e-7 :
    OKpH = 0
    print "Results to be compared haven\'t been obtained at the same time"
    
else :
    OKpH = 1
    string = 'Stability of results for pH over previous ones',pH_w[1],pHref
    print "="*len(string),"\n",string,"\n","="*len(string),"\n"
#
res_Na     = module.getOutput('Na')
NadeX      = res_Na[-1][1]
time        = res_Na[-1][0]
liste_X   = NadeX.getColumn(0)

koord0 = NadeX.values[0]
print " koord0",koord0
Na_w = NadeX.values[2]
Naref = 8.0124041535e-03


if abs(Na_w[1]-Naref)>2.e-6<1.e-7 :
    OKNa = 0
    print 'Be carefull: error on Na differs from previous ones ',Na_w[1],Naref    
else :
    OKNa = 1
    string = 'Stability of Na ',Na_w[1],Naref
    print "="*len(string),"\n",string,"\n","="*len(string),"\n"
#
if OKpH and OKNa:    
    print "\n******************** Test-Chemval with PHREEQC/MT3D coupling OK********************\n"
    pass
else:
    raise Warning," Problem for the Chemval Test-case 1D with PHREEQC/MT3D coupling"

print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print " End of the chemval test case ~"
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
