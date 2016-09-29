from __future__ import absolute_import
from __future__ import print_function
import types
from generictools import isInstance

from listtools import toList

import material

from PhysicalQuantities import PhysicalQuantity,\
                               Pressure,\
                               PressureGradient

from exceptions import Exception
from time import time
from memory import getMemory
import six


def getPhysicalQuantityName(physicalQuantity):
    if type(physicalQuantity) is bytes:
        key=physicalQuantity
        pass
    elif issubclass(physicalQuantity,PhysicalQuantity):
        key=physicalQuantity.__name__
        pass
    else:
        raise Exception
        pass
    return key

def verifySomeOfPhysicalQuantitiesExists(listOfPhysicalQuantities,regions,species=None,option='exclusive'):
    """
    raise an exception if an element of listOfPhysicalQuantities
    is not defined in one region of the region list regions"""
    #
    listOfPhysicalQuantities = toList(listOfPhysicalQuantities)
    
    listOfNames = []
    listOfNames = [getPhysicalQuantityName(physicalQuantity) for physicalQuantity in listOfPhysicalQuantities]
#    for physicalQuantity in listOfPhysicalQuantities:
#        listOfNames.append(getPhysicalQuantityName(physicalQuantity))
#        pass
    listOfNames=tuple(listOfNames)
    affichage='('+(len(listOfNames)-1)*'%s, '+'%s)'
    #
    for reg in regions:
        regPhysicalQuantityAnz = 0
        for physicalQuantity in listOfPhysicalQuantities:
            print("dbg verifyPhysicalQuantityOnRegion",verifyPhysicalQuantityOnRegion(physicalQuantity,reg))
            regPhysicalQuantityAnz +=\
                verifyPhysicalQuantityOnRegion(physicalQuantity,reg)
            pass
        if not regPhysicalQuantityAnz:
            msg='no physical quantity of \n('
            msg+=  affichage%listOfNames
            msg+="\nis defined for material  '%s'."\
                  %reg.getMaterial().getName()
            raise Exception(msg)
        elif regPhysicalQuantityAnz>1 and option=='exclusive':
            msg='more than one of physical quantities in \n'
            msg+=  affichage%listOfNames
            msg+="\nis defined for material : '%s'."\
                  %reg.getMaterial().getName()
            raise Exception(msg)
        else:
            pass
        pass
            
def regionPhysicalQuantitiesCheck(physicalQuantitiesList,regions,species=None):
    """
    raise an exception if a physical property, or an element of physicalQuantitiesList, 
    is not defined in one region of the list regions called list
    """
    #
    physicalQuantitiesList = toList(physicalQuantitiesList)
    physicalQuantitiesNames = []
    physicalQuantitiesNames = [getPhysicalQuantityName(physicalQuantity) for physicalQuantity in physicalQuantitiesList]
#    for physicalQuantity in physicalQuantitiesList:
#        physicalQuantitiesNames.append(getPhysicalQuantityName(physicalQuantity))
#        pass
    physicalQuantitiesNames = tuple(physicalQuantitiesNames)
    affichage='('+(len(physicalQuantitiesNames)-1)*'%s, '+'%s)'
    #
    #
    #
    for reg in regions:
        anzPhysQuant=0
        for PhysQuant in physicalQuantitiesList:
            anzPhysQuant+= verifyPhysicalQuantityOnRegion(PhysQuant,reg,species,option='boolean')
            pass
        if anzPhysQuant == 0:
            verbose = "no physical quantity of "
            verbose+= "is defined for material  '%s'."%reg.getMaterial().getName()
            raise Exception(verbose)
        pass

def setDefaultPhysicalQuantity(physicalQuantity,value,regions,species=None):
    key=getPhysicalQuantityName(physicalQuantity)
    for reg in regions:
        if not species:
            if not verifyPhysicalQuantityOnRegion(physicalQuantity,reg,option='boolean'):
                reg.getMaterial().setProperty(key,value)
                pass
            pass
        else:
            for spe in species:
                if not verifyPhysicalQuantityOnRegion(physicalQuantity,\
                                          reg,spe.getName(),option='boolean'):
                    #print "AFFECTATION !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                    #reg.getMaterial().setProperty(key,(value,spe))
                    reg.getMaterial().changeProperty(physicalQuantity,[(value,spe)])
                    pass
                pass
            pass
        pass
                    #print "AFFECTATION TERMINEE"

## def setDefaultDependPhysicalQuantity(physicalQuantity,value,regions,species=None):
##     key=getPhysicalQuantityName(physicalQuantity)
##     for reg in regions:
##         if not verifyPhysicalQuantityOnRegion(physicalQuantity,reg,option='boolean'):
##             reg.getMaterial().setProperty(key,value)



def verifyPhysicalQuantityExists(physicalQuantity,regions,species=None):
    """
    raise an exception if physicalquantity physicalQuantity is not defined in one region of regions
    """
    
    for reg in regions:
        verifyPhysicalQuantityOnRegion(physicalQuantity,reg,species)

def verifyPhysicalQuantityOnRegion(physicalQuantitiesList, region, species = None, option = None):
    physicalQuantitiesList = toList(physicalQuantitiesList)
    for physicalQuantity in physicalQuantitiesList:
        try:
            key = getPhysicalQuantityName(physicalQuantity)
        except:
            raise Exception("check the list of physical quantities")
        material = region.getMaterial()
        
        if material.hasProperty(key) == 0:
            message = " the material "%material.getName()+" has not the property named "%key
            raise Exception(message)
        else:
            return len(physicalQuantitiesList)
        pass
            

def verifyUnknownTypeBoundaryCondition(unknown_list,boundaries) :
    """raise an exception if boundaries support other unknown
    that those defined in unknown_list
    NOT TO BE USE WITH DIFFERENT SPECIES"""
    found = 0
    for boundary in boundaries:
        value= boundary.getValue()
        for unknown in unknown_list:
            if type(unknown) is type :
                if type(value) == type(unknown):
                    found = 1
                    pass
                pass
            elif isInstance(value,unknown):
                found = 1
                pass
            pass
        if not found:
            raise Warning("Given boundary condition is not of correct type")
#        found = 0
        pass

def verifyZoneBoundaryConditionisUnique(boundaryConditions):
    """
    a boundary should be defined only once, it raises an exception if not
    """
    t0 = time()
    i = 1
    boundaryConditions = toList(boundaryConditions)
    for boundary in boundaryConditions:
        boundlist = boundary.getBoundary()
        boundlist = toList(boundlist)
        for bound in boundlist:
            mesh = None
            for bounds in boundaryConditions[i:]:
                boundslist = bounds.getBoundary()
                boundslist = toList(boundslist)
                for bou in boundslist:
                    if mesh:
                        test = ((bou == bound) or
                                mesh.intersectSupports('test',entity,[bou,bound]))
                        pass
                    else:
                        test = (bou == bound)
                        pass
                    if test:
                        vars1=None
                        vars2=None
                        try:
                            vars1=boundary.getDepend()
                            vars2=bounds.getDepend()
                        except:
                            msg="ERROR : Different boundary conditions "
                            boundname = bound.getName()
                            if bou == bound:
                                msg+="defined on the same boundary"
                                msg+=" named %s"%boundname+ "."
                                pass
                            else:
                                bouname = bou.getName()
                                msg+="defined on boundaries with common elements.\n"
                                msg+="Boundaries with common elements are named %s"%boundname + " and %s"%bouname + "."
                                t1 = time()
                                print('temps de verifyZoneBoundaryConditionisUnique : ' + str(t1- t0) +'s')
                                print('used memory :', getMemory() , 'Ko \n')
                            raise msg
                        for var in vars1:
                            if (var in vars2) or var=='ALL' or vars2==['ALL']:
                                msg="ERROR : Different boundary conditions "
                                msg+="for the same variable : %s"%var
                                boundname = bound.getName()
                                if bou == bound:
                                    msg+=" defined on the same boundary"
                                    msg+=" named %s"%boundname + "."
                                    pass
                                else:
                                    bouname = bou.getName()
                                    msg+=" defined on boundaries with common elements.\n"
                                    msg+="Boundaries with common elements are named %s"%boundname + " and %s"%bouname
                                    t1 = time()
                                    print('temps de verifyZoneBoundaryConditionisUnique : ' + str(t1- t0) +'s')
                                    print('used memory :', getMemory() , 'Ko \n')
                                    pass
                                raise Warning(msg)
                            pass
                        pass
                    pass
                pass
            pass                
        i = i+1
        pass
    t1 = time()
    print('temps de verifyZoneBoundaryConditionisUnique : ' + str(t1- t0) +'s')
    print('used memory :', getMemory() , 'Ko \n')
    return


# -- Use for verifications
        
def verifyPressureBoundaryConditions(boundaryConditions, density,
                                     gravity):
    """raise an exception if pressure boundary conditions have
    been set without setting value of gravity and density"""
    for boundary in boundaryConditions:
        value= boundary.getValue()
        if (isInstance(value,[Pressure,PressureGradient])):
            if ((density is None) or
                (gravity is None)):
                raise Warning("Pressure or PressureGradient boundary condition used without set density and gravity")
            pass
        pass
    pass


def intrinsicPermeabilityCheck(regions, check):
    """
    Raise an exception if intrinsic permeability has been set
    without setting value of gravity, density and viscosity
    """
    for reg in regions:
        if reg.getMaterial().getIntrinsicPermeability():
            if (check == 6):
                pass
            elif (check ==-6):
                six.reraise(Warning, "intrinsic permeability has been set without defining gravity", reg.getMaterial().getName())
            elif (check ==-3):
                raise Warning("intrinsic permeability has been set without defining gravity and viscosity")
            elif (check ==-2):
                raise Warning("intrinsic permeability has been set without defining gravity and density")
            elif (check == 2):
                raise Warning("intrinsic permeability has been set without defining density")
            elif (check == 3):
                raise Warning("intrinsic permeability has been set without defining viscosity")
            pass
        pass
    pass
# --
