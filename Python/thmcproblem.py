# -*- coding: utf-8 -*-
""" 
An elasticity problem is defined here;
It can be steady or transient.
"""

# -- __init__

# -- Verifications .
from chemistry import KineticLaw,\
                      ExpectedOutput

from generictools import isInstance, makeDico, memberShip


from cartesianmesh import CartesianMesh

from typechecktools import verifyClassList

from listtools import toFloatList, toList

from verifyproblem import verifyZoneBoundaryConditionisUnique
from verifyproblem import intrinsicPermeabilityCheck, regionPhysicalQuantitiesCheck, verifyPressureBoundaryConditions,\
                          verifySomeOfPhysicalQuantitiesExists

from chemistry import ChemicalState
                          
from commonproblem import CommonBoundaryCondition, CommonSource,\
                          CommonInitialCondition, CommonZoneCondition
from commonmodel import Region
from vector import V as Vector

from PhysicalProperties import Density,\
                               Porosity,\
                               Velocity,\
                               Viscosity
from PhysicalQuantities import Displacement,\
                               FlowRate,\
                               Head,\
                               HeadGradient,\
                               HydraulicFlux,\
                               NormalForce,\
                               PressureGradient,\
                               Pressure,\
                               Temperature
                                
from species import Species
#
import types

class THMCProblem:
    """
    A /T/hermal /H/ydraulical /M/echanical /C/hemical problem can be treated here
    
        steady or time dependent
        
    The elmer tool enables the TMH treatment
        
    The phreeqc tool enables the chemistry treatment
        
    Aster will be introduced to treat plastic problems.

    Simulation is transient if calculationTimes are given. They can be combined with the transient argument.
    But without the calculationTimes list, the simulation is steady.
        
        The goal is to link mechanics to geochemistry and to handle the physical links.
        
    """
    def __init__(self,\
                 name,\
                 regions,\
                 boundaryConditions,\
                 initialConditions,\
                 calculationTimes,\
                 chemistryDB,\
                 darcyVelocity = None,                                                      # darcy velocity
                 speciesBaseAddenda = None,\
                 kineticLaws =  None,\
                 timeUnit = None, \
                 activityLaw = None,\
                 porosityState = None,\
                 headVPorosity = None,
                 state = None,\
                 simulationType = None,\
                 gravity = None,\
                 density = None,\
                 diffusionLaw = None,\
                 permeabilityLaw = None,\
                 sources = None,\
                 outputs = None,\
                 userProcessing = None,\
                 userFunctionList = None,\
                 variablePorosity = None,\
                 variableElasticity = None,\
                 temperature = None,\
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
                                                                                            # Elsasticy modulus variation
                                                                                            #
        self.variableElasticity = variableElasticity                                                                                  
                                                                                            #
                                                                                            #
                                                                                            #
        self.mpiEnv = None
        # simulation times to be recovered
        if type(calculationTimes) != list: raise TypeError("  simulationTimes must be a list of times ")

        i = 0
        for item in calculationTimes:            
            if type(item) not in [float,int]:
                raise TypeError("  calculationTimes must be a list of times ")
            calculationTimes[i] = calculationTimes[i]
            i += 1
            pass

        previous = calculationTimes[0]            
        for item in calculationTimes:
            if item < 0.:
                raise Exception('Error : Negative calculation time unexpected')
            if item < previous:
                raise Exception('Error : Decreasing calculation time unexpected')
                previous = item
            self.calculationTimes = calculationTimes
            pass
                                                                                            #
                                                                                            # we dont' consider a wellbore
                                                                                            #
        self.wellbore = False                                                                                
                                                                                            #
                                                                                            # species Addenda
                                                                                            #
        if speciesBaseAddenda not in [None,[]]:
            verifyClassList(speciesBaseAddenda, Species)
            self.speciesBaseAddenda = speciesBaseAddenda
            pass
        else:
           self.speciesBaseAddenda = []
           pass                                                                                  
        if type(name) != bytes:
            raise TypeError("name should be a string ")
        self.name = name
                                                                                            #
                                                                                            # mechanical
                                                                                            #
        self.problemType = "thmc"
                                                                                            #
                                                                                            # Darcy and seepage Velocity treatment :
                                                                                            #
        if isinstance(darcyVelocity,Velocity):
            self.darcyVelocity = darcyVelocity 
#        elif isinstance(seepageVelocity,Velocity):
#            self.darcyVelocity = seepageVelocity
#            warnings.warn("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\
#                           seepage velocity is not handled and is equivalent to Darcy velocity for Elmer\n\
#                           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")         
        elif type(darcyVelocity) == bytes:
            if darcyVelocity.lower() == "read":
                                                                                            #
                                                                                            # The Darcy velocity will be read from
                                                                                            # the velocity.ep file
                                                                                            #
                self.darcyVelocity = "read"
                pass
            elif darcyVelocity.lower() == "computed":                                       # the Darcy velocity is transient
                self.darcyVelocity = "computed"
                pass
        else:
            self.darcyVelocity = None
            pass
                                                                                            #
                                                                                            # data Base
                                                                                            #
        if type(chemistryDB) != bytes: raise TypeError("The chemistryDB argument of the THMC Problem must be a string ")
        self.chemistryDB = chemistryDB
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
            if meshdim == 2: value.append(0.)
            gravity=Vector(value)
            print(value)
            pass
        #
        self.gravity = gravity
                                                                                            #
                                                                                            # activity law
                                                                                            #
        if activityLaw:
            if not isinstance(activityLaw,ActivityLaw):
                raise Exception(" the activity law instantiation must be checked")
##        else:
##            self.activityLaw = TruncatedDavies()
            pass
        self.activityLaw = activityLaw
                                                                                            #
                                                                                            # density treatment
                                                                                            #
        if density:
            if type(density) in [int,float]:
               density = Density(density, 'kg/m**3')
            memberShip(density, Density)
            check = 2*check
            pass
        self.solidDensity = density
                                                                                            #
                                                                                            # variable porosity: diffusion law
                                                                                            #
        if diffusionLaw:
            if not isinstance(diffusionLaw,EffectiveDiffusionLaw):
                raise Exceptio(" the diffusion law instanciation must be checked")
            pass
        self.diffusionLaw = diffusionLaw
        self.permeabilityLaw = permeabilityLaw

        if headVPorosity!= None:
            if headVPorosity not in ["constant","variable","constante"]:
                self.headVPorosity = "constant"
                pass
            else:
                self.headVPorosity = headVPorosity
                pass
        else:
            self.headVPorosity = "constant"
            pass
                                                                                            #
                                                                                            # user processing set up
                                                                                            #
        if userProcessing and type(userFunctionList) == types.ListType:
            self.userProcessing = True
            self.processingList = userFunctionList
            for processingFunction in range(len(self.processingList)):
                self.processingList[processingFunction]+="(self)"
                print(self.processingList[processingFunction])
                pass
            pass

        else:
            self.userProcessing = False
            self.processingList = None
            pass
                                                                                            #
                                                                                            # Kinetics Laws
                                                                                            #
        if kineticLaws != None :
            verifyClassList(kineticLaws, KineticLaw)
            self.kineticLaws = kineticLaws
            pass
        else :
            self.kineticLaws = None
            pass
                                                                                            #        
                                                                                            # times definition
                                                                                            #        
        self.simulationType = simulationType
#        #raw_input("calculation times ")
        if calculationTimes:
            self.calculationTimes = calculationTimes
            self.simulationType = "Transient"
        else:
            self.calculationTimes = None
            self.simulationType = "Steady"

        self.steadyState = 1 
        if self.calculationTimes!= None:
            if type(calculationTimes) != list:
                raise typeError(" calculationTimes should be a list ")
            CalculationTimes=toFloatList( self.calculationTimes)
            #
            for item in CalculationTimes:
                if type(item) != float:
                    raise TypeError(" item should be a float ")
            self.calculationTimes = sorted( CalculationTimes)
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
            for bound in boundary: boundaries.append(bound)
            pass
        if self.defaultBC:
            if not self.density:
                self.density = Density(1.)
                pass
            if not self.gravity:
                mesh_dim=regions[0].getZone().getMesh().getSpaceDimension()
                if mesh_dim==2: self.gravity=Gravity(Vector(0.,1.))
                elif mesh_dim==3: self.gravity=Gravity(Vector(0.,0.,1.))
                else: raise Warning('Dimension ????')
                pass
            pass        
        self.boundaryConditions = boundaryConditions
                                                                                            #
                                                                                            # initialConditions treatment
                                                                                            #        
        self.initialConditions = initialConditions
                                                                                            #
                                                                                            # variable porosity
                                                                                            #
        if porosityState:
            if type(porosityState) != bytes:
                raise TypeError(" the porosityState argument of the ChemicalTransportProblem must be a string ")
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
                                                                                            # sources treatment
                                                                                            #
        if sources != None:
            verifyClassList(sources, Source)
            self.sources = sources
            pass
        else : 
            self.sources = None
            pass
                                                                                            #
                                                                                            # temperature
                                                                                            #
        if temperature == None:
            self.temperature = "constant"
            pass
        else:
            self.temperature = temperature
            pass
                                                                                            #
                                                                                            # time unit
                                                                                            #
        if timeUnit:
            if type(timeUnit) != bytes:
                raise TypeError(" the time unit argument of the ChemicalTransportProblem must be a string ")
            pass
        self.timeUnit = timeUnit
                                                                                            #
                                                                                            # outputs treatment
                                                                                            #
        if outputs:
            outputs1 = toList(outputs)
            verifyClassList(outputs1, ExpectedOutput)

            if not hasattr(self,'output_names'):
                self.output_names=[]
                pass
            for output in outputs1:
                if output.getName() in self.output_names:
                    msg = '\n\nDifferent outputs should not share the same name.\n'
                    msg+= 'End of the hydraulic problem run.\n\n'
                    raise msg
                self.output_names.append(output.getName())
                pass
        #
        self.outputs = outputs
        #
        return None

    def getActivityLaw(self):
        """
        Get ChemicalTransportProblem activity law 
          Ouput : 
            (None or activityLaw) 
            """
        return self.activityLaw

    def getBooleanPorosityOption(self):
        """
        Get ChemicalTransportProblem porosity option (constant or variable)
          Ouput : 
            0 (if constant porosity) or 1 (if variable)
        """
        if (self.porosityState == 'variable'): return 1
        else: return 0

    def getBoundaryConditions(self):
        """
        To get the boundary conditions
        """
        return self.boundaryConditions

    def getCalculationTimes(self):
        """get calculation times"""
        return self.calculationTimes
        

    def getChemistryDB(self):
        """
        Get ChemicalTransportProblem  data base
          Ouput : 
            (string) 
            """
        return self.chemistryDB
        
    def getDarcyVelocity(self): 
        """
        Get ChemicalTransportProblem  Darcy velocity, 
        which can be a vector, a string or None
        """
        print("within getDarcyVelocity self.darcyVelocity",self.darcyVelocity)
        return self.darcyVelocity

    def getDensity(self):
        """get the solid density"""
        return self.solidDensity

    def getchemistryDB(self):
        """
        Get ChemicalTransportProblem  data base
          Ouput : 
            (string) 
            """
        return self.chemistryDB
        
    def getBooleanPorosityOption(self):
        """
        Get ChemicalTransportProblem porosity option (constant or variable)
          Ouput : 
            0 (if constant porosity) or 1 (if variable)
        """
        if (self.porosityState == 'variable'): return 1
        else: return 0
            
    def getPorosityOption(self):
        """
        Get ChemicalTransportProblem porosity option (constant or variable)
          Ouput : 
            a string: constant / varialble
        """
        return self.porosityState
        
    def getProcessingList(self):
        """
        To get the list of user defined methods to be processed
        """
        return self.processingList
        
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
        if (self.porosityState == 'variable'): self.variablePorosity = 1
        else: self.variablePorosity = 0
        return None

    def getDiffusionLaw(self):
        """
        Get ChemicalTransportProblem diffusion law 
          Ouput : 
            (None or DiffusionLaw) 
            """
        return self.diffusionLaw

    def getKineticLaws(self):
        """
        Get ChemicalTransportProblem kinetic laws 
          Ouput : 
            (None or list of kineticLaw) 
            """
        return self.kineticLaws

    def getSpeciesBaseAddenda(self):
        """
        Get ChemicalTransportProblem new species 
          Ouput : 
            (None or list of Species) 
            """
        return self.speciesBaseAddenda

    def getGravity(self):
        """get gravity"""
        return self.gravity

    def getInitialConditions(self):
        """get initial conditions"""
        return self.initialConditions

    def getMPIEnv(self):
        """
        to control the simulation environment: self.mpiEnv is None: the simulation is sequential
        """
        return self.mpiEnv

    def getName(self):
        """
        To get the name of the mechanical problem
        """
        return self.name

    def getOutputs(self):
        """get expected outputs"""
        return self.outputs

    def getPermeabilityLaw(self):
        """
        Get ChemicalTransportProblem diffusion law 
          Ouput : 
            (None or DiffusionLaw) 
            """
        return self.permeabilityLaw
            
    def getPorosityOption(self):
        """
        Get ChemicalTransportProblem porosity option (constant or variable)
          Ouput : 
            a string: constant / varialble
        """
        return self.porosityState

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

    def getThermalOption(self):
        if (self.temperature.lower() in ["timeDependent","true","variable"]):
           thermalOption = 1    # we consider a thermal field
           self.fluidThermalConductivity = getfluidThermalConductivity(25.)
           #
           # the volumic Heat Capacity here is given here in J/kg/m3
           #
           self.waterVolHCapacity =  4.189e+6
           pass
        else:
           thermalOption = 0    # the temperature field is constant
           self.fluidThermalConductivity = None
           self.waterVolHCapacity = None
           pass
        return thermalOption

    def getTimeUnit(self):
        """
        Get ChemicalTransportProblem time uniot
          Ouput : 
            (None or String) 
        """
        return self.timeUnit

    def getUserProcessing(self):
        """
        To get user processing control parameter
        """
        return self.userProcessing
        
    def getVariableHeadPorosityOption(self):
        """
        Get ChemicalTransportProblem porosity option (constant or variable)
        \return  0 (if head constant) or 1 (if head and porosity variable )
        """
        if (self.headVPorosity == 'variable'): return 1
        else: return 0
        
    def getViscosity(self):
        """get viscosity"""
        return self.viscosity
                                                                                            #
                                                                                            # boundaryConditions treatment
                                                                                            #
class BoundaryCondition( CommonBoundaryCondition):
    """
    BoundaryCondition definition
    Boundaries can be expressed in terms of displacement, forces and of a chemical state related to chemistry.
    """
    def __init__(self, boundary, btype, value, porosity = None, description = None):
        """Boundary condition initialisation with :
        - one or several boundary(ies) (object (Body) Region). The objet is a region in order to be able to treat several materials
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
        
        boundaryConditionDico = makeDico(Dirichlet=[Displacement, NormalForce, Pressure, ChemicalState])
        #print boundaryConditionDico.keys()
        #raw_input()
        CommonBoundaryCondition.__init__(self, boundary, btype, value, boundaryConditionDico, description)
        BoundaryCondition.porosity = porosity
        ok = 0
        for val in value:
            if val.__class__.__name__ == "ChemicalState":
                ok = 1
                self.chemicalState = val
                break
            pass
        if ok == 0:
            raise Warning(" the association of a chemical state to a boundary is mandatory ")
        ok = 0
        for val in value:
            if val.__class__.__name__ in ["Displacement","NormalForce"]:
                ok = 1
                self.value = val
                break
            pass
        if ok == 0:
            raise Warning(" check the definition of boundary conditions")
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
        - The value is of type Displacement, temperature or chemical state
        """
        CommonInitialCondition.__init__(self, body, value)
        for val in value:
            memberShip(val,[Displacement, Temperature, ChemicalState])
        ok = 0
        for val in value:
            if val.__class__.__name__ == "ChemicalState":
                ok = 1
                self.chemicalState = val
                break
            pass
        if ok == 0: raise Warning(" the association of a chemical state to a boundary is mandatory ")
        ok = 0
        for val in value:
            if val.__class__.__name__ in ["Displacement","NormalForce"]:
                ok = 1
                self.value = val
                break
        if ok == 0: raise Warning(" check the definition of the initial condition linked to").with_traceback(body.bodyName)
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
