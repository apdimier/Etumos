from constant import epspH
from datamodel import *
import fields
from listtools import normMaxListComparison, subtractLists
from chemicaltransport import *
from chemicaltransportmodule import *
from mt3d import Mt3d              # mt3d
from cartesianmesh import *        # Cartesian mesh
from phreeqc import *              # phreeqc
# the first step in the algorithm is non iteratif and can be a reason for the
# algorithm to lose accuracy. A variable porous simulation is necessarly made with CC.
#
# The way the boundary condition is considered with mt3d brings difficulties. Weighting
# factors considering the cell with the boundary condition are  minored by taking a cell of length multiplied by 800.
# The length of the domain is a parameter to be considered with attention due to the way b. c. are considered.
#

import sys

import getopt

from datamodel import * 

specificSurfaceArea = 1.6e+2

setProblemType("ChemicalTransport")
#print len(sys.argv)
#short = 0
#if len(sys.argv)==2:
#    option = sys.argv[1]
#    if option =='--short':
#        short = 33

bdd = "phreeqc.dat"
ChemicalStateList = []
speciesAddenda=[]
#

temp = 25.0
pH = 7.0
pe = 4.0
Aqueousspecieslist_column = []

AqueousSolution_column = AqueousSolution ([ElementConcentration ('Si', 1.31e-4, "mol/l")], 7)

gasPhasesolution_column = GasPhase ([])
#
#
temp = 25.0
pH = 7.0
pe = 4.0
Aqueousspecieslist_leftB = []

AqueousSolution_leftB = AqueousSolution ([ElementConcentration ('Si', 2.12e-3, "mol/l")], 7)

gasPhase_leftB = []
gasPhasesolution_leftB = GasPhase (gasPhase_leftB)

gasPhasesolution_leftB = GasPhase (gasPhase_leftB)
#
##
## Thereafter, we define the sorption site: EXCHANGE_MASTER_SPECIES
##
#
SorbingSiteList = []

Mineralspecies_column = []

Mineral_column = MineralTotalConcentration("Mineral", 0.0, "mol/l")
Mineralspecies_column.append (Mineral_column)

MineralPhaseSolution_column = MineralPhase (Mineralspecies_column)

MineralPhaseSolution_leftB = MineralPhase ([])
IonicExchangerSolution_column = IonicExchangers ([])

IonicExchangerSolution_leftB = IonicExchangers ([])


SurfaceComplexationSolution_leftB = SurfaceComplexation ([])

# Mineral
Mineralreaction = []
Mineralreaction.append (("H4SiO4", 1.0))
Mineralreaction.append (("H2O", -2.0))
log_k = -3.872845
#log_k = -3.8827287
Mineral = MineralSecondarySpecies ("SiO2", Mineralreaction, log_k, "Mineral",Density(2648.29,'kg/m**3'))
speciesAddenda.append (Mineral)
# Si
Si = AqueousMasterSpecies("H4SiO4", "Si", element = "SiO2", molarMass=MolarMass(28.0843,"g/mol"), alkalinity = 0.0)
speciesAddenda.append(Si)

Sireaction = []
Sireaction.append (("H4SiO4", 1))
log_k = 0.0
Si = AqueousSecondarySpecies ("H4SiO4", Sireaction, log_k, "Si")
speciesAddenda.append (Si)
# Si
Sireaction = []
Sireaction.append (("H4SiO4", 1))
log_k = 0.0
Si = AqueousSecondarySpecies ("H4SiO4", Sireaction, log_k, "Si")
speciesAddenda.append (Si)
##
##  Treatment of the SurfaceSiteMasterSpecies
##
#
SurfaceComplexation_column = []
SurfaceComplexationSolution_column = SurfaceComplexation (SurfaceComplexation_column)

SurfaceComplexation_leftB = []
SurfaceComplexationSolution_leftB = SurfaceComplexation (SurfaceComplexation_leftB)


ProblemName = "porosityTest"
Phreeqc_file = "porosityTest.txt"
#~~~~~~~~~~~~~~~~~~
#~ Mesh extension ~
#~~~~~~~~~~~~~~~~~~
mesh = CartesianMesh2D("global","XY")
nx = 201
ny = 1
deltax = []
dx = [0.001]*nx
dx[0]=dx[0]*800.
deltax.extend(dx)
deltay = []
dy = [1.0/1]*1
deltay.extend(dy)

mesh.setdAxis("X",deltax)
mesh.setdAxis("Y",deltay)



material = Material (name = "material", effectiveDiffusion = EffectiveDiffusion (0.79e-9),\
                             permeability = Permeability (value = 1.0),\
                             porosity = Porosity (value = 0.79),)

column = CartesianMesh2D("ColumnT", "XY")
column.setZone ("ColumnT", index_min = Index2D (2, 1), index_max = Index2D (nx, 1))

boundary = CartesianMesh2D("boundary", "XY")
boundary.setZone ("boundary", index_min = Index2D (1, 1), index_max = Index2D (1, 1))

regions_list = []
initialconditions_list = []

reg0 = Region (column, material)
regions_list.append (reg0)
kineticLaws = [ReversibleKineticLaw("Mineral",rate=ReactionRate(6.55e-15,"mol/m**2/s"),sphereModelExponent = 0.0,\
				    specificSurfaceArea = specificSurfaceArea,SRExponent = 1.0)]
Column = ChemicalState ("column_region", \
                                  AqueousSolution_column, \
			          MineralPhaseSolution_column, \
				  gasPhasesolution_column, \
				  IonicExchangerSolution_column)
				  
reg0_ic = InitialCondition (column, value = Column)
initialconditions_list.append (reg0_ic)

boundaryconditions_list = []
reg1 = Region (boundary, material)
regions_list.append (reg1)
bc_left = ChemicalState ("bc_left",\
                          AqueousSolution_leftB,\
			  MineralPhaseSolution_leftB,\
			  gasPhasesolution_leftB, \
			  IonicExchangerSolution_leftB, \
			  SurfaceComplexationSolution_leftB)
			  
bc0 = BoundaryCondition (boundary, 'Dirichlet', value = bc_left)
boundaryconditions_list.append (bc0)
un_an = 365.25*24*3600
tfinal= un_an*10

Times=[0., tfinal]
#
outputlist = []
outputlist.append(ExpectedOutput(quantity='Concentration',unknown='Si',format='table',name='Si'))
outputlist.append(ExpectedOutput(quantity='Concentration',unknown='Mineral',format='table',name='Si'))
outputlist.append(ExpectedOutput('porosity',timeSpecification=TimeSpecification(times=[tfinal]),format='table',save='file'))
#				   
Rtransport=ChemicalTransportProblem("test",\
			            regions_list,\
			            boundaryconditions_list,\
			            initialconditions_list,\
			            Times,\
				    sources = None,\
				    darcyVelocity=Velocity(Vector([0.0, 0.0, 0.0])),\
			            chemistryDB = bdd,\
			            speciesBaseAddenda=speciesAddenda,\
			            kineticLaws = kineticLaws,\
			            activityLaw = None,\
				    timeUnit='s',
				    userProcessing = True,
				    userFunctionList = ["effectiveYoungModulus"],
				    porosityState = 'variable', 
			            outputs = outputlist)
#
# Creation of the link between transport and chemistry
#
InitialTimeStep = 3.1558e+05*10

print "chemicaltransport module "
test = ChemicalTransportModule()
test.setData (Rtransport, trace = 0, mesh = mesh, algorithm = "CC")
test.setCouplingParameter(InitialTimeStep,
                           maxTimeStep            = 3.1536e+06,
                           minTimeStep            = 3.1536e+04,
                           optimalIterationNumber = 15,
                           maxIterationNumber     = 30,
                           increaTimeStepCoef     = 1.05,
                           decreaTimeStepCoef     = 0.75,
                           couplingPrecision      = 1.e-6
                          )
test.setTransportParameters("TVD")
test.setTransportParameters("JACOBI", 1.e-25)
list_of_species_toplot = []
pointtoplot = 0
if list_of_species_toplot !=[]:
    test.setInteractivePlot("test",list_of_species_toplot,pointtoplot,plotfrequency=10)
test.setComponent("mt3d","phreeqc")
intParam = {"Mineral": 		{"cvodeOrder": 5, "cvodetol":4.e-7, "cvodeStep":1000 } }
#test.chemical.setKineticParameter(integrationMethod = "rungekutta",\
#                                    intParamDict = None,\
#                                    intOrder = 5,\
#                                    cvodeStep = None,
#                                    cvodeTol = None)

#
# Simulation
#
test.run()
#
effectiveYoungModulus = test.usE
previousEffectiveYoungModulus = [1.0436943432360708e-06, 1.0378803775150806e-06, 1.032145715051025e-06, 1.026443038371557e-06, 1.020814421590689e-06, 1.0152107651586925e-06, 1.009658274134666e-06, 1.0041710184809715e-06, 9.98735799030556e-07, 9.933460069422324e-07]
#previousEffectiveYoungModulus = [1.9151575673985819e-10, 1.8438484993684937e-10, 1.7751043780249623e-10, 1.7086673198657501e-10, 1.6445544059962237e-10, 1.5828989514689877e-10, 1.5232182513198601e-10, 1.4657358054062875e-10, 1.4102192195982855e-10, 1.356688773554728e-10]
#[1.9481265572812479e-09, 1.8737673256049104e-09, 1.8039067622339525e-09, 1.7363927593889167e-09, 1.6712422327984073e-09, 1.608588521815435e-09, 1.5479406983083178e-09, 1.4895254491923164e-09, 1.4331087812704512e-09, 1.3787097254768541e-09]
norm = normMaxListComparison(previousEffectiveYoungModulus,effectiveYoungModulus[0:len(previousEffectiveYoungModulus)])
effectiveYoungModulus[0:len(previousEffectiveYoungModulus)]
print "effectiveYoungModulus ",effectiveYoungModulus[0:len(previousEffectiveYoungModulus)]
#
print " norm ",norm
error = 5.e-5
if norm > error:
    print "Be careful: error, the Young modulus isn\'t stable"
    mess = " Problem for the Young modulus evaluation test"
    raise Warning," Problem for the Young modulus evaluation test"
    pass
else:
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "Good agreement, the result for the evaluation of the effective Young modulus are stable"
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    pass
#
