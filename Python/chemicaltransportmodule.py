# -*- coding: utf-8 -*-
"""
        A chemical problem being defined with all necessary data, 
        the algorithm over time is established here depending on the software
        to be previous defined by the user:
        
        for flow and transport: 
        
                        modflow/ mt3d and elmer ( openfoam wrapping is currently under dev.)
                        
        for chemistry:
        
                        phreeqC
                        
       Flow initial and boundary conditions are associated to the problem in order to enable a transient flow problem ( porosity variation ...)
       It means that the material should entail hydraulic properties
       
       Rem: the average fluid velocity within the pores, called the seepage velocity, is the Darcy velocity divided by
       the effective porosity of the medium

"""
# 
# A chemical problem being defined, its realization is defined here
# 
import os, resource

from memory import getMemory

from listtools import addLists, extractIndex, normL1

from copy import * 

from numpy import array, concatenate, float, int, ravel, reshape, finfo

import numpy

from fields import  InstanceBodyField,\
                    NumericBodyField
                    
from tensors import IsotropicTensor,Tensor
                             
from cartesianmesh import CartesianMesh

from chemicaltransport  import  ChemicalTransportProblem, CoupledOutput

from chemistry import   ChemicalProblem,\
                        ElementConcentration,\
                        KineticLaw,\
                        ChemicalState,\
                        ExpectedOutput

from FortranFormat import FortranFormat, FortranLine

from generictools import color,\
                         GenericCTModule,\
                         isInstance,\
                         listTypeCheck

from inspect import currentframe

from os import environ

from phreeqc import Phreeqc

from physicallaws import EffectiveDiffusionLaw,\
                         ExpDiffusionLaw,\
                         LinearDiffusionLaw,\
                         MeanThermalConductivityLaw,\
                         ProportionalDiffusionLaw,\
                         WinsauerDiffusionLaw

try:
    from toughreact import ToughReact
except:
    print "toughreact is not available here"
#
# mpi4py
#
from mpi4py import MPI
#from mpoints import AbstractPoint

from timespecification import TimeSpecification

from types import FloatType, IntType, ListType, StringType

from species import Species

from posttables import Table

from chemicalmodule import Chemical

from _chemicaltransportmodule_tools import fixedpoint_source,init_conc_porosity_cst,\
                                           init_conc_porosity_var, init_porosity,\
                                           residualEvaluation, residualEvaluation_level_2,\
                                           residualEvaluation_level_3
    
from PhysicalProperties import Velocity
from PhysicalQuantities import Time

import wx

import wx.lib.plot as plot

import threading,sys

import thread

from gnade import TestFrame

from etuser import *

from vtkxml import XmlVtkUnstructured

from xml.dom.minidom import Document

import subprocess

import platform
#from drahtplot import *
# Needs Numeric or numarray or NumPy
try:
    import numpy.oldnumeric as _Numeric
except:
    try:
        import numarray as _Numeric  #if numarray is used it is renamed Numeric
    except:
        try:
            import numpy as _Numeric
        except:
            msg= """
            This module requires the numpy/numarray or NumPy module,
            which could not be imported.  It is probably not installed
            (it's not part of the standard Python distribution). See the
            Numeric Python site (http://numpy.scipy.org) for information on
            downloading source or binaries."""
            raise ImportError, "numpy, numarray or NumPy not found. \n" + msg

_fe158 = FortranFormat("E15.8")
def _fote158(arg):
    return str(FortranLine([arg],_fe158))

class Plot(wx.Dialog):
        """
        plot
        """
        def __init__(self, parent, id, title):
            wx.Dialog.__init__(self, parent, id, title, size=(180, 280))

            self.data = [(1,2), (2,3), (3,5), (4,6), (5,8), (6,8), (10,10)]
            btn1 = wx.Button(self,  1, 'scatter', (50,50))
            btn2 = wx.Button(self,  2, 'line', (50,90))
            btn3 = wx.Button(self,  3, 'bar', (50,130))
            btn4 = wx.Button(self,  4, 'quit', (50,170))
            wx.EVT_BUTTON(self, 1, self.OnScatter)
            wx.EVT_BUTTON(self, 2, self.OnLine2)
            wx.EVT_BUTTON(self, 3, self.OnBar)
            wx.EVT_BUTTON(self, 4, self.OnQuit)
            wx.EVT_CLOSE(self, self.OnQuit)
            pass

        def OnScatter(self, event):
            frm = wx.Frame(self, -1, 'scatter', size=(600,450))
            client = plot.PlotCanvas(frm)
            markers = plot.PolyMarker(self.data, legend='', colour='pink', marker='triangle_down', size=1)
            gc = plot.PlotGraphics([markers], 'Scatter Graph', 'X Axis', 'Y Axis')
            client.Draw(gc, xAxis=(0,15), yAxis=(0,15))
            frm.Show(True)
            pass

        def OnLine(self, event):
            frm = wx.Frame(self, -1, 'line', size=(600,450))
            client = plot.PlotCanvas(frm)
            line = plot.PolyLine(self.data, legend='', colour='pink', width=5, style=wx.DOT)
            gc = plot.PlotGraphics([line], 'Line Graph', 'X Axis', 'Y Axis')
            client.Draw(gc,  xAxis= (0,15), yAxis= (0,15))
            frm.Show(True)
            pass

        def OnLine2(self, event):
            toto = TestFrame(None, -1, "Gnade")
            line = plot.PolyLine(self.data, legend='', colour='pink', width=5, style=wx.DOT)
            gc = plot.PlotGraphics([line], 'Line Graph', 'X Axis', 'Y Axis')
            toto.client.Draw(gc,  xAxis= (0,15), yAxis= (0,15))
            toto.Show(True)
            pass

        def OnBar(self, event):
            frm = wx.Frame(self, -1, 'bar', size=(600,450))
            client = plot.PlotCanvas(frm)
            bar1 = plot.PolyLine([(1, 0), (1,5)], legend='', colour='gray', width=25)
            bar2 = plot.PolyLine([(3, 0), (3,8)], legend='', colour='gray', width=25)
            bar3 = plot.PolyLine([(5, 0), (5,12)], legend='', colour='gray', width=25)
            bar4 = plot.PolyLine([(6, 0), (6,2)], legend='', colour='gray', width=25)
            gc = plot.PlotGraphics([bar1, bar2, bar3, bar4],'Bar Graph', 'X Axis', 'Y Axis')
            client.Draw(gc, xAxis=(0,15), yAxis=(0,15))
            frm.Show(True)
            pass

        def OnQuit(self, event):
            self.Destroy()
            pass

class MyApp(wx.App):
    """
    essai
    """
    def OnInit(self):
        dlg = Plot(None, -1, 'plot.py')
        dlg.Show(True)
        dlg.Centre()
        return True

class IGPlot:
    """
    Initially for use to plot in an interactive manner
    replaced by gnuplot 
    """
    def __init__(self):
#        self.tPlot = threading.Thread(args=())
#   self.tPlot.setName("Gnade")
#   self.tPlot.setDaemon(1)
#   print "methodes ",dir(self.tPlot)
        self.title = "Gnade: interactive plot"
        self.legend = [""]
        self.xmin = -1
        self.xmax = 11
        self.ymin = -1
        self.ymax = 10
        self.keepGoing = True
        self.farben = ["red","green","orange","blue","yellow"]
        return None

    def setData(self,data):
        self.data = data
        return None

    def setXBounds(self,xmin,xmax):
        self.xmin = xmin
        self.xmax = xmax
        return None

    def setYBounds(self,ymin,ymax):
        self.ymin = ymin
        self.ymax = ymax
        return None

    def setTitle(self,title):
        self.title = title
        return None

    def setLegend(self,legend):
        """
        A list of denominationstrings based on the output
        """
        self.legend = legend
        return None

    def start(self):
        print " Draht start ";#sys.stdout.flush()
#        self.tPlot.start()
        self.keepGoing = True
        return None     

    def stop(self):
        print " Draht stop ";#sys.stdout.flush()
        self.wxapp.tf.Close()
        return None
    
    def init(self):
        self.wxapp = wx.App(False)
        self.wxapp.tf = TestFrame(None, -1, "Gnade")
        self.wxapp.tf.resetDefaults()
    def run(self):
        self.wxapp.tf.resetDefaults()
#    line1 = PolyLine(points1, legend='quadratic', colour='blue', width=1)
#    line2 = PolyLine(points2, legend='cubic', colour='red', width=1)
#    return PlotGraphics([line1,line2], "double log plot", "Value X", "Value Y")
        print " legend",self.legend,type(self.legend[0]);#sys.stdout.flush()
        print " xmin, xmax ",self.xmin,self.xmax;#sys.stdout.flush()
        #raw_input("yes ")
        kurven = []
        ind = 0
        for i in self.data:
            line = plot.PolyLine(i, legend=self.legend[0], colour=self.farben[ind%len(self.farben)], width=5, style=wx.DOT)
            kurven.append(line)
            ind+=1
            pass
        gc = plot.PlotGraphics(kurven, self.title, 'X Axis(m)', 'Y Axis (mol/l)')
        self.wxapp.tf.client.Draw(gc,  xAxis= (self.xmin,self.xmax), yAxis= (self.ymin,self.ymax))
        self.wxapp.tf.Show(True)
        self.wxapp.SetTopWindow(self.wxapp.tf)
    
        return None
        
    def igexit(self):
        self.wxapp.Destroy()
               
    def isAlive(self):
        return self.tPlot.isAlive()       
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class ChemicalTransportModule
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import cPickle as pickle                                                                   # to convert a Python object hierarchy into a byte stream

class ChemicalTransportModule(GenericCTModule):
    """
    That module is used to couple phreeqC to Elmer or Mt3d. For the moment
    it is using a Darcy flow and enables to use a non iterative, NI, or an
    iterative algorithm, a CC algorithm.
    
    Forseen:
    
        Implement a TC or a TT algorithm while using totals structures of phreeqC 
    """
    def __init__(self) :
        """
        
        """
        GenericCTModule.__init__(self)
        
        self.bodyPorosities = None
        self.times = None                                                                    # specification of times, printout gen.
        self.curveTable = None
        self.darcyVelocity  = None

        self.dispersivityBody = None      
        self.effectiveDiffusionZone = None
        self.expectedOutputs = None
        self.initialTimeStep = None
        self.interactivePlot = None
        #
        self.mpiEnv = None
        #
        self.seepageVelocity = None
        self.userPermeability = False

        self.timeBoundaryConditionVariation = None


        self.imposedComputationTimes = []

        self.couplingPrecision  = 1.E-5
        self.decreaTimeStepCoef = 0.8
        self.increaTimeStepCoef = 1.25
        self.maxIterationNumber = 50
        self.optimalIterationNumber  = 20.

        self.chat = 0
        #
        # the two components to be used for coupling
        #
        self.chemicalSolver = None
        self.transportSolver = None
        #
        self.chemicalParameters = []
        #
        self.initFlagControl = None
        self.initialisationOption      = 1
        self.oldDT = None
        #
        # used to control the mesh expansion for one dimensional problems
        #  
        #
        self.oneDimensionalExpansion = "x"
        self.oscControl = ""
        #
        #
        #
        self.convergenceCriterionLevel = 1
        #
        # to be used for control on transport ( to be developped)
        #
        self.listOfNodes = []

        self.minValue = -1.e+2
        self.maxvalue =  1.e+2
        #
        # userProcessing is set to None and eventually updated via he problem
        #
        self.userProcessing = None
        self.boundPlot      = []

        return None

    def setData(self, problem,\
                unstructured = None,\
                trace = None,\
                mesh = None,\
                algorithm = None,\
                coupledOutputs = None,\
                coupledInputs = None):

        if not isinstance(problem, ChemicalTransportProblem):
            #print " problem class name ",problem.__class__.__name__
            if problem.__class__.__name__ != "THMCProblem" and problem.__class__.__name__ != "ChemicalTransportProblem":
                print problem.__class__.__name__
                raise Exception, "\n    the problem instantiation must be verified;\n"+\
                             "    the problem should be a chemical transport or\n"+\
                             "    a chemical mechanical transport problem"
                             
        self.problem = problem

        self.mpiEnv = self.problem.getMPIEnv()
        #print " ctm dbg mpiEnv: ", self.mpiEnv; #sys.stdout.flush()
        #raw_input("mpienv")
        if (self.mpiEnv != None):
            #self.communicator = MPI.world.duplicate()
            self.communicator = MPI.COMM_WORLD.Dup()
                                                                                            #
                                                                                            # the number of processors
                                                                                            # is fixed by the environment,
                                                                                            # It could be fixed by
                                                                                            # the problem via mpiSize
                                                                                            #        
            self.mpiSize = MPI.COMM_WORLD.Get_size()
            self.rank    = MPI.COMM_WORLD.Get_rank()

            print " the simulation is //, the communicator is launched on %s processors"%self.mpiSize;#sys.stdout.flush()
            pass
        else:
            environ["NO_MPI"] = "NO_MPI"
            pass
        #
        if mesh: self.mesh = mesh
        #
        if unstructured==None: 
            try:
                if mesh!=None:
                    if mesh.getMeshType() == "unstructured": unstructured = 1
            except Warning: " you have to define a mesh for the problem"

        self.value = [] 
        self.name = problem.getName()
        self.regions = problem.getRegions()

        self.boundaryConditions = problem.getBoundaryConditions()

        self.initialConditions = problem.getInitialConditions()

        self.times = problem.getCalculationTimes()
        self.finalTime = self.times[-1]
        if len(self.times) > 2:
            self.simTimesList = 1
            pass
        else:
            self.simTimesList = 0
            pass
        self.sources = problem.getSources()
        #
        # porosity is a function of chemistry
        #
        # The darcy velocity varies with permeability considered as a
        # function of porosity. The porosity variation should induce a  source term. That source term is not considered.
        #
        # We get the Darcy velocity here. 
        # The algorithm enabling a variable Darcy velocity is placed out of that
        # module to enable a better lecture of the whole. The function oneTimeStep
        # enables that way of programming.
        #
        #
        self.darcyVelocity = problem.getDarcyVelocity()
        #
        self.chemistryDB = problem.getChemistryDB()
        self.speciesBaseAddenda = problem.getSpeciesBaseAddenda()

        self.kineticLaws = problem.getKineticLaws()
        self.activityLaw = problem.getActivityLaw()
        self.temperature = problem.getThermalOption()

        self.timeUnit = problem.getTimeUnit()
        if self.timeUnit==None: self.timeUnit = 's'                                         # the time unit is set to seconds
        self.variablePorosityOption = problem.getBooleanPorosityOption()
        self.HeadVPorosityOption = problem.getVariableHeadPorosityOption()
        self.diffusionLaw = problem.getDiffusionLaw()
        self.permeabilityLaw = problem.getPermeabilityLaw()
        
        # Check all expectedoutputs outputs for
        #  * detect the files to save
        #  * construct the imposed computation times
        #  * construct the outputs dictionnary
        self.save_tab_file = 0
        if problem.getOutputs():
            self.expectedOutputs = problem.getOutputs()
            for output in problem.getOutputs():
                quantity = output.getQuantity().lower()
                if (quantity == 'numerics'):
                    tableName = "numeric behaviour"
                    self.outputs[output.getName()] = Table(name = tableName,column_titles = ['time','time iteration',\
                                                                 'time step','nb iteration','final error'])
                    pass
                else:
#                    if isinstance(output.getSupport(),AbstractPoint):
#                       if len(output.getSupport().getCoordinates())==2:
#                            name = "%s at point (%8.2e, %8.2e) "\
#                                   %(output.getName(),
#                                     output.getSupport().getCoordinates()[0],
#                                     output.getSupport().getCoordinates()[1])
#                        else:
#                            name = "%s at point (%8.2e, %8.2e) "\
#                                   %(output.getName(),
#                                     output.getSupport().getCoordinates()[0],
#                                     output.getSupport().getCoordinates()[1],
#                                     output.getSupport().getCoordinates()[2])
#                            
#                            pass
#                        self.outputs[output.getName()] = Table(name,['time',output.getName()])
#                        pass
                    if output:
#                    else:                                        
                        if (output.getSave() == 'file'):
                            if (output.getFormat() == 'field'):
                                pass
                            pass
                        else:
                            self.outputs[output.getName()] = []                         
                            pass
                        pass
                    if output.getTimeSpecification():
                        if (output.getTimeSpecification().getSpecification()=='times'):
                            times = output.getTimeSpecification().getTimes()
                            self.addImposedComputationTime(times)
                            pass
                        pass                    
                    if (quantity not in ['porosity','diffusion','volume','temperature']):
                        self.addChemicalOutputs(output)
                        pass

                    pass
                pass
            # erase the tab ouput field if exist 
            file = self.problem.getName() + '.tab'
            if os.path.exists(file):
                os.remove(file)
                pass
            pass

        # Check all coupledOuputs
        self.coupled_outputs_dict = {}
        if coupledOutputs:
            for output in  coupledOutputs:
                self.coupled_outputs_dict[output.getName()] = output 
                quantity = output.getQuantity().lower()
                if (quantity not in ['porosity','diffusion','volume','temperature']):
                    self.addChemicalOutputs(output)
                    pass
                pass
            pass
        #
        # We take here the user processing into account
        #
        self.userProcessing = self.problem.getUserProcessing()
        if self.userProcessing:
            self.processingList = self.problem.getProcessingList()

            exec("userList(self)")
        #
        # User processing is over
        #
        if trace:
            if type(trace) != IntType:
                trace = 0
                raise Warning, " trace has been set to zero, it should be an integer "
        self.trace = trace
 
        if type(algorithm) is StringType:
            self.couplingAlgorithm = algorithm.upper()
            if self.couplingAlgorithm not in ["CC","NI"]: self.couplingAlgorithm = "NI"
            pass
        else:
            self.couplingAlgorithm = "NI"
            pass

        print unstructured;#raw_input("value of the unstructured parameter ")
        if unstructured :

            self.bodies = [region.getSupport() for region in self.regions]
            #
            # Now we will work on the physical properties
            #
            dispersivityBoolean = 0
            porosityBoolean = 0
            effectiveDiffusionBoolean = 0

            bodyPorosities =  NumericBodyField('porosity', self.mesh,['poro'], float)
            
            if self.temperature:
                thermalConductivityZone = InstanceBodyField('thermalconductivity',  self.mesh, type = Tensor)
                self.thermalDelayedFactor_zone = NumericBodyField('thermaldelayedfactor',  self.mesh, ['phirt'], float)
                pass
            print "\neffective_diffusion:\n";#sys.stdout.flush()
            
            effective_diffusion_zone = InstanceBodyField('diffusion', self.mesh,type = Tensor)
            
            dispersivityBody = NumericBodyField('dispersivity', self.mesh,['alphal','alphat'], float)
            
            for region in self.regions:
                material = region.getMaterial()
                zone = region.getSupport()
                #print "\nporosity\n";#sys.stdout.flush()
                materialPorosityValue = material.getPorosity()

                #print "\neffective diffusion\n";#sys.stdout.flush()
                effectiveDiffusion = material.getEffectiveDiffusion()
                dispersivity       = material.getKinematicDispersion()
                #print "\neffective diffusion\n",effectiveDiffusion;#sys.stdout.flush()
            
                if materialPorosityValue:
                    bodyPorosities.setZone(zone,materialPorosityValue.getValue(),material.getName())
                    porosityBoolean = 1
                    pass
                if effectiveDiffusion:
                    component_number_ediff = effectiveDiffusion.getValue().getNbComponents()
                    names_list = []
                    for i in range(component_number_ediff):
                        names_list.append('ed'+str(i))
                        pass
                    effective_diffusion_zone.setComponentsNames(names_list)
                    effective_diffusion_zone.setZone(zone,
                                                     effectiveDiffusion.getValue(),
                                                     material.getName())
                    effectiveDiffusionBoolean = 1
                    pass
                if self.temperature:
                    heatCapacity_value   = material.getSpecificHeat() 
                    thermalConductivityTensor = material.getThermalConductivity()
                    #kinematicDispersion = material.getKinematicDispersion()
                    if thermalConductivityTensor:
                        thermal_conductivity_names = []
                        for i in range(thermalConductivityTensor.getValue().getNbComponents()):
                            thermal_conductivity_names.append('thc'+str(i))
                        #thermalDiffusivity  = $\lambda^{\prime}_{eff}$
                        phi      = materialPorosityValue.value
                        lambda_s = thermalConductivityTensor.value.getValues()
                        lambda_l = self.problem.fluidThermalConductivity
                        rho_cp_f = self.problem.waterVolHCapacity
                        thermalDiffusivity = IsotropicTensor(((1-phi)*lambda_s + phi*lambda_l)/(phi*rho_cp_f))
                        #thermalDelayedFactor = $\phi R_T$
                        rho_cp_s = heatCapacity_value.getValue()
                        thermalDelayedFactor  =  phi + (1-phi)*(rho_cp_s/rho_cp_f)

                        thermalConductivityZone.setComponentsNames(thermal_conductivity_names)
                        thermalConductivityZone.setZone(zone,
                                                        thermalDiffusivity,
                                                        material.getName())
                        self.thermalDelayedFactor_zone.setZone(zone, thermalDelayedFactor, material.getName())
                    pass
                if dispersivity:

                    dispersivityBody.setZone(   zone,
                                                dispersivity.getValue(),
                                                material.getName())
                    dispersivityBoolean = 1
                    pass
                pass
            #print "ctm dbg out of region loop:",region.support.physicalName;#sys.stdout.flush()
            
            if porosityBoolean: self.bodyPorosities = bodyPorosities                        # body porosities

            if effectiveDiffusionBoolean:
                self.effectiveDiffusionZone = effective_diffusion_zone
                pass
            if self.temperature:
                self.thermalConductivityZone = thermalConductivityZone
                pass
            if dispersivityBoolean:
                self.dispersivityBody = dispersivityBody
                pass
                                                                                            #
                                                                                            # We control here the fact that the mesh is
                                                                                            # one dimensional for a wellbore analysis
                                                                                            #
        if self.problem.wellbore == True:
            if self.mesh.spaceDimensions != 1:
                raise Warning, "the mesh dimension should be one."
            
        return None
        
    def setComponent(self,TransportComponent,ChemicalComponent,Memory=None):
        """
        Enables to enter the tools to be used in the algorithm
        """
        self.TransportComponent = TransportComponent.lower()
        print " self transportcomponent",self.TransportComponent, "mpiEnv",self.problem.mpiEnv
        if (self.problem.mpiEnv == None):
            if (self.TransportComponent == "mt3d"):
                #
                # checking the availability of Mt3D
                #
                try:
                    from mt3d import Mt3d
                    self.transportSolver = Mt3d()
                except ImportError:
                    Mt3d = None
                    pass
                pass
            elif (self.TransportComponent.lower() == "elmer"):
                #
                # checking the availability of Elmer
                #
                try:
                    #print " within the try "
                    #raw_input("ctmdbg trying to load elmer")
                    import elmer
                    dir(elmer)
                    from elmer import Elmer
                    self.transportSolver = Elmer(self.mesh)
                    #print dir(Elmer);sys.stdout.flush()
                    #print "tyyyyyyyyyyyyyyyyyyyyyyyyy",type(self.mesh)
                    #raw_input()
                except ImportError:
                    Elmer = None
                    raise Exception, " unable to load Elmer "
                pass
                                                                                            #
                                                                                            # temperature
                                                                                            #
                if self.temperature:
                    print "dbg ctm 662 setTemperature"
                    self.transportSolver.setTemperature()
                    pass
                                                                                            #
                                                                                            # porosity
                                                                                            #
                self.transportSolver.setPorosityState( self.problem.getPorosityOption())
                pass
                
            elif (self.TransportComponent.lower() == "openfoam"):
                pass
                
            else :       
                raise RuntimeError(self.TransportComponent+" transport tool doesn't exist")
        elif (self.problem.mpiEnv != None):
            print "mpiEnv\nmpiEnv\nmpiEnv\nmpiEnv\nmpiEnv\nmpiEnv\nmpiEnv\n"
            if self.communicator.rank == 0:
                if (self.TransportComponent == "mt3d"):
                # Do a try for computer without f90
                    try:
                        from mt3d import Mt3d
                        self.transportSolver = Mt3d()
                    except ImportError:
                        Mt3d=None
                        pass
                    pass
                elif (self.TransportComponent =='elmer'):
                    print " ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ "
                    print " we launch the elmer transport solver ",self.communicator.rank
                    print " ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ "
                    from elmer import Elmer
                    self.transportSolver = Elmer(self.mesh)
                    print " elmer transport solver launched"
                    pass
                if self.temperature:
                    pass
                else :       
                    raise RuntimeError(self.TransportComponent+" transport tool doesn't exist")
        else :       
            raise RuntimeError(self.TransportComponent+" transport tool doesn't exist")
        self.transport = self.transportSolver
        #
        # here we use the transport solver for heat; in the scrips, it will appear
        # as module.heat to provide a better consistancy to the user.
        #
        if self.temperature:
            self.heat = self.transportSolver
        #
        # in the case of a flow treatment
        #
        self.flow()
        #
        self.ChemicalComponent = ChemicalComponent.lower()
        self.internalNodesNumber = 0   
        if (self.problem.mpiEnv == None):
            if (self.ChemicalComponent.lower() == "phreeqc"):
                self.chemicalSolver = Phreeqc()
                self.chemicalSolver.setChat(self.trace)
                pass
            elif (self.ChemicalComponent.lower() == "toughreact"):
                self.chemicalSolver = ToughReact()
                pass
            pass
        else:
            self.chemicalSolver = Phreeqc(self.mpiSize,self.communicator.rank)
            self.chemicalSolver.setChat(self.trace)
            pass
    
        self.chemical = self.chemicalSolver
                                                                                            # we set the mesh
        if (self.problem.mpiEnv == None):
            if (self.TransportComponent == 'elmer'):
                self.transport.setMesh(self.mesh)
                pass
            pass
        elif self.communicator.rank == 0:
            print self.transport
            if (self.TransportComponent == 'elmer'):
                self.transport.setMesh(self.mesh)
                pass
            pass

        return None
        
    def flow (self):
        """
        method used to enable a better lecture of the python script for the user
        """
        self.flow = self.transport
        
    def setTransportParameter(self,*args):
        """
        Used to enter transport solver parameters
        """
        if self.transportSolver:
            self.transportSolver.setParameter(*args)
            pass
        else:
            raise "You have to define the transport tool to be used before setTransportParameter"
        return None

    def setElmerTransportParameter(self, **solverparameterdict):
        """
        Here the parameters of the algebraic solver are introduced
        """
        #print "ctmdbg setElmerTransportParameter"
        self.elmerSolverDico = {}
        for key, value in solverparameterdict.items():
            if key == "accelerator":
                self.elmerSolverDico["Linear System Iterative Method"] = value
                pass
            if key == "algebraicResolution":
                self.elmerSolverDico["algebraicResolution"] = value
                pass
            if key == "BDFOrder" or key == "BDFO" or key.upper() == "BDF":
                self.elmerSolverDico["BDF Order"] = str(value)
                pass
            else:
                self.elmerSolverDico["BDF Order"] = str(1)
                pass
            if key == "Bubbles":
                self.elmerSolverDico["Bubbles"] = value
                pass
            if key == "convSolver":
                self.elmerSolverDico["Linear System Convergence Tolerance"] = value
                pass
            if key == "discretisation":
                self.elmerSolverDico["discretisation"] = value
                pass
            if key == "iterSolver":
                self.elmerSolverDico["Linear System Max Iterations"] = value
                pass
            if key == "linearSystemSymetry":
                self.elmerSolverDico["Linear System Symetry"] = value
                pass
            if key == "preconditioner":
                self.elmerSolverDico["Linear System Preconditioning"] = value
                pass
            if key == "timeSteppingMethod" or key == "tSM":
                self.elmerSolverDico["Timestepping Method"] = value
                pass
            pass
    
    def setTransportParameters(self,*args):
        self.value+=args
        return None
    
    def setChemicalParameter(self,*args):
        """
        Used to enter chemical solver parameters
        """
        if self.chemicalSolver:
            self.chemicalSolver.setParameter(*args)
            pass
        else:
            self.chemicalParameters+=args
            pass
        return None
    
    def setTimeBoundaryConditionVariation(self):
      
    
        def chemicalstatewriter(chemicalProblemInstance):   
            chemistryInstance = Chemical()
            chemistryInstance.setData(chemicalProblemInstance)
            chemistryInstance.setComponent("phreeqc")
            #inputfileName = name+".in"
            #outputfileName = name+".out"
            inputfileName = "phreeqCFile"
            #print "setTimeBoundaryConditionVariation: inputfileName",inputfileName
            #raw_input("setTimeBoundaryConditionVariation")
            #print " chemicalstatewriter speciesBaseAddenda:",self.speciesBaseAddenda
            chemistryInstance.initialise()
            chemistryInstance.setParameter(chemicalProblemInstance.name+".out")
            chemistryInstance.run()
            #
            # list of concentrations
            #
            componentConcentrationsList = chemistryInstance.getOutput('componentsConcentration')
            return componentConcentrationsList

        timeBoundaryConditionVariation = []
                    
        for boundaryCondition in self.boundaryConditions:
            if boundaryCondition.getTimeVariation()!=None:
                for variation in boundaryCondition.getTimeVariation():
                    time = variation[0]
                    chemicalState_at_time = variation[1]
                    name = chemicalState_at_time.name.replace(".","").replace(" ","")
                    chemicalProblemInstance = ChemicalProblem(name = "bcVariation",
                                                              chemistryDB = self.chemistryDB,
                                                              chemicalState = chemicalState_at_time,
                                                              speciesBaseAddenda = self.speciesBaseAddenda)
                                                            #
                                                            # We establish the != equilibria, and retrieve the Primary species
                                                            # in listOfConcentrations
                                                            #                                              
                    listOfConcentrations = chemicalstatewriter(chemicalProblemInstance)
           
                    # Building up the timeBoundaryConditionVariation list    
                    if timeBoundaryConditionVariation ==[]:
                        timeBoundaryConditionVariation.append((time,(boundaryCondition,listOfConcentrations,chemicalState_at_time.aqueousSolution.getTemperature())))
                        pass
                    else:
                        for zeit in timeBoundaryConditionVariation:
                            temporary = None
                            if (zeit[0]==time):
                                zeit[1].append((boundaryCondition,listOfConcentrations))
                                break
                            else:
                                temporary =  (time,(boundaryCondition,listOfConcentrations,chemicalState_at_time.aqueousSolution.getTemperature()))
                                pass
                            pass
                        if temporary != None:
                            timeBoundaryConditionVariation.append(temporary)
                            pass
                        pass
                    pass
                pass
            pass
            #print timeBoundaryConditionVariation
            #raw_input("timeBoundaryConditionVariation")
        return timeBoundaryConditionVariation

    def setCouplingParameter(self,
                             initialTimeStep=None,
                             maxTimeStep=None,
                             minTimeStep=None,
                             increaTimeStepCoef= None,
                             decreaTimeStepCoef= None,
                             couplingPrecision= None,
                             maxIterationNumber=None,
                             optimalIterationNumber=None,
                             chat=None,
                             initialisationOption      = None,
                             convergenceCriterionLevel = None,
                             algorithm=None,
                             debug = None):
        """
        That function enables to set the different
        parameters driving a CC algorithm.
        """
        if algorithm: self.couplingAlgorithm = algorithm.upper() # coupling algorithm, NI or CC

        if decreaTimeStepCoef : self.decreaTimeStepCoef = decreaTimeStepCoef

        if increaTimeStepCoef : self.increaTimeStepCoef = increaTimeStepCoef
 
        if convergenceCriterionLevel: self.convergenceCriterionLevel = convergenceCriterionLevel

        if couplingPrecision  : self.couplingPrecision = couplingPrecision

        if debug: self.debug = debug

        if initialisationOption: self.initialisationOption = initialisationOption

        if initialTimeStep and self.initialTimeStep == None: self.initialTimeStep = initialTimeStep

        if maxIterationNumber : self.maxIterationNumber = maxIterationNumber
            
        if maxTimeStep : self.maxTimeStep  = maxTimeStep

        if minTimeStep : self.minTimeStep = minTimeStep

        if optimalIterationNumber : self.optimalIterationNumber = optimalIterationNumber
        
        if chat : self.chat = chat # mainly cpu time
        
        return None

    def chemicalTransportOutput(self, final_time, it, error):
#        print "InteractiveSpatialPlot";#sys.stdout.flush()
        #
        # we use gnuplot for interactive 1D plotting
        #
        #print ("dbg chemicalTransportOutput self.spatialInteractiveOutputs: ", self.spatialInteractiveOutputs)
        #print ("dbg chemicalTransportOutput self.expectedOutputs: ", self.expectedOutputs)
        #print ("dbg chemicalTransportOutput self.outputs: ", self.outputs)
        #print ("dbg chemicalTransportOutput call of iTimePlot: ")
        if self.spatialInteractiveOutputs and self.timeStepNumber >= 1:
        
            self.iTimePlot(self.spatialInteractiveOutputs,\
                           self.gnuplot,\
                           self.iPFrequency,\
                           self.iPTitle, self.iPSubTitle, self.iPRotate, savingFrequency = self.iPSavingFrequency)
            pass
        #print("spatialSaveOutputs");sys.stdout.flush()
        if  (self.spatialSaveOutputs and
            (self.timeStepNumber % self.spatialSaveFreq ==0)):                    
            self.SaveSpatialPlot(self.simulatedTime)
            pass
        #print ("expectedOutputs: ");sys.stdout.flush()
        if (self.expectedOutputs):
            for output in self.expectedOutputs:
                #print " dbg chemicalTransport module output.getTimeSpecification(): ", output.getTimeSpecification(), output.getTimeSpecification().getSpecification()
                if output.getTimeSpecification():
                    if ((output.getTimeSpecification().getSpecification() ==  'frequency')
                        and (not (self.timeStepNumber == 1 or self.simulatedTime == final_time))):
                        if (self.timeStepNumber % output.getTimeSpecification().getFrequency() !=0): 
                            output = 0
                            pass
                        pass
                    elif ((output.getTimeSpecification().getSpecification() ==  'period')
                          and (not (self.timeStepNumber == 1 or self.simulatedTime == final_time))):
                        raise Exception,"period output type not yet implemented"
                    elif (output.getTimeSpecification().getSpecification() ==  'times'):                     
                        if (self.simulatedTime not in output.getTimeSpecification().getTimes()): 
                            output = 0
                            pass
                        pass
                    else :
                        if self.timeStepNumber == 1:
                            pass
                        elif (output.getTimeSpecification().getSpecification() not in ['frequency','period','times']) :
                            mess = output.getTimeSpecification().getSpecification() + " output type not yet implemented"
                            print mess
                            raise Exception, "output type not yet implemented, available types are times, period or frequency"
                        else:
                            pass
                        pass
                    pass
                if output:
                    support = output.getSupport()
                    if (output.getQuantity().lower() == 'numerics'):
                        self.outputs[output.getName()].addRow( [self.simulatedTime, self.timeStepNumber, self.dT, it, error] )
                        pass                        
                    elif isinstance(support, CartesianMesh):
                         raise Exception, "CartesianMesh output type not yet implemented"
#                    elif isinstance(support,AbstractPoint):
#                        pid = id(support)
#                        self._fillIndexDictionnaryWithPoint(support)                      
#                        
#                        indi = self._dico_point_index[pid]
#                        name, values = self.getOutputValues(output)
#                        value = values[indi]
#                        
#                        self.outputs[output.getName()].addRow([self.simulatedTime,value])
#                        pass
                    else:
                        if (output.getFormat() == 'table'):
                            table = self.outputTable( output,self.simulatedTime)
                            if (output.getSave() == 'file'):
                                if type(output.getName()) is StringType:
                                    name = output.getName() + " at time %10.4e"%self.simulatedTime
                                    table.setName(name)
                                    pass
                                table.writeToFile(self.problem.getName() + '.tab')
                                pass
                            else:
                                                                                            #
                                                                                            # we update the dictionary with new data.
                                                                                            #
                                self.outputs[output.getName()].append( (self.simulatedTime, table) )
                                pass
                        else:
                            raise Warning, " we should be able to define a field and to write it as a file: to do "
                            pass
                        pass
                    pass
                pass
            pass
        pass

    def _fillIndexDictionnaryWithPoint(self,point):
        # we look for index of the nearest element of point ie
        # the index to use in values python list
        dim = self.mesh.getSpaceDimensions()
        if not hasattr(self, "_coord_val"):
            # construction of _coord_val list
#            coord_list = self.transportSolver.getCoordinatesValues()
            if dim == 1:
                self._coord_val = self.meshPointCoordinates[0]
                pass
            else:
                x = self.meshPointCoordinates[0]
                y = self.meshPointCoordinates[1]
                if dim == 2:
                    self._coord_val = [[x[i],y[i]] for i in range(len(x))]
                    pass
                else:
                    z = self.meshPointCoordinates[2]
                    self._coord_val = [[x[i],y[i],z[i]] for i in range(len(x))]
                    pass
                pass
            pass
        
        pid = id(point)

        if not hasattr(self, "_dico_point_index"): self._dico_point_index = {}              # dico initialisation

        if pid not in self._dico_point_index.keys():
            point_coord = point.getCoordinates()
            x = point_coord[0]
            if dim > 2:
                y = point_coord[1]
                if dim == 3:
                    z = point_coord[2]
                    pass
                pass               
            # init
            i = 0
            d2  = (x-self._coord_val[i][0])**2
            if dim > 2:
                d2 += (y-self._coord_val[i][1])**2
                if dim == 3:
                    d2 += (z-self._coord_val[i][2])**2
                    pass
                pass                                
            d_mini_2 = d2
            self._dico_point_index[pid] = i
            #
            for i in range(1,len(self._coord_val)):
                d2  = (x-self._coord_val[i][0])**2
                if d2 > d_mini_2 : continue
                if dim > 2:
                    d2 += (y-self._coord_val[i][1])**2
                    if d2 > d_mini_2 : continue
                    if dim == 3:
                        d2 += (z-self._coord_val[i][2])**2
                        if d2 > d_mini_2 : continue
                        pass
                    pass
                d_mini_2 = d2
                self._dico_point_index[pid]=i
                pass
            #
            pass
        # END OF FILLING DICTIONNARY
        return None
        
    def getSpecificPrimaryspeciesField(self,aPrimarySpecies):
        """
        That function is used in the user defined functions,
        see the etuser python module.
        It enables to retrieve the concentration field for a specific primary species.
        """
        listOfPrimarySpecies = [species.name.lower() for species in self.chemicalSolver.getPrimarySpecies()]
        print listOfPrimarySpecies
        numberOfPrimaryspecies = len(listOfPrimarySpecies)
        index = listOfPrimarySpecies.index(aPrimarySpecies.lower())
        listOfConcentrations = self.chemicalSolver.getMobileConcentrationField('internal')
        nbOfActiveCells = len(listOfConcentrations)/numberOfPrimaryspecies
        deb = nbOfActiveCells*index
        fin = nbOfActiveCells*(index+1)
        #print listOfConcentrations[deb:fin]
        #raw_input("list of Cl")
        return listOfConcentrations[deb:fin]

        
    def getExpectedOutputs(self,name):
        for expectedOutput in self.expectedOutputs:
            if expectedOutput.name == name:
                return expectedOutput
        return None
        
    def getCoupledOutput(self,output_names,support):
        
        output_names = list(output_names)

        returned_outputs = []
                
        support = list(support)
        if type(support) != IntType: raise TypeError, " the support argument must be a string "        
    

        for output_name in output_names:
            if self.coupled_outputs_dict.has_key(output_name):
                output = self.coupled_outputs_dict[output_name]
            else:
                raise "Undefined output "+str(output_name)
            name, values = self.getOutputValues(output)
            values = extractIndex(values,support)
            returned_outputs.append(values)
            
            pass
        if (len(returned_outputs)==1):
            returned_outputs = returned_outputs[0]
            pass             
        return returned_outputs

    def setEffectiveDiffusion(self,diffusionField):
        if self.diffusionLaw:
            mess = 'setEffectiveDiffusion is not possible if a diffusionLaw is defined'
            raise Exception, " for conformity, you cant set a diffusion field\n"+\
                         "if a diffusion law has to be satisfied"
        if self.transportSolver: 
            self.transportSolver.setDiffusion(diffusionField)
            pass
        else:
            raise Exception, 'You should define a transport component before trying to set a diffusion law'
        
        return None

    def modifyKineticLaws(self,kineticLaws,index=None):

        kineticLaws = list(kineticLaws)
        for kineticLaw in kineticLaws:
            if (not isInstance(kineticLaw,KineticLaw)):
                raise str(kineticLaw) + " is not an instance of KineticLaw"
            pass
        self.chemicalSolver.modifyKineticLaws(kineticLaws,index)
        
        return None
    
    def newTimeStepEvaluation(self,it,algorithmParameter):
        """
        evaluation of the new time step self.dT and potential transfert to the transport solver.
        """
        actualDt = self.dT
        if algorithmParameter == 1:
            if self.oldDT != None:
                # meanwhile a computational step has been done, we go on with old
                # time step without looking at optimalIterationNumber
                self.dT = self.oldDT
                pass
            elif self.optimalIterationNumber:
                #print "self.optimalIterationNumber ", self.optimalIterationNumber
                #print "self.convergenceAnalysisParameter",  self.convergenceAnalysisParameter      
                if (it > self.optimalIterationNumber*1.2):
                    #
                    # Too much iterations in comparison with optimalIterationNumber, we decrease the time step
                    #
                    self.oscControl = "dec"
                    if  self.minTimeStep:
                        self.dT = max(self.dT*self.decreaTimeStepCoef,self.minTimeStep)
                    else:
                        self.dT =  self.dT*self.decreaTimeStepCoef
                    pass
                elif ((it < self.optimalIterationNumber*0.8) and (self.convergenceAnalysisParameter == 1)):
                    #
                    # we increase the time step if the number
                    # of iterations satisfies the first criterium
                    # and to avoid oscillations, we wait one time step before increasing the time step
                    # 
                    if self.oscControl == "dec":
                    #
                    # to avoid oscillations, we wait one iteration
                    # before increasing the time step by a scaling factor
                    # defined by the user
                    #
                        self.oscControl = ""
                        pass
                    else:
                        if  self.maxTimeStep:
                            self.dT = min(self.dT*self.increaTimeStepCoef,self.maxTimeStep)
                        else:
                            self.dT =  self.dT*self.increaTimeStepCoef
                            pass
                        self.oscControl = "inc"
                        pass
                    pass
                pass
        else:
            # affectation to the new value
            self.simulatedTime -= self.dT
            self.timeStepNumber -= 1
            
            # computation of the new time step if possible
            if self.decreaTimeStepCoef:
                self.dT =  self.dT*self.decreaTimeStepCoef
                pass
            else:
                raise RuntimeError("no decrease time step define, we stop the computation")
            if self.minTimeStep:
                if (self.dT < self.minTimeStep):
                    raise RuntimeError("Minimal time step reached we stop the computation")
                pass
            
            pass
        if self.oldDT: self.oldDT=None

        #
        # time step control
        #  
        oldDt = self.dT
        # 1) check if an between computation has to be done
        self.dT = min(self.dT,self.betweenComputation(self.simulatedTime))
        # 2) check if final time
        if (self.simulatedTime < self.finalTime):
            self.dT = min(self.dT,(self.finalTime - self.simulatedTime))
            pass
        if (not (oldDt == self.dT)):
            # an between computation has to be done for outputs or until time option
            # we keep old_deltat_t to go on on next time step with this value
            self.oldDT = oldDt
            pass

        cpuTimeBeg = self.cpuTime()
        
        if (not (actualDt == self.dT)):
            if self.environ():
                self.transportSolver.setTimeStep(self.dT)
                self.transportCPUTime += (self.cpuTime() - cpuTimeBeg)
                pass
            pass                     
    
        return None

    def run(self,option = 'all', simulationTime = None):
        """
        Enables to launch the coupling and to ride the simulation over time
        """         
        option = option.lower()
        if option not in ['all','onestep','untiltime']: raise Exception, " check the options for newTimeStepEvaluation run"
        
        
        if (option=='untiltime'):
            if simulationTime:
                self.simulationTime = simulationTime
            else:
                raise Exception,"A duration time has to be defined, cf. the problem definition"
            pass

        # Init
        if not(self.initFlagControl):
            self.initFlagControl = 1
            self.launch()
            pass
        if self.spatialInteractiveOutputs!=None:
            self.interactivePlot = IGPlot()
            data = []
            self.interactivePlot.setData(data)
            print "self.interactivePlot.setData()";#sys.stdout.flush()
            self.interactivePlot.start()
            self.interactivePlot.setXBounds(0,1)
            self.interactivePlot.setYBounds(0,1)
            self.interactivePlot.start()
            self.interactivePlot.init()
            self.interactivePlot.run()
            
            self.evtloop = wx.EventLoop()
            self.old = wx.EventLoop.GetActive()
            wx.EventLoop.SetActive(self.evtloop)
            while self.evtloop.Pending():
                self.evtloop.Dispatch()
                pass
            pass
                                                                                            #
                                                                                            # taking user functions into account
                                                                                            #
        if self.userProcessing:
            for method in self.processingList:
                print " method ",method, self.timeStepNumber
                #raw_input("user processing ")
                exec(method)
            pass
        #
        # User processing is over
        #
        #
        # behavior: option dependent
        #
        if option == 'onestep':
            currentIteration = self.timeStepNumber
            while (self.timeStepNumber == currentIteration) :
                self.oneTimeStep()
                pass
            pass
        else:
            if option == 'untiltime':
                if self.simulationTime <= self.times[-1]*(1.+1.E-7):
                    self.finalTime = simulationTime
                else:
                    raise Exception, "The specified untilTime of the run method is greater"+\
                                     " than the max of the list of time specified in the problem"
                if (self.dT >(self.simulationTime-self.simulatedTime)):
                    self.dT = self.simulationTime-self.simulatedTime
                    self.transportSolver.setTimeStep(self.dT)
                    pass
                pass
            else:
                self.finalTime = self.times[-1]
                pass
                                                        #
                                                        # we iterate over time
                                                        #
            while (self.simulatedTime < self.finalTime) :
                #if self.timeStepNumber == 1: print " ctmdbg oneTimeStep untiltime "
                self.oneTimeStep()
                #if self.timeStepNumber == 1: print " ctmdbg oneTimeStep ended "
                pass
            pass      
        #
        # end of the time step 
        #
        if self.environ():
            self.transportSolver.end()
            pass

        return None
        
    def backup(self,backupFile):
        """
        to enable a restart through the pickle module, backupFile being a string
        """
        self.backupFileName = backupFile
        backupFile = open(backupFile,"w")
        restartDico = {}
#        restartDico["fileName"] = backupFile
        p = pickle.Pickler(backupFile,2)
        print sys.argv[0];#sys.stdout.flush()
        p.dump(sys.argv[0])
        p.dump(self.simulatedTime)
        p.dump(self.chemicalSolver.getMobileConcentrationField('internal'))
#        p.dump(self.chemicalSolver.aqueousStateDump())
        return None
        
    def restart(self,restartFile):
        """
        to enable a restart through the pickle module, see the tutorial in the Restart directory
        """
        backupFile = open(restartFile,"r")
        u = pickle.Unpickler(backupFile)
        initialCaseFile = u.load()
        if initialCaseFile[0:-3] not in str(sys.argv[0]):
            raise Exception(" Check the restart file naming convention")
        self.simulatedTime = u.load()
        conc = u.load()
        self.chemicalSolver.setMobileConcentrationValues('internal',conc)

#        self.chemicalSolver.aqueousStateSet(u.load())
        print " ~~~~~~~~~~~~~~~ ";#sys.stdout.flush()
        print " restart at time ",self.simulatedTime;#sys.stdout.flush()
        print " ~~~~~~~~~~~~~~~ ";#sys.stdout.flush()
        
        return None       

    def getOutput(self, unknown):
        print "\ndbg getOutput keys: ",self.outputs.keys()
        print "\ndbg getOutput: ",type(self.outputs)
        if self.outputs.has_key(unknown):
            print "dbg getOutput output: ",self.outputs[unknown]
            print "dbg getOutput type: ",type(self.outputs[unknown])
            return self.outputs[unknown]
        else:
            print "Undefined output", unknown;#sys.stdout.flush()
            return None
        pass
    
    def end(self):
        """
        Enables to end the simulation with a smile and
        eventually as switcher
        """
        self.finalOutputsWriter()
        
        if not hasattr(self, "transportSolver") or not self.transportSolver:
            return
        import random        
        citations = [
                     "\n\"Ailleurs c'est bien, c'est meme mieux\"\n",
                     "\n\"Apres ? c'est une autre histoire...\"\n",
                     "\n\"Ad libitum\"\n",
                     "\n\"Auf, preiset die Tage!\"\n",
                     "\n\"Ce qu\'un imbecile peut faire, n\'importe quel imbecile peut le faire\"\n",
                     "\n\"Chacun est responsable de tous. Chacun est seul responsable. Chacun est seul responsable de tous.\"\n",
                     "\n\"De omnibus dubitandum est\"\n",
                     "\n\"Die Suche nach der Wahrheit ist wertvoller als ihr Besitz.\"\n",
                     "\n\"Dosis (sola) facit venenum\"\n",
                     "\n\"Do turkeys enjoy Thanksgiving ?\"\n",
                     "\n\"Est-il besoin d'executer,\nL\'on ne rencontre plus personne.\"\n",
                     "\n\"Et ignem regunt numeri\"\n",
                     "\n\"Everything should be kept as simple as possible,\n but not simpler!\"\n",
                     "\n\"Everything is possible, everything is achievable\"\n",
                     "\n\"Forecasts are always difficult,\nespecially if they concern the future!\"\n",
                     "\n\"On devient ce que notre regard contemple\"\n",
                     "\n\"On definit trop l’intelligence par la scolarite. L’intelligence devient alors une classe, la classe de ceux qui ont fait leurs etudes.\n"+\
                         "Les etudes sont demontrees par les diploemes, preuves materielles.\n"+\
                         "Ce systeme est excellent pour la preservation et la transmission des connaissances,"+\
                         "mais il est mediocre, sinon mauvais pour leur accroissement. Il arrive que la preuve materielle, le diploeme, soit plus durable que ce qu’elle prouve,"+\
                         " que le zele, la curiosite, la vigueur mentale de celui qu’elle institue membre de la caste des lettres."+\
                         "Parmi les inconvenients de ce systeme, il faut signaler l’ankylose de l’homme dans son attitude initiale.",
                     "\n\"Und seiner Haende Werk zeigt an das Firmament!\"\n",
                     "\n\"les hommes usent des statistiques comme les ivrognes des reverberes,\n"+\
                         "pour l'appui qu'elles fournissent plutot que pour la lumiere qu'elles repandent\"\n",
                     "\n\"Nul ne doit souffler plus haut qu\'il n\'a l\'esprit!\"\n",
                     "\n\"Ite missa est\"\n",
                     "\n\"La science peut etre l’asymptote de la verite, elle approche sans cesse, et ne touche jamais\"\n",
                     "\n\"Le jardin est dans le jardinier.\"\n",
                     "\n\"like chasing the wind\"\n",
                     "\n\"Money is like muck, not good unless spread.\"\n",
                     "\n\"Numquam ponenda est pluralitas sine necessitate.\"\n",
                     "\n\"Panta rhei\"\n",
                     "\n\"tempus tantum nostrum est\"\n",
                     "\n\"Plus on apprend, plus on ne sait rien\"\n",
                     "\n\"Qui accroit sa science accroit sa douleur\"\n",
                     "\n\"Sachez vous eloigner car, lorsque vous reviendrez a votre travail, votre jugement sera plus suer.\"\n",
                     "\n\"Summum jus, summa injuria\"\n",
                     "\n\"Toi qui chemine, il n\'y a pas de chemin,\n le chemin se fait en marchant\"\n",
                     "\n\"Tout ce qui a pu se dire contre la science ne saurait faire oublier que la recherche scientifique reste, dans la degradation de tant d'ordres humains, l'un des rares domaines ou l'homme se controele, s'incline devant le raisonnable, est non bavard, non violent et pur. Moments de la recherche certes constamment interrompus par les banalites du quotidien mais qui se renouent en duree propre. (Levinas) ?\"\n",
                     "\n\"Tout s\'opere parce qu\'a force de temps tout se rencontre\"\n",
                     "\n\"Where the willingness is great the difficulties cannot be great\"\n",
                     "\n\"Wozu\"\n"
                     ]
        random.seed()     
        print random.choice(citations);#sys.stdout.flush()
        
        if self.spatialInteractiveOutputs != None:
            self.gnuplot.close()
     
        self.cpuPrints()
        
        return None
#
# interactive spatial plot based on gnuplot
#
    def setInteractivePlot(self, listOfOutputs, plotFrequency = None, title = None,\
                           subTitle = None, rotate = None, saving = None, savingFrequency = None):       
        if plotFrequency == None:
            self.iPFrequency = 1
            pass
        else:
            self.iPFrequency = plotFrequency
            pass
        if savingFrequency == None:
            self.iPSavingFrequency = None
            pass
        else:
            self.iPSavingFrequency = savingFrequency
            pass
        if len(listOfOutputs)!=0:
            self.spatialInteractiveOutputs = listOfOutputs
            #print self.pyversion
            if self.pyversion<2.7:
                import _Gnuplot, Gnuplot.funcutils
                self.gnuplot = _Gnuplot.Gnuplot()
                pass
            else:
                import Gnuplot, Gnuplot.funcutils
                self.gnuplot = Gnuplot.Gnuplot()
                pass
            pass
        else:
            raise Warning, " check the list of outputs for the interactive plot"
        self.iPTitle = title
        self.iPSubTitle = subTitle
        if rotate == None or rotate == False:
            self.iPRotate = False
            pass
        else:
            self.iPRotate = rotate
            pass
        #raw_input(" length of listofoutputs"+str(len(listOfOutputs)))
        if len(listOfOutputs) > 0 and saving == True:
            self.iPSaving = 'intGnuFile.dem'                                                # postscript file for gnuplot
            os.system("rm -f intGnuFile.dem")
            pass
            #raw_input(" rm of dem file ")
        else:
            self.iPSaving = None
            pass
        return None
        
    def setInteractiveSpatialPlot(self, outputs, abscissis=None, plotter=None, isfrequency = None):        
        print "dbg call to setInteractiveSpatialPlot",outputs
        if isfrequency==None:
            self.isfrequency = 1
            pass
        else:
            self.isfrequency =  isfrequency
            pass
        self.iPFrequency = self.isfrequency
        if len(outputs)!=0:
            if abscissis:
                abscissis  = abscissis.lower()
                pass
            self.spatialInteractiveAbscissis = abscissis
            if plotter:
                self.plotter = plotter.lower()
                pass             
            
            for output in outputs:
                self.addChemicalOutputs(output)               
                pass
            self.spatialInteractiveOutputs = outputs
            if self.pyversion<2.7:
                import _Gnuplot, Gnuplot.funcutils
                self.gnuplot = _Gnuplot.Gnuplot()
                pass
            else:
                import Gnuplot, Gnuplot.funcutils
                self.gnuplot = Gnuplot.Gnuplot()
            self.iPTitle = "Etumos:"; self.iPSubTitle = "";self.iPRotate = False;self.iPSavingFrequency = 1
            self.listOfOutputs = self.spatialInteractiveOutputs
            print "dbg setInteractiveSpatialPlot listOfOutputs",self.listOfOutputs
        return None

    def setVtkOutputsParameters(self,unknowns, vtkTimeUnit, frequency, vtkFileFormat = None, fmt = None):
        """
        Used to set parameters for vtk outputs.
        
        Example : setVtkOutputsParameters(["pH","Eh","Al","Quartz"],"years",1000)
        
        Here, we save the unknowns "pH","Eh","Al" and "Quartz" every 1000 iterations, the unit being years ...
        It means, the data will be saved at 0, 1000, 2000 ... years
        
        """
        if "Temperature" in unknowns:
            unknowns[unknowns.index("Temperature")] = "temperature"
            pass
        self.vtkFieldSpecies = unknowns
        if self.initialTimeStep == None:
            raise Warning, " You have to call the setVtkOutputsParameters function after the setCouplingParameter function"
            pass
        self.initialTimeStep, self.vtkFrequency = _vtkFrequency( self.initialTimeStep, vtkTimeUnit, self.maxTimeStep, frequency)
    
        self.vtkTimeUnit = vtkTimeUnit
        if vtkTimeUnit in ["days","day","d"]:
            self.vtkScalingFactor = 86400
        elif vtkTimeUnit in ["s", "seconds"]:
            self.vtkScalingFactor = 1
        elif vtkTimeUnit in ["hours","hour","h"]:
            self.vtkScalingFactor = 3600
        elif vtkTimeUnit in ["years", "year","y"]:
            self.vtkScalingFactor = 31557600
        
        self.vtkControl = 1
        
        self.vtkFileFormat = vtkFileFormat
        
        self.vtkfmt = fmt
        return None

    def setSaveSpatialPlot(self,outputs,frequenz=None):
        """
        Used to handle spatial plots for postprocessing
        """
        if len(outputs)!=0: 
            for output in outputs:
                self.addChemicalOutputs(output)               
                pass             
            self.spatialSaveOutputs = outputs
            pass
        if frequenz == None: frequenz = 1                                                   # saving frequency
        self.spatialSaveFreq=frequenz
        return None

    def interactiveSpatialPlot(self,current_time,time_iteration):
        """
        interactive plot driven by a wx tool
        """
        subtitle = "time = "+'%10.4e'%current_time
        print 
        if (time_iteration%self.isfrequency==0) or (time_iteration ==1):
            DummyCurve =  Table(name = 'Spatial plot')
            if self.environ():
                coord_t = [self.meshPointCoordinates[0],self.meshPointCoordinates[1]]
                if (self.TransportComponent == 'mt3d'):
                    if self.transportSolver.fwel =="T" :
                        if (self.transportSolver.iboundf[0]==-1) and ((self.spatialInteractiveAbscissis=='x') or\
                            (self.spatialInteractiveAbscissis==None)):
                            trans = coord_t[0][0]
                            coord_t[0] = self.meshPointCoordinates[0][:-2]
                            for ind in range(0,len(coord_t[0])):
                                coord_t[0][ind]-=trans
                                pass
                            pass
                        if self.transportSolver.iboundf[-1] == -1:
                            coord_t[0] = coord_t[0][:-2]
                            pass
                        pass
                    pass
                print " abs ",coord_t[0];#sys.stdout.flush()
                if self.spatialInteractiveAbscissis:
                    if  (self.spatialInteractiveAbscissis=='x'): 
                       absz = _Numeric.array(coord_t[0])
                    elif (self.spatialInteractiveAbscissis=='y'): 
                       absz = _Numeric.array('Space',coord_t[1])
                    else:
                        mess = self.spatialInteractiveAbscissis + ": not correct as absciss"
                        raise mess
                    pass

                else:
                    absz = _Numeric.array(coord_t[0])
                    pass
                ind = 0
                legend = []
                data = []
                xmax = -1.e20
                xmin = 1.e+20
                ymax = -1.e20
                ymin = 1.e+20
                for i in absz:
                    xmin = min(xmin,i)
                    xmax = max(xmax,i)
                    pass
                for output in self.spatialInteractiveOutputs :
            
                    name =  output.getName().replace('Concentration_',"")
                    legend.append(name)
                    if name.lower() == "diffusion":
                        values = self.transportSolver.getInternalEffectiveDiffusionValues()
                        pass
                    elif ((name.lower() == "temperature") or (name.lower() == "temperature_table")):
                        values = self.transportSolver.getTemperatureField()
                        print "ctm length of values",len(values);#sys.stdout.flush()
                        pass
                    else:
            #print " index",self.chemicalSolver.speciesBaseAddenda,output.getChemicalName()
                        values =  self.chemicalSolver.getOutput(output.getChemicalName())
            #
            # For Mt3d, we take the b. cells into account and translate the whole points from
            # itp depth. Counting flux cells, we eliminate these cells at the end of the list. 
            #
            # refaire cette boucle, car le plot doit etre independant de la boucle sur les outputs          
                        pass
                    if (self.TransportComponent == 'mt3d'):
                        style = None
                        symbols = 0
                        if self.transportSolver.fwel == "T":
                            if self.transportSolver.iboundf[0] == -1:
                                values = values[:-2]
                                pass
                            if self.transportSolver.iboundf[-1] == -1:
                                values = values[:-2]
                                pass
                        pass
                    elif(self.TransportComponent == 'elmer'):
                        style = 0
                        symbols = 1
                        pass
                    ords = _Numeric.array(values)
                    for i in ords:
                        ymin = min(ymin,i)
                        ymax = max(ymax,i)

                    data.append( _Numeric.transpose([absz,ords]))
                    self.interactivePlot.setXBounds(xmin,xmax)
                    self.interactivePlot.setYBounds(ymin,ymax)

                    if i==len(self.spatialInteractiveOutputs)-1:
                        print " ctm we are here ";#sys.stdout.flush()
                        self.interactivePlot.setYBounds(ymin,ymax)
                        self.interactivePlot.setLegend(legend)

                        #print "data ",data;#sys.stdout.flush()
                        self.interactivePlot.setData(data)
                        self.interactivePlot.run()
                        pass
                    else:
                        #print " we are da ",data;#sys.stdout.flush()
                        self.interactivePlot.setData(data)
                        self.interactivePlot.run()
                        pass
                    if (name.lower() == "ph"):
                        self.interactivePlot.setData(data)
                        self.interactivePlot.run()
                        pass
                    elif (name.lower()=="mass_water") or (name.lower()=="watermass"):
#                    self.interactiveplot.ybounds(0.5,1.2)
                        pass
                    elif (name.lower().find("temperature")==0):
                        minv = 1000.
                        maxv = 0.
                        for k in range(len(values)):
                            minv = min(values[k],maxv)
                            maxv = max(values[k],maxv)
                            pass
                        pass
#           self.interactiveplot.ybounds(ymin=minv-1.,ymax=maxv+1)
                        pass
                    elif (name!="pe") and (name!="Eh") and (name!="temperature"):
                        maxv = 0.
                        for k in range(len(values)):
                            values[k] = max(values[k],1.e-20)
                            maxv = max(values[k],maxv)
                            pass
                        pass
                    ind += 1
                    pass
        else:
            pass

        return None

    def SaveSpatialPlot(self,current_time):
        """
        Used to handle post processing
        """        
#        coord = self.transportSolver.getCoordinatesValues()   
        DummyCurve2 =  Table(name = 'Spatial plot')
        DummyCurve2.addColumn('Space',self.meshPointCoordinates[1])
        for output in self.spatialSaveOutputs :
            output_name =  output.getName()

            values =  self.chemicalSolver.getOutput(output.getChemicalName())
            DummyCurve1 =  Table(name = output_name)
            DummyCurve1.addColumn('Space',self.meshPointCoordinates[1])
            DummyCurve1.addColumn(output_name,values)
            DummyCurve2.addColumn(output_name,values)
            pass
        file = self.name +  '_t'
        file += repr(current_time)
        DummyCurve2.writeToFile(file + '.res')
            
        return None

    def timeInteractivePlot(self,current_time,
                            time_iteration,
                            curveTable,
                            curve,
                            gplot,
                            pointtoplotindice,
                            listofSpeciestoplot,
                            list_component,
                            internalNodesNumber,
                            aqueousconcentrations,
                            plotFrequency,
                            cunit,
                            saving,
                            title = None):
        """
        Used to handle interactive plot
        """
        self.title = title
        self.pointtoplot  = pointtoplotindice
        if time_iteration >= 1 and curveTable and time_iteration%plotFrequency==0:
            # what we want to plot 
            listofindices = []
    
            for species in listofSpeciestoplot:
                ind= 0
                for comp in list_component:
                    if species==com:
                        listofindices.append(ind)
                        ind+=1
                        pass
                pass
            row = [current_time]
            for i in listofindices:
                concentration = aqueousconcentrations[pointoplotindice + i*internalNodesNumber]
                row.append(concentration)
                pass
            curve.addRow(row)
            if (self.title!=None):
                gplot.title("essai")
                pass
            else:
                gplot.title("Concentrations over time")
                gplot.subtitle("Conc. at point %d over time, final time = %10.4e"%(self.pointtoplot,current_time))
                pass

            for i in range(0,len(listofSpeciestoplot)):
                gplot.plot(curve,0,'time in (s)',i+1,' mol/l')
                gplot.hold(1)
            #   gplot.plot(curve,0,'time in (s)',1,' mol/l')
            #   gplot.plot(curve,0,'time in (s)',2,' mol/l')
            gplot.legend(curveTable[1:])
            if (saving==1):
                nameofplottosave = "plot"+str(time_iteration)
                gplot.save(nameofplottosave,"png")
                pass
            gplot.hold(0)
            pass
        pass

    def getOutputValues(self,output):
        """
        Used to handle output quantities
        """
        quantity = output.getQuantity().lower()
        name = output.getName()
        unit = output.getUnit()
        if quantity == 'porosity':
            name = quantity
            if self.variablePorosityOption:
                values = self.currentPorosity
                pass
            else:
                values = self.initialPorosityValues
                pass
            pass
        elif quantity == 'diffusion':
            name = quantity
            if self.diffusionLaw:
                values = self.effective_diffusion_k
                pass
            else:
                try:
                    values = self.transportSolver.getEffectiveDiffusionValues()
                except KeyError:
                    raise Exception,'You asked for EffectiveDiffusion but no values was setted'
                pass
            pass
        elif quantity == 'volume':
            name = quantity
            values = self.element_volume_values
            pass
        elif "temperature" in quantity.lower():
            name = 'temperature'
            try:
                values = self.transportSolver.getTemperatureField()
            except KeyError:
                raise Exception,'Temperature as output couldn\'t be retrieved'
            pass
        else:  
            name =  output.getChemicalName()
            values =  self.chemicalSolver.getOutput(name, unit=unit)
            pass
        return name, values

    def outputTable(self,output,time):  
        """
        Used to handle unknowns as tables. Unknowns can be chemical unknowns, porosity, transport properties or mechanical unknowns
        """      
        chemicalSpeciesList = output.getChemicalName()
        #print " ## ctm dbg outputTable chemicalSpeciesList ##",chemicalSpeciesList;sys.stdout.flush()
        dic = {}
        if type(chemicalSpeciesList) is ListType:
            for species in chemicalSpeciesList:
                unknown = self.chemicalOutputNames[species]
                name, values = self.getOutputValues(unknown)
                dic[name]=values
                pass
            title = output.getQuantity() + " at time " + repr(time)
            pass
        else:
            #print(" here we are")
            name, values = self.getOutputValues(output)
            #print(" here we stay")
            name = name + " at time " + repr(time)
            pass
#        if (self.mpiEnv!=None): print " # ctm dbg outputTable %d %s"%(self.communicator.rank,name);#sys.stdout.flush()
#        if (self.mpiEnv!=None): print " # ctm dbg outputTable:",self.communicator.rank,values
#        if (self.mpiEnv!=None): print " # ctm dbg chemicalSpeciesList outputTable over #";#sys.stdout.flush()
        outputTable  =  Table(name)
        if self.environ():
#   coord = self.transportSolver.getCoordinatesValues()
            if (len(self.meshPointCoordinates) == 1):            
                outputTable.addColumn('X',self.meshPointCoordinates[0])
                pass         
            elif (len(self.meshPointCoordinates) == 2):
                outputTable.addColumn('X',self.meshPointCoordinates[0])           
                outputTable.addColumn('Y',self.meshPointCoordinates[1])
                pass
            else:          
                outputTable.addColumn('X',self.meshPointCoordinates[0])           
                outputTable.addColumn('Y',self.meshPointCoordinates[1])           
                outputTable.addColumn('Z',self.meshPointCoordinates[2])
                pass
            if dic=={}:
                title =  name + " t = %10.4e"%time 
                outputTable.addColumn(name,values)
                pass
            else:
                for name in dic.keys():
                    title =  name + " t = %10.4e"%time
                    outputTable.addColumn(title,dic[name])
                    pass
                pass
        return outputTable

    def outputField(self,output,current_time,time_iteration):        
        name, values = self.getOutputValues(output)
     
        field = self.transportSolver.createFieldByValues(name,values)
        
        field.setTime(current_time)

        field.setIteration(time_iteration)

        if output.getUnit():
            field.setComponentsUnits([output.getUnit()])
            pass
        
        name = output.getName()                                    
        if not (name.find('/')==-1):
            name =name.replace('/',' per ')
            pass
        field.setName(name[:26])

        return field

    def addChemicalOutputs(self,output):
        
        chemicalName = list(output.getChemicalName())
        for i in range(len(chemicalName)):
            cN = chemicalName[i]
            unKn = output.getUnknown()
            if type(unKn) is ListType:
                unK = unKn[i]
                pass
            else:
                unK = unKn
                pass
                
            if (cN not in self.chemicalOutputNames.keys()):
                chemicalOutput = ExpectedOutput(quantity = output.getQuantity(),
                                                unknown = unK,                                           
                                                unit =  output.getUnit(),
                                                name =  cN)
                self.chemicalOutputs.append(chemicalOutput)
                self.chemicalOutputNames[cN]=chemicalOutput
                self.chemicalOutputDict[output.getName()] = chemicalName
                pass
            pass
        return None

    def addImposedComputationTime(self,times):
        for time in times:
            if (time not in self.imposedComputationTimes):             
                self.imposedComputationTimes.append(time)
                pass
            pass
        
        return None

    def betweenComputation(self,current_time):
        new_delta_t = self.dT 
        for time in self.imposedComputationTimes:            
            if (time > current_time) and (time < current_time + self.dT):
                new_delta_t = min(new_delta_t,time - current_time)
                pass
            pass

        return new_delta_t

    def getThermalConductivity(self, porosityField, mineralityDependence = None):        
        """         
        Evaluation of the thermal conductivity on each node/cell
        
        As input a porosity fied
        
                Input : porosityField
                
                         conductivityLaw = conductivity law treatment to obtain the mean conductivity law
            mineralityDependence : optionally, the thermal conductivity can be computed as a function 
            of the minerality
            
                Output : mean thermal conductivity
        """
        #
        # problem in the definition of that function check it in reference to the lefebvre course
        #
        if mineralityDependence:
            for node in range(self.internalNodesNumber):
                self.solidThermalConductivity[node] = \
                self.conductivityLaw.eval(new_porosityField[node],self.initialPorosityValues[node],self.initial_effective_diffusion_values[iaux+j])
                pass
            pass
            for node in range(self.internalNodesNumber):
                thermalConductivities[node] = MeanThermalConductivityLaw.eval(  self.currentPorosity[node],\
                                                                                self.solidThermalConductivity[node],\
                                                                                self.fluidThermalConductivity)
                pass
            pass
        else:
            for node in range(self.internalNodesNumber):
                thermalConductivities[node] = MeanThermalConductivityLaw.eval(  self.currentPorosity[node],\
                                                                                self.solidThermalConductivity,\
                                                                                self.fluidThermalConductivity)
                pass
            pass
        return thermalConductivities   
    #
    # varying Heat Capacity
    #
    def getHeatCapacity(self,porosity_values,mineralityDependence = None):
        
        #         Return the heat capacity value for each cell
        #         Input : porosity_values
        #                  = heatcapacity law treatment to obtain the mean heat capacity treatment law
        #       mineralityDependence : optionally, the thermal conductivity can be computed as a function of the minerality
        #         Output : mean thermal conductivity 
        for cell in range(self.internalNodesNumber):
            heatCapacity[i] = self.heatCapacityLaw.eval([i],self.solidHeatCapacity,self.fluidHeatCapacity)
            pass
        return heatCapacity
    #
    # variable porosity: variable diffusion
    #
    def getEffectiveDiffusionFctPorosity(self,new_porosity_values):
        law = self.diffusionLaw
        length = len(self.initial_effective_diffusion_values)
        new_diffusion_values = [0.0]*length
        dim_anisotropy = length / self.internalNodesNumber
        if isInstance(law,WinsauerDiffusionLaw):
            percol_porosity = law.getPercolationThresholdPorosity()
            for node in range(self.internalNodesNumber):
                if ( (new_porosity_values[node]-percol_porosity) > self.small):
                    for j in range(dim_anisotropy):
                        new_diffusion_values[node*dim_anisotropy+j] =\
                        law.eval( new_porosity_values[node],self.initialPorosityValues[node],\
                                 self.initial_effective_diffusion_values[node*dim_anisotropy+j])
                        pass
                    pass
                else:
                    new_diffusion_values[node*dim_anisotropy:(node+1)*dim_anisotropy-1] = 0.
                    pass
                pass
            pass
        else:
            for node in range(self.internalNodesNumber):
                for j in range(dim_anisotropy):
                    new_diffusion_values[node*dim_anisotropy+j] =\
                        law.eval(new_porosity_values[node],\
                        self.initialPorosityValues[node],\
                        self.initial_effective_diffusion_values[node*dim_anisotropy+j])
                    pass
                pass
            pass
        return new_diffusion_values

    def cpuPrints(self):
        """
        function used to print cpu times
        """
        self.globalCPUTime = self.cpuTime() - self.globalCPUTime_deb
        
        print "----------------------";#sys.stdout.flush()
        print "End of the computation";#sys.stdout.flush()
        print "total CPU time : ",self.globalCPUTime;#sys.stdout.flush()

        if self.chat:
             print "chemical cpu time : ",self.chemistryCPUTime, "(",\
              self.chemistryCPUTime/self.globalCPUTime*100," % of global CPU time)" ;#sys.stdout.flush()
             print "transport  cpu time : ",self.transportCPUTime, "(",\
              self.transportCPUTime/self.globalCPUTime*100," % of global CPU time)";#sys.stdout.flush()
             print "call of chemicaltransport module init :",self.initialCPUTime, "(",\
                  self.initialCPUTime/self.globalCPUTime*100," % of global CPU time)";#sys.stdout.flush()
             print "communication chemical/module cpu time :", self.cpuChemicalCommunication, "(",\
                  self.cpuChemicalCommunication/self.globalCPUTime*100," % of global CPU time)";#sys.stdout.flush()
             print "communication transport/module cpu time :",self. cpu_with_transport_communication, "(",\
                  self.cpu_with_transport_communication/self.globalCPUTime*100," % of global CPU time)";#sys.stdout.flush()
             print "cpu source values :", self.cpu_sourceField, "(",\
                  self.cpu_sourceField/self.globalCPUTime*100," % of global CPU time)";#sys.stdout.flush()
             print "cpu work on list :", self.cpuOnList,"(",\
                  self.cpuOnList/self.globalCPUTime*100," % of global CPU time)";#sys.stdout.flush()
             print "cpu setResidualEvaluation :",self.cpu_tot_residu,"(",\
              self.cpu_tot_residu/self.globalCPUTime*100," % of global CPU time)";#sys.stdout.flush()
             print "cpu chemicalTransportOutput :",self.cpu_chemicalTransportOutput,"(",\
                  self.cpu_chemicalTransportOutput/self.globalCPUTime*100," % of global CPU time)";#sys.stdout.flush()
             pass
        print "----------------------";#sys.stdout.flush()
        print "\n\n";#sys.stdout.flush()
        return None

    def launch(self):
        """
        launching the simulation
        """
        #printm("name of the chemical tool: "+self.ChemicalComponent.lower())
        self.cpuTimeInitialisation()
                                                                                            # Chemical solver
                                                                                            # Data Base: The Database is mandatory
                                                                                            # for the definition of a problem
                                                                                            # 
        if (self.ChemicalComponent.lower() == "phreeqc"):
            self.chemicalSolver.setDataBase(self.chemistryDB)
                                                                                            # Chemical solver
                                                                                            # New Species
                                                                                            #
            self.chemicalSolver.setSpeciesBaseAddenda(self.problem.getSpeciesBaseAddenda())
                                                                                            # Chemical solver
                                                                                            # Kinetic Laws
                                                                                            #
        if self.kineticLaws:
            if not(self.timeUnit):
                raise Exception,'Time unit not given with kinetic case'
            self.chemicalSolver.setKineticLaws(self.kineticLaws)                      
            pass
            
        if self.activityLaw:
            self.chemicalSolver.setActivityLaw(self.activityLaw)
            pass
        if (self.TransportComponent == 'mt3d'):
            self.timeBoundaryConditionVariation = self.setTimeBoundaryConditionVariation()
            pass
        else:
            self.timeBoundaryConditionVariation = self.setTimeBoundaryConditionVariation()
            #raw_input("calling timeBoundaryConditionVariation")
            pass
                                                                                            #
                                                                                            # Chemical solver
                                                                                            # Chemical states for initial conditions
                                                                                            #
        internal_chemical_states = []
        if (self.TransportComponent == 'elmer'):
            self.transportSolver.getChemicalSolverIdentifier(self.chemicalSolver.version)
            #print ("ctmdbg self.chemicalSolver.version: %s\n",self.chemicalSolver.version)
            pass
        #raw_input("ctmdbg self.chemicalSolver.version")

        if (self.TransportComponent == 'mt3d'):
            # RQ : ne pourrait on pas avoir une methode mt3d qui fasse cela et se nomme
            # getIndexSubMesh ???
            self.internalNodesNumber = 0
            ideb=1
            for ini_cond in self.problem.initialConditions :
                ind_min=ini_cond.zone.zones[0].min
                ind_max=ini_cond.zone.zones[0].max
                self.internalNodesNumber+= (ind_max.i-ind_min.i+1)*(ind_max.j-ind_min.j+1)
                for i in range(ind_min.i,ind_max.i+1,1):
                    for j in range(ind_min.j,ind_max.j+1,1):
                        internal_chemical_states.append(ideb)
                        ideb+=1
                        pass
                    pass
                pass
            for boundaryCondition in self.problem.boundaryConditions :
                if (boundaryCondition.btype=='Flux'):
                    ind_min=boundaryCondition.boundary.zones[0].min
                    ind_max=boundaryCondition.boundary.zones[0].max
                    self.internalNodesNumber+= (ind_max.i-ind_min.i+1)*(ind_max.j-ind_min.j+1)
                    for i in range(ind_min.i,ind_max.i+1,1):
                        for j in range(ind_min.j,ind_max.j+1,1):
                            internal_chemical_states.append(ideb)
                            ideb+=1
                            pass
                        pass
                    pass
                pass
        
        elif (self.TransportComponent == 'elmer'):
            #raw_input(" ctmdbg elmer within launch ")
            self.listOfBoundaryPoints = []
                                                                                            #
                                                                                            # transsol
                                                                                            # we do not need to partition boundaries,
                                                                                            # because they do not belong to communication
                                                                                            # We have to establish a permutation list in 
                                                                                            # the case of region partitionning: parpertionList
                                                                                            #
            controlList = []
            for boundary in self.boundaryConditions:
                for node in self.mesh.getBody(boundary.boundary.getBodyName()).getBodyNodesList():
                    if node not in self.listOfBoundaryPoints:
                        self.listOfBoundaryPoints.append(node)
                        pass
                    pass
                pass
            print color.bold+" list of boundary points "+color.end, self.listOfBoundaryPoints, len(self.listOfBoundaryPoints)
            indParPer = 0
            #print "ctm debug parpertionList ",self.problem.initialConditions[0].getBody().getElements()
            #print "number of elements ",len(self.problem.initialConditions[0].getBody().getElements())
            #print "ctm debug parpertionList ",self.problem.initialConditions[0].getBody().getBodyNodesList()
            #print "number of points ",len(self.problem.initialConditions[0].getBody().getBodyNodesList())
            #print "ctm debug parpertionList list of boundary points",self.listOfBoundaryPoints
            #print "ctm debug internalNodesAnz",self.mesh.internalNodesAnz
            #raw_input()
            #
            self.parpertionList = [0]*self.mesh.internalNodesAnz
            #
            for initialCondition in self.initialConditions :
                index = initialCondition.getBody().getElements()
                
                for node in initialCondition.getBody().getBodyNodesList():
                    if node not in self.listOfBoundaryPoints and node not in controlList:
                        if (indParPer == self.mesh.internalNodesAnz):
                            print color.bold+" 2269 debug node:"+color.end+" %i"%(node)+color.bold+" indParPer:"+color.end+" %i len(controlList):  %i"%(indParPer, len(controlList))
                            print "self.mesh.internalNodesAnz: %i initialCondition.getBody().getBodyNodesList(): %i"%(self.mesh.internalNodesAnz, len(initialCondition.getBody().getBodyNodesList()))
                            #raise Warning, "Check the treatment of init. cond., "+\
                            #               "you probably forgot to treat some mesh body: %s"%str(indParPer)
                            pass
                        self.parpertionList[indParPer] = node-1
                        indParPer+=1
                        pass
                    pass
                controlList += initialCondition.getBody().getBodyNodesList()      
            
                internal_chemical_states.append((initialCondition.getValue(),index))
                self.internalNodesNumber = self.mesh.internalNodesAnz
              #
              # theta scheme
              #
                pass
            indParPer = 0
            #
            # We establish the list enabling to switch from transport
            # to chemistry
            #
            #raw_input("~~~~\nwithin chem trans init cond\n~~~~")
                                                                                            #               
                                                                                            # Chemical states for boundaries
                                                                                            #
        boundary_chemical_states = []
        boundary_vt_chemical_states = []
        if (self.TransportComponent == 'mt3d') :

            for boundary in self.boundaryConditions:
                ind_min=boundary.boundary.zones[0].min
                ind_max=boundary.boundary.zones[0].max
                for i in range(ind_min.i,ind_max.i+1,1):
                    for j in range(ind_min.j,ind_max.j+1,1):
                        boundary_chemical_states.append(ideb)
                        ideb+=1
                        pass
                    pass
                pass
            pass
        elif (self.TransportComponent == 'elmer') :
            for boundary in self.boundaryConditions:
                #print(boundary)
                #print(boundary.getChemicalStateValue())
                #raw_input("dbg ctm boundary")
                boundary_chemical_states.append(boundary.getChemicalStateValue())
                #for aqu in boundary.getChemicalStateValue().aqueousSolution.elementConcentrations:
                #    print(aqu.symbol, aqu.value)
                #raw_input("boundary getValue ") 
                pass
            pass
        
        # Chemical states for sources
        source_chemical_states = None
        if self.sources :
            source_chemical_states = []
            if (self.TransportComponent == 'mt3d'): 
                pass
            pass
                                                                                            #~~~~~~~~~~~~~~~~~~~~~~~
                                                                                            # initializing chemistry
                                                                                            #~~~~~~~~~~~~~~~~~~~~~~~
        self.StatesBounds = {}
        inputName = self.name.replace(" ","_")
        output = inputName+".phout"
                                                                                            #
                                                                                            # phreeqC
                                                                                            #
        if (self.ChemicalComponent.lower() == "phreeqc"):
            chemicalStateList = self.chemicalSolver.setStatesBounds(self.problem, self.StatesBounds, self.mesh)
            
            self.chemicalSolver.setChemicalStateList( chemicalStateList, self.variablePorosityOption)
            #print("inputName: ",inputName)
            #print("output:    ",output)
            #print("StatesBounds: ",self.StatesBounds)
            #print("trace: ",self.trace)
            #print("inn: ",self.internalNodesNumber)            
            #print("chemParam: ",self.chemicalParameters)
            #print("chemical state list: ", chemicalStateList)
            #raw_input()
            self.chemicalSolver.init(inputName,\
                                     output,\
                                     self.StatesBounds,\
                                     self.trace,\
                                     self.internalNodesNumber,\
                                     chemicalParameters = self.chemicalParameters)                                        
            pass
        elif (self.ChemicalComponent.lower() == "toughreact"):
        
            chemicalStateList = self.chemicalSolver.setStatesBounds(self.problem,self.StatesBounds,self.mesh)
            
            self.chemicalSolver.init()
            self.chemicalSolver.getCellNumber()
            #printm(" ctmdbg chemicalsolver init and getCellNumber: "+str(self.chemicalSolver.getCellNumber()),True)
            pass
        #
                                                                                        #~~~~~~~~~~~~~~~~~~~~~~~~~
        #raw_input(" initialisation of chemical solvers is over\n"+"*\n")
        if (self.ChemicalComponent.lower() == "phreeqc"):
            for i in self.chemicalParameters:
                if i.count("RATES"):
                    self.kineticLaws = 1
                    pass
                pass
            pass
        # Component species retrieval
        self.componentList = self.chemicalSolver.getPrimarySpeciesNames()
        if self.mpiEnv != None:
            print "ctmdbg mpiEnv",self.componentList,self.communicator.rank
            pass
        self.componentAnz = len(self.componentList)
        self.chemUnknownAnz = self.componentAnz

        #conc_aqu_boundary = self.chemicalSolver.getMobileConcentrationField('boundary') 
        #print "ctmdbg mpi 01";sys.stdout.flush()
        #raw_input("ctmdbg mpi 01")

        self.aqueousCn = self.chemicalSolver.getMobileConcentrationField('internal')
        #print self.aqueousCn
        #printm("getMobileConcentrationField ",True)
        #sFFile = open("sF2224File","w");sFFile.write(" %i\n"%(len(self.aqueousCn)))
        #for i in range(0,len(self.aqueousCn)):
        #    sFFile.write(" %i %15.10e\n"%(i,self.aqueousCn[i]))
        #sFFile.close()
        
        #print "ctmdbg mpi 02";#sys.stdout.flush()
#        if self.environ(): 
#            print " ctmdbg Milestone: \n";#sys.stdout.flush()
#            print len(self.aqueousCn),self.aqueousCn[0:10];#sys.stdout.flush()
#            pass
        self.aqueousCkp1 =  [0.0]*len(self.aqueousCn)
        self.data = numpy.zeros((len(self.aqueousCkp1),), numpy.float)
        dim = 1
        #print "ctmdbg mpi 1",self.mpiEnv;#sys.stdout.flush()
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~";#sys.stdout.flush()                      #~~~~~~~~~~~~~~~~~~~~~~~~~
        print "~ ctmdbg Transport initialisation~";#sys.stdout.flush()                      # Transport initialisation
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~";#sys.stdout.flush()                      #~~~~~~~~~~~~~~~~~~~~~~~~~
#
        if (self.mpiEnv == None):
        
                                                                                            #
                                                                                            # call of the transportinitialisation method
                                                                                            # of the chemicaltransport module.
                                                                                            #
            self.transportInitialisation()
                                                                                            #
                                                                                            #
                                                                                            #
            if (self.TransportComponent == 'mt3d'): 
                self.meshPointCoordinates = self.transportSolver.getCoordinatesValues()
                pass
            pass
        elif self.mpiEnv != None:
            dim = numpy.array(1)
            length0 = numpy.array(1)
            length1 = numpy.array(1)
            
            if (self.TransportComponent == 'elmer') and (self.communicator.rank == 0):
                print "ctm dbg setRank method ",self.communicator.rank;#sys.stdout.flush()
                self.transportSolver.setRank(self.communicator.rank)
                pass
                                                                                            #
                                                                                            # to get the mesh point coordinates on each node
                                                                                            #
            if self.communicator.rank == 0:
                self.transportInitialisation()
                #self.meshPointCoordinates = self.transportSolver.getCoordinatesValues()
                #print "ctmdbg type(self.meshPointCoordinates",type(self.meshPointCoordinates);#sys.stdout.flush()
#                print self.meshPointCoordinates[0][100]
                #dim[0] = len(self.meshPointCoordinates)
                #length0[0] = len(self.meshPointCoordinates[0])
                #length1[0] = len(self.meshPointCoordinates[1])
                #print " ctmdbg dim length ####################",dim,length0,length1;#sys.stdout.flush()
                pass
            else:
                self.vtkFileWriter = VtkFileWriter(self.mesh,\
                                                   self.initialConditions,\
                                                   self.chemicalSolver,\
                                                   self.transportSolver,\
                                                   self.TransportComponent)
                pass
            self.communicator.Bcast(dim,0)
            self.communicator.Bcast(length0,0)
            self.communicator.Bcast(length1,0)
            if self.communicator.rank != 0:
                print type(dim),dim[0],len(dim)
                if dim[0] == 1:
                    self.meshPointCoordinates = [[0.0]*length0[0]]
                    pass
                elif dim[0] == 2:
                    print " ctm dbg we treat two dimensions";#sys.stdout.flush()
                    self.meshPointCoordinates = [[0.0]*length0[0],[0.0]*length1[0]]
                    pass
                elif dim[0] == 3:
                    self.meshPointCoordinates = [[0.0]*length0[0],[0.0]*length1[0],[0.0]*length0[0]]
                    pass

        if self.variablePorosityOption:
            #
            # porosity varying
            #
            for node in range(self.internalNodesNumber):
                self.chemicalSolver.setInitialNodePorosity(node, self.initialPorosityValues[node])
                pass
            print " ctmdbg porosity has been initialised ";#sys.stdout.flush()
            pass

        if self.chat:
            self.initialCPUTime = self.cpuTime() - self.globalCPUTime_deb
            print " ctmdbg cpu for  chemicaltransportmodule.init() ",(self.initialCPUTime);#sys.stdout.flush()
            pass
        #
        # initial time and initial time step initialisation
        #
        self.timeStepInitialisation()

        # chemical zero 1.e-12
        if (self.ChemicalComponent.lower() == "phreeqc"): self.small = self.chemicalSolver.getChemicalZero()
        #
        # We update the imposedComputationTimes list
        #
        if self.timeBoundaryConditionVariation != None:
            for bcStates in  self.timeBoundaryConditionVariation:
                self.imposedComputationTimes.append(bcStates[0])
                pass
            self.imposedComputationTimes.sort()
            pass
            
        if (self.mpiEnv == None):
            if (self.TransportComponent == 'mt3d'):
                self.transportSolver.getBoundaryConditionTimeVariation(self.timeBoundaryConditionVariation)
                pass
            pass
        elif self.mpiEnv!=None:
            if (self.communicator.rank == 0) and (self.TransportComponent == 'mt3d'):
                self.transportSolver.getBoundaryConditionTimeVariation(self.timeBoundaryConditionVariation)
                pass
            pass

        self.aqueousCn = self.chemicalSolver.getMobileConcentrationField('internal')
        #print " ctmdbg get MobileConcentration over ",len(self.aqueousCn);#sys.stdout.flush()
        
        #printm(" present line ");print len(self.aqueousCn)
        #printm(" ctm dbg set MobileConcentration \n",1);#sys.stdout.flush()
        self.chemicalSolver.setMobileConcentrationValues('internal',self.aqueousCn)
        #printm(" present line ")
        #printm(" set MobileConcentration over ",1);#sys.stdout.flush()
        self.chemicalSolver.equilibrate()
        #print " ctm dbg equi over ";#sys.stdout.flush()
        #tot#o  = self.chemicalSolver.getJacobian()
        if (self.ChemicalComponent.lower() == "phreeqc"):
            self.fixedCn = self.chemicalSolver.getImmobileConcentrationField('internal')
        elif (self.ChemicalComponent.lower() == "toughreact"):
            #
            # method to be written
            #
            pass
        
        if self.variablePorosityOption:
            self.currentPorosity = copy(self.initialPorosityValues)
            if self.diffusionLaw:
                self.initial_effective_diffusion_values = self.transportSolver.getEffectiveDiffusionValues()
                pass
            pass
        #
        # the two lists created here are used resp. for source term evaluation and fixed point algorithm
    #
        self.sourceField = [0.0]*self.componentAnz*self.internalNodesNumber
        self.fixedCk    = [0.0]*self.componentAnz*self.internalNodesNumber

        if self.convergenceCriterionLevel == 3:
            self.conc_fix_k0 = [0]*self.componentAnz*self.internalNodesNumber
            pass

        # Initialisation for the "initialisationOption"
        if self.initialisationOption == 2:
            self.conc_fix_prec = []
            self.conc_fix_prec.append([0]*self.componentAnz*self.internalNodesNumber)
            self.conc_fix_prec.append([0]*self.componentAnz*self.internalNodesNumber)
            if ((self.couplingAlgorithm=='GC') or (self.couplingAlgorithm=='PF')):
                self.conc_tot_prec = []
                self.conc_tot_prec.append([0]*self.componentAnz*self.internalNodesNumber)
                self.conc_tot_prec.append([0]*self.componentAnz*self.internalNodesNumber)
                pass
            self.deltat_prec = []
            self.deltat_prec.append(-2.)
            self.deltat_prec.append(-1.)
            self.ind_n   = 0
            self.ind_np1 = 1
            if self.variablePorosityOption:
                self.porosity_prec = []
                self.porosity_prec.append([0]*self.internalNodesNumber)
                self.porosity_prec.append([0]*self.internalNodesNumber)
                self.porosity_np2 = [0]*self.internalNodesNumber
                pass
            pass

        # variable porosity : creation of a list for porosity at the fixed point loop iteration
        if self.variablePorosityOption:
            self.kPorosityField    = [0.]*self.internalNodesNumber
            self.kp1PorosityField  = [0.]*self.internalNodesNumber
            pass
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~";#sys.stdout.flush()                    #~~~~~~~~~~~~~~~~~~~~~~~~~
        print "~ ctmdbg Transport init method call~";#sys.stdout.flush()                    # Transport initialisation
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~";#sys.stdout.flush()                    #~~~~~~~~~~~~~~~~~~~~~~~~~
        
                                                                                            #
                                                                                            # we will mention the chemistry solver in the sif file
                                                                                            # 
        if self.mpiEnv == None:
            if (self.TransportComponent == 'mt3d'):
                sizeumt = os.path.getsize('Monod.umt')
                if sizeumt == 0:
                    while sizeumt == 0:
                        sizeumt = os.path.getsize('Monod.umt')
                        pass
                    pass
            #print "ctmdbg transport init method";#sys.stdout.flush()
            #print "self.problem.__class__.__name__.lower() ",self.problem.__class__.__name__.lower()
            #raw_input()
            if self.problem.__class__.__name__.lower() == "chemicaltransportproblem":
                self.transportSolver.setProblemType("chemicaltransport")
                pass
            elif self.problem.__class__.__name__ == "thmcproblem":
                self.transportSolver.setProblemType("thmc")
                pass
                                                                                            #
                                                                                            # call of the init method
                                                                                            # which, for Elmer, enables to write the simulation file
                                                                                            # for the transport.
                                                                                            #
            self.transportSolver.init(self.problem.getName())
                                                                                            #
            if (self.TransportComponent == 'elmer'):
                                                                                            #
                                                                                            # we check which problem we have to solve
                                                                                            # and call some specific initialisation methods
                                                                                            #
                if self.problem.__class__.__name__ == "chemicaltransportproblem":
                    self.transportSolver.setProblemType("chemicaltransport")
                elif self.problem.__class__.__name__ =="thmcproblem":
                    self.transportSolver.setProblemType("thmc")
                #print " dbg mesh point coordinates "
                self.meshPointCoordinates = self.transportSolver.getCoordinatesValues()
                #print " setPorosityField(self.initialPorosityValues)",
                #print self.initialPorosityValues,len(self.initialPorosityValues)
                                                                                            #
                                                                                            # updating the parameters for rhe two phases borehole
                                                                                            #
                if self.transportSolver.parameterDico["oneDimensionalBoreHole"] and self.transportSolver.parameterDico["vapor"]:
                    self.transportSolver.setTwoPhasesBoreholeParameters(self.meshPointCoordinates[0])
                    pass
                print self.meshPointCoordinates
                print len(self.meshPointCoordinates)
                #raw_input(color.bold+" debug20072016 list of node coordinates "+color.end)
                self.transportSolver.setPorosityField(self.initialPorosityValues)
                #print " in porosity ",len(self.initialPorosityValues)
                if "read" in self.transportSolver.advConv.lower():
                    self.transportSolver.readVelocity()
                   #raw_input ("read velocity over")
                #raw_input("read velocity over")
            
            self.transportSolver.setTimeStep(self.initialTimeStep)
            print "self.transportSolver.setTimeStep",len(self.aqueousCn);#sys.stdout.flush()
            pass
            self.transportSolver.setConcentrationValues(self.aqueousCn)
            print "self.transportSolver.setConcentrationValues";#sys.stdout.flush()
            if (self.TransportComponent == 'elmer'):
                self.transportSolver.advanceTime(self.initialTimeStep)
                pass
            else:
                self.transportSolver.advanceTime()
                pass
            #
            # We set the temperature field
            #
            if self.temperature:
                self.transportSolver.setTemperatureField(self.chemicalSolver.getTemperatureField())

        elif self.communicator.rank==0:
            print "ctm dbg transport init method rank: ",self.communicator.rank==0;#sys.stdout.flush()
            print "ctm dbg transport init method rank: ",self.elmerSolverDico;#sys.stdout.flush()
            #self.transportSolver.setTransportParameter(self.elmerSolverDico)
            self.transportSolver.init(self.problem.getName())
            self.meshPointCoordinates = self.transportSolver.getCoordinatesValues()
            self.transportSolver.setPorosityField(self.initialPorosityValues)
            self.transportSolver.setTimeStep(self.initialTimeStep)
            if self.temperature:
                self.transportSolver.setTemperatureField(self.chemicalSolver.getTemperatureField())
                pass
            self.transportSolver.setConcentrationValues(self.aqueousCn)
            if (self.TransportComponent == 'elmer'):
                self.transportSolver.advanceTime(self.initialTimeStep)
                pass
            else:
                self.transportSolver.advanceTime()
                pass
            pass
                                                                                            #
                                                                                            # Time loop 
                                                                                            #
        self.convergenceAnalysisParameter = 1

        self.increment = 2
        print " launch ended ";#sys.stdout.flush()
        return None

    def additionalSourceEvaluation(self):
        """
        Evaluation of additionnal source values
        """
        length = self.componentAnz * self.internalNodesNumber
        #raw_input("we go through")
        if (self.couplingAlgorithm != "TC"):
            #
            # Porosity dependance
            #
            if not self.variablePorosityOption:
            #
            # porosity is constant
            #

#                print " control of source porosity",length,self.componentAnz,len(self.initialPorosityValues)
#                #raw_input("porosity")
#                print self.fixedCk[1200:1500]
#                #raw_input("self.fixedCk")
#                print self.fixedCn[1200:1500]
#                #raw_input("self.fixedCn   ")
#                print "length ",length,self.componentAnz
#                print "self.currentPorosity",self.initialPorosityValues[0]
#                print "self.internalNodesNumber",self.internalNodesNumber
#                print "self.variablePorosityOption",self.variablePorosityOption
                #raw_input()
                self.sourceField = fixedpoint_source(length,
                                                     self.fixedCk, self.fixedCn,\
                                                     self.initialPorosityValues,\
                                                     self.initialPorosityValues,\
                                                     self.componentAnz,\
                                                     self.internalNodesNumber,\
                                                     self.variablePorosityOption)
                #print "self.sourceField: ",self.sourceField
                #raw_input()

#                for component in range(self.componentAnz):
#                    indComp = component * self.internalNodesNumber
#                    for node in range(self.internalNodesNumber):
#                        ind = indComp + node
#                        self.sourceField[ind] = self.initialPorosityValues[node] *\
#                                                ( self.fixedCk[ind] - self.fixedCn[ind] )

            else:
                #
                # porosity is varying
                #
                #print " ctmdbg self.variablePorosityOption",self.variablePorosityOption, self.internalNodesNumber, self.kp1PorosityField[0]
                #print "ctmdbg self.variablePorosityOption",self.currentPorosity[0]
                #print self.kp1PorosityField
                self.sourceField = fixedpoint_source(length, 
                                                     self.fixedCk,
                                                     self.fixedCn,
                                                     self.currentPorosity,
                                                     self.kp1PorosityField,
                                                     self.componentAnz,
                                                     self.internalNodesNumber,
                                                     self.variablePorosityOption)
#                if self.variablePorosityOption:
#                    for comp in range(self.componentAnz) :
#                        k=comp*self.internalNodesNumber
#                        for k1 in range (self.internalNodesNumber) :
#                            ind = k + k1
#                            self.sourceField[ind]-= self.aqueousCn[ind]*((self.kp1PorosityField[k1] - self.currentPorosity[k1]))
#                            #self.sourceField[ind]*=-1.
#                            pass
#                        pass
#                    pass
                self.transportSolver.setPorosityField(self.kPorosityField)
                pass

    def messageDebug(self,message,conc):
        for comp in range(self.componentAnz) :
            k=comp*self.internalNodesNumber
            for node in range (self.internalNodesNumber) :
                ind = k+node;
                if conc[ind]<self.minValue:
                    print message,' < ' ,self.minValue,' FOR INTERNAL NODE i',node,'component ',comp,': ',comp,'ind =',ind , ' :',conc[ind];#sys.stdout.flush()
                    pass
                if conc[ind]>self.maxValue:
                    print message, ' > ' ,self.maxValue,' FOR INTERNAL NODE i',node,'component ',comp,': ',comp,'ind =',ind , ' :',conc[ind];#sys.stdout.flush()
                    pass
                pass
            pass
        pass
    
    def oneTimeStep(self):
        """
        It is used to simulate one time step including the fixed point algorithm and the outputs.
        
        # \todo : automatic call to Darcy velocity computation in TransportComponent when permeability is modified
        #         automatic call to dispersion computation (= function of Darcy velocity) in TransportComponent
        #
        """
#        print "ctmdbg one time step "
        if self.curveTable:
            print "ctmdbg one time step  self.curveTable"
            self.timeInteractivePlot(self.simulatedTime,self.timeStepNumber,
                                     self.curveTable,
                                     self.curve,
                                     self.TimeGplot,
                                     self.pointtoplot,
                                     self.listofSpeciestoplot,
                                     self.componentList,
                                     self.internalNodesNumber,
                                     self.aqueousCn,
                                     self.plotFrequency,
                                     ' mol/l',
                                     0)
            pass
        #print "ctmdbg self.dT",self.dT
        self.simulatedTime = self.simulatedTime+self.dT
       #
       # unstationary boundary condition management
       #
        if self.mpiEnv == None:
           if (self.TransportComponent == 'mt3d'):
               self.transportSolver.setBoundaryConditionsTimeVariation(self.simulatedTime)
               pass
           pass
        elif self.communicator.rank == 0:
            if (self.TransportComponent == 'mt3d'):
                self.transportSolver.setBoundaryConditionsTimeVariation(self.simulatedTime)
                pass
            pass
        self.timeStepNumber += 1
        if self.environ():
            print "------------------------------------------------------------------";#sys.stdout.flush()
            print "Chemical / transport simulation, Time: ", '%10.4e'%self.simulatedTime ,\
                  ", time step:",'%10.4e'%self.dT, "(time iteration #",self.timeStepNumber, " )";#sys.stdout.flush()

        if self.chat : cpu0 = self.cpuTime()                                                # Initialisation
        
        self.fixedCk = copy(self.fixedCn)                                                   # Initial value of fixedCk and porosity_values_k
        
        if self.variablePorosityOption and self.timeStepNumber == 1:
            self.kp1PorosityField = copy(self.currentPorosity)
            pass

        if self.convergenceCriterionLevel == 3: self.conc_fix_k0 = copy(self.fixedCn)       # Optimisation of the initial values computation

        if self.chat: self.cpuOnList += (self.cpuTime()-cpu0)

        if self.convergenceAnalysisParameter == 1: self.chemicalSolver.aqueousStateDump()

        convergence = 0;it = 0
        couplingAlgorithmError = self.couplingPrecision

        #
        # The TEMPERATURE is set and evaluated apart from the fixed point algorithm
        # just one time step for the temperature
        #       
        if self.temperature and (self.TransportComponent == 'elmer'):
            self.transportSolver.HeatOneTimeStep()
#            self.transportSolver.SaturatedHydraulicOneTimeStep()
            
        if self.temperature:
            temperature = self.transportSolver.getTemperatureField()
            self.chemicalSolver.setTemperatureField("internal",temperature)

        # variable porosity -> computation of permeability to change velocity and dispersion in transport
        #if self.variablePorosityOption:
        # TODO : define self.getVelocityFctPorosity(self.porosity_values)
        #           and self.getDispersionFctDarcy(darcyVelocity_n)
        #      redefine self.transportSolver.setDarcyVelocity(darcyVelocity_n)
        #           and self.transportSolver.setKinematicDispersion(dispersivity_n) ?
        # Darcy velocity computation = function of porosity
        ## calcul de la permeabilite a inclure dans methode getVelocity
        ## permeability computation = function of porosity (Kozeny-Carman ou autre ?)
        ## permeability = self.getPermeabilityValues(porosity_values_0,porosity_values_n,permeability_0)
        # permeability_n = self.getPermeabilityFctPorosity(porosity_values_n,law_type)
        # self.transportSolver.setPermeability(permeability_n)
        # TODO : automatic call to Darcy velocity computation in TransportComponent when permeability is modified
        #        automatic call to dispersion computation (= function of Darcy velocity) in TransportComponent
        #pass
        #
        # Fixed  point iteration loop indexed by it.
        #
        #print "ctm dbg Picard loop 0";#sys.stdout.flush()
        while (couplingAlgorithmError >= self.couplingPrecision ) and (it < self.maxIterationNumber):
            if self.chat:
                cpuOneIteration = self.cpuTime()
                pass
            it += 1
            #
        # variable porosity : initialisation of porosity
            # at first iteration, porosity_values_k = porosity_values_n
            #              after, porosity_values_k = porosity_values_kp1
            #
            if self.variablePorosityOption:
                self.kPorosityField = self.kp1PorosityField
                #copyList(self.kp1PorosityField,self.kPorosityField)
                pass

            # ---------- I. Transport step ---------- 

            # construction of transport equation
                
            # variable porosity : computation of diffusion
            if self.diffusionLaw :
                # Types of diffusive law : Winsauer (Archie,Lagneau), exponential
                effective_diffusion_k = self.getEffectiveDiffusionFctPorosity(self.kPorosityField)
                self.transportSolver.setDiffusionValues(effective_diffusion_k)
                self.effective_diffusion_k = effective_diffusion_k
                pass
                                                                                            #
                                                                                            # additional source values
                                                                                            #
            if self.mpiEnv == None:
                self.additionalSourceEvaluation()
                #print "ctm dbg additionalSourceEvaluation 2661",len(self.sourceField);sys.stdout.flush()
                self.transportSolver.setAdditionalSourceValues(self.sourceField)
                pass
            elif self.communicator.rank==0:
                self.additionalSourceEvaluation()
                self.transportSolver.setAdditionalSourceValues(self.sourceField)
                pass
            #sFFile = open("sF2677File","w");sFFile.write(" %i\n"%(len(self.sourceField)))
            #for i in range(0,len(self.sourceField)):
            #    sFFile.write(" %i %15.10e\n"%(i,self.sourceField[i]))
            #sFFile.close()
            #raw_input(" ctmdbg 2677 self.aqueousCkp1")
            
            if self.chat: cpuSource = self.cpuTime()
#            
            cpuTimeBeg = self.cpuTime()
#            print " ctm dbg AqueousComponentOneTimeStep"
            if self.mpiEnv == None:
                #print "ctmdbg transportSolver.AqueousComponentOneTimeStep"
                self.transportSolver.AqueousComponentOneTimeStep()                          # transport step <- Cn+1
                pass
            elif self.communicator.rank==0:
                self.transportSolver.AqueousComponentOneTimeStep()
                pass
            if self.mpiEnv != None:
                self.communicator.barrier()
                pass
        
            cpuTimeEnd = self.cpuTime()
            self.transportCPUTime += (cpuTimeEnd - cpuTimeBeg)
            if self.chat:
                self.cpu_sourceField+=(cpuSource - cpuOneIteration)
                print "    cpu for  self.transportSolver.run() ",(cpuTimeEnd - cpuTimeBeg);#sys.stdout.flush()
                self.cpu_with_transport_communication+=(cpuTimeBeg - cpuSource)
                pass
            #
            # We retrieve the aqueous concentrations indexed by n+1 over time and k+1 for the picard 
            #
            if self.mpiEnv == None:
                self.aqueousCkp1 = self.transportSolver.getConcentrationValues()            # aqueous conc. indexed by
                #print "self.aqueousCkp1: ",len(self.aqueousCkp1)
                #raw_input("2704")
                pass                                                                        # n+1/k+1 for the picard
                                                                                            #
            elif self.communicator.rank==0:                                       #
                self.aqueousCkp1 = self.transportSolver.getConcentrationValues()            # aqueous conc. indexed by
                pass
            #print "ctmdbg onets aqueousCkp1",self.aqueousCkp1[302:310]
            #ckp1File = open("ckp12713File","w");ckp1File.write(" %i\n"%(len(self.aqueousCkp1)))
            #for i in range(0,len(self.aqueousCkp1)):
            #    ckp1File.write(" %i %15.10e\n"%(i,self.aqueousCkp1[i]))
            #ckp1File.close()
            #raw_input(" ctmdbg 2713 self.aqueousCkp1")
                                                                                            # n+1/k+1 for the picard
            if self.mpiEnv != None:
                self.communicator.barrier()
                data = numpy.array(self.aqueousCkp1)
                self.communicator.Bcast(data,0)
                if self.communicator==0: print " mpi rank 0 debug ",len(data)
                    #print " mpi broadcast ",self.aqueousCkp1
                pass
                if self.communicator.rank!=0: self.aqueousCkp1 = data.tolist()
                    
            if self.debug:
                self.messageDebug("!!!WARNING!!! FROM TRANSPORT COMPONENT, AQUEOUS CONCENTRATION ",self.aqueousCkp1)
                pass

            if self.chat:
                cpu_aqu_kp1 = self.cpuTime()
                self.cpu_with_transport_communication+=(cpu_aqu_kp1-cpuTimeEnd)
                pass
                
            # ----------  II. Computation of the total concentration ---------- 
            if self.chat:
                cpu_add = self.cpuTime()
                pass
            # ----------  III. Chemistry step ---------- 
            if self.kineticLaws:
                self.chemicalSolver.setTimeStep(Time(self.dT,self.timeUnit))                # kinetic
                pass

            #print "self.chemicalSolver.setMobileConcentrationValues ",len(self.aqueousCkp1)
            self.chemicalSolver.setMobileConcentrationValues('internal',self.aqueousCkp1)               # setMobileconcentrationvalues
            #print "self.chemicalSolver.setMobileConcentrationValues over",len(self.aqueousCkp1)
            #ckp1File = open("ckp12744File","w");ckp1File.write(" %i\n"%(len(self.aqueousCkp1)))
            #for i in range(0,len(self.aqueousCkp1)):
            #    ckp1File.write(" %i %15.10e\n"%(i,self.aqueousCkp1[i]))
            #ckp1File.close()
            #raw_input(" ctmdbg self.aqueousCkp1")
            #if self.communicator.rank == 0: print " ctm dbg proc 0 ",len(self.aqueousCkp1);#sys.stdout.flush()
            #if self.communicator.rank == 1: print " ctm dbg proc 1 ",len(self.aqueousCkp1);#sys.stdout.flush()
                                                                                                        #
                                                                                                        # the first time step is non iterative
                                                                                                        #
            if self.couplingAlgorithm=="NI" or self.timeStepNumber == 1 :
                couplingAlgorithmError = 1.e-15       # non iterative algorithm
                pass
                
            cpuTimeBeg = self.cpuTime()
            
            if self.chat:
                self.cpuChemicalCommunication +=(cpuTimeBeg - cpu_add)
                pass

            self.chemicalEquilibrium = self.chemicalSolver.equilibrate()                    # chemistry equilibrium

            cpuTimeEnd = self.cpuTime();self.chemistryCPUTime += (cpuTimeEnd - cpuTimeBeg)

            if self.chat:
                print "\n  cpu for  self.chemicalSolver.equilibrate() %e\n"%(cpuTimeEnd - cpuTimeBeg);
                pass

            if not(self.chemicalEquilibrium):
                print "Oops, chemical failed",self.chemicalEquilibrium;#sys.stdout.flush()
                break
            if self.variablePorosityOption:
                #print "first try "
                #print self.chemicalSolver.getPorosity()
                #raw_input("getPorosity")
                #print "  ctmdbgn before getPorosityField\n"
                #print self.chemicalSolver.getPorosityField()
                #raw_input(" ctmdbg checking of self.chemicalSolver.getPorosityField\n")
                self.kp1PorosityField = self.chemicalSolver.getPorosityField()
                #print "  ctmdbgn %d  %15.10e  %15.10e %15.10e %15.10e\n"\
                #%(self.timeStepNumber, self.simulatedTime, self.currentPorosity[0], self.currentPorosity[1], self.currentPorosity[2])
                #pass
                #raw_input("ctm porosity evaluation")
            self.fixedCkp1 = self.chemicalSolver.getImmobileConcentrationField('internal')
            
            if self.debug: self.messageDebug("!!!!!!!!!!WARNING!!!!!! FROM CHEMICAL COMPONENT, FIX CONCENTRATION",self.fixedCkp1) 

            if self.chat:                
                cpuGetFixedConcentration = self.cpuTime()
                self.cpuChemicalCommunication +=( cpuGetFixedConcentration - cpuTimeEnd )
                pass

            if self.chat: cpu0 = self.cpuTime()
                
            if self.couplingAlgorithm=="CC" and  self.timeStepNumber != 1 :
                couplingAlgorithmError,indierror,indjerror = residualEvaluation(self.componentAnz,
                                                                                self.internalNodesNumber,
                                                                                self.small,
                                                                                1.e+6,
                                                                                self.fixedCkp1,
                                                                                self.fixedCk)
                pass
            if self.chat:
                cpu_residu = self.cpuTime()
                self.cpu_tot_residu+=(cpu_residu - cpu0)
                pass

            # ---------- V. re-affectation to the values for the next picard iteration step ---------- 
            self.fixedCk = copy(self.fixedCkp1)

            if self.variablePorosityOption:
                self.kPorosityField[:] = self.kp1PorosityField[:]
                pass
           
            if self.chat:
                cpu2=self.cpuTime()
                self.cpuOnList += (cpu2-cpu_residu)
                pass
#            if self.timeStepNumber == 1: couplingAlgorithmError = 1.e-15

            if self.couplingAlgorithm == "CC"  and  self.timeStepNumber != 1 :
                if self.environ():
                    if self.chat:
                        print "Max error, iteration: %d : %12.6e at point: %d unk.: %d"\
                        %(it,couplingAlgorithmError,indierror,indjerror);#sys.stdout.flush()
                        pass
                    else:
                        print "%20s %15.8e, iteration: %5d at point: %5d"\
                        %("Max error: ",couplingAlgorithmError,it,indierror);#sys.stdout.flush()
                        pass
                    pass
                pass
                                                                                            #
                                                                                            # End of fixed point loop (While)
                                                                                            #
                                                                                            # Chemical/transport convergence being reached
                                                                                            #
        if self.chemicalEquilibrium and couplingAlgorithmError <= self.couplingPrecision:
            if self.temperature:
                self.transportSolver.setTemperatureField(temperature)
                self.chemicalSolver.setTemperatureField('internal',temperature)
                pass

            if (self.mpiEnv == None):
                print "==>  Convergence error is: ", \
                  couplingAlgorithmError ,", it. = ", it," Mem. ",getMemory(),"\n",;#sys.stdout.flush()
                pass
            elif (self.communicator.rank ==0):
                print "==>  Mpi Convergence error is: ", \
                  couplingAlgorithmError ,", it. = ", it," Mem. ",getMemory(),"\n",;#sys.stdout.flush()
                pass

            if self.variablePorosityOption: self.currentPorosity = copy(self.kPorosityField)# porosity from one step to the other
                                                                                            #
                                                                                            # the call of chemicalTransportOutput is made on each processor
                                                                                            # due to a chemical getoutput; it includes interactive outputs
                                                                                            #
            #print " at the output level"
            self.chemicalTransportOutput(self.finalTime, it, couplingAlgorithmError)        # user outputs
            #print " after the output level"

            if (self.environ()):
                if self.chat:
                    outputCPU = self.cpuTime()
                    self.cpu_chemicalTransportOutput+=(outputCPU - cpu2)
                    pass
                pass
            # Reaching convergence, we update unknowns Ci(tn) => Ci(tn+1) and advance in time
            # advance in timeIt is just a list affectation.
            # TO DO : attention avec aqueousCkp1, resultats de la demi-etape de transport ou de chimie.
            # New value for aqueousCkp1,fixedCk ...
            # (be sure to have the mass conservation) 
                                                                                            #
            if self.couplingAlgorithm != "NI":                                              # using an iterative algo.
                                                                                            # we update for the next
                                                                                            # step
                self.fixedCn = self.chemicalSolver.getImmobileConcentrationField('internal')
                self.aqueousCn = self.chemicalSolver.getMobileConcentrationField('internal')
                #print " ctmdbg aqueousCn ",self.aqueousCn[0:5]
                if (self.environ()):
                    #print " ctmdbg self.environ",self.environ()
                    self.transportSolver.setConcentrationValues(self.aqueousCn)
                    pass
                pass
            else:
                #print "self.aqueousCn = self.chemicalSolver.getMobileConcentrationField"
                self.aqueousCn = self.chemicalSolver.getMobileConcentrationField('internal')
                #print "self.aqueousCn = self.chemicalSolver.getMobileConcentrationField"
                self.transportSolver.setConcentrationValues(self.aqueousCn)
                pass
                                                                                            #
                                                                                            # Advance in time for transport
                                                                                            #
            cpuTimeBeg = self.cpuTime()

            if self.couplingAlgorithm == "NI":
                if self.variablePorosityOption:
                    #print "ctm dbg currentPorosity currentPorosity",self.couplingAlgorithm
                    for comp in range(self.componentAnz) :
                        k=comp*self.internalNodesNumber
                        for node in range (self.internalNodesNumber) :
                            ind = k + node
                            pass
                        pass
                    #
                    # d(wC+(1-w)F))/dt = 0  Balance using the strang algorithm
                    # We have evaluated a new porosity kp1 
                    # and we want to determine the actual associated concentrations
                    #     
                    #
                    self.aqueousCn[ind] = ( self.aqueousCn[ind]*self.currentPorosity[node]   - \
                                    self.fixedCkp1  [ind]*(1-self.kp1PorosityField[node]) +  \
                                (1-self.currentPorosity[node])*self.fixedCn[ind]) / self.kp1PorosityField[node]
                    #self.aqueousCn[ind] = ( self.aqueousCkp1[ind]*self.currentPorosity[node]   - \
                    #                        self.fixedCkp1  [ind]*self.kp1PorosityField[node] +  \
                    #                self.currentPorosity[node]*self.fixedCn[ind]) / self.kp1PorosityField[node]

                    #self.chemicalSolver.setMobileConcentrationValues('internal',self.aqueousCn)
                    #res = self.chemicalSolver.equilibrate()
                    self.fixedCn = self.chemicalSolver.getImmobileConcentrationField('internal')
                    self.transportSolver.setPorosityField(self.kp1PorosityField)
                    pass
            else :
                self.fixedCn = self.chemicalSolver.getImmobileConcentrationField('internal')
                self.aqueousCn = self.chemicalSolver.getMobileConcentrationField('internal')
                if self.mpiEnv == None:
                    self.transportSolver.setConcentrationValues(self.aqueousCn)
                    pass
                elif self.communicator.rank == 0:
                    self.transportSolver.setConcentrationValues(self.aqueousCn)
                    pass
                                                                                            #
                                                                                            # The user can introduce here the call to its own functions
                                                                                            # in the way it is done with the functions present in the etuser.py.
                                                                                            #                        
            if self.userProcessing:
                print " user  processing ok "
                for method in self.processingList:
                    print " method ",method,self.timeStepNumber
                    exec(method)
                    pass
                pass
                                                                                            #
                                                                                            # Here we update the time, the simulated time.
                                                                                            #            
            if self.environ():
                if (self.TransportComponent == 'elmer'):
                    self.transportSolver.advanceTime(self.simulatedTime)
                    #raw_input("updating the simulated time: %e with dt: %e"%(self.simulatedTime, self.dT))
                    pass
                else:
                    self.transportSolver.advanceTime()
                    pass
                pass
                                                                                            #
                                                                                            # call to vtk writer
                                                                                            #
            if self.vtkFrequency != None:
                if (self.TransportComponent == 'mt3d'):
                    if int(self.simulatedTime / (self.vtkScalingFactor*self.vtkFrequency)) == self.vtkControl:

                        self.vtkFileWriter.vtkLegDataFileWriter(self.simulatedTime,
                                                                self.vtkTimeUnit,
                                                                self.vtkFieldSpecies,
                                                                self.internalNodesNumber,
                                                                self.componentList,
                                                                self.aqueousCn, self.vtkFileFormat, self.vtkfmt)

                        self.vtkControl += 1
                        pass
                    pass
                else: # It should be elmer or openfoam
                    if int(self.simulatedTime / (self.vtkScalingFactor*self.vtkFrequency)) == self.vtkControl:
                        self.vtkFileWriter.vtkLegDataFileWriter(self.simulatedTime,
                                                                self.vtkTimeUnit,
                                                                self.vtkFieldSpecies,
                                                                self.internalNodesNumber,
                                                                self.componentList,
                                                                self.aqueousCn, self.vtkFileFormat, self.vtkfmt)
                        self.vtkControl += 1
                        pass
                    pass
     
            self.transportCPUTime += (self.cpuTime() - cpuTimeBeg)

            # Advance in time for chemical (in kinetics and/or variable porosity)
            # variable porosity : to complete
            self.timeUpdate(it)
            #
            # The chemistry equilibrium has not been reached or the numerical 
            # constraints are to high
            #   
        else:
                                                                                            #
                                                                                            # The chemistry equilibrium has not been reached or
                                                                                            # the numerical constraints are to high
                                                                                            #   
            if not(self.chemicalEquilibrium) or (self.simTimesList == 0):
                print "Pb in chemistry or equilibrate not reached,", \
                      " we need to decrease the time step\n";#sys.stdout.flush()
                self.newTimeStepEvaluation(it,0)
                self.convergenceAnalysisParameter = 0
            # affectation to the new value
                if self.environ(): print "dbg ctm debug aqueousStateSet";#sys.stdout.flush()

                self.chemicalSolver.aqueousStateSet("internal")
                if self.environ(): print "dbg ctm debug ";#sys.stdout.flush()
                self.aqueousCn =  self.chemicalSolver.getMobileConcentrationField('internal')
                self.fixedCn = self.chemicalSolver.getImmobileConcentrationField('internal')
                if self.environ(): print "dbg ctm debug aqueousStateSet over";#sys.stdout.flush()
                pass
            else:
                raise Exception,\
                    "You impose a calculation times list but the maxIterationNumber"+\
                    " is reached, increase it or change calculation times list"
                pass

        return None
        
    oneChemicalTransportTimeStep = oneTimeStep

    def cpuTimeInitialisation(self):

        self.transportCPUTime = 0
        self.chemistryCPUTime = 0
        self.initialCPUTime   = 0
        self.globalCPUTime_deb = self.cpuTime()
    
        if self.chat:
            # cpu_time
            self.cpuChemicalCommunication = 0
            self.cpu_sourceField = 0.
            self.cpu_with_transport_communication = 0
            self.cpuOnList = 0.
            self.cpu_tot_residu = 0
            self.cpu_chemicalTransportOutput = 0
            pass

    def timeStepInitialisation(self):
    
        self.simulatedTime = self.times[0]
        if self.initialTimeStep and not self.simTimesList:
            self.dT = self.initialTimeStep
            pass
        elif self.simTimesList:
            self.dT = self.times[1] - self.simulatedTime
            self.initialTimeStep = self.dT
            pass
        else:
            raise Exception, 'time step initialisation problem, check problem definition'
        # check if an betweenComputation has to be done (output asked before initial time step)
        self.dT = min(self.dT,self.betweenComputation(self.simulatedTime))
                                                                                            #
                                                                                            # time loop control
                                                                                            #
        self.timeStepNumber = 0
    
    def environ(self):
        """
        method used to control the master in the master-slave  // paradigm
        """
        if self.mpiEnv == None:                                                             # sequential
            return 1
        elif self.communicator.rank == 0:                                                   # // root
            return 1
        else:
            return 0
            
    def timeUpdate(self, it):
        if (self.simTimesList == 0):
            self.newTimeStepEvaluation(it,1)
            self.convergenceAnalysisParameter = 1
            pass
        else:
            #raw_input("dbg here we are ")
            old_dt = self.dT
            if self.increment < len(self.times):
                self.dT = self.times[increment] - self.simulatedTime
                self.increment+=1
                pass
            if (self.mpiEnv == None):
                self.transportSolver.setTimeStep(self.dT)
                pass
            elif (self.communicator.rank == 0):
                self.transportSolver.setTimeStep(self.dT)
                pass
            pass

    def finalOutputsWriter(self):

        # check if it is necessary to write a table
    #print " finalOutputsWriter";sys.stdout.flush()      
        if (self.expectedOutputs) :
            for output in self.expectedOutputs:
                if (output.getName() in self.outputs):
                    if ( (output.getSave()== 'file') and isInstance(self.outputs[output.getName()],Table) ):
                        self.outputs[output.getName()].writeToFile(self.problem.getName() + '.tab')
                        pass
                pass
            pass

        if self.spatialInteractiveOutputs :
            pass

        if self.curveTable :
            try:
                self.timeInteractivePlot(self.simulatedTime,
                                    self.timeStepNumber,
                                    curveTable,
                                    curve,
                                    gplot,
                                    pointoplotindice,
                                    listofSpeciestoplot,
                                    list_component,
                                    internalNodesNumber,
                                    aqueousconcentrations,
                                    plotFrequency,cunit,
                                    1,
                                    title = None)
                self.TimeGplot.close()
                pass
            except: pass
            pass
        return None

    def setUserPermeability(self):
        self.userPermeability = True
        return None

    def getCurrentTime(self):
        return self.simulatedTime

    def getTimeStep(self):
        """
        To be used within a coupling with hydraulic
        """
        return self.dT
        
    def printc(self,messageString):
        if self.mpiEnv == None:
            print messageString;#sys.stdout.flush()
        elif self.communicator.rank==0:
            print messageString;#sys.stdout.flush()
    
    def transportInitialisation(self):
                                                                                            #
                                                                                            # mt3d
                                                                                            #
        if (self.TransportComponent == 'mt3d') :
                #
                # The list of components and associated concentrations being established by the chemistry,
                # we have to use these values to write down chemistry boundary conditions.
                #
            variables = [Species(i) for i in self.componentList]

            self.transportSolver.setPorosityOption(self.variablePorosityOption)
            if self.variablePorosityOption and self.HeadVPorosityOption == 1:
                self.transportSolver.setHydraulicPorosityParameter(1)
            else:
                self.transportSolver.setHydraulicPorosityParameter(0)

            self.transportSolver.setRegions(self.problem.getRegions())

            kboundary = self.chemicalSolver.getInternalCellsBeforeLaunching()+1
            for boundarycondition in self.boundaryConditions :
                for zones in boundarycondition.boundary.zones:
                    ind_min = zones.getIndexMin()
                    ind_max = zones.getIndexMax()
                    liste =self.chemicalSolver.getCellConcAtEqui(kboundary)
                    k2 = kboundary+(ind_max.j-ind_min.j+1)*(ind_max.i-ind_min.i+1)-1
                    kboundary = k2+1
                    boundarycondition.getChemicalStateValue().aqueousSolution.elementConcentrations = []
                    ind = 0
                    for i in variables:
                        boundarycondition.getChemicalStateValue().aqueousSolution.elementConcentrations.append(ElementConcentration(i.symbol,liste[ind],"mol/l"))
                        ind+=1

            self.transportSolver.setBoundaryConditions(self.problem.getBoundaryConditions())
            self.transportSolver.setData(self.mesh,
                                   variables,
                                   name=self.problem.getName(),
                                   velocity = self.darcyVelocity) 
            self.transportSolver.setParameter(self.value)
            self.transportSolver.advectionParametrisation()
            
            self.vtkFileWriter = VtkFileWriter(self.mesh, self.initialConditions, self.chemicalSolver, self.transportSolver,'mt3d')
            
            self.initialPorosityValues = self.transportSolver.getPorosityValues()
            #print "ipv\nipv\nipv\nipv\nipv\nipv\nipv\nipv\nipv\nipv\nipv\nipv\nipv\nipv\nipv\nipv\nipv\n"
            if self.mpiEnv!=None:
                print "ctmdbg rank of  communicator",self.communicator.rank
            print len(self.initialPorosityValues)
            #print "ipv0\nipv\nipv\nipv\nipv\nipv\nipv\nipv\nipv\nipv\nipv\nipv\nipv\nipv\nipv\nipv\nipv\n"
            self.transportSolver.setTimeStep(self.initialTimeStep)


            if isinstance(self.darcyVelocity,Velocity):
                self.transportSolver.setDarcyVelocity(self.darcyVelocity)
                pass
            
            pass
                                                                                            #
                                                                                            # elmer
                                                                                            #
        elif (self.TransportComponent == "elmer"):
            #print "ipv\nipv\nipv\nipv\nipv\nipv\nipv\nipv\nipv\nipv\n"
            if self.mpiEnv!=None:
                print "ctmdbg rank of  communicator",self.communicator.rank
            print "ctmdbg transportinitialisation method ";#sys.stdout.flush()
            print self.problem.__class__.__name__
            #raw_input()
            if self.problem.__class__.__name__ == "ChemicalTransportProblem":
                self.transportSolver.setProblemType("chemicaltransport")
                pass
            elif self.problem.__class__.__name__ == "THMCProblem":
                self.transportSolver.setProblemType("thmc")
                pass
            
            if (self.userPermeability == True): self.transportSolver.setUserPermeability()
            
            #print "ctmdbg transportinitialisation setDarcy ";#sys.stdout.flush()
            if isinstance(self.darcyVelocity,(Velocity,StringType)): 
                self.transportSolver.setDarcyVelocity(self.darcyVelocity)
                pass

            #print " transportinitialisation setBody ";#sys.stdout.flush()
            self.transportSolver.setBodyList(self.problem.getRegions())
            #print "ctmdbg transportinitialisation setBody over";#sys.stdout.flush()
                                                                                            #
                                                                                            # We add a variable : temperature
                                                                                            #
            if self.temperature:
                self.transportSolver.setTemperature()
                pass
            #print "ctmdbg for self.componentList: ",self.componentList
            self.transportSolver.setUnknownsNumber(len(self.componentList))
            #printm ("ctmdbg self.componentList: ")
                                                                                            #
                                                                                            # We treat the resolution scheme
                                                                                            #
            thetaSchemeValue = self.transportSolver.parameterDico['thetaScheme']["ALL"]
            for specName in self.componentList :
                self.transportSolver.parameterDico['thetaScheme'][specName.upper()] = thetaSchemeValue
                pass
            if self.temperature:
                ##
                ## On met setChemicalUnknownsNumber en commentaire
                ##

                self.transportSolver.setSpecies(self.chemicalSolver.getPrimarySpecies())
                pass
            else:
                if self.ChemicalComponent.lower() == "phreeqc":
                    self.transportSolver.setSpecies(self.chemicalSolver.getPrimarySpecies())
                    pass
                elif self.ChemicalComponent.lower() == "toughreact":
                    self.transportSolver.setSpecies(self.chemicalSolver.getPrimarySpecies())
                    pass
                pass
            print "ctmdbg ",self.chemicalSolver.getPrimarySpecies()
            try:
                self.transportSolver.parameterDico['thetaScheme'].keys().remove("ALL")
            except:
                pass
            self.speciesNamesList = self.transportSolver.speciesNamesList
            print("ctmdbg self.speciesNamesList: ",len(self.speciesNamesList), self.speciesNamesList)
            print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~";sys.stdout.flush()                         #
            print "~ ctmdbg Elmer Boundaries: ~";sys.stdout.flush()                         # Elmer boundary conditions
            print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~";sys.stdout.flush()                         #
            numberOfBoundaries = len(self.boundaryConditions)
                                                                                            #
                                                                                            # A boundary is represented by a single point within the chemistry.
                                                                                            # But points belonging to a boundary can belong to a domain region.
                                                                                            # Therefore, a list of these points is established and hereafter for B.C.
                                                                                            # these points are ignored
                                                                                            #
                                                                                            #
                                                                                            #raw_input("ctm dbg loop over boundary conditions")
            indPlot = 0
            for boundary in self.boundaryConditions:
                diclist = {}
                Cvalues = []
                Tvalues = []
                Hvalues = []
                if self.temperature:
                    self.dirichletBodyCond = NumericBodyField('Dirichlet boundary condition ',
                                                              self.mesh, self.componentList+['temperature'], float)
                    pass
                else:
                    #print ("ctmdbg for self.componentList: ",self.componentList)
                    #printm("we call NumericBodyField:\" self.componentList",1)
                    self.dirichletBodyCond = NumericBodyField('Dirichlet boundary condition ',
                                                              self.mesh, self.componentList, float)
                    #print("debug ctm : self.componentList",self.componentList)
                    #printm(" after dirichletBodyCond")
                    pass
                #
                # liste represents the list of primary species (the unknowns) to be handled as boundary condition
                #
                if (self.ChemicalComponent.lower() == "phreeqc"):
                    liste = self.chemicalSolver.getCellConcAtEqui(self.StatesBounds[boundary.boundary.getBodyName()][0][0])
                elif (self.ChemicalComponent.lower() == "toughreact"):
                    #
                    # for toughreact, the b.c. values are taken "as is", no equilibrium is made; or that
                    # one is made prior to the simulation.
                    #
                    #self.chemicalSolver.getMobileConcentrationField()
                    #print "self.StatesBounds: ",self.StatesBounds
                    #print "index ",self.StatesBounds[boundary.boundary.getBodyName()][0][0][0]
                    #raw_input("ctmdbg statesbounds")
                    #liste = self.chemicalSolver.getCellConcAtEqui(self.StatesBounds[boundary.boundary.getBodyName()][0][0][0])
                    #aqueousPrimarySpeciesList = self.chemicalSolver.getPrimarySpeciesNames()
                    #print aqueousPrimarySpeciesList
                    speciesControl = [species.symbol.lower() for species in boundary.aqueousSolution.elementConcentrations]
                    #boundarycondition.aqueousSolution.elementConcentrations.append(ElementConcentration(i.symbol,liste[ind],"mol/l"))

                    listeOfSpecies = [ElementConcentration(species.lower(),1.e-10,"mol/l") for species in self.chemicalSolver.getPrimarySpeciesNames()]
                    for cspecies in boundary.aqueousSolution.elementConcentrations:
                        print cspecies.symbol.lower
                        for species in listeOfSpecies:
                            if cspecies.symbol.lower() == species.symbol.lower():
                                species.value = cspecies.value
                                break
                            pass
                        pass
                    liste = [species.value for species in listeOfSpecies]
                    pass
                diclist["timeVariation"] = []
                diclist["name"] = boundary.getChemicalStateValue().name
                diclist["index"] = boundary.boundary.getEntity()
                diclist["bodyName"] = boundary.boundary.getName()
                #
                # we create an entry to handle temperature
                #
                diclist["TemperatureVariationList"] = [(0.,boundary.chemicalStateValue.aqueousSolution.getTemperature())]
                #
                if self.timeBoundaryConditionVariation not in [None, []]:
                    for chemicalTime in self.timeBoundaryConditionVariation:
                        #print "chemicalTime", chemicalTime
                        #print chemicalTime[1][0]
                        #print chemicalTime[1][0].getName()
                        #print dir(chemicalTime[1][0].boundary)
                        #print "temperature at time ",chemicalTime[1][0], chemicalTime[1][0].value.aqueousSolution.getTemperature()
                        #raw_input("debug list of times")
                        if chemicalTime[1][0].getName() == boundary.getChemicalStateValue().name:
                            diclist["timeVariation"].append((chemicalTime[0],chemicalTime[1][1]))
                            pass
                        pass
                        #
                        #
                        #
                        diclist["TemperatureVariationList"].append((chemicalTime[0], chemicalTime[1][2]))
                    #print " chemical times ",diclist["timeVariation"]
                    #raw_input(" we will update the boundary condition")
                    pass
                diclist["conc"] = liste
                diclist["description"] = boundary.description
                if (boundary.getType() == "Dirichlet"):
                    diclist["type"] = "Dirichlet"
                    pass
                elif boundary.getType() == "Flux":
                    diclist["type"] = "flux"
                    pass
                elif boundary.getType() == "Neumann":
                    diclist["type"] = "Neumann"
                    pass
                else:
                    raise Exception, " boundary type should be Dir. Flux or Neumann\ncheck the %s boundary"\
                    %(boundary.getChemicalStateValue().name)
                                                                                            #
                                                                                            # We update the boundary point list
                                                                                            #
                if self.temperature:
                    #print " boundary.boundary.getElements()",boundary.boundary.getElements()
                    #print " boundary.boundary",dir(boundary.boundary)
                    #print " boundary                      ",dir(boundary)
                    Tliste = self.chemicalSolver.getCellTempAtEqui(self.StatesBounds[boundary.boundary.getBodyName()][0][0])
                    diclist["temperature"] = Tliste
                    pass
                if boundary.enthalpyBoundaryCondition != None:
                    diclist["enthalpyBoundaryCondition"] = boundary.enthalpyBoundaryCondition
                    pass
                                                                                            #
                                                                                            # the study of a well is supposed
                                                                                            # to be linked to an evaluation
                                                                                            # of temperature
                                                                                            #
                if boundary.wellMassFlowBoundaryCondition != None:
                    diclist["wellMassFlowBoundaryCondition"] = boundary.wellMassFlowBoundaryCondition
                    pass
                if boundary.wellPressureBoundaryCondition != None:
                    diclist["wellPressureBoundaryCondition"] = boundary.wellPressureBoundaryCondition
                    pass
                    
                #raw_input(" we retrieve boundary conditions " + self.transportSolver.advConv.lower())
                if "computed" in self.transportSolver.advConv.lower():
                    print " ctmdbg boundary.boundary.getElements()",boundary.boundary.getElements();#sys.stdout.flush()
                    print " ctmdbg boundary.boundary",dir(boundary.boundary);#sys.stdout.flush()
                    print " ctmdbg boundary                      ",dir(boundary);#sys.stdout.flush()
                    print " ctmdbg boundary                      ",boundary.getHeadValue();#sys.stdout.flush()
                    #raw_input(" we retrieve boundary conditions")
                    diclist["head"] = boundary.getHeadValue()
                    pass
                print("ctmdbg self.componentAnz : ",self.componentAnz)
                [Cvalues.append(liste[conc]) for conc in range(self.componentAnz)]
                    #
                    # We need to modify the indexation of points between the mesher and python
                    #
                plotList = []
                for node in boundary.getBoundary().getBodyNodesList():
                    plotList.append(node-1)
                    pass
                #printm("the length of componentList is %s"%(len(self.componentList)))
                self.boundPlot.append((Cvalues, plotList, self.chemicalSolver.getPrimarySpeciesNames()))
                #printm("after boundPlot the length of componentList is %s"%(len(self.componentList)))

                if self.temperature:
                    if (boundary.getType() == "Dirichlet"):
                        self.dirichletBodyCond.setZone(boundary.getBoundary(), Cvalues+Tliste)
                        pass
                                                                                            #
                                                                                            # We need to modify the indexation of points
                                                                                            # between the mesher and python
                                                                                            #
                    plotList = []
                    for temperature in diclist["temperature"]:
                        plotList.append(temperature)
                        pass       
                    self.boundPlot[-1][0].append(plotList[0])
                    self.boundPlot[-1][-1].append("temperature")
                    pass
                else:
                    # print " dbg ctm ",boundary.boundary.getBodyName(),boundary.btype
                    if (boundary.getType() == "Dirichlet") or (boundary.getType() == "Flux"):
                        print("dbg ctm: %s\n"%(boundary.getName()))
                        print("dbg ctm: %i\n"%(len(Cvalues)))
                        print (Cvalues)
                        self.dirichletBodyCond.setZone(boundary.getBoundary(), Cvalues)
                        pass
                    pass
                #
                # to simplify
                #
                #print "dbg ctm diclist",diclist
                #print "dbg ctm diclist, boundary.getType",boundary.getType()
                #raw_input("dbg ctm diclist at the end of the boundary evaluation")
                #printm("before the call to transportSolver the length of componentList is %s"%(len(self.componentList)))
                if self.temperature:
                    if (boundary.getType() == "Dirichlet"):
                        #print "debug ctm 1 ",liste+Tliste
                        self.transportSolver.setBoundaryConditionConcentrations(self.dirichletBodyCond)
                        self.transportSolver.setDirBC([boundary.boundary.getBodyName(),\
                                                       boundary.boundary.getEntity(),\
                                                       "Dirichlet",\
                                                       liste+Tliste,\
                                                       boundary.description],\
                                                       diclist)
                        pass
                    pass
                else:
                    if (boundary.getType() == "Dirichlet"):
                        self.transportSolver.setBoundaryConditionConcentrations(self.dirichletBodyCond)
                        self.transportSolver.setDirBC([boundary.boundary.getBodyName(),\
                                                       boundary.boundary.getEntity(),\
                                                       "Dirichlet",\
                                                       liste,\
                                                       boundary.description],\
                                                       diclist)
                        pass
                    elif (boundary.getType() == "Flux"):
                        #print "debug ctm 1 ";#sys.stdout.flush()
                        diclist["massTC"] = boundary.getMTCoef()
                        self.transportSolver.setFluxBC([boundary.boundary.getBodyName(),\
                                                        boundary.boundary.getEntity(),\
                                                        "Flux",\
                                                        boundary.getMTCoef(),\
                                                        liste,\
                                                        boundary.description],\
                                                        diclist)
                        pass
                    elif (boundary.getType() == "Neumann"):
                        #print "debug ctm 1 "
                        self.transportSolver.setNeuBC([boundary.boundary.getBodyName(), boundary.boundary.getEntity(),\
                                                       "Neumann",\
                                                       liste,\
                                                       boundary.description],\
                                                       diclist)
                        pass
                    else:
                        raise Warning, "Check the definition of your boundary: " + str(boundary.boundary.getBodyName())
                #
                # Addendum of species which are not component species but nevertheless need
                # to be plotted through the vtk file generation, (within the loop over boundary conditions)
                # don't change the position to avoid pointer problems
                #
                indPlot+=1 # enables to treat the right cell within phreeqC
                if self.vtkFieldSpecies != None:
                    for species in self.vtkFieldSpecies:
                        if species not in self.boundPlot[-1][-1] and \
                           species.lower()!="temperature" and \
                           species != "porosity" and \
                           species != "charge":
                            #
                            # Introduce here a function to handle the concerned boundary.
                            #
                            indA = self.internalNodesNumber+indPlot-1
                            indE = indA+1
                            liste = self.chemicalSolver.solver.getSelectedOutput (indA, indE, species, "mol/l")
                            if liste == []: liste.append(0.0)
                            #
                            # species value
                            #
                            self.boundPlot[-1][0].append(liste[0])
                            #
                            # we introduce the species name
                            #
                            print ("self.componentList: ",self.componentList)
                            self.boundPlot[-1][-1].append(species)
                            print ("boundPlot:          ",self.boundPlot[-1][-1])
                            #printm("b in the species loop, %s the length of componentList is %s"%(species, len(self.componentList)), 1)
                            
                            pass
                        elif species == "porosity":
                            #
                            # we introduce the species name
                            #
                            #porosity = boundary.getPorosity()
                            
                            #if porosity == None:
                            #
                            # That value is set to zero to be more easely removed through a threshold
                            #
                            if boundary.getPorosity() == None:
                                porosity = 0.0
                                pass
                            else:
                                porosity = boundary.getPorosity()
                                pass
                            self.boundPlot[-1][-1].append("porosity")
                            self.boundPlot[-1][0].append(porosity)
                            pass
                        pass
                    pass
                printm("after the vtkFieldSpecies treatment, the length of componentList is %s"%(len(self.componentList)))
                #
                    #print self.boundPlot
                    #raw_input(" boundPlot")
                pass # end of the boundary treatment
                        
            print ("type of self.mesh is ",type(self.mesh))
            if self.mesh.getSpaceDimensions() !=1:
                #printm(" self.mesh.getSpaceDimensions() is %i"%(self.mesh.getSpaceDimensions()),1)
                self.transportSolver.vtkMeshFile(self.mesh)

            self.transportSolver.setSorptionLaw()

            #print " ctmdbg setPorosity",len([self.bodyPorosities]);#sys.stdout.flush()
            self.transportSolver.setPorosity([self.bodyPorosities])

            self.transportSolver.setEffectiveDiffusion([self.effectiveDiffusionZone])
            #
            # 3 lignes qui suivent commentees pour int de la temperature
            #
#            if self.temperature:


#       if self.dispersivityBody:

#
# Comment end, must be modified
#

#                if isinstance(self.darcyVelocity,Velocity):

#                    self.transportSolver.setKinematicDispersion(self.dispersivityBody)
            print "~~~~~~~~~~~~~~~~~~~~";sys.stdout.flush()                                 #
            print "~ ctmdbg Elmer IC: ~";sys.stdout.flush()                                 # Elmer initial conditions
            print "~~~~~~~~~~~~~~~~~~~~";sys.stdout.flush()                                 #
            ind = 0
            #printm("the number of initial conditions is %i "%(len(self.initialConditions)), 1)
            for initialCondition in self.initialConditions:
                Cvalues = []
                Tvalues = []
                #
                # The initial conditions are retrieved in the following order: chemistry, temperature, head.
                # As a consequence, they should be used in the same order.
                # Employing a dictionnary should be safer => must be changed.

                #
                # concentration list
                #
                #dir(initialCondition)
                #raw_input("dbg initial condition")
                if (self.ChemicalComponent.lower() == "phreeqc"):
                    liste = self.chemicalSolver.getCellConcAtEqui(self.StatesBounds[initialCondition.getValue().name+str(ind+1)][0][0])
                    pass
                elif (self.ChemicalComponent.lower() == "toughreact"):
                    print "ctmdbg toughreact initial condition name:",initialCondition.getValue().name
                    print "ctmdbg toughreact initial condition body bounds: ",self.StatesBounds[initialCondition.getValue().name]
                    print "ctmdbg toughreact species values",self.StatesBounds[initialCondition.getValue().name][0][0]
                    liste = self.chemicalSolver.getCellConcAtEqui(self.StatesBounds[initialCondition.getValue().name][0][0])
                    pass
                diclist = {}
                diclist["name"] = initialCondition.getValue().name
                diclist["conc"] = liste
                diclist["index"] = initialCondition.body.getEntity()
                diclist["description"] = initialCondition.description
                #
                # temperature
                #
                if self.temperature:
                    liste.append(initialCondition.getChemicalState().getAqueousSolution().getTemperature())
                    diclist["temperature"] = float(initialCondition.getChemicalState().getAqueousSolution().getTemperature())
                if initialCondition.temperatureInitialCondition != None:
                    diclist["temperatureInitialCondition"] = initialCondition.temperatureInitialCondition
                    #
                    # The temperatureInitialCondition should prevail over the chemical state temperature initial condition
                    #
                    if type(initialCondition.temperatureInitialCondition) in [IntType, FloatType]:
                        diclist["temperature"] = initialCondition.temperatureInitialCondition
                        pass
                    pass
                if initialCondition.enthalpyInitialCondition != None:
                    diclist["enthalpyInitialCondition"] = initialCondition.enthalpyInitialCondition
                    pass
                if initialCondition.wellFeedZoneInitialCondition != None:
                    diclist["wellFeedZoneInitialCondition"] = initialCondition.wellFeedZoneInitialCondition
                    pass
                if initialCondition.wellMassFlowInitialCondition != None:
                    diclist["wellMassFlowInitialCondition"] = initialCondition.wellMassFlowInitialCondition
                    pass
                if initialCondition.wellPressureInitialCondition != None:
                    diclist["wellPressureInitialCondition"] = initialCondition.wellPressureInitialCondition
                    pass
                #
                # head
                #
                if "computed" in self.transportSolver.advConv.lower():
                    liste.append(initialCondition.getHeadValue())
                    diclist["head"] = initialCondition.getHeadValue()
                    print " ctm dbg to destroy as soon as stated";#sys.stdout.flush()
                #
                [Cvalues.append(liste[conc]) for conc in range(self.componentAnz)]
                #print "ctmdbg setDirIC",self.componentAnz,initialCondition.getValue().name,len(liste);#sys.stdout.flush()
                self.transportSolver.setDirIC( diclist)
                ind+=1
                for boundary in self.boundaryConditions:
                    for node in self.mesh.getBody(boundary.boundary.getBodyName()).getBodyNodesList():
                        if node not in self.listOfBoundaryPoints:
                            self.listOfBoundaryPoints.append(node)
#            if isinstance(self.darcyVelocity,(Velocity,StringType)): 
#                self.transportSolver.setDarcyVelocity(self.darcyVelocity)

            #printm("the number of initial conditions diclist is %i "%(len(diclist)), 1)
            self.transportSolver.setExpectedOutput([])

            self.initialPorosityValues = self.transportSolver.getPorosityValues()
            #print "ctmdbg length of initialPorosityValues",len(self.initialPorosityValues);#sys.stdout.flush()
            #raw_input("ctmdbg length of initialPorosityValues")
            self.vtkFileWriter = VtkFileWriter(self.mesh,
                                               self.initialConditions,
                                               self.chemicalSolver,
                                               self.transportSolver,'elmer',self.boundPlot, parpertionList = self.parpertionList)

        else: 
        
            raise transportInitialisationException, "Elmer and mt3d are the only components treated within the coupling"
        print " End of transport initialisation ";#sys.stdout.flush()
        print " ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ";sys.stdout.flush()                                #
        return None
                                                                                            #
                                                                                            # interactive processing
                                                                                            # using gnuplot
                                                                                            #
    def iTimePlot(self, listOfOutputs, g, frequency = None, title = None, subTitle = None, rotate = None, extent = None,\
                  savingFrequency = None, outputType = None):

        """
        That function enables to produce an interactive plot over time.
        It uses gnuplot.py and gnuplot 4.4. and 5.0.2
        ListOfOutuputs : list containing the names of the ExpectedOutputs
        if rotate is None, meters are on x, else meters are on x
       
        savingFrequency is thought in terms of number of time steps
       
        The function as class arguments to enable a call within a script.
       
        """
        #print "debuglistOfOutputs: ",listOfOutputs
        #print "debugfrequency: ",frequency
        #print "debugsavingFrequency: ",savingFrequency
        if rotate == None or rotate == False:
            rotate = False
        else:
            rotate = True
        if frequency == None:
            interactivePlotFrequency = 1
            pass
        elif type(frequency) == IntType:
            interactivePlotFrequency = frequency
            pass
        else:
            raise Warning, " the plot frequency in the interActivePlot frequency should be an integer: "+str(frequency)
        #print "dbg itimeplot interactivePlotFrequency: ",interactivePlotFrequency
            
        if savingFrequency == None:
            savingFrequency = None
            outputFrequency = interactivePlotFrequency
        elif type(savingFrequency) != IntType:
            raise Warning," the saving plot frequency should be an integer"
            pass
        else:
            savingFrequency = savingFrequency
            outputFrequency = min(interactivePlotFrequency, savingFrequency)
        #
        # we set the plot frequency to the one requested
        #
        self.iPSaving = 'intGnuFile.dem'
        if self.timeStepNumber == 1:
            #print "dbg itimeplot len(self.problem.getOutputs): ",len(self.problem.getOutputs())
            #raw_input("rm -f intGnuFile.dem")
            for outputs in self.problem.getOutputs():
                if outputs.timeSpecification == None:
                    outputs.timeSpecification = TimeSpecification(frequency = interactivePlotFrequency)
                    outputs.timeSpecification.setFrequency(interactivePlotFrequency)
                else:
                    outputs.timeSpecification.setFrequency(interactivePlotFrequency)
                    pass
                pass
            os.system("rm -f intGnuFile.dem")
            pass
        
        if outputType == None or outputType.lower() == "png":
            outputType = "png"
        else:
            outputType = "ps"
        
        #self.iPSaving = 'intGnuFile.dem'
        #os.system("rm -f intGnuFile.dem")

        if extent == None:
            Nb_meters = 3.0
            pass
        else:
            Nb_meters = extent
            pass
        if (self.mpiEnv != None):
            if (self.communicator.rank != 0):
                return None
            pass

        #g('clear')
        #if platform.uname()[0] == 'Linux': g('set title \"Etumos\"')
        #print "dbg itimeplot self.timeStepNumber % interactivePlotFrequency: ",self.timeStepNumber % interactivePlotFrequency
        #print "dbg itimeplot rotate: ",rotate
        if self.timeStepNumber % interactivePlotFrequency == 0:
            g('set style data lines')
            g('set grid')       
            if self.timeStepNumber / interactivePlotFrequency == 1:
                os.system("rm -f intGnuFile.dem")
                pass
            elapsedTime = self.simulatedTime
            #elapsedTime = self.getOutput(listOfOutputs[0])[-1][0]                          # Time of the last simulation step
            
            gExpectedOutput = []
            aqueousOutputsNames = []
            #print "dbg itimeplot self.problem.outputs", self.problem.outputs
            for indOutput in range(len(self.problem.outputs)):
                #gExpectedOutput.append(self.problem.outputs[i].getName())
                print "dbg itimeplot self.problem.outputs", self.problem.outputs[indOutput].quantity.lower(), self.problem.outputs[indOutput].getName()
                if self.problem.outputs[indOutput].quantity.lower() == 'aqueousconcentration':
                    print "    dbg we update aqueousOutputsNames"
                    aqueousOutputsNames.append(self.problem.outputs[indOutput].getName())
                    pass
                else:
                    print "    dbg we update gExpectedOutput"
                    gExpectedOutput.append(self.problem.outputs[indOutput].getName())
                    pass
                pass
            #print "dbg itimeplot aqueousOutputsNames: ", aqueousOutputsNames,self.problem.outputs[i].quantity.lower()
            #print "dbg itimeplot listOfOutputs: ", listOfOutputs
            #print "dbg itimeplot gExpectedOutput: ", gExpectedOutput
            
            listOfAqueousOutputs = []
            for eO in listOfOutputs:
                eOName = eO.getName()
                if eOName not in gExpectedOutput + aqueousOutputsNames:
                    listOfOutputs.remove(eO)
                    pass
                if eOName in aqueousOutputsNames:
                    listOfAqueousOutputs.append(eO)
                    listOfOutputs.remove(eO)
                    pass
                    
                if len(listOfOutputs) + len(listOfAqueousOutputs) == 0:
                    raise Warning, " You should control the name of Species you want to plot in an interactive manner"
                pass
            listOfOutputs = listOfOutputs + listOfAqueousOutputs
            #print listOfOutputs
            #raw_input("dbg itimeplot listOfOutputs")
            #listOfOutputs = listOfOutputs[0:4]
            
#            if listOfAqueousOutputs != []:
#                if len(listOfOutputs) >= 4:
#                    listOfOutputs[-1] = 'AqueousConcentrationsList'
#                else:
#                    listOfOutputs.append('AqueousConcentrationsList')
            numberOfPlots = min(len(listOfOutputs),4)
                                                                                            #
                                                                                            # Titles & subtitles
                                                                                            #
            g(_gnuTitle(title, subTitle, numberOfPlots, elapsedTime))

            sizeString, origins, rot, rot2 = _gnuRotate(rotate, numberOfPlots)              # we determine gnuplot parameters to the number of plots
                                                                                            # rot = x means "no rotation"
            g(sizeString)               
                                                                                            #
                                                                                            # plotting all the curves via that loop
                                                                                            #
            print "dbg itimeplot listOfOutputs: ", listOfOutputs
            print "dbg itimeplot numberOfPlots of listOfOutputs", len(listOfOutputs)
            print "dbg problem outputs dir ", dir(self.problem.outputs[0])
            print "dbg problem outputs type ", type(self.problem.outputs)
            print "dbg problem outputs[0] ", self.problem.outputs[0]
            print "dbg problem outputs self.problem.outputs[0].__class__.__name__: ", self.problem.outputs[0].__class__.__name__
            #print "dbg problem outputs self.getOutput('K_output')", self.getOutput('K_output'), self.getOutput('K_output')
            #print "dbg problem outputs self.getOutput('K_output')",  self.getOutput('K_output')
            #print "dbg itimeplot self.getOutput(\"Na_output\"): ", self.problem.outputs[0]
            #print "dbg itimeplot self.getOutput(\"Na_output\")[-1]: ", self.problem.outputs[0][-1]
            #print "dbg itimeplot self.getOutput(\"Na_output\")[-1]: ", self.problem.outputs[0][-1][1].getColumn(-1)
            #raw_input()
            for var in range(numberOfPlots):
                name = listOfOutputs[var].getName()
                #print "itime plot ",name
                #raw_input("dbg itimeplot")

                if numberOfPlots>1:
                    g('set origin ' + origins[var])
                    #if rot == 'x':
                    g.title(name + ' profile')
                    pass
                                                                                           #
                                                                                           # Label, scale of output axis
                                                                                           #
                outputToPlot = self.getOutput(name)[-1][1].getColumn(-1)
                yextension = max(outputToPlot)-min(outputToPlot)
                if yextension > 1.e-15:
                    str3 = "%9.3e"%(yextension/3.)
                else:
                    if max(outputToPlot)> 1.e-15:
                        str3 = "%9.3e"%(2.*max(outputToPlot/3)/3.)
                    else:
                        str3 = "%9.3e"%(1.e-5)
                #
                if rotate == False:
                    position = self.getOutput(name)[-1][1].getColumn( 0)
                    position = max(position)-min(position)
                    strx = "%9.3e"%(position/3.)
                    g('set ' + rot + 'tics 0, ' + strx + " rotate by -20")
                    pass
                else:
                    position = self.getOutput(name)[-1][1].getColumn( 1)
                    position = max(position)-min(position)
                    stry = "%9.3e"%(position/3.)
                    g('set ' + rot + 'tics 0, ' + stry)
                    pass
                g('set format ' + rot + ' "%10.3e"')
                g('set ' + rot + 'label "m"')
                                                                                            #
                                                                                            # Label and scale of depth axis
                                                                                            #       
                #yextension = Nb_meters
                yextension = max(outputToPlot)-min(outputToPlot)
                g('set ' + rot2 + 'label "' + name + '"')
                g('set ' + rot2 + 'tics 0, ' + str(yextension/3.))
                g('set format ' + rot2 + ' "%10.3e"')
                                                                                            #
                                                                                            # plot
                                                                                            #
                last_var = outputToPlot
                if (self.TransportComponent == "mt3d"):
                    ext = self.transport.getMeshExtent()
                    if ext[0] < ext[1]:
                        abscisse = self.getOutput(name)[-1][1].getColumn(0).tolist()
                    else:
                        abscisse = self.getOutput(name)[-1][1].getColumn(1).tolist()
                    del abscisse[0]
                else:                                                                       # it should be Elmer
                    abscisse = self.getOutput(name)[-1][1].getColumn( 0)
                courbes = []
                i = 0
                if rot == 'x':
                    while abscisse[i] < Nb_meters and i < len(abscisse)-1:
                        courbes.append([abscisse[i], last_var[i]])
                        i+=1
                        pass
                    pass
                elif rot == 'y':
                    while abscisse[i] < Nb_meters and i+1 < len(abscisse):
                        courbes.append([last_var[i], abscisse[i]])
                        i+=1
                        pass
                    pass
                #print " dbg itimeplot abscisse: ",abscisse;sys.stdout.flush()
                #print " dbg itimeplot rot: ",rot;sys.stdout.flush()
                #print " dbg itimeplot Plots: ",courbes;sys.stdout.flush()
                #print " dbg numberOfPlots: ",len(courbes);sys.stdout.flush()
                g('set autoscale x')
                g('clear')
                g.plot(courbes)
                pass
                                                                                            #
                                                                                            # end of the plotting loop
                                                                                            #
            if savingFrequency != None and self.timeStepNumber % savingFrequency == 0:
                print "dbg itime plot saving frequency: ",savingFrequency, self.timeStepNumber, self.timeStepNumber % savingFrequency
                self.gnuFile = open(self.iPSaving, "a")
                self.gnuFile.write("reset\n")
                if (outputType == "png"):
                    self.gnuFile.write("set term png\n")
                    pass
                else:
                    self.gnuFile.write("set term postscript\n")
                    pass
                self.gnuFile.write("set style data linespoints\n")
                self.gnuFile.write(_gnuTitle(title, subTitle, 1, elapsedTime)+"\n")
                                                                                            #
                                                                                            # -> file saving
                                                                                            #
                for var in range(len(listOfOutputs)):
                    print "listOfOutputs : ",listOfOutputs;sys.stdout.flush()
                    name = listOfOutputs[var].getName()
                    outputToPlot = self.getOutput(name)[-1][1].getColumn(-1)
                    self.gnuFile.write("set output \"int_"+name+"_"+str(str(elapsedTime/3.15576e+7))+"y."+outputType+"\"\n")
                                                                                #
                                                                                # Label and scale of output axis
                                                                                #
                    yextension = max(outputToPlot)-min(outputToPlot)
                    if yextension > 1.e-15:
                        str3 = "%9.3e"%(yextension/3.)
                    else:
                        str3 = "%10.4e"%(2.*max(outputToPlot/3.)/3.)
                    if rotate == False:
                        position = self.getOutput(name)[-1][1].getColumn( 0)
                        position = max(position)-min(position)
                        strx = "%9.3e"%(position/3.)
                        self.gnuFile.write("set " + rot + "tics 0, " + strx + " rotate by -20\n")
                        pass
                    else:
                        position = self.getOutput(name)[-1][1].getColumn( 1)
                        position = max(position)-min(position)
                        stry = "%9.3e"%(position/3.)
                        self.gnuFile.write("set " + rot + "tics 0, " + stry + "\n")
                        pass
                    self.gnuFile.write("set format " + rot + " \"%10.3e\"\n")
                    self.gnuFile.write('set ' + rot + 'label \"m\"\n')
                                                                                #
                                                                                # Label and scale of depth axis
                                                                                #       
                    #yextension = 1.
                    self.gnuFile.write("set " + rot2 + 'label \"' + name + '\"\n')
                    self.gnuFile.write('set ' + rot2 + 'tics 0,' + str(yextension/3.)+'\n')
                    self.gnuFile.write('set format ' + rot2 + ' \"%10.3e\"\n')
                                                                                #
                                                                                # plot
                                                                                #
                    last_var = outputToPlot
                    #
                    if (self.TransportComponent == "mt3d"):
                        ext = self.transport.getMeshExtent()
                        if ext[0] < ext[1]:
                            abscisse = self.getOutput(name)[-1][1].getColumn(0).tolist()
                            pass
                        else:
                            abscisse = self.getOutput(name)[-1][1].getColumn(1).tolist()
                            pass
                        del abscisse[0]
                    else:
                        abscisse = self.getOutput(name)[-1][1].getColumn( 0)
                        pass
                    #
                    courbes = []
                    self.gnuFile.write("plot \"-\""+ " title "+"\""+name+"\"\n")
                    i = 0
                    #print "dbg length of absc ",len(abscisse), abscisse[0], abscisse[1]
                    while abscisse[i] < Nb_meters and i < len(abscisse)-1:
                        if rot == 'x':
                            self.gnuFile.write(" %9.5e %9.4e\n"%(abscisse[i], last_var[i]))
                            pass
                        else:
                            self.gnuFile.write(" %9.5e %9.4e\n"%(last_var[i], abscisse[i]))
                            pass
                        i+=1
                        pass
                    self.gnuFile.write("e\n")
                self.gnuFile.write("exit\n")
                self.gnuFile.close()
                pass

            subprocess.Popen("gnuplot " + str(self.iPSaving), shell = True).wait()
            pass

    def updateDataSaving(self, listOfOutputs, listOfAqueousOutputs, title, subTitle, saving, savingFrequency):
        if saving != None and self.timeStepNumber % savingFrequency == 0:
#                    self.gnuFile = open(self.iPSaving, "w")
            if title != None:
                titre = title
            else:
                titre = 'Etumos Interactive plot'
            if subTitle == None: soustitre = ''
            fileName = 'int_data_' + titre.replace(' ', '_')
            if not os.path.exists(fileName) or self.timeStepNumber == savingFrequency:
                f1 = open(fileName, 'w')
                f1.write('Title\n' + title + '\nSubTitle\n' + subTitle)
                f1.write('\nConcentrations\n')
                for i in listOfOutputs:
                    if i != 'AqueousConcentrationsList':
                        f1.write(i + '\t')
                f1.write('\nAqueousConcentration\n')
                if listOfAqueousOutputs == []:
                    f1.write('None')
                else:
                    for i in listOfAqueousOutputs:
                        f1.write(i + '\t')
            else:
                f2 = open(fileName, 'r')
                Before = f2.read()
                f1 = open(fileName, 'w')
                f1.write(Before)
                
                    
            completeList = listOfOutputs
            if 'AqueousConcentrationsList' in completeList:
                completeList.remove('AqueousConcentrationsList')
                completeList = completeList + listOfAqueousOutputs
            f1.write('\ndate   ' + str(self.getOutput(completeList[0])[-1][0]/3.15576e+7) + '\n')
            for i in range(len(self.getOutput(completeList[0])[-1][1].getColumn(-1))):
                f1.write(str(self.getOutput(completeList[0])[-1][1].getColumn(1)[i]))
                for j in completeList:
                    f1.write('\t'+str(self.getOutput(j)[-1][1].getColumn(-1)[i]))
                f1.write('\n')
            f1.close()    
                                                                                            #
                                                                                            # Class to be used to handle
                                                                                            # postprocessing
                                                                                            # using a vtk file format.
                                                                                            #
class VtkFileWriter:
    """
    
    Vtk file writer with the legacy format
    
    """
    def __init__(self,mesh,initialConditionList,chemistrySolver,transportSolver,solverName,boundPlot = None, parpertionList = None):

        self.chemistrySolver = chemistrySolver
        self.transportSolver = transportSolver
        self.solverName = solverName
        self.mesh = mesh
       #
       # used for elmer
       #
        if boundPlot == None:
            self.boundPlot = []
            pass
        else:
            self.boundPlot = boundPlot
            pass
        if transportSolver == None:
            self.environ = "False"
            pass
        else:
            self.environ = "True"
            pass
        self.InitialConditionList = initialConditionList
        initialCondition=initialConditionList[0]
        if parpertionList != None:
            self.parpertionList = parpertionList
            pass
        if (self.solverName == 'mt3d'):
            for zone in initialCondition.zone.zones:
                indMin = zone.getIndexMin()
                indMax = zone.getIndexMax()
                iMin = indMin.i
                iMax = indMax.i
                jMin = indMin.j
                jMax = indMax.j
            for initialCondition in initialConditionList[1:]:
                for zone in initialCondition.zone.zones:
                    indMin = zone.getIndexMin()
                    indMax = zone.getIndexMax()
                    iMin = min(indMin.i,iMin)
                    iMax = max(indMax.i,iMax)
                    jMin = min(indMin.j,jMin)
                    jMax = max(indMax.j,jMax)
                    pass
                pass
            x = self.mesh.coords[0]
            y = self.mesh.coords[1]
            self.x = []
            position = 0.
            self.x.append(position+(x[0])*0.5)
            for i in range(iMin+1,iMax+2):
                self.x.append(x[i-1])
                pass
            self.y = []
            position = 0.
            self.y.append(position+(y[0])*0.5)
            for i in range(jMin+1,jMax+2):
                self.y.append(y[i-1])
                pass
            self.x = x    
            self.y = y    
            return None

    def vtkXmlDataFileWriter(self,current_time,\
                             vtkTimeUnit,\
                             speciesToPlot,\
                             internalNodesNumber,\
                             list_component,\
                             aqueousconcentrations):
        """
        That function is used for outputs in a xml format. Only the
        elmer unstructured file is treated
        """
                                                                                            #
                                                                                            # We determine the factor
                                                                                            #
        timeUnit,scalingFactor = _scaling(vtkTimeUnit)

        ind= 0
                                                                                            #
                                                                                            # elmer
                                                                                            #
        permutation = self.transportSolver.getPermutation()
        ind = 0

        for i in permutation:
#                print " perm ",ind,i
            if i> 0: ind+=1
            pass
#
        plottingFile = "species_at_"+str(int(current_time/scalingFactor))+timeUnit+".vtu"
        connectivity = self.mesh.getConnectivity()
        #
        # we create a null list to avoid boundary problems
        #
        ScalarValuePoint = [0.0]*self.mesh.getNodesAnz()*len(speciesToPlot)
        ind = 0
        for speciesName in speciesToPlot:
            if speciesName.lower() not in ["temperature"]:
                dataToPlot = self.chemistrySolver.getOutput(speciesName,"internal","mol/l")
                pass
            else:
                dataToPlot = self.chemistrySolver.getTemperatureField()
                pass
            dataToPlot = self.chemistrySolver.getOutput(speciesName,"internal","mol/l")
            #
            # to handle multiple species
            #
            ind = ind*len(self.mesh.getNodesAnz())
            #
            if (speciesName.lower()!="eh"):
                if self.boundPlot != []:
                    index = self.boundPlot[-1][-1].index(speciesName)
                    ind = 0 
                    for  boundary in self.boundPlot:
                    #
                    # We have retrieved the data from a boundary and apply it on all points
                    #
                        for node in boundary[1]:
                            ScalarValuePoint[ind+node] = boundary[0][index]
                            ind+=1
                            pass
                        pass
                    pass
                # We treat field points
                #
                # the node are listed as in gmsh. It should be modified
                # within the gmsh generator.
                #
                for node in range(len(self.parpertionList)):
                    ScalarValuePoint[self.parpertionList[ind+node]-1] = dataToPlot[node]
                    pass
            else:
                for node in range(len(self.parpertionList)):
                    ScalarValuePoint[self.parpertionList[ind+node]-1] = dataToPlot[node]
                    pass
            ind+= 1
        vtkWriter = XmlVtkUnstructured()
        vtkWriter.snapshot(plottingFile,                                                    # name of the file
                           _coordinatesList(self.mesh.getNodesCoordinates()),               # nodes coordinates
                           len(connectivity),                                               # number of cells
                           _connectivityList(connectivity),                                 # cell connectivity
                           Offsets, 
                           _celltypes(connectivity),                                        # list of cell types
                           speciesToPlot,                                                   # unknowns to be plotted
                           ScalarValuePoint,                                                # list of data for each unknown 
                          )

        self.dataFile.close()
        return None
#
#
#                                                                                                                
    def vtkLegDataFileWriter(self,current_time,\
                             vtkTimeUnit,\
                             speciesToPlot,\
                             internalNodesNumber,\
                             list_component,\
                             aqueousconcentrations,\
                             fileFormat = None,\
                             fmt = None):
        """
        That function is used for outputs in a vtk legacy format
        """
                                                                                            #
                                                                                            # We determine the factor
                                                                                            #
        timeUnit,scalingFactor = _scaling(vtkTimeUnit)

        ind= 0
                                                                                        #
                                                                                        # Mt3d
                                                                                        #
        if (self.solverName == 'mt3d'):
            for speciesName in speciesToPlot:
                if 1==1:
                    indices = ind
                    dataToPlot = self.chemistrySolver.getOutput(speciesName,"internal","mol/l")
                    data_temporary = []
                    if self.environ != "False":
                        if self.transportSolver.fwel=="T":
                            iboundf = self.transportSolver.ipermut

                            ind = 0
                            for i in range(0,len(dataToPlot)):
                                data_temporary.append(dataToPlot[iboundf[i]])
                                pass
                            dataToPlot = data_temporary
                            pass    
                        pass
                    pass

                if fileFormat == "legacy" or fileFormat == None:
                    name = speciesName+"_at_"+str(int(current_time/scalingFactor))+timeUnit+".vtk"
                    self.name = name
                    self.file_fil=open(self.name,'w')
                    self.file_fil.write("%s\n"%("# vtk DataFile Version 2.0"))
                    self.file_fil.write("%s\n"%("Sample rectilinear grid"))
                    if fmt == 'binary':
                        self.file_fil.write("%s\n"%("BINARY"))
                        pass
                    else:
                        self.file_fil.write("%s\n"%("ASCII"))
                        self.file_fil.write("%s\n"%("DATASET RECTILINEAR_GRID"))
                        self.file_fil.write("DIMENSIONS %d %d %s\n"%(len(self.x),len(self.y),"1"))
                        self.file_fil.write("X_COORDINATES %d  %s \n"%(len(self.x),"float"))
                        pass
                    if fmt == 'binary':
                        r = struct.pack('!'+'f'*len(self.x),*self.x)
                        self.file_fil.write(r)
                        pass
                    else:
                        for i in self.x:
                            self.file_fil.write("%f \n"%(i))
                            pass
                        pass
                    self.file_fil.write(" Y_COORDINATES  %d %s\n"%(len(self.y),"float"))
                    if fmt == 'binary':
                        r = struct.pack('!'+'f'*len(self.y),*self.y)
                        self.file_fil.write(r)
                        pass
                    else:
                        for i in self.y:
                            self.file_fil.write("%f \n"%(i)) 
                            pass
                        pass
                    #self.file_fil.write("%s %f %s\n"%("Z_COORDINATES",len(self.z),"float"))
                    self.file_fil.write(" Z_COORDINATES %d %s\n"%(1,"float"))
                    if fmt == 'binary':
                        r = struct.pack('!'+'f'*len([0.]),[0.])
                        self.file_fil.write(r)
                        pass
                    else:
                        self.file_fil.write("%f \n"%(0.0))
                        pass
                    self.file_fil.write(" CELL_DATA  %d\n"%((len(self.x)-1)*(len(self.y)-1)))

                    self.file_fil.write(" SCALARS  %s float\n"%(speciesName))

                    self.file_fil.write(" LOOKUP_TABLE default \n")
                    # Introduction of max to avoid tiny negative plotted values
                    if  speciesName!="pe" and speciesName!="Eh" :
                        ind = 0
                        if self.environ != "False":
                            for point in self.transportSolver.ibound:
                                if point == -1:
                                    self.file_fil.write("%15s\n"%(_fote158(0.)))
                                    pass
                                else:
                                    self.file_fil.write("%15s\n"%(_fote158(max(0.,dataToPlot[ind]))))
                                    ind+=1
                                    pass
                                pass
                            pass
                        pass
                    else:
                        for point in dataToPlot:
                            self.file_fil.write("%15s\n"%(_fote158(point)))
                            pass
                        pass
                    pass
                pass
            pass
                                                                                        #
                                                                                        # elmer
                                                                                        #
        else:
            if self.transportSolver != None:
                permutation = self.transportSolver.getPermutation()
                #print " permutation: \n",len(permutation)
                #indpp = 0
                #for permutt in permutation:
                #    print ind+1,permutt
                #    ind+=1
                #raw_input(" permutation distribution")
                pass
            else:
                pass
            ind = 0

#            for i in permutation:
#                print " perm ",ind,i
#                if i> 0: ind+=1
            #print " ctm dbg species to plot"
            for speciesName in speciesToPlot:
                #print " species to plot",speciesName
                #raw_input(" species to plot")
                name = speciesName+"_at_"+str(int(current_time/scalingFactor))+timeUnit+".vtk"
                self.name = name
                if self.transportSolver != None:
                    self.dataFile=open(self.name,'w')
                    self.dataFile.write("# vtk DataFile Version 2.0\n");self.dataFile.flush()
                    self.dataFile.write("obtained with chemicaltransportmodule\n");self.dataFile.flush()
                    self.dataFile.write("ASCII \n");self.dataFile.flush()
                    self.dataFile.write("DATASET UNSTRUCTURED_GRID \n") ;self.dataFile.flush()
                    self.dataFile.write("POINTS  %i double\n"%(self.mesh.getNodesAnz()));self.dataFile.flush()
                    pass
                dim = self.mesh.getSpaceDimensions()
                #print " ctm dbg  mesh.getSpaceDimensions",dim
                #
                # We get the nodes coordinates
                #
                nodesCoordinates = self.mesh.getNodesCoordinates()
                #
                # 2D
                #
                if (dim == 2) and (self.transportSolver != None):
                    for node in range(len(nodesCoordinates)):
                        self.dataFile.write("%15.8e %15.8e %15.8e \n"%(  nodesCoordinates[node][0],\
                                                                    nodesCoordinates[node][1],0.));self.dataFile.flush()
                        pass
                    pass
                #
                # 3D
                #
                elif (dim==3) and (self.transportSolver != None):   
                    for node in range(0,len(nodesCoordinates)):
                        self.dataFile.write("%15.8e %15.8e %15.8e \n"%(nodesCoordinates[node][0],
                                                                       nodesCoordinates[node][1],
                                                                       nodesCoordinates[node][2]));self.dataFile.flush()
                        pass
                    pass
                elif self.transportSolver != None:
                    raise "Error in mesh dimension"
                connectivity = self.mesh.getConnectivity()

                numberOfCells = len(connectivity)

                gmshType, vtkTyp  = self.mesh.getType()
    
                if self.transportSolver != None:
                    self.dataFile.write("CELLS %i %i\n"%(numberOfCells,\
                                        _vtkCellListSize(numberOfCells,connectivity)));#self.dataFile.flush()
                    pass
                ind = 0
                for cell in connectivity:
                    ind = cell[2]+3
                    #print " ctm dbg cell ",vtkTyp,ind,cell," perm ",permutation[ind],permutation[ind+1],permutation[ind+2],permutation[ind+3]
                    # 
                    vtkTyp = _vtkGmsh(cell[1])
                    if (vtkTyp==3):                                                         # 2-node line
                        if self.transportSolver != None:
                            self.dataFile.write("%i %i %i\n"%(2,\
                                                cell[ind]-1,
                                                cell[ind+1]-1)
                                               )
                            pass
                        pass
                
                    elif (vtkTyp==5):                                                       # triangles
                        if self.transportSolver != None:
                            self.dataFile.write("%i %i %i %i\n"%(3, 
                                                cell[ind]-1,\
                                                cell[ind+1]-1,\
                                                cell[ind+2]-1)
                                               )
                            pass
                        pass
                    elif (vtkTyp==9):                                                       # quadr
                        if self.transportSolver != None:
                            self.dataFile.write("%i %i %i %i %i\n"%(4,\
                                                cell[ind]-1,\
                                                cell[ind+1]-1,\
                                                cell[ind+2]-1,\
                                                cell[ind+3]-1)
                                               )
                            pass
                        pass
                    elif (vtkTyp==10):                                                      # tetra
                        if self.transportSolver != None:
                            self.dataFile.write("%i %i %i %i %i\n"%(4,\
                                                cell[ind]-1,\
                                                cell[ind+1]-1,\
                                                cell[ind+2]-1,\
                                                cell[ind+3]-1)
                                               )
                            pass
                        pass
                    elif (vtkTyp==12):                                                      # hexahedron
                        if self.transportSolver != None:
                            self.dataFile.write("%i %i %i %i %i %i %i %i %i\n"%(8,\
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
                    elif (vtkTyp==13):                                                      # prism : 6-nodes
                        if self.transportSolver != None:
                            self.dataFile.write("%i %i %i %i %i %i %i\n"%(6,\
                                              cell[ind  ]-1,\
                                              cell[ind+1]-1,\
                                              cell[ind+2]-1,\
                                              cell[ind+3]-1,\
                                              cell[ind+4]-1,\
                                              cell[ind+5]-1)
                                             )
                            pass
                        pass
                    elif (vtkTyp==14):                                                      # pyramid : 5-nodes
                        if self.transportSolver != None:
                            self.dataFile.write("%i %i %i %i %i %i %i\n"%(5,\
                                              cell[ind  ]-1,\
                                              cell[ind+1]-1,\
                                              cell[ind+2]-1,\
                                              cell[ind+3]-1,\
                                              cell[ind+4]-1)
                                             )
                            pass
                        pass
                    pass
                self.dataFile.flush()
                #print " we are at the CELL_TYPES level"
                if self.transportSolver != None:
                    self.dataFile.write("%s %i\n"%("CELL_TYPES",numberOfCells))
                    for i in range(0,numberOfCells):
                        gmshType = connectivity[i][1]
                        self.dataFile.write("%i\n"%(_vtkCellTyp(gmshType)))
                        pass
                    self.dataFile.write("%s %i\n"%("POINT_DATA ",self.mesh.getNodesAnz()));self.dataFile.flush()
                    pass
                                                                                            #
                                                                                            # loop over unknowns:
                                                                                            #   temperature and chemicalspecies are treated
                                                                                            #
                                                                                            #   porosity is retrieved from the 
                                                                                            #   chemistry solver
                                                                                            #   permeability is retrieved from
                                                                                            #   the hyd/transport solver
                                                                                            #
                    #print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                    #if speciesName.lower()== "t": print self.chemistrySolver.getOutput(speciesName,"internal","mol/l")
                    #if speciesName.lower()== "t": print self.parpertionList
                    #if speciesName.lower()== "t": print len(self.parpertionList)
                    #if speciesName.lower()== "t": print len(self.chemistrySolver.getOutput(speciesName,"internal","mol/l"))
                    #if speciesName.lower()== "t": print self.transportSolver.getPermutation()
                    #print len(permutation)
                    #pprint "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                    #raw_input("debug tr")
                    #pass
                #if speciesName.lower() == "porosity":
                #    print " we reach that level"
                #    print self.chemistrySolver.getOutput(speciesName,"internal","mol/l")
                if speciesName.lower() not in ["temperature","permeability"]:
                    dataToPlot = self.chemistrySolver.getOutput(speciesName,"internal","mol/l")
                    if speciesName.lower() in ["ts","quartz"]:
                        #print dataToPlot
                        #raw_input("dataToPlot: "+str(speciesName))
                        pass
                    pass
                elif speciesName.lower() == "temperature":
                    dataToPlot = self.chemistrySolver.getTemperatureField()
                    pass
                elif speciesName.lower() == "permeability":
                    dataToPlot = self.transportSolver.getPermeabilityField()
                    pass
#                    ind = 0
#                    for i in dataToPlot:
#                        print ind,i
#                        ind+=1
                #if speciesName.lower() == "porosity": print dataToPlot
                #raw_input(" we have reached that point ")
                
                if self.transportSolver != None:
                    form = "SCALARS " + speciesName + " double 1\n"
                    self.dataFile.write("%s"%(form));self.dataFile.flush()
                    self.dataFile.write("LOOKUP_TABLE default\n");self.dataFile.flush()
                    pass
                ind = 0
                if (speciesName.lower()!="eh"):
#
#               for cell in connectivity:
#                       ind = cell[2]+3
#                            print "ctm dbg length of permutation ",len(permutation)
#                       print " ctm dbg  ",ind+2,cell,cell[ind],cell[ind+1],cell[ind+2],cell[ind+3]
#                       print " ctm dbg1 ",permutation[cell[ind  ]-1],permutation[cell[ind+1]-1],permutation[cell[ind+2]-1],permutation[cell[ind+3]-1]
#                       #print " ctm dbg perm",permutation[cell[ind]],permutation[cell[ind+1]],permutation[cell[ind+2]],permutation[cell[ind+3]],len(dataToPlot)
#                       print ind,  cell[ind  ]-1,dataToPlot[cell[ind  ]-1],permutation[cell[ind  ]-1]
#                       print ind+1,cell[ind+1]-1,dataToPlot[cell[ind+1]-1],permutation[cell[ind+1]-1]
#                       print ind+2,cell[ind+2]-1,dataToPlot[cell[ind+2]-1],permutation[cell[ind+2]-1]
#                       print ind+3,cell[ind+3]-1,dataToPlot[cell[ind+3]-1],permutation[cell[ind+3]-1]
#                       #print dataToPlot[cell[ind+3]]
#                   data = dataToPlot[permutation[cell[ind]-1]]
#                       self.dataFile.write("%12.8f %12.8f %12.8f %12.8f\n"%(max(dataToPlot[permutation[cell[ind]-1]],0.),
#                                                                           max(dataToPlot[permutation[cell[ind+1]-1]],0.),
#                                                                           max(dataToPlot[permutation[cell[ind+2]-1]],0.),
#                                                                           max(dataToPlot[permutation[cell[ind+3]-1]],0.)))
#
                    plot = [1.e-15]*self.mesh.getNodesAnz()
                    #
                    # We treat boundary points
                    #
                    if self.boundPlot != []:
                        index = self.boundPlot[-1][-1].index(speciesName)
                        ind = 0
                    
                        for boundary in self.boundPlot:
                        #
                        # We have retrieved the data from a boundary and apply it on all points
                        #
                            for node in boundary[1]:
                                plot[node] = boundary[0][index]
                                ind+=1
                                pass
                            pass
                        pass
                        
                    #
                    # We treat field points
                    #
                    ind1 = 0

#                    for node in range(self.mesh.getNodesAnz()):
#                        k = permutation[node]
#                        if k > 0:
#                            plot[node] = dataToPlot[ind1]
#                            ind1+=1
#                        else:
                            #plot[node] = -1
#                            pass
                    #
                    # the node are listed as in gmsh. It should be modified
                    # within the gmsh generator.
                    #
                    #if speciesName.lower() == "na":
                        #print " dataToPlot",dataToPlot[0],dataToPlot[1],len(dataToPlot)
                        #raw_input(" datat to plot ")
                    nodeToPlot = 0
                    #print "debug length ",len(nodesCoordinates), len(plot), len(dataToPlot)
                    #print self.transportSolver.getPermutation()
                    if self.transportSolver != None:
#                        permutation = self.transportSolver.getPermutation()
#                        for node in range(len(permutation)):
#                            neg = 0
#                            if permutation[node] > 0:
#                                print node, permutation[node]
#                                plot[node] = dataToPlot[nodeToPlot]
#                                nodeToPlot+=1
                        #raw_input("len de "+str(len(self.parpertionList)))
                        for node in range(len(self.parpertionList)):
                            plot[node] = dataToPlot[node]
                            #plot[self.parpertionList[node]] = dataToPlot[node]

                        
                        for conc in plot:
                            self.dataFile.write ("%12.8e \n"%(max(conc,0.)));self.dataFile.flush()
#                        node+=1
#
#                       if ind%6 == 0: self.dataFile.write("\n")
#                   self.dataFile.write("%s\n"%(str(dataToPlot)[1:-1].replace(',',' ')))
#
                else:
                    if self.transportSolver != None:
                        for data in dataToPlot:
                            self.dataFile.write("%12.8e \n"%(data));self.dataFile.flush()
                            ind+=1
                            pass
                        pass
                    pass
#                       if ind%6 == 0: self.dataFile.write("\n")
                if self.transportSolver != None:
                    self.dataFile.close()
                    pass
        return None
    pass
#
# module private functions
#
def _scaling(timeUnit):
    """
    Used to scale the time unit to seconds
    """ 
    tUl = timeUnit.lower()
    if tUl in ["days","day","d"]:                                                                  
        timeUnit="d"
        scalingFactor = 86400
    elif tUl in ["s", "seconds"]:
        timeUnit="s"
        scalingFactor = 1
    elif tUl in ["hours","hour","h"]:
        timeUnit="h"
        scalingFactor = 3600
    elif tUl in ["years", "year","y"]:
        timeUnit="y"
        scalingFactor = 3.15576e+7
    else:
        raise Exception, " your time frequency does\'nt match available ones"
    return timeUnit,scalingFactor
    
    
def _vtkGmsh(indGmsh):
    """
        that function is used to treat the vtk / Gmsh depdency
    """
    if indGmsh == 1:           # 2-node line
        indVtk = 3
    elif indGmsh == 2:         # 3-node triangles
        indVtk = 5
    elif indGmsh == 3:         # 4-node quadrangles
        indVtk = 9
    elif indGmsh == 4:         # 4-node tetrahedron
        indVtk = 10
    elif indGmsh == 5:         # 8-node hexahedrons
        indVtk = 12
    elif indGmsh == 6:         # 6-node prism
        indVtk = 13
    elif indGmsh == 7:         # 5-node pyramid
        indVtk = 14
       
    return indVtk
        
def _coordinatesList(dim,nodesCoordinates):
    #
    # 2D
    #
    x = []
    y = []
    if (dim == 2):
        for node in range(len(nodesCoordinates)):
            x.append(nodesCoordinates[node][0])
            y.append(nodesCoordinates[node][1])
            pass
        pass
        z = [0.]*len(x)
    #
    # 3D
    #
    elif (dim==3):
        z = []  
        for node in range(0,len(nodesCoordinates)):
            x.append(nodesCoordinates[node][0])
            y.append(nodesCoordinates[node][1])
            z.append(nodesCoordinates[node][2])
    else:
       raise "Error in mesh dimension"
    return x,y,z 


def _vtkCellListSize(numberOfCells,connectivity):

    cellListSize = 0
    for i in range(0,numberOfCells):                # gmsh meshes: type of elements
        gmshType = connectivity[i][1]
        if gmshType == 1:           # 2-node line
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
    return cellListSize
    
def _celltypes(connectivity):
    cellType = []
    numberOfCells = len(connectivity)
    for i in range(0,numberOfCells):
        cellType.append(connectivity[i][1])
        pass
    return cellType

def _connectivityList(connectivity):
    connectivityList = []
    for cell in connectivity:
        ind = cell[2]+3
#               print " ctm dbg cell ",vtkTyp,ind,cell," perm ",permutation[ind],permutation[ind+1],permutation[ind+2],permutation[ind+3]
                    # 
        vtkTyp = _vtkGmsh(cell[1])
        if (vtkTyp==3):                                                                     # 2-node line
            connectivityList += [cell[ind]-1, cell[ind+1]-1]
            pass
        elif (vtkTyp==5):                                                                   # triangles
            connectivityList += [cell[ind]-1, cell[ind+1]-1, cell[ind+2]-1]
            pass
        elif (vtkTyp==9):                                                                   # quadr
            connectivityList += [cell[ind]-1, cell[ind+1]-1, cell[ind+2]-1, cell[ind+3]-1]
            pass
        elif (vtkTyp==10):                                                                  # tetra
            connectivityList += [cell[ind]-1, cell[ind+1]-1, cell[ind+2]-1, cell[ind+3]-1]
            pass
        elif (vtkTyp==12):                                                                  # hexahedron
            connectivityList += [cell[ind]-1, cell[ind+1]-1, cell[ind+2]-1, cell[ind+3]-1,\
                       cell[ind+4]-1, cell[ind+5]-1, cell[ind+6]-1, cell[ind+7]-1]
            pass
        pass
    return connectivityList

def _vtkCellTyp(gmshType):
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
    return cellTyp
        
def _vtkFrequency(initialTimeStep, timeUnit, maxTimeStep, vtkFrequency):
    """
    That function is introduced to adapt the frequency plot to the
    minimal time step introduced by the user.
    A Warning is printed if that minimal time step is greater than the frequency introduced.
    """
    tUl = timeUnit.lower()
    if tUl in ["days","day","d"]:                                                                  
        scalingFactor = 86400.
        pass
    elif tUl in ["s", "seconds"]:
        scalingFactor = 1
        pass
    elif tUl in ["hours","hour","h"]:
        scalingFactor = 3600.
        pass
    elif tUl in ["years", "year","y"]:
        scalingFactor = 3.15576e+7
        pass
    else:
        raise Warning, " Your time frequency does\'nt match available ones"
    if vtkFrequency*scalingFactor < maxTimeStep:
        raise Warning, " Vtk plot frequency time should be greater than the max time step" 
    if initialTimeStep == None:
        initialTimeStep = scalingFactor*vtkFrequency
        pass
    else:
        vtkfrequency = max(int(vtkFrequency),int(1.*initialTimeStep/scalingFactor))
        pass
    return initialTimeStep, vtkFrequency
#    
def _gnuTitle(title, subTitle, length, timeSpecification):
    """
    local function used to set the title of a gnuplot output, interactive or png
    """
    if title != None:
        titre = str(title)
        pass
    else:
        titre = 'Etumos Interactive plot:'
        soustitre = '"'
        pass
    #print "title",title
    #raw_input("title")
    if subTitle != None:
        soustitre = '\\n' + str(subTitle) + '"'
        pass
    if length>1:
        return 'set multiplot title "' + titre + ' \\n{/*0.75(time = + %9.2e + years)}'%(timeSpecification/3.15576e+7) + soustitre + \
        " font \"Times-Roman,16\""
    else:
        #return 'set title "' + titre + ' (time = + %9.2e + years)'%(timeSpecification/3.15576e+7) + soustitre + \
        return 'set title "' + titre + ' \\n{/*0.76time = + %9.2e + years)}'%(timeSpecification/3.15576e+7) + soustitre + \
        " font \"Times-Roman,16\""
#    
def _gnuRotate(rotate, length):
    """
    To specify the size of the plots and their origin 
    it returns a string, a list of origins and axis denominations
    """
    if rotate in [None, 'no', 'non', False]:
#      print " value of rotate is False"
        
        if length == 1:
            sizeString = ''
            origins = [' 0.0,0.0',' 0.0,0.0']
            pass
        elif length == 2:           
            sizeString = 'set size 0.4,0.7'
            origins = [' 0.0,0.1',' 0.5,0.1']
            pass
        elif length == 3 or length == 4:
            sizeString = 'set size 0.4,0.445'
            origins = [' 0.0,0.47',' 0.475,0.47', ' 0.0,0.0', ' 0.475,0.0']
            pass
        rot = 'x'
        rot2 = 'y'
        pass
    else:
#                print " value of rotate is True"
        if length == 1:
            sizeString = ''
            origins = [' 0.0,0.0',' 0.0,0.0']
            pass
        elif length == 2:           
            sizeString = 'set size 0.85,0.45'
            origins = [' 0.0,0.45',' 0.0,0.05']
            pass
        elif length == 3 :
            sizeString = 'set size 0.85,0.3'
            origins = [' 0.0,0.5875',' 0.0,0.325', ' 0.0,0.05']
            pass        
        elif length == 4:
            sizeString = 'set size 0.85,0.25'
            origins = [ ' 0.0,0.675', ' 0.0,0.475',' 0.0,0.25', ' 0.0,0.0']
            pass
        rot = 'y'
        rot2 = 'x'
        pass
    return sizeString, origins, rot, rot2

def printm(lineToPrint,ri = None):
    lineToPrint = color.red+"ctmdbg "+lineToPrint+" at line: "+str(currentframe().f_back.f_lineno+1)+" \n"+color.end
    if ri != None:
        raw_input(lineToPrint)
    else:
        print (lineToPrint)
    return None

