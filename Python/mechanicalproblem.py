# -*- coding: utf-8 -*-
""" 
An elasticity problem is defined here;
It can be steady or transient.
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

from PhysicalProperties import  Density,\
                                Viscosity
from PhysicalQuantities import  Displacement,\
                                FlowRate,\
                                Head,\
                                HeadGradient,\
                                HydraulicFlux,\
                                NormalForce,\
                                PressureGradient,\
                                Pressure
#
import types

class MechanicalProblem:
    """
    A mechanical problem can be 
    
        steady or time dependent
        
        The only tool is the elmer software.
        
        Aster will be introduced to treat plastic problems.

        Simulation is transient if calculationTimes are given. They can be combined with the transient argument.
        But without the calculationTimes list, the simulation is steady.
        
        The goal is to link mechanics to geochemistry and to handle the physical links.
        
    """
    def __init__(self,\
                 name,\
                 regions,\
                 boundaryConditions,\
                 initialConditions = None,\
                 state = None,\
                 simulationType = None,\
                 calculationTimes = None,\
                 gravity = None,\
                 density = None,\
                 sources = None,\
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
                                
        - gravity:              default None

        - density:              default None

        - sources               default None

        - outputs               default None

        """                                                                                 # 
                                                                                            # name should be a string
                                                                                            #
        if type(name) != bytes:
            raise TypeError("name should be a string ")
        self.name = name
                                                                                            #
                                                                                            # mechanical
                                                                                            #
        self.problemType = "elasticity"
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
                if meshdim == 2:
                    value.append(0.)

                gravity=Vector(value)
            except:
                pass
            pass
        else:            
            meshdim = regions_zones[0].getSpaceDimension()
            value=[0.]*meshdim
            value[-1] = 9.81
            if meshdim == 2:
                value.append(0.)
                pass
            gravity=Vector(value)
            print(value)
            pass
        #
        self.gravity = gravity
                                                                                            #
                                                                                            # density treatment
                                                                                            #
        if density:
            if type(density) == FloatType:
                density = Density(density, 'kg/m**3')
                pass
            memberShip(density, Density)
            check = 2*check
            pass
        self.solidDensity = density
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
                raise typeError(" calculationTimes should be a list ")
            CalculationTimes=toFloatList( self.calculationTimes)
            #
            for item in CalculationTimes:
                if type(item) != float:
                    raise TypeError(" item should be a float ")
                pass
            self.calculationTimes = sorted( CalculationTimes)
#            print self.calculationTimes;#raw_input(" within the loop, calculation times are printed here")
                                                #
                                                                                            # The simulation is transient
                                                                                            #
            self.steadyState = 0
            pass
                                                                                            #        
                                                                                            # boundaryConditions treatment
                                                                                            #        
        self.defaultBC = None
        boundaryConditions = toList(boundaryConditions)
        print(" problem type ",self.problemType)
        print(dir(boundaryConditions[0])) 
                                                                                            #        
                                                                                            # boundaryConditions treatment
                                                                                            #        
        boundaries = []
        for boundaryElement in boundaryConditions:
            boundary = toList(boundaryElement.getBoundary())
            for bound in boundary:
                boundaries.append(bound)
                pass
            pass
        if self.defaultBC:
            if not self.density:
                self.density = Density(1.)
                pass
            if not self.gravity:
                mesh_dim=regions[0].getZone().getMesh().getSpaceDimension()
                if mesh_dim==2:
                    self.gravity=Gravity(Vector(0.,1.))
                    pass
                elif mesh_dim==3:
                    self.gravity=Gravity(Vector(0.,0.,1.))
                    pass
                else:
                    raise Exception('Dimension ????')
                
                pass
            pass        
        self.boundaryConditions = boundaryConditions
                                                                                            #
                                                                                            # initialConditions treatment
                                                                                            #        
        self.initialConditions = initialConditions
                                                                                            #
                                                                                            # sources treatment
                                                                                            #
        if sources: verifyClassList(sources, Source)
        self.sources = sources
                                                                                            #
                                                                                            # outputs treatment
                                                                                            #
        if outputs:
            outputs1 = toList(outputs)
            verifyClassList(outputs1, _dicoproblem[type].ExpectedOutput)

            if not hasattr(self,'output_names'):
                self.output_names=[]
                pass
            for output in outputs1:
                if output.getName() in self.output_names:
                    msg = '\n\nDifferent outputs should not share the same name.\n'
                    msg+= 'End of the hydraulic problem run.\n\n'
                    raise Exception(msg)
                self.output_names.append(output.getName())
                pass
        #
        self.outputs = outputs
        #
        return None

    def getBoundaryConditions(self):
        """
        To get the boundary conditions
        """
        return self.boundaryConditions

    def getCalculationTimes(self):
        """get calculation times"""
        return self.calculationTimes

    def getDensity(self):
        """get the solid density"""
        return self.solidDensity

    def getGravity(self):
        """get gravity"""
        return self.gravity

    def getInitialConditions(self):
        """get initial conditions"""
        return self.initialConditions

    def getName(self):
        """
        To get the name of the mechanical problem
        """
        return self.name

    def getOutputs(self):
        """get expected outputs"""
        return self.outputs

    def getProblemType(self):
        """
        To get the problem type: 
        is a string: elasticity or plasticity
        """
        return self.problemType

    def getRegions(self):
        """to get the regions"""
        return self.regions

    def getSources(self):
        """get Hsources"""
        return self.sources
        
    def getViscosity(self):
        """get viscosity"""
        return self.viscosity

    pass
                                                                                            #
                                                                                            # boundaryConditions treatment
                                                                                            #
class BoundaryCondition( CommonBoundaryCondition):
    """
    BoundaryCondition definition
    Boundaries can be expressed in terms of displacement or forces.
    """
    def __init__(self, boundary, btype, value, porosity = None, description = None):
        """Boundary condition initialisation with :
        - one or several boundary(ies) (object Region). The objet is a region in order to be able to treat several materials
        - a boundary condition type.
          It can be:
          
            a displacement
            a normal force ( or a pressure)
            In the case of a pressure, the surface of the boundary is retrieved to derive the normal force
            
        - A boundary condition value. Value depends of boundary condition type.
        """
        print("b",boundary,boundary.__class__.__name__)
        print("k",btype)
        print("v",value)
        
        boundaryConditionDico = makeDico(Dirichlet=[Displacement, NormalForce, Pressure])
                        
        CommonBoundaryCondition.__init__(self,boundary, btype, value, boundaryConditionDico, porosity, description)
        return None
    

class InitialCondition(CommonInitialCondition):
    """
    Specific initial condition for a mechanical problem 
     
    InitialCondition definition
    """    
    def __init__(self, body, value):
        """
        The initial condition section may be used to set initial values
        
        - One or several bodies (object Support or StructuredMesh
          or list of)
        - The value is of type Displacement
        """
        CommonInitialCondition.__init__(self, body, value)
        if not isinstance(value,Displacement) and not isinstance(value,Temperature):
            raise Warning("check the definition of the initial conditions")
        return None
    
class Source(CommonSource):
    """ Source definition """        
    def __init__(self, zone, value):
        """Source initialisation with:
        - one or several bodies or CartesianMesh elements
        - a value (object Flowrate)
        """
        CommonSource.__init__(self,zone,value,[Flowrate])
        return None
