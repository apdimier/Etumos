#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# The problem  is saturated 1D
#
# We use Dirichlet boundary conditions, the charge is linear,
#
# the velocity field constant
#
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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

meshFileName = "tuy.msh"
mesh = Mesh2D(meshFileName)
numberOfVertices = mesh._getNumberOfVertices()
#print numberOfVertices
#print mesh.physicalBodyNames.keys()
#print mesh.getBodies()
columnBody    = mesh.getBody('domain')
inletBoundary = mesh.getBody('inlet')
#print " script inletBoundary ",inletBoundary.getBodyName()
outletBoundary = mesh.getBody('outlet')
#print " script outletBoundary ",outletBoundary.getBodyName()
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
#
HeadLeft  =  20.
HeadRight = 100.

#---------------------------------------------------------------------
#   Begin : First, set problem type
#---------------------------------------------------------------------


#---------------------------------------------------------------------
#  Definition of Material and Regions associated
#---------------------------------------------------------------------

columnMaterial = Material(name="Mat",hydraulicconductivity=HydraulicConductivity(value = K), porosity = Porosity(value = 1.0))

#~~~~~~~~~~~
#~ Regions ~
#~~~~~~~~~~~
columnRegion = Region (support = columnBody, material = columnMaterial)
    
inletRegion  = Region (support = inletBoundary,  material = columnMaterial)
outletRegion = Region (support = outletBoundary, material = columnMaterial)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Definition of Boundary Conditions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
bCLeft   = BoundaryCondition(inletRegion, 'Dirichlet',Head(HeadLeft,"m"))
bCRight  = BoundaryCondition(outletRegion,'Dirichlet',Head(HeadRight,"m"))
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Definition of Initial Conditions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
columnInit = InitialCondition (columnRegion, Head(1.,"m"))
#---------------------------------------------------------------------
#  Definition of Problem: Insert all previous variables in the problem
#---------------------------------------------------------------------
# Problem definition
problem = HydraulicProblem( name                     = "SteadyHydraulic",
                            saturation               = "saturated",
                            regions                  = [columnRegion,inletRegion,outletRegion],
                            boundaryConditions       = [bCLeft,bCRight],
                            initialConditions        = [columnInit],
                            source                   = None,
                            outputs                  = [])

#---------------------------------------------------------------------
#  Define the calculation module and set problem data into
#---------------------------------------------------------------------
# Module initialisation
module = HydraulicModule()
module.setData(problem,mesh = mesh)
module.setComponent("elmer")
module.flowComponent.setGravityValue(0.0)
#
# Module parameters
#
linearSystemSolver              = "iterative"
linearSystemIterativeMethod     = "BiCGStab"
linearSystemMaxIterations       = 50
linearSystemConvTolerance       = 1.e-11
linearSystemPreconditioning     = "ILU0"
steadyStateConvergenceTolerance = 1.0e-06
stabilize                       = True

module.setParameter(linearSystemSolver = "iterative",\
                    linearSystemIterativeMethod = "BiCGStab",\
                    linearSystemMaxIterations = 500,\
                    linearSystemConvergenceTolerance = 1.e-15,\
                    linearSystemPreconditioning = "ILU0",\
                    steadyStateConvergenceTolerance = 1.0e-15,\
                    fluxParameter = 1.e-03,\
                    stabilize = True)
module.run()
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
points, charge, velocity = module.getOutput("velocity")
module.writeVelocityPlot()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#print "charge ",charge
#print "velocity",velocity
#print "points  ",points

dH = HeadLeft - HeadRight
#~~~~~~~~~~~~
#  Stability
#~~~~~~~~~~~~
velocityLength = len(velocity)
#print velocityLength
if velocityLength != 63:
    raise Exception, "the velocity hasn't been computed on the same mesh"
velocitycomponent = velocity[10]
velocityModule = sqrt(velocitycomponent[0]**2+velocitycomponent[1]**2)
#print velocityModule
if abs(velocityModule - 0.00566265464738) < 1.e-4:
    print "~~~~~~~~~~~~~~~~~~~\nthe test case is ok\n~~~~~~~~~~~~~~~~~~~",velocityModule
else:
    print " error ",abs(velocityModule - 0.00566265464738),velocityModule
    raise Exception, "the test case is ko"
