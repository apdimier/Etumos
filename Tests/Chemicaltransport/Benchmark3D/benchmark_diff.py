#
# We have four states:
#                       One global state called domain, to describe the initial state and the two inlets. 
#                       One state to describe the mineral barriers
#                       One state to describe the CO2 bubble.
#                       One state to describe the inlet water.
#
#                       Two cases are treated, one using diffusion, the other one using a velocity field.
#
from constant import epspH
import os                  # for file path
from mesh import *         # for Meshes treatment 
from datamodel import *  
import sys
from chemicaltransportmodule import *
from listtools import normMaxListComparison, subtractLists

setProblemType("ChemicalTransport")
#~~~~~~~~~~~~~~~~~~
#   Mesh definition
#~~~~~~~~~~~~~~~~~~
dico = { 'MethodChoice' : 'FE'}

meshFileName = "benchmark.msh"
mesh = Mesh3D(meshFileName)
numberOfVertices = mesh._getNumberOfVertices()
print " within script numberOfVertices",numberOfVertices
print mesh.getPhysicalBodyNames()

co2Body         = mesh.getBody('co2'); co2Body.getNodesNumber()
print "co2     ",co2Body.getSpaceDimension(),co2Body.getBodyDimension()
inlet2Body         = mesh.getBody('inlet2'); co2Body.getNodesNumber()

waterBody      = mesh.getBody('water'); waterBody.getNodesNumber()

rockBody        = mesh.getBody('rock'); rockBody.getNodesNumber()

inlet1Body  = mesh.getBody('inlet1'); print " inlet1 ",inlet1Body.getNodesNumber()
inlet2Body  = mesh.getBody('inlet2'); print " inlet2 ",inlet2Body.getNodesNumber()
#outletBody  = mesh.getBody('outlet'); outletBody.getNodesNumber()
#symmetryBody    = mesh.getBody('symmetry'); symmetryBody.getNodesNumber()
print " inlet1 ",inlet1Body.getNodesNumber(),inlet1Body.getSpaceDimension(),
print " inlet2 ",inlet2Body.getNodesNumber(),inlet2Body.getSpaceDimension()
#raw_input("scriptdbg space dimension")

#
##
## Definition of aqueous states
#
mediumPorosity  = 1.0
rockPorosity    = 0.2
albiteProp      = 0.1
calciteProp     = 0.20*(1.-rockPorosity)
dawsoniteProp   = 0.003
kaoliniteProp   = 0.03
quartzProp      = 0.80*(1.-rockPorosity)
totalVol = calciteProp + quartzProp
if abs( 1. - (totalVol+rockPorosity) )< 1.e-5: 
    print " the volume propotions are ok"
else:
    raise "check the volume proportions "    
#
speciesAddenda = []
albiteVQuantity         = albiteProp    *(1. - rockPorosity)*1./rockPorosity # in terms of volume in contact with one liter of water
calciteVQuantity        = calciteProp   * (1. - rockPorosity)*1./rockPorosity # in terms of volume in contact with one liter of water
dawsoniteVQuantity      = dawsoniteProp *(1. - rockPorosity)*1./rockPorosity # in terms of volume in contact with one liter of water
kaoliniteVQuantity      = kaoliniteProp *(1. - rockPorosity)*1./rockPorosity # in terms of volume in contact with one liter of water
quartzVQuantity         = quartzProp    * (1. - rockPorosity)*1./rockPorosity # in terms of volume in contact with one liter of water
#
Ca      = 40.078
C       = 12.0111
Mg      = 24.312
Al      = 26.9815
Si      = 28.0843
O2      = 31.988
K       = 39.098
#
# the source is thermXu4.dat 
#
# albite is             262.222         g/mol           (NaAlSi3O8 + 8 H2O)
#               and     100.250         cm3/mol
#
# calcite is            100.087         g/mol           (CaCO3)
#               and      36.934         cm3/mol
#
calciteMolWt    = 100.087
calciteMolV     = 36.934
# dawsonite is          143.995         g/mol           (NaAlCO3(OH)2)
#               and      59.300         cm3/mol
#
# kaolinite is          258.159         g/mol           (Al2Si2O5(OH)4)
#               and      99.520         cm3/mol
#
#
# quartz is             60.084          g/mol           (SiO2)
#               and     22.688          cm3/mol
#
# The quantity in contact with one liter of water is calciteVQuantity and 
# in terms of moles it must be divided by cm3/mol*1.e-3 to get mol/l
#
albiteMQuantity         = albiteVQuantity       /       (100.250 * 1.e-3)
#
calciteMQuantity        = calciteVQuantity      /       ( 36.934 * 1.e-3)
#
dawsoniteMQuantity      = dawsoniteVQuantity    /       ( 59.300 * 1.e-3)
#
kaoliniteMQuantity      = kaoliniteVQuantity   /        ( 99.520 * 1.e-3)
#
quartzMQuantity         = quartzVQuantity      /        ( 22.688 * 1.e-3)
#
#
# Definition of the Aqueous chemical State for the medium
#
#
temp = 80
pH = 6.056
pe = 3.38983
mediumAqueousspecieslist = []
#mediumAqueousspecieslist.append (ElementConcentration ('Al',            7.000e-08, "mol/l"))
mediumAqueousspecieslist.append (ElementConcentration ('Ca',            2.320e-02, "mol/l"))
mediumAqueousspecieslist.append (ElementConcentration ('Cl',            0.970e-00, "mol/l"))
#mediumAqueousspecieslist.append (ElementConcentration ('Fe(+2)',        1.720e-07, "mol/l"))
mediumAqueousspecieslist.append (ElementConcentration ('C',             3.460e-03, "mol/l"))
#mediumAqueousspecieslist.append (ElementConcentration ('K',             1.750e-02, "mol/l"))
#mediumAqueousspecieslist.append (ElementConcentration ('Mg',            1.280e-04, "mol/l"))
mediumAqueousspecieslist.append (ElementConcentration ('Na',            0.918e-00, "mol/l"))
mediumAqueousspecieslist.append (ElementConcentration ('Si',            5.710e-04, "mol/l"))

mediumAqueousSolution = AqueousSolution (mediumAqueousspecieslist, pH, pe)
#
#
##
##  ChemicalState Definitions
##
#
Mineralspecies_domain = [ ]

Mineralspecies_barriers = [ MineralConcentration("Calcite",       calciteMQuantity, "mol/l"),
                            MineralConcentration("Quartz",        quartzMQuantity, "mol/l"),
                          ]

MineralPhaseSolution_domain = MineralPhase (Mineralspecies_domain)
MineralPhaseSolution_Infiltration_region = MineralPhase ([])
#
# Fix_H+
#
Fixphreaction = []
Fixphreaction.append (("H+", 1))
log_k = 0.0
Fixph = MineralSecondarySpecies ("H+", Fixphreaction, log_k, "Fix_H+")
speciesAddenda = [Fixph]
#
# End
#
ProblemName = "module"
Phreeqc_file = "module.txt"

medium  = Material (     name = "medium",\
                        effectiveDiffusion = EffectiveDiffusion (1.0E-9),\
                        porosity = Porosity (value = mediumPorosity),\
                        kinematicDispersion = KinematicDispersion (1.5, 1.5)
                  )

co2Medium = Material (  name = "co2",\
                        effectiveDiffusion = EffectiveDiffusion (1.0E-9),\
                        porosity = Porosity (value = mediumPorosity),\
                        kinematicDispersion = KinematicDispersion (1.5, 1.5)
                  )

rock = Material (       name = "rock",\
                        effectiveDiffusion = EffectiveDiffusion (1.0E-9),\
                        porosity = Porosity (value = rockPorosity),\
                        kinematicDispersion = KinematicDispersion (1.5, 1.5)
                )
#
# domain
#
domainRegion = Region   ( support = waterBody,
                          material = medium
                        )

mediumMineralPhaseSolution = []
#
gasPhaseMedium = []
gasPhaseMedium.append (Fugacity ("CO2(g)",      -3.52)       )
mediumWaterGasPhase = GasPhase (gasPhaseMedium)
mediumState = ChemicalState ("medium",\
                             mediumAqueousSolution,\
                             mediumMineralPhaseSolution,\
                             mediumWaterGasPhase,\
                             )
#                                    
mediumIC = InitialCondition (body = waterBody, value = mediumState)
#
# symmetry
#
#symmetryRegion = Region (support = symmetryBody, material = medium)
#regionsList.append(symmetryRegion)
#                                    
#symmetryIC = InitialCondition (body = symmetryBody, value = mediumState)
#initialConditionsList.append (symmetryIC)
#
# CO2
#
#
co2Aqueousspecieslist = []
co2Aqueousspecieslist.append (ElementConcentration ('C',        1.0e-10, "mol/l"))
co2Aqueousspecieslist.append (ElementConcentration ('Ca',       1.0e-10, "mol/l"))
co2Aqueousspecieslist.append (ElementConcentration ('Na',       1.0e-0, "mol/l"))
co2Aqueousspecieslist.append (ElementConcentration ('O(0)',     1.0e-25, "mol/l"))


gasPhaseCO2Water = []
co2 = Fugacity ("CO2(g)",   2.7)
#
# the setAmount is not necessary
#
co2.setAmount(9.9)
gasPhaseCO2Water.append (co2)
co2WaterGasPhase = GasPhase (gasPhaseCO2Water)
co2AqueousSolution = AqueousSolution (co2Aqueousspecieslist, pH, pe)
co2MineralPhaseSolution = MineralPhase([])
co2State = ChemicalState ("co2",\
                          co2AqueousSolution,\
                          co2MineralPhaseSolution,\
                          co2WaterGasPhase,\
                          chargeBalance = ("Cl", 1.e-0)
                         )
co2Region = Region (support = co2Body, material = co2Medium)

co2IC = InitialCondition (body = co2Body, value = co2State)
#
# outlet
#
#outletRegion = Region (support = outletBody, material = medium)
#regionsList.append(outletRegion)
                                    
#outletIC = InitialCondition (body = outletBody, value = mediumState)
#initialConditionsList.append (outletIC)
#
# Rock
#
# calcite under kinetics
#
calciteReaction = [("Ca+2", 1.0),("HCO3-", 1.0),("H+", -1.0)]
log_k = 1.8487
#log_k = -3.8827287
calciteMolWt    = 0.100087      # kg/mol
calciteMolV     = 36.934e-6     # m3/mol

Calcite = MineralSecondarySpecies ("CaCO3",\
                                   calciteReaction,\
                                   log_k, "KCalcite",Density( calciteMolWt/ calciteMolV,'kg/m**3'))
speciesAddenda.append (Calcite)

kineticLaws = [
                ReversibleKineticLaw ("KCalcite",\
                                     rate = ReactionRate(1.6e-9,"mol/m**2/s"),\
                                     SRExponent = 1.0,\
                                     sphereModelExponent = 1.0,\
				     specificSurfaceArea = 10.),
                ReversibleKineticLaw ("KQuartz",\
                                     rate = ReactionRate(1.6e-9,"mol/m**2/s"),\
                                     SRExponent = 1.0,\
                                     sphereModelExponent = 1.0,\
				     specificSurfaceArea = 10.),
	       ]

temp = 25
pH = 7.0
pe = 3.38983
aqueousSpeciesList = []
aqueousSpeciesList.append (ElementConcentration ('Ca',  30.30e-3,       "mol/l"))
#aqueousSpeciesList.append (ElementConcentration ('Mg',  1.070e-4,       "mol/l"))
aqueousSpeciesList.append (ElementConcentration ('Na',  0.946e+0,       "mol/l"))
#aqueousSpeciesList.append (ElementConcentration ('K',   17.50e-3,       "mol/l"))
aqueousSpeciesList.append (ElementConcentration ('Fe',  4.07e-8,        "mol/l"))
#aqueousSpeciesList.append (ElementConcentration ('Cl', 0.968e+0, "mol/l"))
#aqueousSpeciesList.append (ElementConcentration ('Al',  1.770e-8,       "mol/l"))

rockAqueousSolution = AqueousSolution (aqueousSpeciesList, pH, pe)
                  
rockRegion = Region (support = rockBody, material = medium)

#rockState = ChemicalState ("rock",
#                           RockAqueousSolution,
#                           rockMineralPhase,
#                           phFixed = ("HCl", 10),
#                           chargeBalance = ("Cl", 1.e-3))
rockMineralPhase = MineralPhase ([MineralConcentration("Quartz",   quartzMQuantity,  "mol/l", saturationIndex = 0.0),
                                  MineralConcentration("KCalcite",  calciteMQuantity, "mol/l", saturationIndex = 0.0)],
                                )
rockState = ChemicalState ("rock",
                           mediumAqueousSolution,
                           rockMineralPhase,)
#                           chargeBalance = ("Cl", 1.e-3))
rockIC = InitialCondition (body = rockBody, value = rockState)
#
#
#
bCList = []
#
# Definition of the Aqueous chemical State for fresh water
#
#
temp = 25
pH = 7.0
pe = 0.
inletWaterSpecies = []

inletWaterSpecies.append (ElementConcentration ('C' ,   1.0e-10,        "mol/l"))
inletWaterSpecies.append (ElementConcentration ('Ca',   1.0e-10,        "mol/l"))
inletWaterSpecies.append (ElementConcentration ('O(0)', 1.0e-25,        "mol/l"))
inletWaterSpecies.append (ElementConcentration ('Cl',   0.970e-00,      "mol/l"))

inletWaterAqueousSolution = AqueousSolution (inletWaterSpecies, pH, pe)
gasPhaseInletWater = []
gasPhaseInletWater.append (Fugacity ("CO2(g)",   -3.52)       )
gasPhaseInletWater.append (Fugacity ("O2(g)",     -0.69897)   )
#H2O_gas = Fugacity ("H2O(g)",-1.509994)
#gasPhaseInletWater.append (H2O_gas)
inletWaterGasPhase = GasPhase (gasPhaseInletWater)
inletWaterMineralPhase = []
inletState = ChemicalState ("inlet",\
                           inletWaterAqueousSolution,\
			   inletWaterMineralPhase,\
			   inletWaterGasPhase,\
			   chargeBalance = ("Na", 1.e+00))
bCInlet1 = BoundaryCondition (boundary = inlet1Body, btype = 'Dirichlet', value = inletState)
bCList.append (bCInlet1)
bCInlet2 = BoundaryCondition (boundary = inlet2Body, btype = 'Dirichlet', value = inletState)
bCList.append (bCInlet2)
#
#
#
finalTime = 3.155760e+7*201
Times=[0.,finalTime]
#                    ExpectedOutput(quantity='Concentration',unknow='Cl',
#                                   name='Cl',
#                                   unit = 'molal',
#                                   format='table',
#                                   timeSpecification=TimeSpecification(times=[t1,t2,t3,t4])),

outputslist = []
#outputslist.append (ExpectedOutput('Concentration','U',format='table',name='U_table',timeSpecification=TimeSpecification(times=[3.155760e+7])))
#outputslist.append (ExpectedOutput('Concentration','Quartz',format='table',name='Calcite',timeSpecification=TimeSpecification(times=[3.155760e+6])))
#outputslist = []
#outputs.append(ExpectedOutput('Concentration','Na',format='table',name="Na_table",timeSpecification=TimeSpecification(times=[temps_final])))
Rtransport=ChemicalTransportProblem( name                = "module",\
			             regions             = [rockRegion, co2Region, domainRegion],\
			             boundaryConditions  = bCList,\
			             initialConditions   = [rockIC, co2IC, mediumIC],\
			             calculationTimes    = Times,\
				     sources             = None,\
				     darcyVelocity       = None,\
#				    darcyVelocity = Velocity(Vector([0.0, 0.0, 0.0])),\
			             chemistryDB         = "llnl.dat",\
			             speciesBaseAddenda  = speciesAddenda,\
			             kineticLaws         = kineticLaws,\
			             activityLaw         = None,\
			             outputs             = outputslist
			            )
#
# Creation of the link between transport and chemistry
#
#InitialTimeStep = 252460.8*7
MinTimeStep = 252460.8/1000
MaxTimeStep = 86400*10
InitialTimeStep = MinTimeStep
CoefIncreaTimeStep = 1.05
CoefDecreaTimeStep = 0.8
MaxCouplingStep = 20
ObjectiveCouplingStep = 10
CouplingPrecision = 1e-6

print "chemicaltransport module "
module = ChemicalTransportModule()
module.setData (Rtransport, trace = 0, mesh = mesh, algorithm="NI")
module.setComponent('Elmer','Phreeqc')
module.setCouplingParameter(initialTimeStep       = InitialTimeStep,
                           maxTimeStep            = MaxTimeStep,
                           minTimeStep            = MinTimeStep,
                           increaTimeStepCoef     = CoefIncreaTimeStep,
                           decreaTimeStepCoef     = CoefDecreaTimeStep,
                           maxIterationNumber     = MaxCouplingStep,
                           optimalIterationNumber = ObjectiveCouplingStep,
                           couplingPrecision      = CouplingPrecision)
module.setVtkOutputsParameters(["Quartz","KCalcite","C"], "s", 86400*10)

module.transport.setTransportParameter(convSolver               = 1.e-8,\
				       iterSolver               = 400,\
				       indMemory                = 0,\
                                       discretisation           = dico['MethodChoice'],\
				       algebraicResolution      = 'Iterative',\
				       timeSteppingMethod       = "BDF",
# possible values are CG CGS BiCGStab TFQMR GMRES
				       preconditioner           = 'ILU2',accelerator = "GMRES")

list_of_species_toplot = []
pointtoplot = 0

outputsin = []

module.run()
#
#print module.getOutput('UO2_table')
#res_u     = module.getOutput('U_table')
#for i in res_u:
#    print type(i)
#    print type(i[1])
#    print " toto ",i[1].title
print "dbg  getoutput "
#
