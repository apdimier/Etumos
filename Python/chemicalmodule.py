# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
Chemistry module
This module is associated to the class chemical 
"""
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from __future__ import absolute_import
from chemistry  import  ChemicalProblem

from phreeqc import Phreeqc

from PhysicalQuantities import Time,\
                               _findUnit                           

class Chemical:
    """
    Module of Chemistry
    """

    def __init__(self):
        """
        Init

        Examples :
          chem = Chemical()        
        """
        self.activityLaw = None
        self.dB = None
        self.chemicalState = None
        self.comment = ""
        self.kineticLaws = None
        self.name = None
        self.speciesBaseAddenda = None
        self.outputs= None
        self.timeStep= None
        self.simulationTime = None
        
        self.trace= 0

        return None

    def setComment(self, comment):
        self.comment = comment

    def setData(self, problem):
        """
        Within that method we access through the problem to chemical data      
        That method is used in the python script.
        """

        if not isinstance(problem, ChemicalProblem):
            raise Exception(" the problem should be a chemical problem ")

        self.activityLaw =  problem.getActivityLaw()
        self.dB = problem.getDB()
        self.chemicalState = problem.getChemicalState()
        self.kineticLaws =  problem.getKineticLaws()
        self.name =  problem.getName()
        self.outputs =  problem.getOutputs()
        self.speciesBaseAddenda = problem.getSpeciesBaseAddenda()
        self.timeStep =  problem.getTimeStep()
        self.simulationTime = problem.simulationTime

        return None

    def setVerbose(self, trace):
        self.component.setVerbose(trace)

    def initialise(self, componentName= None):
        """
        As in a fairy tale, if the emse software is introduced
        """
        self.component = Phreeqc()
        self.solver = self.component                                                        # to evolve to solver

        self.componentName = "phreeqc"

        self.component.setDataBase(self.dB)       

        self.component.setChemicalState(self.chemicalState)

        if self.activityLaw:
            self.component.setActivityLaw(self.activityLaw)
            pass
        if self.kineticLaws:
            self.component.setKineticLaws(self.kineticLaws)
            pass
        if self.outputs:
            self.component.setExpectedOutputs(self.outputs)
            pass
        if self.speciesBaseAddenda:
            self.component.setSpeciesBaseAddenda(self.speciesBaseAddenda)
            pass
        if self.timeStep:
            self.component.setTimeStep(self.timeStep)
            pass
        if isinstance(self.simulationTime,Time):
                self.component.setSimulationTime(self.simulationTime)
        if self.timeStep and self.simulationTime:
            self.component.batch == True
        return None

    def setParameter(self, out):
        """
        Set specific component parameters
          Input :
              parameter_name (string)
              parameter_value ()
        """
        if self.component:
            self.component.setParameter(out)
        else:
            raise Exception("You have to execute setComponent before setParameter")
        return None

    def setComponent(self,name):
        self.initialise()

    def setComponentTimeParameters(self):
        """
        Set specific time component parameters
          Input :
        """
        if self.component:
            if isinstance(self.timeStep,Time) and isinstance(self.simulationTime,Time):
                self.component.setTimeParameters(self.timeStep, self.simulationTime)
            else:
                raise Warning("check the definition of the time parameters of the chemicalproblem instance.")
        else:
            raise Exception("You have to execute setComponent before setTimeParameters")
        return None

    def run(self):
        """
        Used to simulate a chemical equilibrium once that one
        has been defined within the problem

        module = Chemical()
        problem  = ChemicalProblem(name               = "soda",\
                           dB                = "phreeqc.dat",\
                           speciesBaseAddenda = speciesAddenda,\
                           chemicalState      = sodaChemicalState)
        module.setData(problem)
        module.initialise()
        module.setParameter("soda.out")
        module.run()
        
        The evolution of a batch over time can also be modelled. Then time steps and the simulation time have
        to be introduced.
        """

        if self.component:
            self.component.run()
        else:
            raise Exception("You have to execute setComponent before run")
        return

    def launch(self):

        self.run()


    def end(self):
        """
        To Stop phreeqc
        """
        if self.component:
            self.component.end()
        return None

    def getOutput(self, outputName=None, outputFormat = None):
        """
        To get a specific output
          Input :
            outputName (string) : it can be the name of a specified
            ExpectedOutput or 'state'. If 'state'  specified, it returns a *
            list of data. 
          Ouput :
            ()
          pH = module.getOutput('pH')
        """
        if (outputName==None):
            outputName='state'
        if self.component:
            if (outputName=='state'):
                if outputFormat == None:
                    return self.component.getOutputState()
                else:
                    return self.component.getOutputState({})
            elif (outputName=='componentsConcentration'):
                self.component.getPrimarySpeciesNames()
                return self.component.getMobileConcentration()
            else:
                return self.component.getOutput(outputName)
            pass
        else:
            raise Exception("You have to execute setPrimary before getOutput")
        return

    def outputStateSaving(self):
        """
        Permits to retrieve from Phreeqc information on the current state
        It furnishes a unique list containing in order of appearance:
               aqueous primary species number
               aqueous secondary species number
               sorbed species number
               minerals number            
               ph
           pe
           water activity
           ionicstrength
               temperature
               electrical_balance
           total_h
           total_o
           and a list of tuples representing the aqueous and mineral states
        """
        state = self.getOutput()
        #print type(state)
        if self.component.outFile == None:
            outFile = open("phreeqCFile.out", 'w')
        else:
            outFile = open(self.component.outFile, 'w')
        outFile.write("%20s\n\n\n"%str(self.comment))
        outFile.write("number of aqueous primary species      %20s\n"%str(state[0]))
        outFile.write("number of aqueous secondary species    %20s\n"%str(state[1]))
        outFile.write("number of minerals                     %20s\n"%str(state[3]))
        outFile.write("number of sorbed species               %20s\n"%str(state[2]))
        outFile.write("\npH                                   %20s\n"%str(state[4]))
        outFile.write("pe                                     %20s\n"%str(state[5]))
        outFile.write("water activity                         %20s\n"%str(state[6]))
        outFile.write("ionicstrength                          %20s\n"%str(state[7]))
        outFile.write("temperature                            %20s\n"%str(state[8]))
        outFile.write("electrical_balance                     %20s\n"%str(state[9]))
        outFile.write("total H                                %20s\n"%str(state[10]))
        outFile.write("total O                                %20s\n"%str(state[11]))
        outFile.write("density of water                       %20s\n"%str(state[12]))
        #print " type",state[11],type(state[10])
        ind = 0
        anf = 13
        end = anf + int(state[0])
        #print state
        outFile.write("\n\n primary species: mol/l\n\n")
        for i in state[anf:end]:
            outFile.write("%20s %s\n"%(str(i[0]),str(i[1])))
        anf = end
        end = anf + int(state[1])            
        outFile.write("\n\n secondary species: mol/l\n\n")
        for i in state[anf:end]:
            outFile.write("%20s %s\n"%(str(i[0]),str(i[1])))
        anf = end
        end = anf + int(state[2])            
        outFile.write("\n\n sorbed species: moles\n\n")
        for i in state[anf:end]:
            outFile.write("%20s %s\n"%(str(i[0]),str(i[1])))
        anf = end
        outFile.write("\n\n     SI( target saturation index):        SI < 0 undersaturation, 0: equilibrium and supersaturation otherwise\n\n")
        outFile.write("\n\n")
        outFile.write("\n\n                 mineral species:            SI                   moles\n\n")
        for i in state[anf:]:
            outFile.write("%30s         %15.8e      %15.8e\n\n"%(str(i[0]),float(str(i[2])),float(str(i[1]))))


    def printOutputState(self):
        """
        Print chemical state speciation

          Examples
            chem_uo2.printOutputState()
        """
        if self.component:
            self.component.printOutputState()
        else:
            raise Exception("You have to execute setPrimary before getOutput")
        return
