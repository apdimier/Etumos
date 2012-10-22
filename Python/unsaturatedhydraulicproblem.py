"""Unsaturated Hydraulic Model 

All that is needed to define an Unsaturated Hydraulic problem"""

# -- __init__
from commonproblem import CommonBoundaryCondition
from commonproblem import CommonInitialCondition,CommonExpectedOutput
from PhysicalProperties import SaturationDegree
from PhysicalQuantities import Head, HeadGradient, HydraulicFlux, Pressure, PressureGradient
from generictools import makeDico
from hydraulicproblem import HydraulicProblem
from hydraulicproblem import ZoneCondition, Source
from listtools import toList
### -- Verifications .
from verifyproblem import verifyPhysicalQuantityExists, verifySomeOfPhysicalQuantitiesExists


class UnsaturatedHydraulicProblem(HydraulicProblem):
    
    def __init__(self, name, regions,calculationTimes,
                 gravity,
                 density,
                 viscosity,                 
                 boundaryConditions,
                 initialConditions = None,
                 zoneConditions = None,
                 source=None,
                 outputs=None,
                 defaultBoundaryCondition=None,
                 defaultInitialCondition=None):
        """Problem initialisation with :
        - a name (string)
        - one or several regions (object Region or list of Region)
        - one or several boundary conditions (object BoundaryCondition
          or list of BoundaryCondition)
        - a gravity (object Gravity)
        - a density (object Density)
        - a viscosity (object Viscosity)
        - OPTIONAL :
          --> one or several zone conditions (object ZoneCondition
              or list of ZoneCondition)
          --> one or several sources (object Source or list of Source)
          --> one or several outputs (object ExpectedOutput or list of
              ExpectedOutput)
          --> a tuple to define default boundary condition.
              It will be used if boundaryConditions defined in the problem
              don't cover entire boundaries.
              First element of tuple contains a string which represent
                default boundary condition type ('Dirichlet' or 'Neumann' For example)
              Second Element represent a PhysicalQuantity with default Boundary Condition Value
                Head(0.) or HeadGradient(0.) for example
          --> a PhysiqualQuantity to define value of default initial condition
        """


        # regions treatment
        regions = toList(regions)
        from datamodel import Permeability, IntrinsicPermeability
        from datamodel import MatrixCompressibilityFactor,Porosity,LiquidResidualSaturation
        verifySomeOfPhysicalQuantitiesExists([Permeability, IntrinsicPermeability], regions,option='exclusive')
        verifyPhysicalQuantityExists([MatrixCompressibilityFactor,Porosity,LiquidResidualSaturation], regions)

        HydraulicProblem.__init__(self,'unsaturated',name, regions,boundaryConditions,calculationTimes,
                                  gravity,density,viscosity,
                                  initialConditions,zoneConditions,
                                  source,outputs,defaultBoundaryCondition,defaultInitialCondition)
        
        # Consistance problem verification
        if self.density == None: raise Exception, " you have to define a density before launching the problem "

        return
    
    pass

## - Specific Problem class definition
class BoundaryCondition(CommonBoundaryCondition):
    """Specific UnsaturatedHydraulicProblem BoundaryCondition definition"""
    def __init__(self, boundary, type, value, description = None):
        """Boundary condition initialisation with :
        - one or several boundaries (object Support or StructuredMesh
          or list of Supports)
        - a boundary condition type.
          It can be Dirichlet,Neumann or Flux
        - a boundary condition value. Value depend of boundary condition type.
          If Dirichlet, value can be Head, Pressure or SaturationDegree.
          If Neumann, value can be HeadGradient or PressureGradient.
          If Flux, value can be HydraulicFlux.
        """
        bcdict = makeDico (Dirichlet=[Head,Pressure,SaturationDegree],\
                           Neumann=[HeadGradient,PressureGradient],\
                           Flux=[HydraulicFlux])
        CommonBoundaryCondition.__init__(self,boundary, type, value, bcdict, description)
        return
    
    pass

class InitialCondition(CommonInitialCondition):
    """Specific unsaturatedHydraulicProblem InitialCondition definition"""    
    def __init__(self, zone, value):
        """Initial condition initialisation with
        - one or several zones (object Support or StructuredMesh
          or list of Support)
        - a value of type Head, Pressure or SaturationDegree
        """
        from datamodel import Head,Pressure,SaturationDegree
        CommonInitialCondition.__init__(self,zone, value,[Head,Pressure,SaturationDegree])
        return

class ExpectedOutput(CommonExpectedOutput):
    """Specific TransientHydraulicProblem ExpectedOutput definition. A field, a set of fields or a value"""
    def __init__(self, quantity, support, name = None, unit=None,timeSpecification=None,where=None,save='memory'):
        """ExpectedOutput initialisation with :
        - an expected output quantity.
          It can be Head, Pressure, Flux, DarcyVelocity, TotalFlux, TotalInflux or Saturation
        - a support. Support depends on wanted quantity.
          If Flowrate, Pressure, Saturation or DarcyVelocity, support can be Support, StructuredMesh or AbstractPoint
          If Flux, support is a tuple (boundary, zone) (possible type for
          boundary or for zone : Support or StructuredMesh)
          If TotalFlux or TotalInflux, support can be Support or StructuredMesh
        - OPTIONAL :
          --> a name (string). If none given, name is set to quantity
          --> a unit (string)
          --> where (string) : represents expected output localisation. It's only
                               available is quantity is DarcyVelocity and support is Support
                               or StructuredMesh and on all elements.
                               Value can be center, face or border
          --> timeSpecification (TimeSpecification) : define times to get expected output
        """
        alltype = ['Head', 'Pressure',
                   'Flux', 'DarcyVelocity','TotalFlux',
                   'TotalInflux','Saturation']
        facetype = ['DarcyVelocity']
        CommonExpectedOutput.__init__(self,alltype,facetype,quantity, support, name , unit,timeSpecification,where,[],save) 
