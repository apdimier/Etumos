# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
import types

import os.path
#
from hydraulicproblem import HydraulicProblem
#
from tensors import Tensor
from listtools import toList
from mesh import *
from numpy import  float as Float
from types import StringType
from hydraulicproblem import HydraulicProblem
from six.moves import range
#
class HydraulicModule:
    """
    The hydraulic module can treat (un)saturated flows. Only one software is relevant: Elmer.
    An unsaturated flow solver (Richards) is running.
    """

    def __init__(self):
        self.calculationTimes = None
        self.density = None
        self.gravity = None
        self.hydraulicPorosity = None
        self.intrinsicPermeability = None
        self.liquidResidualSaturation = None
        self.matrixCompressibilityFactor = None
        self.permeability=None
        self.porosity=None
        self.saturation = "saturated"
        self.simulationType = "Steady"
        self.timeStepIntervals = None
        self.sourceField = None
        self.viscosity = None
    #     
    # All physical parameters relevant to the phenomenology are treated here
    #
    # The hydraulic module can treat saturated flows and
    #
    # in the near future unsaturated flows, transient or steady.
    #
    # Boundary conditions are defined through head or pressure boundary conditions. Nevertheless,
    # they are applied as head boundary conditions
    #
    # module.setData(my_problem, dicobc,dicoic)
    #
    def setData(self, problem,\
                mesh = None,\
                dicobc = None,\
                dicoic = None):

        self.expectedOutput = None
        self.problem = problem
        self.saturation = self.problem.saturation
        if not isinstance(problem, HydraulicProblem):
            raise Exception(" the problem must be an hydraulic problem (SaturatedHydraulicProblem or an unSaturatedHydraulicProblem)")
        self.problemName = problem.getName()
        self.regions = problem.getRegions()
        self.mesh = mesh
                                                                                            #
                                                                                            # Permeability
                                                                                            #
                                                                                            # The permeability is a real for the moment,
                                                                                            # depending only on parameters to be treated
                                                                                            # We introduce here a dictionnary,
                                                                                            # to handle in the near future the "ad hoc" version.
                                                                                            #
        mediumProperties = {
                           "density"                    : None,
                           "gravity"                    : None,
                           "HydraulicConductivity"      : None,
                           "intrinsicPermeability"      : None, 
                           "permeability"               : None, 
                           "viscosity"                  : None,
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
            pass
        else:
            self.simulationType = "Transient"
            pass
        #                        
        self.boundaryConditions = {}
        #                        
        self.initialConditions  = {}
                                                                                            #
                                                                                            # we fill the medium properties dictionnary
                                                                                            #
                                                                                            # Density
        self.density = problem.getDensity()
                                                                                            # Gravity
        self.gravity = problem.getGravity()
        # gravity effect
                                                                                            #viscosity
        self.viscosity = problem.getViscosity()
        #
        for reg in self.regions:
            regionName = reg.support.getBodyName()
            material = reg.getMaterial()
            self.regionProperties[regionName] = mediumProperties

            if not self.problem.saturation:
                permeability = material.getPermeability()
                pass
            else:
                permeability = None
                pass
            hydraulicConductivity = material.getHydraulicConductivity()
            intrinsicPermeability = material.getIntrinsicPermeability()
            self.regionProperties[regionName]["density"]                = self.density
            self.regionProperties[regionName]["gravity"]                = self.gravity
            self.regionProperties[regionName]["HydraulicConductivity"]  = hydraulicConductivity
            self.regionProperties[regionName]["intrinsicPermeability"]  = intrinsicPermeability
            self.regionProperties[regionName]["permeability"]           = permeability
            self.regionProperties[regionName]["viscosity"]              = self.viscosity
#        print self.regionProperties
                                                                                            #
                                                                                            # We treat here the boundary conditions.
                                                                                            # We establish a dictionnary independant from
                                                                                            # the tool to be treated.
                                                                                            #
        boundarySpecification = {
                                "typ"           : None,
                                "head"          : None,
                                "material"      : None,
                                }
        boundaryconditions = problem.getBoundaryConditions()
        from vector import V as Vector
        #
        #
        #
        ind = 0
        for boundarycondition in boundaryconditions:
            #print type(boundarycondition),boundarycondition.__class__.__name__
            #print "debug type value ",boundarycondition.getValue().__class__.__name__
            value = boundarycondition.getValue()
            #print "debug type value ",value.__class__.__name__
            boundaryName = boundarycondition.getSupport().getBodyName()
##            print boundaryName
#            print " cont ",boundarycondition.boundary.support.body[0]
#            print " cont0 ",type(boundarycondition.boundary.support)
#            print type(value)
#            print value.getValue()
#            print boundarycondition.getType()
#            raw_input(" hydraulic module")
            val = value.getValue()
            self.boundaryConditions[ind] = {"head":value.getValue(),\
                                            "typ":boundarycondition.getType(),
                                            "material":boundarycondition.getRegion().getMaterial(),
                                            "boundaryName": boundaryName,
                                            "ind":boundarycondition.getSupport().body[0]
                                           }
            ind+=1
#            self.boundaryConditions[boundaryName]["head"]       = value.getValue()
#            self.boundaryConditions[boundaryName]["typ"]        = boundarycondition.getType()
#            self.boundaryConditions[boundaryName]["material"]   = boundarycondition.getRegion().getMaterial()
#            print "D             ",self.boundaryConditions[boundaryName]
            
#        print self.boundaryConditions
                                                                                            #
                                                                                            # We treat here the initial conditions
                                                                                            #
        initialconditions = problem.getInitialConditions()
        for initialcondition in initialconditions:
#            print " dbg hm ",initialcondition
#            print " dbg hm ",initialcondition.domain.getSupport()
            value = initialcondition.getValue()
            initialConditionName = initialcondition.domain.getSupport().getBodyName()
#            print " dbg hm ",initialConditionName
#            print " dbg hm ",type(value)
#            print " dbg hm ",value
#            raw_input()
            self.initialConditions[initialConditionName] = {   "head":value,\
                                                        "material":initialcondition.getRegion().getMaterial(),
                                                        "ind":initialcondition.getRegion().support.body[0]
                                                    }

                                                                                            #
                                                                                            # We treat here the sources
                                                                                            #

            pass                                                                             
        sourceList = problem.getSource()
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
                                                                                            # We treat outputs: outputs -> list of dictionnary
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
            from elmerhydro import ElmerHydro
            if (self.componentName!="elmer"):
                self.componentName == "elmer"
                self.flowComponent = ElmerHydro(self.mesh) # by default the problem is set to saturated
                if (self.timeStepIntervals == None and self.calculationTimes != None):
                    self.timeStepIntervals = len(self.calculationTimes)-1
                    self.timeStepSizes = [self.calculationTimes[i+1]-self.calculationTimes[i] for i in range(len(self.calculationTimes)-1)]
                self.flowComponent.setTimeDiscretisation(self.timeStepIntervals, self.timeStepSizes)
                self.flowComponent.setSimulationKind(self.simulationType)
                raise Warning(" the default hydraulic has been fixed to elmer"+\
                ", other hydraulic tools should be introduced in the near future")
            else:
                self.componentName == "elmer"
                self.flowComponent = ElmerHydro(self.mesh, self.saturation)
                if (self.timeStepIntervals == None and self.calculationTimes != None):
                    self.timeStepIntervals = len(self.calculationTimes)-1
                    self.timeStepSizes = [self.calculationTimes[i+1]-self.calculationTimes[i] for i in range(len(self.calculationTimes)-1)]
                elif (self.timeStepIntervals != None):
                    self.flowComponent.setTimeDiscretisation(self.timeStepIntervals, self.timeStepSizes)
                self.flowComponent.setSimulationKind(self.simulationType)
                print(" the flow component has been set")
                pass
                
        else:
            raise Warning(" the default hydraulic has been fixed to elmer ")
            self.componentName = "elmer"
            pass
        #
        #
        #
#        print "dbg setBodyList"
        self.flowComponent.setBodyList(self.problem.getRegions())
        #
        #
        #
#   print " dbg hm we set the bic ",self.boundaryConditions
        self.flowComponent.setBoundaryConditions(self.boundaryConditions)
                                                                                                                #
                                                                                                                # Density
                                                                                                                #
#        print " self.flowComponent",self.flowComponent
#        raw_input()
        if self.density: self.flowComponent.setDensity(self.density)
        #
        #
        #
#   print " dbg hm we set the ic "
        self.flowComponent.setInitialConditions(self.initialConditions)
                                                                                                                #
                                                                                                                # Gravity
                                                                                                                #
        if self.gravity:
#       print " dbg hm we set the gravity "
            self.flowComponent.setGravity(self.gravity)
            pass
                                                                                            #
                                                                                            # Permeability
                                                                                            #
        if self.permeability:
            self.flowComponent.setPermeability(self.permeability)
            pass
                                                                                            #
                                                                                            # Intrinsic Permeability
                                                                                            #
        if self.intrinsicPermeability:
            self.flowComponent.setIntrinsecPermeability(self.intrinsicPermeability)
            pass       
                                                                                            #
                                                                                            # Porosity
                                                                                            #
        if self.hydraulicPorosity:
            self.flowComponent.setPorosity(self.hydraulicPorosity)
            pass
        elif self.porosity:
            self.flowComponent.setPorosity(self.porosity)
            pass
                                                                                            #
                                                                                            # Viscosity
                                                                                            #
        if self.viscosity:
            self.flowComponent.setViscosity(self.viscosity)
            pass
                                                                                            #
                                                                                            # Matrix compressibility factor
                                                                                            #
        if self.matrixCompressibilityFactor:
            self.flowComponent.setMatrixCompressibilityFactor(self.matrixCompressibilityFactor)
            pass

        if self.liquidResidualSaturation:
            self.flowComponent.setLiquidResidualSaturation(self.liquidResidualSaturation)
            pass
                                                                                            #
                                                                                            # Source
                                                                                            #
        if self.sourceField :
            self.flowComponent.setSource(self.sourceField)
            pass
                                                                                            #
                                                                                            # time steps treatment
                                                                                            #
        if self.simulationType == "Transient":
            self.flowComponent.calcTimesDico ['finalTime']= self.problem.calculationTimes[-1]
            pass
        #
        #setExpectedOutput
        #
#        Module.setExpectedOutput(self)
                                                                                            #       
                                                                                            # to affect numerical parameters
                                                                                            #
    def setParameter(self,*tuple,**dico):
        if self.flowComponent:
            self.flowComponent.setParameter(*tuple,**dico)
            pass
        else:
            raise Exception(" You have to set the Hydraulic component solver")
                                                                                            #       

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
#            raw_input(" trying to retrieve charge")
            
            self.charge = self.flowComponent.essai.getCharge()
            print(self.charge[0:10])
#            raw_input(" trying to retrieve points")
            self.points = self.flowComponent.essai.getCoordinates()
            self.points = self.mesh.getNodesCoordinates()
            #print self.points
#            raw_input(" trying to retrieve velocity")
            self.velocity = self.flowComponent.essai.getVelocity()
            return self.points, self.charge, self.velocity
        #
        # steady part
        #
        #print " we re here "
        #raw_input()
        if type(name) == StringType:
            if name.lower() == "velocity":
                fileName = "./" + self.flowComponent.meshDirectoryName + "/" + "HeVel.ep"
                if not os.path.isfile(fileName):
                    message = " problem with the velocity file: " + fileName
                    raise Exception(message)
                    return None
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
                #print " line ",line
                #raw_input("line : ")
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
            pass
#        print charge[0],charge[-1]
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
        
    def run(self,transient = None):
        """
        Simulation, steady or transient;
        The default flow solver is elmer.
        The simulation is supposed to be a steady one by default.
        """
        if self.flowComponent == None:
            #
            # is it possible ?
            #
            self.flowComponent = ElmerHydro(self.mesh)
            pass
        if not transient:
            #raw_input(" running elmer ")
            self.flowComponent.run()
            pass
        else:
            self.flowComponent.launch()
            #dir(self.flowComponent)
            self.flowComponent.run()
            pass
        
    def setInitialPermeability(self,permeabilityField):
        """
        That function is used to set the initial permeability field.
        """
        if self.flowComponent != None:
            self.flowComponent.setpermeabilityfield(permeabilityField)
            pass
        else:
            raise Exception(" the flow component must be launched before trying to setup K ")
        
    def writeVelocityPlot(self):
        """
        The velocity is plotted using the legacy format of vtk
        """
        name = "velocity.vtk"
        chargeFile = open(name,'w')
        chargeFile.write("%s\n"%("# vtk DataFile Version 2.0"))
        chargeFile.write("%s\n"%("obtained via hydraulicmodule"))
        chargeFile.write("%s\n"%("ASCII"))
        chargeFile.write("%s\n"%("DATASET UNSTRUCTURED_GRID"))
        chargeFile.write("%s %i %s\n"%("POINTS",len(self.points),"double"))
        dim = self.mesh.getSpaceDimensions()
        if (dim==2):        
            for ind in range(0,len(self.points)):
                chargeFile.write("%15.8e %15.8e %15.8e\n"%(self.points[ind][0],\
                                                           self.points[ind][1],\
                                                           0.))
                pass
            pass
        elif (dim==3):  
            for ind in range(0,len(self.points)):
                chargeFile.write("%15.8e %15.8e %15.8e\n"%(self.points[ind][0],\
                                                           self.points[ind][1],\
                                                           self.points[ind][2]))
                pass
            pass
        else:
            raise Exception(" error in mesh dimension ")       
        numberOfCells = self.mesh.getNumberOfCells()
        connectivity = self.mesh.getConnectivity()

        cellListSize = 0
        for i in range(0,numberOfCells):                # gmsh meshes: type of elements
            gmshType = connectivity[i][1]
            if gmshType == 1:                           # 2-node line
                cellListSize += 3
                pass
            elif gmshType == 2:                         # 3-node triangles
                cellListSize += 4
                pass
            elif gmshType == 3:                         # 4-node quadrangles
                cellListSize += 5
                pass
            elif gmshType == 4:                         # 4-node tetrahedron
                cellListSize += 5
                pass
            elif gmshType == 5:                         # 8-node hexahedrons
                cellListSize += 9
                pass
            pass
        chargeFile.write("CELLS %i %i\n"%(numberOfCells,cellListSize))
        ind = 0
        for cell in connectivity:
            ind = cell[2]+3
#               print " ctm dbg cell ",vtkTyp,ind,cell," perm ",permutation[ind],permutation[ind+1],permutation[ind+2],permutation[ind+3]
                    # 
            vtkTyp = _vtkGmsh(cell[1])
            if (vtkTyp==3):                                                                                     # 2-node line
                ind = cell[2]+3
                chargeFile.write("%i %i %i\n"%(
                               2,\
                               cell[ind]-1,\
                               cell[ind+1]-1)
                              )
                pass
                
            elif (vtkTyp==5):                                                                                   # triangles
                chargeFile.write("%i %i %i %i\n"%(
                                 3, 
                                 cell[ind]-1,\
                                 cell[ind+1]-1,\
                                 cell[ind+2]-1)
                                )
                pass
            elif (vtkTyp==9):                                                                                   # quadr
                chargeFile.write("%i %i %i %i %i\n"%(
                                 4,\
                                 cell[ind]-1,\
                                 cell[ind+1]-1,\
                                 cell[ind+2]-1,\
                                 cell[ind+3]-1)
                                )
                pass
            elif (vtkTyp==10):                                                                                  # tetra
                chargeFile.write("%i %i %i %i %i\n"%(
                                 4,\
                                 cell[ind]-1,\
                                 cell[ind+1]-1,\
                                 cell[ind+2]-1,\
                                 cell[ind+3]-1)
                                )
                pass
            elif (vtkTyp==12):                                                                                  # hexahedron
                chargeFile.write("%i %i %i %i %i %i %i %i %i\n"%(
                                 8,\
                                 cell[ind]-1,\
                                 cell[ind+1]-1,\
                                 cell[ind+2]-1,\
                                 cell[ind+3]-1,\
                                 cell[ind+4]-1,\
                                 cell[ind+5]-1,\
                                 cell[ind+6]-1,\
                                 cell[ind+7]-1)
                                )
                pass
            pass
        chargeFile.write("%s %i\n"%("CELL_TYPES",numberOfCells))
#
        for i in range(0,numberOfCells):
            gmshType = connectivity[i][1]

            if (gmshType)==1:
                cellTyp = 3
                pass
            elif (gmshType)==2:
                cellTyp = 5
                pass
            elif (gmshType)==3:
                cellTyp = 9
                pass
            elif (gmshType)==4:
                cellTyp = 10
                pass
            elif (gmshType)==5:
                cellTyp = 12
                pass
            elif (gmshType)==6:
                cellTyp = 13
                pass
            elif gmshType == 7:
                cellTyp = 14
                pass
            else:
                raise Exception(" check gmshtype ")
        chargeFile.write("%i\n"%(cellTyp))
        chargeFile.write("%s %d\n"%("POINT_DATA",len(self.points)))
        chargeFile.write("%s\n"%("VECTORS vectors float"))
        for velocityComponent in self.velocity:
            chargeFile.write(" %e %e %e\n "%(velocityComponent[0], velocityComponent[1], velocityComponent[2]))
        chargeFile.write("%s\n"%("SCALARS charge double"))
        chargeFile.write("%s\n"%("LOOKUP_TABLE default"))
#
        
        chargeDataFile=open("./" + self.flowComponent.meshDirectoryName + "/" + "HeVel.dat",'r')
        line = chargeDataFile.readline()
        while "Number Of Nodes" not in line:
            line = chargeDataFile.readline()
#line.split()
        nodesNumber = line.split()[-1]
        while "Perm" not in line:
            line = chargeDataFile.readline()
#
# We read the permutation
#
        for i in range(int(nodesNumber)): chargeDataFile.readline()
#
# We read the charge
#
        for i in range(int(nodesNumber)): chargeFile.write(" %15.10e\n "%(float(chargeDataFile.readline())))

        
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

