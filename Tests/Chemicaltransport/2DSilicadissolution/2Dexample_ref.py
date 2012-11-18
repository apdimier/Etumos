from constant import epspH
from datamodel import *
import fields
from listtools import normMaxListComparison, subtractLists
from chemicaltransport import *
from chemicaltransportmodule import *
from mt3d import Mt3d              # mt3d
from cartesianmesh import *        # Cartesian mesh
from phreeqc import *              # phreeqc
from chemistry import *
from posttables import Table
from analytical2D_Na import AnalyticalFunction2D_Na

short = 1
sodaMass = 2.5E-5
Phreeqc_file = "2Dexample.txt"      # bounded to Phreeqc
ProblemName  = "2Dexample"          # Phreeqc file 
mesh = CartesianMesh2D("global","XY")
nx  = 101
ny  = 70
#~~~~~~~~~~~~~~~~~~
#~ Mesh extension ~
#~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~
#~ Mesh extension ~
#~~~~~~~~~~~~~~~~~~
dx0 = 0.05
dy0 = 0.05
deltax = []
dx = [5e-06/1]*1
deltax.extend(dx)
dx = [0.075/1]*1
deltax.extend(dx)
dx = [4.95/99]*99
deltax.extend(dx)
deltay = []
dy = [0.075/1]*1
deltay.extend(dy)
dy = [0.05/1]*1
deltay.extend(dy)
dy = [3.35/67]*67
deltay.extend(dy)
dy = [0.075/1]*1
deltay.extend(dy)
mesh.setdAxis("X",deltax)
mesh.setdAxis("Y",deltay)

field_2_190Zone = CartesianMesh2D("field_2_19", "XY")
field_2_190Zone.setZone("field_2_19",index_min = Index2D (2,34), index_max = Index2D (19,34))

field_21_1011Zone = CartesianMesh2D("field_21_101", "XY")
field_21_1011Zone.setZone("field_21_101",index_min = Index2D (21,34), index_max = Index2D (101,34))

field_2_35_702Zone = CartesianMesh2D("field_2_35_70", "XY")
field_2_35_702Zone.setZone("field_2_35_70",index_min = Index2D (2,35), index_max = Index2D (101,70))

field_20_343Zone = CartesianMesh2D("field_20_34", "XY")
field_20_343Zone.setZone("field_20_34",index_min = Index2D (20,34), index_max = Index2D (20,34))

NaOHBoundary4Zone = CartesianMesh2D("NaOHBoundary", "XY")
NaOHBoundary4Zone.setZone("NaOHBoundary",index_min = Index2D (1,1), index_max = Index2D (1,ny))

field_2_335Zone = CartesianMesh2D("field_2_33", "XY")
field_2_335Zone.setZone("field_2_33",index_min = Index2D (2,1), index_max = Index2D (nx,33))
#~~~~~~~~~~~~~
#~ Materials ~
#~~~~~~~~~~~~~
clayMaterial = Material (name = "clay",effectiveDiffusion = EffectiveDiffusion (0.0,unit="m**2/s"),\
permeability = Permeability(value = 1.0),\
porosity = Porosity(value = 1.0),\
kinematicDispersion = KinematicDispersion (0.2,0.05))
#~~~~~~~~~~~
#~ Regions ~
#~~~~~~~~~~~
field_2_190Region    = Region(support=field_2_190Zone, material= clayMaterial)
field_21_1011Region  = Region(support=field_21_1011Zone, material= clayMaterial)
field_2_35_702Region = Region(support=field_2_35_702Zone, material= clayMaterial)
field_20_343Region   = Region(support=field_20_343Zone, material= clayMaterial)
NaOHBoundary4Region  = Region(support=NaOHBoundary4Zone, material= clayMaterial)
field_2_335Region    = Region(support=field_2_335Zone, material= clayMaterial)
#~~~~~~~~~~~~~~~~~~~
# Chemical Addenda ~
#~~~~~~~~~~~~~~~~~~~
speciesAddenda = []
# Na
Na = AqueousMasterSpecies(symbol = "Na+",\
                          name = "Na",\
                          element = "Na",\
                          molarMass = MolarMass(0.0229898,"kg/mol"),\
                          alkalinity = 0.0)
speciesAddenda.append(Na)
# Si
Si = AqueousMasterSpecies(symbol = "H4SiO4",\
                          name = "Si",\
                          element = "SiO2",\
                          molarMass = MolarMass(0.0280843,"kg/mol"),\
                          alkalinity = 0.0)
speciesAddenda.append(Si)
# Na
NaSSp = AqueousSecondarySpecies(symbol = "Na+",\
                                formationReaction = [("Na+",1)],\
                                logK25 = 0.0,\
                                name = "Na")
speciesAddenda.append(NaSSp)
# Si
SiSSp = AqueousSecondarySpecies(symbol = "H4SiO4",\
                                formationReaction = [("H4SiO4",1)],\
                                logK25 = 0.0,\
                                name = "Si")
speciesAddenda.append(SiSSp)
#H3SiO4
H3SiO4SSp = AqueousSecondarySpecies(symbol = "H3SiO4-",\
                                    formationReaction = [("H4SiO4",1),("H+",-1)],\
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
sodaMineralPhase = MineralPhase([MineralTotalConcentration("Quartz",0.0, "mol/l")])

surface = dx0*dy0

C0         = (sodaMass/surface)
print "C0 ",C0

sodaAqueousSolution = AqueousSolution (elementConcentrations = [ElementConcentration ('Na', C0, "mol/l")
                                                               ],\
                                       pH = 12.2545,\
                                       pe = 4)
sodaChemicalState = ChemicalState ("soda", sodaAqueousSolution, sodaMineralPhase)

columnMineralPhase = MineralPhase([MineralTotalConcentration("Quartz",1.0, "mol/l")])
columnAqueousSolution = AqueousSolution (elementConcentrations = [ElementConcentration ("Na",0.0,"mol/l")
                                                                 ],\
                                         pH = 7.0,\
                                         pe = 4)
columnChemicalState = ChemicalState ("column",columnAqueousSolution,columnMineralPhase)

#~~~~~~~~~~~~~~~~~~~~
# Initial condition ~
#~~~~~~~~~~~~~~~~~~~~
field_2_33IC = InitialCondition (body  = field_2_335Zone, value = columnChemicalState)
field_2_19IC = InitialCondition (body  = field_2_190Zone, value = columnChemicalState)
field_21_101IC = InitialCondition (body  = field_21_1011Zone, value = columnChemicalState)
field_2_35_70IC = InitialCondition (body  = field_2_35_702Zone, value = columnChemicalState)
field_20_34IC = InitialCondition (body  = field_20_343Zone, value = sodaChemicalState)
#~~~~~~~~~~~~~~~~~~~~~
# Boundary condition ~
#~~~~~~~~~~~~~~~~~~~~~
NaOHBoundaryBC = BoundaryCondition (boundary = NaOHBoundary4Zone, btype="Dirichlet", value = columnChemicalState)

initialTime = 0.0
if short:
    finalTime= 72000*4
else:
    finalTime= 72000*8
    pass
#finalTime = 6.e+4
Times=[initialTime,finalTime]
#~~~~~~~~~~~~~~~~~~~
# Expected outputs ~
#~~~~~~~~~~~~~~~~~~~
expectedOutputs = [ExpectedOutput("pH",format="table",name="pH_output",timeSpecification=TimeSpecification(times=[finalTime])),
ExpectedOutput("Concentration","Na",format="table",name="Na_output",timeSpecification=TimeSpecification(times=[finalTime]))]
#~~~~~~~~~
# Module ~
#~~~~~~~~~
module = ChemicalTransportModule()
problem = ChemicalTransportProblem(name               = "2Dexample",\
                                    regions            = [field_2_190Region,field_21_1011Region,field_2_35_702Region,field_20_343Region,NaOHBoundary4Region,field_2_335Region],\
                                    initialConditions  = [field_2_19IC,field_21_101IC,field_2_35_70IC,field_20_34IC,field_2_33IC],\
                                    boundaryConditions = [NaOHBoundaryBC],\
			            calculationTimes    = Times,\
                                    sources            = None,\
                                    darcyVelocity      = None,\
                                    chemistryDB        = "water_gui.dat",\
                                    speciesBaseAddenda = speciesAddenda,\
                                    kineticLaws        = None,\
                                    activityLaw        = None,\
                                    outputs            = expectedOutputs)
module.setData (problem, trace = 0, mesh = mesh, algorithm="CC")
module.setComponent("mt3d","phreeqc")
module.setTransportParameters("T.V.D.")
module.setTransportParameters("Jacobi",1e-15)
module.setCouplingParameter(initialTimeStep        = 2000.0,
                            minTimeStep            = 1.5e+3,
                            maxTimeStep            = 4.e+4,
                            couplingPrecision      = 1e-06,
                            optimalIterationNumber = 20,
                            maxIterationNumber     = 40,
                            decreaTimeStepCoef     = 0.75,
                            increaTimeStepCoef     = 1.05)
list_of_species_toplot = []
pointtoplot = 1
if list_of_species_toplot !=[]:
    module.setInteractivePlot(" module ",list_of_species_toplot,pointtoplot,plotfrequency=10)
#module.setInteractiveSpatialPlot(outputs)
print " debut de run"
module.setVtkOutputsParameters(["Na","pH"],"days",2)
module.run()

from analytical_pH_62_2D import AnalyticalFunction_pH_62_2D

print '====================== '
print 'Error estimation on pH '
print '====================== '

pH_analytic = AnalyticalFunction_pH_62_2D(finalTime,sodaMass)

res_ph     = module.getOutput("pH_output")
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
    numerical_value = res_ph[-1][1].values[2][ind]
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
    numerical_value = res_ph[-1][1].values[2][ind]
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
    print "\n \n -- Test-case Alkaline 2D with MTMS/PHREEQC coupling OK -- \n \n"
    pass
else:
    msg = " Problem for the Test-case Alkaline 2D with MTMS/PHREEQC coupling"
    raise msg
    
from analytical_Na_62_2D import AnalyticalFunction2D_Na
Na_analytic = AnalyticalFunction2D_Na(finalTime,sodaMass)
res_na     = module.getOutput("Na_output")


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
    numerical_value = res_na[-1][1].values[2][ind]
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
    numerical_value = res_na[-1][1].values[2][ind]
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
    print "\n \n -- MTMS/PHREEQC coupling OK -- \n \n"
    pass
else:
    msg = " Problem for the MTMS/PHREEQC coupling"
    raise msg
    
    
print '~~~~~~~~~~~~~~~~~~~~~~~'
print 'End of the 2D test case'
print '~~~~~~~~~~~~~~~~~~~~~~~'
#
module.end()
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "        End of the 2Dexample case ~"
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
