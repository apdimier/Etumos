from constant import epspH
from datamodel import *
import fields
from listtools import normMaxListComparison, subtractLists
from chemicaltransport import *
from chemicaltransportmodule import *
from phreeqc import *              # phreeqc
from mesh import *
#
#
#
import sys

import getopt

from datamodel import * 

specificSurfaceArea = 1.6e+2

setProblemType("ChemicalTransport")
dico = { 'MethodChoice' : 'FE'}
#
#
#
meshFileName = "porosity.msh"
mesh = Mesh2D(meshFileName)
numberOfVertices = mesh._getNumberOfVertices()
print numberOfVertices
#
#nodesList = mesh.getData(meshFileName,dimensions = 2)
#
mineralBody    = mesh.getBody('domain')
print mineralBody
inletBoundary  = mesh.getBody('inlet')
outletBoundary = mesh.getBody('outlet')
#
bdd = "phreeqc.dat"
ChemicalStateList = []
speciesAddenda=[]
#
#
#
temp = 25.0
pH = 7.0
pe = 4.0
aqueousSpeciesListColumn = []

aqueousSolutionColumn = AqueousSolution ([ElementConcentration ('Si', 1.31e-4, "mol/l")], 7)
#
#
#
temp = 25.0
pH = 7.0
pe = 4.0
aqueousSpeciesListLeftB = []

inletAqueousSolution = AqueousSolution ([ElementConcentration ('Si', 2.12e-3, "mol/l")], 7)

#

mineralSpeciesColumn = []

mineralColumn = MineralTotalConcentration("Mineral", 0.0, "mol/l")

mineralSpeciesColumn.append (mineralColumn)

columnMineralPhaseSolution = MineralPhase (mineralSpeciesColumn)

IonicExchangerSolution_column = IonicExchangers ([])

# Mineral
mineralReaction = [("H4SiO4", 1.0),("H2O", -2.0)]
log_k = -3.872845
#log_k = -3.8827287
Mineral = MineralSecondarySpecies ("SiO2", mineralReaction, log_k, "Mineral",Density(2648.29,'kg/m**3'))
speciesAddenda.append (Mineral)
# Si
Si = AqueousMasterSpecies("H4SiO4", "Si", element = "SiO2", molarMass=MolarMass(28.0843,"g/mol"), alkalinity = 0.0)
speciesAddenda.append(Si)

SiReaction = [("H4SiO4", 1)]
log_k = 0.0
Si = AqueousSecondarySpecies ("H4SiO4", SiReaction, log_k, "Si")
speciesAddenda.append (Si)
#
##  Treatment of the SurfaceSiteMasterSpecies
#
SurfaceComplexation_column = []

ProblemName = "porosityTest"
Phreeqc_file = "porosityTest.txt"
#
# Materials
#
poreDiffusion = 1.E-10
initialPorosity  = 0.79
material = Material (   name = "material", effectiveDiffusion = EffectiveDiffusion (initialPorosity*poreDiffusion),
                        permeability = Permeability (value = 1.0),
                        porosity = Porosity (value = initialPorosity)
                    )
                    
mineralRegion  = Region (support = mineralBody, material = material)

inletRegion    = Region (support = inletBoundary, material = material)

outletRegion   = Region (support = outletBoundary, material = material)


kineticLaws = [ReversibleKineticLaw("Mineral",rate=ReactionRate(6.55e-15,"mol/m**2/s"),SRExponent = 1.0,sphereModelExponent = 0.0,\
				    specificSurfaceArea = specificSurfaceArea)]
columnChemicalState = ChemicalState ("column_region", aqueousSolutionColumn, columnMineralPhaseSolution)
				  
regIC = InitialCondition (mineralBody, value = columnChemicalState)

boundaryConditionsList = []

inletBC = ChemicalState ("leftBC", inletAqueousSolution)
			  
inletBC  = BoundaryCondition (boundary = inletBoundary, btype ='Dirichlet', value = inletBC)
outletBC = BoundaryCondition (boundary = outletBoundary, btype="Dirichlet", value = columnChemicalState)

oneYear = 365.25*24*3600
tfinal= oneYear*0.4

Times=[0., tfinal]
#
#				   
#				   
outputlist = [  ExpectedOutput(quantity='Concentration',unknown='Si',format='table',name='Si'),
                ExpectedOutput(quantity='Concentration',unknown='Mineral',format='table',name='Si'),
                ExpectedOutput('porosity',timeSpecification=TimeSpecification(times=[tfinal]),
                format='table',save='file')]
#				   
#				   
#				   
Rtransport = ChemicalTransportProblem(  "test",
                                        regions                 = [mineralRegion, inletRegion, outletRegion],
                                        initialConditions       = [regIC],
                                        boundaryConditions      = [inletBC, outletBC],
                                        calculationTimes        = Times,
                                        sources                 = None,
                                        darcyVelocity           = Velocity(Vector([0.0, 0.0, 0.0])),
                                        chemistryDB = bdd,
                                        speciesBaseAddenda=speciesAddenda,
                                        kineticLaws = kineticLaws,
                                        activityLaw= None,
                                        timeUnit='s',
                                        porosityState = 'variable',
                                        outputs = outputlist)
#
# Creation of the link between transport and chemistry
#
InitialTimeStep = 3.1558e+04*0.5
#
print "chemicaltransport module "
test = ChemicalTransportModule()
test.setData (Rtransport, trace = 0, mesh = mesh, algorithm="CC")
test.setCouplingParameter(InitialTimeStep,
                           maxTimeStep                  = 3.1536e+07/3,
                           minTimeStep                  =3.1536e+04,
                           optimalIterationNumber       = 15,
                           maxIterationNumber           = 30,
                           increaTimeStepCoef           =1.05,
                           decreaTimeStepCoef           =0.75,
                           couplingPrecision            =1.e-6)
#
test.setTransportParameters("TVD")
test.setTransportParameters("JACOBI", 1.e-25)
speciesToPlot = []
pointToPlot = 0
if speciesToPlot !=[]:
    test.setInteractivePlot("test",speciesToPlot,pointToPlot,plotfrequency=10)
test.setComponent("Elmer","phreeqc")
test.transport.setTransportParameter(convSolver = 1.e-10,\
                                     iterSolver = 400,\
                                     indMemory = 0,\
                                     discretisation = dico['MethodChoice'],\
                                     algebraicResolution = 'Iterative',\
                                     timeSteppingMethod = "BDF",\
                                     preconditioner='ILU0',accelerator="GMRES") # possible values are CG CGS BiCGStab TFQMR GMRES
raw_input(" alors ")
#
# Outputs for 1.3
#
#test.setInteractiveSpatialPlot([	ExpectedOutput('Si',format='table'),
#					ExpectedOutput('Mineral',format='table')],interactivespatialplotfrequency = 5)
#test.setInteractiveSpatialPlot([	ExpectedOutput('concentration',unknow = 'Si',format='table')],interactivespatialplotfrequency = 5)
test.run()
print test.chemical.getPurePhaseList()
raw_input(" alors ")
#
name = 'Si'
outputs = test.getOutput('Si')
print " loop over times "
ind = 0
for output in outputs:
    ind += 1
    time = ind*InitialTimeStep
    output[1].writeToFile(name + "t%10.4e"%(time) + '.dat')
    #print " fermeture du fichier "
    pass

#====================================================
# Comparison to the analytical solution at final time 
#====================================================

print '============================='
print 'Error estimation on porosity '
print '============================ '

ncell=100
Length=0.10

precision=20

equil_ct = 1.3101E-4
conc_ini = equil_ct
conc_entree = 2.120270E-03
#conc_entree = 2.12E-03
conc_sortie = equil_ct
kinetic_ct  = 5.e-11*equil_ct
#kinetic_ct  = 5.23e-10*equil_ct
S0 = specificSurfaceArea
molar_volume = 22.68796e-03

step=Length/ncell
coef_lambda = kinetic_ct*S0/equil_ct
omega = sqrt(coef_lambda/poreDiffusion)

A=((conc_sortie-equil_ct)-((conc_entree-equil_ct)*exp(-1.*omega*Length)))/(2.*sinh(omega*Length))
B=((-1.*(conc_sortie-equil_ct))+((conc_entree-equil_ct)*exp(omega*Length)))/(2.*sinh(omega*Length))

print conc_sortie, equil_ct, coef_lambda, omega, A, B, pi

b=[0]
if (abs(equil_ct-conc_ini)>1.E-15):
    for i in range(precision):
        n=i+1
        val1=(-2.*((equil_ct-conc_ini)/(n*pi))*((-1)**n - 1.))-((2.*n*pi)/((omega*Length)**2+(n*pi)**2))*(A*(((exp(omega*Length))*(-1)**n)-1.)+B*(((exp(-1.*omega*Length))*(-1)**n)-1.))
        b.append(val1)
        pass
    pass
else:
    for i in range(precision):
        n=i+1
        val1=-((2.*n*pi)/((omega*Length)**2+(n*pi)**2))*(A*(((exp(omega*Length))*(-1)**n)-1.)+B*(((exp(-1.*omega*Length))*(-1)**n)-1.))
        b.append(val1)
        pass
    pass

#print "b=",b

Cinfini=[0]*ncell
serie=[0]*ncell
new_analytic_porosity=[0]*ncell

for j in range(ncell):
    if (j!=0):
        x=j*step+step/2.
        Cinfini[j]=A*exp(omega*x) + B*exp(-1.*omega*x) + equil_ct
        serie[j]=0.
        for i in range(precision):
            n=i+1
            int_expo = tfinal*(poreDiffusion*(n*pi)**2/(Length**2)+coef_lambda)
            if (int_expo < 300):
                serie[j]=serie[j]+b[n]/(poreDiffusion*(n*pi)**2/Length**2+coef_lambda)*sin(n*pi/Length*x)*exp(-int_expo)
            pass
        new_analytic_porosity[j]=initialPorosity*exp(coef_lambda*molar_volume*(tfinal*(equil_ct-Cinfini[j])-serie[j]))
        pass
    else:
        new_analytic_porosity[j]=initialPorosity*exp(coef_lambda*molar_volume*(tfinal*(equil_ct-conc_entree)))
	print " initial poro ",initialPorosity,coef_lambda,molar_volume,tfinal,equil_ct,conc_entree
        pass
    pass

#filename = "porosity_"+ "%10.4e"%(tfinal) +'.tab'
filename = "test.tab"
file = open(filename, 'r')
numeric_results = []
file.readline()
file.readline()
file.readline()
for i in file.readlines()[:-1]:
    numeric_results.append(float(i.split()[3]))
ind = 1
for i in new_analytic_porosity[1:100]:
     x=ind*step+step/2.
     print " x %15.10e analytic %15.10e numeric %15.10e diff %15.10e "%(x,i,numeric_results[ind],abs(numeric_results[ind]-i))
     ind+=1
ind = 0
error = 0.
for i in new_analytic_porosity[1:]:
    error0 = abs(numeric_results[ind]-i)
    error = max(error,error0)
    if abs(error0-error) < 1.e-8:
        ind_error = ind
#    print "error at ",ind,abs(numeric_results[ind]-i),i,numeric_results[ind]
    ind+=1
print " the maximum of the error is ",error," at time ",tfinal
epsilon_norme_porosity = 4E-5
if error > epsilon_norme_porosity:
    OKporo = 0
    print 'Be carefull: error on the porosity higher than 1 per thousand'
    pass
else:
    OKporo = 1
    print 'Good agreement of analytical and numerical results for porosity, the error is ', error
    pass

if OKporo:
    print "\n \n 1D porosity test with PHREEQC / ELMER coupling OK ********************\n \n"
    pass
else:
    mess = " Problem for the 1D constant diffusion porosity test ( PHREEQC / ELMER coupling)"
    raise(mess)
#
