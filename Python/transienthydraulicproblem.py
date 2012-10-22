"""Transient Hydraulic Model 

That module is the base of a Transient Hydraulic problem
"""
# -- __init__
from PhysicalQuantities import HydraulicFlux, Pressure, PressureGradient
from generictools import makeDico
from hydraulicproblem import HydraulicProblem
from commonproblem import CommonBoundaryCondition
from commonproblem import CommonInitialCondition,CommonExpectedOutput
from hydraulicproblem import ZoneCondition, Source
from listtools import toList
from typechecktools import verifyExists
from verifyproblem import verifyPhysicalQuantityExists

# -- Use for verifications

class TransientHydraulicProblem(HydraulicProblem):
    """
    Transient Hydraulic problem class
    """
    def __init__(self,
                 name,\
                 regions,\
                 calculationTimes,\
                 fluidCompressibility,\
                 gravity,\
                 density,\
                 viscosity,\
                 boundaryConditions,\
                 initialConditions = None,\
                 zoneConditions = None,\
                 source=None,\
                 densityLaw=None,\
                 viscosityLaw=None,\
                 outputs=None):
        """
        Problem initialisation with :
        
        - a name (string)
        - one or several regions (object Region or list of Region)
        - one or several boundary conditions (object BoundaryCondition
          or list of BoundaryCondition)
        - a fluidCompressibility (object FluidCompressibility)
        - a gravity (object Gravity)
        - a density (object Density)
        - a viscosity (object Viscosity)
        
        - OPTIONAL :
        
          --> one or several zone conditions (object ZoneCondition
              or list of ZoneCondition)
          --> one or several sources (object Source or list of Source)
          --> one or several outputs (object ExpectedOutput or list of
              ExpectedOutput)
          --> a density law  (object DensityLaw)
          --> a viscosity law (object ViscosityLaw)
        """
        #
        # regions treatment
        #
        regions = toList(regions)
        from datamodel import MatrixCompressibilityFactor
        from datamodel import HydraulicPorosity
        from datamodel import IntrinsicPermeability
        verifyPhysicalQuantityExists([MatrixCompressibilityFactor,HydraulicPorosity,IntrinsicPermeability], regions)

        HydraulicProblem.__init__(self,'transient',name, regions,                 
                                  boundaryConditions,calculationTimes,
                                  gravity,density,viscosity,
                                  initialConditions,zoneConditions,
                                  source,outputs)
        
        #
        # fluidCompressibility treatment
        #
        if fluidCompressibility:
            from datamodel import FluidCompressibility
            if not isinstance(fluidCompressibility, FluidCompressibility):
                raise Exception, " fluid compressibility must be an instance of the FluidCompressibility class"
            pass
        self.fluidCompressibility = fluidCompressibility

        # densityLaw treatment
        if densityLaw:
            from datamodel import DensityLaw
            if not isinstance(densityLaw, DensityLaw):
                raise Exception, " density must be an instance of the densityLaw class"
        self.densityLaw = densityLaw


        # viscosityLaw treatment
        if viscosityLaw:
            from datamodel import ViscosityLaw
            if not isinstance(viscosityLaw, ViscosityLaw):
                raise Exception, " the viscosity law must be an instance of the ViscosityLaw class"
        self.viscosityLaw = viscosityLaw
            
        #
        # Consistance problem verification
        #
        #msg='verification density,gravity,fluidCompressibility,viscosity'
        verifyExists(self.density,self.gravity,\
                     self.fluidCompressibility,self.viscosity)

        return

    def getDensityLaw(self):
        """
        get TransientHydraulicProblem density law
        """
        return self.densityLaw
    
    
    def getViscosityLaw(self):
        """
        get TransientHydraulicProblem viscosity law
        """
        return self.viscosityLaw
    
    def getfluidCompressibility(self):
        """
        get HydraulicProblem fluidcompressibility
        """
        return self.fluidCompressibility        
    pass

## - Specific Problem class definition
class BoundaryCondition(CommonBoundaryCondition):
    """Specific TransientHydraulicProblem BoundaryCondition definition"""
    
    def __init__(self, boundary, type,value, description = None):
        """Boundary condition initialisation with :
        - one or several boundaries 
        - a boundary condition type.
          It can be Dirichlet,Neumann,Mixed or Flux
        - a boundary condition value. Value depend of boundary condition type.
          If Dirichlet, value can be Pressure.
          If Neumann, value can be PressureGradient.
          If Flux, value can be HydraulicFlux.
          If Mixed, value can be PressureMixed.
        """
        from datamodel import Pressure, PressureGradient, PressureMixed
        from datamodel import HydraulicFlux
        bcdict=makeDico(Dirichlet=[Pressure],Neumann=[PressureGradient],\
                        Mixed=[PressureMixed],Flux=[HydraulicFlux])
        CommonBoundaryCondition.__init__(self, boundary, type, value, bcdict, description)
        

class InitialCondition(CommonInitialCondition):
    """Specific ExtentedTransportProblem InitialCondition definition"""
    
    def __init__(self, zone, value):
        """Initial condition initialisation with
        - one or several zones         - a value of type Pressure
        """
        from datamodel import Pressure
        CommonInitialCondition.__init__(self,zone, value,[Pressure])
        


class ExpectedOutput(CommonExpectedOutput):
    """Specific TransientHydraulicProblem ExpectedOutput definition. A field, a set of fields or a value"""
    
    def __init__(self, quantity, support, name = None, unit=None,timeSpecification=None,where=None):
        """ExpectedOutput initialisation with :
        - an expected output quantity.
          It can be Flowrate, Pressure, Flux, DarcyVelocity, TotalFlux or TotalInflux
        - a support. Support depends on wanted quantity.
          If Pressure or DarcyVelocity, support can be StructuredMesh or AbstractPoint
          If Flux, support is a tuple (boundary, zone) (possible type for
          boundary or for zone : StructuredMesh)
          If TotalFlux or TotalInflux, support can be StructuredMesh
        - OPTIONAL :
          --> a name (string). If none given, name is set to quantity
          --> a unit (string)
          --> where (string) : represents expected output localisation. It's only
                               available is quantity is Pressure or DarcyVelocity
                               and support is StructuredMesh and on all elements.
                               Value can be center, face or border
          --> timeSpecification (TimeSpecification) : define times to get expected output
        """
        alltype = ['Pressure','Flux', 'DarcyVelocity','TotalFlux','TotalInflux']
        facetype = ['DarcyVelocity']
        CommonExpectedOutput.__init__(self,alltype,facetype,quantity, support, name , unit,timeSpecification,where)
        
