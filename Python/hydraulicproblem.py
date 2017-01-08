# -*- coding: utf-8 -*-
""" 
Hydraulic is defined here.
It can be steady or transient,
saturated or unsatured. 
Arguments are analysed and the regime determined. 
"""

# -- __init__

# -- Verifications .
from __future__ import absolute_import
from __future__ import print_function
from generictools import isInstance, makeDico, memberShip

from cartesianmesh import CartesianMesh

from typechecktools import verifyClassList

from types import FloatType

from listtools import toFloatList, toList

from verifyproblem import verifyZoneBoundaryConditionisUnique
from verifyproblem import intrinsicPermeabilityCheck, regionPhysicalQuantitiesCheck, verifyPressureBoundaryConditions,\
                          verifySomeOfPhysicalQuantitiesExists
from commonproblem import CommonBoundaryCondition,\
                          CommonInitialCondition,\
                          CommonSource,\
                          CommonZoneCondition
from commonmodel import Region
from vector import V as Vector

from PhysicalProperties import Density,\
                               IntrinsicPermeability,\
                               Viscosity
from PhysicalQuantities import FlowRate,\
                               Head,\
                               HeadGradient,\
                               HydraulicFlux,\
                               PressureGradient,\
                               Pressure,\
                               SaturationLevel
import types

class HydraulicProblem(object):
    """
    A hydraulic problem can be 
    
        steady or time dependant
        
        saturated or undersaturated
        
        It must be defined through charge or pressure at boundary conditions.
        
        The consistancy of boundary conditions will be checked.
        
        Simulation is transient if calculationTimes are given. They can be combined with the transient argument.
        But without the calculationTimes list, the simulation is steady.
        
        05/05/2011 introduction of Richards solver (steady) with the standard Elmer (V. 6.1) Richards dyke test case
        
    """
    def __init__(self,\
                 name,\
                 saturation,\
                 regions,\
                 boundaryConditions,\
                 initialConditions = None,\
                 state = None,\
                 simulationType = None,\
                 calculationTimes = None,\
                 gravity = None,\
                 density = None,\
                 source = None,\
                 intrinsicPermeability = None,\
                 viscosity = None,\
                 outputs = None,\
                 description = None):
                 
        """
        Problem initialisation with :
        
        - name :                name given by the user to the problem

        - saturation:           determines the state to be modelled.
                                Depending on the way the problem is defined, it can be modified.
        - boundary conditions:  
        - initial conditions:   
        - regions:              all regions covering the entire mesh. Regions make up a partition of the mesh
                                
        - gravity:                  default None
        
        - density:                  default None
        
        - intrinsicPermeability:    default None
        
        - viscosity:                default None
        
        - sources                   default None
        
        - outputs                   default None

        """
                                                                                            # 
                                                                                            # name should be a string
                                                                                            #
        if type(name) != bytes:
            raise TypeError("name should be a string ")
        self.name = name
                                                                                            #
                                                                                            # saturation
                                                                                            #
        self.problemType = "saturated"
        self.saturation = "saturated"
        if type(saturation) == bytes:
            if saturation == "unsaturated" or saturation.lower()=="no":
                self.saturation = "unsaturated"
                self.problemType = "unsaturated"
                pass
            pass
                                                                                            #
                                                                                            # regions treatment
                                                                                            #
        verifyClassList(regions, Region)
        regions_zones = [region.getZone() for region in regions]
        self.regions = regions
                                                                                            #
                                                                                            # gravity treatment
                                                                                            #
        check = -1
        if gravity:
            memberShip(gravity, Gravity)
            try:
                value=gravity.getValue()
                if type(value) not in [float, int]:
                    raise TypeError(" value should be a float or an int ")
                meshdim = regions_zones[0].getSpaceDimension()
                value=[0.]*meshdim
                value[-1] = 9.81
                if meshdim == 2: value.append(0.)
                gravity=Vector(value)
            except:
                pass
            pass
        else:            
            meshdim = regions_zones[0].getSpaceDimension()
            value=[0.]*meshdim
            value[-1] = 9.81
            if meshdim == 2: value.append(0.)
            gravity=Vector(value)
            print(value)
            pass
        self.gravity = gravity
                                                                                            #
                                                                                            # density treatment
                                                                                            #        
        if density:
            if type(density) == FloatType: density = Density(density, 'kg/m**3') 
            memberShip(density, Density)
            check = 2*check
            pass
        self.density = density
                                                                                            #
                                                                                            # intrinsicPermeability treatment
                                                                                            # the introduction of the intrinsic permeability
                                                                                            # is related to the introduction of the openfoam solver.
                                                                                            #        
        #print (intrinsicPermeability)
        #print (type(intrinsicPermeability))
        #raw_input("problem type intrinsicPermeability")
        if intrinsicPermeability:
            if type(intrinsicPermeability) == FloatType: intrinsicPermeability = IntrinsicPermeability(intrinsicPermeability, 'm**2') 
            memberShip(intrinsicPermeability, IntrinsicPermeability)
            check = 2*check
            pass
        self.intrinsicPermeability = intrinsicPermeability
        #print (intrinsicPermeability)
        #print (type(intrinsicPermeability))
        #raw_input("problem type intrinsicPermeability b")
                                                                                            #
                                                                                            # viscosity treatment
                                                                                            #
        #print(" dbg viscosity ",viscosity);#raw_input()
        if viscosity:
            if type(viscosity) == FloatType: viscosity = Viscosity(viscosity, 'kg/m/s') 
            memberShip(viscosity, Viscosity)
            check = 3*check
            pass
        else:
            viscosity = Viscosity(1.0, 'kg/m/s')
            pass
        #print(" dbg viscosity 1",viscosity);#raw_input()
        self.viscosity = viscosity
                                                                                            #
                                                                                            # Do we use intrinsic permeability
                                                                                            #
        if self.saturation == "unsaturated": intrinsicPermeabilityCheck(self.regions, check)
                                                                                            #        
                                                                                            # times definition
                                                                                            #        
        self.simulationType = simulationType
#        #raw_input("calculation times ")
        if calculationTimes:
            self.calculationTimes = calculationTimes
            self.simulationType = "Transient"
            pass
        else:
            self.calculationTimes = None
            self.simulationType = "Steady"
            pass
        self.steadyState = 1 
        if self.calculationTimes!= None:
            if type(calculationTimes) != list:
                raise TypeError(" calculationTimes should be a list ")
            CalculationTimes=toFloatList( self.calculationTimes)
            #
            for item in CalculationTimes:
                if type(item) != float:
                    raise TypeError(" item should be a float ")
                pass
            self.calculationTimes = sorted( CalculationTimes)
#            print self.calculationTimes;#raw_input(" within the loop, calculation times are printed here")
            self.steadyState = 0                                                            # The simulation is transient
            pass
                                                                                            #
                                                                                            # Permeability
                                                                                            #
        if self.saturation == "unsaturated":
            #
            # only Richards for the moment
            #
            pass
            #raise Exception, " for the moment, undersaturated flows are not implemented"
            #regionPhysicalQuantitiesCheck([Permeability, IntrinsicPermeability], regions)
                                                                                            #        
                                                                                            # boundaryConditions treatment
                                                                                            #        
        self.defaultBC = None
        boundaryConditions = toList(boundaryConditions)
        print(" problem type ",self.problemType)
#        raw_input(str(self.problemType))
        print(dir(boundaryConditions[0])) 

        # verification if all boundaries are treated.
        # If some are not, affect a default value (an homogeneous
        # neumann boundarycondition)
        boundaries = []
        for boundaryElement in boundaryConditions:
            boundary = toList(boundaryElement.getBoundary())
            for bound in boundary: boundaries.append(bound)
            pass
        # In case of structured mesh, not all the boundary could be defined for the problem
        if self.defaultBC:
            if not self.density:
                self.density = Density(1.)
                pass
            if not self.gravity:
                mesh_dim=regions[0].getZone().getMesh().getSpaceDimension()
                if mesh_dim==2: self.gravity=Gravity(Vector(0.,1.))
                elif mesh_dim==3: self.gravity=Gravity(Vector(0.,0.,1.))
                else:
                    raise Warning('Dimension ????')
                pass
            pass        
        # Verification if a pressure condition has been set
        # that density and gravity have been set
#        verifySomeOfPhysicalQuantitiesExists([Permeability, IntrinsicPermeability], regions)
        
#        verifyPressureBoundaryConditions(boundaryConditions, self.density, self.gravity)       
        self.boundaryConditions = boundaryConditions
                                                                                            #
                                                                                            # initialConditions treatment
                                                                                            #        
        self.initialConditions = initialConditions
#        print " initialConditions",initialConditions;raw_input()
                                                                                            #
                                                                                            # source treatment
                                                                                            #
        if source: verifyClassList(source, Source)
        self.source = source
                                                                                            #
                                                                                            # outputs treatment
                                                                                            #
        if outputs:
            outputs1 = toList(outputs)
            verifyClassList(outputs1, _dicoproblem[type].ExpectedOutput)

            if not hasattr(self,'output_names'): self.output_names=[]
            for output in outputs1:
                if output.getName() in self.output_names:
                    msg = '\n\nDifferent outputs should not share the same name.\n'
                    msg+= 'End of the hydraulic problem run.\n\n'
                    raise Warning(msg)
                self.output_names.append(output.getName())
                pass
            pass
            #
        self.outputs = outputs
        return

    def getBoundaryConditions(self):
        """to get the boundary conditions"""
        return self.boundaryConditions

    def getCalculationTimes(self):
        """get calculation times"""
        return self.calculationTimes

    def getDensity(self):
        """get density"""
        return self.density

    def getGravity(self):
        """get gravity"""
        return self.gravity

    def getInitialConditions(self):
        """get initial conditions"""
        return self.initialConditions
        
    def getIntrinsicPermeability(self):
        """get viscosity"""
        return self.intrinsicPermeability

    def getName(self):
        """to get the name of the hydraulic problem"""
        return self.name

    def getOutputs(self):
        """get expected outputs"""
        return self.outputs

    def getProblemType(self):
        """get problem type: can
           a string saturated or unsaturated
        """
        return self.problemType

    def getRegions(self):
        """to get the regions"""
        return self.regions

    def getSaturation(self):
        """to get the saturation type. It is a string."""
        return self.saturation

    def getSource(self):
        """get Hsources"""
        return self.source
        
    def getViscosity(self):
        """get viscosity"""
        return self.viscosity

    def getZoneConditions(self):
        """get HydraulicProblem zone conditions"""
        return self.zoneconditions

    pass
                                                                                            #
                                                                                            # boundaryConditions treatment
                                                                                            #
class BoundaryCondition_old(CommonBoundaryCondition):
    """
    HydraulicProblem BoundaryCondition definition
    The boundary should be saturated or unsaturated,
    the definition determines the type of boundary.
    """
    def __init__(self, boundary, kind, value, porosity = None, description = None):
        """Boundary condition initialisation with :
        - one or several boundaries (object Body or StructuredMesh
          or list of Supports)
        - a boundary condition type.
          It can be Dirichlet,Neumann and in the future Flux
        - a boundary condition value. Value depends of boundary condition type.
          If Dirichlet, value can be Head, Pressure or SaturationLevel.
          If Neumann, value can be HeadGradient or PressureGradient.
          If Flux, value can be HydraulicFlux.
        """
        print("b",boundary)
        print("k",kind)
        print("v",value)
        
        boundaryConditionDict = makeDico( Dirichlet = [Head, Pressure, SaturationLevel],\
                                          Neumann = [HeadGradient, PressureGradient],\
                                          Flux = [HydraulicFlux])
                        
        CommonBoundaryCondition.__init__(self,boundary, kind, value, boundaryConditionDict, porosity, description)
        return None
        
class BoundaryCondition( CommonBoundaryCondition):
    """
    HydraulicProblem BoundaryCondition definition
    The boundary can be saturated or unsaturated,
    the definition determines the type of boundary.
    """
    def __init__(self, boundary, btype, value, porosity = None, description = None):
        """Boundary condition initialisation with :
        - one or several boundaries (object Body or StructuredMesh
          or list of Supports)
        - a boundary condition type.
          It can be Dirichlet,Neumann and in the future Flux
        - a boundary condition value. Value depends of boundary condition type.
          If Dirichlet, value can be Head, Pressure or SaturationLevel.
          If Neumann, value can be HeadGradient or PressureGradient.
          If Flux, value can be HydraulicFlux.
        """
        #print("b",boundary)
        #print("k",btype)
        #print("v",value)
        
        boundaryConditionDico = makeDico(Dirichlet=[Head, Pressure, SaturationLevel],\
                                         Neumann=[HeadGradient, PressureGradient],\
                                         Flux=[HydraulicFlux])
                        
        CommonBoundaryCondition.__init__(self,boundary, btype, value, boundaryConditionDico, porosity, description)
        return None
        
    def saturationCheck(self,saturation):
        if saturation:
            pass
            #
            # if faut pouvoir verifier qu'une condition de saturation n'a pas ete fixee
            #
    
    pass

class InitialCondition(CommonInitialCondition):
    """
    Specific saturatedHydraulicProblem / unsaturatedHydraulicProblem 
     InitialCondition definition
    *"""    
    def __init__(self, body, value):
        """Initial condition initialisation with
        - One or several bodies (object Support or StructuredMesh
          or list of)
        - The value is of type Head; eventually a Pressure or a SaturationLevel could be introduced: not the case for the moment.
          The value can be inserted as a function
        """
        CommonInitialCondition.__init__(self, body, value)
        return None
        
    def saturationCheck(self,saturation):
        if saturation:
            
            pass
            #
            # if faut pouvoir verifier qu'une condition de saturation n'a pas ete fixee
            #
#   
class Source(CommonSource):
    """Source definition"""        
    def __init__(self, zone, value):
        """Source initialisation with:
        - one or several bodies or CartesianMesh elements
        - a value (object Flowrate)
        """
        CommonSource.__init__(self,zone,value,[Flowrate])
        return
#
class ZoneCondition(CommonZoneCondition):
    """specific ZoneCondition class for hydraulicproblem"""
    def __init__(self, zone, value):
        """Zone condition initialisation"""
        CommonZoneCondition.__init__(self,zone,value,Pressure)
        return
