"""
Enables to treat fields over bodies.
"""

from __future__ import absolute_import
from __future__ import print_function
import copy, os, types

from functions import Function

from generictools import listTypeCheck

from numpy import array,\
                  concatenate,\
                  float,\
                  int,\
                  ravel,\
                  reshape
from six.moves import range

class Field:
    pass

class ZoneField(Field):
    """
    structure used other a body field.
    """
    def __init__(self, name, mesh):
        self.name = name
        self.mesh = mesh
        self.zones = []
        self.bodies = []
        self.materials = []

    def setName(self, name):
        self.name = name
        return

    def getName(self):
        return self.name

    def getEntity(self):
        #print " dbg fields getEntity is:\n ",self.entity
        #print " dbg fields getEntity over\n"
        return self.entity

    def setEntity(self, entity):
        if hasattr(self,'entity'):
            raise RuntimeError("entity value already set")
        print("dbg fields setEntity",self.entity)
        self.entity = entity

    def getNbBodies(self):
        return len(self.bodies)

    def getNbZones(self):
        return len(self.zones)

    def setComponentsNames(self, names):
        self.components_names = names
        return

    def getComponentsNames(self):
        return self.components_names

    def setZone(self, zone, values, material=None):
        try:
            myEntity = self.getEntity()
            #print " dbg fields setZone: it was ok myEntity",myEntity
            #print " dbg fields setZone ok"
        except AttributeError:
            myEntity = zone.getEntity()
            self.entity = myEntity
#        if zone.getEntity() != myEntity:
#            print "dbg fields setZone ",self.entity," zone.getEntity", zone.getEntity()
#            raise ValueError("zone of wrong entity")
        self.zones.append(zone)
        self.materials.append(material)
        self.appendZoneValues(values)
        return None

    def getBodies(self):
        return self.zones

    def getZones(self):
        self.getBodies()
    
    def getBody(self,bodyNumber):
        return self.zones[bodyNumber]
        
    def getZone(self,bodyNumber):
        return self.getBody(bodyNumber)

    def getMaterials(self):
        return self.materials

    def getMaterial(self,bodyNumber):
        return self.materials[bodyNumber]

    def verifyCompatible(self, other):
        if self.__class__ != other.__class__ \
           or self.mesh != other.mesh \
           or self.getEntity() != other.getEntity() \
           or self.type != other.type \
           or self.getNbComponents() != other.getNbComponents()\
           or self.zones != other.zones:
            raise ValueError("incompatible fields")
        return

class NumericZoneField(ZoneField):
    """
    Numerical values defined over a body field
    """
    def __init__(self, name, mesh, components_names, numType=float, depend=None):
        ZoneField.__init__(self, name, mesh)
        self.setComponentsNames(components_names)
        self.nb_components = len(components_names)
        values = array([], numType)
        values = reshape(values, (0, self.nb_components))
        self.values = values
        self.numType = numType
        self.depend=depend

    def appendZoneValues(self, values):
        values = reshape(values, (1, self.nb_components))
        self.values = concatenate((self.values, values))
        return

    def getDepend(self):
        return self.depend

    def setDepend(self,depend):
        self.depend = depend

    def getValues(self):
        return ravel(self.values).tolist()

    def getZoneValues(self, nb_zone):
        return self.values[nb_zone,:].tolist()

    def getNbComponents(self):
        return len(self.components_names)

    def duplicate(self):
        """return an identical copy of self"""
        name = self.name
        copy = NumericZoneField(name, self.mesh, self.components_names, self.numType)
        copy.zones = self.zones
        copy.materials = self.materials
        if 'entity' in list(self.__dict__.keys()): copy.entity = self.entity
        return copy

    def extractComponentValue(self,component_name):
        try:
            index = self.components_names.index(component_name)
        except ValueError:
            raise Exception("problem with the component name!!!")
        name = self.name
        copy = NumericZoneField(name, self.mesh, component_name, self.numType)
        copy.components_names=[component_name]
        copy.zones = self.zones
        copy.materials = self.materials
        copy.values = reshape(self.values[:,index],(len(copy.zones),1))
        return copy
        
    def __add__(self, other):
        self.verifyCompatible(other)
        new_field = self.duplicate()
        new_field.values = self.values + other.values
        return new_field

    def __sub__(self, other):
        self.verifyCompatible(other)
        new_field = self.duplicate()
        new_field.values = self.values - other.values
        return new_field

    def __neg__(self):
        new_field = self.duplicate()
        new_field.values = - self.values
        return new_field

    def __mul__(self, other):
        self.verifyCompatible(other)
        new_field = self.duplicate()
        new_field.values = self.values * other.values
        return new_field

    def __div__(self, other):
        self.verifyCompatible(other)
        new_field = self.duplicate()
        new_field.values = self.values / other.values
        return new_field


    def amult(self,value,components='ALL'):
        new_field = self.duplicate()
        if components=='ALL':
            #raise self.values[0,0]
            try:
                new_field.values = self.values*value
            except:
                nb_zones = self.getNbZones()
                nb_compo = self.getNbComponents()
                for f in range(nb_zones):
                    val=[]
                    for i in range(nb_compo):
                        try:
                            val.append(self.values[f,i].amult(value))
                        except:
##                             print 'value',value
##                             print 'f,i,self.values[f,i]',f,i,self.values[f,i]
                            val.append(self.values[f,i]*value)
                            pass
                        pass
                    new_field.appendZoneValues(val)
                    pass
                #new_field.values = self.values.amult(value)
            pass
        else:
            components=toList(components)
            listTypeCheck(components,int)
            nb_zones = self.getNbZones()
            nb_compo = self.getNbComponents()
            for f in range(nb_zones):
                val=[]
                for i in range(nb_compo):
                    if i in components:
                        try:
                            val.append(self.values[f,i]*value)
                        except:
##                             print 'value',value
##                             print 'f,i,self.values[f,i]',f,i,self.values[f,i]
                            val.append(self.values[f,i].amult(value))
                    else:
                        val.append(self.values[f,i])
                        pass
                    pass
                new_field.appendZoneValues(val)
                pass
            pass
        return new_field

    def aplus(self,value,components='ALL'):
        new_field = self.duplicate()
        if components=='ALL':
            try:
                new_field.values = self.values+value
            except:
                nb_zones = self.getNbZones()
                nb_compo = self.getNbComponents()
                for f in range(nb_zones):
                    val=[]
                    for i in range(nb_compo):
                        try:
                            val.append(self.values[f,i].aplus(value))
                        except:
##                             print 'value',value
##                             print 'f,i,self.values[f,i]',f,i,self.values[f,i]
                            val.append(self.values[f,i]+value)
                            pass
                        pass
                    new_field.appendZoneValues(val)
                    pass
            pass
        else:
            components=toList(components)
            listTypeCheck(components,int)
            nb_zones = self.getNbZones()
            nb_compo = self.getNbComponents()
            for f in range(nb_zones):
                val=[]
                for i in range(nb_compo):
                    if i in components:
                        try:
                            val.append(self.values[f,i]+value)
                        except:
##                             print 'value',value
##                             print 'f,i,self.values[f,i]',f,i,self.values[f,i]
                            val.append(self.values[f,i].aplus(value))
                    else:
                        val.append(self.values[f,i])
                        pass
                    pass
                new_field.appendZoneValues(val)
                pass
            pass
        return new_field
#
# numeric field over a body
#
class NumericBodyField(ZoneField):
    """
    Numerical values defined over a body
    """
    def __init__(self, name, mesh, components_names, numType=float, depend=None):
        ZoneField.__init__(self, name, mesh)
        self.setComponentsNames(components_names)
        self.nb_components = len(components_names)
        values = array([], numType)
        values = reshape(values, (0, self.nb_components))
        self.values = values
        self.numType = numType
        self.depend=depend

    def appendZoneValues(self, values):
        values = reshape(values, (1, self.nb_components))
        self.values = concatenate((self.values, values))
        return

    def getDepend(self):
        return self.depend

    def setDepend(self,depend):
        self.depend = depend

    def getValues(self):
        return ravel(self.values).tolist()

    def getZoneValues(self, nb_zone):
        return self.values[nb_zone,:].tolist()

    def getNbComponents(self):
        return len(self.components_names)

    def duplicate(self):
        """
        self explained : to copy
        """
        name = self.name
        copy = NumericBodyField(name, self.mesh, self.components_names, self.numType)
        copy.zones = self.zones
        copy.materials = self.materials
        if 'entity' in list(self.__dict__.keys()): copy.entity = self.entity  
        return copy

    def extractComponentValue(self,component_name):
        try:
            index = self.components_names.index(component_name)
        except ValueError:
            raise Exception("You should give a correct component_name!!!")
        name = self.name
        copy = NumericBodyField(name, self.mesh, component_name, self.numType)
        copy.components_names=[component_name]
        copy.zones = self.zones
        copy.materials = self.materials
        copy.values = reshape(self.values[:,index],(len(copy.zones),1))
        return copy
        
    def __add__(self, other):
        self.verifyCompatible(other)
        new_field = self.duplicate()
        new_field.values = self.values + other.values
        return new_field

    def __sub__(self, other):
        self.verifyCompatible(other)
        new_field = self.duplicate()
        new_field.values = self.values - other.values
        return new_field

    def __neg__(self):
        new_field = self.duplicate()
        new_field.values = - self.values
        return new_field

    def __mul__(self, other):
        self.verifyCompatible(other)
        new_field = self.duplicate()
        new_field.values = self.values * other.values
        return new_field

    def __div__(self, other):
        self.verifyCompatible(other)
        new_field = self.duplicate()
        new_field.values = self.values / other.values
        return new_field


    def amult(self,value,components='ALL'):
        new_field = self.duplicate()
        if components=='ALL':
            #raise self.values[0,0]
            try:
                new_field.values = self.values*value
            except:
                nb_zones = self.getNbZones()
                nb_compo = self.getNbComponents()
                for f in range(nb_zones):
                    val=[]
                    for i in range(nb_compo):
                        try:
                            val.append(self.values[f,i].amult(value))
                        except:
##                             print 'value',value
##                             print 'f,i,self.values[f,i]',f,i,self.values[f,i]
                            val.append(self.values[f,i]*value)
                            pass
                        pass
                    new_field.appendZoneValues(val)
                    pass
                #new_field.values = self.values.amult(value)
            pass
        else:
            components=toList(components)
            listTypeCheck(components,int)
            nb_zones = self.getNbZones()
            nb_compo = self.getNbComponents()
            for f in range(nb_zones):
                val=[]
                for i in range(nb_compo):
                    if i in components:
                        try:
                            val.append(self.values[f,i]*value)
                        except:
##                             print 'value',value
##                             print 'f,i,self.values[f,i]',f,i,self.values[f,i]
                            val.append(self.values[f,i].amult(value))
                    else:
                        val.append(self.values[f,i])
                        pass
                    pass
                new_field.appendZoneValues(val)
                pass
            pass
        return new_field

    def aplus(self,value,components='ALL'):
        new_field = self.duplicate()
        if components=='ALL':
            try:
                new_field.values = self.values+value
            except:
                nb_zones = self.getNbZones()
                nb_compo = self.getNbComponents()
                for f in range(nb_zones):
                    val=[]
                    for i in range(nb_compo):
                        try:
                            val.append(self.values[f,i].aplus(value))
                        except:
##                             print 'value',value
##                             print 'f,i,self.values[f,i]',f,i,self.values[f,i]
                            val.append(self.values[f,i]+value)
                            pass
                        pass
                    new_field.appendZoneValues(val)
            pass
        else:
            components=toList(components)
            listTypeCheck(components,int)
            nb_zones = self.getNbZones()
            nb_compo = self.getNbComponents()
            for f in range(nb_zones):
                val=[]
                for i in range(nb_compo):
                    if i in components:
                        try:
                            val.append(self.values[f,i]+value)
                        except:
##                             print 'value',value
##                             print 'f,i,self.values[f,i]',f,i,self.values[f,i]
                            val.append(self.values[f,i].aplus(value))
                    else:
                        val.append(self.values[f,i])
                        pass
                    pass
                new_field.appendZoneValues(val)
                pass
            pass
        return new_field

class InstanceBodyField(ZoneField):
    """
    Body field of objects.

    Objects can be vectors or tensors.
    """
    def __init__(self, name, mesh, type=float, depend=None):
        ZoneField.__init__(self, name, mesh)
        self.values = []
        self.type = type
        self.depend=depend

    def appendZoneValues(self, instance):
        self.values.append(instance)
        return

    def getDepend(self):
        return self.depend

    def setDepend(self,depend):
        self.depend = depend
        
    def getValues(self):
        values = []
        for instance in self.values:
            values.extend(instance.tolist())
        return values

    def getZoneValues(self, nb_zone):
        return self.values[nb_zone].tolist()

    def getNbComponents(self):
        return self.values[0].getNbComponents()


    def duplicate(self):
        name = self.name
        copy = InstanceBodyField(name, self.mesh, self.type)
        copy.setComponentsNames(self.getComponentsNames())
        copy.zones = self.zones
        copy.materials = self.materials
        return copy

    def __add__(self, other):
        self.verifyCompatible(other)
        new_field = self.duplicate()
        values = []
        values_0 = self.values
        values_1 = other.values
        for i in range(len(values_0)): values.append(values_0[i] + values_1[i])
        new_field.values = values
        return new_field

    def __sub__(self, other):
        self.verifyCompatible(other)
        new_field = self.duplicate()
        values = []
        values_0 = self.values
        values_1 = other.values
        for i in range(len(values_0)): values.append(values_0[i] - values_1[i])
        new_field.values = values
        return new_field

    def __neg__(self):
        new_field = self.duplicate()
        values = []
        values_0 = self.values
        for i in range(len(values_0)): values.append(- values_0[i])
        new_field.values = values
        return new_field

    def amult(self, scalar):
        new_field = self.duplicate()
        values = []
        values_0 = self.values
        for i in range(len(values_0)): values.append(values_0[i].amult(scalar))
        new_field.values = values
        return new_field


class BodyFieldFunction(ZoneField):
    """
    Zone field of functions.

    
    WARNING : FOR INSTANCE, IT SUPPOSE THAT ALL COMPONENTS ARE OF SAME TYPE (FLOAT, FUNCTION)
    """
    def __init__(self, name, mesh, components_names, type=float,depend=None):
        ZoneField.__init__(self, name, mesh)
        self.components_names = components_names
        self.nb_components = len(components_names)
        values = array([], type)
        values = reshape(values, (0, self.nb_components))
        self.values = values
        self.depend=depend
        self.type = type

    def appendZoneValues(self, values):
        values = reshape(values, (1, self.nb_components))
        self.values = concatenate((self.values, values))
        return

    def getDepend(self):
        return self.depend

    def setDepend(self,depend):
        self.depend = depend
        
    def getZoneValues(self, nb_zone):
        return self.values[nb_zone,:].tolist()

    def getNbComponents(self):
        return len(self.components_names)

    def duplicate(self):
        name = self.name
        copy = BodyFieldFunction(name, self.mesh, self.components_names, self.type)
        copy.zones = self.zones
        copy.materials = self.materials
        return copy

    def amult(self,value,components='ALL'):
        new_field = self.duplicate()
        if components=='ALL':
            #raise self.values[0,0]
            try:
                new_field.values = self.values*value
            except:
                nb_zones = self.getNbZones()
                nb_compo = self.getNbComponents()
                for f in range(nb_zones):
                    val=[]
                    for i in range(nb_compo):
                        val.append(self.values[f,i].amult(value))
                        pass
                    new_field.appendZoneValues(val)
                #new_field.values = self.values.amult(value)
        else:
            components=toList(components)
            listTypeCheck(components,int)
            nb_zones = self.getNbZones()
            nb_compo = self.getNbComponents()
            for f in range(nb_zones):
                val=[]
                for i in range(nb_compo):
                    if i in components:
                        try:
                            val.append(self.values[f,i]*value)
                        except:
                            val.append(self.values[f,i].amult(value))
                    else:
                        val.append(self.values[f,i])
                        pass
                    pass
                new_field.appendZoneValues(val)
                pass
            pass
        return new_field
