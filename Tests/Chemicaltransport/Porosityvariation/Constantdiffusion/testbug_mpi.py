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

MineralPhaseSolution_column = MineralPhase ([MineralTotalConcentration("Mineral", 0.0, "mol/l")])

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
dx[0]=dx[0]*52.
deltax.extend(dx)
deltay = []
dy = [0.1/1]*1
deltay.extend(dy)

mesh.setdAxis("X",deltax)
mesh.setdAxis("Y",deltay)



material = Material (name = "material", effectiveDiffusion = EffectiveDiffusion (0.79e-10),\
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
oneYear = 365.25*24*3600
tfinal= oneYear*10

Times=[0., tfinal]
#
outputlist = []
outputlist.append(ExpectedOutput(quantity='Concentration',unknown='Si',format='table',name='Si'))
outputlist.append(ExpectedOutput(quantity='Concentration',unknown='Mineral',format='table',name='Min'))
#
# It generates a file called test.tab
#
outputlist.append(ExpectedOutput('porosity',
                                 timeSpecification = TimeSpecification(times=[tfinal]),
                                 format='table',
                                 save='file')
                                )
#outputlist.append(ExpectedOutput(quantity='Concentration',unknown='Mineral',
#                                 timeSpecification = TimeSpecification(times=[tfinal]),
#                                 format='table',
#                                 save='file')
#                                )
#				   
Rtransport=ChemicalTransportProblem("test",\
			            regions_list,\
			            boundaryconditions_list,\
			            initialconditions_list,\
			            Times,\
				    sources=None,\
				    darcyVelocity=Velocity(Vector([0.0, 0.0, 0.0])),\
			            chemistryDB = bdd,\
			            speciesBaseAddenda=speciesAddenda,\
			            kineticLaws = kineticLaws,\
			            mpiSize = 2,\
			            activityLaw= None,\
				    timeUnit='s',
				    porosityState = 'variable', 
			            outputs = outputlist)
#
# Creation of the link between transport and chemistry
#
initialTimeStep = 3.1558e+03

print "chemicaltransport module "
test = ChemicalTransportModule()
test.setData (Rtransport, trace = 0, mesh = mesh, algorithm="CC")
test.setCouplingParameter(      initialTimeStep,
                                maxTimeStep             = 3.1536e+07/10.,
                                minTimeStep             = 3.1536e+04,
                                optimalIterationNumber  = 15,
                                maxIterationNumber      = 20,
                                increaTimeStepCoef      = 1.08,
                                decreaTimeStepCoef      = 0.5,
                                couplingPrecision       = 1.e-3)
test.setTransportParameters("TVD")
test.setTransportParameters("JACOBI", 1.e-20)
list_of_species_toplot = []
pointtoplot = 0
if list_of_species_toplot !=[]:
    test.setInteractivePlot("test",list_of_species_toplot,pointtoplot,plotfrequency=10)
test.setComponent("mt3d","phreeqc")
#
# Outputs for 1.3
#
#test.setInteractiveSpatialPlot([	ExpectedOutput('Si',format='table'),
#					ExpectedOutput('Mineral',format='table')],interactivespatialplotfrequency = 5)
#test.setInteractiveSpatialPlot([	ExpectedOutput('concentration',unknow = 'Si',format='table')],interactivespatialplotfrequency = 5)
test.run()
#
name = 'Si'
outputs = test.getOutput('Si')
print " loop over times "
i = 0
for output in outputs:
    i+=1
    time = i*initialTimeStep
    file = name + "t%10.4e"%(time) + '.dat'
    #print output
    output[1].writeToFile(file)
    #print " fermeture du fichier "
    pass

#=============================
# Comparison to the analytical
#=============================

print '============================ '
print 'Error estimation on porosity '
print '============================ '

ncell=100
Length=0.10

precision=20

equil_ct = 1.3101E-4
pore_diffus = 1.E-10
initial_porosity  = 0.79
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
omega = sqrt(coef_lambda/pore_diffus)

A=((conc_sortie-equil_ct)-((conc_entree-equil_ct)*exp(-1.*omega*Length)))/(2.*sinh(omega*Length))
B=((-1.*(conc_sortie-equil_ct))+((conc_entree-equil_ct)*exp(omega*Length)))/(2.*sinh(omega*Length))

print conc_sortie,equil_ct,coef_lambda,omega,A,B,pi

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
            int_expo = tfinal*(pore_diffus*(n*pi)**2/(Length**2)+coef_lambda)
            if (int_expo < 300):
                serie[j]=serie[j]+b[n]/(pore_diffus*(n*pi)**2/Length**2+coef_lambda)*sin(n*pi/Length*x)*exp(-int_expo)
            pass
        new_analytic_porosity[j]=initial_porosity*exp(coef_lambda*molar_volume*(tfinal*(equil_ct-Cinfini[j])-serie[j]))
        pass
    else:
        new_analytic_porosity[j]=initial_porosity*exp(coef_lambda*molar_volume*(tfinal*(equil_ct-conc_entree)))
	print " initial poro ",initial_porosity,coef_lambda,molar_volume,tfinal,equil_ct,conc_entree
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
    numeric_results.append(float(i.split()[2]))
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
epsilon_norme_porosity = 4E-2
if error > epsilon_norme_porosity:
    OKporo = 0
    print 'Be careful: error on the porosity higher than 1 per thousand'
    pass
else:
    OKporo = 1
    print 'Good agreement of analytical and numerical results for porosity, the error is ', error
    pass

if OKporo:
    print "\n \n 1D porosity test with PHREEQC / MT3D coupling OK ********************\n \n"
    pass
else:
    raise Exception, " Problem for the 1D constant diffusion porosity test ( PHREEQC / MT3D coupling)"
#
