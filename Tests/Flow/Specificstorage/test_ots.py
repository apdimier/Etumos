"""
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 The problem  is saturated 2D: file SDarcy2d.geo

 We set a Dirichlet boundary condition on 
 the left side of the domain H = H0.
 
 The initial condition is H = 0
 
 The specific storage is constant S0 and 
 the hydraulic conductivity is isotropic: K0.
 
 The analytic solution is :
 
            h = H0*erfc(x/(2sqrt(K0t/S0))
 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import os
from mesh import *
from datamodel import *
from math import sqrt,pow
from hydraulicmodule import *
import sys
from time import time
from material import *
from exceptions import Exception
from hydraulicproblem import *
from saturatedhydraulicproblem import *
from functions import LinearFunction
from _erffunctions import erfc
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Define Mesh, and get Zones and Boundaries from.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
dico = { 'MethodChoice' : 'FE'}

ProblemName  = "testHydraulic" 

meshFileName = "SDarcy2d.msh"
mesh = Mesh3D(meshFileName)
numberOfVertices = mesh._getNumberOfVertices()
print numberOfVertices
#
print mesh.getBodies()
#
print mesh.getDim()
columnBody    = mesh.getBody('domain')
#
AB = mesh.getBody('AB')
print " AB "
#
coords = mesh.getNodesCoordinates()
#
# Specific constants of the problem
#
hydraulicConductivity       = 1.e-5
k0 = hydraulicConductivity
SpecificStorageCoefficient  = 1.e-0
initialCharge               = 1.e-0
H0 = initialCharge
#
# The simulation is transient
#
density         = 1.
viscosity       = 1.
compressibilityModel = False
#
#---------------------------------------------------------------------
#   Begin : First, set problem type
#---------------------------------------------------------------------
#
#---------------------------------------------------------------------
#  Definition of Material and Regions associated
#---------------------------------------------------------------------
#
columnMaterial = Material(name="Mat",hydraulicconductivity = HydraulicConductivity(value = hydraulicConductivity),\
                                     porosity = Porosity(value = 1.0),\
                                     specificStorage = SpecificStorage(SpecificStorageCoefficient))

#~~~~~~~~~~~
#~ Regions ~
#~~~~~~~~~~~
columnRegion = Region (support = columnBody, material = columnMaterial)
    
ABRegion = Region (support = AB, material = columnMaterial)
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Definition of Boundary Conditions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
ABBoundary = BoundaryCondition(ABRegion, 'Dirichlet', Head(initialCharge, "m"))
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Definition of Initial Conditions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
columnInit = InitialCondition (columnRegion, Head(0.,"m"))
#---------------------------------------------------------------------
#  Definition of Problem: Insert all previous variables in the problem
#---------------------------------------------------------------------
# Problem definition
finalTime = 1000.
problem = SaturatedHydraulicProblem( name                    = "TransientHydraulic",
#                           saturation              = "saturated",
                            regions                 = [columnRegion, ABRegion],\
                            boundaryConditions      = [ABBoundary],\
                            initialConditions       = [columnInit],\
                            calculationTimes        = [0., finalTime],\
                            source                  = None,\
                            outputs                 = [],\
                            viscosity = Viscosity(1.0e-0,"kg*m/s"),\
                            density   = Density(1.0e-0,"kg/m**3"))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Define the calculation module and set problem data into
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Module initialisation
module = HydraulicModule()
module.setData(problem,mesh = mesh)
module.setTimeDiscretisation(timeStepIntervals = 50)
module.setComponent("elmer")
#
# Module parameters
#
module.setParameter(linearSystemSolver                  = "iterative",\
                    linearSystemIterativeMethod         = "BiCGStab",\
                    linearSystemMaxIterations           = 500,\
                    linearSystemConvergenceTolerance    = 1.e-11,\
                    linearSystemPreconditioning         = "ILU0",\
                    steadyStateConvergenceTolerance     = 1.0e-08,\
                    stabilize = True)
#
module.flowComponent.launch()
t = 0.0
while t < finalTime:
    module.flowComponent.oneTimeStep()
    module.flowComponent.setTimeStep(module.timeStepSizes)
    t = t + min(module.timeStepSizes, finalTime-t)
    pass
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# The velocity is transient, given by the erfc function
#            h = H0*erfc(x/(2sqrt(K0t/S0)))
listOfPoints, charge, velocity = module.getOutput ("velocity")
print " length of points",len(listOfPoints)
ind = 0
for point in listOfPoints:
#    print ind,point
    ind+=1
ind = 0
chargeTocompare = []
for pcharge in charge:
    if ind%3==0:
        chargeTocompare.append(pcharge)
#        print "charge",ind, pcharge
    ind+=1
print "dbg py velocity length ",len(velocity)
def chargeFunction(listOfPoints,time,h0,k0,s0):
    h = []
    k = k0/s0
    for point in listOfPoints:
        h.append( H0*erfc ( point/( 2.*sqrt(k0*time/s0) ) ) )
    return h
lOfP = []
ind = 0
for point in listOfPoints[3:]:
    if ind%3==0: lOfP.append(point[0]) # due to the fact that the mesh is 2D, we consider only 1 point over 3
    ind+=1
#
# Some remarks: The position of points in the center of the mesh is not aligned with those of boundaries. So, some slight
# variations of the charge appear in tne center of the mesh.
#
analyticalCharge = chargeFunction(lOfP, finalTime, initialCharge, hydraulicConductivity, SpecificStorageCoefficient)
print " analytic charge ",analyticalCharge
eps = 2.e-3
ok = 1
ind = 0
normMax = 1.e-10
for head in analyticalCharge:
    normMax = max(abs(head - chargeTocompare[ind]),normMax)
    print " normax: %15.10e  analytical sol.: %15.10e nume. sol:  %15.10e"%(normMax, head, chargeTocompare[ind])
    if normMax> eps:
        raise Exception, " the hydraulic transient test on specific storage with analytical solution failed"
    ind+=1
if ok:
    print "\n \n ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"+\
    " The hydraulic transient test on specific storage with analytical solution is ok\n"+\
    " ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
    pass
