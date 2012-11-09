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

ProblemName  = "testHydraulic"          # Phreeqc file 

meshFileName = "SDarcy1d.msh"
mesh = Mesh2D(meshFileName)
numberOfVertices = mesh._getNumberOfVertices()
print numberOfVertices
#print mesh.physicalBodyNames.keys()
print mesh.getBodies()
columnBody    = mesh.getBody('domain')
inletBoundary = mesh.getBody('inlet')
print " script inletBoundary ",inletBoundary.getBodyName()
outletBoundary = mesh.getBody('outlet')
print " script outletBoundary ",outletBoundary.getBodyName()
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
HeadLeft = 100.
HeadRight = 20.

#---------------------------------------------------------------------
#   Begin : First, set problem type
#---------------------------------------------------------------------


#---------------------------------------------------------------------
#  Definition of Material and Regions associated
#---------------------------------------------------------------------

columnMaterial = Material(name="Mat", hydraulicconductivity = HydraulicConductivity(value = K),\
                          porosity = Porosity(value = 1.0))

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
                            outputs                  = []
                           )

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
module.run()

#
#
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
points, charge, velocity = module.getOutput("velocity")
module.writeVelocityPlot()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

dH = HeadLeft - HeadRight
L = 20.0
print " arg ",HeadLeft,HeadRight,dH
f = LinearFunction2D([(HeadRight -HeadLeft)/L, 0., HeadLeft])
analyticalField = []
for point in coords:
    analyticalField.append(f.eval(point))
#~~~~~~~~~~~~~~~~~~
#  Error estimation
#~~~~~~~~~~~~~~~~~~
print ' '
print "~~~~~~"
print "Head :"
print "~~~~~~"
eps = 1.e-5
diff = 1.e-20
for i in range(len(analyticalField)):
    diff = max(diff,abs(analyticalField[i] - charge[i]))
#    print 'Difference on Linf norm for point  ' , i+1 , '=' ,abs(diff), '%'
    if diff*100 > eps:
        okch = 0
        print 'difference on Linf norm is too high :',abs(diff), '%'
        print 'test on headings  :N OK, for point ',i+1, 'the results are greater than  :',eps,analyticalField[i],charge[i]
if diff < eps:
    okch = 1
    print 'test on headings  : OK, the results are better than  :',eps*100,'%'

print '~~~~~~~~~~~'
print 'Velocities:'
print '~~~~~~~~~~~'
diff = 1.e-20
analyticalVelocity = -K*(HeadRight -HeadLeft)/L
for i in range(len(velocity)):
    diff = max(diff,abs(analyticalVelocity - velocity[i][0]))
    if diff*100>eps:
        okvit= 0
        message =  "differences to high for velocity:, test is ko"
        raise Exception,message

if diff < eps:
    okvit = 1
    print 'tests for the two components of the velocity  : OK the results are better than  :',eps*100,'%'
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# End of the saturated Dirichlet hydraulic problem
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if (okch and okvit):
    print "\n \n ~~~~~~~~~~~~~~~~~~~ Test case is ok ~~~~~~~~~~~~~~~\n"
    pass
else:
    raise Exception, "the test case failed to converge to the right solution"

