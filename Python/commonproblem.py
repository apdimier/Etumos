# -*- coding: utf-8 -*-
"""
common problem

We define here the base of all problems to be defined within
the coupling.

"""

# -- __init__

from __future__ import absolute_import
from __future__ import print_function
from generictools import isInstance, memberShip

from listtools import toList

from cartesianmesh import CartesianMesh

from mesh import Body

from PhysicalQuantities import Head, Pressure, Displacement, NormalForce

from types import ListType, StringType, TupleType

from typechecktools import verifyClass, verifyClassList

from types import DictType
from six.moves import range

## - Specific Problem class definition
class CommonBoundaryCondition_old:
    """ BoundaryCondition definition"""
    def __init__(self, boundary, kind, value, bcdict, porosity = None, description = None):
        """Boundary condition initialisation with :
        - one boundary

        - a boundary condition type.
          We verify that it's a key of bcdict dictionnary
        - a boundary condition value. Value depend of boundary condition type.
        -bcdict : a dictionnary with key = type of boundary condition and value = Possible class of boundary condition value
        """        
        self.value_species =None

        memberShip(boundary.support,[CartesianMesh, Body])

#        verifyClass(boundary,[CartesianMesh,Body])
        self.boundary = boundary
        if type(kind) != StringType:
            raise TypeError(" type should be a string")
        if kind not in list(bcdict.keys()): raise Exception(" check the boundary condition type ")
        self.type = kind

        value = toList(value)
        for val in value:
            if type(val) is TupleType:
                checked = val[0] 
                for i in range(1,len(val)):
                    from datamodel import Species
                    memberShip(val[i], Species)
                    pass
                pass
            else:
                checked = val
                pass
            for definedtype in bcdict:
                if kind == definedtype:
                    memberShip(checked, bcdict[kind])
                    pass
                pass
            pass
        if not self.value_species:
            from PhysicalQuantities import PhysicalQuantity
            from species import createList
            print(value)
            self.value_species, self.value_property = createList(value, PhysicalQuantity)
            pass

        if description == None:
            self.description = ""
            pass
        else:
            self.description = description
            pass
        return

class CommonBoundaryCondition:
    """ 
    BoundaryCondition definition
    """
    def __init__(self, boundary, btype, value, bcdict, porosity = None, description = None):
        """
        Boundary condition initialisation with :
        
        - one boundary

        - a boundary condition type.
          We verify that it's a key of bcdict dictionnary
        - a boundary condition value. Value depend of boundary condition type.
        
        - bcdict : a dictionnary with key = type of boundary condition and value = Possible class of boundary condition value
        
        All boundary conditions satisfy that format. It should enable the lecture of hydraulic, mechanical and chemical-transport boundary conditions.
        
        Exemple: bcdict = {'Flux': [class chemistry.ChemicalState , class PhysicalQuantities.HeadGradient],
                   'Dirichlet': [class chemistry.ChemicalState, class PhysicalQuantities.Head,\
                         class PhysicalQuantities.Displacement, class PhysicalQuantities.NormalForce], 
                   'Neumann': [class chemistry.ChemicalState, class PhysicalQuantities.HeadGradient]}
        
        """   
        self.value = None       
        self.value_species = None
        #print " here we are 1, bcdict ", bcdict
        #print " here we are 2, bcdict ", bcdict.keys()
        #print value
        #raw_input()
        #print("dbg bcdict ",list(bcdict.keys()))
        if isInstance(boundary,[CartesianMesh, Body]):
            pass
        else:
            memberShip(boundary.support,[CartesianMesh, Body])
            pass

        self.boundary = boundary
        if type(btype) != StringType: raise TypeError(" type should be a string ")
        if btype not in list(bcdict.keys()): 
            print("bcdict.keys():",list(bcdict.keys()))
            print("btype : ",btype)
            raise Exception(" check the boundary condition type ")
        self.type = btype
        print("value: ",type(value.__class__.__name__),value.__class__.__name__)
        #print "dbg bcdict ",bcdict.keys()
        #raw_input( "valuefffffffff     fff")
        #if value.__class__.__name__ == 'Head':
        #    print "valueeeee Head",value.__class__.__name__
        #else:
        #    print "valueeeef",value.__class__.__name__
        if isinstance(value,ListType):
            print(" value is of type ListType")
            for val in value:
                if isinstance(val,Displacement):
                    self.value = {"Displacement":val.getValue()}
                    pass
                elif isinstance(val,NormalForce):
                    if self.value != None:
                        self.value["NormalForce"] = val.getValue()
                        pass
                    else:
                        self.value = {"NormalForce":val.getValue()}
                        pass
                elif isinstance(value,Head):
                    valeurs=toList (val)
                    for vale in valeurs:
                        if type(val) is TupleType:
                            checked = val[0] 
                            for i in range(1,len(val)):
                                memberShip(val[i], Species)
                                pass
                            pass
                        else:
                            checked = val
                            pass
                        pass
                    pass

        elif isinstance(value,Displacement):
            print(" value is of type Displacement")
            self.value = {"Displacement":value.getValue()}
            pass
        elif isinstance(value,NormalForce):
            print(" value is of type NormalForce")
            if self.value != None:
                self.value["NormalForce"] = value.getValue()
                pass
            else:
                self.value = {"NormalForce":value.getValue()}
                pass
            pass
            
        elif isinstance(value,Head):
            print(" value is of type Head")
            from datamodel import Species
            value=toList (value)
            for val in value:
                if type(val) is TupleType:
                    checked = val[0] 
                    for i in range(1,len(val)):
                        memberShip(val[i], Species)
                        pass
                    pass
                else:
                    checked = val
                    pass
                for definedType in bcdict:
                    if btype == definedType:
                        memberShip(checked, bcdict[btype])
                        #raw_input("here we are")
                        pass
                    pass
                pass
            if not self.value_species:
                from PhysicalQuantities import PhysicalQuantity
                from species import createList
                print(value)
                self.value_species, self.value_property = createList(value, PhysicalQuantity)
                pass

        if description == None:
            self.description = None
            pass
        else:
            self.description = description
            pass
        return None

    def getBoundary (self):
        """
        to retrieve boundary conditions
        """
        return self.boundary

    def getRegion (self):
        """
        to retrieve regions
        """
        return self.boundary

    def getSupport(self):
        """
        get boundary support
        """
        return self.boundary.support

    def getDisplacementValue(self, displacement = None):
        """
        get the displacement components, if any. Value can be a dictionary or a 
        """
        print("getDisplacementValue",self.value)
        if type(self.value) == DictType:
            if "Displacement" in list(self.value.keys()):
                return self.value["Displacement"]
        elif isinstance(self.value,Displacement):
            return self.value
        else:
            return None

    def getNormalForceValue(self, normalForce = None):
        """
        get the normal force value, if any
        """
        if type(self.value) == DictType:
            if "NormalForce" in list(self.value.keys()):
                return self.value["NormalForce"]
            pass
        elif isinstance(self.value,NormalForce):
            return self.value
        else:
            return None

    def getValue(self, species = None):
        """
        get boundary conditions value
        """
        return _getValue(species, self.value_species, self.value_property)
        
    getChemicalValue = getValue

    def getType(self):
        """
        get boundary conditions type
        """
        return self.type

    pass

class CommonInitialCondition:
    """
    Common InitialCondition definition. 
    It means we should use that class for any kind of problem, hydraulic, chemical/transport ...
    """    
    def __init__(self, body = None, value = None, description = None):
        """
        domain can be a region of the domain, it could also be a simple body associated to .
        """
        if isInstance(body,[CartesianMesh, Body]):
            pass
        else:
            memberShip(body.support,[CartesianMesh, Body])
            pass
        self.body   = body
        self.zone = body
        self.domain = body
        
#        if domain !=None:
#            if isinstance(domain,Region):
#                memberShip(domain.support,[CartesianMesh, Body])
#            elif isinstance(domain,Body):
#                pass
#            elif isinstance(domain,CartesianMesh):
#                pass
#        self.domain = domain
        #
        #
        #
        if not isinstance(value,(Head,Pressure)):
            pass
        else:
            #print "dbg CommonInitialCondition",value
            if type(value) == None:
                self.value = Head(0.0,"m")
                pass
            elif isinstance(value,Head):
                self.value = value
                pass
            else:
                raise Exception(" to modify, the pressure must be scaled to be entered as a head")
        if not isinstance(value,(Displacement)):
            pass
        else:
            #print "dbg CommonInitialCondition",value
            if type(value) == None:
                self.value = Displacement(0.0,"m")
                pass
            elif isinstance(value,Displacement):
                self.value = value
                pass
            else:
                raise Exception(" to modify, the pressure must be scaled to be entered as a head")
        if description == None:
            self.description = None
            pass
        else:
            self.description = description
            pass
        return None

    def getBody(self):
        """
        to retrieve the domain
        
        """
        if isInstance(self.body,Body):
            return self.body
        else:
            return None

    def getDomain(self):
        """
        to retrieve the domain
        """
        return self.domain

    def getRegion(self):
        """
        syntaxic equivalence
        """
        return self.body

    def getSupport(self):
        """
        get initial conditions  zones
        """
        dir(self.domain)
        return self.domain

    def getValue(self):
        """
        get initial conditions Value
        """
        return self.value.getValue()

    def getZone(self):
        """
        to retrieve the domain
        
        """
        if isInstance(self.body,Body):
            return self.body
        else:
            return None

class CommonSource:
    """Common Source definition"""

    def __init__(self, zone, value, some_classes):
        """
        Initialisation of the source with:
        - one or several zones
        - value : instance of a class defined in some_classes
                  or a list of couple (Value,Species)
                  or a list with a default value and couples (Value,Species) 
                  for example [value,(value1,species1),(value2,species2)]
        - some_classes : list of possible classes of value
        """
        self.value_species, self.value_property = _associateZoneValue(zone, value, some_classes)
        verifyZones(toList(zone))
        self.zone = zone


        return

    def getZone(self):
        """get Source zones"""
        return self.zone

    def getValue(self, species = None):
         """get Source Value
         if a species is specified,
                return the associated source value
         else return the default value"""
         return _getValue(species, self.value_species, self.value_property)
    pass

class CommonExpectedOutput:
    # 
    # (TimeSpecification)  define times to get expected output
    #

    # 
    # brief an expected output quantity
    #

    # unit 
    # unit of the expected output quantity
    #

    # 
    # Support depends on wanted quantity.
    #
    # - For Hydraulic and Transport support is not optional:
    #       - If Flux, support is a tuple (boundary, zone)
    #       - If TotalFlux or TotalInflux, support can be CartesianMesh          
    #       - If other quantities, support can be CartesianMesh
    # - For Chemical and ChemicalTransport :
    #       - support is optional (chemistry ) but if indicated support can be a CartesianMesh or a body
    # - Mecanics 
    #       - support has already been verified => no check
    #

    #  name 
    #  name of the Expected Output
    #

    #  where 
    #   represents expected output localisation. 
    #
    # It's only
    # available is quantity is Pressure,, Saturation or DarcyVelocity
    # Value can be center, face or border
    #

    #  unknown 
    #  (List) define specific wanted species.
    #
    # - List of Species for Hydraulic and Transport
    # - String for Chemical and ChemicalTransport
    #
    def __init__(self, alltype, facetype, quantity, support = None,
                 name = None, unit = None, timeSpecification = None,
                 where = None, unknown = [],save = 'memory',chemical = 0):
        if type(quantity) != StringType:
            raise TypeError(" the quantity must be a string ")
        alltypeupper = [q.upper() for q in alltype]
        #print "alltypeupper",alltypeupper
        quantityupper = quantity.upper()
        if quantityupper not in alltypeupper: raise Exception("the quantity "+quantityupper+" must be checked in Output")
        self.quantity = quantity

        mecanic = ( chemical == 2)
        chemical = (chemical == 1)

        hydrau_transport_type = ['HEAD','PRESSURE','DARCYVELOCITY','SATURATION','CONCENTRATION','SOLIDCONCENTRATION']

        if quantityupper in hydrau_transport_type and not chemical:
            supports=toList(support)
            if len(supports) != 1:
                raise Exception("The support hans not the good length")
            # Support should be Point or Zone
            verifyClassList(supports, [CartesianMesh])
            pass
        elif (quantityupper == 'FLUX'):
            # Support should be TupleType of Boundary, Zone
            if type(support) != TupleType:
                raise TypeError(" support should be a tuple ")
            if (len(support) !=2):
                raise Exception("support must have a length of 2")
            fzone = support[1]
            fbound =  support[0]
            fbounds = toList(fbound)
            entity = fbounds[0].getMesh().getBoundariesEntity()
            memberShip(fbound, MedSupport)
            memberShip(fzone, MedSupport)
            verifyZones(toList(fzone))
            # verifyBoundaries verify now that bounds are borders. We use verifySupports in place
            verifySupports(fbounds,entity)
            pass
        elif quantityupper in ['TOTALFLUX','TOTALINFLUX']:
            supports=toList(support)
            if len(supports) != 1:
                raise Exception("the support has not the good length")
            # Support should be Zone
            verifyClassList(supports, [CartesianMesh])
            pass
        else:
            if support and chemical:
                # chemical transport quantity : support is optionnal
                memberShip(support, [CartesianMesh])
                pass
            elif mecanic:
                # mecanic quantity :    support class is verified by XData      
                pass
            pass
        self.support = support

        if name:
            if type(name) != StringType:
                raise TypeError("the name of a CommonExpectedOutput must be a string")
            self.name = name
            pass
        else:
            self.name = self.quantity
            pass
        #
        if unit:
            if type(unit) != StringType:
                raise TypeError(" unit should be a string ")
        self.unit = unit

        if timeSpecification:
            from timespecification import TimeSpecification
            memberShip(timeSpecification, TimeSpecification)
            mode=timeSpecification.getSpecification()
            if mode not in ['frequency','period','times']: raise Exception(" check the mode argument in CommonExpectedOutput")
            pass
        self.timeSpecification = timeSpecification

        self.where=where

        if save:
            if save not in ['memory','file']: raise Exception(" check the save argument in CommonExpectedOutput")
            pass
        self.save = save

        if unknown:
            if chemical:
                if type(unknown) is ListType:
                    for unbekannte in unknown:
                        if type(unbekannte) != StringType:
                            raise TypeError(" unknown should be a string ")
                            pass
                        pass
                    pass
                else:
                    if type(unknown) != StringType:
                        raise TypeError(" the unknown must be a string ")
                    pass
                pass
            elif mecanic:
                unknown=toList(unknown)
                for u in unknown:
                    if type(u) != StringType:
                        raise TypeError(" u should be a string ")
                    pass
                pass
            else:
                from datamodel import  Species
                verifyClassList(unknown,Species)
                pass
            pass
        self.unknown=unknown

    def getTimeSpecification(self):
        return self.timeSpecification

    def getQuantity(self):
        return self.quantity

    def getUnit(self):
        return self.unit  

    def getSupport(self):
        return self.support

    def getName (self):
        return self.name

    def getLocalisation (self):
        return self.where

    def getSave (self):
        return self.save

    def getUnknown (self):
        return self.unknown

    def getPhenomena (self):
        return None

    def get (self):
        try:
            return self.bc
        except:
            return self

class CommonExpectedOutput_old:
    """Common ExpectedOutput definition. A field, a set of fields or a value"""
    def __init__(self, alltype,facetype,quantity, support, name = None, unit=None,
                 timeSpecification=None,where=None,variables=[]):
        """ExpectedOutput initialisation with :
        - all possible expected output quantity
        - expected output quantity which can be define with attribute 'where=face' or 'where = border'
        - an expected output quantity.
        - a support. Support depends on wanted quantity.
          If Flux, support is a tuple (boundary, zone) (possible type for
          boundary or for zone : MedSupport or CartesianMesh)
          If TotalFlux or TotalInflux, support can be MedSupport or CartesianMesh          
          If other quantities, support can be MedSupport, CartesianMesh
        - OPTIONAL :
          --> a name (string). If None given, name is set to quantity
          --> a unit (string)
          --> where (string) : represents expected output localisation. It's only
                               available if quantity is Pressure,, Saturation or DarcyVelocity
                               and support is MedSupport or CartesianMesh and on all elements.
                               Value can be center, face or border
          --> timeSpecification (TimeSpecification) : define times to get expected output
          --> variables (default value = []) : define specific wanted species
        """

        if type(quantity) != StringType:
            raise TypeError(" quantity for CommonExpectedOutput_old should be a string")
        if quantity not in alltype: raise Exception("check the quantity you want to plot ")
        self.quantity = quantity

        partialtype = alltype[:]
        partialtype.remove('Flux')
        partialtype.remove('TotalFlux')
        partialtype.remove('TotalInflux')

        if self.quantity in partialtype:
            supports=toList(support)
            if len(supports) != 1:
                raise Exception(" the support has not the good length")
            verifyClassList(supports, [CartesianMesh])
            for sup in supports:                    
                pass
            pass
        elif (self.quantity == 'Flux'):
            # Support should be TupleType of Boundary, Zone
            if type(support) != TupleType:
                raise TypeError(" support should be a tuple ")
            if (len(support) !=2):
                Message = repr(len(support[sup])) + ' MedSupport given, 2 wanted for a flux expected output'
                raise Message
            fzone = support[1]
            fbound =  support[0]
            memberShip(fbound, MedSupport)
            memberShip(fzone, MedSupport)
            verifyZones(toList(fzone))
            #verifyBoundaries(toList(fbound))
            pass
        elif self.quantity in ['TotalFlux','TotalInflux']:
            supports=toList(support)
            if len(supports) !=1:
                raise Exception(" the support has not the good length ")
            # Support should be Zone
            verifyClassList(supports, [MedSupport, CartesianMesh])
            for sup in supports:                    
                pass
            pass
        self.support = support

        if name:
            if type(name) != StringType:
                raise TypError("name should be a string  within CommonExpectedOutput_old")
            self.name = name
            pass
        else:
            self.name = self.quantity
        #
        if unit: 
            if type(unit)  != StringType:
                raise typeError(" unit should be a string ")
        self.unit = unit

        if timeSpecification:
            from timespecification import TimeSpecification
            memberShip(timeSpecification, TimeSpecification)
            mode=timeSpecification.getSpecification()
            if mode not in ['frequency','period','times']: raise Exception(" check the mode argument in CommonExpectedOutput")
            pass
        self.timespecification = timeSpecification

        self.where=where

        if len(variables):
            from datamodel import  Species
            verifyClassList(variables,Species)
        self.variables=variables

    def getTimeSpecification(self):
        """get expected output time specification"""
        return self.timespecification

    def getQuantity(self):
        """get expected output quantity"""
        return self.quantity

    def getUnit(self):
        """get expected output unit"""
        return self.unit  

    def getSupport(self):
        """get expected output support"""
        return self.support

    def getName(self):
        """get expected output name"""
        return self.name

    def getLocalisation(self):
        """get expected output localisation"""
        return self.where

    def getVariablesList(self):
        """get species list"""
        return self.variables

class CommonZoneCondition:
    """Common ZoneCondition class"""
    def __init__(self, zone, value,some_classes):
        """Zone condition initialisation"""
        self.value_species, self.value_property = _associateZoneValue(zone, value,some_classes)
        verifyZones(toList(zone))
        self.zone = zone
        return

    def getZone(self):
        """get zone condition zone"""
        return self.zone

    def getValue(self, species = None):
        """get zone condition value"""
        return _getValue(species,self.value_species, self.value_property)
    pass

def _associateZoneValue(zone,value,some_classes):
    zones=toList(zone)
    verifyClassList(zones,[CartesianMesh])
    value = toList(value)
    for val in value:
        if type(val) is TupleType:
            from datamodel import  Species
            memberShip(val[0], some_classes)
            memberShip(val[1], Species)
            pass
        else:
            memberShip(val, some_classes)
            pass
        pass

    from datamodel import createList
    from datamodel import PhysicalQuantity
    value_species, value_property = createList(value, PhysicalQuantity)
    return value_species, value_property


def _getValue(species = None,value_species=[], value_property=[]):
        if species:
            for spe in range(len(value_species)):
                if (value_species[spe] == species):
                    return value_property[spe]
                pass
            pass
        if len(value_property) > 0:
            return value_property[0]  
        else:
            return None

class CommonInitialConditionOld:
    """Common InitialCondition definition"""    
    def __init__(self, zone, value,some_classes,some_solid_classes=None):
        """
        Initial condition initialisation with
        - one or several zones 
        - a value instance of a class defined in some_classes
                           or a list of couple (Value,Species)
                           or a list with a defaut value and couples (Value,Species) 
                           for example [c,(c1,species1),(c2,species2)]
        - some_classes : list of possible classes of value (soluble classes)
        - some_solid_classes : list of possible classes of value (solid classes)
        """
        zones=toList(zone)
        #verifyZones(zones)
        self.zone = zone
        if some_solid_classes:
            all_classes = some_classes + some_solid_classes
            pass
        else:
            all_classes = some_classes
            pass

        val_solub=[]
        val_solid=[]     
        self.value_species=[] 
        self.value_property=[]
        self.value_solid_species=[]
        self.value_solid_property=[]
        value = toList(value)
        for val in value:
            solubOK = 0
            if type(val) is TupleType:
                from datamodel import  Species
                memberShip(val[0], all_classes)
                memberShip(val[1], Species)
                for sc in some_classes:
                    if isInstance(val[0], sc):
                        val_solub.append(val)
                        solub0K = 1
                        break
                    pass            
                if some_solid_classes and not solubOK:
                    for sc in some_solid_classes:
                        if isInstance(val[0], sc):
                            val_solid.append(val)
                            break
                        pass
                    pass
                pass
            else:
                memberShip(val, all_classes)
                for sc in some_classes:
                    if isInstance(val, sc):
                        val_solub.append(val)
                        solub0K = 1
                        break            
                if some_solid_classes and not solubOK:
                    for sc in some_solid_classes:
                        if isInstance(val, sc):
                            val_solid.append(val)
                            break
                    pass
                pass
            pass

        if val_solub:
            from datamodel import createList
            from datamodel import PhysicalQuantity
            self.value_species, self.value_property = createList(val_solub, PhysicalQuantity)
            pass
        if val_solid:
            from datamodel import createList
            from datamodel import PhysicalQuantity
            self.value_solid_species, self.value_solid_property = createList(val_solid, PhysicalQuantity)
            pass
        return

    def getZone(self):
        """get initial conditions  zones"""
        return self.zone

    def getValue(self, species = None):
        """get initial conditions Value"""
        return _getValue(species,self.value_species, self.value_property)

    def getSolidValue(self, species = None):
        """get initial conditions solid value"""       
        return _getValue(species,self.value_solid_species, self.value_solid_property)

class CommonInitialCondition_old:
    """
    Common InitialCondition definition. 
    It means we can use that class for any kind of problem, hydraulic, chemical/transport ...
    """    
    def __init__(self, domain = None, value = None):
        """
        domain can be a region of the domain, it could also be a simple body associated to .
        """
        memberShip(domain.support,[CartesianMesh, Body])
        self.domain = domain
        
#        if domain !=None:
#            if isinstance(domain,Region):
#                memberShip(domain.support,[CartesianMesh, Body])
#            elif isinstance(domain,Body):
#                pass
#            elif isinstance(domain,CartesianMesh):
#                pass
#        self.domain = domain
        #
        #
        #
        print("dbg CommonInitialCondition",value)
        if type(value) == None:
            self.value = Head(0.0,"m")
        elif isinstance(value,Head):
            self.value = value
        else:
            raise Exception(" to modify, the pressure must be scaled ")

    def getDomain(self):
        """get initial conditions  zones"""
        return self.domain

    def getRegion(self):
        """get initial conditions  zones"""
        return self.domain

    def getSupport(self):
        """get initial conditions  zones"""
        dir(self.domain)
        return self.domain

    def getValue(self):
        """
        get initial conditions Value
        """
        return self.value.getValue()

