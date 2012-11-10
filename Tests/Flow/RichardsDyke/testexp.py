"""
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# The problem  is unsaturated. It stems from the richards dyke case 
# of the 6.1 elmer version (Rev: 4955M)
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
from physicallaws import VanGenuchtenSaturation
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Define Mesh, and get Zones and Boundaries from.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
dico = { 'MethodChoice' : 'FE'}

ProblemName  = "testHydraulic" 

meshFileName = "RichardsDyke.msh"
mesh = Mesh2D(meshFileName)
numberOfVertices = mesh._getNumberOfVertices()
print numberOfVertices
#
print mesh.getBodies()
#
dykeBody = mesh.getBody("dyke")
print " dykeBody ",type(dykeBody)
#
RightWall  = mesh.getBody("RightWall")
print " RightWall ",type(RightWall)
print RightWall.body,type(RightWall.body)
print RightWall.bodyName
#
LeftWall   = mesh.getBody("LeftWall")
print "LeftWall",type(LeftWall)
#
WetRight   = mesh.getBody("WetRight")
print " Wet Right ",type(WetRight)
#
WetLeft   = mesh.getBody('WetLeft')
print " WetLeft ",type(WetLeft)
#
Bottom    = mesh.getBody('Bottom')
print " Bottom ",type(Bottom)
#
coords    = mesh.getNodesCoordinates()
#
K = 5.e-7
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
alpha = 100.0
n = 1.4
m = 0.3
residualWaterContent = 0.23
saturatedWaterContent = 0.55
columnMaterial = Material(name="Mat",hydraulicconductivity = HydraulicConductivity(value = K),\
                          porosity = Porosity(value = 1.0),\
                          saturatedWaterContent = SaturatedWaterContent(saturatedWaterContent),\
                          residualWaterContent = ResidualWaterContent(residualWaterContent),\
                          saturationLaw = ExponentialSaturation(alpha, 0.1, 2.0))
print columnMaterial
raw_input("Material")
#~~~~~~~~~~~
#~ Regions ~
#~~~~~~~~~~~
columnRegion = Region (support = dykeBody, material = columnMaterial)
    
RightWallRegion = Region (support = RightWall, material = columnMaterial)
LeftWallRegion  = Region (support = LeftWall,  material = columnMaterial)
WetRightRegion  = Region (support = WetRight,  material = columnMaterial)
WetLeftRegion   = Region (support = WetLeft,   material = columnMaterial)
BottomRegion    = Region (support = Bottom,    material = columnMaterial)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Definition of Boundary Conditions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
WetLeftHead    = 8.5
WetRightHead     = 6.0


WetRightBoundary = BoundaryCondition(WetRightRegion,  'Dirichlet',      Head(WetRightHead, "m"))
WetLeftBoundary = BoundaryCondition(WetLeftRegion,    'Dirichlet',      Head(WetLeftHead, "m"))
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Definition of Initial Conditions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
columnInit = InitialCondition (columnRegion, Head(1.,"m"))
#---------------------------------------------------------------------
#  Definition of Problem: Insert all previous variables in the problem
#---------------------------------------------------------------------
# Problem definition
problem = HydraulicProblem( name                     = "SteadyHydraulic",
                            saturation               = "unsaturated",
                            regions                  = [columnRegion, RightWallRegion, LeftWallRegion,\
                                                        WetRightRegion, WetLeftRegion, BottomRegion],
                            boundaryConditions       = [WetRightBoundary, WetLeftBoundary],
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
# Now the parameters for the non linear solver
#
module.setParameter(nonlinearSystemMaxIterations = 101,\
                    nonlinearSystemConvergenceTolerance = 1.1e-6,\
                    nonlinearSystemRelaxationFactor = 1.0)

#
module.run()
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
points, charge, velocity = module.getOutput("velocity")
module.writeVelocityPlot()
eps = 1.e-3
ok = 1
for v in velocity:
    norml2 = ((v[0]-45.)**2+(v[1]-80.)**2)**0.5
    if norml2> eps:
        raise Exception, " The test on an isotropic velocity field failed"
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
