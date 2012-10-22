# -*- coding: utf-8 -*-
"""
Chemical Transport Model.
All that is needed to define a Chemical Transport problem.
"""

##from utilities import *
##from chemistry import TotalConcentration, Davies, ActivityLaw,  KineticLaw, ReversibleKineticLaw
from chemistry import *
from physicallaws import EffectiveDiffusionLaw #, WinsauerDiffusionLaw, ExponentialDiffusionLaw, LinearDiffusionLaw

from commonmodel import Region, BoundaryCondition, InitialCondition, Source

from listtools import toList

from timespecification import TimeSpecification

from PhysicalQuantities import Head,\
                               HeadGradient,\
                               PhysicalQuantity

from PhysicalProperties import Density,\
                               EffectiveDiffusion,\
                               KinematicDispersion,\
                               Porosity,\
                               Velocity,\
                               Viscosity

from material import Material
import types
from typechecktools import verifyClassList

from species import Species

from os import environ,\
               system

from sys import argv

import warnings

from getopt import getopt

from vector import V as Vector
# -- Verifications ...
from verifyproblem import verifyPhysicalQuantityOnRegion

#from vector import V as Vector
#--------------------------
# ChemicalTransport Problem
#---------------------------

def getfluidThermalConductivity(temp):
    """ 
    Used to get the thermal conductivity given in W/(m-K)
    as a function of temperature
    """
    return 0.5621+0.00193*temp-7.3e-6*temp*temp

class ChemicalTransportProblem:
    """
    Chemical transport problem Definition         

        Input :
          name (string)
          regions (list of regions)
          initialConditions     the list of InitialConditions
          boundaryConditions    the list of BoundaryConditions
          calculationTimes (list of two float)
          chemistryDB (string) : it can be a name 
          sources (list of Source, OPTIONAL)
          darcyVelocity: a Velocity, None, or a string (read, computed)
          seePage velocity:  a Velocity, None, or a string (read, computed)
          speciesBaseAddenda (list of Species, OPTIONAL)
          kineticLaws (list of KineticLaw, OPTIONAL)
          timeUnit    (time unit, NECESSARY IF KINETIC)
          activityLaw (ActivityLaw, OPTIONAL)
          porosityState (string, OPTIONAL) : 'constant' (default) or 'variable'
          diffusionLaw (EffectiveDiffusionLaw, OPTIONAL)
          outputs (list of ExpectedOutput, OPTIONAL)

        Examples :
                problem  = ChemicalTransportProblem(    name               = "guiteste",
                                                        regions            = [columnRegion],
                                                        initialConditions  = [columnIC],
                                                        boundaryConditions = [inletBC],
                                                        calculationTimes   = [0.0,24000.],
                                                        sources            = None,
                                                        darcyVelocity      = Velocity(Vector([darcy,0.0,0.0])),
                                                        chemistryDB        = "water_gui.dat",
                                                        speciesBaseAddenda = speciesAddenda,
                                                        kineticLaws        = None,
                                                        activityLaw        = None,
                                                        outputs            = expectedOutputs)

        """
    def __init__(self,
                 name,
                 regions,
                 boundaryConditions,
                 initialConditions,
                 calculationTimes,
                 chemistryDB,
                 sources = None,
                 darcyVelocity = None,                                                      # darcy velocity
                 seepageVelocity = None,
                 speciesBaseAddenda = None,
                 kineticLaws =  None,
                 timeUnit = None, 
                 activityLaw = None,
                 # variable porosity
                 porosityState = None,
                 headVPorosity = None,
                 mpiSize = None,
                 # variable porosity and variable diffusion
                 diffusionLaw = None,
                 permeabilityLaw = None,
                 outputs = None,
                 userProcessing = None,
                 userFunctionList = None,
                 variablePorosity = None,
                 saturation = None,
                 temperature = None,
                 temperatureField = None,
                 outputTimeStudy = None) :
                 
        self.mpiEnv = None
        environ["MPIROOT"] = ""
        self.outputTimeStudy = outputTimeStudy
        print "dbg argv ",argv
        #raw_input("problem")
        if mpiSize!=None:
            self.mpiEnv = 1
            environ["MPIROOT"] = "MPI"
            print "mpi is in argv ",argv,system("echo $MPIROOT")
        else:
            system("unset MPIROOT")
        #raw_input("argv")
                                                                                            #
                                                                                            # the problem is saturated
                                                                                            #
        self.saturation = "saturated"
        # name
        if type(name) != types.StringType: raise TypeError, "the name of the ChemicalTransportProblem must be a string "
        self.name = name

        # boundary conditions
        print " dbg bd",dir(boundaryConditions[0])
        print " dbg bd",boundaryConditions[0].type
        print " dbg bd",boundaryConditions[0].description
        #print " dbg bd",boundaryConditions[0].headValue
        #raw_input()
        verifyClassList(boundaryConditions, BoundaryCondition)
        self.boundaryConditions = boundaryConditions
                                                                                            #
                                                                                            # regions
                                                                                            #
        verifyClassList(regions, Region)
        self.regions = regions
                                                                                            #
                                                                                            # Darcy and seepage Velocity treatment :
                                                                                            #
        if isinstance(darcyVelocity,Velocity):
            self.darcyVelocity = darcyVelocity 
        elif isinstance(seepageVelocity,Velocity):
            self.darcyVelocity = seepageVelocity
            warnings.warn("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\
                           seepage velocity is not handled and is equivalent to Darcy velocity for Elmer\n\
                           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")         
        elif type(darcyVelocity) == types.StringType:
            if darcyVelocity.lower() == "read":
                                                                                            #
                                                                                            # The Darcy velocity will be read from
                                                                                            # the velocity.ep file
                                                                                            #
                self.darcyVelocity = "read"
            elif darcyVelocity.lower() == "computed":                                       # the Darcy velocity is transient
                self.darcyVelocity = "computed"
                                                                                            #
                                                                                            # we check that materials contain relevant properties
                                                                                            #
                meshdim = self.regions[0].support.getSpaceDimension()
                for region in self.regions:
                    meshdim = max(meshdim,region.support.getSpaceDimension())
                    verifyPhysicalQuantityOnRegion(["porosity"],region)
                    if region.getMaterial().getHydraulicConductivity():
                         continue
                    if region.getMaterial().getIntrinsicPermeability() == None and region.getMaterial().getPermeability() == None:
                        raise Exception, " the permeability or the intrinsic permeability should be set"
                    elif (self.permeability and self.intrinsicPermeability):
                        raise Exception, "A Material with both permeability and intrinsicpermeability can\'t be defined"
                self.meshdim = meshdim
                #
                # default values are set here for density, gravity and density
                #
                value=[0.]*meshdim
                value[-1] = 9.81
                if meshdim == 2:
                    value.append(0.)

                gravity=Vector(value)
                self.gravity = gravity
                self.density = Density(1.0,'kg/l')
                self.viscosity = Viscosity(1.0,'kg/m/s')

        else:
            self.darcyVelocity = None
                                                                                            #
                                                                                            # data Base
                                                                                            #
        if type(chemistryDB) != types.StringType: raise TypeError,\
        " the chemistryDB argument of the ChemicalTransportProblem must be a string "
        self.chemistryDB = chemistryDB
                                                                                            #
                                                                                            # initial conditions
                                                                                            #
        verifyClassList(initialConditions, InitialCondition)
        self.initialConditions = initialConditions
                                                                                            #
                                                                                            # Sources
                                                                                            #
        if sources != None:
            verifyClassList(sources, Source)
            self.sources = sources
	else : 
	    self.sources = None
            pass


        # simulation times to be recovered
        if type(calculationTimes) != types.ListType: raise TypeError, "  simulationTimes must be a list of times "

        i = 0
        for item in calculationTimes:            
            if type(item) not in [types.FloatType,types.IntType]:
                raise TypeError, "  calculationTimes must be a list of times "
            calculationTimes[i] = calculationTimes[i]
            i += 1
            pass

        previous = calculationTimes[0]            
        for item in calculationTimes:
            if item < 0.:
                raise 'Error : Negative calculation time unexpected'
            if item < previous:
                raise 'Error : Decreasing calculation time unexpected'
                previous = item
            self.calculationTimes = calculationTimes
            pass

        # New chemical species
        if speciesBaseAddenda:
            verifyClassList(speciesBaseAddenda, Species)
            pass
        self.speciesBaseAddenda = speciesBaseAddenda

        # Kinetics Laws
        if kineticLaws != None :
            verifyClassList(kineticLaws,KineticLaw)
            self.kineticLaws = kineticLaws
	else :
            self.kineticLaws = None

        # time unit
        if timeUnit:
            if type(timeUnit) != types.StringType:
                raise TypeError, " the time unit argument of the ChemicalTransportProblem must be a string "
            pass
        self.timeUnit = timeUnit

        #
        # Activity Law
        # TODO : check the default activity law
        #
        if activityLaw:
            if not isinstance(activityLaw,ActivityLaw):
                raise Exception, " the activity law instantiation must be checked"
##        else:
##            self.activityLaw = TruncatedDavies()
            pass
        self.activityLaw = activityLaw

        #
        # variable porosity
        #
        if porosityState:
            if type(porosityState) != types.StringType:
                raise TypeError, " the porosityState argument of the ChemicalTransportProblem must be a string "
            porosityState = porosityState.lower()
            if (porosityState == 'constant') or (porosityState == 'variable'):
                self.porosityState = porosityState
                pass
            elif porosityState in ['steady',"cst"]:
                self.porosityState = 'constant'
            elif porosityState in ['transient',"var"]:
                self.porosityState = 'constant'
            else:
##                self.porosityState = None
                mess = "porosityState badly defined (default : 'constant', else 'variable')"
                raise mess
            pass
        else:
            self.porosityState = 'constant'
            pass
        #
        # user processing set up
        #
        if userProcessing and type(userFunctionList) == ListType:
            self.userProcessing = True
            self.processingList = userFunctionList
            for processingFunction in range(len(self.processingList)):
                self.processingList[processingFunction]+="(self)"
                print self.processingList[processingFunction]
                #raw_input()

        else:
            self.userProcessing = False
            self.processingList = None
        #
        # variable porosity : diffusion law
        #
        if diffusionLaw:
            if not isinstance(diffusionLaw,EffectiveDiffusionLaw):
                raise Exceptio, " the diffusion law instanciation must be checked"
            pass
        self.diffusionLaw = diffusionLaw

        self.permeabilityLaw = permeabilityLaw

        if headVPorosity!= None:
            if headVPorosity not in ["constant","variable","constante"]:
                self.headVPorosity = "constant"
            else:
                self.headVPorosity = headVPorosity
        else:
            self.headVPorosity = "constant"

        # Outputs 
        if outputs != None :
            verifyClassList(outputs, ExpectedOutput)
            self.outputs = outputs
	else :
            self.outputs = None

        # timeVaryingBoundaryConditionList 

        self.timeBoundaryConditionVariation = None

        # Mpi
        print "environ ",environ.get('WMPI')
#        if environ.get('WMPI') != None:
#	    opts = argv[:]
#            self.mpiSize = argv[1]
#            print "self.mpiSize ",self.mpiSize
#	else : 
#	    self.mpiSize = None
        self.mpiSize = mpiSize
        #temperature is by default constant
        if temperature == None:
            self.temperature = "constant"
        else:
            self.temperature = temperature

        if temperatureField == None:
            self.temperatureField = None
        else:
            self.temperatureField = temperatureField

        return None
                                                                                            #
                                                                                            # init method end
                                                                                            #
    def getOutputTimeStudy(self):
        """
        """
        return self.outputTimeStudy

    def getBoundaryConditions(self):   
        """
        To get ChemicalTransportProblem boundary conditions
          Ouput :
            (list of BoundaryCondition)
        """
        return self.boundaryConditions

    def getCalculationTimes(self):
        """
        To get ChemicalTransportProblem  calculation times
          Ouput : 
            (list of float) 
            """
        return self.calculationTimes

    def getHelp(self,func = None):
        """
        That function is used to get some help on the
        class and on relevant functions
        Ex: getHelp() or getHelp(a.function)
        """
        if func == None:
            print self.__doc__
        else:
            print func.__doc__
        pass

    def getInitialConditions(self):    
        """
        To get ChemicalTransportProblem initial conditions
          Ouput :
            (list of InitialCondition)
        """
        return self.initialConditions

    def getMPIEnv(self):
        """
        to control the simulation environment: self.mpiEnv is None: the simulation is sequential
        """
        return self.mpiEnv

    def getName(self):
        """
        To get ChemicalTransportProblem name
          Ouput :
            (string)
        """
        return self.name

    def getProcessingList(self):
        """
        To get the list of user defined methods to be processed
        """
        return self.processingList

    def getRegions(self):
        """
        To get ChemicalTransportProblem regions
          Ouput :
            (list of Region)
        """
        return self.regions

    def getUserProcessing(self):
        """
        To get user processing control parameter
        """
        return self.userProcessing

    def setName(self,name):
        """
        Get ChemicalTransportProblem name
          Ouput :
            (string)
        """
        if type(name) != types.StringType:
                raise TypeError, " the name argument of the ChemicalTransportProblem must be a string "

        if name != None:
	    self.name = name
	return


    def setRegions(self,regions):
        """
        set ChemicalTransportProblem regions
        """
        verifyClassList(regions, Region)
        self.regions = regions
	return

    def setBoundaryConditions(self,boundaryConditions):   
        """
        set ChemicalTransportProblem boundary conditions
        """
        verifyClassList(boundaryConditions, BoundaryCondition)
        self.boundaryConditions = boundaryConditions
	return

    def setCalculationTimes(self, calculationTimes):
        """
        set ChemicalTransportProblem  calcultaion times
            """
        if type(calculationTimes) != types.ListType:
                raise TypeError, " the calculationTimes argument of the ChemicalTransportProblem must be a list"
        self.calculationTimes = calculationTimes
	return

    def setInitialConditions(self, initialConditions):    
        """
        Get ChemicalTransportProblem initial conditions
          Ouput :
            (list of InitialCondition)
        """
        verifyClassList(initialConditions, InitialCondition)
        self.initialConditions = initialConditions
	return

    def getSources(self):    
        """
        Get ChemicalTransportProblem sources
          Ouput :
            (None or list of Source)
        """
        return self.sources

    def setSources(self,sources):    
        """
        set ChemicalTransportProblem sources
        """
        if sources != None:
	    verifyClassList(sources, Source)
        self.sources = sources
	return

    def fluidThermalConductivity(self,fluidThermalConductivity):
        self.fluidThermalConductivity = fluidThermalConductivity
        return None

    def getThermalOption(self):
        if (self.temperature.lower() in ["timeDependent","true","variable"]):
           thermalOption = 1    # we consider a thermal field
           self.fluidThermalConductivity = getfluidThermalConductivity(25.)
           #
           # the volumic Heat Capacity here is given here in J/kg/m3
           #
           self.waterVolHCapacity =  4.189e+6
        else:
           thermalOption = 0    # the temperature field is constant
           self.fluidThermalConductivity = None
           self.waterVolHCapacity = None
        return thermalOption

    def setThermalOption( self,thermalOption):
        self.temperature = thermalOption
	pass

    def getDarcyVelocity(self): 
        """
        Get ChemicalTransportProblem  Darcy velocity, 
        which can be a vector, a string or None
        """
        print "within getDarcyVelocity self.darcyVelocity",self.darcyVelocity
        return self.darcyVelocity

    def setDarcyVelocity(self,darcyVelocity): 
        """
        Set ChemicalTransportProblem Darcy velocity
        """   
        if darcyVelocity != None:
	    if not isinstance(darcyVelocity,(Velocity,types.StringType)):
	        raise Exception, " the velocity definition should be checked"
	print "  setDarcyVelocity      ",darcyVelocity
        self.darcyVelocity = darcyVelocity
	return None
	
    def setDensity (self,density,unit = None):
        """
        used to change the default value
        """
        if isinstance(density,Density):
            self.Density = density
        elif isinstance(density,FloatType):
            if unit == None:
                raise Warning, " you have to give a unit while entering a density\n"+\
                "through the setDensity function\n"
            self.density = Density(density,unit)
        else:
            raise Warning, " check the input of the density through the set densityfunction"
        pass
	
    def setGravity (self,gravity, unit = None):
        """
        used to set the gravity
        """
        if memberShip(gravity, Gravity):
            self.gravity = Gravity
        elif isinstance(gravity, FloatType):
            if unit == None:
                raise Warning, " you have to give a unit while entering a gravity\n"+\
                "through the setGravity function\n"
                value=[0.]*self.meshdim
                value[-1] = gravity
                if self.meshdim == 2:
                    value.append(0.)
                gravity=Vector(value)
            
            self.gravity = Gravity(gravity, unit)
        else:
            raise Warning, " check the input of the gravity through the set gravityfunction"
        pass
	
    def setViscosity (self,viscosity, unit = None):
        """
        used to set the viscosity
        """
        if memberShip(viscosity, Viscosity):
            self.viscosity = Viscosity
        elif isinstance(viscosity,FloatType):
            if unit == None:
                raise Warning, " you have to give a unit while entering a viscosity\n"+\
                "through the setViscosity function\n"
            self.viscosity = Viscosity(viscosity,unit)
        else:
            raise Warning, " check the input of the viscosity through the set viscosityfunction"
        pass

    def getchemistryDB(self):
        """
        Get ChemicalTransportProblem  data base
          Ouput : 
            (string) 
            """
        return self.chemistryDB

    def getchemistryDBFileName(self):
        """
        Get ChemicalTransportProblem  data base
          Ouput : 
            (string) 
            """
        filename = ""
        if not(self.chemistryDB):
            raise Exception, " a database must be associated to the problem through the chemistryDB element"

        return self.chemistryDB.getFileName()

    def setchemistryDB(self,chemistryDB):
        """
        set ChemicalTransportProblem  data base
             """
        if type(chemistryDB) != types.StringType:
                raise TypeError, " the chemistryDB argument of the ChemicalTransportProblem must be a string "

        self.chemistryDB = self.chemistryDB
	return

    def getSpeciesBaseAddenda(self):
        """
        Get ChemicalTransportProblem new species 
          Ouput : 
            (None or list of Species) 
            """
        return self.speciesBaseAddenda

    def setSpeciesBaseAddenda(self,speciesBaseAddenda):
        """
        set ChemicalTransportProblem new species 
            """
        if speciesBaseAddenda != None:
	    verifyClassList(speciesBaseAddenda, Species)
        self.speciesBaseAddenda = speciesBaseAddenda
	return

        return self.chemistryDB

    def getKineticLaws(self):
        """
        Get ChemicalTransportProblem kinetic laws 
          Ouput : 
            (None or list of kineticLaw) 
            """
        return self.kineticLaws

    def setKineticLaws(self,kineticLaws):
        """
        set ChemicalTransportProblem kinetic laws 
            """
        if kineticLaws != None :
            verifyClassList(kineticLaws,KineticLaw)
            self.kineticLaws = kineticLaws
	else :
            self.kineticLaws = None
	return

    def getTimeUnit(self):
        """
        Get ChemicalTransportProblem time uniot
          Ouput : 
            (None or String) 
            """
        return self.timeUnit

    def setTimeUnit(self,timeUnit):
        """
        set ChemicalTransportProblem time uniot
            """
        if timeUnit:
            if type(timeUnit) != types.StringType:
                raise TypeError, " time unit is a string "
            pass
        self.timeUnit = timeUnit
	return

    def getActivityLaw(self):
        """
        Get ChemicalTransportProblem activity law 
          Ouput : 
            (None or activityLaw) 
            """
        return self.activityLaw

    def setActivityLaw(self,activityLaw=None):
        """
        Get ChemicalTransportProblem activity law 
          Ouput : 
            (None or activityLaw) 
            """
        if activityLaw:
            if not isinstance(activityLaw,ActivityLaw):
                " setting the activity law: check the instanciation"
            pass
        self.activityLaw = activityLaw
	return

##    #variable porosity
##    def getPorosityState(self):
##        """
##        Get ChemicalTransportProblem porosity state (constant or variable)
##          Ouput : 
##            (None or porosityState) 
##            """
##        return self.porosityState

    #variable porosity
    def getBooleanPorosityOption(self):
        """
        Get ChemicalTransportProblem porosity option (constant or variable)
          Ouput : 
            0 (if constant porosity) or 1 (if variable)
        """
        if (self.porosityState == 'variable'):
            return 1
        else:
            return 0
            
    def getPorosityOption(self):
        """
        Get ChemicalTransportProblem porosity option (constant or variable)
          Ouput : 
            a string: constant / varialble
        """
        return self.porosityState
        
        
    def getVariableHeadPorosityOption(self):
        """
        Get ChemicalTransportProblem porosity option (constant or variable)
        \return  0 (if head constant) or 1 (if head and porosity variable )
        """
        if (self.headVPorosity == 'variable'):
            return 1
        else:
            return 0


    def setVariablePorosityOption(self,variablePorosity):
        """
        Set ChemicalTransportProblem porosity option (constant or variable)
            """
	if (self.porosityState == 'variable'):
            self.variablePorosity = 1
        else:
            self.variablePorosity = 0
	return None

    #variable porosity and variable diffusion
    def getDiffusionLaw(self):
        """
        Get ChemicalTransportProblem diffusion law 
          Ouput : 
            (None or DiffusionLaw) 
            """
        return self.diffusionLaw

    def getPermeabilityLaw(self):
        """
        Get ChemicalTransportProblem diffusion law 
          Ouput : 
            (None or DiffusionLaw) 
            """
        return self.permeabilityLaw

    def setDiffusionLaw(self,diffusionLaw=None):
        """
        Get ChemicalTransportProblem diffusion law 
          Ouput : 
            (None or DiffusionLaw) 
            """
        if diffusionLaw:
            if not isinstance(diffusionLaw,EffectiveDiffusionLaw):
                raise Exception, "the diffusion law must be checked"
        self.diffusionLaw = diffusionLaw
	return None

    def getOutputs(self):
        """
        Get ChemicalTransportProblem expected outputs
          Ouput :
            (None or list of expectedOuputs)
        """
        return self.outputs

    def setOutputs(self,outputs=None):
        """
        Get ChemicalTransportProblem expected outputs
          Ouput :
            (None or list of expectedOuputs)
        """
        if outputs != None :
            verifyClassList(outputs, ExpectedOutput)
            self.outputs = outputs
	else :
            self.outputs = None
        return None

    def getBoundaryConditionVariation(self):
        """
        Get the boundary conditions time variation
          Ouput :
            (None or list of time in association to a list of tuples (BC, values)
        """
        return self.timeBoundaryConditionVariation

    def setBoundaryConditionVariation(self,timeBoundaryConditionVariation):
        """
        set the boundary conditions time variation
        """
        self.timeBoundaryConditionVariation = timeBoundaryConditionVariation
	return None

    def getTimeBoundaryConditionVariation(self,time):
        """
        Get the boundary conditions time variation
          Ouput :
            (None or list of tuples (BC, values)
        """
	for timeElement in self.timeBoundaryConditionVariation:
	    if abs(time-timeElement[0])<1.e-5:
                return timeElement
	return None	

    def getMpiSize(self):
        """
        Allows to access to the global number of processors
        """
	return self.mpiSize
    getMPISize = getMpiSize

class CoupledOutput(CommonExpectedOutput):
    """
    default value of quantity is concentration, it is set to that default value if
    quantity is n't of the right type
    name : Name of the output
    unknown Unknown of the coupled output
    unit : Unit of the output
    """
    def __init__(self,quantity, unknown = None, unit = None, name = None):
        allOut = ['Activity', 'AqueousTotalConcentration', 'Concentration', 'Diffusion', 'Eh', 'FixedTotalConcentration',
                  'IonicStrength', 'GaseousTotalConcentration', 'MineralTotalConcentration',
                  'Numerics', 'pe', 'pH', 'Porosity', 'SaturationIndex', 'TotalConcentration',
                   'Volume', 'VolumicFraction']
        self.quantity = quantity
        if type(self.quantity) != types.StringType:
            raise TypeError, " quantity should be a string "
            if self.quantity not in allOut:
                raise " the quantity is notin coupled output is not considered by the software"
        else:
            self.quantity = "Concentration"

        self.unknown = unknown
        self.unit = unit
        self.name = name

        self.chemicalName = self.quantity

        if self.unknown:
            self.chemicalName += '_' + self.unknown 
            pass

        if not self.name:
            self.name = self.chemicalName
            pass

        if self.unit:
            self.chemicalName += '_' + self.unit 
            pass

        CommonExpectedOutput.__init__(self,
                                      alltype = allOut,
                                      facetype = [],
                                      quantity = self.quantity,
                                      name = self.name,
                                      unit = self.unit,
                                      unknown = self.unknown,
                                      chemical = 1)

        return None

    def getChemicalName(self):
        """
        to get the name of the chemical name, the \"quantity\" , output
        """
        return self.chemicalName

    def getHelp(self):
        print self.__doc__
        pass

