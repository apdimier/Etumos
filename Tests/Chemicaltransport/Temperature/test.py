# -*- coding: utf-8 -*-
#
#  Problem name: Temperature
#
#  Description:  This test-case involves the diffusion
#  of alkaline water (NaOH) in a column composed of grains
#  of pure quartz, leading to acid/base reactions together
#  with mineral dissolution and a temperature from 25 to 70 C 
#
#  Units :
#    length : m
#    time   : s
#
#  Geometry : column of 0.06 m. The mesh is regular
#  (2D mesh with one cell in the other direction)
#
#  Diffusive problem:   Molecular diffusion     : 3.E-10 m2/s = 9.5E-18 m2/y
#    Pore water Darcy velocity   : 0.
#    Porosity                    : 1.
#    Molecular diffusion         : 3.E-10 m2/s = 9.5E-18 m2/y
#    Thermal conductivity        :  = rho*Cp*kappa where kappa is the thermal diffusivity
#    Effective diffusion = Porosity x Molecular diffusion
#    Thermal Diffusion   = Porosity x Molecular diffusion
#
#  Chemical states :
#    NaOH water on the boundary condition
#    quartz groundwater
#
# Chemical parameters
#
# Ks = 1E-3.6 at 25°C and 1E-2 at 70°C
# Ka = 1E-9.8 at 25°C and 1E-7 at 70°C
#
#  Author  : A. Dimier
#  Date    : 18/10/2009
#
# The heat conduction equation is :
#
#   				rho*Cp*DT/dt = K*Nabla(Nabla(T) + Hrho
#
# A reference temperature of T0 = 25. is taken
#
from constant import epspH
import os
from mesh import *         
from datamodel import *   
import sys
from chemicaltransportmodule import *
from listtools import normMaxListComparison, subtractLists

dico = {'MethodChoice' : 'FE'}

ProblemName  = "temperature"          # necessary for Phreeqc
setProblemType("ChemicalTransport")

 
ChemicalStateList = []
newSpeciesList=[]

meshFileName = "essai.msh"
mesh = Mesh2D(meshFileName)
numberOfVertices = mesh._getNumberOfVertices()
#print "numberOfVertices",numberOfVertices
#raw_input()
columnBody    = mesh.getBody('domain')
#print columnBody
inletBoundary = mesh.getBody('inlet')
#raw_input()

############################################################
#  For Modules requiring Species, define Species and Element properties
############################################################

# =========================================================
# New species definition
# =========================================================
speciesAddenda = []

logKa25 = -9.83
logKa70 = -7
logKs25 = -3.6
logKs70 = -2
Na = AqueousMasterSpecies(symbol = "Na+",\
                             name = "Na",\
                             element = "Na",\
                             molarMass = MolarMass(0.02299,"g/mol"),\
                             alkalinity = 0)
speciesAddenda.append(Na)
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
				   
cte = (logKa25 - logKa70)/(298.15 - 343.15)

H3SiO4SSp = AqueousSecondarySpecies(symbol = "H3SiO4-",\
                                    formationReaction = [('H4SiO4', 1),('H+', -1)],
                                    logK25 = logKa25,
                                    logK  = [logKa25-cte*298.15,cte],
                                    name ='H3SiO4')
				  
cte = (logKs25 - logKs70)/(298.15 - 343.15)
QuartzAd = MineralSecondarySpecies(symbol = "SiO2",\
                                   formationReaction = [("H2O",-2),("H4SiO4",1)],\
                                   logK25 = -3.6,\
                                   logK = [logKs25-cte*298.15,cte],
                                   name = "Quartz",\
                                   density = Density(2648.29,"kg/m**3"))
speciesAddenda.append(QuartzAd)

#~~~~~~~~~~~~~~~~~~~~~~~
#  Materials and regions
#~~~~~~~~~~~~~~~~~~~~~~~
De = 3.e-10
poro = 1
constEffecCond = 1.e-7
#
# The thermal conductivity is the one of the material. For the analytical solution, the thermal conductivity to be
# considered is the WaterThermalConductivity. 
#
columnMaterial = Material       (name = "quartz",
                                effectiveDiffusion = EffectiveDiffusion (De),\
                                porosity = Porosity (value = 1.0),\
                                specificHeat = SpecificHeat(1.),\
                                thermalConductivity = ThermalConductivity (constEffecCond,unit='kg*m/s3/K'))

columnRegion = Region (support=columnBody, material = columnMaterial)

inletRegion  = Region (support=inletBoundary, material = columnMaterial)
#~~~~~~~~~~~~~~~~~~~~~~~
#  Materials and regions
#~~~~~~~~~~~~~~~~~~~~~~~

#velocity = Velocity(Vector(0.,0.))
ChemicalStateList = []

#~~~~~~~~~~~~~~~~
# Chemical States
#~~~~~~~~~~~~~~~~
boundaryAqueousSolution = AqueousSolution (elementConcentrations = [ElementConcentration ('Na', 2.0e-02, "mol/l")\
                                                                   ],\
                                           pH = 7.0,\
                                           temperature = 70.0)
boundaryChemicalState   = ChemicalState ("boundary", boundaryAqueousSolution, charge = 1)

columnAqueousSolution = AqueousSolution (elementConcentrations = [ElementConcentration ('Na', 0.0, "mol/l")\
                                                                 ],\
                                         pH= 7.0, temperature = 25.0)
columnMineralPhase = MineralPhase([MineralTotalConcentration("Quartz",10.0, "mol/l", saturationIndex = 0.0)])
columnChemicalState = ChemicalState ("column", columnAqueousSolution, columnMineralPhase)

#~~~~~~~~~~~~~~~~~~~
# Initial conditions
#~~~~~~~~~~~~~~~~~~~

columnInit = InitialCondition (body  = columnBody,
                                             value = columnChemicalState)
#~~~~~~~~~~~~~~~~~~~
# Boundary conditions
#~~~~~~~~~~~~~~~~~~~

inletBC = BoundaryCondition (boundary = inletBoundary,   btype='Dirichlet', value = boundaryChemicalState)

#~~~~~~~~~~~~~~~
# Simulated time
#~~~~~~~~~~~~~~~
initialTime = 0.0
time1   =  3600.*24.*1    
time2   = 3600.*24.*1.5   
finalTime = 3600*24*2
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Definition of Expected Outputs
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

times = TimeSpecification(times=[time1,time2,finalTime])
expectedOutputs = [ExpectedOutput('pH',format='table',name='pHOutput', timeSpecification=times),
                   ExpectedOutput('Concentration', 'Na', 'mol/l', name='NaOutput', format='table', timeSpecification=times),
                   ExpectedOutput('temperature', format ='table',  name   ='TempOutput', timeSpecification=times)]
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Definition of Problem: Insert all previous variables in the problem
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

module = ChemicalTransportModule()
problem  = ChemicalTransportProblem(name               = "temperature",
                                    regions            = [columnRegion],
                                    initialConditions  = [columnInit],
                                    boundaryConditions = [inletBC],
                                    calculationTimes   = [initialTime, finalTime],
                                    sources            = None,
                                    darcyVelocity      = Velocity(Vector([0.0, 0.0, 0.0])),
                                    chemistryDB        = "water_gui.dat",\
                                    speciesBaseAddenda = speciesAddenda,\
				    temperature        = "variable",
                                    kineticLaws        = None,
                                    activityLaw        = None,
                                    outputs            = expectedOutputs)

module.setData(problem,mesh=mesh,trace=0,algorithm="NI")
module.setComponent("Elmer","Phreeqc")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Define the Component and its solver parameters
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

module.transport.setTransportParameter(convSolver = 1.e-8,\
				       iterSolver = 800,\
				       indMemory = 0,\
                                       discretisation = dico['MethodChoice'],\
				       algebraicResolution = 'Iterative',\
				       timeSteppingMethod = "BDF",BDFOrder = "1",\
				       preconditioner='ILU4',accelerator="CG")
#				       timeSteppingMethod = "BDF",\
#				       preconditioner='ILU0',accelerator="TFQMR",thetaScheme=0.0)
module.transport.setWaterDensity(1.0)
module.transport.setWaterHeatCapacity(1.)
module.transport.setWaterHeatConductivity(1.0e-7)
module.setCouplingParameter(initialTimeStep       = 2.e+0,
                            maxTimeStep           = 5000,
                            minTimeStep           = 5.e+0,
                            couplingPrecision     = 1.e-3,
                            maxIterationNumber    = 30,
                            optimalIterationNumber = 20,
                            increaTimeStepCoef    = 1.05,
                            decreaTimeStepCoef    = 0.8)

module.setVtkOutputsParameters(["Na","temperature"], "s", 3600.*24)

module.launch()
while (module.simulatedTime < module.times[-1]):
    module.oneTimeStep()
    pass

#~~~~~~~~~~~~~~~~~~~~~~
# post processing 
#~~~~~~~~~~~~~~~~~~~~~~

outpH = module.getOutput('pHOutput')
outNa = module.getOutput('NaOutput')
outT  = module.getOutput('TempOutput')

NadeX      = outNa[-1][-1]
pHdeX      = outpH[-1][-1]
TdeX       = outT[-1][-1]
#print ' first element of the time list: ',outT
#print ' first element of the ph list: ',pHdeX
tps        = outpH[-1][0]

import os
file = 'pHdeX_2j_70.tab'
if os.path.exists(file):
    os.remove(file)
    pass
pHdeX. writeToFile(file)

file = 'NadeX_2j_70.tab'
if os.path.exists(file):
    os.remove(file)
    pass
NadeX. writeToFile(file)


file = 'T_2j_70.tab'
if os.path.exists(file):
    os.remove(file)
    pass
TdeX. writeToFile(file)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Comparison to analytical concentration
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
listX = []
for i in range(150):
    listX.append(i*0.001)
print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
print ' Comparison to analytical solution'
print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
from analyticalT import AnalyticalSolution
# comparison at short time  for T 
Na0 = 2.E-2
Kw,Ks,Ka = 1.E-7, pow(10.,logKs70), pow(10.,logKa70) # valeurs definies pour une temperature de 70°C

temperatureTable = TdeX
numericalSolution  = temperatureTable.getColumn(3)
# constante calculee pour une temperature de 25°C
#-----------------------------------------------
T0_LamW     = 25.5       
                         # pour le calcul de la conductivite de l'eau
rhocpW_ini = 4189000.0  

old_version = 0

if old_version :
    LamW   = 0.5621 + 0.00193 * T0      - 7.3e-6 * T0**2
    rhocpW = 1.e3 * 4284.9
else:
    LamW   = 0.5621 + 0.00193 * T0_LamW - 7.3e-6 * T0_LamW**2
    rhocpW = rhocpW_ini   

solidThermalConductivityConstant = 0.0
LamS   = solidThermalConductivityConstant
poro   = 1.
Lameff = ((1 - poro) * LamS + poro * LamW) / rhocpW

rhoS   = 2678.29            
Cps    = 1.
rhocpS = rhoS * Cps
RT     = 1 + ( ((1 - poro) * rhocpS) / (poro *rhocpW))

Dd     = 0
const  = (Lameff + poro * Dd) / (poro * RT) 
##print "effective conductivity = ", const
print listX
#raw_input()
A = AnalyticalSolution(finalTime,Na0,listX,De,Kw,Ks,Ka, 1, 1.,constEffecCond,25.,70.)
analyticalSolution = A.evalT()
#print analyticalSolution[2:21]
numSol = []
ind = 0
for i in numericalSolution[0:40]:
    ind+=1
    if ind % 2 == 0:
        numSol.append(i)
#    print " num sol ",ind,i,analyticalSolution[ind]
print " numer ",numericalSolution
normT = normMaxListComparison(numericalSolution[0:15],analyticalSolution[0:15])
ind  = 0
print analyticalSolution
epsilonT = 3.E-2
if normT > epsilonT:
    OKT = 0
    print 'Be carefull: error on  T higher than 3% and equal to ', normT
else :
    OKT = 1
    print 'Good agreement between numerical and analytical results for  T , error lower than 3%, equal to ', normT
print ' '

if (OKT):    
    print "\n \n ~~~~~~~~~~~~~~~~~~~~~~ Test-case on temperature is OK ~~~~~~~~~~~~~~~~~~~~~~\n \n"
    pass
else:
    raise Warning, " Problem for the Test-case on temperature"
print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
print ' End of the temperature test case'
print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'

module.end()

