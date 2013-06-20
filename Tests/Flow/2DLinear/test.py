"""#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# The problem  is saturated 2D: file SDarcy2d.geo
#
# We use Dirichlet boundary conditions, the charge is linear,
# the material itself being isotropic Kx = 1., Ky = 1.
# A second test case with K orthotropic Kx = 1., Ky = 3./4.
# should be implemented
#
# Boundaries are:
#   
#       AB P(X) = -45x + 30.5
#       BC P(X) = -80y + 18.0
#       CD P(X) = -45x + 14.5
#       DA P(X) = -80y + 27.0 
#
# The velocity field is constant V(45,80)
#
# the geometry is made of a square ABCD, point positions being:
#
#       A (-0.1,-0.1)
#
#       B ( 0.1,-0.1)
#
#       C ( 0.1, 0.1)
#
#       D (-0.1, 0.1)
#
#
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
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
from functions import LinearFunction
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Define Mesh, and get Zones and Boundaries from.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
dico = { 'MethodChoice' : 'FE'}

ProblemName  = "testHydraulic" 

meshFileName = "SDarcy2d.msh"
mesh = Mesh2D(meshFileName)
numberOfVertices = mesh._getNumberOfVertices()
print numberOfVertices
#
print mesh.getBodies()
#
columnBody    = mesh.getBody('domain')
#
AB = mesh.getBody('AB')
print " AB "
#
BC = mesh.getBody('BC')
print " BC "
#
CD = mesh.getBody('CD')
print " CD "
#
DA = mesh.getBody('DA')
print " DA "
#
coords = mesh.getNodesCoordinates()
#
K = 1.e-0
#
# The simulation being steady, no storage coefficient need to be specified
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
columnMaterial = Material(name="Mat",hydraulicconductivity=HydraulicConductivity(value = K), porosity = Porosity(value = 1.0))
#~~~~~~~~~~~
#~ Regions ~
#~~~~~~~~~~~
columnRegion = Region (support = columnBody, material = columnMaterial)
    
ABRegion = Region (support = AB, material = columnMaterial)
BCRegion = Region (support = BC, material = columnMaterial)
CDRegion = Region (support = CD, material = columnMaterial)
DARegion = Region (support = DA, material = columnMaterial)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Definition of Boundary Conditions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ABHead = LinearFunction([30.5, -45.])
BCHead = LinearFunction([18.0, 0., -80.])
CDHead = LinearFunction([14.5, -45.])
DAHead = LinearFunction([27.0, 0., -80.])

ABBoundary = BoundaryCondition(ABRegion, 'Dirichlet', Head(ABHead, "m"))
BCBoundary = BoundaryCondition(BCRegion, 'Dirichlet', Head(BCHead, "m"))
CDBoundary = BoundaryCondition(CDRegion, 'Dirichlet', Head(CDHead,"m"))
DABoundary = BoundaryCondition(DARegion, 'Dirichlet', Head(DAHead,"m"))
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
                            regions                  = [columnRegion, ABRegion, BCRegion, CDRegion, DARegion],
                            boundaryConditions       = [ABBoundary, BCBoundary, CDBoundary, DABoundary],
                            initialConditions        = [columnInit],
                            source                   = None,
                            outputs                  = [],
                            viscosity                = Viscosity(1.0e+0,"kg*m/s" ),
                            density                  = Density  (1.0e+0,"kg/m**3"))

#---------------------------------------------------------------------
#  Define the calculation module and set problem data into
#---------------------------------------------------------------------
# Module initialisation
module = HydraulicModule()
module.setData(problem,mesh = mesh)
module.setComponent("elmer")
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
                    linearSystemMaxIterations = 100,\
                    linearSystemConvergenceTolerance = 1.e-15,\
                    linearSystemPreconditioning = "ILU0",\
                    steadyStateConvergenceTolerance = 1.0e-08,\
                    stabilize = True)
#
module.run()
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
points, charge, velocity = module.getOutput("velocity")
#print velocity
eps = 1.e-3
ok = 1
for v in velocity:
    norml2 = ((v[0]-45.)**2+(v[1]-80.)**2)**0.5
    if norml2> eps:
        raise Exception, " The test on an isotropic velocity field failed: "+str(norml2)
if ok:
    print "\n \n ~~~~~~~~~~~~~~~~~~~ The test case on isotropic velocity is ok ~~~~~~~~~~~~~~~\n"
    pass
else:
    raise Exception, "the test case failed to converge"
module.writeVelocityPlot()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#print "charge ",charge
#print "velocity",velocity
#print "points  ",points
