#       Transporty and Cation Exchange
#       The following example of advective transport in presence
#       of a cation exchanger is derived from a sample calculation
#       Appelo and Postma 1993 p 431-434.
#       Initially the column contains a sodium-potassium-nitrate solution
#       in equilibrium with the cation exchanger. The column is flushed
#       with a calcium chloride solution.
#
#	Number of moles on exchange sites can induce algorithmic divergence
#       5.5e-4 => convergence jusqu'a t=2e+4
#
from constant import epspH
import os                  # for file path
from mesh import *        # for Meshes treatment 
from datamodel import *
import sys
from chemicaltransportmodule import *
from listtools import normMaxListComparison, subtractLists

dico = { 'MethodChoice' : 'FE'}

import os
Phreeqc_file = "guitest1_e.txt"      # bounded to Phreeqc
ProblemName  = "guitest1_e"          # Phreeqc file 
setProblemType("ChemicalTransport")
#
# meshing
#
meshFileName = "ex11.msh"
mesh = Mesh1D(meshFileName)
numberOfVertices = mesh._getNumberOfVertices()
print numberOfVertices

columnBody    = mesh.getBody('domain')
print columnBody
inletBoundary = mesh.getBody('inlet')
print " script outletBoundary ",inletBoundary.getBodyName()



ChemicalStateList = []
speciesAddenda=[]
#Na = AqueousMasterSpecies("Na+", "Na", element = "Na", molarMass=MolarMass(22.9898e-3,'g/mol'), alkalinity = 0.0)
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
#
# Definition of aqueous states
# It will be modified 
#
#
# Definition of the Aqueous bc chemical State
#
temp = 25
pH = 7.0
pe = 12.5
Aqueousspecieslist_bc = []
Aqueousspecieslist_bc.append(ElementConcentration('Ca'    ,6.0E-04,"mol/l"))
Aqueousspecieslist_bc.append(ElementConcentration('Cl'    ,1.2E-03,"mol/l"))
AqueousSolution_bc = AqueousSolution(Aqueousspecieslist_bc,pH,pe)
#
# Definition of the Aqueous column_clay chemical State
#
temp = 25
pH = 7.0
pe = 1.25E+01
Aqueousspecieslist_argile = []

Aqueousspecieslist_argile.append(ElementConcentration('K',0.2E-3,"mol/l"))
Aqueousspecieslist_argile.append(ElementConcentration('Na',1.0E-3,"mol/l"))
Aqueousspecieslist_argile.append(ElementConcentration('N(5)',1.2E-3,"mol/l"))
AqueousSolution_clay = AqueousSolution(Aqueousspecieslist_argile,pH,pe)

gasPhase_column=[]
#O2gaz = Fugacity("O2(g)",0.3)
#gasPhase_column.append(O2gaz)
gasPhasesolution_column=GasPhase(gasPhase_column)
#gasPhasesolution_column = []
#
##
## Thereafter, we define the sorption site: EXCHANGE_MASTER_SPECIES
##
SorbingSiteList = []
##
## Then, we define the Sorbed Secondary Species: EXCHANGE_SPECIES
##
SorbedSecondarySpecies_column = []
log_k = 0.0

##
## ChemicalState definitions
##
#
# ChemicalState for the boundary
#
clayBCStage = ChemicalState("clayBC",AqueousSolution_bc,charge = True)
ChemicalStateList.append(clayBCStage)
#
# ChemicalState for the entire column
#
# "-------------------------------------------"
# " Definition of the clay chemical state     "
# "-------------------------------------------"
#
listofmineralp_argile = []

Mineralspecies_clay = []
MineralPhaseSolution_clay = MineralPhase(Mineralspecies_clay)

#
IonicExchangerSolution_clay=IonicExchangers([ExchangeBindingSpecies('X',MolesAmount(1.1e-3,'mol'))])
#
# "---------------------------------"
# " clay chemical state definition"
# "---------------------------------"
#
ClayColumnStage = ChemicalState("column",AqueousSolution_clay,MineralPhaseSolution_clay,\
gasPhasesolution_column,\
IonicExchangerSolution_clay,charge = True)
#
ChemicalStateList.append(ClayColumnStage)
#
# "---------------------------------"
# " cement chemical state definition"
# "---------------------------------"
#
Mineralspecies_cement = []
MineralPhaseSolution_cement = MineralPhase(Mineralspecies_cement)
IonicExchangerSolution_cement = []
#
##
## SorbedSecondarySpecies
##
#
ProblemName = "Ex 11 of Phreeqc"
Phreeqc_file = "ex11.txt"
#----------------------------------------------

columnMaterial = Material(name="column",effectiveDiffusion=EffectiveDiffusion(3.e-9),\
                          permeability=Permeability(value=1.0),\
                          porosity=Porosity(value=1.0),\
			  kinematicDispersion=KinematicDispersion(0.0,0.0))
#
columnRegion = Region (support = columnBody, material = columnMaterial)

inletRegion  = Region (support = inletBoundary, material = columnMaterial)
#
# Definition of regions
#
print "-"*25
print " Definition of regions :"
print "-"*25
regions_list = []

#print "  ---- type ----", hasattr(reg1,"material")
#print "  ---- type ----", hasattr(reg1,"support")
#temp = reg1.__class__
#name = temp.__name__
#print " nom ",name
#pos = name.find('_objref_')
#print " pos ",pos
tclasses=[Region]
#for c in tclasses:
#    if isinstance(reg1,c):
#        print " ok ",c
#
# Definition of boundary conditions
#
print "-"*20
print " Definition of boundary conditions :"
print "-"*20
boundaryconditions_list = []
print "-"*10
print " east_bo_m :"
print "-"*10

#boundaryconditions_list.append(bc_west)
inletBC  = BoundaryCondition (boundary = inletBoundary,  btype="Dirichlet", value = clayBCStage)
#
# Definition of initial conditions
#
initialconditions_list = []

columnIC = InitialCondition(columnBody,value=ClayColumnStage)
initialconditions_list.append(columnIC)

print " out of the loop "
interactiveOutputs = [ExpectedOutput("Concentration","Na",format = "table",name = "Na_outputs"),
                      ExpectedOutput("Concentration","Cl",format = "table",name = "Cl_outputs")
                     ]
interactiveOutputs = []
finalTime = 3600.
Times=[0.0,finalTime]
expectedOutputs = [ExpectedOutput("Concentration","K",format = "table",name = "K_output",timeSpecification=TimeSpecification(times=[finalTime]))]
problem = ChemicalTransportProblem("Essai",\
			          regions            = [columnRegion],\
			          initialConditions  = [columnIC],\
			          boundaryConditions = [inletBC],\
			          calculationTimes   = Times,\
				  sources = None,\
				  darcyVelocity = Velocity(Vector([0.002/720., 0.0, 0.0])),\
			          chemistryDB = "water_gui_cv.dat",\
			          speciesBaseAddenda=speciesAddenda,\
			          kineticLaws = None,\
			          activityLaw = None,\
			          outputs = expectedOutputs)
#
# Creation of the link between transport and chemistry
#

ex11=ChemicalTransportModule()
ex11.setData(problem,trace=0,mesh = mesh,algorithm = "CC")
ex11.setComponent('Elmer','Phreeqc')
ex11.setCouplingParameter(20.,
                          maxTimeStep = 50.,
                          minTimeStep = 0.01,
                          increaTimeStepCoef = 1.05,
                          decreaTimeStepCoef = 0.5,
                          couplingPrecision = 3.e-3,
                          maxIterationNumber = 30,
                          optimalIterationNumber = 20)

ex11.transport.setTransportParameter(convSolver = 1.e-15,\
				     iterSolver = 1000,\
				     indMemory = 0,\
                                     discretisation = dico['MethodChoice'],\
				     algebraicResolution = 'Iterative',\
				     timeSteppingMethod = "BDF",BDFOrder = "1",\
				     preconditioner='ILU0',accelerator="BiCG")
#				       timeSteppingMethod = "BDF",\
#				       preconditioner='ILU0',accelerator="TFQMR",thetaScheme=0.0)

list_of_species_toplot = ["Ca","Cl","K","Na"]
#pointtoplot = 5
#if list_of_species_toplot !=[]:
#    ex11.setInteractivePlot(" essai ",list_of_species_toplot,pointtoplot,plotfrequency=1)
ex11.setInteractiveSpatialPlot(interactiveOutputs)
ex11.run()
#
#       Comparison to reference solution issued from a previous simulation
#       The comparison between phreeqC and Elmer FE is difficult because of the different schemes used, FD and FE
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
2.0000e-04, 2.0000e-04, 2.0000e-04, 2.0000e-4]

K_num     = ex11.getOutput('K_output')
print K_num
absc = K_num[-1][-1].getColumn(0)[0:]
knum = K_num[-1][-1].getColumn(3)[0:]
print "K =",knum
errorNorm = normMaxListComparison(K_num[-1][1].getColumn(3)[1:11],refSolution[0:10])
#for i in range(0,40):
#    print " %15.10e %15.10e %15.10e "%(absc[i],knum[i],refSolution[i])
#
# The front is sharp, so the error control (0.2) is relatively large
#
print 'error norm = ',errorNorm
if errorNorm < 0.2 :
    print "~~~~~~~~~~~~~~~\nThe results are stable\n~~~~~~~~~~~~~~~\n"
else:
    raise Exception, "~~~~~~~~~~~~~~~\nThe results have significantely changed, check the case\n~~~~~~~~~~~~~~~\n"
ex11.end()

