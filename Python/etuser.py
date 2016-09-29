# -*- coding: utf-8 -*-
#/usr/bin/python
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This file is used to enable the introduction of 
# user defined functions. Through that way, the user can 
# introduce its own programming to handle specific parameters
# or physical parameters. The user has to pay attention to the 
# unknown definition due to the python paradigms:
# Every external variable and every method should have "us" as prefix
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
        This file is used to enable the introduction of 
        user defined functions. Through that way, the user can 
        introduce its own programming to handle specific parameters
        or physical parameters.

        Warning:
        
               Every external variable and every method should have "us" as prefix
               
               The timeStepNumber is initially 0 and it has to be taken into account within the algorithm
"""
from __future__ import absolute_import
from __future__ import print_function
import wx

from physicallaws import IntrinsicPermeabilityLaw
from six.moves import range

def totoUser():
    print("It works")
    
def userList (ctmi):
    """
    The user defines here the lists involved in the user defined functions
    """
    ctmi.initialPorosity = []
    pass
    
def userTuple (ctmi):
    """
    The user defines here the lists involved in the user defined functions
    """
    pass
    
def userDictionnary (ctmi):
    """
    The user defines here the dictionnary involved in the user defined functions
    """
    ctmi.usE = {}
    pass

def userBrasilianTestLaw (ctmi):
    """
    Setting the porosity to variable, you 
    construct here the following effective Young modulus
    
     E = E0(1-w/w0)**f 
    """
    #print "It works too: ",ctmi.cpuTime()
    E0 = 57.73
    f = 2.1
    ctmi.youngModulusField = []
    if (ctmi.variablePorosityOption ):
        porosityField = ctmi.chemical.getPorosityField()
        pass
    else:
        print(" che mod? ",ctmi.__class__.__name__)
        porosityField = ctmi.initialPorosityValues
        pass
    #print "porosity field ",porosityField[0:5],len(porosityField),len(ctmi.initialPorosityValues)
    ind = 0
    for porosity in porosityField:
        if porosity <= ctmi.initialPorosityValues[ind]:
            aux = E0
            ind+=1
            pass
        else:
            aux = E0*((1-porosity)/(1- ctmi.initialPorosityValues[ind]))**f
            ind+=1
            pass
        #print " ind of the etuser loop ",ind,aux
        ctmi.youngModulusField.append(aux)
        pass
    #
    #
    #
    print(" effective Young modulus ",ctmi.youngModulusField[0:5],len(ctmi.youngModulusField))
    ctmi.transportSolver.essai.setMYField(ctmi.youngModulusField)
    print(" effective Young modulus ",ctmi.youngModulusField[0:5],len(ctmi.youngModulusField))

def effectiveYoungModulus (ctmi):
    """
    Setting the porosity to variable, you 
    construct here the following effective Young modulus
    
     E = E0(1-w/w0)**f 
    """
#    print "It works too: ",ctmi.cpuTime()
    E0 = 1.e+3
    f = 2.1
    ctmi.usE = []
    porosityField = ctmi.chemical.getPorosityField()
    #print porosityField[0:5]
    if ctmi.initialPorosity == []:
        for i in porosityField:
            ctmi.initialPorosity.append(i)
            pass
        pass
    ind = 0
    for i in porosityField:
        if i > ctmi.initialPorosity[ind]:
            aux = E0
            pass
        else:
            aux = E0*(1-i/ctmi.initialPorosity[ind])**f
            pass
        ctmi.usE.append(aux)
        ind+=1
        pass
#    print " effective Young modulus ",ctmi.usE[0:10]

def setInitialPorosity (ctmi):
    """
    Example of a function used to set an initial porosity field for a plug:
    
            the initial porosity is 0.05
            the initial mineral amount is 2.57216e+01
    """
    print("It works too: ",ctmi.cpuTime())
    if ctmi.timeStepNumber == 0:
        amount = []
        if ctmi.TransportComponent == 'elmer':
            #print " we are in the setInitialPorosity function "
            ind = 0
            coordinates = ctmi.transportSolver.getCoordinatesValues() #meshPointCoordinates
            
            #print type(coordinates),len(coordinates[0])
            elementsNumber = len(coordinates[0])
            initialPorosity = []
            for point in range(1,elementsNumber+1):
                #print point, elementsNumber
                radius = coordinates[ 1][(point-1)]**2+coordinates[ 2][(point-1)]**2
                porosity = 0.05 + radius**0.5
                #print " porosity ",point, porosity
                initialPorosity.append(porosity)
                amount.append(2.57216e+01*0.05/porosity)
                pass
            #print "we are out of the porosity evaluation ",len(initialPorosity)
            ctmi.transportSolver.setPorosityField(initialPorosity)
            ctmi.chemical.setPorosity(initialPorosity)
            print("we go out of the porosity function and call set mineral amount\n")
            ctmi.chemical.setMineralAmount("KCalcite",amount)
            print(" python set Mineral Amount %s\n"%(2.57216e+01*0.05/porosity))
            pass
        else:
            raise Exception("You are using Mt3d, the setInitialPorosity user function has only been validated using Elmer")
        pass
    else:
        pass

def setInitialPorosity1 (ctmi):
    """
    Example of a function used to set an initial porosity field for a plug:
    
            the initial porosity is 0.1, see the Gaussian distribution parameters:
            
            gauss(mu,sigma) mu is the mean, and sigma is the standard deviation.
            the outer radius is 0.0125
    """
    print("It works too: ",ctmi.cpuTime())
    outerRadius = 0.0125
    if ctmi.timeStepNumber == 0:
        amount = []
        if ctmi.TransportComponent == 'elmer':
            #print " we are in the setInitialPorosity function "
            ind = 0
            coordinates = ctmi.transportSolver.getCoordinatesValues() #meshPointCoordinates
            
            #print type(coordinates),len(coordinates[0])
            elementsNumber = len(coordinates[0])
            initialPorosity = []
            for point in range(1,elementsNumber+1):
                #print point, elementsNumber
                radius = (coordinates[ 1][(point-1)]**2+coordinates[ 2][(point-1)]**2)**0.5
                porosity = 0.10 + (radius-outerRadius/2.)/(outerRadius*50)
                #print " porosity ",point, porosity
                initialPorosity.append(porosity)
                amount.append(2.57216e+01*0.09/porosity)
                pass
            #print "we are out of the porosity evaluation ",len(initialPorosity)
            ctmi.transportSolver.setPorosityField(initialPorosity)
            ctmi.chemical.setPorosity(initialPorosity)
            print("we go out of the porosity function and call set mineral amount\n")
            ctmi.chemical.setMineralAmount("KCalcite",amount)
            print(" python set Mineral Amount %s\n"%(2.57216e+01*0.05/porosity))
            pass
        else:
            raise Exception("You are using Mt3d, the setInitialPorosity user function has only been validated using Elmer")
        pass
    else:
        pass

def setInitialPorosity2 (ctmi):
    """
    Example of a function used to set an initial porosity field for a plug:
    
            the initial porosity is 0.1, see the Gaussian distribution parameters:
            
            gauss(mu,sigma) mu is the mean, and sigma is the standard deviation.
            the initial mineral amount is 2.57216e+01
            the outer radius is 0.0125
    """
    from random import gauss 
    print("It works too: ",ctmi.cpuTime())
    outerRadius = 0.0125
    if ctmi.timeStepNumber == 0:
        amount = []
        if ctmi.TransportComponent == 'elmer':
            #print " we are in the setInitialPorosity function "
            ind = 0
            coordinates = ctmi.transportSolver.getCoordinatesValues() #meshPointCoordinates
            
            #print type(coordinates),len(coordinates[0])
            elementsNumber = len(coordinates[0])
            initialPorosity = []
            for point in range(1,elementsNumber+1):
                #print point, elementsNumber
                radius = (coordinates[ 1][(point-1)]**2+coordinates[ 2][(point-1)]**2)**0.5
                porosity = gauss(0.1,0.005)
                initialPorosity.append(porosity)
                amount.append(2.57216e+01*0.10/porosity)
                #print " porosity ",point, porosity, amount[-1]
                pass
            print("we are out of the porosity evaluation ",len(initialPorosity))
            ctmi.transportSolver.setPorosityField(initialPorosity)
            ctmi.chemical.setPorosity(initialPorosity)
            ctmi.chemical.setMineralAmount("KCalcite", amount)
            print(" python set Mineral Amount\n",porosity, 2.57216e+01*0.09/porosity, amount[10], amount[-1])
            #raw_input( "we go out of the porosity function and call set mineral amount\n")
            print("length of amount",len(amount))
            #print ctmi.chemical.getImmobileConcentration("KCalcite")
            #raw_input( "we go out of the porosity function and call set mineral amount\n")
            pass
        else:
            raise Exception("You are using Mt3d, the setInitialPorosity user function has only been validated using Elmer")
        pass
    else:
        pass

def setInitialPorosityAutoklav (ctmi):
    """
    Example of a function used to set an initial porosity field for a plug:
    
            the initial porosity is 0.131, see the Gaussian distribution parameters:
            
            gauss(mu,sigma) mu is the mean, and sigma is the standard deviation.
            the initial mineral amount is 2.57216e+01
            the outer radius is 0.5*0.02553
    """
    from random import gauss 
    print("It works too: ",ctmi.cpuTime())
    outerRadius = 0.5*0.02553
    if ctmi.timeStepNumber == 0:
        amount = []
        if ctmi.TransportComponent == 'elmer':
            #print " we are in the setInitialPorosity function "
            ind = 0
            coordinates = ctmi.transportSolver.getCoordinatesValues() #meshPointCoordinates
            
            #print type(coordinates),len(coordinates[0])
            elementsNumber = len(coordinates[0])
            initialPorosity = []
            for point in range(1,elementsNumber+1):
                #print point, elementsNumber
                radius = (coordinates[ 1][(point-1)]**2+coordinates[ 2][(point-1)]**2)**0.5
                porosity = gauss(0.131,0.005)
                initialPorosity.append(porosity)
                amount.append(177.4072192041498*0.90/porosity)
                #print " porosity ",point, porosity, amount[-1]
                pass
            print("we are out of the porosity evaluation ",len(initialPorosity))
            ctmi.transportSolver.setPorosityField(initialPorosity)
            ctmi.chemical.setPorosity(initialPorosity)
            ctmi.chemical.setMineralAmount("KCalcite", amount)
            print(" python set Mineral Amount\n",porosity, 177.4072192041498*0.90/porosity, amount[10], amount[-1])
            #raw_input( "we go out of the porosity function and call set mineral amount\n")
            print("length of amount",len(amount))
            #print ctmi.chemical.getImmobileConcentration("KCalcite")
            #raw_input( "we go out of the porosity function and call set mineral amount\n")
            pass
        else:
            raise Exception("You are using Mt3d, the setInitialPorosity user function has only been validated using Elmer")
        pass
    else:
        pass

def getChemicalSpecificOutputs (ctmi):
    """
    That function enables to retrieve a value or a list of values over time
    """
#    indice = 131
#    listOfUnknownsToPlot = ["Temperature","Anhydrite","Ta"]
#    print " ctmi ",ctmi.timeStepNumber
    if ctmi.timeStepNumber == 0:
        ctmi.usE = {}
        ctmi.usE["indice"] = 90
        listOfUnknownsToPlot = ["temperature", "Anhydrite", "Ca", "Tr"]
        for unknown in listOfUnknownsToPlot:
            ctmi.usE[unknown] = []
            pass
        ctmi.usE["time"] = []
        pass
    else:
        pass
    ctmi.usE["time"].append(ctmi.simulatedTime)
#    print " ctm dbgggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggguse indice",ctmi.usE["indice"]
    for unknown in ctmi.usE.keys():
        if unknown not in ["indice","time"] :
#            print " unknown ",unknown
            unknownValue = ctmi.chemical.getOutput( unknown, 
                                                    outputType = "point", 
                                                    anf = ctmi.usE["indice"])
#            print " unknown value ",unknownValue
            ctmi.usE[unknown].append(unknownValue[0])
            pass
        pass
        
#    print     ctmi.usE

def getBChemicalSpecificOutputs (ctmi):
    """
    That function enables to retrieve a value or a list of values over time
    """
#    indice = 131
#    listOfUnknownsToPlot = ["Temperature","Anhydrite","Ta"]
    if ctmi.timeStepNumber == 0:
#        print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        ctmi.usE = {}
        ctmi.usE["indice"] = 100
        listOfUnknownsToPlot = ["temperature", "KBarite", "Ba", "Tr"]
        for unknown in listOfUnknownsToPlot:
            ctmi.usE[unknown] = []
            pass
        ctmi.usE["time"] = []
        pass
    else:
        pass
    ctmi.usE["time"].append(ctmi.simulatedTime)
#    print " ctm dbgggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggguse indice",ctmi.usE["indice"]
    for unknown in ctmi.usE.keys():
        if unknown not in ["indice","time"] :
#            print " unknown ",unknown
            unknownValue = ctmi.chemical.getOutput( unknown, 
                                                outputType = "point", 
                                                anf = ctmi.usE["indice"])
#            print " unknown value ",unknownValue
            ctmi.usE[unknown].append(unknownValue[0])
            pass
        pass
        
#    print     ctmi.usE

def plotOverTime (ctmi):
    """
    That function enables to retrieve a value or a list of values over time
    """
    nameFile = "plotOverTime.data"
    
    if ctmi.timeStepNumber == 1:
        f = open(nameFile,"w")
        ctmi.usTimeStudy = {}
        ctmi.usTimeStudy["Indice"]=[]
        ctmi.usTimeStudy["Output"]=[]
        ctmi.usTimeStudy["Result"]=[]
        f.write("time ")
        for parameter in ctmi.problem.getOutputTimeStudy() :
            ctmi.usTimeStudy["Indice"].append(parameter[1])
            ctmi.usTimeStudy["Output"].append(parameter[0])
            ctmi.usTimeStudy["Result"].append([])
            f.write("\""+parameter[0]+"\"_at_Point_"+str(parameter[1])+" ")
            pass
        ctmi.usTimeStudy["time"] = []
        f.write("\n")
        pass
    else:
        f = open(nameFile,"a")
        pass
    ctmi.usTimeStudy["time"].append(ctmi.simulatedTime)
    f.write(str(ctmi.simulatedTime)+" ")
    for i in range(len(ctmi.usTimeStudy["Output"])):
        unknownValue = ctmi.chemical.getOutput( ctmi.usTimeStudy["Output"][i], 
                                                outputType = "point", 
                                                anf = ctmi.usTimeStudy["Indice"][i])
        ctmi.usTimeStudy["Result"][i].append(unknownValue[0])
        f.write(str(unknownValue[0])+" ")
        pass
    f.write("\n")
    f.close()
    
def progressionSimulation (ctmi):
    if ctmi.timeStepNumber == 1:
        ctmi.usAPP = wx.App(0)
        ctmi.usAPP.MainLoop()
        ctmi.usDLG = wx.ProgressDialog( "Progression", "Simulation...", parent = None)
        pass
    l = ctmi.simulatedTime
    total = ctmi.finalTime
    temp= l*100./total
    ctmi.usDLG.Update(temp,"Simulation...")
    if l>total or l==total :
        ctmi.usDLG.Destroy()
        pass
#
# A generic user specified intrinsic permeability law
#    
class userKozenyCarmanLaw(IntrinsicPermeabilityLaw):
    """
    
    Kozeny-Carman law defined as :
    
        k_i     initial permeability
        por_i   initial porosity
        
        and via the eval function wth :
        
        por     current porosity
        
        Ki * ((1. - por_i)/(1. - por))**2/( (por/por_i)**3 )
        
    """
    def __init__(self,**kargs):
        print(" args ",kargs)
        IntrinsicPermeabilityLaw.__init__(self,**kargs)
        pass
#
    def eval(self,currentPorosityValue):
        print(currentPorosityValue,self.k0,self.initialPorosity)
        return  self.k0 * pow( (1.-self.initialPorosity) / (1.-currentPorosityValue), 2) / \
                          pow( currentPorosityValue / self.initialPorosity, 3)
#
#
#
def userPermeabilityLaw(ctmi):
    """

    The function defined here is used to test the algorithm

    """
    if ctmi.hydraulicFrequency  != 0:
        if ctmi.timeStepNumber % ctmi.hydraulicFrequency == 0 or ctmi.timeStepNumber == 1:
            print(" length of the permeabilityField ", ctmi.mesh._getNumberOfVertices())
            permeabilityField = [0.0]*ctmi.mesh._getNumberOfVertices()
            print(" length of the permeabilityField ", len(permeabilityField))
            #raw_input(" length of the permeabilityField ")
            for i in range(len(permeabilityField)):
                if ctmi.timeStepNumber<= 10:
                    factore = 2.0
                    pass
                else:
                    factore = 1.0
                    pass
                permeabilityField[i] = factore*1.e-5
                pass
            ctmi.transportSolver.setPermeabilityField(permeabilityField)
            pass
        pass
    return None
#
def fracturePermeabilityLaw (ctmi):
    """

    That function enables to treat the evolution of the permeability law as
    a function of porosity.

    """
    if ctmi.hydraulicFrequency != 0:
        if ctmi.timeStepNumber % ctmi.hydraulicFrequency == 0 or ctmi.timeStepNumber == 1:
            permeabilityField = [0.0]*ctmi.internalNodesNumber
            poros = ctmi.chemicalSolver.getPorosityField()
            nodes = ctmi.mesh.getNodesCoordinates()
            for node in range(len(ctmi.parpertionList)):
                ind = ctmi.parpertionList[node]
                if nodes[ind][0] <= 0.005:
                    permeabilityField[ind] = (1.6e-14*1000*10/1.e-3)*(poros[ind]/0.4)**3
                    #permeabilityField[node] = 1.6e-14*1000*10/1.e-3
                else:
                    permeabilityField[ind] = 1.6e-18*1000*10/1.e-3*(poros[ind]/0.15)**3
                    #permeabilityField[node] = 1.6e-18*1000*10/1.e-3
            ctmi.transportSolver.setPermeabilityField(permeabilityField)
    return None
#
def plugPermeabilityLaw(ctmi):
    """

    The function is used to redefine the permeability as a function of porosity evolution.
    
    We use a Verma Pruess law for the evolution of the permeability.
    

    """
    if ctmi.hydraulicFrequency  != 0:
        #
        # we update the flow at the first time step (ctmi.timeStepNumber == 1)
        #
        if ctmi.timeStepNumber % ctmi.hydraulicFrequency == 0 or ctmi.timeStepNumber == 1:
            print(" length of the permeabilityField ", ctmi.mesh._getNumberOfVertices())
            permeabilityField = [0.0]*ctmi.mesh._getNumberOfVertices()
            print(" length of the permeabilityField ", len(permeabilityField))
            #raw_input(" length of the permeabilityField ")
            for i in range(len(permeabilityField)):
                if ctmi.timeStepNumber== 10:
                    factore = 2.0
                    pass
                else:
                    factore = 1.0
                    pass
                permeabilityField[i] = factore*1.e-5
                pass
            ctmi.transportSolver.setPermeabilityField(permeabilityField)
            pass
        pass
    return None
#
#
#
def userPermeability_old (ctmi):
    print("It works too: ",ctmi.cpuTime())
    if ctmi.timeStepNumber == 0:
        amount = []
        if ctmi.TransportComponent == 'elmer':
            ind = 0
            coordinates = ctmi.transportSolver.getCoordinatesValues() #meshPointCoordinates
            
            print(type(coordinates),len(coordinates[0]))
            elementsNumber = len(coordinates[0])
            initialPorosity = []
            for point in range(1,elementsNumber+1):
                radius = coordinates[ 1][(point-1)]**2+coordinates[ 2][(point-1)]**2
                porosity = 0.05 + radius**0.5
                initialPorosity.append(porosity)
                amount.append(2.57216e+01*0.05/porosity)
                pass
            ctmi.transportSolver.setPorosityField(initialPorosity)
            ctmi.chemical.setPorosity(initialPorosity)
            print("we go out of the porosity function and call set mineral amount\n")
            ctmi.chemical.setMineralAmount("KCalcite",amount)
            print(" python set Mineral Amount %s\n"%(2.57216e+01*0.05/porosity))
            pass
        else:
            raise Exception("You are using Mt3d, the setInitialPorosity user function has only been validated using Elmer")
        pass
    else:
        pass


#
def userVermaPruessPermeability (ctmi):
    print(" It works too: ",ctmi.cpuTime())
                
    porosityField = ctmi.transportSolver.getPorosityField()
    for i in range(porosityField):
        permeabilityField[i] = initialPermeability[i]*\
                               ( (porosityField[i] - criticalPorosity)/(initialPorosity[i] - criticalPorosity) )**1.5
        pass
    
def specificHeatCapacityLaw(ctmi):
    """
    To set the heat capacity of water
    
      Cp(T) =  4.214 - 2.286 * 1.e-3 * T + 4.991 * 1.e-5 * T**2 - 4.519 * 1.e-7 * T**3 + 1.857 * 1.e-9 * T**4 in kJ/m/K
      
      The température is expressed here in Celcius degree, and thereafter in K:
      
      Cp(T) =  28.07 - 0.2817 * T + 1.250 * 1.e-3 * T**2 - 2.480 * 1.e-6 * T**3 + 1.857 * 1.e-9 * T**4 
 
      source http://www.iapws.org
       
    """
    ctmi.usE = []
    temperatureField = ctmi.transport.getTemperatureField()
    specificHeatCapacityField = []
    for temp in temperatureField:
        cp = 4.214 + (-2.286 * 1.e-3 + 4.991 * 1.e-5 * temp - 4.519 * 1.e-7 * temp*temp + 1.857 * 1.e-9 * temp*temp*temp)*temp
        specificHeatCapacityField.append(cp*1000) #  a factor of 1000 to obtain J per kg
        #print(" Variable Heat Capacity ",temp,cp*1000)
        pass
    ctmi.transportSolver.setWHeatCapacityField(specificHeatCapacityField)
    return None

    
def specificHeatCapacityLaw_ex(ctmi):
    """
    To set the heat capacity of water
    
      Cp(T) =  4.414 - 2.286 * 1.e-3 * T + 4.991 * 1.e-5 * T**2 - 4.519 * 1.e-7 * T**3 + 1.857 * 1.e-9 * T**4 in kJ/m/K
      
      The température is expressed here in Celcius degree, and thereafter in K:
      
      Cp(T) =  28.07 - 0.2817 * T + 1.250 * 1.e-3 * T**2 - 2.480 * 1.e-6 * T**3 + 1.857 * 1.e-9 * T**4 
 
      source http://www.iapws.org
       
    """
    ctmi.usE = []
    temperatureField = ctmi.transport.getTemperatureField()
    specificHeatCapacityField = []
    for temp in temperatureField:
        cp = 4.414 + (-2.286 * 1.e-3 + 4.991 * 1.e-5 * temp - 4.519 * 1.e-7 * temp*temp + 1.857 * 1.e-9 * temp*temp*temp)*temp
        specificHeatCapacityField.append(cp*1000) #  a factor of 1000 to obtain J per kg
        #print(" Variable Heat Capacity ",temp,cp*1000)
        pass
    ctmi.transportSolver.setWHeatCapacityField(specificHeatCapacityField)
    return None
    
def heatConductivityLawKelvin1(ctmi):
    """
    To set the thermal conductivity
    
      k(T) =  -1.48445 + 4.12292 *  T - 1.63866 * T**2 with T = T/298.15
      
      ref. conductivity is at 298.15 : 0.6065 W/ m/ K
      
      Standard Reference Data for the Thermal Conductivity Of Water
      
      M. L. V. Ramires and Al.: http://www.nist.gov/data/PDFfiles/jpcrd493.pdf
      
    """
    refConductivity = 0.6065
    ctmi.usE = []
    temperatureField = ctmi.transport.getTemperatureField()
    thermalConductivityField = []
    for temperature in temperatureField:
        ktemperature = (temperature+273.15)/298.15
        #print " normalised temperature ",ktemperature, (-1.48445 + 4.12292 * ktemperature - 1.63866 * ktemperature*ktemperature)*refConductivity
        thermalConductivityField.append((-1.48445 + 4.12292 * ktemperature - 1.63866 * ktemperature*ktemperature)*refConductivity)
        pass
    ctmi.transportSolver.setWHeatConductivityField(thermalConductivityField)
    return None
    
def heatConductivityLaw(ctmi, units = None):
    """
    To set the thermal conductivity of water
    
      k(T) =  0.5636 + 1.946 * 1.e-3 * T -8.151 * 1.e-6 * T**2
      
      The température is expressed here in Celcius degree, and thereafter in K:
      
      k(T) =  -0.5752 + 6.397 * 1.e-3 * T - 8.151 * 1.e-6 * T**2
 
      source http://www.iapws.org
       
    """
    ctmi.usE = []
    temperatureField = ctmi.transport.getTemperatureField()
    thermalConductivityField = []
    for temperature in temperatureField:
        thermalConductivityField.append(0.5636 + 1.946 * 1.e-3 * temperature -8.151 * 1.e-6 * temperature*temperature)
        pass
    ctmi.transportSolver.setWHeatConductivityField(thermalConductivityField)
    return None

    
def DieserSpecificHeatCapacityLaw_ex(ctmi):
    """
    To set the heat capacity of water
    
      Cp(T) =  4.414 - 2.286 * 1.e-3 * T + 4.991 * 1.e-5 * T**2 - 4.519 * 1.e-7 * T**3 + 1.857 * 1.e-9 * T**4   in kJ/kg/C
      
      The température is expressed here in Celcius degree, and thereafter in K:
      
      Cp(T) =  28.07 - 0.2817 * T + 1.250 * 1.e-3 * T**2 - 2.480 * 1.e-6 * T**3 + 1.857 * 1.e-9 * T**4          in kJ/kg/K
 
      source http://www.iapws.org
       
    """
    ctmi.usE = []
    p_bar = 10.
    # parameters
    # ----------
    #
    # formula 23
    #
    q10 = 47.9048 - 9.36994e-3*p_bar + 6.51059e-6*p_bar**2
    q11 = -32.1724 + 0.0621255*p_bar
    q12 = (-1)*(q10 + q11)
    #
    # formula 24
    #
    q21 = -1.69513 - 4.52781e-4*p_bar - 6.04279e-8*p_bar**2
    q22 = 0.0612567 + 1.88082e-5*p_bar
    q20 = 1 - q21*q22**0.5
    q23 = (0.241022 + 3.45087e-5*p_bar - 4.28356e-9*p_bar**2) - q20 - q21*(1+q22)**0.5
    #
    temperatureField = ctmi.transport.getTemperatureField()
    clConcentrationField = ctmi.getSpecificPrimaryspeciesField("Cl")
    specificHeatCapacityField = []
    ind = 0
    for temperature in temperatureField:
    #
    # formula 22
    #
    #   q1 = q10 + q11*(1-molFrac_NaCl) + q12*(1-molFrac_NaCl)**2
        molFrac_NaCl = clConcentrationField[ind]
        q2 = q20 + q21*(molFrac_NaCl+q22)**0.5 + q23*molFrac_NaCl
        cp =    4.414 + (-2.286 * 1.e-3 + 4.991 * 1.e-5 * temperature - 4.519 * 1.e-7 * temperature*temperature + 1.857 * 1.e-9 * temperature*temperature*temperature)*\
                temperature
        specificHeatCapacityField.append(cp) #  a factor of 1000 to obtain J per kg
        #print " Variable Heat Capacity ",ind, molFrac_NaCl, temperature, cp
        ind+=1
        pass
    ctmi.transportSolver.setWHeatCapacityField(specificHeatCapacityField)
    return None


