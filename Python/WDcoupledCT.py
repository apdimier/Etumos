"""

 Module in test phase
 
 The case to be run are in the ~/Wrapper/Tests/Chemicaltransport/Caprockintegrity/2d1 directory
                              
                              /home/dimier/Wrapper/Tests/Chemicaltransport/FlowComp1:
                              
                                test.py     coupling hydraulic and chemistry
                                
                                verma.py    coupling hydraulic and chemistry with a Verma-pruess law
                              
                              
 the file is Tests/Chemicaltransport/Caprockintegrity/testpv2d1.py
 
 For the moment, only an aqueous saturated phase is considered.
 
"""
# -*- coding: utf-8 -*-
#/usr/bin/python
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
# The user module is imported to enable the introduction of a new permeability function
#
from user import *

class WDcoupledCT(ChemicalTransportModule):
    """
    That class is used to enable a straightforward coupling of a:
    
    one phase Darcy flow with a chemical transport

    Initially the only enabled tools are:

    phreeqC as chemical tool and

    Elmer as flow and transport tool

    The time step is evaluated in the chemical transport module.

    Once the elmer files are established, elmer and phreeqC are launched.

    The advection/diffusion solver is driven by the chemical transport module and

    the flow solver is driven by the WDcoupledCT module, more explicitly by its

    run method or its specific oneTimestep method.

    Due to the fixed point algorithm, the chemistry is the tool driving the time step.

    The hydraulic conductivity is a function of the intrinsic permeability (m**2). That one

    can be a function of porosity or suction.

    See test.py in the $WTCT/FlowComp1 directory.

    It means that the hydraulic time evolution is only bounded to permeability evolution and not to the transient
    term associated to specific storage.

    """
    def __init__(self, problem, mesh, permeabilityLaw = None, hydraulicFrequency = None, algorithm = None) :
        """
        We give here the chemical transport module.
 
        The permeability law is by default the Kozeny one.
        
        But we can also introduce a user permeability law. The permeability law
        
        can be :    None or
        	        "userdefined" or 
        	        a permeability law predefined through python modules, Kozeny or Verma-Pruess

        """
        self.ChemicalTransportModule = ChemicalTransportModule
        ChemicalTransportModule.__init__(self)
        self.setCouplingAlgorithm(algorithm)
        self.setData (problem, trace = 0, mesh = mesh, algorithm = self.algorithm)
        #
        #
        #
        self.userPermeabilityLaw = None
        self.waterDynamicViscosity = 1.e-3	# kg/(m*s)
        ind= -1
        #
        # We check if a permeability law has been introduced by the user.
        #
        if self.userProcessing:
            for method in self.processingList:
                if isinstance(method, IntrinsicPermeabilityLaw) or "PermeabilityLaw" in method :
                    ind = self.processingList.index(method)
                    self.userPermeabilityLaw = method
                    print " WD dbg user permeability law", method
                    break
            self.permeabilityLaw = method
            self.userPermeabilityLaw = True
            if ind>=0:
                del(self.processingList[ind])
                pass
                
        elif permeabilityLaw != None and isinstance(permeabilityLaw, IntrinsicPermeabilityLaw):
            self.permeabilityLaw = permeabilityLaw
            pass
        else:
            raise Warning, " a permeability law should be associated to the algorithm"
        #
        # The hydraulic frequency corresponds to the frequency of the Darcy velocity evaluation.
        # For the moment hydraulic and chemistry share the same time step.
        # If hydraulic frequency is zero, Darcy velocity is evaluated only once.
        #
        if hydraulicFrequency == None:
            self.hydraulicFrequency = 0
        else:
            if type(hydraulicFrequency) == IntType:
                self.hydraulicFrequency = hydraulicFrequency
            else:
                raise Warning, " check the hydraulicFrequency setting,\n"\
                              +"it should be None or an integer"

        print " WD dbg self.userPermeabilityLaw", self.userPermeabilityLaw
        print dir(permeabilityLaw)
        if (self.userPermeabilityLaw) or (self.userPermeabilityLaw != None):
            if (self.userPermeabilityLaw == None):
                if self.userProcessing == True:
                    raise Warning, " You have to set or to define a permeability law"
        elif (permeabilityLaw != None):
                                                                                                            #
                                                                                                            # available laws are described
                                                                                                            # in physicalaws.py
                                                                                                            #
            if isinstance(permeabilityLaw, IntrinsicPermeabilityLaw):
                self.permeabilityLaw = permeabilityLaw
                print " WD permeabilityLaw ", self.permeabilityLaw
            pass
        else:
            raise Warning, " You have to set or to define a permeability law"
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
        else:
            self.algorithm = "NI"

    def setHydraulicFrequency(self, newHydraulicFrequency):
        """
        The hydraulic frequency is set here. The hydraulic must be updated due to permeability evolution.
        It is set to 1 or zero. One ,if we want to evaluate hydraulic evolution over time and zero if just
        an initial velocity field is evaluated.
        """
        self.hydraulicFrequency = newHydraulicFrequency

        if self.hydraulicFrequency != 0:
            print "self.hydraulicFrequency",self.hydraulicFrequency
        else:
            self.hydraulicFrequency = -1

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
        elif isinstance (permeabilityLaw, IntrinsicPermeabilityLaw):
            self.permeabilityLaw = permeabilityLaw
        
    def getOutput (self, name):
        """
        the outputs depend from the solver:
        
                charge and velocity     : transportSolver
                
                others                  : chemical ones
        """
        print "dbg getOutput\n",
        if "velocity" == name.lower():
            return self.transportSolver.getVelocity ()
            print " velocity end "
        elif "charge" == name.lower():
            return self.transportSolver.getCharge ()
        elif "permeability" == name.lower():
            return self.transportSolver.getCharge ()
        else:    
            self.getOutput(name)
        
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
            print "self.hydraulicFrequency",self.hydraulicFrequency,\
            				    self.timeStepNumber,self.timeStepNumber % self.hydraulicFrequency
            #raw_input("self.hydraulicFrequency")
            if self.hydraulicFrequency  != 0:
                if self.timeStepNumber % self.hydraulicFrequency == 0 or self.timeStepNumber == 1:
                    print " WDcoupledCT dbg permeability evaluation ",dthydr
                    print "self.permeabilityLaw  ", self.permeabilityLaw
                    print "self.userProcessing  ", self.userProcessing
                    #raw_input("we evaluate the userPermeabilityLaw")
                    #self.transportSolver.setTimeStep(dthydr)
                    #
                    # To consider the case of multiple user's law, the user permeability law has been retrieved from the list
                    # and is pointed by the userPermeabilityLaw.
                    #
                    if self.permeabilityLaw != None and self.userProcessing:
                        print " WDcoupledCT dbg permeabilityLaw", self.permeabilityLaw
                        #raw_input("we evaluate the userPermeabilityLaw")
            		#for method in self.processingList:
                	#    print " method ",method,self.timeStepNumber
                	#    #raw_input("user processing ")
                	#    exec (method)
                        exec(self.userPermeabilityLaw)
                        #raw_input("we have evaluated the userPermeabilityLaw")
                    elif (self.permeabilityLaw != None):
                        newPermeability = [self.permeabilityLaw.eval(porosity ) \
                		           for porosity in \
                		           self.chemicalSolver.getPorosityField()]
                        self.transportSolver.setPermeabilityField(newPermeability)
                        pass

                        #self.transportSolver.setPermeabilityField(self.permeabilityLaw(porosity)/self.waterDynamicViscosity)
                    #
                    # u = -K(t) grad(H)
                    #
                    print "WD oneSHTimeStep"
                    self.oneSHTimeStep ()

                    dthydr = 0.

    def oneSHTimeStep (self):
        """
        That method is used to solve the saturated transient flow.
        """
        print " wd coupled oneSHTimeStep "
        self.transportSolver.SaturatedHydraulicOneTimeStep ()
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
                print " WDcoupledCT dbg permeability evaluation in oneCoupledTimeStep"
                #porosityField = self.ChemicalTransportModule.chemicalSolver.getPorosityField()
                print " length of the porosityfield oneCoupledTimeStep",\
                len(self.ChemicalTransportModule.chemicalSolver.getPorosityField())
		#
		# updating of the permeability 
		#
                newPermeability = [self.permeabilityLaw(porosity ) \
                		   for porosity in self.ChemicalTransportModule.chemicalSolver.getPorosityField()]
		#
		#
		#
                print " length of the permeabilityfield ", len(newPermeability)
                print " WDcoupledCT dbg -> permeability update"
                #
                #
                #
                self.transportSolver.setPermeabilityField(newPermeability)
                self.transportSolver.setTimeStep(dt_hydraulic)
                #
                # Il faut verifier que la vitesse est recuperee, sinon une methode doit etre creee.
                # 
                self.oneSHTimeStep()
                #raw_input(" WDcoupledCT dbg permeability evaluation")
                dt_hydraulic = 0.
            else:
                dt_hydraulic += dt_chemistry
        pass

    def stop(self):
        return None
