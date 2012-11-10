#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# We want to establish here the flow field for the ANR problem
#
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# H = P/(Rho*g) H representing the Head is in meters
#
# Rho   is in kg/m3
# g     is in m/s2
# P     is in Pa (kg/(ms2))
#
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
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Define Mesh, and get Zones and Boundaries from.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
dico = { 'MethodChoice' : 'FE'}

ProblemName  = "testHydraulic" 

meshFileName = "benchmark.msh"
mesh = Mesh2D(meshFileName)
numberOfVertices = mesh._getNumberOfVertices()

mesh = Mesh2D(meshFileName)
numberOfVertices = mesh._getNumberOfVertices()
print " within script numberOfVertices",numberOfVertices
print mesh.getPhysicalBodyNames()

co2Body         = mesh.getBody('co2'); co2Body.getNodesNumber()
print "co2     ",co2Body.getSpaceDimension(),co2Body.getBodyDimension()
inlet2Body         = mesh.getBody('inlet2'); co2Body.getNodesNumber()
print " inlet2 ",inlet2Body.getSpaceDimension(),inlet2Body.getBodyDimension()

waterBody      = mesh.getBody('water'); waterBody.getNodesNumber()

rockBody        = mesh.getBody('rock'); rockBody.getNodesNumber()

inlet1Body  = mesh.getBody('inlet1'); print " inlet1, number of nodes ",inlet1Body.getNodesNumber()
inlet2Body  = mesh.getBody('inlet2'); print " inlet2, number of nodes ",inlet2Body.getNodesNumber()
outletBody  = mesh.getBody('outlet'); print " outlet, number of nodes ",outletBody.getNodesNumber()
#
#raw_input(" bodies lecture")
#
coords = mesh.getNodesCoordinates()
#
#
#
K = 1.e-4
#
# The simulation being steady, no storage coefficient need to be specified
#
specificStorage = 100.
density         = 1.
viscosity       = 1.
compressibilityModel = False

#mediumMaterial =        Material (name = "medium", intrinsicpermeability = IntrinsicPermeability(value = 1.0e-13), porosity = Porosity(1))
#rockMaterial =          Material (name = "medium", intrinsicpermeability = IntrinsicPermeability(value = 1.0e-15), porosity = Porosity(0.2))
#
HeadInlet1 =   0.
HeadInlet2 = 200.
HeadOutlet =  150.
#
#---------------------------------------------------------------------
#   Begin : First, set problem type
#---------------------------------------------------------------------
#
#
#---------------------------------------------------------------------
#  Definition of Material and Regions associated
#---------------------------------------------------------------------
#
Kmedium = 1.e-12        # in m2
Krock   = 1.e-15        # in m2

mu      = 1.e-3 # Pa.s ( kg /(m*s) )
rho     = 1000  # kg/m3
g       = 9.78  # m/s**2
coef = rho * g / mu
Kmedium = Kmedium * coef
Krock   = Krock * coef * 0.2

mediumMaterial  = Material (name="Mat",hydraulicconductivity=HydraulicConductivity(value = Kmedium), porosity = Porosity(value = 1.0))

rockMaterial    = Material (name="Mat",hydraulicconductivity=HydraulicConductivity(value = Krock), porosity = Porosity(value = 1.0))

inlet1Material  = Material (name="Mat",hydraulicconductivity=HydraulicConductivity(value = Kmedium), porosity = Porosity(value = 1.0))
inlet2Material  = Material (name="Mat",hydraulicconductivity=HydraulicConductivity(value = Kmedium), porosity = Porosity(value = 1.0))
#
#~~~~~~~~~~~
#~ Regions ~
#~~~~~~~~~~~
#
waterRegion     = Region (support = waterBody,  material =      mediumMaterial)
co2Region       = Region (support = co2Body,    material =      mediumMaterial)
rockRegion      = Region (support = rockBody,   material =      rockMaterial)
    
inlet1Region    = Region (support = inlet1Body, material =      inlet1Material)
inlet2Region    = Region (support = inlet2Body, material =      inlet2Material)
outletRegion    = Region (support = outletBody, material =      mediumMaterial)
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Definition of Boundary Conditions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
rho     = 1000.0        # kg/m3
gravity = 9.8           # m/s2
Pressure1 = 110.e+5
HeadInlet1 = 110.e+5/(rho*gravity)
HeadInlet2 = 105.e+5/(rho*gravity)
HeadOutlet = 100.e+5/(rho*gravity)
#
bCLeft1   = BoundaryCondition(inlet1Region, 'Dirichlet', Head(HeadInlet1, "m"))
bCLeft2   = BoundaryCondition(inlet2Region, 'Dirichlet', Head(HeadInlet2, "m"))
bCRight   = BoundaryCondition(outletRegion, 'Dirichlet', Head(HeadOutlet, "m"))
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Definition of Initial Conditions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
waterInit =     InitialCondition (waterRegion, Head(0.,"m"))
co2Init =       InitialCondition (co2Region,   Head(0.,"m"))
rockInit =      InitialCondition (rockRegion,  Head(0.,"m"))
#
#---------------------------------------------------------------------
#  Definition of Problem: Insert all previous variables in the problem
#---------------------------------------------------------------------
#
# Problem definition
#
problem = HydraulicProblem( name                     = "SteadyHydraulic",
                            saturation               = "saturated", 
                            regions                  = [inlet1Region, inlet2Region, outletRegion, rockRegion, co2Region, waterRegion],
#                            regions                  = [waterRegion, co2Region, rockRegion, inlet2Region, outletRegion],
#                            boundaryConditions       = [bCLeft2, bCRight],
                            boundaryConditions       = [bCLeft1, bCLeft2, bCRight],
                            initialConditions        = [rockInit, co2Init, waterInit],
                            source                   = None,
                            outputs                  = [])
#
#---------------------------------------------------------------------
#  Define the calculation module and set problem data into
#---------------------------------------------------------------------
#
# Module initialisation
module = HydraulicModule()
module.setData(problem,mesh = mesh)
module.setComponent("elmer")
#
# Module parameters
#
linearSystemSolver              = "iterative"
linearSystemIterativeMethod     = "BiCGStab"
linearSystemMaxIterations       = 100
linearSystemConvTolerance       = 1.e-11
linearSystemPreconditioning     = "ILU0"
steadyStateConvergenceTolerance = 1.0e-08
stabilize                       = True

module.setParameter(linearSystemSolver = "iterative",\
                    linearSystemIterativeMethod = "BiCGStab",\
                    linearSystemMaxIterations = 100,\
                    linearSystemConvergenceTolerance = 1.e-15,\
                    linearSystemPreconditioning = "ILU0",\
                    steadyStateConvergenceTolerance = 1.0e-08,\
                    stabilize = True)
module.run()
#
#
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
points, charge, velocity = module.getOutput("velocity")
module.writeVelocityPlot()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#print "charge ",charge
ok = 1
#
# The three first elements of the velocity are compared with previously obtained ones
#
#
prev = [1.9711231866e-09, 1.0329601084e-09, 0.0], [3.7274883058e-10, -2.7540410988e-10, 0.0], [3.7224700379e-10, -2.7653964319e-10, 0.0]
if prev[0] == velocity[0] and prev[1] == velocity[1] and prev[2] == velocity[2]:
    pass
else:
    ok = 0
#print "points  ",points
print '~~~~~~~~~~~'
print 'Velocities:'
print '~~~~~~~~~~~'
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# End of the ANR Benchmark hydraulic problem
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print "value of ok ",ok,velocity[0], velocity[1]
if (ok):    
    print "\n \n ~~~~~~~~~~~~~~~~~~~ Test case is ok ~~~~~~~~~~~~~~~\n"
    pass
else:
    raise Exception, "the test case failed to converge"

