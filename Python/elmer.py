# -*- coding: utf-8 -*-
"""
class Elmer, enables to handle elmer as a transport tool
In fine should be able to launch elmer for linear and
non linear transport
Temperature is added
A linear elasticity mechanical problem can also be treated.
Velocity: saturated

        For the moment, the velocity can be:

                constant:

                        In that case, the velocity is introduced as a Darcy velocity, There are two ways to introduce the porosity :
                                1/ introducing the porosity coefficient in the effective diffusion coefficient, the porosity being set to one
                                2/ introducing the real porosity.


                piecewiseConstant:

                        The velocity is introduced as a matc function, the only dependance is over time

                variable:

                        In that case, the velocity is introduced as a Darcy velocity



         If the porosity is varying

         It enables to introduce 1D wellbores in the simulation; potentially two phases with a varying mass flow over time.

"""

from __future__ import absolute_import
from __future__ import print_function
from elmertools import *

from exceptions import Exception

from elmerroot import ElmerRoot

from FortranFormat import FortranFormat, FortranLine

from generictools import color, memberShip

from inspect import currentframe

from listtools import toList

#from tools import *

from listtools import elimCommonElementsInList

import os

import string
import sys

from types import NoneType, StringType, FloatType, IntType

from vector import V

from PhysicalProperties import Density,\
                               Velocity

import WElmer
from six.moves import range
from six.moves import input

_fe158 = FortranFormat("E15.8")
def _fote158(arg):
    return str(FortranLine([arg],_fe158))

_i10   = FortranFormat("I10")

def _foti10(arg):
    return str(FortranLine([arg],_i10))

class Elmer(ElmerRoot):
    """
    Class used to define elmer as transport or mechanical tool
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
    def __init__(self, meshFile="elmerMesh"):
        """
        meshFileName : mesh file name, with the extension .msh
        and that associated elmer format grid files are available
        """
        #print " dbg elmer class instantation "
        ElmerRoot.__init__(self,meshFile)
        self.__dict = {}
        self.advConv                    = "No"
        self.saturation                 = "saturated"
        self.dirBCList                  = []
        self.dirBCList1                 = []                                                # it should replace self.dirBCList
        self.dirICList                  = []
#        if meshFile.getName()[-4:]  == ".msh":
#            print "toto"
            #raw_input()
#       self.meshFile           = meshFile.getName()
#       self.meshDirectoryName = self.meshFile[0:-4]
        self.gravityDirection           = V(0,-1,0)
        self.gravityValue               = 9.78
                                                                                            #
                                                                                            # water parameters and liquid parameters ?
                                                                                            # 
        self.waterDensity               = 1000.0        # kg/m3
        self.waterHeatCapacity          = 4187          # J/(kgK)
        self.waterHeatConductivity      = 0.60          # W/(mK)
        self.mesh                       = meshFile
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
        self.mechanicsParameterDico     = Dico()
        self.porosityDico               = Dico()
        self.sifFileName                = "test.sif"
        self.simulationType             = "transient"
        self.bdfOrder                   = "2"
        self.sorptionLawDico            = Dico()
        self.temperature                = None
        self.zonePerCellDico            = Dico()
        self.charge                     = []
        self.velocity                   = []
        self.boundPlot                  = []
                                                                                            # young modulus is a
                                                                                            # scalar in the isotropic case
                                                                                            # or a 6x6 (3D)
                                                                                            # or a 4x4 (2D or axys. case)
        self.elasticity                 = None
        self.ElasticityModulus          = "Constant"                                        # default value
        #
        self.youngModulus               = None                                              # a scalar in the isotropic case
                                                                                            #
                                                                                            # for the moment only an
                                                                                            # isotropic case is considered
                                                                                            #
        self.poissonRatio               = None
        self.referenceTemperature       = None

        self.elmerZonesNamesList = []
        self.timespec = 0
        self.instance = 0
        if not hasattr(self,'problemType'):
            self.problemType='unknown'
            pass
        if self.problemType not in ['unknown','hydro','chemicaltransport','mechanical','thmc']:
            raise Exception(" check the kind of problem you want to solve ")
        #
        # call to setDefaultParameters, settings of default tool parameters
        #
        self.setDefaultParameters()
        self.setDefaultParameters(self.chargeParameterDico)
        self.outputs_point = None
        self.outputs_zone  = None
        self.outputs_surf  = None
        return None

    def createSifFile(self, problemType = None):
        """
        This method is used to generate the sif file. The sif
        file is the one read by the Elmer solver.
        Parameters relevant to time and time step
        are not relevant, the time step being driven through python.
        """
        if problemType == None:
            problemType = self.problemType
        self.sifFile = sifFile = open(self.sifFileName,"w")
        self.sifFileW = sifFileW = sifFile.write
        sifFileW("Check Keywords Warn\n\n")
        #sifFileW("$ function essaif(X){\\\n\n"+\
        #         " a = 15.0;\\\n\n"+\
        #         " b = 0.08;\\\n\n"+\
        #         "  _essaif = a + b*(X);\\\n"+\
        #         "\n}\n\n")
        sifFileW("Header\n")
        sifFileW("Mesh DB \".\" \"%s\"\n"%self.meshDirectoryName)
        sifFileW("Include Path \".\" \n")
        sifFileW("Results Directory \"\"\nEnd\n\n")
#        sifFileW("Results Directory \"\"\nEnd\n\n")
        #
        self.writeSimulation()
        self.writeConstants()
        self.writeBodies()
        self.writeMaterial()
#        if self.bodyForce: self.writeBodyForce()
        if problemType in ["chemicaltransport","chemicaltransportproblem","thmc","thmcproblem"]:
            self.writeBodyForce()
            pass
        if problemType in ['unknown','chemicaltransport',"thmcproblem"]:
            self.writeEquation()
            self.writeSolver()
            pass
        elif problemType in ["mechanical"]:
            self.writeMechanicalEquation()
            self.writeMechanicalSolver()
            pass
        self.writeBoundaryCondition(problemType)
        #printm( "dbg16032015 writeBoundaryCondition over\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        self.writeInitialCondition()
        #printm( "dbg16032015 writeInitialCondition over\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        #raw_input(color.red+"siffile written"+color.end)
        sifFile.close()

    def getVelocity(self):
        """
        Used to retrieve the velocity from elmer with the computed option, the velocity is obtained through elmer.
        """
        if "computed" in self.advConv.lower():
            return self.elmso.getVelocity()
        else:
            return False

    def getCharge(self):
        """
        Used to retrieve the velocity from elmer with the computed option, the velocity is obtained through elmer.
        """
        if "computed" in self.advConv.lower():
            return self.elmso.getCharge()
        else:
            return False

    def getHelp(self,func = None):
        """
        That function is used to get some help on the
        class and on relevant functions
        Ex: getHelp() or getHelp(a.function)
        """
        if func == None:
            print(self.__doc__)
            pass
        else:
            print(func.__doc__)
            pass
        pass

    def writeBodies(self):
        """
        Bodies are asociated to materials and equations.
        Only one equation is treated when temperature is set to None.
        It means that element has to be modified for chemistry/temperature coupling
        Otherwise, two equations are taken into account...
        So, bodies are associated to initial conditions and their number
        mostly depends on material numbers.
        """
        sifFileW = self.sifFileW
        sifFileW("! ~~\n! Body\n! ~~\n")
        indb = 0
        ibc = 0
        if self.problemType in["chemicaltransport","thmc"]:
            #for ibc in range(len(self.dirBCList)):
            #    indBody = self.dirBCList[ibc][1]
            #    sifFileW("Body %i\n"%(indBody))
            #    sifFileW("  Name = \"body%s\"\n"%(indBody))
            #    sifFileW("  Equation = 1\n")
            #    stinds = _digit(0)
            #    stindb = str(indb+1) + stinds
            #    sifFileW("  Material = %s\n"%(indBody))
            #    sifFileW("End\n\n")
            #    pass
#
# doit etre modifie des que plusieurs materiaux interviennent
# ok for the mechanics, the dictionnary having material as key.
# its construction is based on regions.
#
#        if len(self.dirBCList) == 0:
#            dec = 1                     # no boundary condition
#        else:
#            dec = 2                     # one boundary condition
            if (len(self.dirBCList) != 0): ibc+=1
            for  indic in range(len(self.dirICList)):
                print(self.dirICList)
                indBody = self.dirICList[indic]["index"]
                sifFileW("Body %i\n"%(indBody))
                sifFileW("  Equation = 1 \n")
                sifFileW("  Target Bodies (1) = %s\n"%str(self.dirICList[indic]["index"]))

                stinds = _digit(0)
                stindb = str(indic+1) + stinds
                sifFileW("  Material = %s\n"%(indBody))
                sifFileW("  Initial Condition = %s\n"%(indBody))
#            sifFileW("  Body Force = %s\n"%(indb+1))
                sifFileW("  Body Force = %s\n"%(1))
                sifFileW("End\n\n")
                pass
            pass
        elif self.problemType == "mechanical":
            print(self.dirBCList1)
            #
            # boundary conditions are set at once through an appennd => [0]
            #
            for boundaryCondition in range(len(self.dirBCList1[0].keys())):
                print(" body treatment ", self.dirBCList1[0][boundaryCondition])
                sifFileW("Body %i\n"%( self.dirBCList1[0][boundaryCondition]["index"]))
                sifFileW("  Equation = 1 \n")
                sifFileW("  Material = %s\n"%(self.dirBCList1[0][boundaryCondition]["index"]))

                sifFileW("End\n\n")
                pass
#
# to be modified
#
            ic = 1
            print(self.dirICList)
            for initialCondition in range(len(self.dirICList[0].keys())):
#            sifFileW("Body %i\n"%(indb+ibc+1))
                sifFileW("Body %i\n"%(self.dirICList[0][initialCondition]["index"]))
                sifFileW("  Equation = 1 \n")
                stinds = _digit(0)
                stindb = str(ibc+indb+1)+stinds
                sifFileW("  Material = %i\n"%(self.dirICList[0][initialCondition]["index"]))
                sifFileW("  Initial Condition = %s\n"%(ic))
                sifFileW("End\n\n")
                ic+=1
                pass
            pass



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
        sifFileW = sifFile.write
        sifFileW("! ~~\n! Material p29 ref. Manual\n! ~~\n")

        for indb in range(len(self.bodies)):
            stinds = _digit(0)
            stindb = str(indb+1)+stinds
            sifFileW("Material %s\n"%(self.bodies[indb].support.body[0]))
            #
            # water density is supposed to be 1000 kg / m3. But it can
            # be fixed to other walues through the setWaterDensity function
            #
            #
            # rock density                    2700 kg / m3
            #
            sifFileW(" ! --------------------------------------------\n")
            sifFileW(" !Properties linked to the host rock simulation\n")
            sifFileW(" ! --------------------------------------------\n")
            porosity = self.bodies[indb].getMaterial().getPorosity().value
            sifFileW(" Density = Real %15.10e\n"%(self.waterDensity*porosity+2700*(1.-porosity)))
            if self.problemType in ["chemicaltransport","thmc"]:
                sifFileW(" Water Density = Real %15.10e\n"%(self.waterDensity))
                pass
            if self.problemType in ["chemicaltransport", "mechanical", "elasticity","thmc"] :
                if self.problemType in ["mechanical", "elasticity","thmc"] :
                    sifFileW("! Solid Density = Real %15.10e\n"%(self.bodies[indb].getMaterial().getDensity().value))
                    pass
                pass
            else:
                raise Warning, "to be enhanced to consider the specific density"
            sifFileW(" Viscosity = Real %15.10e\n"%(1.e-4))                            # dynamic viscoity of water.
            sifFileW(" Porosity = Real %15.10e\n"%(porosity))
            if self.problemType in ["mechanical", "elasticity","thmc"] :
                if self.ElasticityModulus in ['Constant',False]:
                    sifFileW(" Variable Elasticity Modulus = Logical False\n")
                    pass
                else:
                    sifFileW(" Variable Elasticity Modulus = Logical True\n")
                    pass
                print(self.bodies[indb].getMaterial().youngModulus.value)
                print(self.bodies[indb].getMaterial().poissonRatio.value)
                #raw_input()
                if self.bodies[indb].getMaterial().youngModulus:
                    sifFileW(" Youngs Modulus = Real %15.10e\n"%(self.bodies[indb].getMaterial().youngModulus.value))
                    pass
                else:
                    raise Warning, " the young modulus is mandatory"
                if self.bodies[indb].getMaterial().poissonRatio:
                    sifFileW(" Poisson Ratio = Real %15.10e\n"%(self.bodies[indb].getMaterial().poissonRatio.value))
                    pass
                else:
                    raise Warning, " the poisson ratio is mandatory"
                pass

                                                                                            #
                                                                                            #       temperature:
                                                                                            #       specificHeatCapacity and heatConductivity
                                                                                            #
            if self.temperature==True:
                if self.bodies[indb].getMaterial().getSpecificHeat() :
                    specificHeatCapacity    = self.bodies[indb].getMaterial().getSpecificHeat().value
                    sifFileW(" Heat Capacity = Real %15.10e\n"%(specificHeatCapacity))
                    pass
                else :
                    raise Exception("As the temperature mode is used, you have to give a heat capacity")
                if self.bodies[indb].getMaterial().getThermalConductivity() :
                    heatConductivity        = self.bodies[indb].getMaterial().getThermalConductivity().value.value
                    sifFileW(" Heat Conductivity = Real %15.10e\n"%(heatConductivity))
                    pass
                else :
                    raise Exception("As temperature mode is used, you have to give a heat conductivity")
                #
                # we treat the heat capacity
                #
                if self.parameterDico["variableHeatCapacity"] == True:
                    sifFileW(" !\n ! We consider a variable heat capacity\n !\n")
                    sifFileW("  Variable Heat Capacity = Logical True \n\n")
                    pass
                #
                # we treat the heat conductivity
                #
                if self.parameterDico["variableHeatConductivity"] == True:
                    sifFileW(" !\n ! We consider a variable heat conductivity\n !\n")
                    sifFileW("  Variable Heat Conductivity = Logical True \n\n")
                    pass
                #
                # viscosity
                #
                if self.bodies[indb].getMaterial().getViscosity() != None:
                    viscosity       = self.bodies[indb].getMaterial().getViscosity().value
                    sifFileW(" Viscosity         = Real %15.10e\n"%(viscosity))
                    pass
                pass
                                                                                            #
                                                                                            #       computed velocity: saturated flow
                                                                                            #
            if "computed" in str(self.darcyVelocity) and self.saturation == "saturated":
                if self.bodies[indb].getMaterial().getViscosity() != None:
                    viscosity       = self.bodies[indb].getMaterial().getViscosity().value
                    sifFileW(" Viscosity         = Real %15.10e\n"%(viscosity))
                    pass
                #print self.bodies[indb].getMaterial().getHydraulicConductivity()
                if type(self.bodies[indb].getMaterial().getHydraulicConductivity()) != NoneType:
                    sifFileW(" Hydr Conductivity = Real %15.10e\n"%(self.bodies[indb].getMaterial().getHydraulicConductivity().value.value))
                    sifFileW(" Saturated Hydraulic Conductivity = Real %15.10e\n"%(self.bodies[indb].getMaterial().getHydraulicConductivity().value.value))
                    pass
                if self.bodies[indb].getMaterial().getSpecificStorage() != None:
                    sifFileW(" Specific Storage = Real %15.10e\n"%(self.bodies[indb].getMaterial().getSpecificStorage().value))
                    pass
                pass
            elif "computed" in str("self.darcyVelocity") and self.saturation == "undersaturated":
                raise Exception, " for the moment, no unsaturated flow can be bounded to chemical transport "
                                                                                            #
                                                                                            #       compressibility
                                                                                            #
            sifFileW(" Compressibility Model = Incompressible\n")
            if self.problemType in ["chemicaltransport","thmc"]:
                tempcont = len(self.speciesNamesList)
                                                        #
                                                        # we write the diff.disp tensor
                                                        #
                for inds in range(tempcont):
                    effecDiff       = self.bodies[indb].getMaterial().getEffectiveDiffusion()
                    if (type(effecDiff) not in [NoneType]):
                        effecDiff       = effecDiff.value.value
                        pass
                    else:
                        effecDiff       = 0.0
                        pass
                    porosity        = self.bodies[indb].getMaterial().getPorosity()
                    if (porosity not in [NoneType]):
                        porosity        = porosity.value
                        pass
                    else:
                        porosity        = 1.0
                        pass
                    longitudinalDispersivity = self.bodies[indb].getMaterial().getKinematicDispersion()
                    if (type(longitudinalDispersivity) not in [NoneType]):
                        longDisp        = longitudinalDispersivity.value[0]
                        tranDisp        = longitudinalDispersivity.value[1]
                        pass
                    else:
                        longDisp        = 0.0
                        tranDisp        = 0.0
                        pass
                    v = None
                    if isinstance(self.darcyVelocity,Velocity):
                        v = self.darcyVelocity.getValue()
                        print(" v ",v)
                        pass
                    elif isinstance(self.darcyVelocity,StringType):
                        pass
                    if type(v)!=type(None):
                        if (len(filter(lambda x: type(x)==FloatType, v)) ==3):
                            norm = (v[0]**2+v[1]**2+v[2]**2)**0.5
                            if norm > 0:
                                darcy_x = v[0]**2/norm
                                darcy_y = v[1]**2/norm
                                darcy_z = v[2]**2/norm
                                pass
                            else:
                                darcy_x = 0.0
                                darcy_y = 0.0
                                darcy_z = 0.0
                                pass
                            pass
                        else:
                            darcy_x = 0.0
                            darcy_y = 0.0
                            darcy_z = 0.0
                            pass
                    else:
                        darcy_x = 0.0
                        darcy_y = 0.0
                        darcy_z = 0.0
                        pass
                    sifFileW(" %s Diffusivity\n"%(self.speciesNamesList[inds]))
                    sifFileW("     Size 3 3\n")
                    sifFileW("      Real    %15.10e %15.10e %15.10e\\\n" %(longDisp*darcy_x + effecDiff,0.,0.))
                    sifFileW("              %15.10e %15.10e %15.10e\\\n" %(0.,longDisp*darcy_y + effecDiff,0.))
                    sifFileW("              %15.10e %15.10e %15.10e\\\n" %(0.,0.,longDisp*darcy_z + effecDiff))
                    sifFileW(" End\n")
                                                                                            #
                                                                                            # to handle a one phase, one dimensional borehole
                                                                                            #
                    if self.parameterDico["oneDimensionalBoreHole"] and self.parameterDico["onePhaseBoreHole"]:
                        if inds == tempcont-1:
                            _writeHeatLoadParameters(sifFile, self.bodies[indb].support.body[0],self.bodies[indb].support.bodyName)
                            pass
                        pass
                                                                                            #
                                                                                            # to handle a two phases, one dimensional borehole
                                                                                            #
                    elif self.parameterDico["oneDimensionalBoreHole"] and self.parameterDico["vapor"]:
                        if inds == tempcont-1:
                            _writeTwoPhaseHeatLoadParameters(sifFile, self.bodies[indb].support.body[0],self.bodies[indb].support.bodyName)
                            pass

##                sifFileW(" %s Diffusivity = Real %15.10e\n"%(self.speciesNamesList[inds],\
##                                  longDisp*darcy_x + effecDiff))
#                sifFileW(" %s Soret Diffusivity = Real %15.10e\n"%(self.speciesNamesList[inds],\
#                                  self.bodies[indb].getMaterial().getThermalConductivity().value.value))
                    sifFileW("\n")
                sifFileW(" Long Dispersivity = Real %15.10e\n"%(longDisp))
                sifFileW(" Tran Dispersivity = Real %15.10e\n"%(tranDisp))
                                                                                            #
                                                                                            # We treat the velocity, see page 22
                                                                                            #
            if self.advConv == "Constant" and not self.parameterDico["vapor"]:
                v = self.darcyVelocity.getValue()
                sifFileW(" Convection Velocity 1 = %e\n"%v[0])
                sifFileW(" Convection Velocity 2 = %e\n"%v[1])
                sifFileW(" Convection Velocity 3 = %e\n\n"%v[2])
                pass
                                                                                           #
                                                                                           # the velocity is piecewise constant;
                                                                                           # introduced as a matc function or as a float if constant
                                                                                           #
            elif self.advConv == "PiecewiseConstant" and  not self.parameterDico["vapor"]:
                v = self.darcyVelocity.getValue()
                if (type(v[0]) == StringType):
                    if (indb==0):
                        sifFileW("%s"%(v[0]))
                        pass
                    sifFileW(" Convection Velocity 1 = Variable Time \n  Real MATC \"ux(tx)\"\n")
                    pass
                else:
                    sifFileW(" Convection Velocity 1 = %e\n"%v[0])
                    pass
                if (type(v[1]) == StringType):
                    if (indb==0):
                        sifFileW("%s"%(v[1]))
                        pass
                    sifFileW(" Convection Velocity 2 = Variable Time \n  Real MATC \"uy(tx)\"\n")
                    pass
                else:
                    sifFileW(" Convection Velocity 2 = %e\n"%v[1])
                    pass
                if (type(v[2]) == StringType):
                    if (indb==0):
                        sifFileW("%s"%(v[2]))
                        pass
                    sifFileW(" Convection Velocity 3 = Variable Time \n  Real MATC \"uz(tx)\"\n")
                    pass
                else:
                    sifFileW(" Convection Velocity 3 = %e\n"%v[2])
                    pass
                pass
                                                                                            #
                                                                                            # We read a velocity field:
                                                                                            # for steady and transient flows
                                                                                            #
            elif "Read" in self.advConv or self.advConv == "RComputed" and not self.parameterDico["vapor"]:
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
                formatToBeUsedForReading = len(line.split()[-1])+2
                self.points = []
                while "#group all" not in line:
                    #line = line.split()
                    self.points.append([float(line[0:formatToBeUsedForReading]),\
                                        float(line[formatToBeUsedForReading:2*formatToBeUsedForReading]),\
                                        float(line[2*formatToBeUsedForReading:3*formatToBeUsedForReading])])
                    line = velocityFile.readline()
                    pass
                while "#time" not in velocityFile.readline():
                    pass
                line = velocityFile.readline()
                physic = []
                while len(line) > 1:
                    physic.append([float(line[0:formatToBeUsedForReading]),\
                                   float(line[  formatToBeUsedForReading:2*formatToBeUsedForReading]),\
                                   float(line[2*formatToBeUsedForReading:3*formatToBeUsedForReading]),\
                                   float(line[3*formatToBeUsedForReading:4*formatToBeUsedForReading])])
                    line = velocityFile.readline()
                    pass
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
                    pass
                velFile = open("velRead","w")
                velFile.write("# generic velocity file to be read by WElmer\n")
                form = "%10s\n"
                velFile.write(form%(_foti10(len(vx))))
                form = "%15s %15s %15s\n"
                ind = 0
                for i in vx:
                    velFile.write(form%(_fote158(vx[ind]),_fote158(vy[ind]),_fote158(vz[ind])))
                    ind+=1
                    pass
                velFile.close()
                del(vx);del(vy);del(vz)
                #
                sifFileW(" Convection Velocity 1 = %e\n"%0.0)
                sifFileW(" Convection Velocity 2 = %e\n"%0.0)
                sifFileW(" Convection Velocity 3 = %e\n\n"%0.0)
                pass
                
            elif self.advConv == "Computed" and not self.parameterDico["vapor"]:
                sifFileW(" Convection Velocity 1 = %e\n"%0.0)
                sifFileW(" Convection Velocity 2 = %e\n"%0.0)
                sifFileW(" Convection Velocity 3 = %e\n\n"%0.0)
                pass
                                                                                            #
                                                                                            # if we have a vapor phase the
                                                                                            # fluid velocity is evaluated.
                                                                                            #
            elif self.parameterDico["vapor"]:
                sifFileW(" Convection Velocity 1 = Variable WMassFlow, Quality, VoidFraction\n")
                sifFileW("   Real Procedure \"aqueousVeloCalc\" \"getAqueousPhaseVelocity\"\n")
                sifFileW(" Convection Velocity 2 = %e\n"%0.0)
                sifFileW(" Convection Velocity 3 = %e\n"%0.0)
                pass
            else:
                sifFileW(" Convection Velocity 1 = %e\n"%0.0)
                sifFileW(" Convection Velocity 2 = %e\n"%0.0)
                sifFileW(" Convection Velocity 3 = %e\n\n"%0.0)
                pass
                                                                                            #
                                                                                            # we write here the data necessary to handle
                                                                                            # the thermal transfer for a 1D wellbore simulation
                                                                                            #
            sifFileW(" Save Materials = Logical true\n\n")
            sifFileW("End\n\n")
            pass
        return None

    def writeBodyForce(self):
        """
        The body force section may be used to give additional force terms for the equations

        For the one dimensional borehole simulator, the source term for heat is introduced. For the moment,
        only one body is considered over the whole pipe length
        the
        """
        sifFile = self.sifFile
        sifFileW = sifFile.write
        sifFileW("! ~~~~~~~~~~\n! Body Force\n! ~~~~~~~~~~\n")
        print(self.dirICList)
        for  indb in range(len(self.dirICList[0]["conc"])):
            if (indb==0):
                sifFileW("Body Force %i\n"%(indb+1))
                #for inds in range(len(self.speciesNamesList)):
                #    sifFile.write(" %s Diffusion Source = Real %15.10e\n"%(self.speciesNamesList[inds],0.0))
#                sifFile.write(" %5s Diffusion = Real %15.10e\n"%(self.speciesNamesList[inds],1.23456e-10))
#                Curvature Diffusion = Real 0.0
#                sifFile.write("Physical Units True \n")
                if self.oneDimensionalBoreHole != None:
                    if self.parameterDico["vapor"]:
                        sifFileW("  Twell = Variable WEnthalpy\n")
                        sifFileW("    Real Procedure \"wellTemperatureCalc\" \"getTwellLoad\"\n")
                        #
                        sifFileW("  Quality = Variable WEnthalpy\n")
                        sifFileW("    Real Procedure \"qualityCalc\" \"getQualityLoad\"\n")
                        #
                        sifFileW("  VoidFraction = Variable Quality\n")
                        sifFileW("    Real Procedure \"voidFractionCalc\" \"getWVoidFractionCalc\"\n")
                        #
                        sifFileW("  Heat Source = Variable WMassFlow, Twell, Quality, WEnthalpy\n")
                        sifFileW("    Real Procedure \"twoPhasesWellHeatSource\" \"getTwoPhasesWellHeatSource\"\n")
                        #
#                        sifFileW("  HTC = Variable MassFlow, Twell, Text, Quality, Enthalpy\n")
#                        sifFileW("  HTC = Variable WMassFlow, Twell, Quality, WEnthalpy\n")
#                        sifFileW("    Real Procedure \"heatTransferCoeff\" \"getHTCLoad\"\n")
                        #
                        sifFileW("  Pressure Diffusion Source = Real 0.0 !Variable WMassFlow\n")
                        sifFileW("    !Real Procedure \"frictionHydrostatic\" \"getPressureLoad\"\n")
                        pass                
                    else:
                        sifFileW("  Heat Source = Variable Temperature\n")
                        sifFileW("    Real Procedure \"monophasicWellHeatSource\" \"getMonophasicWellHeatSource\"\n")
                        pass
                pass
            pass

#        sifFileW("  Physical Units True \n")

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
        sifFileW = sifFile.write
        sifFileW("! ~~\n! Equation p28 ref. Manual\n! ~~\n\n")
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

        sifFileW("Equation 1\n")
        if self.advConv == "Computed":
            for i in range(ind,ind+2):
                string += str(ind+1)+" "
                ind+=1
        if self.problemType == "thmc":
            for i in range(ind,ind+2):
                string += str(ind+1)+" "
                ind+=1
        if self.parameterDico["vapor"]:
            string += str(ind+1)+" "
            ind+=1
            string += str(ind+1)+" "
            ind+=1

        sifFileW("  Active Solvers(%i) = %s\n"%(ind,string))
#        sifFileW("Advection Diffusion Equation = True\n")
#        sifFileW("Darcy Equation = True\n")
        #raw_input("porosity state "+ self.porosityState)
        if self.advConv == "Constant" or self.advConv == "PiecewiseConstant":
            sifFileW("  Convection = Constant\n")
            pass
        elif self.advConv == "Read":
            sifFileW("  Convection = \"read\"\n")
            pass
        elif "computed" in self.advConv.lower():# Should be changed to distinguish between darcy and navier-Stokes solver
            sifFileW("  Convection = \"dcomputed\"\n")
            pass
        elif (self.porosityState == "variable"):
            sifFileW("  Convection = %s\n"%"Constant")
            #raw_input("checking the variable porosity option ")
            #raise Warning, " That part of the software is under development at the moment"
        else: # we consider as delault value a constant velocity for a variable porosity
            sifFileW("  Convection = %s\n"%"No")

        sifFileW("  Concentration Units = Absolute Mass\n")

#        if self.temperature == None:
#            sifFileW("  ActiveSolvers(1) = 1\n")
#        else:
#            sifFileW("  ActiveSolvers(2) = 1 2\n")
        sifFileW("End\n\n")
        return None

    def writeMechanicalEquation(self):
        """
        The equation section is used to define a set of equations for a body or set of bodies.

        Elasticity solver linear relation between stress and deformation for small deformations
        if 2D problem:
            Plane Stress = True

        https://www.youtube.com/watch?v=XG0QRNo9AI0

        """
        sifFile = self.sifFile
        sifFileW = sifFile.write
        sifFileW("! ~~\n! Equation p28 ref. Manual\n! ~~\n\n")

        sifFileW("Equation 1\n")
        #
        #
        #
        if self.problemType == "mechanical":
            #
            # three solvers:        1 stress solver
            #                       2 ReleaseRateSolver
            #                       3 ResultOutputSolver
            #
            ind = 3
            string = "1 2 3"
            sifFileW("  Active Solvers(%i) = %s\n"%(ind,string))
            pass
        sifFileW("  Name = \"Elasticity\"\n")
        sifFileW("  Calculate Stresses = %s\n"%"True")

        if self.mesh.getDimensionString() == 2:
            sifFileW("  Plane Stress = True\n")
            pass
        sifFileW("End\n\n")
        return None

    def writeSolver(self):
        """
        The solver section defines equation solver control variables.
        Equation String [Advection Diffusion Equation Variable_name]
        Variable String Variable_name
        """
        sifFile = self.sifFile
        sifFileW = self.sifFileW
        sifFileW("! ~~\n! Solver p27 ref. Manual\n! ~~\n")
                                                                                            #
                                                                                            # aqueous unknowns treatment
                                                                                            #
        for ind in range(len(self.speciesNamesList)):
            sifFileW("Solver %i\n"%(ind+1))
            sifFileW("  Equation = Advection Diffusion Equation %s\n"%(self.speciesNamesList[ind]))

            sifFileW("  Variable = %s\n"%self.speciesNamesList[ind])
            sifFileW("  Variable DOFs = 1\n\n")

            sifFileW("  Procedure = \"AdvectionDiffusionTimeStep\" \"AdvectionDiffusionTimeStepSolver\"\n")
            sifFileW("  Linear System Solver = %s\n"%self.parameterDico["Linear System Solver"])
            if self.parameterDico["algebraicResolution"].lower() == "direct":
                if self.parameterDico["Linear System Direct Method"] in ["Banded","Umfpack"] :
                    sifFileW("  Linear System Direct Method = %s\n"%self.parameterDico["Linear System Direct Method"])
                    pass
                else :
                    sifFileW("  Linear System Direct Method = %s\n"%"Banded")
                    sifFileW("  Linear System Max Iterations = %s\n"%self.parameterDico["Linear System Max Iterations"])
                    sifFileW("  Linear System Convergence Tolerance = %e\n"%self.parameterDico["Linear System Convergence Tolerance"])
                    pass
                    #raise Exception("Linear System Direct Method is not correct.\nChoose between Banded and Umfpack")
                sifFileW("  Optimize Bandwidth = %s\n"%self.parameterDico["Optimize Bandwidth"])
            elif self.parameterDico["algebraicResolution"].lower() == "iterative":
                sifFileW("  Linear System Iterative Method = %s\n"%self.parameterDico["Linear System Iterative Method"])
                sifFileW("  Linear System Max Iterations = %s\n"%self.parameterDico["Linear System Max Iterations"])
                sifFileW("  Linear System Convergence Tolerance = %e\n"%self.parameterDico["Linear System Convergence Tolerance"])
                sifFileW("  Linear System Preconditioning = %s\n"%self.parameterDico["Linear System Preconditioning"])
                #sifFileW("  Linear System ILUT Tolerance = %e\n"%self.parameterDico["Linear System Convergence Tolerance"])
                pass
            elif self.parameterDico["algebraicResolution"].lower() == "multigrid":
                raise Exception("Multigrid does not work for the moment.\nError:: LoadMesh: Unable to load mesh: ./mgrid2")
#                sifFileW("  Linear System Direct Method = %s\n"%self.parameterDico["Linear System Direct Method"])
            else :
                raise Exception("Algebraic resolution is not correct.\nChoose between Direct, Iterative and Multigrid")

            sifFileW("  Linear System Symmetric = %s\n"%self.parameterDico["Linear System Symmetric"])
            sifFileW("  Nonlinear System Max Iterations = %s\n"%self.parameterDico["Nonlinear System Max Iterations"])
            sifFileW("  Nonlinear System Convergence Tolerance = %s\n"\
            %self.parameterDico["Nonlinear System Convergence Tolerance"])
            sifFileW("  Nonlinear System Newton After Tolerance = %s\n"\
            %self.parameterDico["Nonlinear System Newton After Tolerance"])
            sifFileW("  Nonlinear System Newton After Iterations = %s\n"\
            %self.parameterDico["Nonlinear System Newton After Iterations"])
            sifFileW("  Nonlinear System Relaxation Factor = %s\n"\
            %self.parameterDico["Nonlinear System Relaxation Factor"])
            sifFileW("  Steady State Convergence Tolerance = %s\n"%self.parameterDico["Steady State Convergence Tolerance"])
            sifFileW("  Lumped Mass Matrix = %s\n"%self.parameterDico["Lumped Mass Matrix"])

#            sifFileW("  Stabilize ="+self.parameterDico['Stabilize']+"\n")
#            sifFileW("  Stabilize = True \n")
            #print "dbg stabil ",self.parameterDico['Stabilize']
            #print " self.darcyVelocity",self.darcyVelocity,self.parameterDico['Bubbles']
            if self.parameterDico["Bubbles"] and type(self.darcyVelocity) != None:
                                                                                            #
                                                                                            # bubbles is set to true
                                                                                            # to stabilize the solver
                                                                                            #
                sifFileW("  Bubbles = "+str(self.parameterDico['Bubbles'])+"\n")
                pass
            else:
                sifFileW("  Bubbles  = False\n")
                pass
            sifFileW("  Namespace = string \"%s\"\n"%self.speciesNamesList[ind])
            sifFileW("End\n\n")
            sifFile.flush()
            pass
                                                                                                        #
                                                                                                        # temperature treatment
                                                                                                        #
        if self.temperature:
            ind +=1
            sifFileW("Solver %i\n"%(ind+1))
            sifFileW("  Equation = Heat Equation TEMPERATURE\n")
            sifFileW("  Variable = -dofs 1 TEMPERATURE\n")
            #sifFileW("  Variable DOFs = 1\n\n")

#            sifFileW("  Procedure = \"AdvectionDiffusionTimeStep\" \"AdvectionDiffusionTimeStepSolver\"\n")
            sifFileW("  Procedure = \"HeatTimeStep\" \"HeatTimeStepSolver\"\n")

            sifFileW("  Linear System Solver = %s\n"%self.parameterDico["Linear System Solver"])
            if self.parameterDico["algebraicResolution"] == "Direct":
                if self.parameterDico["Linear System Direct Method"] in ["Banded","Umfpack"] :
                    sifFileW("  Linear System Direct Method = %s\n"%self.parameterDico["Linear System Direct Method"])
                    sifFileW("  Linear System Max Iterations = %s\n"%self.parameterDico["Linear System Max Iterations"])
                    sifFileW("  Linear System Convergence Tolerance = %e\n"%self.parameterDico["Linear System Convergence Tolerance"])
                    pass
                else :
                    raise Exception("Linear System Direct Method is not correct.\nChoose between Banded and Umfpack")
                sifFileW("  Optimize Bandwidth = %s\n"%self.parameterDico["Optimize Bandwidth"])
            else:
                if self.parameterDico["Linear System Iterative Method"] in ["CG","CGS","BICGStab","TFQMP","GMRES"] :
                    sifFileW("  Linear System Iterative Method = %s\n"%self.parameterDico["Linear System Iterative Method"])
                    pass

                sifFileW("  Linear System Max Iterations = %s\n"%self.parameterDico["Linear System Max Iterations"])
                sifFileW("  Linear System Convergence Tolerance = %e\n"%(self.parameterDico["Linear System Convergence Tolerance"]))
                sifFileW("  Linear System Preconditioning = %s\n"%self.parameterDico["Linear System Preconditioning"])
                sifFileW("  Linear System ILUT Tolerance = %e\n"%(self.parameterDico["Linear System ILUT Tolerance"]))
                sifFileW("  Linear System Symmetric = %s\n"%self.parameterDico["Linear System Symmetric"])
                pass
            #sifFileW("  Linear System Direct Method = %s\n"%self.parameterDico["Linear System Direct Method"])
            sifFileW("  Lumped Mass Matrix = %s\n"%self.parameterDico["Lumped Mass Matrix"])
            self.parameterDico['Stabilize'] = "True"
            sifFileW("  Stabilize ="+self.parameterDico['Stabilize']+"\n")
            #print "dbg stabil ",self.parameterDico['Stabilize']
            if self.parameterDico['Stabilize']=="True":
                sifFileW("  Bubbles = "+self.parameterDico['Bubbles']+"\n")
            else:
                sifFileW("!  Bubbles = False\n")
            sifFileW("  Namespace = string \"TEMPERATURE\"\n")
            sifFileW("End\n\n")
        #if self.temperature:
        #    self.parameterDico["oneDimensionalBoreHole"] = True
        #    if self.parameterDico["oneDimensionalBoreHole"] == True:
        #        ind+=1
        #        sifFileW("Solver %i\n"%(ind+1))
        #        sifFileW("  Equation = \"SaveMaterial\"\n")
        #        sifFileW("  Procedure = File \"SaveData\" \"SaveMaterials\"\n")
        #        sifFileW("  Parameter 1 = String \"earthTemperature\"\n")
        #        sifFileW("End\n\n")
            sifFile.flush()
            pass
                                                                                                        #
                                                                                                        # Darcy treatment
                                                                                                        #
        if "computed" in self.advConv.lower():
#
            ind +=1
            sifFileW("Solver %i\n"%(ind))
            sifFileW("  Exec Solver = \"%s\"\n"%("Always"))
            sifFileW("  Equation = \"%s\"\n"%("Darcy Equation"))

            sifFileW("  Procedure = \"SaturatedDarcyTimeStep\" \"SaturatedDarcyTimeStepSolver\"\n")
            sifFileW("  Variable = %s\n"%("Charge"))
            if (self.userPermeability): sifFileW("  UserPermeability = %s\n"%("True"))
            sifFileW("  Variable Dofs = %i\n"%(1))

            if self.chargeParameterDico["algebraicResolution"] != "Direct":
                self.chargeParameterDico['linearSystemSolver'] = "Iterative"
                pass
            else:
                sifFileW("  Linear System Direct Method = %s\n"%self.chargeParameterDico["linear System Iterative Method"])
                pass

            sifFileW("  Linear System Solver = \"%s\"\n"%self.chargeParameterDico['Linear System Solver'])
            sifFileW("  Linear System Iterative Method = \"%s\"\n"%self.chargeParameterDico["Linear System Iterative Method"])
            sifFileW("  Linear System Max Iterations = %s\n"%self.chargeParameterDico["Linear System Max Iterations"])
            sifFileW("  Linear System Convergence Tolerance = %e\n"%self.chargeParameterDico["Linear System Convergence Tolerance"])
            sifFileW("  Linear System Preconditioning = \"%s\"\n"%self.chargeParameterDico["Linear System Preconditioning"])
            sifFileW("  Steady State Convergence Tolerance = %s\n"%self.chargeParameterDico["Steady State Convergence Tolerance"])

            if self.chargeParameterDico['stabilize'] == True:
                sifFileW("  Stabilize = True\n")
                pass
            else:
                sifFileW("  Stabilize = True\n")
                pass

            sifFileW("  Namespace = string \"charge\"\n")
            sifFileW("End\n\n")
                                                                                            #
                                                                                            # charge has been treated,
                                                                                            # now we extract the velocity
                                                                                            #
            ind+=1
            sifFileW("Solver %i\n"%(ind))
            sifFileW("  Equation = ComputeFlux\n")
#            sifFileW("  Procedure = \"DFluxTimeStepSolver\" \"DFluxTimeStepSolver\"\n")
            sifFileW("  Procedure = \"DFluxSolver\" \"DFluxSolver\"\n")

            if (self.userPermeability): sifFileW("  UserPermeability = %s\n"%("True"))
            sifFileW("  Flux Variable = String \"Charge\"\n")
            sifFileW("  Flux Coefficient = String \"Hydr Conductivity\"\n")
            sifFileW("  Flux Coefficient = String \"Saturated Hydraulic Conductivity\"\n")
            sifFileW("  Linear System Convergence Tolerance = %e\n"%(self.chargeParameterDico["Flux Parameter"]))
            sifFileW("End\n\n")
            sifFile.flush()
            pass
        ind +=1
                                                                                            #
                                                                                            # Elasticity Solver
                                                                                            #
        if self.problemType == "thmc":
            ind+=1
            sifFileW("Solver %i\n"%(ind))
            sifFileW("  Equation = Linear Elasticity\n")

            sifFileW("  Procedure = \"LinearElasticityTimeStep\" \"LinearElasticityTimeStepSolver\"\n")
            sifFileW("  Variable = Displacement\n")
            sifFileW("  Variable DOFs = 2\n\n")
            sifFileW("  Exec Solver = Always\n")
            sifFileW("  Calculate Stresses = TRUE\n")
            #print "self.mechanicsParameterDico.keys(): ",self.mechanicsParameterDico.keys()
            #raw_input()
            sifFileW("  Steady State Convergence Tolerance =%e\n"\
                          %self.mechanicsParameterDico["Steady State Convergence Tolerance"])
            sifFileW("  Stabilize = True\n")
            sifFileW("  Bubbles = True\n")
            sifFileW("  Lumped Mass Matrix = False\n")
            sifFileW("  Optimize Bandwidth = False\n")
                                                                                            #
                                                                                            # non linear solver Non Linear System Max Iterations
                                                                                            #
            sifFileW("  !\n")
            sifFileW("  Nonlinear System Newton After Iterations = %s\n"%self.mechanicsParameterDico["Non Linear System Newton After Iterations"])
            sifFileW("  Nonlinear System Max Iterations = %s\n"%self.mechanicsParameterDico["Non Linear System Max Iterations"])
            sifFileW("  Nonlinear System Convergence Tolerance = %s\n"%self.mechanicsParameterDico["Non Linear System Convergence Tolerance"])
            sifFileW("  Nonlinear System Relaxation Factor = %s\n"%self.mechanicsParameterDico["Non Linear System Relaxation Factor"])
            sifFileW("  !")
            sifFileW("  Steady State Convergence Tolerance = %s\n"%self.mechanicsParameterDico["Steady State Convergence Tolerance"])

            sifFileW("  Linear System Solver = %s\n"%self.parameterDico["Linear System Solver"])
            if self.parameterDico["algebraicResolution"] == "Direct":
                if self.parameterDico["Linear System Direct Method"] in ["Banded","Umfpack"] :
                    sifFileW("  Linear System Direct Method = %s\n"%self.mechanicsParameterDico["Linear System Direct Method"])
                    sifFileW("  Linear System Max Iterations = %s\n"%self.mechanicsParameterDico["Linear System Max Iterations"])
                    sifFileW("  Linear System Convergence Tolerance = %e\n"%self.mechanicsParameterDico["Linear System Convergence Tolerance"])
                    pass
                else :
                    raise Exception("Linear System Direct Method is not correct.\nChoose between Banded and Umfpack")
                sifFileW("  Optimize Bandwidth = %s\n"%self.mechanicsParameterDico["Optimize Bandwidth"])
                pass
            else:
                                                                                            #
                                                                                            # linear solver
                                                                                            #
                if self.parameterDico["Linear System Iterative Method"].lower() in ["cg","cgs","bicgstab","tgqmp","gmres","gcr"] :
                    sifFileW("  Linear System Iterative Method = %s\n"%self.mechanicsParameterDico["Linear System Iterative Method"])
                    pass
                else:
                    sifFileW("  Linear System Iterative Method = BiCGStab\n")
                    pass
                sifFileW("  Linear System Max Iterations = %s\n"%self.mechanicsParameterDico["Linear System Max Iterations"])
                sifFileW("  Linear System Convergence Tolerance = %e\n"%(self.mechanicsParameterDico["Linear System Convergence Tolerance"]))
                sifFileW("  Linear System Preconditioning = %s\n"%self.mechanicsParameterDico["Linear System Preconditioning"])
                sifFileW("  Linear System ILUT Tolerance = %e\n"%(self.mechanicsParameterDico["Linear System ILUT Tolerance"]))
                sifFileW("  Linear System Symmetric = %s\n"%self.mechanicsParameterDico["Linear System Symmetric"])
                sifFileW("  Linear System Precondition Recompute = %i\n"%self.mechanicsParameterDico["Linear System Precondition Recompute"])
                sifFileW("  Linear System Abort Not Converged = False\n")
                sifFileW("  Linear System Residual Output = %s\n"%self.mechanicsParameterDico["Linear System Residual Output"])
                pass
            sifFileW("End\n\n")
            pass
                                                                                            #
                                                                                            # Compute Energy Release Rate
                                                                                            #
##            sifFileW("Solver %i\n"%(ind+1))
##            sifFileW("  Equation = \"Compute Energy Release Rate\" \n")
##            sifFileW("  Procedure = \"EnergyRelease\" \"ReleaseRateSolver\"\n")
##            sifFileW("End\n\n")
##            ind+=1
                                                                                            #
                                                                                            #
            sifFileW("Solver %i\n"%(ind+1))
            sifFileW("  Exec Solver = String \"after timestep\" \n")
            sifFileW("  Equation = String \"ResultOutput\" \n")
            sifFileW("  Procedure = File \"ResultOutputSolve\" \"ResultOutputSolver\"\n")
            sifFileW("  Output File Name = String  \"%s\" \n"%self.outputName)
            sifFileW("  Output Format = String  \"vtu\" \n")
            sifFileW("End\n\n")
            sifFile.flush()
            pass
                                                                                            #
                                                                                            # the two phase wellbore Solver
                                                                                            #

        if self.parameterDico["vapor"]:
            ind+=1
            wPDico = self.wellboreParameterDico
            #
            # we write the mass energy solver for the well
            #
            sifFileW("Solver %i\n"%(ind))
            sifFileW("  Equation = \"Mass-Energy\"\n")
            sifFileW("  Variable = POT[WMassFlow:1 WEnthalpy:1]\n")
            sifFileW("  Procedure = \"MassEnergySolveWell\" \"MassEnergySolver\"\n")
            sifFileW("  !\n")
            sifFileW("  Element = \"p:1\"\n")
            sifFileW("  !\n")
            sifFileW("  Nonlinear System Newton After Iterations = %s\n"%wPDico["Nonlinear System Newton After Iterations"])
            sifFileW("  Nonlinear System Max Iterations = %s\n"         %wPDico["Nonlinear System Max Iterations"])
            sifFileW("  Nonlinear System Convergence Tolerance = %s\n"  %wPDico["Nonlinear System Convergence Tolerance"])
            sifFileW("  Nonlinear System Relaxation Factor = %s\n"      %wPDico["Nonlinear System Relaxation Factor"])
            sifFileW("  !\n")
            if wPDico["algebraicResolution"] == "Direct":
                if wPDico["Linear System Direct Method"] in ["Banded","Umfpack"] :
                    sifFileW("  Linear System Direct Method = %s\n"        %wPDico["Linear System Direct Method"])
                    sifFileW("  Linear System Max Iterations = %s\n"       %wPDico["Linear System Max Iterations"])
                    sifFileW("  Linear System Convergence Tolerance = %e\n"%wPDico["Linear System Convergence Tolerance"])
                    pass
                else :
                    raise Exception("Linear System Direct Method is not correct.\nChoose between Banded and Umfpack")
                sifFileW("  Optimize Bandwidth = %s\n"%wPDico["Optimize Bandwidth"])
                pass
            else:
                                                                                            #
                                                                                            # linear solver
                                                                                            #
                if wPDico["Linear System Iterative Method"].lower() in ["cg","cgs","bicgstab","tgqmp","gmres","gcr"] :
                    sifFileW("  Linear System Iterative Method = %s\n"%wPDico["Linear System Iterative Method"])
                    pass
                else:
                    sifFileW("  Linear System Iterative Method = BiCGStab\n")
                    pass
                sifFileW("  Linear System Max Iterations = %s\n"        %wPDico["Linear System Max Iterations"])
                sifFileW("  Linear System Convergence Tolerance = %e\n" %wPDico["Linear System Convergence Tolerance"])
                sifFileW("  Linear System Preconditioning = %s\n"       %wPDico["Linear System Preconditioning"])
                sifFileW("  Linear System ILUT Tolerance = %e\n"        %wPDico["Linear System ILUT Tolerance"])
                sifFileW("  Linear System Symmetric = %s\n"             %wPDico["Linear System Symmetric"])
                sifFileW("  Linear System Precondition Recompute = %i\n"%wPDico["Linear System Precondition Recompute"])
                sifFileW("  Linear System Abort Not Converged = False\n")
                sifFileW("  Linear System Residual Output = %s\n"       %wPDico["Linear System Residual Output"])
                pass
            sifFileW("  !\n")
            sifFileW("  Steady State Convergence Tolerance = 1e-6\n")
            sifFileW("  Exported Variable 1 = String \"Heat Source\"\n")
            #sifFileW("  Exported Variable 2  = String \"Time1\"\n")
            #sifFileW("  Exported Variable 3  = String \"Time0\"\n")
            #sifFileW("  Exported Variable 4  = String \"Temperature1\"\n")
            #sifFileW("  Exported Variable 5  = String \"Temperature0\"\n")
            #sifFileW("  Exported Variable 6  = String \"Pressure1\"\n")
            #sifFileW("  Exported Variable 7  = String \"Pressure0\"\n")
            sifFileW("  Exported Variable 2 = String \"MG\"\n")
            sifFileW("  Exported Variable 3 = String \"Twell\"\n")
            #sifFileW("  Exported Variable 4 = String \"HTC\"\n")
            sifFileW("  Exported Variable 4 = String \"Quality\"\n")
            sifFileW("  Exported Variable 5 = String \"VoidFraction\"\n")
            sifFileW("  !\n")
            sifFileW("  Update Exported Variables = Logical True\n")
            sifFileW("  Nonlinear Update Exported Variables = Logical True\n")
            sifFileW("  Calculate Flow = Logical True\n")
            
            sifFileW("End\n\n")
            ind+=1
            #
            # we integrate to get the pressure field along the well
            #
            sifFileW("Solver %i\n"%(ind))
            sifFileW("  Equation = Incompressible Momentum Equation\n")
            sifFileW("  Procedure = \"WellMomentum\" \"WellMomentumSolver\"\n")
            sifFileW("  Variable = \"Pressure\"\n")
            sifFileW("  Variable DOFs = 1\n")
            sifFileW("  Linear System Solver = Iterative\n")            #sifFileW("  Linear System Iterative Method = UMFPACK\n")
            sifFileW("  Linear System Iterative Method = BiCGStab\n")
            sifFileW("  Linear System Max Iterations = %s\n"       %wPDico["Linear System Max Iterations"])
            sifFileW("  Linear System Convergence Tolerance = %e\n"%wPDico["Linear System Convergence Tolerance"])
            sifFileW("  Linear System Preconditioning = ILU0\n")
            sifFileW("  Linear System ILUT Tolerance = 1.0e-3\n")
            sifFileW("  Linear System Abort Not Converged = False\n")
            sifFileW("  Linear System Residual Output = 1\n")
            sifFileW("  Linear System Precondition Recompute = 1\n")

            #sifFileW("  Linear System Convergence Tolerance = %e\n"%wPDico["Linear System Convergence Tolerance"])
            sifFileW("Exported Variable 1 = String \"Pressure Diffusion Source\"\n")
            sifFileW("Update Exported Variables = Logical True\n")
            sifFileW("Nonlinear Update Exported Variables = Logical True\n")
            sifFileW("End\n\n")
            
            pass
        return None

    def writeMechanicalSolver(self):
        """
        The mechanical solver section enables the treatment of the stress solver and the
        definition of the way the resulting algebraic system will be solved.
        """
        sifFile = self.sifFile
        sifFileW = sifFile.write
        sifFileW("! ~~\n! Solver p27 ref. Manual\n! ~~\n")
        ind = 0
                                                                                            #
                                                                                            # Elasticity treatment
                                                                                            #
        sifFileW("Solver %i\n"%(ind+1))
        sifFileW("  Equation = Linear Elasticity \n")
        sifFileW("  Variable = -dofs %s Displacement\n\n"%self.mesh.getDimensionString()[0])
        #sifFileW("  Variable = Displacement\n")
        #sifFileW("  Variable DOFs = 2\n\n")

        sifFileW("  Procedure = \"StressSolve\" \"StressSolver\"\n")
        #sifFileW("  Exec Solver = Always\n")
        sifFileW("  Calculate Stresses = TRUE\n")
                                                                                            #
                                                                                            # Algebraic solver
                                                                                            #
        sifFileW("  Steady State Convergence Tolerance =%e\n"%(self.mechanicsParameterDico["Steady State Convergence Tolerance"]))
        #

        if "Stabilize" in self.mechanicsParameterDico.keys():
            sifFileW("  Stabilize = %s\n"%(self.mechanicsParameterDico["Stabilize"]))
            pass
        else:
            sifFileW("  Stabilize = True\n")
            pass
        if "Bubbles" in self.mechanicsParameterDico.keys():
            sifFileW("  Bubbles = %s\n"%(self.mechanicsParameterDico["Bubbles"]))
            pass
        else:
            sifFileW("  Bubbles = False\n")
            pass
        if "Lumped Mass Matrix" in self.mechanicsParameterDico.keys():
            sifFileW("  Lumped Mass Matrix = %s\n"%(self.mechanicsParameterDico["Lumped Mass Matrix"]))
        else:
            sifFileW("  Lumped Mass Matrix = False\n")

        if "Optimize Bandwidth" in self.mechanicsParameterDico.keys():
            sifFileW("  Optimize Bandwidth = %s\n"%(self.mechanicsParameterDico["Optimize Bandwidth"]))
            pass
        else:
            sifFileW("  Optimize Bandwidth = False\n")
            pass
                                                                                            #
                                                                                            # non linear solver
                                                                                            #
        sifFileW("  !")
        if "Elasticity_Nlinear_Newton_After_Tol" in self.mechanicsParameterDico.keys():
            sifFileW("  Nonlinear System Newton After Tolerance  = %s\n"
                          %self.mechanicsParameterDico["Elasticity_Nlinear_Newton_After_Tol"])
        else:
            sifFileW("  Nonlinear System Newton After Tolerance  = %s\n"%1.0e-4)
            pass
        if "Non Linear System Newton After Iterations" in self.mechanicsParameterDico.keys():
            sifFileW("  Nonlinear System Newton After Iterations = %s\n"
                          %self.mechanicsParameterDico["Non Linear System Newton After Iterations"])
            pass
        else:
            sifFileW("  Nonlinear System Newton After Iterations  = %s\n"%3)
            pass
        #
        if "Elasticity_Nlinear_Newton_After_Iter" in self.mechanicsParameterDico.keys():
            sifFileW("  Nonlinear System Max Iterations = %s\n"
                          %self.mechanicsParameterDico["Elasticity_Nlinear_Newton_Max_Iter"])
            pass
        else:
            sifFileW("  Nonlinear System Max Iterations = %s\n"%10)
            pass
        if "Elasticity_Nlinear_Convergence_Tol" in self.mechanicsParameterDico.keys():
            sifFileW("  Nonlinear System Convergence Tolerance = %s\n"
                     %self.mechanicsParameterDico["Elasticity_Nlinear_Convergence_Tol"])
            pass
        else:
            sifFileW("  Nonlinear System Convergence Tolerance = %s\n"%1.0e-9)
            pass
        if "Elasticity_Nlinear_Convergence_Tol" in self.mechanicsParameterDico.keys():
            sifFileW("  Nonlinear System Relaxation Factor = %s\n"
                     %self.mechanicsParameterDico["Nonlinear_System_Relaxation_Factor"])
            pass
        else:
            sifFileW("  Nonlinear System Relaxation Factor = %s\n"%0.5)
            pass
        sifFileW("  !")
        sifFileW("  Steady State Convergence Tolerance = %s\n"%self.mechanicsParameterDico["Steady State Convergence Tolerance"])
                                                                                            #
                                                                                            # linear algebraicsolver
                                                                                            #
        if self.mechanicsParameterDico["algebraicResolution"] == "Direct":
            sifFileW("  Linear System Solver = Direct\n")
            if self.mechanicsParameterDico["Linear System Direct Method"] in ["Banded","Umfpack"] :
                sifFileW("  Linear System Direct Method = %s\n"%self.mechanicsParameterDico["Linear System Direct Method"])
                pass
            else :
                print("Linear System Direct Method is not correct has been set to Umfpack")
                sifFileW("  Linear System Direct Method = %s\n"%"Umfpack")
                pass
            sifFileW("  Optimize Bandwidth = %s\n"%self.mechanicsParameterDico["Optimize Bandwidth"])
        elif self.mechanicsParameterDico["algebraicResolution"] == "Iterative":
            sifFileW("  Linear System Solver = Iterative\n")
            sifFileW("  Linear System Iterative Method = %s\n"%self.mechanicsParameterDico["Linear System Iterative Method"])
            sifFileW("  Linear System Max Iterations = %s\n"%self.mechanicsParameterDico["Linear System Max Iterations"])
            sifFileW("  Linear System Convergence Tolerance = %e\n"
                          %self.mechanicsParameterDico["Linear System Convergence Tolerance"])
            sifFileW("  Linear System Preconditioning = %s\n"%self.mechanicsParameterDico["Linear System Preconditioning"])
            sifFileW("  Linear System Abort Not Converged = False\n")
            sifFileW("  Linear System Precondition Recompute = %s\n"%1)
            sifFileW("  Linear System Residual Output = %s\n"%(str(self.mechanicsParameterDico["Linear System Residual Output"])))
            if "Linear System ILUT Tolerance" in self.mechanicsParameterDico.keys():
                sifFileW("Linear System ILUT Tolerance = %s\n"
                         %self.mechanicsParameterDico["Linear System ILUT Tolerance"])
                pass
            else:
                sifFileW("  Linear System ILUT Tolerance = %e\n"%1.e-3)
                pass

        elif self.mechanicsParameterDico["algebraicResolution"] == "Multigrid":
            raise Exception("Multigrid does not work for the moment.\nError:: LoadMesh: Unable to load mesh: ./mgrid2")
        else :
            raise Exception("Algebraic resolution is not correct.\nChoose between Direct, Iterative and Multigrid")

        #sifFileW("  Calculate Loads = Logical = True\n")
        sifFileW("End\n\n")
        ind+=1
                                                                                            #
                                                                                            # Compute Energy Release Rate
                                                                                            #
        sifFileW("Solver %i\n"%(ind+1))
        sifFileW("  Equation = \"Compute Energy Release Rate\" \n")
        sifFileW("  Procedure = \"EnergyRelease\" \"ReleaseRateSolver\"\n")
        sifFileW("End\n\n")
        ind+=1
                                                                                            #
                                                                                            #
        sifFileW("Solver %i\n"%(ind+1))
        sifFileW("  Exec Solver = String \"after timestep\" \n")
        sifFileW("  Equation = String \"ResultOutput\" \n")
        sifFileW("  Procedure = File \"ResultOutputSolve\" \"ResultOutputSolver\"\n")
        sifFileW("  Output File Name = String  \"%s\" \n"%self.outputName)
        sifFileW("  Output Format = String  \"vtu\" \n")
        sifFileW("End\n\n")
        ind+=1
                                                                                            #
        if self.temperature:
            sifFileW("Solver %i\n"%(ind+1))
            sifFileW("  Equation = Heat Equation TEMPERATURE\n")

            sifFileW("  Variable = TEMPERATURE\n")
            sifFileW("  Variable DOFs = 1\n\n")

#            sifFileW("  Procedure = \"AdvectionDiffusionTimeStep\" \"AdvectionDiffusionTimeStepSolver\"\n")
            sifFileW("  Procedure = \"HeatTimeStep\" \"HeatTimeStepSolver\"\n")
            sifFileW("  Linear System Solver = %s\n"%self.mechanicsParameterDico["Linear System Solver"])
            if self.mechanicsParameterDico["algebraicResolution"] == "Direct":
                if self.mechanicsParameterDico["Linear System Direct Method"] in ["Banded","Umfpack"] :
                    sifFileW("  Linear System Direct Method = %s\n"%self.mechanicsParameterDico["Linear System Direct Method"])
                    pass
                else :
                    raise Exception("Linear System Direct Method is not correct.\nChoose between Banded and Umfpack")
                sifFileW("  Optimize Bandwidth = %s\n"%self.mechanicsParameterDico["Optimize Bandwidth"])
            else:
                if self.mechanicsParameterDico["Linear System Iterative Method"] in ["CG","CGS","BICGStab","TFQMP","GMRES"] :
                    sifFileW("  Linear System Iterative Method = %s\n"%self.mechanicsParameterDico["Linear System Iterative Method"])
                    pass
                sifFileW("  Linear System Max Iterations = %s\n"%self.mechanicsParameterDico["Linear System Max Iterations"])
                sifFileW("  Linear System Convergence Tolerance = %e\n"%(self.mechanicsParameterDico["Linear System Convergence Tolerance"]*0.01))
                sifFileW("  Linear System Preconditioning = %s\n"%self.mechanicsParameterDico["Linear System Preconditioning"])
                sifFileW("  Linear System ILUT Tolerance = %e\n"%(self.mechanicsParameterDico["Linear System ILUT Tolerance"]))
                sifFileW("  Linear System Symmetric = %s\n"%self.mechanicsParameterDico["Linear System Symmetric"])
                pass
            #sifFileW("  Linear System Direct Method = %s\n"%self.mechanicsParameterDico["Linear System Direct Method"])
            sifFileW("  Lumped Mass Matrix = %s\n"%self.mechanicsParameterDico["Lumped Mass Matrix"])
            self.mechanicsParameterDico['Stabilize'] = "True"
            sifFileW("  Stabilize ="+self.mechanicsParameterDico['Stabilize']+"\n")
            #print "dbg stabil ",self.mechanicsParameterDico['Stabilize']
            if self.mechanicsParameterDico['Stabilize']=="True":
                sifFileW("  Bubbles = "+self.mechanicsParameterDico['Bubbles']+"\n")
                pass
            else:
                sifFileW("!  Bubbles = False\n")
                pass
            sifFileW("  Namespace = string \"TEMPERATURE\"\n")

            sifFileW("End\n\n")

        return None

    def writeBoundaryCondition(self,problemType = None):
        """
        In advection-diffusion equation we may set the concentration directly by Dirichlet boundary conditions
        or use mass flux condition. The natural boundary condition is zero flux condition.

        Elmer enables the treatment of elasticity (small deformations). In that frame, we have two kind of boundary conditions:

                a displacement or a normal force.
                The displacement is expressed other the three directionx x, y and z.

                displacement 1 = Real
                displacement 2
                displacement 3

                Normal Force = Real -10.

        """
        #print problemType
        #raw_input("writeBoundaryCondition problemType")
        if self.parameterDico["oneDimensionalBoreHole"]:
            from wellBoreReader import *
            fineName = os.environ["PWD"]+"/Data/wellbore.dat"
            wellboreDataDict = wellBoreDataRead(fineName)

        sifFile = self.sifFile
        sifFileW = sifFile.write
        sifFileW("! ~~\n! Boundary p30 ref. Manual\n! ~~\n");sifFile.flush()
                                                                                            #
                                                                                            # Two kinds of boundary cond.:
                                                                                            #    Dirichlet or Flux
                                                                                            #
        if problemType in ["elasticity", "mechanical", "mechanicalproblem"]:
            print("1037 self.dirBCList1: ",self.dirBCList1[0][0])
            for dirBC in self.dirBCList1[0].keys():
                print("index: ",self.dirBCList1[0][dirBC]["index"])
                print("name: ", self.dirBCList1[0][dirBC]["name"])
                sifFileW("Boundary Condition %i ! %s\n"%(self.dirBCList1[0][dirBC]["index"], self.dirBCList1[0][dirBC]["name"]))
                sifFileW("  Target Boundaries (1) = %s\n"%str(self.dirBCList1[0][dirBC]["index"]))
                if self.dirBCList1[0][dirBC]["description"] != None:
                    sifFileW("! ~~\n! %s\n! ~~\n"%dirBC[0].description)
                    pass
                if self.dirBCList1[0][dirBC]["Normalforce"] != None:
                    sifFileW(" Normal Force = Real %e\n"%(self.dirBCList1[0][dirBC]["Normalforce"]))
                    pass
                if self.dirBCList1[0][dirBC]["Displacement"] != None:
                    print(" displacement ", self.dirBCList1[0][dirBC]["Displacement"])
                    ind = 1
                    for component in  self.dirBCList1[0][dirBC]["Displacement"]:
                        sifFileW(" Displacement %i = Real %e\n"%(ind,component))
                        ind+=1
                        pass
                    pass
                sifFileW("End\n\n");sifFile.flush()
                pass
            return None
        elif problemType in ["chemicaltransport","thmc","chemicaltransportproblem","thmcproblem"]:
            #print self.dirBCList1
            #printm("reaching that level",1)
            for dirBC in self.dirBCList1:
                #print("----------------")
                #print(dirBC)
                #print(" borehole",self.parameterDico["oneDimensionalBoreHole"])
                #raw_input(" elmer dbg dirBC")
                inds = 0
                                                                                            #
                                                                                            # Dirichlet
                                                                                            #
                if (dirBC["type"].lower() == "dirichlet"):
                    #if isinstance(dirBC ,ToughDirichletCondition): pass
                    stinds = _digit(inds)
                    stindb = str(dirBC["index"])+stinds
                    print("index: ",dirBC["index"])
                    print("name: ", dirBC["name"])
                    #printm(" boundary condition looking for the transient term",1)
                    sifFileW("Boundary Condition %i ! %s\n"%(dirBC["index"], dirBC["name"]))
                    sifFileW("  Target Boundaries (1) = %s\n"%str(dirBC["index"]))
                    if dirBC.has_key("description"):
                        if dirBC["description"] != None:
                            sifFileW("! ~~\n! %s\n! ~~\n"%dirBC["description"])
                            pass
                        pass
                    if dirBC.has_key("normalforce"):
                        #if dirBC["normalforce"] != None:
                        sifFileW(" Normal Force = Real %e\n"%(dirBC["normalforce"].value))
                        pass
                    if dirBC.has_key("Displacement"):
                        if dirBC["Displacement"] != None:
                            print(" displacement ", dirBC["Displacement"])
                            ind = 1
                            for component in  dirBC["Displacement"]:
                                sifFileW(" Displacement %i = Real %e\n"%(ind,component))
                                ind+=1
                                pass
                            pass
                        pass
                    conc = dirBC["conc"]
                                                                                            #
                                                                                            # Dirichlet boundary conditions on species
                    if dirBC.has_key("timeVariation"):
                        if (dirBC["timeVariation"] not in (None,[])):
                            print(" timeVariation",dirBC["timeVariation"])
                            for concName in self.speciesNamesList:
                                sifFileW("  %s = Variable time\n"%(concName))
                                sifFileW("    Real\n")
                                stinds = _digit(inds+1)
                                stindb = str(dirBC["name"])+stinds
                                sifFileW("    %e    %e\n"%(0.0, dirBC["conc"][inds]))
                                for time in dirBC["timeVariation"]:
                                    sifFileW("    %e    %e\n"%(time[0], time[1][inds]))
                                    pass
                                inds+=1
                                sifFileW("    End\n");sifFile.flush()
                                pass
                            pass
                        else:
                            #print dirBC["conc"]
                            #printm("dbg writing the bc with time variation",1)
                            for concName in self.speciesNamesList:
                                stinds = _digit(inds+1)
                                stindb = str(dirBC["name"])+stinds
                                sifFileW("  %s = Real %e\n"%(concName,dirBC["conc"][inds]))
                                inds+=1
                                pass
                            pass
                        pass
                    else:
                        for concName in self.speciesNamesList:
                            stinds = _digit(inds+1)
                            stindb = str(dirBC["name"])+stinds
                            sifFileW("  %s = Real %e\n"%(concName,dirBC["conc"][inds]))
                            inds+=1
                            pass
                        pass
                                                                                            #
                                                                                            # we take the first element of the list.
                                                                                            # We keep a list because we can have a varying temp. B.
                                                                                            #
                    if (self.temperature) or (self.parameterDico["oneDimensionalBoreHole"]):

                        if (dirBC["timeVariation"] not in (None,[])):                   # temperature is varying with time
                            if dirBC["TemperatureVariationList"] not in (None,[]):
                                sifFileW("  %s = Variable time\n"%("Temperature"))
                                sifFileW("    Real\n")
                                for time in dirBC["TemperatureVariationList"]:
                                    sifFileW("      %e      %e\n"%(time[0], time[1]))
                                    pass
                                #    print time[0], time[1]
                                sifFileW("    End\n")
                                pass
                            else:
                                sifFileW("! temperature\n")
                                sifFileW("  %s = Real %e\n"%("temperature", dirBC["temperature"][0]))
                                pass
                            pass
                        elif dirBC.has_key("temperature"):                                   # temperature is set to constant over time
                            #sifFileW("! temperature\n")
                            #sifFileW("  %s = Real %e\n"%("temperature", dirBC["temperature"][0]))
                            #pass
                            sifFileW("! temperature\n")
                            sifFileW("  %s = Real %e\n"%("temperature", dirBC["temperature"][0]))
                            pass
                            
                                                                                            #
                                                                                            # the study of a well is supposed
                                                                                            # to be linked to an evaluation
                                                                                            # of temperature but a well simulation
                                                                                            # can be made as standalone
                                                                                            #
                        if dirBC.has_key("enthalpyBoundaryCondition"):
                            sifFileW("! Enthalpy\n")
                            if (type(dirBC["enthalpyBoundaryCondition"]) in [FloatType, IntType]):
                              if self.parameterDico["oneDimensionalBoreHole"]:
                                sifFileW("  %s = Real %e\n"%("WEnthalpy", dirBC["enthalpyBoundaryCondition"]))
                              else:
                                sifFileW("  %s = Real %e\n"%("Enthalpy", dirBC["enthalpyBoundaryCondition"]))
                                pass
                            else:
                                raise Exception("%s should be a float"%("enthalpyBoundaryCondition"))
                            pass
                        if dirBC.has_key("wellMassFlowBoundaryCondition"):
                            sifFileW("! mass flow\n")
                            if (type(dirBC["wellMassFlowBoundaryCondition"]) in [FloatType, IntType]):
                                sifFileW("  %s = Real %e\n"%("WMassFlow", dirBC["wellMassFlowBoundaryCondition"]))
                                pass
                            else:
                                raise Exception("%s should be a float"%("enthalpyBoundaryCondition"))
                            pass
                        if dirBC.has_key("wellPressureBoundaryCondition"):
                            sifFileW("! pressure\n")
                            if (type(dirBC["wellPressureBoundaryCondition"]) in [FloatType, IntType]):
                                sifFileW("  %s = Real %e\n"%("Pressure", dirBC["wellPressureBoundaryCondition"]))
                                pass
                            else:
                                raise Exception("%s should be a float"%("enthalpyBoundaryCondition"))
                            pass
                        pass
                    if "computed" in str(self.advConv.lower()):
                        sifFileW("! charge\n")
                        sifFileW("  %s = Real %e\n"%("Charge", dirBC["head"]))
                        for body in self.bodies:
                            print(body.support.getName(),dirBC["bodyName"])
                            if body.support.getName() == dirBC["bodyName"]:
                                print(body.getMaterial().getHydraulicConductivity().getValue().value)
                                hydrCond = body.getMaterial().getHydraulicConductivity().getValue().value
                                break
                        sifFileW("  %s = Real %e\n"%("Hydraulic Conductivity", hydrCond))
                    sifFileW("End\n\n");sifFile.flush()
                elif (dirBC["type"].lower() == "flux"):
                                                                                            #
                                                                                            # Flux B. C.
                                                                                            #
                    stinds = _digit(inds+1)
                    stindb = str(dirBC["index"])+stinds
                    sifFileW("Boundary Condition %s\n"%dirBC["index"])
                    sifFileW("  Target Boundaries (1) = %s\n"%str(dirBC["index"]))
                    for spconc in dirBC["conc"]:
                        #stinds = _digit(inds+1)
                        #stindb = str(dirBC[1])+stinds
                        #sifFileW("Boundary Condition %s\n"%stindb)
                        #sifFileW("  Target Boundaries (1) = %s\n"%str(dirBC[1]))

#                        if (inds == 3):
#                            dirBC[3] = 2.e-3
#                             pass
#                        sifFileW("  Mass Transfer Coefficient = Real %e\n"%(dirBC[3]))

#                        sifFileW("  Mass Transfer Coefficient %s = Real %e\n"%(self.speciesNamesList[inds],dirBC[3]+inds))
#                        sifFileW("  External Concentration %s = Real %e\n"%(self.speciesNamesList[inds],spconc))
#                        sifFileW("  %s: External Concentration = Real %e\n"%(self.speciesNamesList[inds],spconc))
                        if (inds == 3 ):
                            sifFileW("  %s Mass Transfer Coefficient = Real %e\n"%(self.speciesNamesList[inds],dirBC["massTC"]))
                            sifFileW("  %s External Concentration = Real %e\n"%(self.speciesNamesList[inds],abs(spconc)))
                            #sifFileW("  Mass Transfer Coefficient = Real %e\n"%(dirBC[3]))
                            #sifFileW("  External Concentration = Real %e \n"%(abs(spconc)))
                        else:
                            sifFileW("  %s Mass Transfer Coefficient = Real %e\n"%(self.speciesNamesList[inds],dirBC["massTC"]))
                            sifFileW("  %s External Concentration = Real %e\n"%(self.speciesNamesList[inds],abs(spconc)))
                            #sifFileW("  Mass Transfer Coefficient = Real %e\n"%(dirBC[3]))
                            #sifFileW("  External Concentration = Real %e \n"%(0.))
                            pass
                        inds+=1
                    sifFileW("End\n\n");sifFile.flush()
                elif (dirBC["type"].lower() == "neumann"):
                                                                                            #
                                                                                            # Neumann boundary condition.
                                                                                            # For the moment,
                                                                                            # only a no flux boundary
                                                                                            # condition is treated
                                                                                            #
                    stinds = _digit(inds)
                    print("pydbg elmer ",dirBC)
                    #stindb = str(dirBC[1])+stinds
                    stindb = str(dirBC["index"])+stinds
                    sifFileW("Boundary Condition %s\n"%dirBC["index"])
                    sifFileW("  Target Boundaries (1) = %s\n"%str(dirBC["index"]))
                    print(" no flux neumann")
                    for spconc in dirBC["conc"]:
                        stinds = _digit(inds+1)
                        stindb = str(dirBC["name"])+stinds
                        sifFileW("  %s Flux = Real %e\n"%(self.speciesNamesList[inds],0.0))
                        inds+=1

                    sifFileW("End\n\n");sifFile.flush()
        return None

    def writeInitialCondition(self):
        """
        The initial condition section may be used to set initial values for:

            - the concentrations Ci
            - for displacment if elasticity is solved
            - for temperature if temperature is solved
        """
        sifFile = self.sifFile
        sifFileW = sifFile.write
        inds = 0
        sifFileW("! ~~\n! initial condition p8 ref. ElmersolverManual\n! ~~\n")

                                                                                            #
                                                                                            # elasticity
                                                                                            #
        if self.problemType in ["mechanical","elasticity"]:
            print(self.dirICList)
            sifFileW("! elasticity\n")
            for dirIC in self.dirICList:
                sifFileW("Initial Condition %s\n"%(dirIC[0]["index"]))
                displacement = dirIC[0]["Displacement"]
                print("displacement ",displacement)
                for ind in range(len(displacement.value)):
                    sifFileW("  Displacement %i = Real %e\n"%(ind+1, displacement.value[ind]))
                pass
                sifFileW("End\n")
            return None

        elif  self.problemType in ["chemicaltransport","thmc"]:
            for dirIC in self.dirICList:
                #print "diric",dirIC
                inds+=1
                #for indb in range(len(self.bodies)):
                #for inds in range(len(self.speciesNamesList)):
                sifFileW("Initial Condition %s\n"%(dirIC["index"]))

                if self.problemType == "thmc":
                    print(dirIC)
                    if dirIC.has_key("displacement"):
                        for ind in range(len(dirIC["displacement"].value)):
                            sifFileW("  Displacement %i = Real %e\n"\
                                    %(ind+1,dirIC["displacement"].value[ind]))
                            pass
                        pass
                    pass
                ind = 0

                for spconc in self.speciesNamesList:
                    sifFileW("  %2s = Real %e\n"%(self.speciesNamesList[ind], dirIC["conc"][ind]))
                    ind+=1
                    pass
                                                                                            #
                                                                                            # Temperature
                                                                                            #
                if (self.temperature==True) or (self.parameterDico["oneDimensionalBoreHole"]==True):
                    sifFileW("! temperature\n")
                    #print(dirIC)
                    #raw_input("temperatureInitialCondition debug\n")
                    if "temperatureInitialCondition" in dirIC.keys():
                        sifFileW("  Temperature = Variable Coordinate\n")
                        sifFileW("    Real MATC \"(%s)\"\n"%(_matcString(dirIC["temperatureInitialCondition"])))
                        #sifFileW("  Text = Variable Coordinate\n")
                        #sifFileW("    Real MATC \"(%s)\"\n"%(_matcString(dirIC["temperatureInitialCondition"])))
                        pass
                    elif type(dirIC["temperature"]) == FloatType:
                        sifFileW("  %s = Real %e\n"%("TEMPERATURE", dirIC["temperature"]))
                        pass
                    #elif type(dirIC["temperature"]) == FloatType:
                    #    sifFileW("  %s = Real %e\n"%("TEMPERATURE", dirIC["temperature"]))
                    pass
                                                                                            #
                                                                                            # wellbore tratment
                                                                                            #
                    if "enthalpyInitialCondition" in dirIC.keys():
                        if type(dirIC["enthalpyInitialCondition"]) in [FloatType,IntType]:
                            if self.parameterDico["oneDimensionalBoreHole"]:
                                sifFileW("  %s = Real %e\n"%("WEnthalpy", dirIC["enthalpyInitialCondition"]))
                                pass
                            else:
                                sifFileW("  %s = Real %e\n"%("Enthalpy", dirIC["enthalpyInitialCondition"]))
                                pass
                            pass
                        else:
                            if self.parameterDico["oneDimensionalBoreHole"]:
                                sifFileW("  WEnthalpy = Variable Coordinate\n")
                                sifFileW("    Real MATC \"(%s)\"\n"%(_matcString(dirIC["enthalpyInitialCondition"])))
                                pass
                            else:
                                sifFileW("  Enthalpy = Variable Coordinate\n")
                                sifFileW("    Real MATC \"(%s)\"\n"%(_matcString(dirIC["enthalpyInitialCondition"])))
                                pass
                            pass
                    if "wellMassFlowInitialCondition" in dirIC.keys():
                        if type(dirIC["wellMassFlowInitialCondition"]) in [FloatType,IntType]:
                            sifFileW("  %s = Real %e\n"%("WMassFlow", dirIC["wellMassFlowInitialCondition"]))
                            pass
                        else:
                            sifFileW("  WMassFlow = Variable Coordinate\n")
                            sifFileW("    Real MATC \"(%s)\"\n"%(_matcString(dirIC["wellMassFlowInitialCondition"])))
                            pass
                        pass
                    if "wellPressureInitialCondition" in dirIC.keys():
                        if type(dirIC["wellPressureInitialCondition"]) in [FloatType,IntType]:
                            sifFileW("  %s = Real %e\n"%("Pressure", dirIC["wellPressureInitialCondition"]))
                            pass
                        else:
                            sifFileW("  Pressure = Variable Coordinate\n")
                            sifFileW("    Real MATC \"(%s)\"\n"%(_matcString(dirIC["wellPressureInitialCondition"])))
                            pass
                        pass
                                                                                            #
                                                                                            # Charge
                                                                                            #
                if ("computed" in self.advConv.lower()):
                     sifFileW("! charge\n")
                #print dirIC
                     sifFileW("  %s = Real %e\n"%("Charge", dirIC["head"]))
                     pass
                sifFileW("End\n")

        return None

    def writeSimulation(self):
        """
        The simulation section gives the case control data:
        Simulation Type: Transient
        BDF Order: Value may range from 1 to 5
        """
        sifFile = self.sifFile
        sifFileW = sifFile.write
        sifFileW("Simulation\n")
        #
        #
        #       2D meshes: a cartesian or a delaunay mesh is identical in its identification
        #
        sifFileW("  Coordinate System = Cartesian "+self.mesh.getDimensionString()+"\n\n")
        sifFileW("  Simulation Type = "+self.getSimulationType()+"\n")
#        sifFileW("  Steady State Max Iterations ="+self.getSteadyStateMaxIter()+"\n\n")
        sifFileW("  Coordinate Mapping(3) = 1 2 3\n")
        sifFileW("  Timestepping Method = "+self.getTimeSteppingMethod()+"\n")
        if self.getTimeSteppingMethod() == "BDF":
            if int(self.getBDFOrder())>0 and int(self.getBDFOrder())<6 :
                #sifFileW("  BDF Order = "+str(self.getBDFOrder())+"\n")
                sifFileW("  BDF Order = 1\n")
                pass
            else:
                raise Exception("BDF Order must integer between 1 and 5")
        else:
            sifFileW("  \n")
            pass
        # the following parameters are irrelevant, they are treated via the coupling algorithm
        sifFileW("  Solver Input File = %s\n"%(self.sifFileName))
        sifFileW("  Timestep Sizes = 100\n")
        sifFileW("  Timestep Intervals = 5\n\n")

        sifFileW("  Output Intervals = 1\n")
        sifFileW("!  Lumped Mass Matrix = "+self.parameterDico["Lumped Mass Matrix"]+"\n")
        sifFileW("  Max Output Level = 3\n")
        sifFileW("End\n\n")
        return None

    def end(self):

       self.elmso.stop()
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
        self.elmso(len(self.speciesNamesList),domainSpeciesAqueousConcentrations)

    def readVelocity(self):
        #print "dbge before the reading"
        self.elmso.readVelocity("velRead")
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
        print("dbg set Darcy velocity ",darcyVelocity)
        #raw_input("set Darcy velocity")
        norm = 0.
        if isinstance(darcyVelocity,Velocity):
                                                                                            #
                                                                                            # we have to distinguish between a constant and a piecewise constant velocity
                                                                                            # For a piecewise constant velocity, the only dependance can be time.
                                                                                            #
            for ind in darcyVelocity.getValue():
                if type(ind) == StringType:
                    self.advConv = "PiecewiseConstant"
                    break
                else:
                    norm += ind**2
            if self.advConv != "PiecewiseConstant":
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

    def setChargeParameter(self, **solverparameterdict):
        """
        Here the parameters of the algebraic solver for the charge are introduced
        """
        print(solverparameterdict.items())
        for key, value in solverparameterdict.items():
            print("setChargeParameter key, value ",key, value)
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
                print(" we set itersolver to ",value)
                self.chargeParameterDico["Linear System Max Iterations"] = value
        self.chargeParameterDico["Flux Parameter"]                      = 5.e-1
        return None

    def setConstantsParameter(self, **constantsdict):
        """
        Here the constants of the problem are introduced
        For gravity, linked to production or injection, the sign can be important.
        """
        for key, value in constantsdict.items():
            if key == "gravityDirection":
                self.gravityDirection = value
                pass
            if key == "gravityValue" :
                self.gravityValue = value
                pass
            if key == "gravity" :
                if value.__class__.__name__ == "V":
                    self.gravityDirection = value.normalize()
                    self.gravityValue = value.magnitude()
                    pass
                pass
            if key == "Stefan Boltzmann" :
                self.stefanBoltzmann = value
                pass
            pass
        return None

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
        
    def setMechanicalSolverParameter(self, **solverparameterdict):
        """
        Here the parameters of the algebraic solver for linear elasticity equations are introduced
        """
        self.mechanicsParameterDico['Steady State Convergence Tolerance'] = 1.e-10
        self.mechanicsParameterDico["Linear System Residual Output"] = 10
        self.mechanicsParameterDico["Non Linear System Newton After Iterations"] = 3
        self.mechanicsParameterDico["Non Linear System Max Iterations"] = 10
        self.mechanicsParameterDico["Non Linear System Convergence Tolerance"] = 1e-09
        self.mechanicsParameterDico["Non Linear System Relaxation Factor"] = 0.5
        self.mechanicsParameterDico["Linear System Iterative Method"] = "BiCGStab"
        self.mechanicsParameterDico["Linear System Convergence Tolerance"] = 1.000000e-08
        self.mechanicsParameterDico["Linear System Preconditioning"] = "ILU1"
        self.mechanicsParameterDico["Linear System ILUT Tolerance"] = 1.e-3
        self.mechanicsParameterDico["Linear System Symmetric"] = False
        self.mechanicsParameterDico["Linear System Precondition Recompute"] = 1
        self.mechanicsParameterDico["Linear System Residual Output"] = 20

        #self.mechanicsParameterDico["Steady State Convergence Tolerance"] = 1e-08

        for key, value in solverparameterdict.items():
            if key == "accelerator" or key =="linearSystemIterativeMethod":
                self.mechanicsParameterDico["Linear System Iterative Method"] = value
            if key == "algebraicResolution":
                self.mechanicsParameterDico["algebraicResolution"] = value
                #
                # for the moment, no multigrid
                #
                self.mechanicsParameterDico["Linear System Direct Method"] = "Banded"
            if key == "BDFOrder" or key == "BDFO" or key.upper() == "BDF":
                self.mechanicsParameterDico["BDF Order"] = str(value)
            else:
                self.mechanicsParameterDico["BDF Order"] = str(1)
            if key == "Bubbles":
                self.mechanicsParameterDico["Bubbles"] = value
            if key == "convSolver":
                self.mechanicsParameterDico["Linear System Convergence Tolerance"] = value
            if key == "discretisation":
                self.mechanicsParameterDico["discretisation"] = value
            if key == "iterSolver":
                self.mechanicsParameterDico["Linear System Max Iterations"] = value
            if key == "linearSystemMaxIterations":
                self.mechanicsParameterDico["Linear System Max Iterations"] = value
            if key == "nonLinearSystemAfterIterations" or key == "nonLinearSystemNewtonAfterIterations":
                self.mechanicsParameterDico["Non Linear System Newton After Iterations"] = value
            if key == "nonLinearSystemMaxIterations":
                self.mechanicsParameterDico["Non Linear System Max Iterations"] = value
            if key == "nonLinearSystemRelaxationFactor":
                self.mechanicsParameterDico["Non Linear System Relaxation Factor"] = value
            if key == "linearSystemConvergenceTol":
                self.mechanicsParameterDico["Linear System Convergence Tolerance"] = value
            if key == "linearSystemILUTTol":
                self.mechanicsParameterDico["Linear System ILUT Tolerance"] = value
            if key == "linearSystemSymetry":
                self.mechanicsParameterDico["Linear System Symmetric"] = value
            if key == "preconditioner":
                self.mechanicsParameterDico["Linear System Preconditioning"] = value
            if key == "steadyStateConvergenceTolerance":
                self.mechanicsParameterDico['Steady State Convergence Tolerance'] = value
            if key == "timeSteppingMethod" or key == "tSM":
                self.mechanicsParameterDico["Timestepping Method"] = value



            pass
        return None

    def setHeatParameter(self, **heatparameterdict):
        """
        Here potential parameters fro the heat equation are introduced.
        For the moment, only the source term necessary for the study of a one dimensional borehole
        is taken into account.
        """
        self.oneDimensionalBoreHole = False
        self.twoPhaseBoreHole = False
        self.parameterDico["variableHeatCapacity"] = False
        self.parameterDico["variableHeatConductivity"] = False
                                                    #
                                                    # we check if we have to handle
                                                    # a one dimensional borehole
                                                    #
        for key, value in heatparameterdict.items():
            if key == "oneDimensionalBoreHole":
                self.parameterDico["oneDimensionalBoreHole"] = True
                self.parameterDico["onePhaseBoreHole"] = True
                break
        for key, value in heatparameterdict.items():
            if key == "variableHeatConductivity":
                self.parameterDico["variableHeatConductivity"] = value
                pass
            elif key == "variableHeatCapacity":
                self.parameterDico["variableHeatCapacity"] = value
                pass
            elif key == "vapor":
                self.parameterDico["vapor"] = value
                if self.parameterDico["vapor"]:
                    self.parameterDico["onePhaseBoreHole"] = False
                    print(" debug ok ? ",self.parameterDico["onePhaseBoreHole"],self.parameterDico["vapor"])
                    self.setWellboreSolverDefaults()
                    #raw_input()
                    pass
                pass
            pass                                                                                #
        return None

    setHeatParameters = setHeatParameter
    
    def setTransportParameter(self, **solverparameterdict):
        """
        Here the parameters of the algebraic solver for transport species equarions are introduced
        """
        self.parameterDico['Steady State Convergence Tolerance'] = 1.e-10
        self.parameterDico["Linear System Residual Output"] = 10
        for key, value in solverparameterdict.items():
            if key == "accelerator":
                self.parameterDico["Linear System Iterative Method"] = value
            if key == "algebraicResolution":
                self.parameterDico["algebraicResolution"] = value
                #
                # for the moment, no multigrid
                #
                self.parameterDico["Linear System Direct Method"] = "Banded"
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
            if key == "linearSystemConvergenceTol":
                self.parameterDico["Linear System Convergence Tolerance"] = value
            if key == "linearSystemILUTTol":
                self.parameterDico["Linear System ILUT Tolerance"] = value
            if key == "linearSystemSymetry":
                self.parameterDico["Linear System Symmetric"] = value
            if key == "preconditioner":
                self.parameterDico["Linear System Preconditioning"] = value
            if key == "steadyStateConvergenceTolerance":
                self.chargeParameterDico['Steady State Convergence Tolerance'] = value
            if key == "timeSteppingMethod" or key == "tSM":
                self.parameterDico["Timestepping Method"] = value
            if key == "Linear System Residual Output":
                self.parameterDico["Linear System Residual Output"] = value
            pass

    def setTwoPhaseProperty(self,aField,propertyName):
        """
        To set properties linked with a two phase flow.

        it enables to handle some properties, see the core of the function.
        """
        if (propertyName.lower() == "aqueousdensity"):
            self.elmso.setPropertyField(aField,"aqueousdensity")
            pass
        elif (propertyName.lower() == "quality"):
            self.elmso.setPropertyField(aField,"quality")
            pass
        else:
            raise Warning, " the field you want to transfer to the solver is not managed."
        return None
        
    def setWaterDensity(self,waterDensity):
        """
        To set the water density to a walue != from 1000.0
        """
        if isinstance(waterDensity,Density):
            self.waterDensity = waterDensity.getValue()
        elif isinstance(waterDensity,float):
            self.waterDensity = waterDensity

    def setSolidDensity(self,solidDensity):
        """
        To set the solid density in the frame of a mechanical problem
        """
        if isinstance(solidDensity,Density):
            self.solidDensity = solidDensity.getValue()
            pass
        elif isinstance(solidDensity,float):
            self.solidDensity = waterDensity
            pass
        return None

    def setWaterHeatCapacity(self,waterHeatCapacity):
        """
        To set the water heatcapacity:  default walue is 4187 J/kg/K
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
            self.elmso.advanceTime()
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
            self.elmso.dt(deltat)
        else:
            self.essaig.dt(deltat)
        return None

    def getConcentrationValues(self):
        """
        used to transfer species concentrations from elmer to the coupling tool
        """
#   print " call of getConcentrationValues"
        if self.instance==2:
            print(" we get from the gas transport concentrations ")
            return self.essaig.getConcentration()
        else:
#       print " call of getConcentrationValues"
            return self.elmso.getConcentration()

    def getCoordinatesValues(self):
        """
        Used to get coordinate values: return is a list of coordinates for node points
        """
    #print " call of getCoordinates"
#        coordinates = self.mesh.getNodesCoordinates()
        coordinates = self.elmso.getCoordinates()
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
        #print " within the python call to getPermutation "
        return self.elmso.getPermutation()

    def getTemperatureField(self):
        """
        Used to transfer the temperature field from elmer to the coupling tool
        """
        return self.elmso.getTemperature()

    def majExpectedOutput(self):
        """
        frequency treatment
        """
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
        if self.problemType not in ['unknown','saturatedhydro','transienthydro',"chemicaltransport","thmc"]:
            raise Exception, " check the kind of problem you want to solve "
        print("self.problemType",self.problemType)
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
                print('tab[0].getColumn(0)',type(tab[0].getColumn(0)),tab[0].getColumn(0))
                poro=list(tab[0].getColumn(1))
                mcf=list(tab[1].getColumn(1))
                stor=[self.density*self.absoluteGravity*(poro[i]*self.fluid_comp+mcf[i]) for i in range(len(poro))]
                tnew.addColumn('f(t)', stor)
                print('poro,mcf,self.fluid_comp,stor',poro,mcf,self.fluid_comp,stor)
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
                                                                                            #
                                                                                            # method used to write the sif file
                                                                                            #
    def init(self,studienName=None, problemType = None):
        """
        Used to launch the Elmer code:
        you set-up here all the file system
        to launch elmer
        """
        if problemType != None:
            problemType = problemType.lower()
            pass
        if self.instance!= None and self.instance!=2:
#           self.name = "./Data/"+studienName + "_ctr"+str(self.instance)
            self.name = "./Data/"+studienName + "_ctr"
            pass
        elif self.instance==2:
            self.name = "./Datag/" + studienName + "_ctr"
            pass

        meshFileName = self.getMeshFileName()

        # Data directory creation
        if not os.path.exists('Data') or not os.path.isdir('Data'):
            os.mkdir('Data')
            pass

        if self.instance==2:
            if not os.path.exists('Datag') or not os.path.isdir('Datag'):
                os.mkdir('Datag')
                pass
            pass
                                                                                            #
                                                                                            # ELMERSOLVER_STARTINFO is the file enabling Elmer to be launched
                                                                                            #
        self.elmerStartInfo = open("ELMERSOLVER_STARTINFO","w")
        self.elmerStartInfo.write("%s\n"%(self.sifFileName))
        self.elmerStartInfo.close()
                                                                                            #
                                                                                            # the sif file defining the simulation
                                                                                            #
        self.createSifFile(problemType)

        if self.instance==0 or self.instance==1:
            print(" initialisation of the instance ");sys.stdout.flush()
            self.elmso = WElmer
            lstring = len(self.elmso.__doc__[self.elmso.__doc__.find("A"):])-2
            print("~"*lstring)
            print(self.elmso.__doc__)
            print("~"*lstring)
            #raw_input()
            self.elmso.initialize()

#           self.elmso.setInstance(self.instance)
            #print "ic_new dbg setSpeciesAnzahl: ",self.instance,self.unAnzahl,type(self.unAnzahl)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(" End of the elmer files writing phase")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            pass
        return None

    def AqueousComponentOneTimeStep(self):
        """
        This method enables to solve one step in time for the aqueous equations
        """
        return self.elmso.oneACTimeStep()

    def HeatOneTimeStep(self):
        """
        This method enables to solve one step in time for the heat equation
        """
        return self.elmso.oneHeatTimeStep()

    def SaturatedHydraulicOneTimeStep(self):
        """
        This method enables to solve one step in time for the saturated hydraulic equation
        """
        return self.elmso.oneSHTimeStep()

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
        print(" ic dbg self.nbTimes %i\n"%(self.nbTimes))
        return

    def setExpectedOutput(self, expected_output_dict_list_ini):
        """
    Set expected outputs
        """
        print("ic dbg Set expected outputs\n")
        expected_output_dict_list=\
           [eoDict.copy() for eoDict in expected_output_dict_list_ini]

        for eoDict in expected_output_dict_list:
            if (eoDict['quantity']=='TotalInflux') or\
               ( eoDict['quantity']=='TotalFlux' and self.problemType=='extendedtransport' ):
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
            pass
        else:
            first_time = 0
            pass

        if self.calculationTimesDico.has_key('final_time'):
            final_time = self.calculationTimesDico ['final_time']
            pass
        else:
            final_time = 1
            pass
        eoTimesList = []
        eo_zone_TimesList = []
        for eoDict in expected_output_dict_list:
            timespec=None
            OKtimespec='timespec' in eoDict.keys()
            if OKtimespec: timespec  = eoDict['timespec']
##             if 'timespec' in eoDict.keys():
            if timespec:
                eoName    = eoDict['name']
##                 timespec  = eoDict['timespec']
                spec = timespec.getSpecification()
                if spec == 'times':
                    eoTimes = timespec.getTimes()
                    pass
                    #print " 'times' eoTimes",eoTimes
                elif spec == 'period':
                    f  = timespec.getPeriod()
                    t  = first_time
                    ft = final_time
                    eoTimes = [t]
                    while t < ft:
                        t += f
                        if t <= ft: eoTimes.append(t)
                        pass
                    eoDict['timespec'] = TimeSpecification(times = eoTimes)
                    pass
                    #print " 'period' eoTimes",eoTimes

                elif spec == 'frequency':
                    eoTimes = []
                    pass
                else:
                    raise Exception, "The way you try to introduce output time specification has not been treated"

                eoTimesList += eoTimes
                #
                support = eoDict['support']
                pass
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
                print('eoTimesJGLIST[ifin-1],final_time',eoTimesJGLIST[ifin-1],final_time)
                ifin-=1
                pass
            eoTimesJGLIST=eoTimesJGLIST[ideb:ifin]
            self.calculationTimesDico['all_times']=\
                     tableUnion(self.calculationTimesDico['all_times'],eoTimesJGLIST)
            pass

        # Traitement des differents types de support :
        if len(outpoint) != None:
            nbCell    = len(outpoint)
            pass
        else:
            nbCell    = 0
            pass
        if len(outsurf) != None:
            nbSurf    = len(outsurf)
            pass
        else:
            nbSurf    = 0
            pass

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
                pass
            pass

        # Zones ...
        nbCellZone   = []
        cellZoneTemp = []
        quantiteZone = []
        nomZone      = []
        supportZone  = []
        where        = []
        tempsZone    = []
        for zz in outzone:
            print('OUTPUT ZONE !',zz['name'])
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
                    pass
                pass
            else:
                where.append('center')
                pass
            pass

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
                pass
            pass
        elif (dim==3):
            for i in range(0,len(koordinaten)):
                self.file_mesh.write("%15.8e %15.8e %15.8e\n"%(koordinaten[i][0],koordinaten[i][1],koordinaten[i][2]))
                pass
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
                pass
            if gmshType == 2:           # 3-node triangles
                cellListSize += 4
                pass
            if gmshType == 3:           # 4-node quadrangles
                cellListSize += 5
                pass
            elif gmshType == 4:         # 4-node tetrahedron
                cellListSize += 5
                pass
            elif gmshType == 5:         # 8-node hexahedrons
                cellListSize += 9
                pass
            elif gmshType == 6:         # 6-node prism
                cellListSize += 7
                pass
            elif gmshType == 7:         # 5-node pyramid
                cellListSize += 6
                pass
            pass

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
                pass
            elif (vtkTyp==5):                                                               # 3-node triangle
                self.file_mesh.write("%i %i %i %i\n"%(3,\
                                                   cell[ind]-1,
                                                   cell[ind+1]-1,
                                                   cell[ind+2]-1))
                pass
            elif (vtkTyp==9):                                                               # 4-node quadr
                self.file_mesh.write("%i %i %i %i %i\n"%(4,\
                                                   cell[ind  ]-1,
                                                   cell[ind+1]-1,
                                                   cell[ind+2]-1,
                                                   cell[ind+3]-1))
                pass
            elif (vtkTyp==10):                                                              # 4-node tetra
            #print "zcell ",cell
                self.file_mesh.write("%i %i %i %i %i\n"%(4,\
                                                   cell[ind  ]-1,
                                                   cell[ind+1]-1,
                                                   cell[ind+2]-1,
                                                   cell[ind+3]-1))
                pass
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
                pass
            elif (vtkTyp==13):                                                              # prism : 6-nodes
                self.file_mesh.write("%i %i %i %i %i %i %i\n"%(6,\
                                                   cell[ind  ]-1,\
                                                   cell[ind+1]-1,\
                                                   cell[ind+2]-1,\
                                                   cell[ind+3]-1,\
                                                   cell[ind+4]-1,\
                                                   cell[ind+5]-1))
                pass
            elif (vtkTyp==14):                                                              # pyramid : 5-nodes
                self.file_mesh.write("%i %i %i %i %i %i %i\n"%(5,\
                                                 cell[ind  ]-1,\
                                                 cell[ind+1]-1,\
                                                 cell[ind+2]-1,\
                                                 cell[ind+3]-1,\
                                                 cell[ind+4]-1))
                pass
        self.file_mesh.flush()
        self.file_mesh.write("%s %i\n"%("CELL_TYPES",numberOfCells))
        #print "dbg vtkTyp",vtkTyp,numberOfCells
        for i in range(0,numberOfCells):
            gmshType = connectivity[i][1]
            if gmshType not in [1,2,3,4,5,6]: print(" gmshType ",gmshType)
            if gmshType == 1:           # 2-node line
                cellTyp = 3
                pass
            elif gmshType == 2:         # 3-node triangle
                cellTyp = 5
                pass
            elif gmshType == 3:         # 4-node quadrangle
                cellTyp = 9
                pass
            elif gmshType == 4:         # 4-node tetrahedron
                cellTyp = 10
                pass
            elif gmshType == 5:         # 8-node hexahedron
                cellTyp = 12
                pass
            elif gmshType == 6:         # 6-node prism
                cellTyp = 13
                pass
            elif gmshType == 7:         # 5-node pyramid
                cellTyp = 14
                pass
            self.file_mesh.write("%i\n"%(cellTyp))
            pass
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
        self.elmso.setSource(source)
        return None

    def setBodyList(self,bodies):
        """
        we give access of bodies list to elmer, bodies
        here are to be understood in the sense of the coupling algorithm
        """
        #raw_input("we are within set bodies list")
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
#       print " coupling ",py setconcentration values for instance 0",self.instance,self.unAnzahl,len(concentrations)
        #raw_input()
            self.elmso.setConcentration(concentrations)
            pass
        elif self.instance==2:
            print(" type of self.unAnzahl for instance 2",self.instance,self.gunAnzahl)
            #self.essaig.setConcentration(concentrations,1,self.gunAnzahl)
            pass
        else:
            #self.elmso.setConcentrationValues(concentrations,1,self.unAnzahl-1)
            pass
        return None
    #---------------------------------------------------------------------------
    #---------------------------------------------------------------------------

    def setPermeabilityField(self,permeabilityField):
        """

        """
        self.elmso.setPermeabilityField(permeabilityField)

    def getPermeabilityField(self):
        """

        Used to retrieve th permeability field for output

        """
        return self.elmso.getPermeabilityField()

    def setSpeciesNames(self):
        """set species names
           speciesList :  contains a species list
           return a species names list
        """
        self.speciesNamesList = []
        ind = 0
        for species in self.speciesList:
            #print "dbg elmer species names ",ind,species.getName()
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
        self.elmso.setTemperature(temperatureField)
        return None

    def setWHeatCapacityField(self,thermalCapacityField):
        """
        to set the thermal capacity field at constant pressure

        """
        self.elmso.setWHeatCapacityField(thermalCapacityField)

    def setWHeatConductivityField(self,thermalConductivityField):
        """
        to set the thermal conductivity field

        """
        self.elmso.setWHeatConductivityField(thermalConductivityField)

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
        print(dir(fieldList[0]),self.speciesNamesList)
        for specInd in range(len(self.speciesNamesList)):
            speciesName = self.speciesNamesList[0]
            field      = fieldList[0]
            values     = field.getValues()
            bodiesDico  = Dico()
            val      = values[0]
            bodiesDico["domain"] = (val)
            self.effectiveDiffusionDico[speciesName] = bodiesDico
            pass
        return

    def setOutputName(self, name):
        self.outputName = name

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
            print("dbg porosity dico setting",values)
            self.porosityDico[specieName] = values
            pass
        return None

    def setPorosityField(self,porosityfield):
        """
        sets the porosity to elmer

        Input  : a porosity field, a scalar being associated to each mesh node
        """
        self.elmso.setPorosityField(porosityfield)
        print(" im_n dbg setPorosityValues")
        return None

    def getPorosityValues(self):
        """
        This method is used to supply a porosity list to the chemistry code.
        It should be enhanced .
        """
        porosityField = [1.0]*self.mesh.getNodesAnz()
        #print(" e dbg transport: number of nodes",self.mesh.getNodesAnz())
        #for body in self.getBodies():
        #print dir(body)
        #print " support          ",dir(body.getSupport())
        #print " zone             ",body.getZone()

        for body in self.getBodies():
            porosityValue = body.material.getPorosity().value
            #print "porosityValue ",porosityValue,len(body.getSupport().getBodyNodesList())
            for i in body.getSupport().getBodyNodesList():
                porosityField[i-1] = porosityValue
                pass
            pass
        #print "edbg length of porosityfield ",len(porosityField)
        #raw_input("elmer length porosity field")
        #raw_input("getPorosityValues")
        return porosityField

    def setTwoPhasesBoreholeParameters(self,nodeCoordinates):
        """
        method to be called in chemicaltransportmodule
        """
        self.deltaL = [300.]*len(nodeCoordinates)
        self.roughnesses = [1.e-5]*len(nodeCoordinates)
        self.tubeDiameters = [2.1033700000e-01]*len(nodeCoordinates)
        self.coordinates = nodeCoordinates
        self.gravityField = [9.81]*len(nodeCoordinates)
        #
        # twoPhasesPressureEvaluationControl is a parameter to control the way the presure is evaluated
        # Before a call to the mass flow solver, the initial pressure field is taken.
        #
        self.twoPhasesPressureEvaluationControl = 0
        pass
        

    def setUnknownsNumber(self,unAnzahl):
        """
        Set the transported phase unknown number
        """
        self.unAnzahl = unAnzahl
        return None

    def writeEquation1(self):
        sifFile = self.sifFile
        sifFileW = sifFile.write
        sifFileW("! ~~\n! Equation p28 ref. Manual\n! ~~\n")
        #print "self.speciesNamesList",self.speciesNamesList
        #raw_input("self.speciesNamesList")
        for ind in range(len(self.speciesNamesList)):
            sifFileW("Equation %i\n"%(ind+1))
            sifFileW("  Advection Diffusion Equation %s True\n"%self.speciesNamesList[ind])
            sifFileW("  Convection %s\n"%self.advConv)
            sifFileW("  Concentration Units = Absolute Mass\n")
            pass
        if self.temperature == None:
            sifFileW("  ActiveSolvers(1) = 1\n")
            pass
        else:
            sifFileW("  ActiveSolvers(2) = 1 2\n")
            pass
        sifFileW("End\n\n")
        return None

    def writeMaterial1(self):
        """
        A loop over materials and species.
        Each material is associated to each species.
        The numbering is on three digits, two for the species, at least one for the region.
        For the moment, the material is independant of the species.
        """

        sifFile = self.sifFile
        sifFileW = sifFile.write
        sifFileW("! ~~\n! Material p29 ref. Manual\n! ~~\n")
        for inds in range(len(self.speciesNamesList)):
            for indb in range(len(self.bodies)):
                stinds = _digit(inds)
                stindb = str(indb+1)+stinds
                sifFileW("Material %s\n"%(stindb))
                if self.advConv == "Constant":
                    v = self.darcyVelocity.getValue()
                    sifFileW("  ! darcy velocity\n")
                    sifFileW("  Convection velocity %e %e %e\n"%(v[0],v[1],v[2]))
                    pass
                sifFileW(" %s Diffusivity %15.10e\n"%(self.speciesNamesList[inds],\
                                  self.bodies[indb].getMaterial().getEffectiveDiffusion().value.value))

                sifFileW(" %s Soret Diffusivity %15.10e\n"%(self.speciesNamesList[inds],\
                                  self.bodies[indb].getMaterial().getThermalConductivity().value.value))
                sifFileW("End\n\n")
                pass
            pass
        return None


def printm(lineToPrint,ri = None):
    lineToPrint = " el_dbg "+lineToPrint+" at line: "+str(currentframe().f_back.f_lineno+1)+" \n"
    if ri != None:
        raw_input(lineToPrint)
    else:
        print(lineToPrint)
        pass
    return None


def _digit(ind):
    if ind < 8:
        return "0"+str(ind+1)
    else:
        return str(ind+1)

def _matcString(matcListOfChar):
    """
    enables to control, in some extent, the introduction of a matc string.
    In commonmodel, the string has been analysed. The user doesn't neeed to known anything about matc functions.
    He has just to handle x, y or z.
    """
    matcListOfChar = string.join(matcListOfChar).replace(" ","")
    if "x" in matcListOfChar:
        matcListOfChar = matcListOfChar.replace("x","tx(0)")
        pass
    if "y" in matcListOfChar:
        matcListOfChar.replace("y","tx(1)")
        pass
    if "z" in matcListOfChar:
        matcListOfChar.replace("z","tx(2)")
        pass
    return matcListOfChar
    
def _TimeException():
    message = "look at the time discretisation, discrepancies exist\n"
    raise Exception, message

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
        pass

    return indVtk

def _wellboreParameter(wellboreDataDict, sifFile, string):
    #print(wellboreDataDict.keys())
    #raw_input()
    sfpar = " %18s"
    sifFileW = sifFile.write
    if string in wellboreDataDict.keys():
        #print " debug ",string,wellboreDataDict[string].keys()[0][0]
        if wellboreDataDict[string].keys()[0].lower() == "real":
            print ("dbg elmer: ",wellboreDataDict[string])
            sifFileW(" %-20s = Real %15.10e ! %s\n"%(string.ljust(16),float(wellboreDataDict[string]["Real"][0]), wellboreDataDict[string]["Real"][1]))
            pass
        elif wellboreDataDict[string].keys()[0].lower() == "int":
            sifFileW(" %-20s = Integer %5i ! %s\n"%(string.ljust(16),int(wellboreDataDict[string]["Int"][0]), wellboreDataDict[string]["Int"][1]))
            pass
        elif wellboreDataDict[string].keys()[0].lower() == "variable":
#            sifFileW(" %16s = Variable \"Coordinate 1\"\n%s\n"%(string.ljust(16), wellboreDataDict[string]["Variable"][0]))
            sifFileW(" %-20s = Variable Coordinate 1\n%s %13s %s\n"%(string.ljust(16), wellboreDataDict[string]["Variable"][0],"!",\
                                                                                            wellboreDataDict[string]["Variable"][1]))
            pass
        elif wellboreDataDict[string].keys()[0].lower() == "logical":
            sifFileW(" %-20s = Logical %s\n"%(string.ljust(16),str(wellboreDataDict[string]["Logical"][0]),))
            pass
        else:
            #print(" debug : %s\n"%(wellboreDataDict[string].keys()[0].lower()))
            raise Warning, color.red+"check the wellbore or the two phase wellbore data file for key string of unknown type: "+color.end+string

    else:
        print("debug: ",wellboreDataDict.keys())
        raise Warning, color.red+"check the wellbore or the two phase wellbore data file for string: "+color.end+string


def _writeHeatLoadParameters(sifFile, materialId, bodyName = None):
    from wellBoreReader import *
    fineName = os.environ["PWD"]+"/Data/wellbore.dat"
    #
    # the file has not to be read for each material : has to be corrected
    #
    sifFileW = sifFile.write
    wellboreDataDict = wellBoreDataRead(fineName)
    #print (wellboreDataDict)
    #raw_input("_writeHeatLoadParameters: "+str(materialId) +" "+ str(bodyName))
    if bodyName == None:
        materialKey = "Material"+str(materialId)
    else:
        try:
            materialKey = wellboreDataDict[bodyName]
        except:
            raise Warning, " check the way the data for the wellbore are implemented: "+str(bodyName)

    #
    # at least we consider one material => the dictionary has Material1 as a key
    #
    if wellboreDataDict.has_key(materialKey) == False:
        materialKey = "Material1"
    sifFileW("! -------------------------------------------------\n")
    sifFileW("! Physical properties linked to a wellbore analysis\n")
    sifFileW("! -------------------------------------------------\n")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "fluidDensity")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "dynViscosity")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "fluidThermCond")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "fluidCp")
    sifFileW("! --------------------------------------\n")
    sifFileW("! geometrical parameters of the wellbore\n")
    sifFileW("! --------------------------------------\n")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "d_tubing")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "t_tube")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "t_annulus")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "t_casing")
    #_wellboreParameter(wellboreDataDict[materialKey], sifFile, "t_insulation")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "t_cement")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "inclination")
    sifFileW("! ---------------------------------------------------\n")
    sifFileW("! physical properties linked to the wellbore geometry\n")
    sifFileW("! ---------------------------------------------------\n")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "tubeThermCond")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "tubeRoughness")
    #_wellboreParameter(wellboreDataDict[materialKey], sifFile, "insulationThermCond")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "casingThermCond")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "cementThermCond")
    sifFileW("! ---------------------------------------------\n")
    sifFileW("! physical properties linked to the underground\n")
    sifFileW("! ---------------------------------------------\n")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "earthDensity")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "earthThermCond")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "earthCp")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "earthTempGradient")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "groundTemperature")
   # _wellboreParameter(wellboreDataDict[materialKey], sifFile, "earthTemperature")
    if wellboreDataDict[materialKey].has_key("TemperatureInterpolation"):
        #raw_input(" wellboreDataDict")
        _wellboreParameter(wellboreDataDict[materialKey], sifFile, "TemperatureInterpolation")
                                                         #
                                                     # we realize the interpolation with a second order polynomial
                                                     #
        _wellboreParameter(wellboreDataDict[materialKey], sifFile, "T1")
        _wellboreParameter(wellboreDataDict[materialKey], sifFile, "T2")
        _wellboreParameter(wellboreDataDict[materialKey], sifFile, "T3")
        pass
    sifFileW("! ---------------\n")
    sifFileW("! Dummy arguments\n")
    sifFileW("! ---------------\n")
    if wellboreDataDict[materialKey].has_key("p0"):
        _wellboreParameter(wellboreDataDict[materialKey], sifFile, "p0")
        pass
    else:
        sifFileW("  p0 = Real 1.5e6\n")
        pass
    if wellboreDataDict[materialKey].has_key("p1"):
        _wellboreParameter(wellboreDataDict[materialKey], sifFile, "p1")
        pass
    else:
        sifFileW("  p1 = Real 1.5e6\n")
        pass
    sifFileW("! ---------------\n")
    sifFileW("! transient terms\n")
    sifFileW("! ---------------")
    #os.system("cp -rp $WRAPPER/Python/Data/p_wellhead.dat $PWD")
    #sifFile.write(" p1 = Variable (time - 0.1)\n%8s\n%s\n"%("Real","    include p_wellhead.dat"))
    #sifFile.write(" p1 = Variable (time + 0.1)\n%8s\n%s\n"%("Real","    include p_wellhead.dat"))

    return None


def _writeTwoPhaseHeatLoadParameters(sifFile, materialId, bodyName = None):
    from wellBoreReader import *
    sifFileW = sifFile.write
    fileName = os.environ["PWD"]+"/Data/twophasewellbore.dat"
    #
    # the file has not to be read for each material : has to be corrected
    #
    wellboreDataDict = wellBoreDataRead(fileName, onePhase = False)
    #print wellboreDataDict
    #raw_input("_writeHeatLoadParameters: "+str(materialId) +" "+ str(bodyName))
    if bodyName == None:
        materialKey = "Material"+str(materialId)
        pass
    else:
        try:
            materialKey = wellboreDataDict[bodyName]
        except:
            raise Warning, " check the way the data for the wellbore are implemented: "+str(bodyName)

    #
    # at least we consider one material => the dictionary has Material1 as a key
    #
    if wellboreDataDict.has_key(materialKey) == False:
        materialKey = "Material1"
        pass
    sifFileW("! -------------------------------------------------------------------------\n")
    sifFileW("! Physical properties linked to a homogenised two phases wellbore analysis \n")
    sifFileW("! -------------------------------------------------------------------------\n")
    sifFileW("! ----------------------------------------\n")
    sifFileW("! Physical properties of the liquid phase \n")
    sifFileW("! ----------------------------------------\n")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "liquidDensity")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "liquidDynViscosity")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "liquidThermCond")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "liquidEnthalpy")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "liquidCp")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "liquidAlphaCoef")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "liquidKappaCoef")
    print(wellboreDataDict.keys)
    sifFileW("! --------------------\n")
    sifFileW("! water level parameter\n")
    sifFileW("! --------------------\n");sifFile.flush()
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "annWaterLevel")
    sifFileW("! --------------------\n");sifFile.flush()
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "enthalpyScale")
    sifFileW("! --------------------\n");sifFile.flush()
    sifFileW("! ---------------------------------------\n")
    sifFileW("! Physical properties of the vapor phase \n")
    sifFileW("! ---------------------------------------\n")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "gasDensity")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "gasDynViscosity")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "gasThermCond")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "gasEnthalpy")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "gasCp")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "gasAlphaCoef")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "gasKappaCoef");sifFile.flush()
    sifFileW("! ---------------------------\n")
    sifFileW("! average physical properties\n")
    sifFileW("! ---------------------------\n")
    sifFileW(" mixedDensity = Variable VoidFraction\n")
                                                                                            #
                                                                                            # density of the mixture
                                                                                            #
    sifFileW("   Real MATC \"%s*tx +(1-tx)*%s\"\n"%(wellboreDataDict[materialKey]["gasDensity"]["Real"][0],\
                                                         wellboreDataDict[materialKey]["liquidDensity"]["Real"][0]))
                                                                                            #
                                                                                            # surface tension
                                                                                            #
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "SurfaceTension")
    
    sifFileW("! --------------------------------------\n")
    sifFileW("! geometrical parameters of the wellbore\n")
    sifFileW("! --------------------------------------\n")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "d_tubing")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "t_tube")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "t_annulus")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "t_casing")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "t_insulation")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "t_cement")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "inclination");sifFile.flush()
    sifFileW("! ---------------------------------------------------\n")
    sifFileW("! physical properties linked to the wellbore geometry\n")
    sifFileW("! ---------------------------------------------------\n")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "tubeThermCond")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "tubeRoughness")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "insulationThermCond")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "casingThermCond")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "cementThermCond");sifFile.flush()
    sifFileW("! ---------------------------------------------\n")
    sifFileW("! physical properties linked to the underground\n")
    sifFileW("! ---------------------------------------------\n")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "earthDensity")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "earthThermCond")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "earthCp")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "earthTempGradient")
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "groundTemperature");sifFile.flush()
    _wellboreParameter(wellboreDataDict[materialKey], sifFile, "earthTemperature")
    if wellboreDataDict[materialKey].has_key("TemperatureInterpolation"):
        #raw_input(" wellboreDataDict")
        _wellboreParameter(wellboreDataDict[materialKey], sifFile, "TemperatureInterpolation")
                                                                                            #
                                                                                            # we realize the interpolation with a second order polynomial
                                                                                            #
        _wellboreParameter(wellboreDataDict[materialKey], sifFile, "T1")
        _wellboreParameter(wellboreDataDict[materialKey], sifFile, "T2")
        _wellboreParameter(wellboreDataDict[materialKey], sifFile, "T3")
        pass
    sifFileW("! ---------------\n")
    sifFileW("! Dummy arguments\n")
    sifFileW("! ---------------\n")
    if wellboreDataDict[materialKey].has_key("p0"):
        _wellboreParameter(wellboreDataDict[materialKey], sifFile, "p0")
        pass
    else:
        sifFileW("  p0 = Real 1.5e6\n")
        pass
    if wellboreDataDict[materialKey].has_key("p1"):
        _wellboreParameter(wellboreDataDict[materialKey], sifFile, "p1")
        pass
    else:
        sifFileW("  p1 = Real 1.5e6\n")
        pass
    sifFileW("! ---------------\n")
    sifFileW("! transient terms\n")
    sifFileW("! ---------------\n")
    #os.system("cp -rp $WRAPPER/Python/Data/p_wellhead.dat $PWD")
    #sifFile.write(" p1 = Variable (time - 0.1)\n%8s\n%s\n"%("Real","    include p_wellhead.dat"))
    #sifFile.write(" p1 = Variable (time + 0.1)\n%8s\n%s\n"%("Real","    include p_wellhead.dat"))

    return None
