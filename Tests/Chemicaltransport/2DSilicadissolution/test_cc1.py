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

#
columnMineralPhase = MineralPhase([MineralTotalConcentration("Quartz",1.0, "mol/l")])

#
pH = 7.0
pe = 4.0
Aqueousspecieslist_NaOH_bc0 = []


Na_NaOH_bc0 = ElementConcentration ("Na", 0.0e-02, "mol/l")
Aqueousspecieslist_NaOH_bc0.append (Na_NaOH_bc0)

AqueousSolution_NaOH_bc0 = AqueousSolution (Aqueousspecieslist_NaOH_bc0, pH, pe)
#
#
# Definition of the Aqueous column chemical State
#
#
columnAqueousSolution = AqueousSolution (elementConcentrations = [ElementConcentration ("Na",0.0,"mol/l")
                                                                 ],\
                                         pH = 7.0,\
                                         pe = 4)
columnChemicalState = ChemicalState ("column",columnAqueousSolution,columnMineralPhase)

clayMaterial = Material(name = "clay",effectiveDiffusion = EffectiveDiffusion (0.0,unit="m**2/s"),\
                        permeability = Permeability(value = 1.0),\
                        porosity = Porosity(value = 1.0),\
                        kinematicDispersion = KinematicDispersion (0.2,0.05))
                                                        
listOfRegions = []
initialconditions_list = []
column_reg_m = CartesianMesh2D ("columnRegion", "XY")
column_reg_m.setZone ("columnRegion", index_min = Index2D (2, 1), index_max = Index2D (nx, 33))
reg0 = Region (column_reg_m, clayMaterial)
listOfRegions.append (reg0)

reg0_ic = InitialCondition (column_reg_m, value = columnChemicalState)
initialconditions_list.append (reg0_ic)

column_reg_m1 = CartesianMesh2D ("columnRegion1", "XY")
column_reg_m1.setZone ("columnRegion", index_min = Index2D (2, 34), index_max = Index2D (19, 34))
reg1 = Region (column_reg_m1, clayMaterial)
listOfRegions.append (reg1)
reg1_ic = InitialCondition (column_reg_m1, value = columnChemicalState)
initialconditions_list.append (reg1_ic)

column_reg_m2 = CartesianMesh2D ("columnRegion2", "XY")
column_reg_m2.setZone ("columnRegion", index_min = Index2D (20, 34), index_max = Index2D (20, 34))
reg2 = Region (column_reg_m2, clayMaterial)
listOfRegions.append (reg2)

reg2_ic = InitialCondition (column_reg_m2, value = sodaChemicalState)
initialconditions_list.append (reg2_ic)

column_reg_m3 = CartesianMesh2D ("columnRegion3", "XY")
column_reg_m3.setZone ("columnRegion", index_min = Index2D (21, 34), index_max = Index2D (nx, 34))
reg3 = Region (column_reg_m3, clayMaterial)
listOfRegions.append (reg3)
reg3_ic = InitialCondition (column_reg_m3, value = columnChemicalState)
initialconditions_list.append (reg3_ic)

column_reg_m4 = CartesianMesh2D ("columnRegion4", "XY")
column_reg_m4.setZone ("columnRegion", index_min = Index2D (2, 35), index_max = Index2D (nx, ny))
reg4= Region (column_reg_m4, clayMaterial)
listOfRegions.append (reg4)
reg4_ic = InitialCondition (column_reg_m4, value = columnChemicalState)
initialconditions_list.append (reg4_ic)

boundaryconditions_list = []
NaOH_bc0_bo_m0 = CartesianMesh2D ("NaOH_bc0boundary", "XY")
NaOH_bc0_bo_m0.setZone ("NaOH_bc0boundary", index_min = Index2D (1, 1), index_max = Index2D (1, ny))
NaOHBoundary4Region = Region (NaOH_bc0_bo_m0, clayMaterial)
listOfRegions.append (NaOHBoundary4Region)

NaOHBoundaryBC = BoundaryCondition (boundary = NaOH_bc0_bo_m0,  btype="Dirichlet", value = columnChemicalState)
#NaOHBoundaryBC = BoundaryCondition (boundary = NaOHBoundary4Zone, btype="Dirichlet", value = columnChemicalState)
boundaryconditions_list.append (NaOHBoundaryBC)

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
			            regions             = listOfRegions,\
			            boundaryConditions  = boundaryconditions_list,\
			            initialConditions   = initialconditions_list,\
			            calculationTimes    = Times,\
				    sources             = None,\
				    darcyVelocity       = None,\
			            chemistryDB         = "water_gui.dat",\
			            speciesBaseAddenda  = speciesAddenda,\
			            kineticLaws         = None,\
			            activityLaw         = None,\
			            outputs             = expectedOutputs)
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
module.setVtkOutputsParameters(["Na"],"days",2)
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
