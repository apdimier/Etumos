# -*- coding: utf-8 -*-
"""
        that python module enables to deal with Saturated Hydraulic 
"""
# -- __init__

from commonproblem import CommonBoundaryCondition
from commonproblem import CommonExpectedOutput
from material import Permeability, IntrinsicPermeability
from PhysicalQuantities import Head, HeadGradient, HydraulicFlux, PressureGradient, Temperature
from PhysicalProperties import SpecificHeat, Density
from datamodel import Pressure
from generictools import makeDict
from hydraulicproblem import HydraulicProblem,\
                             InitialCondition,\
                             Source,\
                             ZoneCondition

# -- Verifications ...
from listtools import toList
from verifyproblem import verifySomeOfPhysicalQuantitiesExists
        
class SaturatedHydraulicProblem(HydraulicProblem):
    """
    class for Saturated Hydraulic problems
    """
    def __init__(self, 
                 name,
                 regions,
                 boundaryConditions,
                 initialConditions = None,\
                 temperature = None,\
                 simulationType = None,\
                 calculationTimes = None,\
                 gravity = None,
                 density = None,
                 source = None,
                 intrinsicPermeability = None,\
                 viscosity = None,
                 outputs = None):
        """Problem initialisation with :
        - a name (string)
        - one or several regions (object Region or list of Region)
        - one or several boundary conditions (object BoundaryCondition
          or list of BoundaryCondition)
        - OPTIONAL :
          --> one or several zone conditions (object ZoneCondition
              or list of ZoneCondition)
          --> one or several sources (object Source or list of Source)
          --> a gravity (object Gravity) 
          --> a density (object Density)
          --> a viscosity (object Viscosity)
          --> one or several outputs (object ExpectedOutput or list of
              ExpectedOutput)
          """
        

        # regions treatment
        regions = toList(regions)
        verifySomeOfPhysicalQuantitiesExists([Permeability, IntrinsicPermeability], regions,option = "inclusive")
        
        HydraulicProblem.__init__(self,
                                  name = name,\
                                  saturation = "saturated",\
                                  regions = regions,
                                  boundaryConditions = boundaryConditions,\
                                  initialConditions = initialConditions,\
                                  temperature = temperature,\
                                  simulationType = simulationType,\
                                  calculationTimes = calculationTimes,\
                                  gravity = gravity,\
                                  density = density,\
                                  intrinsicPermeability =intrinsicPermeability,\
                                  viscosity = viscosity,\
                                  source = source,\
                                  outputs = outputs)



    
## - Specific Problem class definition
class BoundaryCondition(CommonBoundaryCondition):
    """
    Specific SaturatedHydraulicProblem BoundaryCondition definition
    """
    def __init__(self, boundary, btype, value, description = None):
        """
        Boundary condition initialisation with :
        - one or several boundaries (a body or a structured mesh element)
        - a boundary condition type.
          It can be Dirichlet,Neumann or Flux
        - a boundary condition value. Value depends of boundary condition type.
          If Dirichlet, value can be Head or Pressure.
          If Neumann, value can be HeadGradient or PressureGradient.
          If Flux, value can be HydraulicFlux.
        """
        boundaryConditionDico = makeDict(Dirichlet=[Head, Pressure, Temperature],
                                         Neumann=[HeadGradient,PressureGradient],
                                         Flux=[HydraulicFlux])

        CommonBoundaryCondition.__init__(self,boundary, btype, value,\
                                         boundaryConditionDico, porosity = None, description = None)

    def getValue(self):
        """
        get boundary conditions value
        """
        return self.value

class ExpectedOutput(CommonExpectedOutput):
    """
    Specific SaturatedHydraulicProblem ExpectedOutput definition.
    """
    def __init__(self, quantity, support, name = None, unit=None,where=None):
        """
          ExpectedOutput initialisation with :
        - an expected output quantity.
          It can be Head, Flowrate, Pressure, Flux, DarcyVelocity, TotalFlux or
          TotalInflux
        - a support. Support depends on wanted quantity.
          If Head, Pressure or DarcyVelocity, support can be bodies,
          StructuredMesh or AbstractPoint
          If Flux, support is a tuple (boundary, zone) (possible type for
          boundary or for zone : Body or StructuredMesh)
          zone orientates the boundary to calculate flux (outgoing normal positive)
          If TotalFlux or TotalInflux, support can be bodies or StructuredMesh
        - OPTIONAL :
          --> a name (string). If none given, name is set to quantity
          --> a unit (string)
          --> where (string) : represents expected output localisation. It's only
                               available is quantity is Flowrate or DarcyVelocity
                               and support is bodies or StructuredMesh and on all elements.
                               Value can be center, face or border
        """
        
        alltype = ['Head', 'Pressure',
                   'Flux', 'DarcyVelocity','TotalFlux',
                   'TotalInflux']
        facetype = ['DarcyVelocity']
        CommonExpectedOutput.__init__(self,alltype,facetype,quantity, support, name , unit,None,where)


