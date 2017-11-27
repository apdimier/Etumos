# -*- coding: utf-8 -*-
"""
file_elemerroot

That file entails an object common to all other elmer classes:
For the moment, two classes are created:
                elmerhydro      :       a velocity field is estimated.
                
                elmer           :       is used to be coupled with chemistry. The question is
                                        to know wether a saturated module and ans usaturated module must be created
                
                A generic sif file is created here
"""

from __future__ import absolute_import

from argparse import *

from elmertools import *

from exceptions import Exception

from mesh import Mesh

from generictools import        Generic,\
                                memberShip

from listtools import toList

#from tools import *

from listtools import elimCommonElementsInList

import os

import string

from types import NoneType

from vector import V
from six.moves import range
from six.moves import input

class ElmerRoot(Generic):
    """
    Elementary class, receptor of the common methods for elmer classes

    enabling to treat flow, heat, transport and mechanics.
    A two phase wellbore is currently included.

    elmer
    elmerhydro
    """
    def __init__(self, meshFile=None):

        self.chargeParameterDico = {}
        self.mechanicsParameterDico = {}
        self.gravityDirection                   = None
        self.porosityState                      = "constant"
        self.gravityValue                       = None
        self.meshFile = meshFile
        #print meshFile.__repr__()
        #raw_input("meshFile.__repr__")
        if meshFile.__repr__() in ["Mesh1D", "Mesh2D()", "Mesh3D()"]:
            if meshFile.__module__!= "mesh":
                raise Exception(" problem with the mesh to be considered\na one dimensional version should be created")
            pass
        if meshFile.getName()[-4:] == ".msh":
            self.meshFileName       = meshFile.getName()
            self.meshDirectoryName  = self.meshFileName[0:-4]
            pass
                                                                                            #
                                                                                            # the introduction of the heatParameterDico
                                                                                            # is made to structure of the data to be
                                                                                            # handled.
                                                                                            #
        self.heatParameterDico              = Dico()
        self.parameterDico              = Dico()
        #
        # as default parameter, we set the one dimensional borehole simulation parameter to false
        #
        self.parameterDico["oneDimensionalBoreHole"] = False
        self.parameterDico["vapor"]                  = False
        self.wellboreParameterDico = {}
        
        self.chemicalSolverVersion  = None
        self.temperature            = False
        self.oneDimensionalBoreHole = None
    #
    # by default, heat capacity and thermal conductivity are supposed to be constant
    #
        self.parameterDico["variableHeatCapacity"] = False
        self.parameterDico["variableHeatConductivity"] = False
        

    def acreateSifFile(self):
        """
        This method is used to generate the sif file. The sif
        file is the one read by the Elmer solver.
        Parameters related to time and time step
        are not relevant, the time step being driven through python.
        """
        self.sifFile = sifFile = open(self.sifFileName,"w")
        sifFileW = self.sifFile.write
        sifFileW("Check Keywords Warn\n\n")
        sifFileW("Header\n")
        sifFileW("Mesh DB \".\" \""+self.meshDirectoryName+"\"\nEnd\n\n")
        sifFileW("Include Path \".\"\n")
        sifFileW("Results Directory \"\"\nEnd\n\n")
        writeSimulation()
        self.writeConstants()
        self.writeBodies()
        self.writeMaterial()
        self.writeEquation()
        self.writeSolver()
        #
        self.writeBoundaryCondition()
        self.writeInitialCondition()
        sifFile.close()
        return None

    def writeConstants(self):
        sifFileW = self.sifFile.write
        sifFileW("! ~~\n! Constants\n! ~~\n")        
        sifFileW("Constants\n")
        gVector = self.gravityDirection
        sifFileW(" Gravity(4) = %i %i %i %e\n"%(gVector[0],gVector[1],gVector[2],self.gravityValue))
        if self.temperature: sifFileW(" Stefan Boltzmann = %e\n"%(0.0))
        if self.temperature: sifFileW(" Water Heat Capacity = Real %15.10e\n"%(self.waterHeatCapacity)) # J/kgK
        if self.temperature: sifFileW(" Water Heat Conductivity = Real %15.10e\n"%(self.waterHeatConductivity)) # W/mK
        #
        #
        #
        #if self.temperature: sifFile.write(" groundTemperature = Real %15.10e\n"%(15.0)) # C degree
        #if self.temperature: sifFile.write(" earthTemperatureGradient = Real %15.10e\n"%(0.08)) # C degree

        sifFileW("End\n\n")
        return None

    def getGravityDirection(self):
        return self.gravityDirection

    def setGravityDirection(self,stringDirection):
        """
        A direction is set through direction naming: X, Y, Z
        """
        if stringDirection.lower() == "x":
            self.gravityDirection = V(-1,0,0)
            pass
        if stringDirection.lower() == "y":
            self.gravityDirection = V(0,-1,0)
            pass
        if stringDirection.lower() == "z":
            self.gravityDirection = V(0,0,-1)
            pass
        return self.gravityDirection

    def getGravityValue(self):
        return self.gravityValue
        
    def rawInput(self,arg):
        return input("dbg"+self.__class__.__name__ +" "+str(arg))

    def setChargeSolverDefaults_old(self):
        self.chargeParameterDico["hydroSolverId"]                       = 1
        self.chargeParameterDico["equation"]                            = "Darcy Equation"
        self.chargeParameterDico["procedure"]                           = "DarcySolve" "DarcySolver"
        self.chargeParameterDico["variable"]                            = "Charge"
        self.chargeParameterDico["dof"]                                 = 1
        self.chargeParameterDico["algebraicResolution"]                 = "Iterative"
        self.chargeParameterDico["linearSystemSolver"]                  = "Iterative"
        self.chargeParameterDico['Linear System Iterative Method']      = "BiCGStab"
        self.chargeParameterDico['Linear System Max Iterations']        = 50
        self.chargeParameterDico['Linear System Convergence Tolerance'] = 1.0e-11
        self.chargeParameterDico["linearSystemAbortNotConverged"]       = True
        self.chargeParameterDico['Linear System Preconditioning']       = "ILU0"
        self.chargeParameterDico["linearSystemResidualOutput"]          = 1
        self.chargeParameterDico["steadyStateConvergenceTolerance"]     = 1.0e-06
        self.chargeParameterDico["stabilize"]                           = "True"
        self.chargeParameterDico['Timestepping Method']                 = "BDF"
        self.chargeParameterDico["BDF Order"]                           = 1
        self.chargeParameterDico["Flux Parameter"]                      = 5.e-3
        self.chargeParameterDico["Flux Multiplier"]                     = 1.e-9

    def setChargeSolverDefaults(self):
        """
        We set here the default parameters associated to the charge solver
        
        Shared parameters are in the setDefaultParameters
        
        """
        self.chargeParameterDico["hydroSolverId"]                          = 1
        self.chargeParameterDico["equation"]                               = "Darcy Equation"
        self.chargeParameterDico["procedure"]                              = "DarcySolve" "DarcySolver"
        self.chargeParameterDico["variable"]                               = "Charge"
        self.chargeParameterDico["linearSystemSolver"]                     = "Iterative"

        self.chargeParameterDico["linearSystemAbortNotConverged"]          = True
        self.chargeParameterDico["linearSystemResidualOutput"]             = 1
        
        self.chargeParameterDico['steadyStateConvergenceTolerance']        = 1.0e-06
        #
        # The stabilize parameter appears in setDefaultParameters
        #
        self.chargeParameterDico["stabilize"]                              = "True"
        self.chargeParameterDico["BDF Order"]                              = 1
        self.chargeParameterDico["Flux Parameter"]                         = 5.e-1
        self.chargeParameterDico["Flux Multiplier"]                        = 1.e-9
        #
        # non linear parameters
        #
        self.chargeParameterDico["Nonlinear System Max Iterations"]        = 100
        self.chargeParameterDico["Nonlinear System Convergence Tolerance"] = 1.0e-6
        self.chargeParameterDico["Nonlinear System Convergence Measure"]   = 100
        self.chargeParameterDico["Nonlinear System Relaxation Factor"]     = 1.0


    def setMechaSolverDefaults(self):
        """
        We set here the default parameters associated to the algebraic solver
        associated to the resolution of the linear elasticity equations
        
        Shared parameters are in the setDefaultParameters
        
        """
        self.mechanicsParameterDico["algebraicResolution"]                   = "Iterative"
        self.mechanicsParameterDico["Linear System Solver"]                     = "Iterative"
        self.mechanicsParameterDico["Linear System Iterative Method"]           = "BiCGStab"
        self.mechanicsParameterDico["Linear System Max Iterations"]             = 200
        self.mechanicsParameterDico["Linear System Convergence Tolerance"]      = 1.e-08
        self.mechanicsParameterDico["Linear System Preconditioning"]            = "ILU1"
        self.mechanicsParameterDico["Linear System ILUT Tolerance"]             = 0.001
        self.mechanicsParameterDico["Linear System Abort Not Converged"]        = False
        self.mechanicsParameterDico["Linear System Precondition Recompute"]     = 2
        self.mechanicsParameterDico["Linear System Residual Output"]            = 10

        
        self.mechanicsParameterDico['steadyStateConvergenceTolerance']          = 1.0e-10
        #
        # The stabilize parameter appears in setDefaultParameters
        #
        self.mechanicsParameterDico["stabilize"]                                = "False"
        self.mechanicsParameterDico["stabilize"]                                = "False"
        self.mechanicsParameterDico["lumpedMassMatrix"]                         = "False"
        self.mechanicsParameterDico["Bubbles"]                                  = "True"
        self.mechanicsParameterDico["optimizeBandWidth"]                        = "True"
        self.mechanicsParameterDico["BDF Order"]                                = 1
        self.mechanicsParameterDico["Flux Parameter"]                           = 5.e-1
        self.mechanicsParameterDico["Flux Multiplier"]                          = 1.e-9
        #
        # non linear parameters
        #
        self.mechanicsParameterDico["Nonlinear System Newton After Iterations"] = 3
        self.mechanicsParameterDico["Nonlinear System Max Iterations"]          = 15
        self.mechanicsParameterDico["Nonlinear System Convergence Tolerance"]   = 1.0e-8
        self.mechanicsParameterDico["Nonlinear System Convergence Measure"]     = 100
        self.mechanicsParameterDico["Nonlinear System Relaxation Factor"]       = 0.75


    def setDefaultParameters(self,parameterDico = None):
        """
        default parameter values for elmer, see the manual p 30
        
        Time Stepping Method can be either euler explicit, Crank Nicholson or BDF
        
         in the case where the scheme is a Crank Nicholson scheme
         0. explicit scheme
         1  fully implicit
         
         Between 0 and 1 : weighted scheme, see Hirsch

         range from 1 to 5
         self.parameterDico['BDF Order']                     = "5"
        """
        if parameterDico == None:
            parameterDico = self.parameterDico
            pass
        parameterDico['Timestepping Method']      = "BDF"
        parameterDico['thetaScheme']    = Dico()
        #
        parameterDico['thetaScheme'] ["ALL"] =  0
        #
        # steady state
        #self.parameterDico['Steady State Max Iterations'] = "2"
        # the two following terms are array values, see the solver manual p. 30
        parameterDico['Timestep Intervals']            = "100"
        parameterDico['Timestep Sizes']                = "10."
        # see the round.sif file for that term, it enables a variable time step size definition         
        parameterDico['Timestep Function']             = "Real"
        parameterDico['Lumped Mass Matrix']            = False
        # number of unknowns at a single node, it must stay to 1                
        parameterDico['Variable DOFs']                 = 1
         #  is a string:        "Cartesian 1D", "Cartesian 2D", "Cartesian 3D", "Cylindric" 
        parameterDico['Coordinate System']             = "Cartesian 3D"
         # name of the default equation to be solved. It will change in the future du to porosity addition
        parameterDico['Equation']                      = "Advection Diffusion"
         # name of the unknown for the system to be solved
        parameterDico['Variable']                      = "CB"
        parameterDico["Procedure"]                     = "AdvectionDiffusionTimeStep" "AdvectionDiffusionTimeStepSolver"
        parameterDico['Simulation Type']               = "Transient"
        
        parameterDico["algebraicResolution"]                   = "Iterative"
        parameterDico['Linear System Solver']                  = "Iterative"
         # possible values are CG CGS BiCGStab TFQMR GMRES
        parameterDico['Linear System Iterative Method']        = "BiCGStab"
        parameterDico['Linear System Max Iterations']          = 200
        parameterDico['Linear System Convergence Tolerance']   = 1.0e-8
        parameterDico['Linear System Preconditioning']         = "ILU1"
        parameterDico['Linear System ILUT Tolerance']          = 1.0e-03
        parameterDico['Linear System Symmetric']               = "False"
        parameterDico['Lumped Mass Matrix']                    = "False"
        #
        parameterDico['Nonlinear System Max Iterations']       = 1
        parameterDico['Nonlinear System Convergence Tolerance']= 1.0e-4
        parameterDico['Nonlinear System Newton After Tolerance']= 1.0e-3
        parameterDico['Nonlinear System Newton After Iterations']= 10
        parameterDico['Nonlinear System Relaxation Factor']    = 1
        parameterDico['Steady State Convergence Tolerance']    = 1.e-4
         
        parameterDico['Optimize Bandwidth']       = "True"
         # can be useful to stabilize the solution procedure in a convection case
        parameterDico['Stabilize']                = "False"
         # used in case of convection, default value is True
        parameterDico['Bubbles']                  = "True"
        parameterDico['Mesh']                     = self.meshFileName
        parameterDico['Mesh Input File']          = self.meshFileName
        parameterDico["BDF Order"]                = 1
#         self.parameterDico[]               = 1
        parameterDico["oneDimensionalBoreHole"]              = False    
        return None

    def setPorosityState(self, porosityOption):
        """
        the porosity option is usually retrieved from the problem, see  the ctm module
        """
        #raw_input(" within elmerroot porositystate: " + porosityOption)
        self.porosityState = porosityOption
        


    def setSorptionLaw(self):
        """
        is people ask for 
        """
        for spec in range(len(self.speciesNamesList)):
            specName = self.speciesNamesList[spec]
            self.sorptionLawDico[specName] = Dico()   
            self.sorptionLawDico[specName]['NOSORP'] =  None
            pass


        return

    def setGravityValue(self,gravityValue):
        """
        to set the gravity
        """
        self.gravityValue = gravityValue


    def setWellboreSolverDefaults(self):
        """
        We set here the default parameters of the algebraic solver
        associated to the resolution of the 2 phase mass flow for a wellbore.
        
        Shared parameters are in the setDefaultParameters
        
        """
        self.wellboreParameterDico["algebraicResolution"]                      = "Iterative"
        self.wellboreParameterDico["Linear System Solver"]                     = "Iterative"
        self.wellboreParameterDico["Linear System Iterative Method"]           = "BiCGStab"
        self.wellboreParameterDico["Linear System Max Iterations"]             = 200
        self.wellboreParameterDico["Linear System Symmetric"]                  = False
        self.wellboreParameterDico["Linear System Convergence Tolerance"]      = 1.e-08
        self.wellboreParameterDico["Linear System Preconditioning"]            = "ILU1"
        self.wellboreParameterDico["Linear System ILUT Tolerance"]             = 0.001
        self.wellboreParameterDico["Linear System Abort Not Converged"]        = False
        self.wellboreParameterDico["Linear System Precondition Recompute"]     = 2
        self.wellboreParameterDico["Linear System Residual Output"]            = 10

        
        self.wellboreParameterDico['steadyStateConvergenceTolerance']          = 1.0e-10
        #
        # The stabilize parameter appears in setDefaultParameters
        #
        self.wellboreParameterDico["stabilize"]                                = "False"
        self.wellboreParameterDico["lumpedMassMatrix"]                         = "False"
        self.wellboreParameterDico["Bubbles"]                                  = "True"
        self.wellboreParameterDico["optimizeBandWidth"]                        = "True"
        self.wellboreParameterDico["BDF Order"]                                = 1
        self.wellboreParameterDico["Flux Parameter"]                           = 5.e-1
        self.wellboreParameterDico["Flux Multiplier"]                          = 1.e-9
        #
        # non linear parameters
        #
        self.wellboreParameterDico["Nonlinear System Newton After Iterations"] = 3
        self.wellboreParameterDico["Nonlinear System Max Iterations"]          = 15
        self.wellboreParameterDico["Nonlinear System Convergence Tolerance"]   = 1.0e-8
        self.wellboreParameterDico["Nonlinear System Convergence Measure"]     = 100
        self.wellboreParameterDico["Nonlinear System Relaxation Factor"]       = 0.75
