# -*- coding: utf-8 -*-
"""

Used to define an Elmer file to be used with the:

                 Darcy solver for saturated flows
                 
                 Richards solver for unsaturated flows

Varying boundary conditions can be introduced as linear functions 

"""
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Name : ElmerHydro
#
# Description :
#
#
# Author    :   A. Dimier
#
# Date      :   04 12 2009
#
# Modified  :   30/10/2010 introduction of varying hydraulic B.C.
#
# Modified  :   12/01/2011 polishing
#
# Modified  :   08/05/2011 introduction of Richards
#               
#               to comply with the Elmer solver we use total head as variable
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from datamodel import TimeTabulatedFunction, LinearFunction, PolynomialFunction

from elmertools import *

from exceptions import Exception

from elmerroot import ElmerRoot

try:
    pass
#    import DarcyCurrentSolve
except ImportError:
    print 'Unable to import the elmer module'

import exceptions
#from functions import LinearFunction
import functions
from os import system
import subprocess
import string
import sys
from posttables import Table
from tensors import Tensor,Tensor3D,Tensor2D,IsotropicTensor
import types
from tensors import Tensor,Tensor3D,Tensor2D,IsotropicTensor
from types import StringType
from typechecktools import verifyItem,verifyClass
from vector import V as Vector

from PhysicalProperties import SpecificStorage

from wrappertools import *

import WElmer

class ElmerHydro(ElmerRoot):
    """ 
    Basic hydraulic class for Elmer component
    
    The default simulation type is steady. In that case, the elmer solver is launched. 
    Otherwise, the WElmer shared object takes the transient simulation into account.
    """
    #
    #---------------------------------------------------------------------------
    #---------------------------------------------------------------------------
    #
    def __init__(self, meshFileName="elmerMesh", saturation = None):
    
	ElmerRoot.__init__(self,meshFileName)
        self.problemName                = "hydraulic problem"
        self.module                     = "hydro"
        self.meshType                   = "msh"
        self.meshFileName               = meshFileName
        if saturation == None:
            self.saturation             = "saturated"
        elif type(saturation) == StringType and saturation.lower() in ["unsaturated","unsaturated"]:
            self.saturation             = saturation.lower()
        else:
            #raise Warning, " check the saturation parameter, it has been set to its default value "
            self.saturation             = "saturated"
        self.calc_type                  = ""
        self.title                      = "hydraulic with elmer"
        self.srcDict={}
        self.permHydroDictList=[]
        self.dirichletDict={'nbTypeCal':0,
                            'nbTimeCal':0,
                            'nbFac':[], 
                            'valCalT':[],
                            'indFac':[]}
        self.neumannDict ={'nbTypeCal':0,
                           'nbTimeCal':0,
                           'nbFac':[],
                           'valCalT':[],
                           'indFac':[]}
        self.gradientDict ={'nbTypeCal':0,
                           'nbTimeCal':0,
                           'nbFac':[],
                           'valCalT':[],
                           'indFac':[]}
        self.dirichletPressDict={'nbTypeCal':0,
                                 'nbTimeCal':0,
                                 'nbFac':[], 
                                 'valCalT':[],
                                 'indFac':[]}
        self.neumannPressDict ={'nbTypeCal':0,
                                'nbTimeCal':0,
                                'nbFac':[], 
                                'valCalT':[],
                                'indFac':[]}
        self.mixtePressDict={'nbTypeCal':0,
                             'nbTimeCal':0,
                             'nbFac':[], 
                             'valCalT':[],
                             'indFac':[]}
        self.calcTimesDico              = Dico()

        self.meshType                   = "msh"
#
        self.gravityDirection           = Vector(0.,-1.,0.)
        self.gravityValue               = 9.78
#
        self.mesh                       = self.meshFile
        self.meshType                   = "msh"
        self.meshDico                   = Dico()
        self.calcTimesDico ['finalTime']= 0.5
        self.density                    = 1000. # water density under standard conditions, density is
        self.initHydro                  = []
        self.massVolT                   = None
        self.nbMassVol                  = 1
        self.nbPoros                    = 1
        self.nbStorageCoefficient       = 1
        self.nbTimes                    = 0
        self.nbViscos                   = 1
        self.porosity                   = None
        self.viscosity                  = None
#
        self.simulationType             = "Steady"
        self.sifFileName                = "htest.sif"
        self.specificStorage            = SpecificStorage(0.0)      
        self.setDefaultParameters(self.chargeParameterDico)
        self.setChargeSolverDefaults()

        return None

    def launch(self):
        """
        Method to launch the simulation,
        interactivally (transient) or directly (steady state)
        """
	#
	# ELMERSOLVER_STARTINFO is the file enabling Elmer to be launched
	#
	self.elmerStartInfo = open("ELMERSOLVER_STARTINFO","w")
	self.elmerStartInfo.write(self.sifFileName)
	self.elmerStartInfo.close()
	#
        self.createSifFile()
        if self.simulationType == "Transient":
            print "dbgpy launching WElmer"
            self.essai = WElmer
            print "dbgpy reading the sif file"
            self.essai.initialize()
#            raw_input("dbg elmerhydro launch")

    def run(self):

        self.launch()
#        retcode = subprocess.Popen("ElmerSolver " + "htest.sif", shell=True)
#        if retcode < 0:
#            print >>sys.stderr, "Child was terminated by signal", -retcode
#        else:
#            print >>sys.stderr, "Child returned", retcode
#        print retcode
        if self.simulationType == "Steady":
            #self.essai.oneSHTimeStep()
            system("$ELMER_SOLVER htest.sif")
        elif self.simulationType == "Transient":
            #system("ElmerSolver htest.sif")
            print " ////////////////// dbg elmersolver transient //////////////////"
            t = 0.0
            while t < self.calcTimesDico ['finalTime']:
                self.essai.oneSHTimeStep()
                print " dbg elmerhydro oneSHTimeStep over",timeStepSizes
                self.setTimeStep(self.timeStepSizes)
                t = t + min(self.timeStepSizes,self.calcTimesDico['finalTime']-t)
#                raw_input(" dbg one hydraulic time step is over")
            pass
        pass

    def oneTimeStep(self):
        """
        one hydraulic time step
        """
        self.essai.oneSHTimeStep()
        
    def setBoundaryConditions(self,boundaryConditions):
        print " debug eh setBoundaryConditions",boundaryConditions,type(boundaryConditions)
        self.boundaryConditions = boundaryConditions

    def setBodyList(self,bodies):
        """
        We give access of bodies list to elmer, bodies
        """
        self.bodies = bodies
        return None

    def setSimulationKind(self,simulationType = None):
        """
        To set the kind of simulation to handle, steady or transient
        """
        if type(simulationType) is StringType:
            if simulationType.lower() in ["steady"]:
                self.simulationType = "Steady"
            else:
                self.simulationType = "Transient"
        else:
           self.simulationType ="Steady"

    setSimulationType = setSimulationKind

    def setTimeStep(self,dt):
        """
        You set here the time step
        """
        self.essai.dt(dt)

    def setInitialConditions(self,initialConditions):
        """
        to set initial conditions
        """
        print " debug eh setinitialConditions",initialConditions
        self.initialConditions = initialConditions

    def createSifFile(self):
        """
        This method is used to generate the sif file. The sif
        file is the one read by the Elmer solver.
        Parameters relevant to time and time step
        are not relevant, the time step being driven through python.
        """
        self.sifFile = sifFile = open(self.sifFileName,"w")
        sifFile.write("Check Keywords Warn\n\n")
        sifFile.write("Header\n")
        sifFile.write("Mesh DB \".\" \"" + self.meshDirectoryName+"\"\n")
        sifFile.write("Include Path \".\"\n")
        sifFile.write("Results Directory \"\"\nEnd\n\n")
        #
        if self.simulationType.lower() == "steady":
            self.writeSimulation()
            pass
        elif self.simulationType.lower() == "transient":
            self.writeSimulation()
            pass
        self.writeConstants()
        self.writeBodies()
        self.writeMaterial()
#        self.writeBodyForce()
        self.writeEquation()
        self.writeSolver()
        self.writeBoundaryCondition()
        self.writeInitialCondition()
        sifFile.close()

    def writeEquation(self):
        sifFile = self.sifFile
        sifFile.write("! ~~\n! Equation p28 ref. Manual\n! ~~\n\n")
        string = "1 2"

        sifFile.write("Equation 1\n")
        sifFile.write("  Active Solvers(%i) = %s\n"%(2,string))

        sifFile.write("End\n\n")
        return None

    def writeSimulation(self):
        sifFile = self.sifFile
        sifFile.write("Simulation\n")
        #
        #       2D meshes: a cartesian or a delaunay mesh is identical in its identification
        #
        sifFile.write("  Coordinate System = \"Cartesian "+self.mesh.getDimensionString()+"\"\n\n")
        sifFile.write("  Simulation Type = \""+self.getSimulationType()+"\"\n")
#        sifFile.write("  Steady State Max Iterations ="+self.getSteadyStateMaxIter()+"\n\n")
        sifFile.write("  Coordinate Mapping(3) = 1 2 3\n")
#        raw_input("simulationTyp:  "+str(self.simulationType))
        if not self.simulationType == "Steady":
            self.getTimeStepIntervals()
            sifFile.write("  Timestepping Method = "+self.getTimeSteppingMethod()+"\n")
            if self.getTimeSteppingMethod() == "BDF":
                if int(self.getBDFOrder())>0 and int(self.getBDFOrder())< 6 :
                    sifFile.write("  BDF Order = "+str(self.getBDFOrder())+"\n")
                else :
            	    raise Exception("BDF Order must integer between 1 and 5")
            else:
                sifFile.write("  \n")
            sifFile.write("  Solver Input File = %s\n"%(self.sifFileName))
            sifFile.write("  Timestep Sizes = "+str(self.timeStepSizes)+"\n")
            sifFile.write("  Timestep Intervals = "+str(self.timeStepIntervals)+"\n")
                
#            sifFile.write("  Newmark Beta 0.0\n\n")
        else:
                sifFile.write("  Steady State Max Iterations = 1\n")
                sifFile.write("  Output Intervals = 1\n")
                sifFile.write("  Solver Input File =  \"%s\"\n"%(self.sifFileName))
                sifFile.write("  Output File = \"HeVel.dat\"\n")
                sifFile.write("  Post File = \"HeVel.ep\"\n")
        sifFile.write("End\n\n")
        return None

    def writeSolver(self):
        sifFile = self.sifFile
        sifFile.write("! ~~\n! Solver p27 ref. Manual\n! ~~\n")
                                                                                                                #
                                                                                                                # only charge is treated
                                                                                                                #
        if (self.saturation == "saturated"):
            sifFile.write("Solver %i\n"%(1))
            sifFile.write("  Exec Solver = \"%s\"\n"%("Always"))
            sifFile.write("  Equation = \"%s\"\n"%("Darcy Equation"))

            if self.simulationType == "Transient":
                sifFile.write("  Procedure = \"SaturatedDarcyTimeStep\" \"SaturatedDarcyTimeStepSolver\"\n")
            else:
                sifFile.write("  Procedure = \"DarcySolve\" \"DarcySolver\"\n")
            sifFile.write("  Variable = \"%s\"\n"%("Charge"))
            sifFile.write("  Variable Dofs = %i\n"%(1))
        elif (self.saturation == "unsaturated"):
            sifFile.write("Solver %i\n"%(1))
            sifFile.write("  Exec Solver = \"%s\"\n"%("Always"))
            sifFile.write("  Equation = \"%s\"\n"%("WRichardsSolver"))
            sifFile.write("  Procedure = File \"WRichardsSolver\" \"WRichardsSolver\"\n")
            sifFile.write("  Variable = %s\n"%("Total Head"))
            sifFile.write("!  Discontinuous Galerkin = Logical True ! not operational yet\n")
            sifFile.write("! Uses saturated conditions (pure Darcy flow) for the 1st iteration\n")
            sifFile.write("  Saturated Initial Guess = True\n")
            
          

        if self.chargeParameterDico["algebraicResolution"] != "Direct":
           self.chargeParameterDico['linearSystemSolver'] = "Iterative"
        else:
           # a corriger
           sifFile.write("  Linear System Direct Method = %s\n"%self.chargeParameterDico["linear System Iterative Method"])

        sifFile.write("  Linear System Solver = \"%s\"\n"%self.chargeParameterDico['Linear System Solver'])
        sifFile.write("  Linear System Iterative Method = \"%s\"\n"%self.chargeParameterDico["Linear System Iterative Method"])
        sifFile.write("  Linear System Max Iterations = %s\n"%self.chargeParameterDico["Linear System Max Iterations"])
        sifFile.write("  Linear System Convergence Tolerance = %e\n"%self.chargeParameterDico["Linear System Convergence Tolerance"])
        sifFile.write("  Linear System Preconditioning = \"%s\"\n"%self.chargeParameterDico["Linear System Preconditioning"])
        sifFile.write("  Steady State Convergence Tolerance = %s\n"%self.chargeParameterDico["Steady State Convergence Tolerance"])
        #sifFile.write("  Linear System Direct Method = %s\n"%self.chargeParameterDico["Linear System Direct Method"])

        if self.chargeParameterDico['stabilize'] == True:
            sifFile.write("  Stabilize = True\n")
        else:
            sifFile.write("  Stabilize = True\n")

        if (self.saturation == "saturated"):
            sifFile.write("  Namespace = string \"charge\"\n")
        else:
            sifFile.write("  Namespace = string \"Total Head\"\n")
            sifFile.write("  Nonlinear System Max Iterations = %s\n"%self.chargeParameterDico["Nonlinear System Max Iterations"])
            sifFile.write("  Nonlinear System Convergence Tolerance = %s\n"%self.chargeParameterDico["Nonlinear System Convergence Tolerance"])
            sifFile.write("  Nonlinear System Convergence Measure = solution\n")
            sifFile.write("  Nonlinear System Relaxation Factor = %s\n"%self.chargeParameterDico["Nonlinear System Relaxation Factor"])
            
        
        sifFile.write("End\n\n")
#
#                       charge has been treated, now we have to extract the velocity
#
        if (self.saturation == "saturated"):
            sifFile.write("Solver %i\n"%(2))
            sifFile.write("  Equation = ComputeFlux\n")
            sifFile.write("  Procedure = \"DFluxSolver\" \"DFluxSolver\"\n")

            sifFile.write("  Flux Variable = String \"Charge\"\n")
            #
            # the two terms should disappear
            #
            sifFile.write("  Flux Coefficient = String \"Hydr Conductivity\"\n")
            sifFile.write("  Flux Coefficient = String \"Saturated Hydraulic Conductivity\"\n")

#            sifFile.write("  Procedure = \"AdvectionDiffusionTimeStep\" \"AdvectionDiffusionTimeStepSolver\"\n")
            sifFile.write("  Linear System Convergence Tolerance = %e\n"
            %(self.chargeParameterDico["Flux Parameter"]))
        else:
            sifFile.write("Solver %i\n"%(2))
            sifFile.write("  Equation = RichardsFlux\n")
            sifFile.write("  Procedure = \"WRichardsSolver\" \"WRichardsPostprocess\"\n")
            sifFile.write("  Linear System Convergence Tolerance = %e\n"
            %(self.chargeParameterDico["Linear System Convergence Tolerance"]))
        
            sifFile.write("  Flux Multiplier = Real %s\n"%(self.chargeParameterDico["Flux Multiplier"]))

        sifFile.write("End\n\n")

        return None

    def writeBodies(self):
        """
        Bodies are asociated to materials and equations. Only one equation is treated when temperature is set to None. 
        Otherwise, two equations are taken into account. So, bodies are associated to initial conditions and their number
        mostly depends on material numbers.
        """
        sifFile = self.sifFile
        sifFile.write("! ~~\n! Body\n! ~~\n")
        indb = 0
        ibc = 0
        print "writing bodies "
        #raw_input(" type de self.boundaryConditions")
        for ibc in range(len(self.boundaryConditions.keys())):
            print " body treatment ", self.boundaryConditions[ibc]
            sifFile.write("Body %i\n"%(self.boundaryConditions[ibc]["ind"]))
            sifFile.write("  Name = \"body%s\"\n"%(self.boundaryConditions[ibc]["ind"]))
            sifFile.write("  Equation = 1\n")
            stinds = _digit(0)
            stindb = str(ibc+1)+stinds
            #sifFile.write("  Material = %s\n"%(stindb))
            sifFile.write("  Material = %s\n"%(self.boundaryConditions[ibc]["ind"]))

            sifFile.write("End\n\n")
            
#
# doit etre modifie des que plusieurs materiaux interviennent
#            
        ibc+=1
        for initialCondition in self.initialConditions.keys():
#            sifFile.write("Body %i\n"%(indb+ibc+1))
            sifFile.write("Body %i\n"%(self.initialConditions[initialCondition]["ind"]))
            sifFile.write("  Equation = 1 \n")
            stinds = _digit(0)
            stindb = str(ibc+indb+1)+stinds
#            sifFile.write("  Material = %s\n"%(stindb))
#            sifFile.write("  Initial Condition = %s\n"%(indb+1))
            sifFile.write("  Material = %s\n"%(self.initialConditions[initialCondition]["ind"]))
            sifFile.write("  Initial Condition = %s\n"%(self.initialConditions[initialCondition]["ind"]))
#            sifFile.write("  Body Force = %s\n"%(indb+1))
            sifFile.write("  Body Force = %s\n"%(1))
            sifFile.write("End\n\n")
        return None

    def writeMaterial(self):
        """
        A loop over materials driven by the bodies
        Intrinsic permeability rho mu and gravity have to be defined.
        """
        sifFile = self.sifFile
        sifFile.write("! ~~\n! Material p29 ref. Manual\n! ~~\n")

        for indb in range(len(self.bodies)):
            stinds = _digit(0)
            stindb = str(indb+1)+stinds
            #sifFile.write("Material %s\n"%(stindb))
            sifFile.write("Material %s\n"%(self.bodies[indb].support.body[0]))
            sifFile.write("  Water Density = Real %15.10e\n"%(self.density))
            sifFile.write("  Viscosity = Real %15.10e\n"%(self.viscosity.getValue()))
            #
            # the two terms should disappear
            #
            sifFile.write("  Hydr Conductivity = Real %15.10e\n"\
                          %(self.bodies[indb].getMaterial().getHydraulicConductivity().value.value))
            sifFile.write("  Saturated Hydraulic Conductivity = Real %15.10e\n"\
                          %(self.bodies[indb].getMaterial().getHydraulicConductivity().value.value))
            sifFile.write("  Specific Storage = Real %15.10e\n"\
                          %(self.bodies[indb].getMaterial().getSpecificStorage().value))
            sifFile.write("  Porosity = Real %15.10e\n"%(self.bodies[indb].getMaterial().getPorosity().value))
#            sifFile.write(" Specific Storage = Real %15.10e\n"%(self.specificStorage.getValue()))
            sifFile.write("  Compressibility Model = Incompressible\n")
            if self.bodies[indb].getMaterial().saturationLaw != None:
                sifFile.write("  !~~~~~~~~~~~~\n")
                sifFile.write("  !~ saturation: %s\n"%(self.bodies[indb].getMaterial().saturationLaw.name))
                sifFile.write("  !~~~~~~~~~~~~\n")
                sifFile.write("  Porosity Model = \"%s\"\n"%(self.bodies[indb].getMaterial().saturationLaw.name))
                if self.bodies[indb].getMaterial().saturationLaw.name == "van Genuchten":
                    sifFile.write("  van Genuchten Alpha = %s\n"%(self.bodies[indb].getMaterial().saturationLaw.alpha))
                    sifFile.write("  van Genuchten N = %s\n"%(self.bodies[indb].getMaterial().saturationLaw.n))
                    sifFile.write("  van Genuchten M = %s\n"%(self.bodies[indb].getMaterial().saturationLaw.m))
                elif self.bodies[indb].getMaterial().saturationLaw.name == "exponential":
                    sifFile.write("  exp Alpha = %s\n"%(self.bodies[indb].getMaterial().saturationLaw.alpha))
                    sifFile.write("  exp N = %s\n"%(self.bodies[indb].getMaterial().saturationLaw.n))
                    sifFile.write("  exp C = %s\n"%(self.bodies[indb].getMaterial().saturationLaw.c))
            if (self.saturation != "saturated"):
                sifFile.write("  Residual Water Content = %s\n"%(self.bodies[indb].getMaterial().residualWaterContent.value))
                sifFile.write("  Saturated Water Content = %s\n"%(self.bodies[indb].getMaterial().saturatedWaterContent.value))
                pass
            sifFile.write("End\n\n")
        return None

    def writeBoundaryCondition(self):
        sifFile = self.sifFile
        sifFile.write("! ~~\n! Material p29 ref. Manual\n! ~~\n")
        ##
        ## Two kinds of boundary conditions: Dirichlet or Flux
        ##
        inds = 0
        for boundary in self.boundaryConditions.keys():
            #
            # Dirichlet Boundary. The head can vary lineary
            #
            if (self.boundaryConditions[boundary]["typ"].lower() == "dirichlet"):
                stinds = _digit(boundary)
                stindb = str(1)+stinds
                sifFile.write("! %s\n"%self.boundaryConditions[boundary]["boundaryName"])
                sifFile.write("Boundary Condition %s\n"%stindb)
                #sifFile.write("  Target Boundaries (1) = %s\n"%str(boundary+1))
                sifFile.write("  Target Boundaries (1) = %s\n"%str(self.boundaryConditions[boundary]['ind']))
                print " 355dbg ",self.boundaryConditions[boundary]["head"].__class__.__name__
                if self.saturation == "saturated":
                    sifFile.write("! charge\n")
                else:
                    sifFile.write("! Total Head\n")
                if type(self.boundaryConditions[boundary]["head"]) == FloatType:
                    if self.saturation == "saturated":
                        sifFile.write("  %s = Real %e\n"%("Charge", self.boundaryConditions[boundary]["head"]))
                    else:
                        sifFile.write("  %s = Real %e\n"%("Total Head", self.boundaryConditions[boundary]["head"]))
#                    print  type(self.boundaryConditions[boundary]["head"]).__name__
#                    print " toto",self.boundaryConditions[boundary]["head"]
                    pass
                elif isinstance(self.boundaryConditions[boundary]["head"], LinearFunction):
                    #string,ptuple = linear1DMatc(self.boundaryConditions[boundary], "head", variable = None)
                    #sifFile.write(string%("Charge",self.boundaryConditions[boundary]["head"]))
                    string, elementsToPrint = linear1DMatc(self.boundaryConditions[boundary], "head", variable = None)
#                    print "dbg elmerhydro ",string, elementsToPrint
                    sifFile.write(string%elementsToPrint)
#                    print  type(self.boundaryConditions[boundary]["head"]).__name__
#                    print " toto",self.boundaryConditions[boundary]["head"]
#                    raw_input("list type")
                    pass
                else:
                    raise Exception, " you have to check the type of the Head definition "
                sifFile.write(" End\n\n")
            elif (self.boundaryConditions[boundaryName]["typ"].lower() == "neumann"):
            #
            # Neumann p 16 Elmer models manual
            #
#                sifFile.write("Boundary Condition %s\n"%stindb)
#                sifFile.write("  Target Boundaries (1) = %s\n"%str(dirBC[1]))
#                sifFile.write("  Charge Flux BC = True\n")                    
#                sifFile.write("  Charge flux %e\n"%(dirBC[-1][-1]))                    
#                sifFile.write("End\n\n")
                pass
            inds+=1
        return None

    def writeInitialCondition(self):
        """
        We can have two kinds of initial conditions: 
        
        a constant head or a variable  head introduced via the MATC language:
        
        Head = Variable Coordinate 2
        Real MATC "20*tx"
        
        """
        sifFile = self.sifFile
        inds = 0        
        sifFile.write("! ~~\n! initial condition p8 ref. ElmersolverManual\n! ~~\n")
        print self.initialConditions
        for initialConditionName in self.initialConditions.keys():
            inds+=1
            sifFile.write("Initial Condition %s\n"%self.initialConditions[initialConditionName]["ind"])
            ind = 0
            if type(self.initialConditions[initialConditionName]["head"]) == FloatType:
                sifFile.write("  %s = Real %e\n"%("Charge", self.initialConditions[initialConditionName]["head"]))
            elif isinstance(self.initialConditions[initialConditionName]["head"], LinearFunction):
                string, elementsToPrint = linear1DMatc(self.initialConditions[initialConditionName], "head", variable = None)
                sifFile.write(string%elementsToPrint)
                pass
            sifFile.write("End\n")
        return None

    def setDensity(self, density):
        """ 
        A scalar to set density
        """
        self.density = density.getValue()
        return None

    def setGravity(self, gravity):
        """ 
        A scalar or a vector to define the gravity
        """
        self.gravity = gravity
        if isinstance(self.gravity,Vector):
            if len(self.gravity) != 3:
                raise Whoops,"Gravity vector has not the right dimension"
            self.absoluteGravity=self.gravity.magnitude()
        elif isinstance(self.gravity,float):
            self.absoluteGravity=abs(self.gravity)
            pass
        else:
            raise Whoops,"gravity has to be a scalar or a vector"
                        
        if abs(self.absoluteGravity)<1e-100:
            self.absoluteGravity = 9.78
        return None

    def setViscosity(self , viscosity):
        """
        Used to set viscosity
        """
        self.viscosity = viscosity
        return None

    def setIntrinsicPermeability(self, inpermeability):
        """
        Used to set an intrinsic permeability field
        """
        self.setPermea(inpermeability,'inperm')
        return None
        
    def setMesh(self,  mesh):
        """
	to set or reset the name or the mesh
        """        
        self.mesh  = mesh
        return None
        
    def setPermeability(self , permeability):
        """ Used to set a permeability field
        """
        self.setPermea(permeability,'perm')
        return None

    def setPermea(self, field, type):
        """
        That function is used to set permeability and setIntrinsicPermeability.
        """
        self.defineElmerZones(field)        
        
        spaceDimensions = self.meshDico['spaceDimensions']

        if type=='inperm':
            hCCoef = 1
            rho = self.density
            g = self.absoluteGravity
            mu = self.viscosity
        elif type=='perm':
            self.viscosity = self.absoluteGravity * self.density
            rho = self.density
            g = self.absoluteGravity
            if hasattr(self,'facticegravity'):
                g = max(self.absoluteGravity,self.facticegravity)
                pass
            mu = rho*g
#            print 'self.absoluteGravity,self.density,self.viscosity',self.absoluteGravity,self.density,self.viscosity
#            mu = self.viscosity
            hCCoef = rho*g/mu
        else:
            raise Whoops("Not Allowed permeability")
#        print 'type,hCCoef',type,hCCoef

        self.hCCoef=rho*g/mu
#        raw_input(" valeur du coeff : "+str(self.hCCoef))
        i=0
        permHydroDictList = []

        nbZones = field.getNbZones()
        field=field.amult(musurroger_ou_1)
        for zoneInd in range(nbZones):
            zone       = field.getZone(zoneInd)
            zoneName   = zone.getName()
            val        = field.getZoneValues(zoneInd)

            permHydroDictList.append({})
            permHydroDictList[i]['nbzones'] = nbZones
            
            permT = []
            if len(val) == 1:
# Considering isotropic tensors, extra diagonal terms are set to zero
                if spaceDimensions == 2:

                    permT.append(val[0]) # kxx
                    permT.append(val[0]) # kyy
                    permT.append(0.)     # kxy
                else:

                    permT.append(val[0]) # kxx
                    permT.append(val[0]) # kyy
                    permT.append(0.)     # kxy
                    permT.append(val[0]) # kzz
                    permT.append(0.)     # kyz
                    permT.append(0.)     # kxz
            elif len(val) == 3:
                permT.append(val[0]) 	 # kxx
                permT.append(val[1]) 	 # kyy
                permT.append(val[2]) 	 # kxy
            elif len(val) == 6:
                permT.append(val[0]) 	 # kxx
                permT.append(val[2]) 	 # kyy
                permT.append(val[1]) 	 # kxy
                permT.append(val[5]) 	 # kzz
                permT.append(val[3]) 	 # kyz
                permT.append(val[4]) 	 # kxz
                pass
            print 'zone,permea',zoneName,permT
            permHydroDictList[i]['permT'] = permT
            i += 1
            pass
        self.permHydroDictList=permHydroDictList
        return

    def setPressureBoundaryCondition(self , pressurebc):
        """ set a field of pressure boundary condition
        """
        #field = pressurebc
        head_list_by_element=self.pressure2head(pressurebc)
        nbTimeCal = 2
        nbFac     = []
        indFac    = []
        valCalT   = []
        nbTypeCal = 0
        for li in head_list_by_element:
            nbTypeCal += 1
            el,val=tuple(li)
            if isinstance(val,Table):
                tnew=val
                nbTimeCal=max(nbTimeCal,tnew.getNbRows() )
                tnew.setTitle('Dirichlet')
            elif isinstance(val,float):
                tnew=Table('Dirichlet')
                tnew.addColumn('time',[0.,1.])
                tnew.addColumn('f(t)',[val,val])
                pass
            valCalT.append(tnew)
            nbFac.append(1)                
            indFac.append([el])
            pass
        self.dirichletPressDict={'nbTypeCal': nbTypeCal,
                                 'nbTimeCal': nbTimeCal,
                                 'nbFac':     nbFac,
                                 'valCalT':   valCalT,
                                 'indFac':    indFac}

        return

    def setPressureGradientBoundaryCondition(self , pressuregbc):
        """ set a field of pressure gradient boundary condition
        """
        head_list_by_element=self.pressure2head(pressuregbc)
        nbTimeCal = 2
        nbFac     = []
        indFac    = []
        valCalT   = []
        nbTypeCal = 0
        for li in head_list_by_element:
            nbTypeCal += 1
            el,val=tuple(li)
            if isinstance(val, Table):                    
                tnew = val
                tnew.setTitle('Neumann')
            else:
                tnew = Table('Neumann')
                tnew.addColumn('time',[0.,1.])
                tnew.addColumn('f(t)',[val, val])
                pass
            valCalT.append(tnew)
            nbFac.append(1)
            indFac.append([el])
            pass
        self.neumannPressDict={'nbTypeCal':nbTypeCal,
                               'nbTimeCal':nbTimeCal,
                               'nbFac':    nbFac, 
                               'valCalT':  valCalT,
                               'indFac':   indFac}

        return

    def setSource(self , source):
        """ set a field of source
        """
        spaceDimensions = self.meshDico['spaceDimensions']

        zones = source.getZones()
        field = source
        nbZones = field.getNbZones()
        valeurs = []
        for zoneInd in range(nbZones):
            #zone       = field.getZone(zoneInd)
            #zoneName   = zone.getName()
            val        = field.getZoneValues(zoneInd)
            valeurs.append(val)
            
        nbTypeSrc = nbZones

        nbTimeSrc   = 1
        indZone     = 0
        listTimeTab = []
        dictValeurs = []
        for val in valeurs:
            zone = zones[indZone]
            if isinstance(val[0], float):
                dictValeurs.append({
                    'nbTypeSrc': nbTypeSrc,
                    'time': [0.0],
                    'val': [val[0]],
                    'numerozone': indZone,     
                    'nbNm': zone.getNbElements(),      
                    'mailSrc': zone.getGlobalIndexes(), 
                    'timetab': 0
                    })
                
            elif isinstance(val[0], TimeTabulatedFunction):
                dictValeurs.append({
                     'nbTypeSrc': nbTypeSrc,
                     'time': val[0].getTimeCoefficient().getColumn(0).tolist(),      
                     'val':  val[0].getTimeCoefficient().getColumn(1).tolist(),       
                     'numerozone': indZone,
                     'nbNm':zone.getNbElements(),
                     'mailSrc': zone.getGlobalIndexes(),
                     'timetab':val[0].getTimeCoefficient()
                     })
            elif isinstance(val[0], LinearFunction):
                globalface = zone.getGlobalIndexes()
                baryField  = zone.getBarycenters()
                points     = baryField.getValues()
                newPoint = []

                for indP in range(0, len(points), spaceDimensions):
                    px = points[indP]
                    py = points[indP+1]
                    if spaceDimensions == 2:
                        newPoint.append((px, py))
                    else:
                        pz = points[indP+2]
                        newPoint.append((px, py, pz))
                for indElem in range (zone.getNbElements()):
                    point = newPoint[indElem]
                    eval = val[0].eval(point)
                    dictValeurs.append({
                        'nbTypeSrc':len(newPoint),
                        'time':[0.0],
                        'val':[val[0].eval(point)],
                        'numerozone':indZone,
                        'nbNm':1,
                        'mailSrc': [globalface[indElem]],
                        'timetab':0
                        })
            else:
                raise Whoops('Not Yet Implemented')
          
            indZone += 1
            
        listTimeTab=[]
        for valeurs in dictValeurs:
            if valeurs['timetab']:
                newtab=valeurs['timetab']
                indZone=valeurs['numerozone']
                newtab.setTitle("%s" %indZone)
                listTimeTab.append(newtab)
                
        if listTimeTab:
            listTimeTab=tuple(listTimeTab)
            listTimeTab=getTimeUnifiedTables(*listTimeTab)
            timeref=listTimeTab[0].getColumn(0).tolist()
            nbTimeSrc=listTimeTab[0].getNbRows()

        for timeTab in listTimeTab:
            indZone=string.atoi(timeTab.getTitle())
            time=timeTab.getColumn(0).tolist()
            val=timeTab.getColumn(1).tolist()
            dictValeurs[indZone]['time']=time
            dictValeurs[indZone]['val']=val
            dictValeurs[indZone]['timetab']=1
        if listTimeTab:
            #si certaines sources dependent du temps alors il faut aligner les
            #autres valeurs non dependantes du temps :
            for valeurs in dictValeurs:
                if (not valeurs['timetab']):
                    indZone=valeurs['numerozone']
                    dictValeurs[indZone]['time']=timeref
                    newval=valeurs['val']*nbTimeSrc
                    dictValeurs[indZone]['val']=newval

        #Calcul du nombre d'Elements concerernes par un puit/source
        nmSrc=0
        for valeurs in dictValeurs:
            nmSrc+=valeurs['nbNm']
            dictValeurs[0]['nmSrc']=nmSrc
            # Attention seul le premier dictionnaire contiendra ce nombre total !!
            
        self.srcDict = dictValeurs
        return
        
    def getSimulationKind(self):
        return self.simulationType
        
    getSimulationType = getSimulationKind
        
    def getSteadyStateMaxIter(self):
        return self.chargeParameterDico["Steady State Max Iterations"]
	
    def getTimeSteppingMethod(self):
        return self.chargeParameterDico["Timestepping Method"]
        return timeStepIntervals, timeStepSizes
        
    def setTimeDiscretisation(self,timeStepIntervals = None, timeStepSizes = None):
        """
        Setting time steps through the number of time Steps or the size of time steps.
        Every time, a real is used. It should become a list.
        """
        if timeStepIntervals != None:
            self.timeStepIntervals = timeStepIntervals
        elif timeStepSizes != None:
            self.timeStepSizes = timeStepSizes
        else:
            raise Warning, "You should give at least an argument to the setTimeDiscretisation function"

    setCalculationTimes = setTimeDiscretisation
	
    def getTimeStepIntervals(self,timeStepIntervals = None):
        """
        That function is used as a control for the time step in 
        """
        if timeStepIntervals == None:
            if self.timeStepIntervals == None:
                raise Exception, " You should define the time discretisation for a transient hydraulic problem"
        else:
                self.timeStepIntervals = timeStepIntervals
        self.timeStepSizes = self.calcTimesDico ['finalTime']/self.timeStepIntervals
        return None
	
    def getBDFOrder(self):
        return self.chargeParameterDico["BDF Order"]

    def getDarcyVelocity(self):
        """ 
        To return the darcy velocity field        
        """
        return self.darcyVelocity
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
    def getDensityGravity(self):
        if not hasattr(self,'density'):
            raise Exception," Density should be defined"
        if not hasattr(self,'gravity'):
            raise Exception," Density should be defined"
        return self.density, self.gravity
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
    def pressure_HeadPressure(self,pressureField,way='go'):
        """
        The problem solved through elmer needs charge boundary conditions.
        Having a field of Pressure Boundary Condition we transform it
        in head boundarycondition by the relation: H = (P - Po)/(ro*g) + z -zo
        """
        density, gravity = self.getDensityGravity()
        roger=density*gravity
        mul=1./roger
        if way=='go':
            return pressureField.amult(mul)
        elif way=='back':
            return pressureField.amult(roger)
        pass
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
    def setParameter(self,**parameters):
        """
        To assign the different numerical parameters 
        """
#        print " debug ",type(self.chargeParameterDico)
        for key, value in parameters.items():
            if key == "linearSystemSolver":
                self.chargeParameterDico['Linear System Iterative Method'] = value
            if key == "linearSystemIterativeMethod":
                self.chargeParameterDico['Linear System Iterative Method'] = value
            
            if key == "linearSystemMaxIterations":
                self.chargeParameterDico['Linear System Max Iterations']   = value
            
            if key == "linearSystemConvergenceTolerance":
                self.chargeParameterDico['Linear System Convergence Tolerance'] = value
            if key == "fluxMultiplier":
                self.chargeParameterDico['Flux Multiplier'] = value
            if key == "linearSystemPreconditioning":
                self.chargeParameterDico['Linear System Preconditioning'] = value
            if key == "steadyStateConvergenceTolerance":
                self.chargeParameterDico['Steady State Convergence Tolerance'] = value
            if key == "stabilize":
                self.chargeParameterDico['Stabilize'] = value
            #
            # non linear parameters => richards solver
            #
            if key == "nonlinearSystemMaxIterations":
                self.chargeParameterDico["Nonlinear System Max Iterations"] = value
            if key == "nonlinearSystemConvergenceTolerance":
                self.chargeParameterDico["Nonlinear System Convergence Tolerance"] = value
            if key == "nonlinearSystemConvergenceMeasure":
                self.chargeParameterDico["Nonlinear System Convergence Measure"] = value
            if key == "nonlinearSystemRelaxationFactor":
                self.chargeParameterDico["Nonlinear System Relaxation Factor"] = value

#            verifyItem(key, self.chargeParameterDico)
#            self.chargeParameterDico[key] = value

    def pressure2Head(self, funcfield, Rho=1, g=-9.8):
        """
        To convert a pressure boundary condition in a head boundary condition
        """
        spaceDimensions  = self.meshDico['spaceDimensions']
        rho = self.density
        g = self.absoluteGravity
        roger = rho*g
        mul = 1./roger
        
        field   = funcfield
        nbZones = field.getNbZones()
        head    = []

        #gr  = tuple(self.gravity.getValues())
        grunit = self.gravity.toUnitVector()
        gr  = tuple(grunit.getValues())
        dim = self.dimensions

        indexMax = 0
        for indZone  in range(nbZones):
            zone          = field.getZone(indZone)
            #ent = zone.getEntity()
            globalIndexes = zone.getGlobalIndexes()
            indexMax = max(indexMax,max(globalIndexes))
            pass
##         print "indexMax,self.meshDico['nbElements'], self.meshDico['nbFaces'] :",\
##               indexMax,self.meshDico['nbElements'], self.meshDico['nbFaces']
        if indexMax > max(self.meshDico['nbElements'], self.meshDico['nbFaces']):
            raise exceptions.Exception('cas non prevu (pressure2head)')
        for indZone  in range(nbZones):
            zone          = field.getZone(indZone)
## ##             z             = zone.getHeights()
## ##             extCompoz = z.extractComponentValues(1)
##
## ***********************************************************
##
            coo = zone.getBarycenters().getValues()
            extCompoz=[]
            for i in range(0,len(coo),dim):
                h=0.
                for n in range(dim):
                    h=h-gr[n]*coo[i+n]
                    pass
                extCompoz.append(h)
                #extCompoz.extend([gr[n]*coo[i+n]] for n in range(dim)])
                pass
##             print 'extCompoz',extCompoz
##             print 'len(extCompoz)',len(extCompoz)
##             print 'len(coo),dim',len(coo),dim
##             print 'coo( maille 900)',coo(899
##             print "self.meshDico['nbElements'] ",self.meshDico['nbElements'] 
##
## ***********************************************************
##
            globalIndexes = zone.getGlobalIndexes()
            val           = field.getZoneValues(indZone)[0]
            #print 'val',val
##             print 'val',val
##             raise toto
            if isinstance(val, list):
                # cas mixte
                pressureA = val[0].getValues()[0]
                pressureB = val[0].getValues()[1]
                pressureC = val[0].getValues()[2]
               
                ind=0
                for zi in extCompoz:
                    resA = mul*pressureA+zi
                    resB = mul*pressureB+zi
                    resC = mul*pressureC+zi
                    head.append((globalIndexes[ind], resA, resB, resC))
                    ind = ind+1
            elif isinstance(val, float):
                # cas general : FLOAT
                pressure = val
                #z = zone.getHeights()
                
                ind = 0
                #print 'len(globalIndexes)',len(globalIndexes)
                for zi in extCompoz:
                    calcu = mul*pressure+zi
                    #print 'globalIndexes[ind],mul,pressure,zi,calcu',globalIndexes[ind],mul,pressure,zi,calcu
                    head.append([globalIndexes[ind],calcu])
##                     if globalIndexes[ind] == 1:
##                         print '\n\n'
##                         print 'MAILLE 1 : pressure,head :',pressure,calcu
##                         print 'GRAVITY, DENSITY',self.absoluteGravity,self.density
##                         print '\n\n'
##                         #print extCompoz
##                         print '\n\n      FIN LISTING pressure2head\n\n'
##                         pass
                        
                        
                    #if globalIndexes[ind] == 900:raise toto
                    ind += 1
                    pass
                #raise toto
            elif isinstance(val,TimeTabulatedFunction):
                pressure=val
                #z=zone.getHeights()
                ind = 0
                for zi in extCompoz:
                    tabletime=pressure.getTimeCoefficient()
                    valcolumn=tabletime.getColumn(1)
                    newval=[]
                    for vv in valcolumn:
                        newval.append( mul*vv+zi )
                        print 'pressure %e  ==> head %e'%(vv,mul*vv+zi)
               

                    tabletime.setColumn( 1, newval )
                   
                    head.append([globalIndexes[ind],tabletime])
                    ind+=1
           
            elif isinstance(val,PolynomialFunction) or isinstance(val,LinearFunction):
                bary =  zone.getBarycenters()
                xx=bary.extractComponentValues(1)
                yy=bary.extractComponentValues(2)
                nbCoord = len(xx)
                if spaceDimensions==3: zz = bary.extractComponentValues(3)
                
                ind = 0
                for indCo in range(nbCoord):
                    x = xx[indCo]
                    hh = y = yy[indCo]
                    tupl=(x,y)
                    if spaceDimensions == 3:
                        hh = z = zz[indCo]
                        tupl=(x,y,z)
                        pass
##                     else:
##                         tupl=(x,y)
                    hh = extCompoz[indCo]
                    valf = val.eval(tupl)
                    head.append([globalIndexes[ind],valf/roger+hh])
##                     if spaceDimensions==2:
##                         head.append([globalIndexes[ind],valf/roger+hh])
##                     else:
##                         head.append([globalIndexes[ind],valf/roger+hh])
##                         pass
                    ind += 1
                    pass
                pass
            else:
                raise Exception, " Implementation failure"
            #print 'head_resultant',head
##             raise toto
        return head
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
    def pressureGradient2HeadGradient(self, funcfield, Rho=1, g=-9.8):
        """
        Convert a Pressure Boundary Condition to a Head Boundary Condition
        """
        spaceDimensions  = self.meshDico['spaceDimensions']
        rho = self.density
        g = self.absoluteGravity
        roger = rho*g
        mul = 1./roger
        
        field   = funcfield
        nbZones = field.getNbZones()
        head    = []
        for indZone  in range(nbZones):
            zone          = field.getZone(indZone)
            z             = zone.getHeights()
            globalIndexes = zone.getGlobalIndexes()
            val           = field.getZoneValues(indZone)[0]
            if isinstance(val, list):
                # cas mixte
                pressureA = val[0].getValues()[0]
                pressureB = val[0].getValues()[1]
                pressureC = val[0].getValues()[2]
               
                extCompoz = [0.]*len(z.extractComponentValues(1))
##                 extCompoz = z.extractComponentValues(1)
                ind=0
                for zi in extCompoz:
                    resA = mul*pressureA+zi
                    resB = mul*pressureB+zi
                    resC = mul*pressureC+zi
                    head.append((globalIndexes[ind], resA, resB, resC))
                    ind = ind+1
            elif isinstance(val, float):
                # cas general : FLOAT
                pressure = val
                z = zone.getHeights()
                
                extCompoz = [0.]*len(z.extractComponentValues(1))
##                 extCompoz = z.extractComponentValues(1)
                ind = 0
                for zi in extCompoz:
                    calcu = mul*pressure+zi
                    head.append([globalIndexes[ind],calcu])
                    ind += 1
            elif isinstance(val,TimeTabulatedFunction):
                pressure=val
                z=zone.getHeights()
                extCompoz = [0.]*len(z.extractComponentValues(1))
##                 extCompoz = z.extractComponentValues(1)
                ind = 0
                for zi in extCompoz:
                    tabletime=pressure.getTimeCoefficient()
                    valcolumn=tabletime.getColumn(1)
                    newval=[]
                    for vv in valcolumn:
                        newval.append( mul*vv+zi )
               

                    tabletime.setColumn( 1, newval )
                   
                    head.append([globalIndexes[ind],tabletime])
                    ind+=1
           
            elif isinstance(val,PolynomialFunction) or isinstance(val,LinearFunction):
                bary =  zone.getBarycenters()
                xx=bary.extractComponentValues(1)
                yy=bary.extractComponentValues(2)
                nbCoord = len(xx)
                if spaceDimensions==3: zz = bary.extractComponentValues(3)
                
                ind = 0
                for indCo in range(nbCoord):
##                     x = xx[indCo]
##                     y = yy[indCo]
##                     if spaceDimensions == 3:
##                         z = zz[indCo]
##                         tupl=(x,y,z)
##                     else:
##                         tupl=(x,y)
                    
##                     valf = val.eval(tupl)
##                     if spaceDimensions==2:
##                         head.append([globalIndexes[ind],valf/roger+y])
##                     else:
##                         head.append([globalIndexes[ind],valf/roger+z])
##                         pass
                    head.append([globalIndexes[ind],valf/roger])
                    ind += 1
            else:
               raise Exception, "has to be Implemented"
        raise 'False implementation. To be corrected.'   
        return head
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
    def head2Pressure(self,field, Rho=1, g=-9.8):
        """
        Convert a head field object in a Pressure list
        useful for the getOutput:

        En entree : un objet de class Field contenant des valeurs de type CHARGE
        En sortie : une liste de valeurs converties en PRESSION
        """
        rho   = self.density
        g     = self.absoluteGravity
        roger = rho*g

        head = field.getValues()
        zone = field.getSupport()
##
##         extCompoz=z.extractComponentValues(1)
##        
## ***********************************************************
##
        #gr  = tuple(self.gravity.getValues())
        grunit = self.gravity.toUnitVector()
        gr  = tuple(grunit.getValues())
        coo = zone.getBarycenters().getValues()
        dim = self.dimensions
        extCompoz=[]
        for i in range(0,len(coo),dim):
            h=0.
            for n in range(dim):
                h=h-gr[n]*coo[i+n]
                pass
            extCompoz.append(h)
            pass
##         for i in range(0,len(coo),dim):
##             extCompoz.extend([gr[n]*coo[i+n] for n in range(dim)])
##             pass
#
#***********************************************************
#
        
        ind=0
        press=[]
        for zi in extCompoz:
            pressure=(head[ind]-zi)*roger
            #print 'head,zi,roger,pressure',head[ind],zi,roger,pressure
##             if not ind :
##                 print '<methode head2pressure de ElmerHydro > :'
##                 print 'roger,Z,head,pressure',roger,zi,head[ind],pressure
##                 pass
            press.append(pressure)
            ind += 1
        
        return press
        
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
    def setHeadBoundaryCondition(self , headbc):
        """ set a field of Head Boundary Condition
        """
        spaceDimensions = self.meshDico['spaceDimensions']
        tempsref  = [0]
        nbTimeCal = 2
        nbFac     = []
        indFac    = []

        valCalT = []
        i = 0

        field = headbc
        nbZones = field.getNbZones()
        for zoneInd in range(nbZones):
            zone       = field.getZone(zoneInd)
            val        = field.getZoneValues(zoneInd)

            if isinstance(val[0], TimeTabulatedFunction):
                nbFac.append( zone.getNbElements() )
                indFac.append( zone.getGlobalIndexes() )
                tableTime=val[0].getTimeCoefficient().copy()
                tableTime.setTitle('Dirichlet')
                valCalT.append(tableTime) 
                nbTimeCal=tableTime.getNbRows()
    
            elif isinstance(val[0],float):
                nbFac.append( zone.getNbElements() )
                indFac.append( zone.getGlobalIndexes() )
                tnew=Table('Dirichlet')
                tnew.addColumn('time',[0.,1.])
                tnew.addColumn('f(t)',[val[0],val[0] ])
                valCalT.append(tnew)
                                
            elif isinstance(val[0],LinearFunction):
                baryField=zone.getBarycenters()
                points=baryField.getValues()
                newPoint=[]
                
                for indP in range(0, len(points), spaceDimensions):
                    px = points[indP]
                    py = points[indP+1]
                    if spaceDimensions==2:
                        newPoint.append((px, py))
                    else:
                        pz = points[indP+2]
                        newPoint.append((px, py, pz))

                for indElem in range (zone.getNbElements()):
                    nbFac.append(1)
                    indFac.append( [zone.getGlobalIndexes()[indElem]] )                   
                    tnew=Table('Dirichlet')
                    point=newPoint[indElem]                    
                    tnew.addColumn('time',[0.,1.])
                    tnew.addColumn('f(t)',[val[0].eval(point),val[0].eval(point)])
                    valCalT.append(tnew)
            else:
                print 'val',val
                print 'type de val[0]',type(val[0])
                print 'Instance ?',val[0].__class__.__name__
                raise Exception, "implementation failure"
            i+=1
    
        nbTypeCal=len(valCalT)

        self.dirichletDict={'nbTypeCal': nbTypeCal,
                            'nbTimeCal': nbTimeCal,
                            'nbFac':     nbFac,
                            'valCalT':   valCalT,
                            'indFac':    indFac}
        print "len(self.dirichletDict['valCalT'])",len(self.dirichletDict['valCalT'])
        return
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
    def setHeadGradientBoundaryCondition(self , headgbc): 
        """ set a field of Head Gradient Boundary Condition
        """

        if not hasattr(self,'rogersurmu'):
            self.rogersurmu=self.absoluteGravity * self.density/self.viscosity
            pass

        spaceDimensions = self.meshDico['spaceDimensions']
        nbTimeCal = 2
        nbFac   = []
        indFac  = []
        valCalT=[]

        field   = headgbc
        nbZones = field.getNbZones()
        for zoneInd in range(nbZones):
            valCalTZone=[]            
            zone       = field.getZone(zoneInd)
            #zoneName   = zone.getName()
            val        = field.getZoneValues(zoneInd)
            
            coef=-(self.rogersurmu*self.permHydroDictList[zoneInd]['permT'][0])

            if isinstance(val[0],TimeTabulatedFunction):
                tableTime=val[0].getTimeCoefficient().copy()
                tableTime=val[0].getTimeCoefficient().amult(coef)
                tableTime.setTitle('Gradient')
                valCalTZone.append(tableTime)
                nbTimeCal=tableTime.getNbRows()
            elif isinstance(val[0],float):
                tnew=Table('Gradient')
                tnew.addColumn('time',[0.,1.])
                tnew.addColumn('f(t)',[val[0]*coef,val[0]*coef ])
                valCalTZone.append(tnew)
                nbFac.append( zone.getNbElements() )
                indFac.append( zone.getGlobalIndexes() )
            elif isinstance(val[0],LinearFunction):
                baryField=zone.getBarycenters()
                points=baryField.getValues()
                newPoint=[]
                for indP in range(0, len(points), spaceDimensions):
                    px = points[indP]
                    py = points[indP+1]
                    if spaceDimensions==2:
                        newPoint.append((px, py))
                    else:
                        pz = points[indP+2]
                        newPoint.append((px, py, pz))
                        pass
                    pass
                for indElem in range (zone.getNbElements()):
                    nbFac.append(1)
                    indFac.append( [zone.getGlobalIndexes()[indElem]] )                   
                    tnew=Table('Gradient')
                    point=newPoint[indElem]
                    tnew.addColumn('time',[0.,1.])
                    tnew.addColumn('f(t)',[val[0].eval(point)*coef,val[0].eval(point)]*coef)
                    valCalTZone.append(tnew)
                    pass
                pass
            else:
                raise Exception, "implementation failure"
            if len(self.permHydroDictList[zoneInd]['permT']) != 1:
                for tab in valCalTZone:
                    va=map(abs,tab.getColumn('f(t)').tolist()[:])
                    if max(va) > 1e-200:
                        raise Exception,"HeadGradient B.C. eventually bounded to a scalar permeability"
                    pass
                pass
            valCalT.extend(valCalTZone)
            pass
            
        nbTypeCal=len(valCalT)

        self.gradientDict={'nbTypeCal': nbTypeCal,
                          'nbTimeCal': nbTimeCal,
                          'nbFac':     nbFac,
                          'valCalT':   valCalT,
                          'indFac':    indFac} 
  
        return
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
    def setFluxBoundaryCondition(self , headgbc): 
        """
        set a field of Head Gradient Boundary Condition
        """
        spaceDimensions = self.meshDico['spaceDimensions']
        nbTimeCal = 2
        nbFac   = []
        indFac  = []
        valCalT=[]
        
        field   = headgbc
        nbZones = field.getNbZones()
        for zoneInd in range(nbZones):
            zone       = field.getZone(zoneInd)
            val        = field.getZoneValues(zoneInd)
            print 'setFluxBoundaryCondition : VAL ?',val
            if isinstance(val[0],TimeTabulatedFunction):
                tableTime=val[0].getTimeCoefficient().copy()
                tableTime.setTitle('Neumann')
                valCalT.append(tableTime)
                nbTimeCal=tableTime.getNbRows()
                print '1len(valCalT)',len(valCalT)
    
            elif isinstance(val[0],float):
                tnew=Table('Neumann')
                tnew.addColumn('time',[0.,1.])
                tnew.addColumn('f(t)',[val[0],val[0] ])
                print 'flux_nul ?',val[0]
##                 raise stop
                valCalT.append(tnew)
                print '2len(valCalT)',len(valCalT)
                nbFac.append( zone.getNbElements() )
                indFac.append( zone.getGlobalIndexes() )
                
            elif isinstance(val[0],LinearFunction):
                baryField=zone.getBarycenters()
                points=baryField.getValues()
                newPoint=[]

                for indP in range(0, len(points), spaceDimensions):
                    px = points[indP]
                    py = points[indP+1]
                    if spaceDimensions==2:
                        newPoint.append((px, py))
                    else:
                        pz = points[indP+2]
                        newPoint.append((px, py, pz))

                for indElem in range (zone.getNbElements()):
                    nbFac.append(1)
                    indFac.append( [zone.getGlobalIndexes()[indElem]] )                   
                    tnew=Table('Neumann')
                    point=newPoint[indElem]
                    tnew.addColumn('time',[0.,1.])
                    tnew.addColumn('f(t)',[val[0].eval(point),val[0].eval(point)])              
                    valCalT.append(tnew)
                print '3len(valCalT)',len(valCalT)
            else:
                raise Exception, "to be Implemented"

        nbTypeCal=len(valCalT)
        print '4len(valCalT)',len(valCalT)

        self.neumannDict={'nbTypeCal': nbTypeCal,
                          'nbTimeCal': nbTimeCal,
                          'nbFac':     nbFac,
                          'valCalT':   valCalT,
                          'indFac':    indFac} 
        print "len(self.neumannPressDict['valCalT'])",len(self.neumannPressDict['valCalT'])
  
        return
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
    def setHeadMixedBoundaryCondition(self , headmbc):        
        """
        set a field of Head Mixed Boundary Condition
        """
        nbTimeCal=2
        nbFac=[]
        indFac=[]
        valCalT = []
        
           
        field   = headmbc
        nbZones = field.getNbZones()
        nbTypeCal = nbZones
        for zoneInd in range(nbZones):
            zone = field.getZone(zoneInd)
            #val  = field.getZoneValues(zoneInd)[0]
            val  = field.getZoneValues(zoneInd)
            if isinstance(val, Vector):
                abc = val._v
            elif type(val) == types.ListType:
                abc = val[:]
            else:
                raise Exception, "to be Implemented"

            if isinstance(abc[0],float):
                nbFac.append( zone.getNbElements() )
                indFac.append( zone.getGlobalIndexes() )
                tnewa=Table('MixteA')
                tnewb=Table('MixteB')
                tnewc=Table('MixteC')
                a=abc[0]
                b=abc[1]
                c=abc[2]
                tnewa.addColumn('time',[0.,1.])
                tnewa.addColumn('a',[a,a])
                tnewb.addColumn('time',[0.,1.])
                tnewb.addColumn('b',[b,b])
                tnewc.addColumn('time',[0.,1.])
                tnewc.addColumn('c',[c,c])
                valCalT.append(tnewa)
                valCalT.append(tnewb)
                valCalT.append(tnewc)
            elif isinstance(abc[0],TimeTabulatedFunction):
                nbFac.append( zone.getNbElements() )
                indFac.append( zone.getGlobalIndexes() )   
                tnewa=abc[0].getTimeCoefficient().copy()
                tnewb=abc[1].getTimeCoefficient().copy()
                tnewc=abc[2].getTimeCoefficient().copy()
                tnewa.setTitle('MixteA')
                tnewb.setTitle('MixteB')
                tnewc.setTitle('MixteC')
                nbTimeCal=max(nbTimeCal,tnewa.getNbRows())
                nbTimeCal=max(nbTimeCal,tnewb.getNbRows())
                nbTimeCal=max(nbTimeCal,tnewc.getNbRows())   
                valCalT.append(tnewa)
                valCalT.append(tnewb)
                valCalT.append(tnewc)
                pass
            pass
        self.mixteDict={'nbTypeCal': nbTypeCal,
                        'nbTimeCal': nbTimeCal,
                        'nbFac':     nbFac,
                        'valCalT':   valCalT,
                        'indFac':    indFac}
        
        return
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
def _digit(ind):
    if ind < 8:
        return "0"+str(ind+1)
    else:
      return str(ind+1)
