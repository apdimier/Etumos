# -*- coding: utf-8 -*-
"""
class Elmer, enables to handle elmer as a transport tool
In fine should be able to launch elmer for linear and
non linear transport

The temperature is added as new.

Introduction of the elasticity solver.

Velocity: saturated

        For the moment, the velocity can be:

                constant:

                        In that case, the velocity is introduced as a Darcy velocity,
                        there are two ways to introduce the porosity :

                                1/ introducing the porosity coefficient in the effective diffusion coefficient,
                                   the porosity being set to one.

                                2/ introducing the real porosity.
                
                variable:

                        In that case, the velocity is introduced as a Darcy velocity

         If the porosity is varying 

"""

from elmertools import *

from exceptions import Exception

from elmerroot import ElmerRoot

from FortranFormat import FortranFormat, FortranLine

from generictools import memberShip

from listtools import toList

#from tools import *

from listtools import elimCommonElementsInList

import os

import string

import sys

from types import NoneType,StringType

from vector import V

from PhysicalProperties import Density,\
                               Velocity

import WElmer

_fe158 = FortranFormat("E15.8")
def _fote158(arg):
    return str(FortranLine([arg],_fe158))

_i10   = FortranFormat("I10")

def _foti10(arg):
    return str(FortranLine([arg],_i10))

class Elmer(ElmerRoot):
    """ Class used to define elmer as transport tool
        It enables to handle the following elmer keywords:
          Header
          Simulation
          Constants
          Body n
          Material n
          Body Force n
          Equation n
          Solver n
          Boundary Condition n
          Initial Condition n

    """
    def __init__(self, meshFileName="elmerMesh"):
        """
        meshFileName : mesh file name, with the extension .msh
        and that associated elmer format grid files are available
        """
        print " dbg elmer class instantation "
	ElmerRoot.__init__(self,meshFileName)
        self.__dict = {}
        self.advConv                    = "No"
        self.saturation                 = "saturated"
        self.dirBCList                  = []
        self.dirBCList1                 = []                                                # it should replace self.dirBCList
        self.dirICList                  = []
#        if meshFileName.getName()[-4:]  == ".msh":
#            print "toto"
            #raw_input()
#	    self.meshFileName           = meshFileName.getName()
#	    self.meshDirectoryName = self.meshFileName[0:-4]
        self.gravityDirection           = V(0,-1,0)
        self.gravityValue               = 9.78
        self.waterDensity               = 1000.0
        self.waterHeatCapacity          = 4187          # J/(kgK)
        self.waterHeatConductivity      = 0.60          # W/(mK)
        self.mesh                       = None
        self.meshType                   = "msh"
        self.meshDico                   = Dico()
        self.bodyForce                  = None
        self.boundaryConditionConcDico  = Dico()
        self.calculationTimesDico       = Dico()
        self.calculationType            = 1
        self.darcyVelocity              = None
        self.userPermeability           = False
        self.expectedOutputDico         = Dico()
        self.elmerZonesDico             = Dico()
        self.elmerNumberZoneDico        = Dico()
        self.effectiveDiffusionDico     = Dico()
        self.initialConditionConcDico   = Dico()
        self.lumpedMassMatrix           = None
        self.porosityDico               = Dico()
        self.sifFileName                = "test.sif"
        self.simulationType             = "transient"
        self.bdfOrder                   = "2"
        self.sorptionLawDico            = Dico()
                                                                                            #
                                                                                            # elasticity
                                                                                            #
        self.elasticity                = None
                                                                                            #
                                                                                            # temperature
                                                                                            #
        self.temperature                = None

        self.zonePerCellDico            = Dico()
        self.charge                     = []
        self.velocity                   = []
        self.boundPlot                  = []
                                                                                            # Young modulus is a
                                                                                            # scalar in the isotropic case
                                                                                            # scalar in the isotropic case
                                                                                            # or a 6x6 (3D)
                                                                                            # or a 4x4 (2D or axys. case) 
        self.youngModulus               = []
                                                                                            # a scalar in the isotropic case
        self.poissonRatio               = []
                                                                                            # to evaluate the thermal stresses 
        self.referenceTemperature       = None
        self.heatExpansionCoef          = None

        self.elmerZonesNamesList = []
        self.timespec = 0
        self.instance = 0
        if not hasattr(self,'problemType'):
            self.problemType='unknown'
            pass
        if self.problemType not in ['unknown','hydro','chemicaltransport']:
            raise Exception, " check the kind of problem you want to solve "
        #
        # call to setDefaultParameters, settings of default tool parameters
        #
        self.setDefaultParameters()
        self.setDefaultParameters(self.chargeParameterDico)
        self.outputs_point = None
        self.outputs_zone  = None
        self.outputs_surf  = None
        return None

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
        sifFile.write("Mesh DB \".\" \"%s\"\n"%self.meshDirectoryName)
        sifFile.write("Include Path \".\" \n")
        sifFile.write("Results Directory \"\"\nEnd\n\n")
#        sifFile.write("Results Directory \"\"\nEnd\n\n")
        #
        self.writeSimulation()
        self.writeConstants()
        self.writeBodies()
        self.writeMaterial()
#        if self.bodyForce: self.writeBodyForce()
        self.writeBodyForce()
        self.writeEquation()
        self.writeSolver()
        self.writeBoundaryCondition()
        self.writeInitialCondition()
        sifFile.close()

    def getVelocity(self):
        """
        Used to retrieve the velocity from elmer with the computed option, the velocity is obtained through elmer.
        """
        if "computed" in self.advConv.lower():
            return self.essai.getVelocity()
        else:
            return False

    def getCharge(self):
        """
        Used to retrieve the velocity from elmer with the computed option, the velocity is obtained through elmer.
        """
        if "computed" in self.advConv.lower():
            return self.essai.getCharge()
        else:
            return False

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

    def writeBodies(self):
        """
        Bodies are asociated to materials and equations.
        Only one equation is treated when temperature is set to None. 
        Otherwise, two equations are taken into account...
        So, bodies are associated to initial conditions and their number
        mostly depends on material numbers.
        """
        sifFile = self.sifFile
        sifFile.write("! ~~\n! Body\n! ~~\n")
        indb = 0
        ibc = 0
        #print " dbg self.dirBCList",self.dirBCList
        for ibc in range(len(self.dirBCList)):
            indBody = self.dirBCList[ibc][1]
            #raw_input("ibc")
            sifFile.write("Body %i\n"%(indBody))
            sifFile.write("  Name = \"body%s\"\n"%(indBody))
            sifFile.write("  Equation = 1\n")
            stinds = _digit(0)
            stindb = str(indb+1) + stinds
            sifFile.write("  Material = %s\n"%(indBody))
            sifFile.write("End\n\n")
#
# doit etre modifie des que plusieurs materiaux interviennent
#            
#        if len(self.dirBCList) == 0:
#            dec = 1                     # no boundary condition
#        else:
#            dec = 2                     # one boundary condition
        if (len(self.dirBCList) != 0): ibc+=1
        for  indb in range(len(self.dirICList)):
            print self.dirICList
            indBody = self.dirICList[indb]["index"]      
            sifFile.write("Body %i\n"%(indBody))
            sifFile.write("  Equation = 1 \n")
            stinds = _digit(0)
            stindb = str(indb+1) + stinds
            sifFile.write("  Material = %s\n"%(indBody))
            sifFile.write("  Initial Condition = %s\n"%(indBody))
#            sifFile.write("  Body Force = %s\n"%(indb+1))
            sifFile.write("  Body Force = %s\n"%(1))
            sifFile.write("End\n\n")
        return None

    def writeMaterial(self):
        """
        A loop over materials and species.
        Each material is associated to each species.
        The numbering is on three digits, two for the species, at least one for the region.
        For the moment, the material is independant of the species: a direct consequence of 
        the way the problem is formulated.
        """
        sifFile = self.sifFile
        sifFile.write("! ~~\n! Material p29 ref. Manual\n! ~~\n")        

        for indb in range(len(self.bodies)):
            stinds = _digit(0)
            stindb = str(indb+1)+stinds
            sifFile.write("Material %s\n"%(self.bodies[indb].support.body[0]))
            #
            # water density is supposed to be 1000 kg / m3. But it can
            # be fixed to other walues through the setWaterDensity function
            #
            #
            # rock density                    2700 kg / m3
            #
            porosity = self.bodies[indb].getMaterial().getPorosity().value
            sifFile.write(" Density = Real %15.10e\n"%(self.waterDensity*porosity+2700*(1.-porosity)))
            sifFile.write(" Water Density = Real %15.10e\n"%(self.waterDensity))
            sifFile.write(" Viscosity = Real %15.10e\n"%(1.0))
            sifFile.write(" Porosity = Real %15.10e\n"%(porosity))
                                                                                            #
                                                                                            # elasticity
                                                                                            #
                                                                                            # the material is supposed to be isotropic
                                                                                            #
            if self.elasticity == True:
                sifFile.write(" Young Modulus = Real %15.10e\n"%(self.youngModulus[0]))
                sifFile.write(" Poisson Ratio = Real %15.10e\n"%(self.poissonRatio[0]))
                sifFile.write(" Heat Expansion Coefficient = Real %15.10e\n"%(self.heatExpansionCoef))
                sifFile.write(" Reference Temperature = Real %15.10e\n"%(self.referenceTemperature))
                pass
                                                                                            #
                                                                                            # temperature: 
                                                                                            # specificHeatCapacity and
                                                                                            # heatConductivity
                                                                                            #            
            if self.temperature == True:
                if self.bodies[indb].getMaterial().getSpecificHeat() :
                    specificHeatCapacity    = self.bodies[indb].getMaterial().getSpecificHeat().value
                    sifFile.write(" Heat Capacity = Real %15.10e\n"%(specificHeatCapacity))
                else :
                    raise Exception("As the temperature mode is used, you have to give a heat capacity")
                if self.bodies[indb].getMaterial().getThermalConductivity() :  
                    heatConductivity        = self.bodies[indb].getMaterial().getThermalConductivity().value.value
                    sifFile.write(" Heat Conductivity = Real %15.10e\n"%(heatConductivity))
                else :
                    raise Exception("As temperature mode is used, you have to give a heat conductivity")
                #
                # viscosity
                #
                if self.bodies[indb].getMaterial().getViscosity() != None:
                    viscosity		= self.bodies[indb].getMaterial().getViscosity().value
                    sifFile.write(" Viscosity         = Real %15.10e\n"%(viscosity))
                pass
                                                                                            #
                                                                                            #       computed velocity: saturated flow
                                                                                            #
            if "computed" in str(self.darcyVelocity) and self.saturation == "saturated":
                if self.bodies[indb].getMaterial().getViscosity() != None:
                    viscosity		= self.bodies[indb].getMaterial().getViscosity().value
                    sifFile.write(" Viscosity         = Real %15.10e\n"%(viscosity))
                #print self.bodies[indb].getMaterial().getHydraulicConductivity()
                if type(self.bodies[indb].getMaterial().getHydraulicConductivity()) != NoneType:
                    sifFile.write(" Hydr Conductivity = Real %15.10e\n"%(self.bodies[indb].getMaterial().getHydraulicConductivity().value.value))
                    sifFile.write(" Saturated Hydraulic Conductivity = Real %15.10e\n"%(self.bodies[indb].getMaterial().getHydraulicConductivity().value.value))
                if self.bodies[indb].getMaterial().getSpecificStorage() != None:
                    sifFile.write(" Specific Storage = Real %15.10e\n"%(self.bodies[indb].getMaterial().getSpecificStorage().value))
                
            elif "computed" in str("self.darcyVelocity") and self.saturation == "undersaturated":
                raise Exception, " for the moment, no unsaturated flow can be bounded to chemical transport "
                                                                                                                           
                                                                                            #
                                                                                            #       compressibility
                                                                                            #            
            sifFile.write(" Compressibility Model = Incompressible\n")
            tempcont = len(self.speciesNamesList)
            #sifFile.write(" Diffusivity = Real %15.10e\n"%(3.e-10))
            for inds in range(tempcont):
                effecDiff       = self.bodies[indb].getMaterial().getEffectiveDiffusion()
                #print type(effecDiff),effecDiff.value.value
                if (type(effecDiff) not in [NoneType]):
                    effecDiff       = effecDiff.value.value
                else:
                    effecDiff       = 0.0
                porosity        = self.bodies[indb].getMaterial().getPorosity()
                #print type(porosity),porosity.value
                if (porosity not in [NoneType]):
                    porosity        = porosity.value
                else:
                    porosity        = 1.0
                longitudinalDispersivity = self.bodies[indb].getMaterial().getKinematicDispersion()
                #print longitudinalDispersivity,type(longitudinalDispersivity)
                if (type(longitudinalDispersivity) not in [NoneType]):
                    longDisp        = longitudinalDispersivity.value[0]
                    tranDisp        = longitudinalDispersivity.value[1]
                else:
                    longDisp        = 0.0
                    tranDisp        = 0.0
                v = None
                if isinstance(self.darcyVelocity,Velocity):
#                if type(self.darcyVelocity) != type(None):
                    v = self.darcyVelocity.getValue()
                    print " v ",v
                elif isinstance(self.darcyVelocity,StringType):
                    pass
                if type(v)!=type(None):
                    norm = (v[0]**2+v[1]**2+v[2]**2)**0.5
                    if norm > 0:
                        darcy_x = v[0]**2/norm
                        darcy_y = v[1]**2/norm
                        darcy_z = v[2]**2/norm
                    else:
                        darcy_x = 0.0
                        darcy_y = 0.0
                        darcy_z = 0.0
                else:
                    darcy_x = 0.0
                    darcy_y = 0.0
                    darcy_z = 0.0
                #print " we write the difusion ",effecDiff,darcy_x
                sifFile.write(" %s Diffusivity\n"%(self.speciesNamesList[inds]))
                sifFile.write("     Size 3 3\n")
                sifFile.write("      Real    %15.10e %15.10e %15.10e\\\n" %(longDisp*darcy_x + effecDiff,0.,0.))
                sifFile.write("              %15.10e %15.10e %15.10e\\\n" %(0.,longDisp*darcy_y + effecDiff,0.))
                sifFile.write("              %15.10e %15.10e %15.10e\\\n" %(0.,0.,longDisp*darcy_z + effecDiff))
                
                sifFile.write(" End\n")
                
##                sifFile.write(" %s Diffusivity = Real %15.10e\n"%(self.speciesNamesList[inds],\
##                                  longDisp*darcy_x + effecDiff))
#                sifFile.write(" %s Soret Diffusivity = Real %15.10e\n"%(self.speciesNamesList[inds],\
#                                  self.bodies[indb].getMaterial().getThermalConductivity().value.value))
                sifFile.write("\n")
            sifFile.write(" Long Dispersivity = Real %15.10e\n"%(longDisp))
            sifFile.write(" Tran Dispersivity = Real %15.10e\n"%(tranDisp))
                                                                                            #
                                                                                            # We treat the velocity, see page 22
                                                                                            #
            #raw_input(" self.advConv value :"+self.advConv)
            if self.advConv == "Constant":
                v = self.darcyVelocity.getValue()
                sifFile.write(" Convection Velocity 1 = %e\n"%v[0])
                sifFile.write(" Convection Velocity 2 = %e\n"%v[1])
                sifFile.write(" Convection Velocity 3 = %e\n\n"%v[2])
                                                                                            #
                                                                                            # We read a velocity field:
                                                                                            # for steady and t flows
                                                                                            #
            elif "Read" in self.advConv or self.advConv == "RComputed":
                #
                # The flow is issued from a previous flow run.
                # The file is contained in the mesh directory.
                # Its name is: HeVel.ep
                #
                fileName = "./" + self.meshDirectoryName + "/" + "HeVel.ep"
                if not os.path.isfile(fileName):
                    message = " problem with the velocity file " + fileName
                    raise Exception,message
                    return None
                
                velocityFile=open(fileName,'r')
                velocityFile.readline()
                velocityFile.readline()
                line = velocityFile.readline()
                f = len(line)/3
                self.points = []
                while "#group all" not in line:
                    #line = line.split()
                    self.points.append([float(line[0:20]),float(line[20:40]),float(line[40:60])])
                    line = velocityFile.readline()
                while "#time" not in velocityFile.readline():
                    pass
                line = velocityFile.readline()
                physic = []
                while len(line) > 1:
                    physic.append([float(line[0:20]),\
                                   float(line[20:40]),\
                                   float(line[40:60]),\
                                   float(line[60:80])])
                    line = velocityFile.readline()
                ind = 0
                vx = []
                vy = []
                vz = []
                for iunknown in range(0,len(physic)):
                    a = physic[iunknown]
                    self.charge.append(a[0])
                    vx.append(a[1])
                    vy.append(a[2])
                    vz.append(a[3])
                    ind+=1
                velFile = open("velRead","w")
                velFile.write("# generic velocity file to be read by WElmer\n")
                form = "%10s\n"
                velFile.write(form%(_foti10(len(vx))))
                form = "%15s %15s %15s\n"
                ind = 0
                for i in vx:
                    velFile.write(form%(_fote158(vx[ind]),_fote158(vy[ind]),_fote158(vz[ind])))
                    ind+=1
                velFile.close()
                del(vx);del(vy);del(vz)
                #
                sifFile.write(" Convection Velocity 1 = %e\n"%0.0)
                sifFile.write(" Convection Velocity 2 = %e\n"%0.0)
                sifFile.write(" Convection Velocity 3 = %e\n\n"%0.0)
                pass
            elif self.advConv == "Computed":
                sifFile.write(" Convection Velocity 1 = %e\n"%0.0)
                sifFile.write(" Convection Velocity 2 = %e\n"%0.0)
                sifFile.write(" Convection Velocity 3 = %e\n\n"%0.0)
                pass
            else:
                sifFile.write(" Convection Velocity 1 = %e\n"%0.0)
                sifFile.write(" Convection Velocity 2 = %e\n"%0.0)
                sifFile.write(" Convection Velocity 3 = %e\n\n"%0.0)
            
            sifFile.write("End\n\n")
        return None

    def writeBodyForce(self):
        """
        The body force section may be used to give additional force terms for the equations
        """
        sifFile = self.sifFile
        sifFile.write("! ~~~~~~~~~~\n! Body Force\n! ~~~~~~~~~~\n")
        for  indb in range(len(self.dirICList[0]["conc"])):
            if (indb==0):
                sifFile.write("Body Forces %i\n"%(indb+1))
                for inds in range(len(self.speciesNamesList)):
#                pass
                    sifFile.write(" %s Diffusion Source = Real %15.10e\n"%(self.speciesNamesList[inds],0.0))
#                sifFile.write(" %5s Diffusion = Real %15.10e\n"%(self.speciesNamesList[inds],1.23456e-10))
#                Curvature Diffusion = Real 0.0
#                sifFile.write("Physical Units True \n")
#        sifFile.write("  Physical Units True \n")
        sifFile.write("End\n\n")
        return None

    def writeEquation(self):
        """
        The equation section is used to define a set of equations for a body or set of bodies.
        Advection Diffusion Equation Variable_name      Logical
        If set to True, solve the advection-diffusion equation.
        Convection String
                The type of convection to be used in the advection-diffusion equation, 
                one of: None, Computed, Constant.
        Concentration Units String

        """
        sifFile = self.sifFile
        sifFile.write("! ~~\n! Equation p28 ref. Manual\n! ~~\n\n")
        ind = len(self.speciesNamesList)
        string = ""
        #print " dbgy elmer writeEquation",self.speciesNamesList
        #print "self.speciesNamesList",self.speciesNamesList
        #raw_input("self.speciesNamesList")
        for ind in range(len(self.speciesNamesList)):
            string += str(ind+1)+" "
        ind+=1
        if self.temperature != None:
            string += str(ind+1)+" "
            ind+=1
            
        sifFile.write("Equation 1\n")
        if self.advConv == "Computed": 
            for i in range(ind,ind+2):
                string += str(ind+1)+" "
                ind+=1
            
        sifFile.write("  Active Solvers(%i) = %s\n"%(ind,string))
#        sifFile.write("Advection Diffusion Equation = True\n")
#        sifFile.write("Darcy Equation = True\n")
        #raw_input("porosity state "+ self.porosityState)
        if self.advConv == "Constant":
            sifFile.write("  Convection = %s\n"%self.advConv)
            pass
        elif self.advConv == "Read":
            sifFile.write("  Convection = \"read\"\n")
            pass
        elif "computed" in self.advConv.lower():# Should be changed to distinguish between darcy and navier-Stokes solver
            sifFile.write("  Convection = \"dcomputed\"\n")
            pass
        elif (self.porosityState == "variable"):
            sifFile.write("  Convection = %s\n"%"Constant")
            #raw_input("checking the variable porosity option ")
            #raise Warning, " That part of the software is under development at the moment"
        else: # we consider as delault value a constant velocity for a variable porosity
            sifFile.write("  Convection = %s\n"%"No")
            
        sifFile.write("  Concentration Units = Absolute Mass\n")
               
#        if self.temperature == None:
#            sifFile.write("  ActiveSolvers(1) = 1\n")
#        else:
#            sifFile.write("  ActiveSolvers(2) = 1 2\n")
        sifFile.write("End\n\n")
        return None
        
    def writeSolver(self):
        """
        The solver section defines equation solver control variables.
        Equation String [Advection Diffusion Equation Variable_name]
        Variable String Variable_name
        """
        sifFile = self.sifFile
        sifFile.write("! ~~\n! Solver p27 ref. Models Manual\n! ~~\n")
                                                                                            #
                                                                                            # aqueous chemical unknowns treatment
                                                                                            #
        for ind in range(len(self.speciesNamesList)):      
            sifFile.write("Solver %i\n"%(ind+1))
            sifFile.write("  Equation = Advection Diffusion Equation %s\n"%(self.speciesNamesList[ind]))
            
            sifFile.write("  Variable = %s\n"%self.speciesNamesList[ind])
            sifFile.write("  Variable DOFs = 1\n\n")

            sifFile.write("  Procedure = \"AdvectionDiffusionTimeStep\" \"AdvectionDiffusionTimeStepSolver\"\n")
            sifFile.write("  Linear System Solver = %s\n"%self.parameterDico["Linear System Solver"])
            if self.parameterDico["algebraicResolution"] == "Direct":
            	if self.parameterDico["Linear System Direct Method"] in ["Banded","Umfpack"] :
            	    sifFile.write("  Linear System Direct Method = %s\n"%self.parameterDico["Linear System Direct Method"])
            	else :
            	    raise Exception("Linear System Direct Method is not correct.\nChoose between Banded and Umfpack") 
            	sifFile.write("  Optimize Bandwidth = %s\n"%self.parameterDico["Optimize Bandwidth"])   
            elif self.parameterDico["algebraicResolution"] == "Iterative":
                sifFile.write("  Linear System Iterative Method = %s\n"%self.parameterDico["Linear System Iterative Method"])
                sifFile.write("  Linear System Max Iterations = %s\n"%self.parameterDico["Linear System Max Iterations"])
                sifFile.write("  Linear System Convergence Tolerance = %e\n"%self.parameterDico["Linear System Convergence Tolerance"])
                sifFile.write("  Linear System Preconditioning = %s\n"%self.parameterDico["Linear System Preconditioning"])
                sifFile.write("  Linear System ILUT Tolerance = %e\n"%self.parameterDico["Linear System Convergence Tolerance"])
            elif self.parameterDico["algebraicResolution"] == "Multigrid":
            	raise Exception("Multigrid does not work for the moment.\nError:: LoadMesh: Unable to load mesh: ./mgrid2")
#                sifFile.write("  Linear System Direct Method = %s\n"%self.parameterDico["Linear System Direct Method"])
            else :
            	raise Exception("Algebraic resolution is not correct.\nChoose between Direct, Iterative and Multigrid")
                
            sifFile.write("  Linear System Symmetric = %s\n"%self.parameterDico["Linear System Symmetric"])
            #sifFile.write("  Linear System Abort Not Converged = %s\n"%self.parameterDico["Linear System Abort Not Converged"])
            sifFile.write("  Lumped Mass Matrix = %s\n"%self.parameterDico["Lumped Mass Matrix"])
                        
#            sifFile.write("  Stabilize ="+self.parameterDico['Stabilize']+"\n")
#            sifFile.write("  Stabilize = True \n")
            #print "dbg stabil ",self.parameterDico['Stabilize']
            #print " self.darcyVelocity",self.darcyVelocity,self.parameterDico['Bubbles']
            if self.parameterDico["Bubbles"] and type(self.darcyVelocity) != None:
                                                                                            #
                                                                                            # bubbles is set to true
                                                                                            # to stabilize the solver
                                                                                            #
                sifFile.write("  Bubbles = "+str(self.parameterDico['Bubbles'])+"\n")
            else:
                sifFile.write("  Bubbles  = False\n")
            sifFile.write("  Namespace = string \"%s\"\n"%self.speciesNamesList[ind])
            sifFile.write("End\n\n")
                                                                                            #
                                                                                            # temperature treatment
                                                                                            #
        ind +=1
        if self.temperature:
            sifFile.write("Solver %i\n"%(ind+1))
            sifFile.write("  Equation = Heat Equation TEMPERATURE\n")
            
            sifFile.write("  Variable = TEMPERATURE\n")
            sifFile.write("  Variable DOFs = 1\n\n")

#            sifFile.write("  Procedure = \"AdvectionDiffusionTimeStep\" \"AdvectionDiffusionTimeStepSolver\"\n")
            sifFile.write("  Procedure = \"HeatTimeStep\" \"HeatTimeStepSolver\"\n")
            sifFile.write("  Linear System Solver = %s\n"%self.parameterDico["Linear System Solver"])
            if self.parameterDico["algebraicResolution"] == "Direct":
            	if self.parameterDico["Linear System Direct Method"] in ["Banded","Umfpack"] :
            	    sifFile.write("  Linear System Direct Method = %s\n"%self.parameterDico["Linear System Direct Method"])
            	else :
            	    raise Exception("Linear System Direct Method is not correct.\nChoose between Banded and Umfpack") 
            	sifFile.write("  Optimize Bandwidth = %s\n"%self.parameterDico["Optimize Bandwidth"])   
            else:
                if self.parameterDico["Linear System Iterative Method"] in ["CG","CGS","BICGStab","TFQMP","GMRES"] :
                    sifFile.write("  Linear System Iterative Method = %s\n"%self.parameterDico["Linear System Iterative Method"])

                sifFile.write("  Linear System Max Iterations = %s\n"%self.parameterDico["Linear System Max Iterations"])
                sifFile.write("  Linear System Convergence Tolerance = %e\n"%(self.parameterDico["Linear System Convergence Tolerance"]*0.01))
                sifFile.write("  Linear System Preconditioning = %s\n"%self.parameterDico["Linear System Preconditioning"])
                sifFile.write("  Linear System ILUT Tolerance = %e\n"%(self.parameterDico["Linear System Convergence Tolerance"]*0.01))
                sifFile.write("  Linear System Symmetric = %s\n"%self.parameterDico["Linear System Symmetric"])
            #sifFile.write("  Linear System Direct Method = %s\n"%self.parameterDico["Linear System Direct Method"])
            sifFile.write("  Lumped Mass Matrix = %s\n"%self.parameterDico["Lumped Mass Matrix"])
            self.parameterDico['Stabilize'] = "True"
            sifFile.write("  Stabilize ="+self.parameterDico['Stabilize']+"\n")
            #print "dbg stabil ",self.parameterDico['Stabilize']
            if self.parameterDico['Stabilize']=="True":
                sifFile.write("  Bubbles = "+self.parameterDico['Bubbles']+"\n")
            else:
                sifFile.write("!  Bubbles = False\n")
            sifFile.write("  Namespace = string \"TEMPERATURE\"\n")
            
            sifFile.write("End\n\n")
                                                                                            #
                                                                                            # Darcy treatment
                                                                                            #
        ind+=1
        if "computed" in self.advConv.lower():
#
            sifFile.write("Solver %i\n"%(ind))
            sifFile.write("  Exec Solver = \"%s\"\n"%("Always"))
            sifFile.write("  Equation = \"%s\"\n"%("Darcy Equation"))

            sifFile.write("  Procedure = \"SaturatedDarcyTimeStep\" \"SaturatedDarcyTimeStepSolver\"\n")
            sifFile.write("  Variable = %s\n"%("Charge"))
            if (self.userPermeability): sifFile.write("  UserPermeability = %s\n"%("True"))
            sifFile.write("  Variable Dofs = %i\n"%(1))

            if self.chargeParameterDico["algebraicResolution"] != "Direct":
               self.chargeParameterDico['linearSystemSolver'] = "Iterative"
            else:

               sifFile.write("  Linear System Direct Method = %s\n"%self.chargeParameterDico["linear System Iterative Method"])

            sifFile.write("  Linear System Solver = \"%s\"\n"%self.chargeParameterDico['Linear System Solver'])
            sifFile.write("  Linear System Iterative Method = \"%s\"\n"%self.chargeParameterDico["Linear System Iterative Method"])
            sifFile.write("  Linear System Max Iterations = %s\n"%self.chargeParameterDico["Linear System Max Iterations"])
            sifFile.write("  Linear System Convergence Tolerance = %e\n"%self.chargeParameterDico["Linear System Convergence Tolerance"])
            sifFile.write("  Linear System Preconditioning = \"%s\"\n"%self.chargeParameterDico["Linear System Preconditioning"])
            sifFile.write("  Steady State Convergence Tolerance = %s\n"%self.chargeParameterDico["Steady State Convergence Tolerance"])

            if self.chargeParameterDico['stabilize'] == True:
                sifFile.write("  Stabilize = True\n")
            else:
                sifFile.write("  Stabilize = True\n")

            sifFile.write("  Namespace = string \"charge\"\n")
            sifFile.write("End\n\n")
                                                                                            #
                                                                                            # charge has been treated,
                                                                                            # now we extract the velocity
                                                                                            #
            ind+=1
            sifFile.write("Solver %i\n"%(ind))
            sifFile.write("  Equation = ComputeFlux\n")
#            sifFile.write("  Procedure = \"DFluxTimeStepSolver\" \"DFluxTimeStepSolver\"\n")
            sifFile.write("  Procedure = \"DFluxSolver\" \"DFluxSolver\"\n")

            if (self.userPermeability): sifFile.write("  UserPermeability = %s\n"%("True"))
            sifFile.write("  Flux Variable = String \"Charge\"\n")
            sifFile.write("  Flux Coefficient = String \"Hydr Conductivity\"\n")
            sifFile.write("  Flux Coefficient = String \"Saturated Hydraulic Conductivity\"\n")
            sifFile.write("  Linear System Convergence Tolerance = %e\n"%(self.chargeParameterDico["Flux Parameter"]))
            sifFile.write("End\n\n")
            pass
                                                                                            #
                                                                                            # we treat the elasticity
                                                                                            # p36 Models manual 13/01/2011
                                                                                            #
        ind +=1
        if self.elasticity:
            sifFile.write("Solver %i\n"%(ind))
            sifFile.write("  Equation = Elasticity Solver\n")
            sifFile.write("  Displace Mesh = Logical FALSE\n")
            sifFile.write("  Linear System Solver = Iterative\n")
            sifFile.write("  Linear System Iterative Method = BiCGStab\n")
            sifFile.write("  Linear System Preconditioning = ILU1\n")
            sifFile.write("  Linear System Max Iterations = 500\n")
            sifFile.write("  Linear System Convergence Tolerance = 1.0e-8\n")
            sifFile.write("  Nonlinear System Newton After Tolerance = 1.0e-3\n")
            sifFile.write("  Nonlinear System Newton After Iterations = 20\n")
            sifFile.write("  Nonlinear System Max Iterations = 1000\n")

            sifFile.write("  !\n")
            sifFile.write("  Nonlinear System Convergence Tolerance = 1.0e-5\n")
            sifFile.write("  Nonlinear System Relaxation Factor = 1.0\n")
            sifFile.write("  Displace Mesh = Logical FALSE\n")
            sifFile.write("  !\n")
            sifFile.write("  Steady State Convergence Tolerance = 1.0e-4\n")
            pass
        """
Solver 1
  Equation = Elasticity Solver
  Variable = Displacement
  Variable DOFs = 2
  Procedure = "ElasticSolve" "ElasticSolver"
  
  Calculate Loads = Logical True
End

Solver 2
  Equation = "Elasticity Analysis"
  Procedure = "StressSolve" "StressSolver"
  Variable = String "True Displacement"
  Variable DOFs = Integer 2
  Time Derivative Order = 2

  Calculate Stresses = TRUE
  Displace Mesh = Logical FALSE
 

  Optimize Bandwidth = True
End

Solver 3
  Equation = "Compute Energy Release Rate"
  Procedure = "EnergyRelease" "ReleaseRateSolver"
End

        """



        return None
        
    def writeBoundaryCondition(self):
        """
        In advection-diffusion equation we may set the concentration directly by Dirichlet boundary conditions
        or use mass flux condition. The natural boundary condition is zero flux condition.
        """
        sifFile = self.sifFile
        sifFile.write("! ~~\n! Boundary p30 ref. Manual\n! ~~\n")
                                                                                            #
                                                                                            # Two kinds of boundary cond.:
                                                                                            #
                                                                                            # Dirichlet or Flux
                                                                                            #
        #print self.dirBCList
        for dirBC in self.dirBCList1:
            #print " dbg write BC ",dirBC,self.speciesNamesList
            #raw_input(" dbg ctm bc ")
            inds = 0
            #print " bc elmer ",dirBC[0],dirBC[1],dirBC[2],dirBC[3]," inds ",inds
                                                                                            #
                                                                                            # Dirichlet
                                                                                            #
            #print " elmer dbg ",dirBC[2].lower()
            if (dirBC["type"].lower() == "dirichlet"):
                stinds = _digit(inds)
                stindb = str(dirBC["index"])+stinds
                sifFile.write("Boundary Condition %s\n"%dirBC["index"])
                sifFile.write("  Target Boundaries (1) = %s\n"%str(dirBC["index"]))
                conc = dirBC["conc"]

                for concName in self.speciesNamesList:
                    stinds = _digit(inds+1)
                    stindb = str(dirBC["name"])+stinds
                    sifFile.write("  %s = Real %e\n"%(concName,dirBC["conc"][inds]))
                    inds+=1
                                                                                            #
                                                                                            # elasticity
                                                                                            #
                if self.elasticity:
                    sifFile.write("! elasticity\n")
                    for component in range(self.spaceDimensions):
                        sifFile.write("Displacement %s = 0"%(component+1))

                    pass
                                                                                            #
                                                                                            # temperature
                                                                                            #
                if self.temperature:
                    sifFile.write("! temperature\n")
                    sifFile.write("  %s = Real %e\n"%("temperature", dirBC["temperature"][0])) # we take the first element of the list. 
                                                                                            # We keep a list because we can have a varying temp. Boundary
                if "computed" in str(self.advConv.lower()):
                    #print " dbg elmer charge ",self.advConv
                    sifFile.write("! charge\n")
                    sifFile.write("  %s = Real %e\n"%("Charge", dirBC["head"]))
                    #raw_input("boundaryName")
                    for body in self.bodies:
                        print body.support.getName(),dirBC["bodyName"]
                        if body.support.getName() == dirBC["bodyName"]:
                            print body.getMaterial().getHydraulicConductivity().getValue().value
                            hydrCond = body.getMaterial().getHydraulicConductivity().getValue().value
                            break
                    sifFile.write("  %s = Real %e\n"%("Hydraulic Conductivity", hydrCond))
                sifFile.write("End\n\n")
            elif (dirBC["type"].lower() == "flux"):
                                                                                            #
                                                                                            # Flux B. C.
                                                                                            #
###                stinds = _digit(inds)
#                stindb = str(dirBC[1])+stinds
#                sifFile.write("Boundary Condition %s\n"%stindb)
#                sifFile.write("  Target Boundaries (1) = %s\n"%str(dirBC[1]))
#                sifFile.write("  Mass Transfer Coefficient = Real %e\n"%(dirBC[3]))
                stinds = _digit(inds+1)
                stindb = str(dirBC["index"])+stinds
                sifFile.write("Boundary Condition %s\n"%stindb)
                sifFile.write("  Target Boundaries (1) = %s\n"%str(dirBC["index"]))
                for spconc in dirBC["conc"]:
                    #stinds = _digit(inds+1)
                    #stindb = str(dirBC[1])+stinds
                    #sifFile.write("Boundary Condition %s\n"%stindb)
                    #sifFile.write("  Target Boundaries (1) = %s\n"%str(dirBC[1]))

#                    if (inds == 3):
#                        dirBC[3] = 2.e-3
#                         pass
#                    sifFile.write("  Mass Transfer Coefficient = Real %e\n"%(dirBC[3]))

#                    sifFile.write("  Mass Transfer Coefficient %s = Real %e\n"%(self.speciesNamesList[inds],dirBC[3]+inds))
#                    sifFile.write("  External Concentration %s = Real %e\n"%(self.speciesNamesList[inds],spconc))
#                    sifFile.write("  %s: External Concentration = Real %e\n"%(self.speciesNamesList[inds],spconc))
                    if (inds == 3 ):
                        sifFile.write("  %s Mass Transfer Coefficient = Real %e\n"%(self.speciesNamesList[inds],dirBC["massTC"]))
                        sifFile.write("  %s External Concentration = Real %e\n"%(self.speciesNamesList[inds],abs(spconc)))
                        #sifFile.write("  Mass Transfer Coefficient = Real %e\n"%(dirBC[3]))
                        #sifFile.write("  External Concentration = Real %e \n"%(abs(spconc)))
                    else:
                        sifFile.write("  %s Mass Transfer Coefficient = Real %e\n"%(self.speciesNamesList[inds],dirBC["massTC"]))
                        sifFile.write("  %s External Concentration = Real %e\n"%(self.speciesNamesList[inds],abs(spconc)))
                        #sifFile.write("  Mass Transfer Coefficient = Real %e\n"%(dirBC[3]))
                        #sifFile.write("  External Concentration = Real %e \n"%(0.))
                        pass
                    inds+=1
                sifFile.write("End\n\n")
            elif (dirBC["type"].lower() == "neumann"):
                                                                                            #
                                                                                            # Neumann boundary condition.
                                                                                            # For the moment,
                                                                                            # only a no flux 
                                                                                            # boundary condition is considered
                                                                                            #
                stinds = _digit(inds)
                stindb = str(dirBC[1])+stinds
                sifFile.write("Boundary Condition %s\n"%stindb)
                sifFile.write("  Target Boundaries (1) = %s\n"%str(dirBC["name"]))
                print " no flux neumann",
                for spconc in dirBC["conc"]:
                    stinds = _digit(inds+1)
                    stindb = str(dirBC["name"])+stinds
                    sifFile.write("  %s Flux = Real %e\n"%(self.speciesNamesList[inds],0.0))
                    inds+=1
            
                sifFile.write("End\n\n")
        return None

    def writeInitialCondition(self):
        """
        The initial condition section may be used to set initial values for the concentration Ci
        """
        sifFile = self.sifFile
        inds = 0        
        sifFile.write("! ~~\n! initial condition p8 ref. ElmersolverManual\n! ~~\n")
        
        for dirIC in self.dirICList:
            #print "diric",dirIC
            inds+=1
 #       for indb in range(len(self.bodies)):
 #           for inds in range(len(self.speciesNamesList)):
            sifFile.write("Initial Condition %s\n"%(dirIC["index"]))
            ind = 0
            for spconc in self.speciesNamesList:
                sifFile.write("  %s = Real %e\n"%(self.speciesNamesList[ind], dirIC["conc"][ind]))
                ind+=1
                                                                                            #
                                                                                            # Temperature
                                                                                            #
            if (self.temperature==True):
                sifFile.write("! temperature\n")
                sifFile.write("  %s = Real %e\n"%("TEMPERATURE", dirIC["temperature"]))
                pass
                                                                                            #
                                                                                            # Charge
                                                                                            #
            if ("computed" in self.advConv.lower()):
                sifFile.write("! charge\n")
                #print dirIC
                sifFile.write("  %s = Real %e\n"%("Charge", dirIC["head"]))
                pass
            sifFile.write("End\n")
                
        return None

    def writeSimulation(self):
        """
        The simulation section gives the case control data:
        Simulation Type: Transient
        BDF Order: Value may range from 1 to 5
        """
        sifFile = self.sifFile
        sifFile.write("Simulation\n")
        #
        #
        #       2D meshes: a cartesian or a delaunay mesh is identical in its identification
        #
        sifFile.write("  Coordinate System = Cartesian "+self.mesh.getDimensionString()+"\n\n")
        sifFile.write("  Simulation Type = "+self.getSimulationType()+"\n")
#        sifFile.write("  Steady State Max Iterations ="+self.getSteadyStateMaxIter()+"\n\n")
        sifFile.write("  Coordinate Mapping(3) = 1 2 3\n")
        sifFile.write("  Timestepping Method = "+self.getTimeSteppingMethod()+"\n")
        if self.getTimeSteppingMethod() == "BDF":
            if int(self.getBDFOrder())>0 and int(self.getBDFOrder())<6 :
                #sifFile.write("  BDF Order = "+str(self.getBDFOrder())+"\n")
                sifFile.write("  BDF Order = 1\n")
            else :
            	raise Exception("BDF Order must integer between 1 and 5")
        else:
            sifFile.write("  \n")
        # the following parameters are irrelevant, they are treated via the coupling algorithm    
        sifFile.write("  Solver Input File = %s\n"%(self.sifFileName))
        sifFile.write("  Timestep Sizes = 100\n")
        sifFile.write("  Timestep Intervals = 5\n\n")

        sifFile.write("  Output Intervals = 1\n")        
        sifFile.write("!  Lumped Mass Matrix = "+self.parameterDico["Lumped Mass Matrix"]+"\n")
        sifFile.write("  Max Output Level = 3\n")
        sifFile.write("End\n\n")
        return None
        
    def end(self):
    
       self.essai.stop()
       return
        
    def getSimulationType(self):
        return self.simulationType
        
    def getSteadyStateMaxIter(self):
        return self.parameterDico["Steady State Max Iterations"]
	
    def getTimeSteppingMethod(self):
        return self.parameterDico["Timestepping Method"]
	
    def getBDFOrder(self):
        return self.parameterDico["BDF Order"]
	
    def initDomain(self,domainSpeciesAqueousConcentrations):
        if len(self.speciesNamesList) != len(domainSpeciesAqueousConcentrations):
            raise Exception(" problem within elmer with initialisation")
        self.essai(len(self.speciesNamesList),domainSpeciesAqueousConcentrations)
        
    def readVelocity(self):
        #print "dbge before the reading"
        self.essai.readVelocity("velRead")
        #print "dbge after the reading"

    def setDirBC(self, dirichletBoundaryCondition, dicList = None):
        """
        Used to set dirichlet boundary conditions, we use a dictionnary 
        """
        self.dirBCList.append( dirichletBoundaryCondition)
        self.dirBCList1.append( dicList)
        return None

    def setFluxBC(self, fluxBoundaryCondition, dicList = None):
        """
        Used to set flux boundary conditions ( should be checked )
        """
        self.dirBCList.append(fluxBoundaryCondition)
        self.dirBCList1.append( dicList)
        return None

    def setNeuBC(self, dirichletBoundaryCondition, dicList = None):
        """
        Used to set dirichlet boundary conditions (should be checked )
        """
        self.dirBCList.append(dirichletBoundaryCondition)
        self.dirBCList1.append( dicList)
        return None
        
    def setDirIC(self, dicList):
        """
        used as an example in the module chemicaltransport
        """
#        self.dirICList.append(initialCondition)
        self.dirICList.append(dicList)
        #print dicList
        #raw_input(" azry")
        return None
        
    def setDarcyVelocity(self, darcyVelocity):
        """
        To set the Darcy velocity for elmer.
        A computed Darcy velocity can be inserted through the "read" option
        """
        print "dbg set Darcy velocity ",darcyVelocity
        #raw_input("set Darcy velocity")
        norm = 0.
        if isinstance(darcyVelocity,Velocity):
            for ind in darcyVelocity.getValue():
                norm += ind**2
            if norm>0: 
                self.advConv = "Constant"
        elif isinstance(darcyVelocity,StringType):
            if darcyVelocity.lower() == "read":
                self.advConv = "Read"
            elif darcyVelocity.lower() == "rcomputed":
                self.advConv = "rComputed"
                #self.setDefaultParameters(self.chargeParameterDico)

            elif "computed" in darcyVelocity.lower():
                #self.setDefaultParameters(self.chargeParameterDico)
                #print self.chargeParameterDico
                #raw_input("we set the darcy velocity as computed")
                self.advConv = "Computed"
        #raw_input(" we have already defined the velocity ")
        self.darcyVelocity = darcyVelocity
        
    def setInitBody(self,initialisedBody):
        """
	An initial field is set overwritten, should be overwritten by concentration values
        """        
        self.initialisedBody = initialisedBody
	return None


    def setInstance(self, instance):
        """
	a control parameter of the instance
        """        
        #print "  elmer dbg instance ",self.instance
        self.instance = instance
        return None

    def setMesh(self,  mesh):
        """
	to set or reset the name or the mesh
        """        
        self.mesh  = mesh
        return None

    def getMeshFileName(self):
        """
        to recover the name of the mesh file
        """        
        return self.meshFileName

    def setBoundaryConditionConcentrations(self, bCField):
        """
        set fields table of Concentration Boundary Condition (Dirichlet)
        """
	self.boundaryConditionConcDico["dirichlet"] = bCField
	#print "setBoundaryConditionConcentrations ", bCField
	#raw_input("setBoundaryConditionConcentrations ")

    def setMeshFileName(self,  meshFileName="elmerMesh"):
        """
	to set or reset the name or the mesh
        """        
        self.meshFileName  = meshFileName
        return None
        
    def setProblemType(self,  problemType = "chemicaltransport"):
        self.problemType = problemType
    
       
    def setSifFile(self,sifFile):
        """
        to define the name of the sif file
        """
        self.sifFile = sifFile
    
    def setChargeParameter(self, **solverparameterdict):
        """
        Here the parameters of the algebraic solver for the charge are introduced
        """
        for key, value in solverparameterdict.items():
            print "setChargeParameter key, value ",key, value
            if key == "preconditioner":
                self.chargeParameterDico['Linear System Preconditioning'] = value
            if key == "steadyStateConvergenceTolerance":
                self.chargeParameterDico['Steady State Convergence Tolerance'] = value
            if key == "stabilize":
                self.chargeParameterDico['stabilize'] = value
            if key == 'linearSystemPreconditioning':
                self.chargeParameterDico["Linear System Preconditioning"] = value
            if key == "linearSystemMaxIterations":
                self.chargeParameterDico["Linear System Max Iterations"] = value
            if key == "linearSystemConvergenceTol":
                self.chargeParameterDico["Linear System Convergence Tolerance"] = value
            if key == "linearSystemConvergenceTolerance":
                self.chargeParameterDico["Linear System Convergence Tolerance"] = value
            if key == "iterSolver":
                print " we set itersolver to ",value
                self.chargeParameterDico["Linear System Max Iterations"] = value
        self.chargeParameterDico["Flux Parameter"]                      = 5.e-1
                
    def setConstantsParameter(self, **constantsdict):
    	"""
        Here the constants of the problem are introduced
        """
        for key, value in constantsdict.items():
            if key == "gravityDirection":
            	self.gravityDirection = value
            if key == "gravityValue" :
            	self.gravityValue = value
            if key == "Stefan Boltzmann" :
            	self.stefanBoltzmann = value

    def setTransportParameter(self, **solverparameterdict):
        """
        Here the parameters of the algebraic solver are introduced
        """
        for key, value in solverparameterdict.items():
            if key == "accelerator":
                self.parameterDico["Linear System Iterative Method"] = value
            if key == "algebraicResolution":
                self.parameterDico["algebraicResolution"] = value
            if key == "BDFOrder" or key == "BDFO" or key.upper() == "BDF":
                self.parameterDico["BDF Order"] = str(value)
            else:
                self.parameterDico["BDF Order"] = str(1)
            if key == "Bubbles":
                self.parameterDico["Bubbles"] = value
            if key == "convSolver":
                self.parameterDico["Linear System Convergence Tolerance"] = value
            if key == "discretisation":
                self.parameterDico["discretisation"] = value
            if key == "iterSolver":
                self.parameterDico["Linear System Max Iterations"] = value
            if key == "LinearSystemSymetry":
                self.parameterDico["Linear System Symmetric"] = value
            if key == "preconditioner":
                self.parameterDico["Linear System Preconditioning"] = value
            if key == "timeSteppingMethod" or key == "tSM":
                self.parameterDico["Timestepping Method"] = value
            pass
            
    def setWaterDensity(self,waterDensity):
        """
        To set the water density to a walue != from 1000.0
        """
        if isinstance(waterDensity,Density):
            self.waterDensity = waterDensity.getValue()
        elif isinstance(waterDensity,float):
            self.waterDensity = waterDensity
            
    def setWaterHeatCapacity(self,waterHeatCapacity):
        """
        To set the water heatcapacity:  default walue is 4185 J/kg/K
        """
        self.waterHeatCapacity = waterHeatCapacity
            
    def setWaterHeatConductivity(self,waterHeatConductivity):
        """
        To set the water heat conductivity to a walue != from 0.6 W/m/K
        """
        self.waterHeatConductivity = waterHeatConductivity

    def defineElmerZones(self, field):
        """ 
	definition of zones for the elmer component
        """
        zonesList  = field.getZones()
        zoneNumber = 0
        for zone in zonesList:
            zoneNumber   += 1
            zoneName      = zone.getName()
            globalIndexes = zone.getGlobalIndexes()
            self.elmerZonesDico[zoneName] = (zoneNumber, globalIndexes)
            self.elmerNumberZoneDico[zoneNumber]=zoneName
            self.elmerZonesNamesList.append(zoneName)

        # zone-element connectivity, define zonePerCellDico
        for zoneName in self.elmerZonesNamesList:
            zoneNumber, globalIndexes = self.elmerZonesDico[zoneName] 
            for cell in globalIndexes:
                self.zonePerCellDico[cell] = zoneNumber
        return

    def advanceTime(self):
        """
        used to update time
        """
	if self.instance!=2:
	    self.essai.advanceTime()
	else:
	    self.essaig.advanceTime()
	return None
	
    def setTimeSteppingMethod(self,tSM):
        """
        Used to set the time step
        """
        if type(tSM) is StringType:
            if tSM in ["Explicit Euler","BDF","Crank-Nicholson"]:
                self.parameterDico["Timestepping Method"] = tSM

    def setTimeStep(self,deltat):
        """
        used to update the time step
        """
	if self.instance!=2:
	    self.essai.dt(deltat)
	else:
	    self.essaig.dt(deltat)
	return None

    def getConcentrationValues(self):
        """
        used to transfer species concentrations from elmer to the coupling tool
        """
#	print " call of getConcentrationValues"
	if self.instance==2:
	    print " we get from the gas transport concentrations "
	    return self.essaig.getConcentration()
	else:
#	    print " call of getConcentrationValues"
	    return self.essai.getConcentration()

    def getCoordinatesValues(self):
        """        
        Used to get coordinate values: return is a list of coordinates for node points
        """
	print " call of getCoordinates"
#        coordinates = self.mesh.getNodesCoordinates()
	coordinates = self.essai.getCoordinates()
	elementsNumber = len(coordinates)/3
	listex = []
	listey = []
	listez = []
	for i in range(1,elementsNumber+1):
	    listex.append(coordinates[(i-1)*3])
	    listey.append(coordinates[(i-1)*3+1])
	    listez.append(coordinates[(i-1)*3+2])
	
	return [listex,listey,listez]

    def getPermutation(self):
        """
        Used to get the permutaton of nodes occuring within elmer
        """
        print " within the python call to getPermutation "
	return self.essai.getPermutation()

    def getTemperatureField(self):
        """
        Used to transfer the temperature field from elmer to the coupling tool
        """
	return self.essai.getTemperature()
	    
    def majExpectedOutput(self):
        """
        frequency treatment
        """
        # on retouche les temps de sortie au cas ou il y a des frequency
        # pour les zones uniquement
        #print "self.outputs_zone['nom']",self.outputs_zone['nom']
        #print "self.calculationTimesDico['timespec']",self.calculationTimesDico['timespec']
        #print "self.calculationTimesDico['all_times']",self.calculationTimesDico['all_times']
##         if len(self.outputs_zone['nom']) == 0:
##             self.calculationTimesDico['timespec'] = [self.calculationTimesDico['final_time']]
##         else:
##             for output_name in self.outputs_zone['nom']:
##                 #print "self.outputs_zone['nom'],'timespec'",zone,self.outputs_zone['timespec']
##                 if self.outputs_zone.has_key('timespec'):
##                     for i in range(len(self.outputs_zone['timespec'])):
##                         timespec = self.outputs_zone['timespec'][i]
##                         print 'output_name,timespec',output_name,timespec
##                         if timespec.getSpecification() == 'frequency':
##                             f  = timespec.getFrequency()
##                             for j in range(0,len(self.calculationTimesDico['all_times']),f):
##                                 self.calculationTimesDico['timespec'].append(self.calculationTimesDico['all_times'][j])
##                                 pass
##                             pass
##                         pass
##                     pass
##                 pass
##             pass

        if self.outputs_zone['nom'] != []:
	    if not self.outputs_zone['nom']:
                self.calculationTimesDico['timespec'] = [self.calculationTimesDico['final_time']]
            else:
##             for output_name in self.outputs_zone['nom']:
##                 #print "self.outputs_zone['nom'],'timespec'",zone,self.outputs_zone['timespec']
                if self.outputs_zone.has_key('timespec'):
                    for i in range(len(self.outputs_zone['timespec'])):
                        timespec = self.outputs_zone['timespec'][i]
                        #print 'output_name,timespec',self.outputs_zone['nom'][i],timespec
                        if timespec.getSpecification() == 'frequency':
                            f  = timespec.getFrequency()
                            for j in range(0,len(self.calculationTimesDico['all_times']),f):
                                self.calculationTimesDico['timespec'].append(self.calculationTimesDico['all_times'][j])
                                pass
                            pass
                        pass
                    pass
                pass

        if self.calculationTimesDico['timespec']:
            self.calculationTimesDico['timespec'].sort()
            #print "self.calculationTimesDico['timespec'] APRES",self.calculationTimesDico['timespec']
            self.calculationTimesDico['timespec'] = elimCommonElementsInList(self.calculationTimesDico['timespec'], 1E-15)
            #print "self.calculationTimesDico['timespec'] APRES2",self.calculationTimesDico['timespec']
            pass
        return

    def majStorageCoefficient(self):
        if self.problemType not in ['unknown','saturatedhydro','transienthydro',"chemicaltransport"]:
            raise Exception, " check the kind of problem you want to solve "
        print "self.problemType",self.problemType
        if self.problemType=='transienthydro':
            self.storageCoefficient=[]
            nbZones = len(self.porosT)
            if len(self.mat_comp)!=nbZones:
                msg='not same nbzones between porosity '+\
                     'and matrix compressibility factor ??'
                raise msg
            for zoneInd in range(nbZones):            
                tab=getTimeUnifiedTables(self.porosT[zoneInd],self.mat_comp[zoneInd])
                tnew=Table('Storativity')
                tnew.addColumn('time', tab[0].getColumn(0))
                print 'tab[0].getColumn(0)',type(tab[0].getColumn(0)),tab[0].getColumn(0)
                poro=list(tab[0].getColumn(1))
                mcf=list(tab[1].getColumn(1))
                stor=[self.density*self.absoluteGravity*(poro[i]*self.fluid_comp+mcf[i]) for i in range(len(poro))]
                tnew.addColumn('f(t)', stor)
                print 'poro,mcf,self.fluid_comp,stor',poro,mcf,self.fluid_comp,stor
                self.storageCoefficient.append(tnew)
                pass
            self.storageCoefficient=getTimeUnifiedTables(*tuple(self.storageCoefficient))
            self.nbStorageCoefficient=self.storageCoefficient[0].getNbRows()
            pass
        elif self.problemType=='saturatedhydro':
            self.nbStorageCoefficient=self.nbPoros
            pass
        elif self.problemType=='chemicaltransport':
            pass
        else:
            msg='Unknown Component : <%s>'%self.__class__.__name__
            raise msg
            
    def setHydraulicPorosityParameter(self,hpor):
        return None

    def init(self,studienName=None):
        """
	Used to launch the Elmer code:
		you set-up here all the file system 
		to launch elmer
        """
        print " dbg elmer init method";sys.stdout.flush()
        self.timeDiscretizationTreatment()
#        print "majStorageCoefficient"
#        print "dbg elmer instance ",self.instance
        self.majStorageCoefficient()
##             pass
        #print " ic_n dbg ",studienName
	if self.instance!= None and self.instance!=2:
#	    self.name = "./Data/"+studienName + "_ctr"+str(self.instance)
	    self.name = "./Data/"+studienName + "_ctr"
	elif self.instance==2:
	    self.name = "./Datag/" + studienName + "_ctr"

        meshFileName = self.getMeshFileName()

        # Data directory creation 
        if not os.path.exists('Data') or not os.path.isdir('Data'):
            os.mkdir('Data')
            pass
	    
	if self.instance==2:
            if not os.path.exists('Datag') or not os.path.isdir('Datag'):
                os.mkdir('Datag')
	#
	# ELMERSOLVER_STARTINFO is the file enabling Elmer to be launched
	#
	self.elmerStartInfo = open("ELMERSOLVER_STARTINFO","w")
	self.elmerStartInfo.write("%s\n"%(self.sifFileName))
	self.elmerStartInfo.close()

	print "dbg createSifFile";sys.stdout.flush()
        self.createSifFile()
	print "dbg createSifFile end",self.instance;sys.stdout.flush()
	    
	if self.instance==0 or self.instance==1:
	    print " initialisation of the instance ";sys.stdout.flush()
	    self.essai = WElmer
	    lstring = len(self.essai.__doc__[self.essai.__doc__.find("A"):])-2
	    print "~"*lstring
	    print self.essai.__doc__
	    print "~"*lstring
	    #raw_input()
	    self.essai.initialize()

#	    self.essai.setInstance(self.instance)
	    #print "ic_new dbg setSpeciesAnzahl: ",self.instance,self.unAnzahl,type(self.unAnzahl)
            print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
            print " End of the elmer files writing phase"
            print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
            pass
        return None

    def AqueousComponentOneTimeStep(self):
        """
        This method enables to solve one step in time for the aqueous equations
        """
        return self.essai.oneACTimeStep()

    def HeatOneTimeStep(self):
        """
        This method enables to solve one step in time for the heat equation
        """
        return self.essai.oneHeatTimeStep()

    def SaturatedHydraulicOneTimeStep(self):
        """
        This method enables to solve one step in time for the saturated hydraulic equation
        """
        return self.essai.oneSHTimeStep()

    #---------------------------------------------------------------------------
    #---------------------------------------------------------------------------
    def setCalculationTimes(self, calculationTimesList):
        """
        set calculation times
        """

        self.calculationTimesDico ['first_time'] = calculationTimesList[0]
        self.calculationTimesDico ['final_time'] = calculationTimesList[-1]
##         print "self.calculationTimesDico ['final_time']",self.calculationTimesDico ['final_time']
##         raise stop
        self.calculationTimesDico ['all_times']  = calculationTimesList

        # Determination du premier temps non nul
        t0 = calculationTimesList[0]
        if t0 != 0.0 :
            self.calculationTimesDico ['first_time_not_null'] = calculationTimesList[1]
        self.nbTimes = len(calculationTimesList)
	print " ic dbg self.nbTimes %i\n"%(self.nbTimes)
        return

    def setExpectedOutput(self, expected_output_dict_list_ini):
        """
	Set expected outputs
        """
	print "ic dbg Set expected outputs\n"
        expected_output_dict_list=\
           [eoDict.copy() for eoDict in expected_output_dict_list_ini]

        for eoDict in expected_output_dict_list:
            if (eoDict['quantity']=='TotalInflux') or ( eoDict['quantity']=='TotalFlux' and self.problemType=='extendedtransport' ):
                msg = '%s outputs not yet implemented.'%eoDict['quantity']
                raise Exception(msg)
            pass
        for eoDict in expected_output_dict_list:
            timespec=None
            OKtimespec='timespec' in eoDict.keys()
            if OKtimespec:timespec  = eoDict['timespec']
            if (not timespec) and OKtimespec:
                del eoDict['timespec']
                pass
##             print 'EXPECTED OUTPUT :\n',eoDict
            pass
            
        # times list of outputs
        if self.calculationTimesDico.has_key('first_time'):
            first_time = self.calculationTimesDico ['first_time']
        else:
            first_time = 0
            
        if self.calculationTimesDico.has_key('final_time'):
            final_time = self.calculationTimesDico ['final_time']
        else:
            final_time = 1
            
        eoTimesList = []
        eo_zone_TimesList = []
        for eoDict in expected_output_dict_list:
            timespec=None
            OKtimespec='timespec' in eoDict.keys()
            if OKtimespec:timespec  = eoDict['timespec']
##             if 'timespec' in eoDict.keys():
            if timespec:
                eoName    = eoDict['name']
##                 timespec  = eoDict['timespec']
                spec = timespec.getSpecification()
                if spec == 'times':
                    eoTimes = timespec.getTimes()
                    #print " 'times' eoTimes",eoTimes
                elif spec == 'period':
                    f  = timespec.getPeriod()
                    t  = first_time
                    ft = final_time 
                    eoTimes = [t]
                    while t < ft:
                        t += f
                        if t <= ft: eoTimes.append(t)
                    eoDict['timespec'] = TimeSpecification(times = eoTimes)
                    #print " 'period' eoTimes",eoTimes

                elif spec == 'frequency':
                    eoTimes = []  
                else:
                    raise Exception, "The way you try to introduce output time specification has not been treated"

                eoTimesList += eoTimes
                #
                support = eoDict['support']
                
            else:
                # il faut au moins un temps dans la liste des temps de sortie
                # pour l'hydro stationnaire
                eoTimesList=[0]
                eo_zone_TimesList=[0]
                pass
            pass

        if len(eo_zone_TimesList):
            eo_zone_TimesList.sort()
            eo_zone_TimesList = elimCommonElementsInList(eoTimesList, 1E-15)
            pass
        if len(eoTimesList):
            eoTimesList.sort()
            eoTimesList = elimCommonElementsInList(eoTimesList, 1E-15)
            pass
        self.expectedOutputDico['eoTimesList'] = eoTimesList

        if self.calculationTimesDico.has_key('timespec'):
            calculationTimes = self.calculationTimesDico['timespec'] + eoTimesList
        else:
            calculationTimes = eoTimesList
            pass
        #print 'eoTimesList',eoTimesList
        if calculationTimes:
            calculationTimes.sort()
            calculationTimes = elimCommonElementsInList(calculationTimes, 1E-15)
        self.calculationTimesDico['timespec'] = eo_zone_TimesList
        

        self.timespec=1

        # for outputs
        self.outputs_point = None
        self.outputs_zone  = None
        self.outputs_surf  = None
        outpoint = []
        outzone  = []
        outsurf  = []
        
        for eoDict in expected_output_dict_list:
            support = eoDict['support']
            supportType =  support.__class__.__name__
            if   supportType in ["Point2D","Point3D","Point"]:    outpoint.append(eoDict)
            elif supportType =="tuple":                           outsurf.append(eoDict)
            pass
#
        eoTimesJGLIST=[]
        for eoDict in outpoint+outsurf:
            OKtimespec='timespec' in eoDict.keys()
            if OKtimespec:timespec  = eoDict['timespec']
##             if 'timespec' in eoDict.keys():
            if timespec:
##                 timespec  = eoDict['timespec']
                spec = timespec.getSpecification()
                if spec == 'times':
                    eoTimesJGLIST.extend(timespec.getTimes())
                    pass
                pass
            pass
        if len(eoTimesJGLIST):
            eoTimesJGLIST.sort()
            eoTimesJGLIST=elimCommonElementsInList(eoTimesJGLIST, 1E-15)
            ideb=0
            while (eoTimesJGLIST[ideb]-first_time) < -1E-15:
                ideb+=1
                pass
            ifin=len(eoTimesJGLIST)
            while (eoTimesJGLIST[ifin-1]-final_time) > 1E-15:
                print 'eoTimesJGLIST[ifin-1],final_time',eoTimesJGLIST[ifin-1],final_time
                ifin-=1
                pass
            eoTimesJGLIST=eoTimesJGLIST[ideb:ifin]
            self.calculationTimesDico['all_times']=\
                     tableUnion(self.calculationTimesDico['all_times'],eoTimesJGLIST)
            pass

        # Traitement des differents types de support :
        if len(outpoint) != None:
	    nbCell    = len(outpoint)
	else:
	    nbCell    = 0
        if len(outsurf) != None:
            nbSurf    = len(outsurf)
	else:
            nbSurf    = 0
	
        nbZoneBil = len(outzone)

        # Points ...
        outCell       = []
        quantitePoint = []        
        nomPoint      = []
        supportPoint  = []        
        tempsPoint  = []        
        for pp in outpoint:
#  
            point=pp['support']
            #elem_index=getElementContainingPoint(list(point.getCoordinates() ),self.mesh)
            elem_index=getElementOnPoint(point.getCoordinates(),self.mesh) 
#    
            supportPoint.append(pp['support'])
            outCell.append(elem_index)
            quantitePoint.append(pp['quantity'].upper())
            nomPoint.append(pp['name'])
            if 'timespec' in pp.keys():
                tempsPoint.append(pp['timespec'])
                pass
            pass

        nbFac        = []
        quantiteSurf = []
        nomSurf      = []
        supportSurf  = []
        globalInd    = []
        tempsSurf    = []
        for ss in outsurf:
            bboundary = ss['support'][0]
            nbFac.append( bboundary.getNbElements() )
            globalInd.append(bboundary.getGlobalIndexes())
            quantiteSurf.append(ss['quantity'].upper())
            nomSurf.append(ss['name'])
            supportSurf.append(ss['support'])
            if 'timespec' in ss.keys():
                tempsSurf.append(ss['timespec'])

        # Zones ...
        nbCellZone   = []
        cellZoneTemp = []
        quantiteZone = []
        nomZone      = []
        supportZone  = []
        where        = []
        tempsZone    = []
        for zz in outzone:
            print 'OUTPUT ZONE !',zz['name']
            #raise stop
            zzone = zz['support']
            supportZone.append(zzone)
            nbCellZone.append(zzone.getNbElements())
            cellZoneTemp.append(zzone.getGlobalIndexes())
            quantiteZone.append(zz['quantity'].upper())
            nomZone.append(zz['name'])
            if 'timespec' in zz.keys():
                tempsZone.append(zz['timespec'])
            # localisation de la sortie pour une zone : 'face' ou 'center' sont implementees
            if 'localisation' in zz.keys():
                if zz['localisation'] not in ['face','center']:
                    raise "Not Yet Implemented"
                else:
                    where.append(zz['localisation'])
            else:
                where.append('center')

        self.outputs_point = {'nbCell':nbCell,
                              'outCell' :outCell,
                              'quantite':quantitePoint,
                              'nom':nomPoint,
                              'support':supportPoint,
                              'timespec':tempsPoint}
        
        self.outputs_zone  = {'nbZoneBil':nbZoneBil,
                              'nbCellZone':nbCellZone,
                              'cellZoneTemp':cellZoneTemp,
                              'quantite':quantiteZone,
                              'nom':nomZone,
                              'support':supportZone,
                              'where':where,
                              'timespec':tempsZone}
        
        self.outputs_surf = {'nbSurf':nbSurf,
                             'nbFac':nbFac,
                             'quantite':quantiteSurf,
                             'nom':nomSurf,
                             'support':supportSurf,
                             'globalInd':globalInd,
                             'timespec':tempsSurf}

        return
        
    def setUserPermeability(self):
        self.userPermeability = True
        return None
        
    def setRank(self,rank):
        self.mpirank = rank
        return None

    def timeDiscretizationTreatment(self):
        """ Once the user has given time discretization parameters,
        calculationtimes are changed for Traces (Imfs code).

        One must take care of ExpectedOutputs (EO) :
        - EO with a timespec in 'frequency' have to be changed
        in EO with timespec in 'times' with good dates.
        """
        #
        dico=self.parameterDico
        if not dico.has_key('timediscr') :
            self.setCalculationTimes([0.,1.])
            return
        timediscr=dico['timediscr']

        temps=self.calculationTimesDico ['all_times'][:]
        begin_time=temps[0]
        end_time=temps[-1]
        #
        for td in timediscr:
            li=td.getTimeInterval()
            tdeb,tfin=li[0],li[1]
            if tdeb<begin_time:tdeb=begin_time
            if tfin>end_time:tfin=end_time
            td.setTimeInterval([tdeb,tfin])
            pass

        newtemps=[]
        for i in range(len(temps)-1):
            period=temps[i+1]-temps[i]
            tdiscrOk=0
            for td in timediscr:
                try:
                    li=td.getTimeInterval()
                except:
                    end_time=self.calculations_times[-1]
                    li=(begin_time,end_time)
                    pass
                tdeb,tfin=li[0],li[1]

                espinol=1.e-6
                ttdeb=tdeb-abs(tfin-tdeb)*espinol
                ttfin=tfin+abs(tfin-tdeb)*espinol
                if ttdeb<=temps[i] and temps[i+1]<=ttfin:
                    td_good=td
                    tdiscrOk=1
                    break
                pass
            if not tdiscrOk:
                msg="\nLes intervalles de temps choisis pour la discretisation temporelle"
                msg+='\n(via le setParameter), de la forme [t_debut,t_fin], doivent '
                msg+='\netre en accord avec les instants passes au probleme (qui sont justement'
                msg+='\nles dates jalons prevues a cet effet. En clair, t_debut et t_fin'
                msg+='\nde chaque ImfsTimeDiscr doivent correspondre a des instants passes au probleme.'
                msg+='\n\nARRET !\n'
                raise _TimeException()
            td_good.adapt2period(tdeb,temps[i],temps[i+1])
            if i==0:newtemps.append(temps[i])
            newtemps+=td_good.getDatesList(temps[i],temps[i+1],interval='opened')
            newtemps.append(temps[i+1])
            pass
        self.setCalculationTimes(newtemps)

        return None

    #---------------------------------------------------------------------------
    #---------------------------------------------------------------------------
    def vtkMeshFile(self,mesh,fileType = None):
        """
	vtk representation in the legacy format of a mesh file :
	
	ASCII
        DATASET UNSTRUCTURED_GRID
        POINTS 302 float
        CELLS
        CELL_TYPES
        CELL_DATA  300
        SCALARS material_values float

        LOOKUP_TABLE default

        """
        self.vtkMeshFile = 'mesh.vtk'
 	self.file_mesh=open(self.vtkMeshFile,'w')
        self.file_mesh.write("%s\n"%("# vtk DataFile Version 2.0"))
        self.file_mesh.write("%s\n"%("vtk output"))
        self.file_mesh.write("%s\n"%("ASCII"))
        self.file_mesh.write("%s\n"%("DATASET UNSTRUCTURED_GRID")) 
	self.file_mesh.write("%s %i %s\n"%("POINTS",mesh.getNodesAnz(),"float "))

	dim = mesh.getSpaceDimensions()
	#
	# coordinates of nodal points
	#
	koordinaten = mesh.getNodesCoordinates()

	if (dim==2):
	    for i in range(0,len(koordinaten)):
	        self.file_mesh.write("%15.8e %15.8e %15.8e\n"%(koordinaten[i][0],koordinaten[i][1],0.))
	elif (dim==3):	
	    for i in range(0,len(koordinaten)):
	        self.file_mesh.write("%15.8e %15.8e %15.8e\n"%(koordinaten[i][0],koordinaten[i][1],koordinaten[i][2]))
	else:
	    raise " error in mesh dimension "

	connectivity = mesh.getConnectivity()
	
	numberOfCells = len(connectivity)

	gmshType, vtkTyp  = mesh.getType()
        #print "dbg vtkTyp ",vtkTyp,connectivity[0:100]
        #print "dbg gmshType ",gmshType
        #raw_input("dbg elmer: ")
        cellListSize = 0
	for i in range(0,numberOfCells):                # gmsh meshes have only one type of elements
	    gmshType = connectivity[i][1]
	    if gmshType == 1:           # 2-node lines
	        cellListSize += 3
	    if gmshType == 2:           # 3-node triangles
	        cellListSize += 4
	    if gmshType == 3:           # 4-node quadrangles
	        cellListSize += 5
	    elif gmshType == 4:         # 4-node tetrahedron
	        cellListSize += 5
            elif gmshType == 5:         # 8-node hexahedrons
	        cellListSize += 9
            elif gmshType == 6:         # 6-node prism
		cellListSize += 7
            elif gmshType == 7:         # 5-node pyramid
		cellListSize += 6

        self.file_mesh.write("CELLS %i %i\n"%(numberOfCells,cellListSize))
	for cell in connectivity:
	    #print " cell ",cell,cell[1]
	    #print " cell _vtkGmsh",cell,cell[1],_vtkGmsh(cell[1])
	    #raw_input(" cell ")
	    vtkTyp = _vtkGmsh(cell[1])
	    ind = cell[2]+3
	    if (vtkTyp==3):                                                                 # 2-node line
	        self.file_mesh.write("%i %i %i\n"%(2,\
		                                      cell[ind]-1,
		                                      cell[ind+1]-1))
	    elif (vtkTyp==5):                                                               # 3-node triangle
	        self.file_mesh.write("%i %i %i %i\n"%(3,\
		                                      cell[ind]-1,
		                                      cell[ind+1]-1, 
		                                      cell[ind+2]-1))
 	    elif (vtkTyp==9):                                                               # 4-node quadr
 	        self.file_mesh.write("%i %i %i %i %i\n"%(4,\
		                                         cell[ind  ]-1, 
		                                         cell[ind+1]-1, 
		                                         cell[ind+2]-1, 
		                                         cell[ind+3]-1))
 	    elif (vtkTyp==10):                                                              # 4-node tetra
 	        #print "zcell ",cell
 	        self.file_mesh.write("%i %i %i %i %i\n"%(4,\
		                                         cell[ind  ]-1,
		                                         cell[ind+1]-1,
		                                         cell[ind+2]-1, 
		                                         cell[ind+3]-1))
  	    elif (vtkTyp==12):                                                              # 8-node hexahedron	
	        self.file_mesh.write("%i %i %i %i %i %i %i %i %i\n"%(8,\
		                                         cell[ind  ]-1,\
		                                         cell[ind+1]-1,\
		                                         cell[ind+2]-1,\
		                                         cell[ind+3]-1,\
		                                         cell[ind+4]-1,\
		                                         cell[ind+5]-1,\
		                                         cell[ind+6]-1,\
		                                         cell[ind+7]-1))
  	    elif (vtkTyp==13):                                                              # prism	: 6-nodes
	        self.file_mesh.write("%i %i %i %i %i %i %i\n"%(6,\
		                                         cell[ind  ]-1,\
		                                         cell[ind+1]-1,\
		                                         cell[ind+2]-1,\
		                                         cell[ind+3]-1,\
		                                         cell[ind+4]-1,\
		                                         cell[ind+5]-1))
  	    elif (vtkTyp==14):                                                              # pyramid : 5-nodes
	        self.file_mesh.write("%i %i %i %i %i %i %i\n"%(5,\
		                                         cell[ind  ]-1,\
		                                         cell[ind+1]-1,\
		                                         cell[ind+2]-1,\
		                                         cell[ind+3]-1,\
		                                         cell[ind+4]-1))
            self.file_mesh.flush()
        self.file_mesh.write("%s %i\n"%("CELL_TYPES",numberOfCells))
        #print "dbg vtkTyp",vtkTyp,numberOfCells
	for i in range(0,numberOfCells):
	    gmshType = connectivity[i][1]
	    if gmshType not in [1,2,3,4,5,6]: print " gmshType ",gmshType
	    if gmshType == 1:           # 2-node line
	        cellTyp = 3
	    elif gmshType == 2:         # 3-node triangle
	        cellTyp = 5
	    elif gmshType == 3:         # 4-node quadrangle
	        cellTyp = 9
	    elif gmshType == 4:         # 4-node tetrahedron
	        cellTyp = 10
	    elif gmshType == 5:         # 8-node hexahedron
	        cellTyp = 12
            elif gmshType == 6:         # 6-node prism
		cellTyp = 13
            elif gmshType == 7:         # 5-node pyramid
		cellTyp = 14
	    self.file_mesh.write("%i\n"%(cellTyp))
        self.file_mesh.write("%s %i\n"%("CELL_DATA",numberOfCells))
        self.file_mesh.write("%s\n"%("SCALARS material_values float\n"))
	
        self.file_mesh.write("%s\n"%("LOOKUP_TABLE default\n"))
	for i in range(0,numberOfCells):
	    self.file_mesh.write("%i\n"%(0))
	self.file_mesh.flush()
	self.file_mesh.close()
	return None
    #---------------------------------------------------------------------------
    #---------------------------------------------------------------------------    
    def setAdditionalSourceValues(self,source):
        """
        Transfer of a concentration field to elmer. this corresponds to the source term necessary
	to the Picard algorithm. In the case of the chemistry coupling, this source term is issued
	from the variation of the solid phase.
	See the AdvectionDiffusion solver
        """
	self.essai.setSource(source)
	return None
	
    def setBodyList(self,bodies):
        """
        we give access of bodies list to elmer, bodies
        here are to be understood in the sense of the coupling algorithm
        """
        self.bodies = bodies
#        print bodies
#        print dir(bodies)
        #raw_input("bodies")
        return None
	
    #-----------------------------------------------
    #-----------------------------------------------
    def setConcentrationValues(self,concentrations):
        """
        Transfer of concentrations to elmer: two cases with or without temperature
        0:      without temperature
        2:      with temperature
        """
        if self.instance==0:
#	    print " coupling ",py setconcentration values for instance 0",self.instance,self.unAnzahl,len(concentrations)
	    #raw_input()
	    self.essai.setConcentration(concentrations)
        elif self.instance==2:
	    print " type of self.unAnzahl for instance 2",self.instance,self.gunAnzahl
	    #self.essaig.setConcentration(concentrations,1,self.gunAnzahl)
        else:
	    #self.essai.setConcentrationValues(concentrations,1,self.unAnzahl-1)
	    pass
	return None
    #---------------------------------------------------------------------------
    #---------------------------------------------------------------------------
       
    def setPermeabilityField(self,permeabilityField):
        """
        
        """
        self.essai.setPermeabilityField(permeabilityField)
       
    def getPermeabilityField(self):
        """
        
        Used to retrieve th permeability field for output
        
        """
        return self.essai.getPermeabilityField()
    
    
       
    def setSpeciesNames(self):
        """set species names
           speciesList :  contains a species list
           return a species names list
        """        
        self.speciesNamesList = []
        ind = 0
        for species in self.speciesList:
            print "dbg elmer species names ",ind,species.getName()
            #raw_input()
            self.speciesNamesList.append(species.getName().upper())
            ind+=1
        return None

    def setSpecies(self, speciesList):
        """
        used to specify species names to the transport tool.
        """

        self.nbSpecies        = len(speciesList)
        self.speciesList      = speciesList
        self.setSpeciesNames()

    def setTemperature(self):
        """
        temperature for elmer is switched on.
        """
	self.temperature = True  
	return None

    def unsetTemperature(self):
        """
        temperature for elmer is switched off.
        """
	self.temperature = False  
	return None

    def setTemperatureField(self,temperatureField):
        """
        Transfer of the temperature field to elmer.
        
        """
#        print " setTemperatureField",len(temperatureField)
	self.essai.setTemperature(temperatureField)
	return None

    def setBodies(self,bodies):
    
        """
        We set a list of bodies to be handled by elmer
        """
        self.bodies = bodies

    def getBodies(self):
    
        """
        We get from elmer a bodies list
        """
        return self.bodies

    def setEffectiveDiffusion(self, fieldList):
        """
        Through that function, we set the effective diffusion over the domain
        for all species
        """
        print dir(fieldList[0]),self.speciesNamesList
        for specInd in range(len(self.speciesNamesList)):
            speciesName = self.speciesNamesList[0]
            field      = fieldList[0]
            values     = field.getValues()
            bodiesDico  = Dico()
            val      = values[0]
            bodiesDico["domain"] = (val)
            self.effectiveDiffusionDico[speciesName] = bodiesDico
        return
        
    def setPorosity(self, fieldList):
        """
        A porosity for all species is set, the porosity field 
        being valid over the domain, so as constructed, the porosity
        is affected to CB
        """
        for specInd in range(len(fieldList)):
            specieName = self.speciesNamesList[specInd]
            field      = fieldList[specInd]
            values     = field.getValues()
            print "dbg porosity dico setting",values
            self.porosityDico[specieName] = values
        return None

    def setPorosityField(self,porosityfield):
        """
        sets the porosity to elmer
                       
        Input  : a porosity field, a scalar being associated to each mesh node 
        """
        self.essai.setPorosityField(porosityfield)
	print " im_n dbg setPorosityValues"
	return None
    
    def getPorosityValues(self):
        """
        This method is used to supply a porosity list to the chemistry code.
	It should be enhanced .
        """
        porosityField = [1.0]*self.mesh.getNodesAnz()
        print " e dbg transport: number of nodes",self.mesh.getNodesAnz()
	#for body in self.getBodies():
	    #print dir(body)
	    #print " support          ",dir(body.getSupport())
	    #print " zone             ",body.getZone()
        
	for body in self.getBodies():
            porosityValue = body.material.getPorosity().value
	    print "porosityValue ",porosityValue,len(body.getSupport().getBodyNodesList())
            for i in body.getSupport().getBodyNodesList():
                porosityField[i-1] = porosityValue
        #print "edbg length of porosityfield ",len(porosityField)
        #raw_input("elmer length porosity field")
        #raw_input("getPorosityValues")
	return porosityField
    
    def setUnknownsNumber(self,unAnzahl):
        """
        Set the transported phase unknown number
        """
        self.unAnzahl = unAnzahl
	return None
	WElmer.c
    def writeEquation1(self):
        sifFile = self.sifFile
        sifFile.write("! ~~\n! Equation p28 ref. Manual\n! ~~\n")
        #print "self.speciesNamesList",self.speciesNamesList
        #raw_input("self.speciesNamesList")
        for ind in range(len(self.speciesNamesList)):
            sifFile.write("Equation %i\n"%(ind+1))
            sifFile.write("  Advection Diffusion Equation %s True\n"%self.speciesNamesList[ind])
            sifFile.write("  Convection %s\n"%self.advConv)
            sifFile.write("  Concentration Units = Absolute Mass\n")
               
        if self.temperature == None:
            sifFile.write("  ActiveSolvers(1) = 1\n")
        else:
            sifFile.write("  ActiveSolvers(2) = 1 2\n")
        sifFile.write("End\n\n")
        return None
        
    def writeMaterial1(self):
        """
        A loop over materials and species.
        Each material is associated to each species.
        The numbering is on three digits, two for the species, at least one for the region.
        For the moment, the material is independant of the species.
        """
       
        sifFile = self.sifFile
        sifFile.write("! ~~\n! Material p29 ref. Manual\n! ~~\n")        
        for inds in range(len(self.speciesNamesList)):
            for indb in range(len(self.bodies)):
                stinds = _digit(inds)
                stindb = str(indb+1)+stinds
                sifFile.write("Material %s\n"%(stindb))
                if self.advConv == "Constant":
                    v = self.darcyVelocity.getValue()
                    sifFile.write("  ! darcy velocity\n")
                    sifFile.write("  Convection velocity %e %e %e\n"%(v[0],v[1],v[2]))
                sifFile.write(" %s Diffusivity %15.10e\n"%(self.speciesNamesList[inds],\
                                  self.bodies[indb].getMaterial().getEffectiveDiffusion().value.value))
                
                sifFile.write(" %s Soret Diffusivity %15.10e\n"%(self.speciesNamesList[inds],\
                                  self.bodies[indb].getMaterial().getThermalConductivity().value.value))
                sifFile.write("End\n\n")
        return None

def _TimeException():	
    message = "look at the time discretisation, discrepancies exist\n"
    raise Exception, message
  
def _digit(ind):
    if ind < 8:
        return "0"+str(ind+1)
    else:
      return str(ind+1)
def _vtkGmsh(indGmsh):
        """
        that function is used to treat the vtk / Gmsh depdency
        see page 9 of the vtkfile-formats.pdf (4.2)
        """
	if indGmsh == 1:           # 2-node line        vtk_line
	    indVtk = 3
	elif indGmsh == 2:         # 3-node triangles   vtk_triangle
	    indVtk = 5
	elif indGmsh == 3:         # 4-node quadrangles vtk_quad
	    indVtk = 9
	elif indGmsh == 4:         # 4-node tetrahedron vtk_tetra
	    indVtk = 10
        elif indGmsh == 5:         # 8-node hexahedrons vtk_hexaedron
	    indVtk = 12
        elif indGmsh == 6:         # 6-node prism       vtk_wedge
	    indVtk = 13
        elif indGmsh == 7:         # 5-node pyramid     vtk_pyramid
	    indVtk = 14
       
        return indVtk
