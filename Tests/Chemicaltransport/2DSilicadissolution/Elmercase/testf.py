from constant import epspH
import os                  # for file path
from mesh import *         # for the mesh treatment 
from datamodel import * 
import sys
from chemicaltransportmodule import *
from listtools import normMaxListComparison, subtractLists

dico = { 'MethodChoice' : 'FE'}

import os
Phreeqc_file = "2Dexample.txt"      # bounded to Phreeqc
ProblemName  = "2Dexample"          # Phreeqc file 
setProblemType("ChemicalTransport")
#~~~~~~~~~~~~~~~~~~
#~ Mesh extension ~
#~~~~~~~~~~~~~~~~~~
meshFileName = "2D.msh"
mesh = Mesh2D(meshFileName)
numberOfVertices = mesh._getNumberOfVertices()
print " within script numberOfVertices",numberOfVertices
#raw_input()

quartzBody      = mesh.getBody('domain')
sodaBody        = mesh.getBody('domain1')
inletBoundary   = mesh.getBody('inlet')
outletBoundary  = mesh.getBody('outlet')
symmetryBoundary= mesh.getBody('symmetry')
#~~~~~~~~~~~~~
#~ Materials ~
#~~~~~~~~~~~~~
quartzMaterial = Material (name = "quartz",\
#                           effectiveDiffusion = EffectiveDiffusion (5.7e-7,unit="m**2/s"),\
                           effectiveDiffusion = EffectiveDiffusion (1.14e-7,unit="m**2/s"),\
#                           permeability = Permeability(value = 1.0),\
                           porosity = Porosity(value = 1.0),\
                           kinematicDispersion = KinematicDispersion (0.2,0.05))
print " within script quartzmaterial"
#~~~~~~~~~~~
#~ Regions ~
#~~~~~~~~~~~
quartzRegion = Region (support = quartzBody, material=quartzMaterial)

sodaRegion   = Region (support = sodaBody, material=quartzMaterial)

#~~~~~~~~~~~~~~~~~~~
# Chemical Addenda ~
#~~~~~~~~~~~~~~~~~~~
speciesAddenda = []
H3SiO4SSp = AqueousSecondarySpecies(symbol = "H3SiO4-",\
                                    formationReaction = [("H+",-1),("H4SiO4",1)],\
                                    logK25 = -9.83,\
                                    name = "H3SiO4")
speciesAddenda.append(H3SiO4SSp)
Na = AqueousMasterSpecies(symbol = "Na+",\
                          name = "Na",\
                          element = "Na",\
                          molarMass = MolarMass(22.9898,"kg/mol"),\
                          alkalinity = 0.0)
speciesAddenda.append(Na)
Si = AqueousMasterSpecies(symbol = "H4SiO4",\
                          name = "Si",\
                          element = "SiO2",\
                          molarMass = MolarMass(28.0843,"kg/mol"),\
                          alkalinity = 0.0)
speciesAddenda.append(Si)
NaSSp = AqueousSecondarySpecies(symbol = "Na+",\
                                formationReaction = [("Na+",1)],\
                                logK25 = 0.0,\
                                name = "Na")
speciesAddenda.append(NaSSp)
SiSSp = AqueousSecondarySpecies(symbol = "H4SiO4",\
                                formationReaction = [("H4SiO4",1)],\
                                logK25 = 0.0,\
                                name = "Si")
speciesAddenda.append(SiSSp)
QuartzAd = MineralSecondarySpecies(symbol = "SiO2",\
                                   formationReaction = [("H4SiO4",1),("H2O",-2)],\
                                   logK25 = -3.6,\
                                   name = "Quartz",\
                                   density = Density(2648.29,"kg/m**3"))
speciesAddenda.append(QuartzAd)
#~~~~~~~~~~~~~~~~~~
# Chemical States ~
#~~~~~~~~~~~~~~~~~~
ChemicalStateList = []
sodaMineralPhase = []
sodaAqueousSolution = AqueousSolution   (elementConcentrations = [ElementConcentration ("Na",2.0e-2,"mol/l")],pH = 12.2545,pe = 4)

sodaChemicalState = ChemicalState       ("soda", sodaAqueousSolution, sodaMineralPhase)
#
columnMineralPhase = MineralPhase       ([MineralTotalConcentration("Quartz",1.0, "mol/l")])

columnAqueousSolution = AqueousSolution (elementConcentrations = [ElementConcentration ("Na",1.e-10,"mol/l")],pH = 7.0,pe = 4)
#
column1ChemicalState = ChemicalState    ("column",      columnAqueousSolution)
columnChemicalState = ChemicalState     ("column",      columnAqueousSolution,  columnMineralPhase)

#~~~~~~~~~~~~~~~~~~~~
# Initial condition ~
#~~~~~~~~~~~~~~~~~~~~
initial_condition_quartz        = InitialCondition (body  = quartzBody, value = columnChemicalState)
initial_condition_soda          = InitialCondition (body  = sodaBody,   value = sodaChemicalState)

#~~~~~~~~~~~~~~~~~~~~~
# Boundary condition ~
#~~~~~~~~~~~~~~~~~~~~~
inletBoundary  =  BoundaryCondition (boundary = inletBoundary, btype='Dirichlet', value = column1ChemicalState)
outletBoundary = BoundaryCondition (boundary = outletBoundary, btype='Dirichlet', value = column1ChemicalState)

# On doit rajouter une condition de symetrie dans le systeme pour traiter correctement le passage volumes finis elements finis
#
symmetryBoundary = BoundaryCondition (boundary = symmetryBoundary, btype="Symmetry", value = columnChemicalState)

#raw_input(" symetry boundary")
#~~~~~~~~~~~~~~~~~~~
# Expected outputs ~
#~~~~~~~~~~~~~~~~~~~
finalTime = 288000
expectedOutputs = [     ExpectedOutput("pH",    format = "table",name = "pH_output",timeSpecification = TimeSpecification(times=[finalTime])),\
                        ExpectedOutput("Concentration","Na",format="table",name="Na_output",timeSpecification=TimeSpecification(times=[finalTime]))]
#raw_input(" expected outputs")

# Module ~
#~~~~~~~~~
module = ChemicalTransportModule()
problem  = ChemicalTransportProblem(name               = "2Dexample",\
                                    regions            = [quartzRegion,sodaRegion],\
                                    initialConditions  = [ initial_condition_soda, initial_condition_quartz],\
                                    boundaryConditions = [inletBoundary, outletBoundary, symmetryBoundary],\
                                    calculationTimes   = [0.0,finalTime],\
                                    sources            = None,\
                                    darcyVelocity      = Velocity(Vector([5.7e-7, 0.0, 0.0])),\
                                    chemistryDB        = "water_gui.dat",\
                                    speciesBaseAddenda = speciesAddenda,\
                                    kineticLaws        = None,\
                                    activityLaw        = None,\
                                    outputs            = expectedOutputs)
#raw_input(" module set data")
module.setData(problem,unstructured=1,mesh=mesh,trace=0,algorithm="NI")
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Define the Component and its solver parameters
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
module.setComponent('Elmer','Phreeqc')
#
module.setCouplingParameter(initialTimeStep          = 2000,
                            minTimeStep              = 1.5e+3,
                            maxTimeStep              = 1.e+4,
                            couplingPrecision        = 1e-06,
                            maxIterationNumber       = 40,
                            optimalIterationNumber   = 20,
                            increaTimeStepCoef       = 1.05,
                            decreaTimeStepCoef       = 0.75)

module.transport.setTransportParameter(convSolver = 1.e-8,
				       iterSolver = 400,
				       indMemory = 0,
                                       discretisation = dico['MethodChoice'],
				       algebraicResolution = 'Iterative',
# possible values are CG CGS BiCGStab TFQMR GMRES
				       preconditioner='ILU0',accelerator="GMRES",thetaScheme=0.0)
module.setVtkOutputsParameters(["Na"],"d",1)

module.run()

print "teste.py out of run module function "
from analytical_pH_62_2D import AnalyticalFunction_pH_62_2D
short = True
mass_soude = 5.E-5
finalTime = 288000.0*2
print '============================================= '
print 'Calcul d erreurs pour le pH '
print '============================================= '

pH_analytic = AnalyticalFunction_pH_62_2D(finalTime,mass_soude)

res_ph     = module.getOutput("pH_output")
res_na     = module.getOutput("Na_output")
ind = 0
OK = 1
erreur=0.
if short:
    epsilon = 0.3
else:
    epsilon = 0.15
    pass
difference='rel'
ind = 0
inderr = 0
maxcont = 0.0
for i in res_ph[-1][1].values[0]:
    a = res_ph[-1][1].values[0][ind]
    b = res_ph[-1][1].values[1][ind]
    numerical_value = res_ph[-1][1].values[3][ind]
    analytical_value = pH_analytic.eval([a,b])
    delt = abs(analytical_value-numerical_value)
    if difference=='rel':
        delt/=analytical_value
	#print "delt ",delt
        erreur=max(erreur,delt)
        pass
            #pass
    if (delt) > epsilon:
        OK = 0
	inderr+=1
        print 'diff trop importante :',ind,a,b,numerical_value,analytical_value,erreur
    ind+=1
print "inderr ",inderr
print " max of error ",erreur,erreur*100
ind = 0
for i in res_ph[-1][1].values[0]:
    a = res_ph[-1][1].values[0][ind]
    b = res_ph[-1][1].values[1][ind]
    numerical_value = res_ph[-1][1].values[3][ind]
    if numerical_value>maxcont:
        maxcont = numerical_value
	imaxcont = a
	jmaxcont = b
    ind+=1
    #print 'numerical value :',a,b,numerical_value
print " maximal concentration ", imaxcont,jmaxcont, maxcont  
print 'maximal error for pH = ', erreur," and % of error is ",erreur*100
OKConc = 1
if (OK):
    print "\n \n -- Test-case Alkaline 2D with ELMER/PHREEQC coupling OK -- \n \n"
    pass
#else:
#    raise Warning(" Problem for the Test-case Alkaline 2D with ELMER/PHREEQC coupling")
    
from analytical_Na_62_2D import AnalyticalFunction2D_Na
Na_analytic = AnalyticalFunction2D_Na(finalTime,mass_soude)
res_na     = module.getOutput("Na_output")

short = True
ind = 0
OK = 1
erreur=0.
if short:
    epsilon = 2.e-3
else:
    epsilon = 1.e-3
    pass
difference='inf'
ind = 0
inderr = 0
maxcont = 0.0
for i in res_na[-1][1].values[0]:
    a = res_na[-1][1].values[0][ind]
    b = res_na[-1][1].values[1][ind]
    numerical_value = res_na[-1][1].values[3][ind]
    analytical_value = Na_analytic.eval([a,b])
    delt = abs(analytical_value-numerical_value)
    erreur=max(erreur,delt)    
    if difference=='rel' and abs(analytical_value)>1.e-15:
        delt/=analytical_value
	#print "delt ",delt
        erreur=max(erreur,delt)
        pass
            #pass
    if (delt) > epsilon:
        OK = 0
	inderr+=1
        print 'diff trop importante :',ind,a,b,numerical_value,analytical_value
    ind+=1
print "inderr ",inderr
ind = 0
for i in res_na[-1][1].values[0]:
    a = res_na[-1][1].values[0][ind]
    b = res_na[-1][1].values[1][ind]
    numerical_value = res_na[-1][1].values[3][ind]
    if numerical_value>maxcont:
        maxcont = numerical_value
	imaxcont = a
	jmaxcont = b
    ind+=1
    #print 'numerical value :',a,b,numerical_value
print " maximal concentration ", imaxcont,jmaxcont, maxcont  
#for i in res_na:
#    print " res_na ",i[-1].title
#OKConc,erreur=comparesMedField2SpaceFunction(res_na[-1][1],Na_analytic,1.e-3,'inf','abs')
#print 'OKConc = ', OKConc
print 'maximal error for Na = ', erreur," and % of error is ",erreur*100
OKConc = 1
if (OK):
    print "\n \n -- ELMER/PHREEQC coupling OK -- \n \n"
    pass
else:
    msg = " Problem for the ELMER/PHREEQC coupling"
    raise msg


print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "        End of the 2Dexample case ~"
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
