#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#
#  We study here the diffusion  of alkaline water (NaOH) in a column 
#  made of Quartz => leading to acide/base reactions inducing quartz dissolution.
#
#  The transport parameters are the following:
#
#    Pore water Darcy velocity   : 0.
#    Porosity                    : 1.
#    Effective diffusion =  3.e-10 m**2/s (medium porosity * Molecular diffusion
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
Phreeqc_file = "test.txt"      # bounded to Phreeqc
ProblemName  = "test"          # Phreeqc file 
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
expectedOutputs = [ExpectedOutput("Concentration","Na",format="table",name="NaOutput"),
ExpectedOutput("pH",format="table",name="pH_output")]
#~~~~~~~~~
# Module ~
#~~~~~~~~~
module = ChemicalTransportModule()
problem  = ChemicalTransportProblem(name               = "test",\
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
                            minTimeStep            = 2.e+2,
                            maxTimeStep            = 5.e+4,
                            couplingPrecision      = 1e-08,
                            optimalIterationNumber = 20,
                            maxIterationNumber     = 30,
                            decreaTimeStepCoef     = 0.8,
                            increaTimeStepCoef     = 1.1)
module.run()
#~~~~~~~~~~~~~~~~~~
# Post processing ~
#~~~~~~~~~~~~~~~~~~
res_ph     = module.getOutput('pH_output')
res_na     = module.getOutput('NaOutput')

NadeX      = res_na[-1][1]
pHdeX      = res_ph[-1][1]
time       = res_ph[-1][0]
print "time:", time
dx0 = dx[1]
liste_X   = NadeX.getColumn(0)
liste_dx0 = [dx0] * (len(liste_X))
liste_decalX = subtractLists(liste_X,liste_dx0)

from posttables import Table

tab1  = Table(name='TabNa')
tab1.addColumn('X',liste_decalX)
tab1.addColumn('Y',NadeX.getColumn(1))
tab1.addColumn('Na',NadeX.getColumn(2))
NadeX = tab1

tab2  = Table(name='TabpH')
tab2.addColumn('X',liste_decalX)
tab2.addColumn('Y',pHdeX.getColumn(1))
tab2.addColumn('Na',pHdeX.getColumn(2))
pHdeX = tab2

pHdeX. writeToFile('pHdeX_10j.tab')
NadeX. writeToFile('NadeX_10j.tab')

############################################################
#  Comparison to analytical concentration
############################################################
from analyticalSolution_Sildissolution import *
dx = [0.004]
finalTime = 864000.0
for i in range(1,30):
    dx.append(dx[0]+dx[i-1])
analFunction = analyticalFunction(finalTime, 0.02, dx, 3.e-10)
print '================================================= '
print '       comparison to the analytic solution'
print '================================================= '

table_Na_numeric = NadeX


list_Na_analytic = analFunction.evalNa()
list_Na_numeric  = table_Na_numeric.getColumn(2)
print " ana: ",list_Na_analytic[0:20]
print " num: ",list_Na_numeric[0:20]
# on tronque la liste de la solution analytique si elle est trop longue


norme_Na = normMaxListComparison(list_Na_numeric[0:30],list_Na_analytic[0:30])
print 'norme_Na = ',norme_Na
epsilon_Na = 10.E-2
if norme_Na > epsilon_Na:
    OKConc = 0
    print 'Be carefull: error on the Na concentration higher than 10% and equal to ',norme_Na*100,"%"
else :
    OKConc = 1
    print 'Good agreement between numerical and analytical results for the Na concentration, error equal to ',norme_Na*100,"%"
print ' '

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Comparison to analytical pH
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

table_pH_numeric = pHdeX

list_pH_analytic = analFunction.evalPH()
list_pH_numeric  = table_pH_numeric.getColumn(2)
print "num: ",list_pH_numeric[0:20]
print "anal:",list_pH_analytic[0:20]
# on tronque la liste de la solution analytique si elle est trop longue


pHinf = normMaxListComparison(list_pH_numeric[0:30],list_pH_analytic[0:30])

print 'pH max norm is ',pHinf
if pHinf > epspH:
    OKpH = 0
    print 'Be carefull: error on the pH higher than 3% and equal to: ', pHinf*100,"%"
else :
    OKpH = 1
    print 'Good agreement between numerical and analytical results for pH, error equal to: ',pHinf*100,"%"

if (OKpH):    
    print "\n \n -- Silicate dissolution test PHREEQC/ MT3D coupling OK --\n \n"
    pass
else:
    raise Warning, " Problem for the Silicate Dissolution 1D test with PHREEQC/ MT3D coupling"
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "        End of the Silicate dissolution test case "
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
module.end()
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "        End of the test case ~"
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

module.end()
