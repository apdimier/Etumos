""" Common Model to be specialized by problem type """
from generictools import isInstance

from generictools import makeDico, memberShip
import types

from cartesianmesh import CartesianMesh

from commonproblem import CommonBoundaryCondition

from mesh import Body

from typechecktools import verifyClassList
#
# import units
#
from functions import LinearFunction2D

from material import Material

from PhysicalQuantities import Head,\
                               HeadGradient,\
                               Length,\
                               PhysicalQuantity

from PhysicalProperties import FlowRate

from chemistry import	ChemicalState

from species import createList

class GeometricObject:
    """
    generic class
    """
    pass

class Edge(GeometricObject):
    """
    An edge
    """
    def __init__(self, length):
        memberShip(length, Length)
        self.length = length
        return None
    def getLength(self):
        return self.length
    pass

class Cylinder(GeometricObject):
    def __init__(self, radius, height):
        memberShip(radius, Length)
        self.radius = radius
        memberShip(height, Length)
        self.height = height
        return None
    def getHeight(self):
        return self.height
    def getRadius(self):
        return self.radius
    pass

class DiscreteObject:
    def __init__(self):
        return
    pass

class DiscreteEdge(DiscreteObject):
    '''
    DiscreteEdge
    '''
    def __init__(self, edge, nb_points):
        """
        constructor with :
        - edge : instance of Edge
        - nb_points : integer
        """
        DiscreteObject.__init__(self)
        memberShip(edge, Edge)
        self.edge = edge
        from types import IntType
        if type(nb_points) != IntType:
            raise TypeError, "nb_points should be an integer"
        self.nb_points = nb_points
        return None
    def getEdge(self):
        return self.edge
    def getNbPoints(self):
        return self.nb_points
    pass


class Region:
    """
    Region
    """
    def __init__(self, support, material):
        """
        Constructor with :
        
                -support : unstructured or CartesianMesh
                - material : object Material
        """
        print support
        memberShip(material, Material)
        self.material = material
        memberShip(support,[CartesianMesh, Body])
        self.support = support
        return

    def getBody(self):
	return self.support

    def getMaterial(self):
        """get material"""
	return self.material
    pass

    def getSupport(self):
	return self.support

    def getZone(self):
	return self.support
    pass

class BoundaryCondition ( CommonBoundaryCondition):
    """
    BoundaryCondition default class : is used if None is defined in specific problem
    """
    def __init__(self, boundary, btype, value = None, massTCoef = None, velocity = None, flowRate = None, porosity = None, timeVariation = None,
                 description = None):
        """
        Constructor with :
        - boundary :    a mesh part element of type Cartesian or Unstructured ( made of bodies)
        
        - btype :       is a string and should be "Dirichlet", "Flux", "Mixed", "Neumann"
        
                For a "symmetry", a Neumann boundary condition with g = 0 must be specified
                
        - OPTIONAL :
        
            --> value : a PhysicalQuantity or a list of tuples (PhysicalQuantity,species)
                        or a  ChemicalState

            --> massTCoef :             float : mass transfer coefficient or set to zero

            --> velocity :		object Velocity

            --> porosity :		a scalar.

            --> flowRate :		a Flowrate, see PhysicalQuantities

            --> timeVariation : 	a list of tuples [(time,chemical state)] or [(time,(list of species))]
	"""
#	raw_input(" make dico within the common model")
        bcDico = makeDico(Dirichlet = [ChemicalState, Head], Flux = [ChemicalState, HeadGradient], Neumann = [ChemicalState, HeadGradient])
#	raw_input (" make dico within the common model over")

        CommonBoundaryCondition.__init__(self,boundary, btype, value, bcDico, description)
#        print "dbg commonmodel CommonBoundaryCondition1"
        
        if type(boundary) is types.ListType:
#            print "type of boundary is list type "
#            raw_input("type of boundary is list type ")
            verifyClassList(boundary,[ CartesianMesh, Body])
        else:
            memberShip(boundary,[ CartesianMesh, Body])
#            raw_input("membership ")
            pass
#        raw_input("dbg commonmodel CommonBoundaryCondition2")
        self.boundary = boundary

        if type(btype) != types.StringType:
            raise TypeError, " problem on the definition of  the boundary type "
        if btype.lower() not in ["dirichlet","symmetry","flux","mixed","neumann","noflux"]: raise Exception, " check the boundary condition kind"
        
        self.btype = btype

        self.value_species = None
        self.value_property = None
        self.value = None
        self.headValue = None
        self.massTCoef = 0.
#        raw_input("here we are ")
#        print "type(value)",type(value)
                                                                                                                #
                                                                                                                # We treat B.C. 
                                                                                                                # by default, a chemical state is introduced
                                                                                                                # and in the case of a transient flow, a list
                                                                                                                # made of a chemical state and a head.
                                                                                                                #
        if type(value) is types.ListType:
            for i in value:
                print "dbg commonmodel",type(i)
            verifyClassList(value, [ Head, ChemicalState])
            for bc in value:
                if isinstance(bc, Head):
                    self.headValue = bc # it should be the charge
                else:
                    self.value = bc # it should be chemistry
            pass
        else:
            memberShip(value,[PhysicalQuantity, ChemicalState])
            pass
            if (isinstance(value, PhysicalQuantity) or
                type(value) is types.ListType):
                self.value_species, self.value_property = createList(value, PhysicalQuantity)
            else:
                self.value = value
                pass
            pass

        if massTCoef:
            memberShip(massTCoef,[types.FloatType])
            pass
            if (type(massTCoef) is types.FloatType): 
                self.massTCoef = massTCoef
            else:
                self.massTCoef = 0.0
                pass
            print " common model mass transfer coefficient ",self.massTCoef
            pass

        if porosity:
            self.porosity = porosity
            pass

        if velocity:
            memberShip(velocity,Velocity)
            pass
        self.velocity = velocity

        if flowRate:
            if flowRate.__class__.__name__=="FlowRate":
                pass
            else:
                flowrate = FlowRate(flowrate,"m**3/s") # the flow rate is supposed to be in m**3/s
        self.flowRate = flowRate

        if timeVariation:
            if type(timeVariation) != types.ListType:
                raise typeError, " Time variation should be a list"
	    for item in timeVariation:
	        if type(item[0]) not in [types.FloatType,types.IntType]:
                    raise typeError, "item[@]  should be a list"
	        memberShip(item[1],[ChemicalState])
            pass

        self.timeVariation = timeVariation
        
        return

    def getBoundary (self):
        """get boundary condition boundary"""
        return self.boundary

    def getHeadValue(self):
        """ 
        To get the head used as initialisation for the field
        """
        return self.headValue.getValue()

    def getRegion (self):
        """
        to get boundary condition boundary
        """
        return self.boundary

    def getSupport (self):
        """
        to get boundary condition boundary
        """
        return self.boundary

    def getMTCoef (self):
        """
        to get the mass transfer coefficient
        """
        return self.massTCoef
        
    def getName(self):
        """
        To retrieve the name of the mesh part bounded to the boundary
        """
        return self.boundary.getName()

    def getTimeVariation (self):
        """get the variation over time of boundary conditions"""
        return self.timeVariation

    def getType (self):
        """get boundary condition type"""
        return self.btype

    def getBoundaryType (self):
        """
        to retrieve the boundary condition type
        """
        return self.btype

    def getPorosity (self):
        """
        to retrieve the porosity
        """
        return self.porosity

    def getValue (self, species = None):
        """get boundary condition Value
         if a species is specified,
                return the associated boundary condition value
         else return the default value"""
        if self.value:
            return self.value
        elif self.value_species:
            if species:
                for spe in range(len(self.value_species)):
                    if (self.value_species[spe] == species):
                        return self.value_property[spe]

            return self.value_property[0]
        else:
            return None            

    def getVelocity (self):
        """
        get boundary condition velocity
        """
        return self.velocity

    def getFlowRate (self):
        """
        get boundary condition flowrate
        """
        return self.flowRate

    pass

class InitialCondition:
    """
    InitialCondition
    """    
    def __init__(self, body, value):
        """
        constructor with :
        - body : object body or CartesianMesh
        - value : a PhysicalQuantity or a list of tuples (PhysicalQuantity,species)
                  or a ChemicalState
        """

        if type(body) is types.ListType:
            verifyClassList(body,[CartesianMesh])
        else:
            memberShip(body,[CartesianMesh, Body])
            pass
        self.zone = body
        self.body = body
#        print " body within initialcondition 0",self.body

#        raw_input("body within initialcondition ")

        self.value_species = None
        self.value_property = None
        self.value = None
        self.headValue = None
        if type(value) is types.ListType:
            for i in value:
                print "dbg commonmodel",type(i)
            verifyClassList(value, [ Head, ChemicalState])
            for bc in value:
                if isinstance(bc, Head):
                    self.headValue = bc # it should be the charge
                else:
                    self.value = bc     # it should be chemistry
        else:
            memberShip(value,[PhysicalQuantity,ChemicalState])
            if (isinstance(value, PhysicalQuantity) or type(value) is types.ListType): 
                self.value_species,self.value_property  = createList(value, PhysicalQuantity)
            else:
                self.value = value
            pass
        return None

    def getZone(self):
        """get InitialCondition zone"""
        return self.zone

    def getBody(self):
        """get InitialCondition body"""
        return self.body

    def getBody(self):
        """get InitialCondition body"""
        return self.zone

    def getTemperature(self):
        """ to get the temperature from the aqueous solution """
        return self.value.getTemperature()

    def getHeadValue(self):
        """ 
        To get the head used as initialisation for the field
        """
        return self.headValue.getValue()

    def getValue(self, species = None):
        """ value is the chemical state"""
        if self.value:
            return self.value
        elif self.value_species:
            if species:
                for spe in range(len(self.value_species)):
                    if (self.value_species[spe] == species):
                        return self.value_property[spe]

            return self.value_property[0]
        else:
            return None

    def getChemicalState(self):
        """ value is the chemical state"""
        if self.value:
            return self.value
        else:
            return None 

    pass


class ZoneCondition:
    """
    ZoneCondition default class :
        is used if None is defined in specific problem
    """    
    def __init__(self, zone, value=None):
        """
        constructor with :
        - zone : object CartesianMesh
        - OPTINAL :
        --> value : a PhysicalQuantity or a list of couple (PhysicalQuantity,species)
                    or a ChemicalState
        """
        if type(zone) is types.ListType:
            verifyClassList(zone,[CartesianMesh])
        else:
            memberShip(zone,[CartesianMesh])
            pass
        self.zone = zone

        self.value_species = None
        self.value_property = None
        self.value = None
        if value:
            memberShip(value,[PhysicalQuantity,ChemicalState])
            if (isInstance(value, PhysicalQuantity) or
                type(value) is types.ListType): 
                self.value_species, self.value_property = createList(value, PhysicalQuantity)
            else:
                self.value = value
            pass
        pass

    def getZone(self):
        """
        get ZoneCondition zone
        """
        return self.zone

    def getValue(self, species = None):
        """get zonecondition Value
         if a species is specified,
                return the associated zone condition value
         else return the default value"""
        if self.value:
            return self.value
        elif self.value_species:
            if species:
                for spe in range(len(self.value_species)):
                    if (self.value_species[spe] == species):
                        return self.value_property[spe]

            return self.value_property[0]
        else:
            return None            
    pass


class Source:    
    """Source default class : is used if None is defined in specific problem"""
    def __init__(self, zone, value, rate=None):
        """constructor with :
        - zone : Mesh support
        - value : a PhysicalQuantity or a list of couple (PhysicalQuantity,species)
                  or a ChemicalState
        - OPTIONAL :
        --> rate : FlowRate
        """
        memberShip(zone, [CartesianMesh])
        self.zone = zone

        self.value_species = None
        self.value_property = None
        self.value = None
        if value:
            memberShip(value,[PhysicalQuantity,ChemicalState])
            if (isInstance(value, PhysicalQuantity) or
                type(value) is types.ListType): 
                self.value_species,self.value_property  = createList(value, PhysicalQuantity)
            else:
                self.value = value
            pass

        if rate:
            memberShip(value, Flowrate)
        self.rate = rate
        return

    def getZone(self):
        """get source zone"""
        return self.zone

    def getRate(self):
        """get source rate"""
        return self.rate

    def getValue(self, species = None):
        """get source Value
         if a species is specified,
                return the associated source value
         else return the default value"""
        if self.value:
            return self.value
        elif self.value_species:
            if species:
                for spe in range(len(self.value_species)):
                    if (self.value_species[spe] == species):
                        return self.value_property[spe]

            return self.value_property[0]
        else:
            return None  

    pass
