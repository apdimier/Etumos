"""

 Module representing the coupling between mechanical and chemical phenomena?
 
 The case to be run are in the ~/Wrapper/Tests/Mechanics/ChemBrasiliantest directory
                               
"""
# -*- coding: utf-8 -*-
#/usr/bin/python
from __future__ import absolute_import
from __future__ import print_function
from etuser import *

from generictools import GenericCTModule

from typechecktools import verifyClass, verifyClassList

from chemicaltransportmodule import ChemicalTransportModule

from hydraulicmodule import HydraulicModule

from physicallaws import IntrinsicPermeabilityLaw,\
                         KozenyCarmanLaw,\
                         VermaPruessLaw
from types import IntType
#
# Here, the user module is imported to enable the introduction of a young modulus function
#
from user import *

class CoupledTHMC():
    """
    That class is used to enable a straightforward coupling of a:
    
    one phase Navier Linear elasticity solver with a chemical transport

    Initially the only enabled tools are:

    phreeqC as chemical tool and

    Elmer as flow, mechanical and transport tool

    The time step is evaluated in the chemical transport module.

    Once the elmer files are established, elmer and phreeqC are launched.

    The advection/diffusion solver is driven by the chemical transport module and

    the mechanical solver is driven by the WMcoupledCT module, more explicitly by its

    run method or its specific oneTimestep method.

    Due to the fixed point algorithm, the chemistry is the tool driving the time step.
    
    The evolution of the young modulus is driven by the porosity evolution. A user function defined
    
    at the user level establishes the new young modulus field which is imposed to the stress solver.

    """
    def __init__(self, problem, mesh, chemicalTransportModule = None,
                 mechanicalModule = None, elasticityLaw = None, MechaFrequency = None, algorithm = None) :
        """
        We give here the chemical transport module.
 
        The elasticity is driven by the porosity change and is defined through the elasticityLaw parameter
        
        can be :    None or "userdefined" 
        """
        if isInstance(problem, THMCProblem):
            self.problem = THMCProblem
        else:
            raise Warning(" the problem class should be THMC instead of "+str(problem.__class__.__name__))
        self.ChemicalTransportModule = ChemicalTransportModule
        ChemicalTransportModule.__init__(self)
        self.calculationTimes            = None
        self.density                     = None
        self.gravity                     = None
        self.matrixCompressibilityFactor = None
        self.porosity                    = None
        self.simulationType              = "Steady"
        self.sifFileName                 = "test.sif"
        self.timeStepIntervals           = None
        self.sourceField                 = None
        
        self.setCouplingAlgorithm(algorithm)
        self.setData (problem, trace = 0, mesh = mesh, algorithm = self.algorithm)
        #
        #
        #
        self.userPermeabilityLaw = None
        self.waterDynamicViscosity = 1.e-3  # kg/(m*s)
        ind= -1
        #
        # We check if a permeability law has been introduced by the user.
        #
        if self.userProcessing:
            for method in self.processingList:
                if isinstance(method, IntrinsicPermeabilityLaw) or "PermeabilityLaw" in method :
                    ind = self.processingList.index(method)
                    self.userPermeabilityLaw = method
                    print(" WD dbg user permeability law", method)
                    break
                    pass
                pass
            self.permeabilityLaw = method
            self.userPermeabilityLaw = True
            if ind>=0:
                del(self.processingList[ind])
                pass
            pass       
        elif permeabilityLaw != None and isinstance(permeabilityLaw, IntrinsicPermeabilityLaw):
            self.permeabilityLaw = permeabilityLaw
            pass
        else:
            raise Warning(" a permeability law should be associated to the algorithm")
        #
        # The hydraulic frequency corresponds to the frequency of the Darcy velocity evaluation.
        # For the moment hydraulic and chemistry share the same time step.
        # If hydraulic frequency is zero, Darcy velocity is evaluated only once.
        #
        if hydraulicFrequency == None:
            self.hydraulicFrequency = 0
            pass
        else:
            if type(hydraulicFrequency) == IntType:
                self.hydraulicFrequency = hydraulicFrequency
                pass
            else:
                raise Warning(" check the hydraulicFrequency setting,\n"\
                              +"it should be None or an integer")

        print(" WD dbg self.userPermeabilityLaw", self.userPermeabilityLaw)
        if (permeabilityLaw.lower() == "userdefined") or (self.userPermeabilityLaw != None):
            if (self.userPermeabilityLaw == None):
                if self.userProcessing == True:
                    raise Warning(" You have to set or to define a permeability law")
                pass
            pass
        elif (permeabilityLaw != None):
                                                                                            #
                                                                                            # available laws are described
                                                                                            # in physicalaws.py
                                                                                            #
            if isinstance(permeabilityLaw, IntrinsicPermeabilityLaw):
                self.permeabilityLaw = permeabilityLaw
                print(" WD permeabilityLaw ", self.permeabilityLaw)
                pass
            pass
        else:
            raise Warning(" You have to set or to define a permeability law")
        #
        # We have now a permeability and a hydraulic frequency
        #
        self.setUserPermeability()
                                 
    def setCouplingAlgorithm(self,algorithm):
        """
        Here we define a function enabling to define the coupling algorithm
        """
        if algorithm.lower() in ["cc","ni"]:
            self.algorithm = algorithm.upper()
            pass
        else:
            self.algorithm = "NI"
            pass
    def setHydraulicFrequency(self, newHydraulicFrequency):
        """
        The hydraulic frequency is set here. The hydraulic must be updated due to permeability evolution.
        It is set to 1 or zero. One ,if we want to evaluate hydraulic evolution over time and zero if just
        an initial velocity field is evaluated.
        """
        self.hydraulicFrequency = newHydraulicFrequency

        if self.hydraulicFrequency != 0:
            print("self.hydraulicFrequency",self.hydraulicFrequency)
            pass
        else:
            self.hydraulicFrequency = -1
            pass

    def setPermeabilityLaw(self, permeabilityLaw = None):
        """
        The default permeability law is set to the Kozeny one.
        A new permeability law can be introduced via the user module.
        The permeability is an intrinsic property. It is divided by the water dynamic viscosity to obtain the hydraulic conductivity which is used
        within the Darcy law.
        
        dynamic viscosity of water: 1.e-3 Pa.s = kg/(s.m)
        
        """
        if permeabilityLaw == None:
            from physicallaws import KozenyCarmanLaw
                                                                                            # The kozeny permeability law
                                                                                            # has fixed coefficients and is a
                                                                                            # function of porosity
            self.permeabilityLaw = "KozenyCarmanLaw"
            pass
        elif isinstance (permeabilityLaw, IntrinsicPermeabilityLaw):
            self.permeabilityLaw = permeabilityLaw
            pass
    def getOutput (self, name):
        """
        the outputs depend from the solver:
        
                charge and velocity     : transportSolver
                
                others                  : chemical ones
        """
        print("dbg getOutput\n", end=' ')
        if "velocity" == name.lower():
            return self.transportSolver.getVelocity ()
            print(" velocity end ")
            pass
        elif "charge" == name.lower():
            return self.transportSolver.getCharge ()
        elif "permeability" == name.lower():
            return self.transportSolver.getCharge ()
        else:    
            self.getOutput(name)
            pass
        
    def initialise (self):
        """
        The couple module is launched via the chemical transport module method:
        """
        self.launch()

    def run (self):
        """
        The evolution of the simulation is treated through a simple time step loop.
        
        The time step is driven by the chemical transport module.
        
        
        """
        self.initialise()
        #raw_input("initialise is over ")
        #self.transportSolver.setTimeStep(self.getTimeStep())
        #self.oneSHTimeStep ()
        #raw_input(" s h is over ")
        dthydr = 0.0
        while (self.simulatedTime < self.times[-1]): # should be replaced by the call of oneCoupledTimeStep within the while
            dt = self.getTimeStep()
            dthydr += dt
            self.oneChemicalTransportTimeStep ()
            print("self.hydraulicFrequency",self.hydraulicFrequency,\
                                self.timeStepNumber,self.timeStepNumber % self.hydraulicFrequency)
            #raw_input("self.hydraulicFrequency")
            if self.hydraulicFrequency  != 0:
                if self.timeStepNumber % self.hydraulicFrequency == 0 or self.timeStepNumber == 1:
                    print(" WDcoupledCT dbg permeability evaluation ",dthydr)
                    print("self.permeabilityLaw  ", self.permeabilityLaw)
                    print("self.userProcessing  ", self.userProcessing)
                    #raw_input("we evaluate the userPermeabilityLaw")
                    #self.transportSolver.setTimeStep(dthydr)
                    #
                    # To consider the case of multiple user's law, the user permeability law has been retrieved from the list
                    # and is pointed by the userPermeabilityLaw.
                    #
                    if self.permeabilityLaw != None and self.userProcessing:
                        print(" WDcoupledCT dbg permeabilityLaw", self.permeabilityLaw)
                        #raw_input("we evaluate the userPermeabilityLaw")
                    #for method in self.processingList:
                    #    print " method ",method,self.timeStepNumber
                    #    #raw_input("user processing ")
                    #    exec (method)
                        exec(self.userPermeabilityLaw)
                        #raw_input("we have evaluated the userPermeabilityLaw")
                        pass
                    elif (self.permeabilityLaw != None):
                        newPermeability = [self.permeabilityLaw.eval(porosity ) \
                                   for porosity in \
                                   self.ChemicalTransportModule.chemicalSolver.getPorosityField()]
                        self.transportSolver.setPermeabilityField(newPermeability)
                        pass

                        #self.transportSolver.setPermeabilityField(self.permeabilityLaw(porosity)/self.waterDynamicViscosity)
                    #
                    # u = -K(t) grad(H)
                    #
                    print("WD oneSHTimeStep")
                    self.oneSHTimeStep ()

                    dthydr = 0.
                    pass
                pass
            pass

    def oneElasticityTimeStep (self):
        """
        That method is used to solve the saturated transient flow.
        """
        print(" wd coupled oneSHTimeStep ")
        self.transportSolver.ElasticityOneTimeStep ()
        return None

    def oneCoupledTimeStep (self):
        """
        The evolution of the simulation is treated through a simple time step loop.
        """
        #
        # one chemical time step
        #
        #self.oneTimeStep()
        self.oneChemicalTransportTimeStep()
        #
        #
        #
        dt_chemistry = self.getTimeStep()
        #
        # new evaluation of the velocity field
        #
        if self.hydraulicFrequency != 0:
            #
            # new evaluation of the velocity field
            #
            if self.timeStepNumber % self.hydraulicFrequency==0 or self.timeStepNumber == 1:
                print(" WDcoupledCT dbg permeability evaluation in oneCoupledTimeStep")
                #porosityField = self.ChemicalTransportModule.chemicalSolver.getPorosityField()
                print(" length of the porosityfield oneCoupledTimeStep",\
                len(self.ChemicalTransportModule.chemicalSolver.getPorosityField()))
        #
        # updating of the permeability 
        #
                newPermeability = [self.permeabilityLaw(porosity ) \
                           for porosity in self.ChemicalTransportModule.chemicalSolver.getPorosityField()]
        #
        #
        #
                print(" length of the permeabilityfield ", len(newPermeability))
                print(" WDcoupledCT dbg -> permeability update")
                #
                #
                #
                self.transportSolver.setPermeabilityField(newPermeability)
                self.transportSolver.setTimeStep(dt_hydraulic)
                #
                # Il faut verifier que la vitesse est recuperee, sinon une methode doit etre creee.
                # 
                self.oneElasticityTimeStep()
                #raw_input(" WDcoupledCT dbg permeability evaluation")
                dt_hydraulic = 0.
                pass
            else:
                dt_hydraulic += dt_chemistry
                pass
            pass

    def stop(self):
        return None
