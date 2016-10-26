# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
import types

import os.path
#

from elmertools import *
from tensors import Tensor
from listtools import toList
from mesh import *
from numpy import  float as Float
from os import system
from types import StringType
from mechanicalproblem import MechanicalProblem
from thmcproblem import THMCProblem
from six.moves import range
#
class MechanicalModule:
    """
    The mechanical module will be set up to treat elastic and plastic problems.
    Here only elasticity is treated, elmer being the only available tool.
    
    Elasticity:
    
     The Youngs's modulus or elasticity modulus is the constant linking constraint ( traction or compression ) to deformation:
     
        sigma = E * eps
        
        sigma: constraint with the dimension of a pressure
        
        E: Young's modulus
        
        eps: deformation
        
    """
    def __init__(self):
        self.calculationTimes            = None
        self.density                     = None
        self.gravity                     = None
        self.matrixCompressibilityFactor = None
        self.porosity                    = None
        self.simulationType              = "Steady"
        self.sifFileName                 = "test.sif"
        self.timeStepIntervals           = None
        self.sourceField                 = None
    #     
    # All physical parameters relevant to the phenomenology are treated here
    #
    # Boundary conditions are defined through Normal forces or displacements.
    #
    def setData(self, problem,\
                mesh = None,\
                dicobc = None,\
                dicoic = None):

        self.expectedOutput = None
        self.problem = problem
        #print problem.__class__.__name__
        if not isinstance(problem, MechanicalProblem) and not isinstance(problem, THMCProblem):
            raise Exception(" the problem must be a mechanical problem")
        self.problemName = problem.getName()
        self.regions = problem.getRegions()

        self.mesh = mesh
        mediumProperties = {
                            "density"                    : None,
                            "gravity"                    : None,
                            "YoungModulus"               : None,
                            "PoissonRatio"               : None, 
                           }
        #
        # regionProperties is a dictionnary. It is made of a list of tuples, each region is associated to a dictionnary,
        # the dictionnary containing the medium region properties.
        #                        
        self.regionProperties   = {}
        #
        self.times = problem.getCalculationTimes()
        #
        if self.times == None:
            self.simulationType = "Steady"
        else:
            self.simulationType = "Transient"
        #                        
        self.boundaryConditions = {}
        #                        
        self.initialConditions  = {}
                                                                                            #
                                                                                            # we fill the medium properties dictionnary
                                                                                            #
        self.solidDensity = problem.getDensity()
        self.gravity      = problem.getGravity()
        #
        for reg in self.regions:
            regionName = reg.support.getBodyName()
            material = reg.getMaterial()
            self.regionProperties[regionName] = mediumProperties

            youngModulus = material.youngModulus
            poissonRatio = material.poissonRatio
            intrinsicPermeability = material.getIntrinsicPermeability()
            self.regionProperties[regionName]["density"]                = material.density
            self.regionProperties[regionName]["gravity"]                = self.gravity
            self.regionProperties[regionName]["youngModulus"]           = youngModulus
            self.regionProperties[regionName]["poissonRatio"]           = poissonRatio
            pass
                                                                                            #
                                                                                            # We treat here the boundary conditions.
                                                                                            # We establish a dictionnary independant
                                                                                            # from the tool to be treated.
                                                                                            #
        boundarySpecification = {
                                "typ"           : None,
                                "Displacement"  : None,
                                "Normalforce"   : None,
                                "material"      : None,
                                }
        boundaryConditions = problem.getBoundaryConditions()
        from vector import V as Vector
        #
        ind = 0
        for boundaryCondition in boundaryConditions:
            #print "dir boundary",dir(boundaryCondition)
            #print "boundary name ",boundaryCondition.name
            #print boundaryCondition.getSupport()
            bodyToConsider = boundaryCondition.boundary
            print(bodyToConsider)
            print("entity ", bodyToConsider.getEntity())
            print(" type " , boundaryCondition.getType())
            print(" name " , bodyToConsider.getName())
            #print "material ",boundaryCondition.boundary.material
            #raw_input()
            dis = boundaryCondition.getDisplacementValue()
            #print type(dis)
            #raw_input("dis")
            nf = boundaryCondition.getNormalForceValue()
            ok = 0
            for reg in self.regions:
                if reg.getSupport().getName() == bodyToConsider.getName():
                    #print "material ",reg.material;raw_input()
                    ok = 1
                    break
                pass
            if ok == 0:
                raise Warning("Check the definition of regions and boundaries")
            
            self.boundaryConditions[ind] = {"name": bodyToConsider.getName(),\
                                            "index": bodyToConsider.getEntity(),\
                                            "bodyName": bodyToConsider.getBodyName(),\
                                            "Displacement": dis,\
                                            "Normalforce": nf,\
                                            "Material":reg.material, # boundaryCondition.boundary.material,
                                            "type": boundaryCondition.getType()[0],
                                            "description": boundaryCondition.description
                                           }
            ind+=1
            pass
                                                                                            #
                                                                                            # We treat now the initial conditions
                                                                                            #
        ind = 0
        initialConditions = problem.getInitialConditions()
        if initialConditions!= None:
            for initialCondition in initialConditions:
                value = initialCondition.value # a displacement
                initialConditionName = initialCondition.body.getBodyName()
                ok = 0
                for reg in self.regions:
                    if reg.getSupport().getName() == bodyToConsider.getName():
                        #print "material ",reg.material;raw_input()
                        ok = 1
                        break
                if ok == 0:
                    raise Warning("Check the definition of regions and boundaries")
            
                self.initialConditions[ind] = {"name": initialConditionName,\
                                               "Displacement": value,\
                                               "material": reg.getMaterial(),
                                               "index": initialCondition.body.getEntity(),\
                                               "description": initialCondition.description
                                              }
                pass
            pass
                                                                                            #
                                                                                            # We treat now the sources
                                                                                            #
        sourceList = problem.getSources()
        sourceCtrl = 0
        if sourceList:
            from datamodel import Flowrate
            sourceFlowrate = NumericZoneField('source', mesh, ["source"])
            sourceList = toList(sourceList)
            for source in sourceList:

                value = source.getValue()
                if isInstance(value,Flowrate):
                    sourceFlowrate.setZone(source.getZone(), [value.getValue()])
                    sourceCtrl = 1
                    pass
                pass
            pass

        if sourceCtrl:
            self.sourceField = sourceFlowrate
            pass
                                                                                            #        
                                                                                            # We treat outputs: 
                                                                                            # outputs -> list of dictionnary
                                                                                            #
        if self.expectedOutput:
            for eo in self.expectedOutput:
                varnames=['Pressure']
                eo['varnames'] = varnames
                pass
            pass
        
    def setComponent(self,componentName):
        
        if type(componentName) == StringType:
            self.componentName = componentName.lower()
            from elmer import Elmer
            self.componentName == "elmer"
            self.mechanicalSolver = Elmer(self.mesh)
            self.mechanicalSolver.calcTimesDico              = Dico()

            self.mechanicalSolver.setMechaSolverDefaults()
            self.mechanicalSolver.setProblemType("mechanical")
            self.mechanicalSolver.setDirBC(None, self.boundaryConditions)
            self.mechanicalSolver.setDirIC(self.initialConditions)
            if (self.timeStepIntervals == None and self.calculationTimes != None):
                self.timeStepIntervals = len(self.calculationTimes)-1
                self.timeStepSizes = [self.calculationTimes[i+1]-self.calculationTimes[i] for i in range(len(self.calculationTimes)-1)]
                pass
            elif (self.timeStepIntervals != None):
                self.mechanicalSolver.setTimeDiscretisation(self.timeStepIntervals, self.timeStepSizes)
                pass
            self.mechanicalSolver.setOutputName(self.problem.name)
            pass
        else:
            raise Warning(" the default mechanical solver has been fixed to elmer ")
            self.componentName = "elmer"
            pass
        #
        #
        #
        self.mechanicalSolver.setBodyList(self.problem.getRegions())
        #
        #
        #
#   print " dbg hm we set the bic ",self.boundaryConditions
        self.mechanicalSolver.setBoundaryConditionConcentrations(self.boundaryConditions)
                                                                                            #
                                                                                            # Density
                                                                                            #
        if self.density: self.mechanicalSolver.setSolidDensity(self.density)
                                                                                            #
                                                                                            #
                                                                                            #
        #self.mechanicalSolver.setInitialConditions(self.initialConditions)
                                                                                            #
                                                                                            # Gravity
                                                                                            #
        #if self.gravity:
    #    self.mechanicalSolver.setGravity(self.gravity)
                                                                                            #
                                                                                            # Porosity
                                                                                            #
        if self.matrixCompressibilityFactor: self.mechanicalSolver.setMatrixCompressibilityFactor(self.matrixCompressibilityFactor)
                                                                                            #
                                                                                            # Sources
                                                                                            #
        if self.sourceField : self.mechanicalSolver.setSource(self.sourceField)
                                                                                            #
                                                                                            # time steps treatment
                                                                                            #
        if self.simulationType == "Transient": self.mechanicalSolver.calcTimesDico ['finalTime']= self.problem.calculationTimes[-1]
                                                                                            #       
                                                                                            # to affect numerical parameters
                                                                                            #
    def setSolverParameter(self,*tuple,**dico):
    
        if self.mechanicalSolver:
            self.mechanicalSolver.setMechanicalSolverParameter(*tuple,**dico)
            #print self.mechanicalSolver.mechanicsParameterDico.keys()
            #raw_input("setMechanicalSolverParameter")
            pass
        else:
            raise Exception(" You have to set the Mechanical component solver")

    def setTimeDiscretisation(self,timeStepIntervals = None, timeStepSizes = None):
        """
        setting time steps through the number of time Steps or the size of time steps.
        Every time, a real is used. It should become a list.
        """
        if timeStepIntervals != None:
            self.timeStepIntervals = timeStepIntervals
            pass
        elif timeStepSizes != None:
            self.timeStepSizes = timeStepSizes
            pass
        else:
            raise Warning("You should give at least an argument to the setTimeDiscretisation function")
        if self.timeStepIntervals != None:
            print("dbg hm ",self.timeStepIntervals)
            print("dbg hm ",self.problem.calculationTimes[-1])
            self.timeStepSizes = self.problem.calculationTimes[-1]/self.timeStepIntervals
            pass
        else:
            self.timeStepIntervals = self.problem.calculationTimes[-1]/self.timeStepSizes
            pass
            
    setCalculationTimes = setTimeDiscretisation

    def writeToFile(self):
        pass

    def getOutput(self,name, outputType = None):
        """
        The velocity is read from the file HeVel.ep within the mesh file.
        This file is issued from the successfull run of the two method,
        Darcy and Flux
        """
        #
        # transient part
        #
        if self.simulationType == "Transient":
            #
            # charge
            #
            #raw_input(" trying to retrieve charge")
            
            self.charge = self.flowComponent.essai.getCharge()
            print(self.charge[0:10])
           #raw_input(" trying to retrieve points")
            self.points = self.flowComponent.essai.getCoordinates()
            self.points = self.mesh.getNodesCoordinates()
            print(self.points)
            #raw_input(" trying to retrieve velocity")
            self.velocity = self.flowComponent.essai.getVelocity()
            return self.points, self.charge, self.velocity
        #
        # steady part
        #
        if type(name) == StringType:
            if name.lower() == "velocity":
                fileName = "./" + self.flowComponent.meshDirectoryName + "/" + "HeVel.ep"
                if not os.path.isfile(fileName):
                    message = " problem with the velocity file: " + fileName
                    raise Exception(message)
                    return None
                pass
            elif name.lower() == "watercontent":
                fileName = "./" + "watercontent.vtu"
                pass

            velocityFile=open(fileName,'r')
            velocityFile.readline()
            velocityFile.readline()
            line = velocityFile.readline()
            f = len(line)/3
            self.points = []
            while "#group all" not in line:
                #line = line.split()
                self.points.append([float(line[0:17]),float(line[17:34]),float(line[34:53])])
                line = velocityFile.readline()
                pass
            while "#time" not in velocityFile.readline():
                pass
            line = velocityFile.readline()
            physic = []
            while len(line) > 1:
                physic.append([float(line[0:17]),\
                               float(line[17:34]),\
                               float(line[34:51]),\
                               float(line[51:68])])
                line = velocityFile.readline()
                pass
            self.charge = []
            self.velocity = []
            ind = 0
            for iunknown in range(0,len(physic)):
                a = physic[iunknown]
                self.charge.append(a[0])
                self.velocity.append([a[1],a[2],a[3]])
                ind+=1
                pass
        return self.points, self.charge, self.velocity
            
    def end(self):
        """simulation stop and clean"""
        if self.flowComponent:
            self.flowComponent.end()
            pass
            
    def getComponentName(self):
        """
        to get the name of the component, that has been defined, if any
        """
        if self.componentName:
            return self.componentName
        else:
            raise Warning("No component name has been currently defined")
            
    def getComponent(self):
        """
        to get the component
        """
        return self.flowComponent

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
        self.mechanicalSolver.createSifFile()
        if self.simulationType == "Transient":
            print("dbgpy launching WElmer")
            #
            # the definition of chemistry being needed, we make the hypothesis the chemytry/solver
            # part is launched first
            #
            if isinstance(problem, MechanicalProblem) and not isinstance(problem, THMCProblem):
                self.essai = WElmer
                print("dbgpy reading the sif file")
                self.essai.initialize()
                pass
            pass
        
    def run(self):
        """
        As steady state, we just need an access to the standard solver
        For a transient simulation, we have to check wether the solver is
        already launched, see the launch method.
        """
        #raw_input(" sim type :"+str(self.simulationType))
        if self.simulationType == "Steady":
            self.launch()
            print(" ////////////////// dbg elmersolver steady //////////////////")
            system("$ELMER_SOLVER test.sif")
            pass
                                                        #
                                                        # we iterate over time
                                                        #
        elif self.simulationType == "Transient":
            print(" ////////////////// dbg elmersolver transient //////////////////")
            self.finalTime = self.times[-1]
            while (self.simulatedTime < self.finalTime) :
                self.oneTimeStep()
                pass
            pass
                
def _vtkGmsh(indGmsh):
    """
        That function is used to treat the vtk / Gmsh dependency (a switch)
    """
    if (indGmsh == 1):
        indVtk = 3
        pass
    elif (indGmsh == 2):
        indVtk = 5
        pass
    elif (indGmsh == 3):
        indVtk = 9
        pass
    elif (indGmsh == 4):
        indVtk = 10
        pass
    elif (indGmsh == 5):
        indVtk = 12
        pass
    elif indGmsh == 6:         # 6-node prism
        indVtk = 13
        pass
    elif indGmsh == 7:         # 5-node pyramid
        indVtk = 14
        pass
    return indVtk

