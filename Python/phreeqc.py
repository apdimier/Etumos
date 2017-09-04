# -*- coding: utf-8 -*-
"""
    The file is used to build up the PhreeqC structure necessary to phreeqc 
    and to ensure communication within the splitting algorithm
    
    internal nodes are set within the init method
"""
from __future__ import absolute_import
from __future__ import print_function
from chemistry import ActivityLaw,\
                      Bdot,\
                      Davies,\
                      DebyeHuckel,\
                      ExchangeBindingSpecies,\
                      FreeKineticLaw,\
                      GasPhase,\
                      MineralConcentration,\
                      MineralTotalConcentration,\
                      ReversibleKineticLaw,\
                      Salt,\
                      Species,\
                      SpecificAreaPerMole,\
                      SpecificAreaPerGram,\
                      SurfaceBindingSpecies,\
                      SurfaceMineralBindingSpecies,\
                      ToDissolveMineralTotalConcentration,\
                      WYMEKineticLaw

from chemicaltransport import ChemicalTransportProblem
from thmcproblem import THMCProblem       
from constant import epsFP

from exceptions import Warning

from generictools import isInstance

from generictools import color

from math import floor,log10

from os import system

import os

from PhysicalProperties import ElectricPotential,\
                               ReactionRate

from PhysicalQuantities import MolesAmount,\
                               PhysicalQuantity,\
                   Time
                 
from re import compile as recompile

from species import AqueousMasterSpecies,\
                    AqueousSecondarySpecies,\
                    MineralSecondarySpecies,\
                    SorbedSecondarySpecies,\
                    SorbingSiteMasterSpecies,\
                    SurfaceSecondarySpecies,\
                    SurfaceSiteMasterSpecies
                   
from species import molarMassStringEval

from string import ascii_letters, lower, upper, uppercase

from sys import exit,path

from types import DictType, FloatType, IntType, NoneType, StringType
from six.moves import range

def molarMassStringEval_old(mineralName):
    """ 
    Enables to determine the molar mass via an anlysis of the name:
    molarMassStringEval("SiO2") -> [('Si', 1.0), ('O', 2.0)]
    
    """
    #print " string name of the species ",mineralName
    #raw_input()
    mineralString = mineralName[:]
    if mineralString.find(":")!=-1:
        #
        # Some elements entail ":", we extract it from the name
        # we search the occurence of : and work hereafter on two lists: is it necessary?
        #
        mineralString = [mineralName[0:mineralName.index(":")],mineralName[mineralName.index(":")+1:]]
        print(" Warning in the evaluation of molar mass ",mineralString)
        pass
    else:
        mineralString = [mineralName[:]]
        pass
        
    elementList = []
    listOfSpecies = []
    #print " mineralString to be treated ",mineralString
    for character in mineralString:
        if len(character)!=0:
            elementList.append((character,1.))
            pass
        pass
        
    print(" elementList",elementList)
    #
    # the list of master species being established,
    # we treat it.
    #
    for element in elementList:
        elementName = element[0]
        lengthName = len(elementName)
        lange = 0
        while lange < lengthName:
            gewicht = element[1]
            digit = 1.0
            char = elementName[lange]
            if (lange<lengthName):
                if lange+1<lengthName:
                    if elementName[lange+1].isalpha():
                        #
                        # we have an element and now we control its length
                        #
                        if elementName[lange+1] != elementName[lange+1].upper():
                            char += elementName[lange+1]
                            lange += 2
                            if lange < lengthName:
                                iaux = lange
                                print(" here we are ",lange,elementName[lange],lengthName)
                                while elementName[lange].isdigit()  or elementName[lange] == "." and lange < lengthName:
                                    digit = digit*float(elementName[iaux:lange+1])
                                    lange += 1
                        else:
                            lange += 1
                            pass
                    elif elementName[lange+1].isdigit():
                        #
                        # if the element is made only of one character O, C, ...
                        #
                        ind,digit = ionNumbering(elementName[lange+1:])
                        lange += ind+1
                    else:
                        lange += 1
                        cont = 1
                else:
                    lange += 1
            listOfSpecies.append((char,float(gewicht)*float(digit)))
        ind = 0
        indBeg = 0
        indEnd = 0
        for species in listOfSpecies:
            if species[0] == '(':
                indBeg = ind
                pass
            if species[0] == ')':
                indEnd = ind
                for indlist in  range(indBeg+1,indEnd):
                    coef = listOfSpecies[indlist][1]*listOfSpecies[indEnd][1]
                    listOfSpecies[indlist] = (listOfSpecies[indlist][0],coef)
                    pass
            ind += 1
            pass
        ind = 0
        for char in listOfSpecies:
            if char[0] == '(' or char[0] == ')':
                del listOfSpecies[ind]
                pass
            ind+=1
            pass
    return listOfSpecies
    
def contactV(density, porosity = None, grainSize = None):
    """
    that function is used to determine volume of water in contact with 1kg soil
    
    """
    if grainSize == None:
        grainSize = 0.1.e-3
        pass
    if porosity == None or porosity == 1.:
        raise Warning("porosity should not be equal to one if considering a mineral phase ")
        
    radius = grainSize / 2.
    volume_of_one_grain = 4.*3.14159*(radius)**3/3.
    volume_of_one_kg_mineral = 1./density
    number_of_grains_in_one_kg = volume_of_one_kg_mineral / volume_of_one_grain
    surface_of_one_grain = 3.* volume_of_one_grain /radius
    if (porosity < 1):
        volume_of_contact_water = volume_of_one_kg_mineral * porosity / (1. - porosity)
        pass
    print(volume_of_contact_water)
    return volume_of_contact_water
    
def contactV1(density, porosity = None):
    """
    that function is used to determine volume of water in contact with 1kg soil
    surface is the surface contact area in contact with 1kg soil
    
    """        
#    radius = 3./density/surface
#    print radius
    
    return (1./density)*porosity/(1.-porosity)

    
def ionNumbering(element):
    """
    ionNumbering: used within the determination of the molar mass
    """
    digital = ""
    ind = 0
    while element[ind].isdigit() or element[ind] ==  ".":
        digital += element[ind]
        if ind+1 == len(element): break
        ind += 1
        pass
    ind = len(digital)
#
    print(" out of ion numbering ",element, ind, digital)
#
    return ind, digital

def saltSpecies(saltSpeciesList,inFile):
    """ cf. the PhreeqC SOLUTION_MASTER_SPECIES keyword, used to define component unknowns
        The word master is taken in the sense of the phreeqC software
    """
    b0 = []
    b1 = []
    b2 = []
    c0 = []
    inFileWriter = inFile.write
    for salt in saltSpeciesList:
        if salt.b0 != None : b0.append([salt.formationElements,salt.b0, salt.description])
        if salt.b1 != None : b1.append([salt.formationElements,salt.b1, salt.description])
        if salt.b2 != None : b2.append([salt.formationElements,salt.b2, salt.description])
        if salt.c0 != None : c0.append([salt.formationElements,salt.c0, salt.description])
        pass
    if b0 != []:
       inFileWriter(" b0\n")
       for couple in b0:
           _b0Writer(inFile,couple[0], couple[1], couple[2])
           pass
       pass
    if b1 != []:
       inFileWriter(" b1\n")
       for couple in b1:
           _b1Writer(inFile,couple[0],couple[1], couple[2])
           pass
       pass
    if b2 != []:
       inFileWriter(" b2\n")
       for couple in b2:
           _b2Writer(inFile,couple[0],couple[1], couple[2])
           pass
       pass
    if c0 != []:
       inFileWriter(" c0\n")
       for couple in c0:
           _c0Writer(inFile,couple[0],couple[1], couple[2])
           pass
       pass
    
#          inFileWriter("%25s %10.5f%10s%10.5f\n"%(string,masterSpecies.alkalinity,masterSpecies.element,masterSpecies.molarMass.getValue()))
    return None

def solutionMasterSpecies(masterSpecies,inFile):
    """ cf. the PhreeqC SOLUTION_MASTER_SPECIES keyword, used to define component unknowns
        The word master matches the phreeqC terminology ( primary iwithin the Yeh article)
    """
    string = masterSpecies.name+"   "+masterSpecies.symbol
    inFileWriter = inFile.write
    if not(masterSpecies.element):
        if not(masterSpecies.molarMass):
            form = "%25s %10.5f\n"
            inFileWriter(form%(string,masterSpecies.alkalinity))
            pass
        else:
            form = "%25s %10.5f%10.5f\n"
            inFileWriter(form%(string,masterSpecies.alkalinity,masterSpecies.molarMass.getValue()))
            pass
        pass
    else:
        if not(masterSpecies.molarMass):
            form = "%25s %10.5f %10s\n"
            inFileWriter(form%(string,masterSpecies.alkalinity,masterSpecies.element))
            pass
        else:
            form = "%25s %10.5f %10s %10.5f\n"
            if masterSpecies.molarMass.getValue()<1:
                masterSpecies.molarMass.convertToUnit("g/mol")
            inFileWriter(form%(string,masterSpecies.alkalinity,masterSpecies.element,masterSpecies.molarMass.getValue()))
            masterSpecies.molarMass.convertToUnit("kg/mol")
            pass
        pass
    return None

def solutionSpecies(spezien,inFile):

    """
    Secondary species reaction treatment
    """
    #raw_input("within solutionSpecies0")
    _formationReaction(0,inFile,spezien.formationReaction,spezien.symbol)
    
    #rraw_input("within solutionSpecies1")
    _gamma(inFile,spezien)
    
    if (spezien.logK != None):
        _logKWriter(inFile,spezien.logK25)
        #print("_logKCoefWriter ",spezien.name)
        _logKCoefWriter(inFile,spezien.logK)
        pass
    else:
        _logKWriter(inFile,spezien.logK25)
        pass
    inFile.write("#\n")
      
def sorbingSiteMaster(exchangeSite,inFile):
    """
    used to define exchange master species sites, see EXCHANGEMASTERSPECIES
    """
    form = "%10s%s\n"
    inFile.write(form%(" ",exchangeSite.name+"   " + exchangeSite.symbol))

def sorbedSpecies(sorbedSpezien,inFile):
    """
    used to define reactions in association with an exchange site
    """
    _reaction(inFile,sorbedSpezien.formationReaction,sorbedSpezien.symbol)
    
    _logKWriter(inFile,sorbedSpezien.logK25)

    inFileWriter = inFile.write

    _gamma(inFile,sorbedSpezien)
        
        
def surfaceSiteMaster(surfaceSite,inFile):
    """
    used to define exchange master species sites, see SURFACEMASTERSPECIES
    """
    form = "%10s%s\n"
    inFile.write(form%(" ",surfaceSite.name+"   " + surfaceSite.symbol))
    
def surfaceSpecies(spezien,inFile):
    """
    used to define reactions in association with a surface site
    """    
    _speciesFormationReaction(inFile,spezien.formationReaction,spezien.symbol)
    _logKWriter(inFile,spezien.logK25)
    return None

    
def mineralSpecies(mineral,inFile):
    """
    used to  treat Precipitation/Dissolution reactions
    """
    _formationReaction(1,inFile,mineral.formationReaction,mineral.symbol)

    if mineral.logK == None:
        _logKWriter(inFile,mineral.logK25)
        pass
    else:
        _logKWriter(inFile,mineral.logK25)
        _logKCoefWriter(inFile,mineral.logK)
        pass

def aqueousSolution(state,iAnf,iEnd,inFile):
    """ 
    used to define each aqueous solution, using
    the SOLUTION keyword.
    
    The default unit for species is mol/l. The default meaning is mol per liter sample. That unit reflects the 
    number of molecules of a substance.
    The molality, sometimesalso called molal concentration is a measure of the concentration of a solute in a solution in terms 
    of amount of a substance in a specified amount of mass of the solvent.
    The molality unit can be used by specifying it explicitely in the state.
    The SI unit for molality is mol/kg; the solvent being here water.
    """
    _keywordWriter(inFile,"SOLUTION",iAnf,iEnd,state.name)
    #inFile.write("#debug line %i %i "%(iAnf,iEnd))
    aqueousSol = state.aqueousSolution
    if aqueousSol.temperature == None:
        form = "   temp %15.10e\n"
        inFile.write(form%(25.0))
        pass
    else:
        form = "   temp %15.10e\n"
        inFile.write(form%(aqueousSol.temperature))
        pass
    if aqueousSol.pH != None:
        if state.charge == None:
            form = "   pH    %15.10e \n"
            inFile.write(form%(aqueousSol.pH))
            pass
        else:
            form = "   pH    %15.10e charge\n"
            inFile.write(form%(aqueousSol.pH))
            pass

    if aqueousSol.pe!=None:
        form = "   pe    %15.10e\n"
        inFile.write(form%(aqueousSol.pe))
        pass
    inFile.write("   units "+aqueousSol.units+"\n")
    
    for spezien in aqueousSol.elementConcentrations:
        #
        # converting to default unit; the conversion doesn't work for mg/l to mol/l as the molar density should be known
        #
        #
        # The default unit is molarity
        #
        spezien.convertToUnit('mol/l')
        form = "%25s    %15.10e\n"
        inFile.write(form%(spezien.symbol,spezien.value))
#
# p. 151 of the phreeqC manual 2.0
#
# Indicates the concentration of this element will be adjusted to achieve charge balance. The element
# must have ionic species. If charge is specified for one element, it may not be specified for
# pH or any other element.
#
    if state.chargeBalance != None:
        #
        # used to equilibrate charge
        #
        form = "%25s    %15.10e charge \n"
        inFile.write(form%(state.chargeBalance[0],float(state.chargeBalance[1])))
        pass
    if state.mineralEquilibrium != None:
        for mineral in state.mineralEquilibrium:
            form = "%25s    %15.10e %25s\n"
            inFile.write(form%(mineral[0],mineral[2],mineral[1]))
            pass
        pass
#
#   Exchange species treatment
#  
    if state.ionicExchanger:
        _keywordWriter(inFile,"EXCHANGE",iAnf,iEnd,state.name)
        form = "               equilibrate   %5i\n"
        inFile.write(form%(iAnf))
        for spezien in state.ionicExchanger.exchangers:
            if spezien.__class__ == ExchangeBindingSpecies:
                form = "%25s    %15.10e\n"
                inFile.write(form%(spezien.symbol,spezien.getExchangeAmount().getValue()))
                pass
            elif spezien.__class__ == ExchangeMineralBindingSpecies:
                form = "%25s%20s equilibrium_phase    %15.10e\n"
                inFile.write(form%(spezien.symbol,spezien.mineral,float(spezien.exchangePerMole)))
                pass
            pass
#
#   Surfaces species treatment
#    
    if state.surfaceComplexation and state.surfaceComplexation.surfaces != []:
        _keywordWriter(inFile,"SURFACE",iAnf,iEnd,state.name)
        form = "               equilibrate with solution %5i\n"
        inFile.write(form%(iAnf))
        for spezien in state.surfaceComplexation.surfaces:
            if spezien.__class__ == SurfaceBindingSpecies:
                if isinstance(spezien.specificAreaPerGram,SpecificAreaPerGram):
                    form = "%25s    %15.10e    %15.10e    %15.10e\n"
                    inFile.write(form%(spezien.name,\
                    spezien.getSites().getValue(),\
                    spezien.getSpecificAreaPerGram().getValue(),\
                    spezien.getMass().getValue()))
                    pass
                else:
                    form = "%25s    %15.10e\n"
                    inFile.write(form%(spezien.name,spezien.getSites().getValue()))
                    pass
                pass

            if spezien.__class__ == SurfaceMineralBindingSpecies:
                form = "%25s%20s  equilibrium_phase  %15.10e    %15.10e\n"
                inFile.write(form%(spezien.symbol,spezien.mineral,\
                float(spezien.getSitesPerMole()),\
                spezien.getSpecificAreaPerMole().getValue()))
                pass
            pass

def mineralSolution (State, batchBeg, batchEnd, inFile, kineticLaws, gasOption, integrationMethod, intParamDict, timeStep, simulationTime):
    """
    To define mineral phases associated to an aqueous phase within a batch cell
    
    """
    boolean = 0
    mineralPhase = State.mineralPhase
    gasPhase = State.gasPhase
    phFixed = State.phFixed
    if gasPhase != [] or mineralPhase != [] or phFixed:
        try:
            if kineticLaws == []:
                if phFixed or gasPhase != []:
                    boolean = 1
                pass
            if mineralPhase != [] and mineralPhase != None:
                for spezien in mineralPhase.minerals:
                    if kineticLaws == []:
                        boolean =1
                        pass
                    else:
                        for kineticLaw in kineticLaws:
                            if (spezien.symbol == kineticLaw.symbol):
                                break
                            else:
                                boolean = 1
                                pass
                            pass
            pass
        except Warning:
            print("##Caution: No mineral phase in contact with the aqueous phase within that solution")
        #
        #
        #
        if (boolean == 1):
            _keywordWriter(inFile,"EQUILIBRIUM_PHASES",batchBeg, batchEnd,State.name)
            try:
                if mineralPhase != [] and mineralPhase != None:
                    for spezien in mineralPhase.minerals:
                        test = 0
                        if kineticLaws != []:
                            for kineticLaw in kineticLaws:
                                #print kineticLaw
                                #raw_input("kinetic law ")
                                if (spezien.symbol == kineticLaw.symbol):
                                    test = 1
                                    break
                                pass
                            pass
                        if (test == 0):
                            saturationIndex = 0.0
                            if spezien.__class__.__name__ in ["MineralTotalConcentration","MineralConcentration"]:
                                saturationIndex = spezien.saturationIndex
                            elif spezien.__class__.__name__ in ["TotalConcentration"]:
                                pass
                            else:
                                raise Exception("the mineral total concentration instanciation has to be checked")
                            if spezien.__class__.__name__ in ["ToDissolveMineralTotalConcentration"]:
                                form = "%25s    %12.7e  %12.7e Dissolve_only\n"
                                inFile.write(form%(spezien.symbol,saturationIndex,spezien.value))
                            else:
                                form = "%25s    %12.7e  %12.7e\n"
                                inFile.write(form%(spezien.symbol,saturationIndex,spezien.value))
            except Warning:
                print("## Caution: No mineral phase found associated to that solution")
        if (boolean == 1) and (State.gasMassBalance.lower() != "ok"):
            try:
                if gasPhase:
                    for spezien in gasPhase.gas:
                        form = "%25s    %10.5e  %10.5e\n"
                        inFile.write(form%(spezien.symbol,spezien.value,spezien.amount))
            except Warning:
                print("# Caution: No gaz phase associated to this solution")     
            if phFixed:
                form = "%25s    %10.5e  %s  %10.5e\n"
                inFile.write(form%("Fix_H+",-1.0*State.aqueousSolution.pH,\
                phFixed[0],phFixed[1]))
                pass
            pass
        elif (boolean == 0) and (State.gasMassBalance.lower() != "ok"):
            #
            # in that case the only phase is a gas phase
            #
            _keywordWriter(inFile,"EQUILIBRIUM_PHASES",batchBeg, batchEnd,State.name)
            try:
                if gasPhase:
                    for spezien in gasPhase.gas:
                        print("gasPhase.symbol ",spezien.symbol)
                        form = "%25s    %10.5e  %10.5e\n"
                        inFile.write(form%(spezien.symbol,spezien.value,spezien.amount))
                        pass
                    pass
            except Warning:
                print(" Caution: The solution does\'nt entail any gas phase")
            if phFixed != None:
                form = "%25s    %10.5e  %s  %10.5e\n"
                inFile.write(form%("Fix_H+",-1.0*State.aqueousSolution.pH,\
                phFixed[0],phFixed[1]))
                pass
            pass
        elif (State.gasMassBalance.lower() == "ok"):
            #
            # in that case the only phase is a gas phase
            #
            #_keywordWriter(inFile,"GAS_PHASE",batchBeg, batchEnd,State.name)
            gasSolution(State, batchBeg, batchEnd, inFile)
            pass
    #
    # Considering kinetic laws
    #
    kineticBoolean = 1
    incremental = 1
    if kineticLaws != [] and mineralPhase not in [None,[]]:
        try: 
#            print mineralPhase, dir(mineralPhase)
#            print type(mineralPhase)
            #raw_input("mineral phase ")
            for spezien in mineralPhase.minerals:
                for kineticLaw in kineticLaws:
                    if isInstance(kineticLaw,ReversibleKineticLaw):
                        if (spezien.symbol == kineticLaw.symbol):
                            if kineticBoolean == 1 :
                                _keywordWriter(inFile,"KINETICS", batchBeg, batchEnd," ")
                                kineticBoolean = 0
                                pass
                            p2Boolean = _exponentControl(kineticLaw.sphereModelExponent)
                            form = "    %s\n"
                            inFile.write(form%(spezien.symbol))        
                            form = "    -m %15.10e %15.10e\n"
                            inFile.write(form%(spezien.value,spezien.saturationIndex)) 
                            form = "    -m0 %15.10e\n"
                            inFile.write(form%(spezien.value))
                            if p2Boolean == 1:
                                form = "    -parms %15.10e %15.10e %15.10e %15.10e\n"
                                inFile.write(form%( kineticLaw.specificSurfaceArea,         # surface area        
                                        kineticLaw.sphereModelExponent,                     # sphere model exponent
                                        kineticLaw.rate.value,                              # k
                                        kineticLaw.SRExponent))                             # saturation ratio exponent
                                pass
                            else:
                                form = "    -parms %15.10e %15.10e\n"
                                inFile.write(form%( \
                                     kineticLaw.specificSurfaceArea * kineticLaw.rate.value,# surface area * kinetic rate       
                                     kineticLaw.SRExponent))                                # saturation ratio exponent
                                pass
                
#
                            if integrationMethod[0] == "cvode":
                                cvodewriter(inFile, kineticLaw, integrationMethod, intParamDict)
                                kineticBoolean = -1
                                pass

                    elif isInstance(kineticLaw,WYMEKineticLaw):
                        if (spezien.symbol == kineticLaw.name):
                            if batchBeg == batchEnd and kineticBoolean == 1:
                                _keywordWriter(inFile,"KINETICS", batchBeg, batchBeg," ")
                                kineticBoolean = 0
                                pass
                            elif kineticBoolean == 1 :
                                _keywordWriter(inFile,"KINETICS",batchBeg, batchEnd," ")
                                kineticBoolean = 0
                                pass
                            form = "    %25s\n"
                            inFile.write(form%(kineticLaw.name))
                            form = "  -m %15.10e         # moles of %s\n"
                            inFile.write(form%(spezien.value,kineticLaw.name)) 
                            if (kineticLaw.rate.unit == "mol/m2/s") or (kineticLaw.rate.unit == ""):
                                parm1 = kineticLaw.rate.value
                                pass
                            form = "    -parms %15.10e %15.10e\n"
                            inFile.write(form%(parm1,kineticLaw.surface.value ))        
                            form = "    -formula %s\n"
                            inFile.write(form%(kineticLaw.symbol))        
                            inFile.write("  -cvode true\n")        
                            inFile.write("  -tol 1.e-7\n")        
                            inFile.write("  -cvode_order 5\n")    
                            inFile.write("  -cvode_steps 400\n")        
                    elif isInstance(kineticLaw,FreeKineticLaw):
                        if (spezien.symbol == kineticLaw.symbol):
                            if kineticBoolean == 1 :
                                _keywordWriter(inFile,"KINETICS", batchBeg, batchEnd," ")
                                kineticBoolean = 0
                                pass
                            form = "    %s\n"
                            inFile.write(form%(spezien.symbol))
                            length = len(kineticLaw.lawParameter)
                            form = "    -parms"
                            for fl in kineticLaw.lawParameter:
                                form += " %15.10e"%fl
                                pass
                            inFile.write("%s\n"%(form))
                            if kineticLaw.m0 != None:
                                form = "    -m0 %15.10e                 # mol/L\n"
                                inFile.write(form%(kineticLaw.m0))
                                pass
                            if spezien.value != None:
                                form = "    -m0 %15.10e                 # mol/L\n"
                                inFile.write(form%(spezien.value))
                                pass
                            kineticLaw.imp = 1
                            pass
                    
            if kineticBoolean ==0:
                if integrationMethod[0] == "cvode":
                    cvodewriter(inFile, kineticLaw, integrationMethod, intParamDict)
                    pass
                if incremental == 1:
                    inFile.write("    INCREMENTAL_REACTIONS true\n")
                    incremental = 0
                    pass
                pass
            pass
        
        except Warning:
            print("## Caution: No kinetic law within the "+State.name+" state ")
                                                                                #
                                                                                # we don't want to use a FreeKineticLaw here
                                                                                #
#    if (kineticLaws != []) and (isInstance(kineticLaw,FreeKineticLaw) == False):
    elif (kineticLaws != []):
        nokinetic = 1
        for kineticLaw in kineticLaws:
            if isInstance(kineticLaw,FreeKineticLaw):
                if kineticLaw.m0 != None:
                    nokinetic = 0
                    pass
                pass
            pass
        if batchBeg == batchEnd and kineticBoolean == 1 and nokinetic == 0:
            _keywordWriter(inFile,"KINETICS", batchBeg, batchBeg,"")
            kineticBoolean = 0
            pass
        elif kineticBoolean == 1 and nokinetic == 0:
            _keywordWriter(inFile,"KINETICS",batchBeg, batchEnd,"")
            kineticBoolean = 0
            pass
        if nokinetic == 0:
            for kineticLaw in kineticLaws:
            #raw_input(" free kinetic law 1")
                if isInstance(kineticLaw,FreeKineticLaw):
                #raw_input(" free kinetic law 2")
                    if (kineticLaw.imp == 0):
                    #raw_input(" free kinetic law 3")
                    #_keywordWriter(inFile,"KINETICS", batchBeg, batchEnd,"")
                        form = "    %s\n"
                        inFile.write(form%(kineticLaw.symbol))
                        if kineticLaw.formula != None:
                            form = "    -formula %s\n"
                            inFile.write(form%(kineticLaw.formula))
                            pass
                        length = len(kineticLaw.lawParameter)
                        form = "    -parms"
                        for fl in kineticLaw.lawParameter:
                            form += " %15.10e"%fl
                            pass
                        inFile.write("%s\n"%(form))
                        form = "    -m0 %15.10e\n"
                        inFile.write(form%(kineticLaw.m0))
#
                        if integrationMethod[0] == "cvode":
                            cvodewriter(inFile, kineticLaw, integrationMethod, intParamDict)
                            pass
                    else:
                        kineticLaw.imp = 0
                        pass
                    pass
                #
                # The time step is by construction the same for all kinetics
                #
                if simulationTime != None and timeStep != None:
                    form = "    -steps %i in %i # time in s\n"
                    inFile.write(form%(int(simulationTime),int(simulationTime/timeStep)))
                    pass
            
        if kineticBoolean == 0 and incremental == 1: inFile.write("    INCREMENTAL_REACTIONS true\n\n")
    elif mineralPhase != None:
        print("## Caution: No kinetic law within the "+State.name+" state ")
        pass
        
def solidSolution(solidSol,iAnf,iEnd,inFile, name = None):
    """ 
    We treat solid solutions here, the solidSolution is of type solidsolution. See the chemical.py module
    
    example of the phreeqC SOLID SOLUTIONS keyword, cf. the manual page 144:
    
     SOLID SOLUTIONS 1 Two solid solutions
        CaSrBaSO4 # greater than 2 components, ideal
            -comp   Anhydrite   1.500
            -comp   Celestite   0.05
            -comp   Barite      0.05
            
         SOLID_SOLUTION            1-1 Solid Solution of Strontianite and Aragonite
                Ca(x)Sr(1-x)CO3     # binary, nonideal
                    -comp                 Aragonite             0.0E+00
                    -comp              Strontianite             0.0E+00
                    -temp              2.5E+01
                    -Gugg_nondim         0.0E+00         0.0E+00
    """
    if name == None: name = ""
    if type(iAnf) != IntType:
        raise TypeError(" the first indices must be an integer ")
    if iEnd == None:
        _keywordWriter(inFile,"SOLID_SOLUTION",iAnf,iAnf,name)
        pass
    else:
        if iAnf < iEnd:
            _keywordWriter(inFile,"SOLID_SOLUTION",iAnf,iEnd,name)
            pass
        else:
            Warning(" verify the parameters bound of the SOLID SOLUTION keyword")
            _keywordWriter(inFile,"SOLID_SOLUTION",iEnd,iAnf,name)
            pass
        pass 
#
# Solid solution name treatment
#
    form = "%20s        #ideal\n"
    inFile.write(form%(solidSol.name))
#
# Pure phase components within solid solution
#
    for purephase in solidSol.mineralAmounts:
        form = "%20s%25s    %15.10e\n"
        inFile.write(form%("-comp ",purephase.symbol,float(purephase.value)))
        pass
#
# Solid solution temperature
#
    if solidSol.temperature != None:
        form = "   %16s %15.10e\n"
        inFile.write(form%("-temp    ",solidSol.temperature))
        pass
    else:
        form = "  %16s %15.10e\n"
        inFile.write(form%("-temp    ",25.0))
        pass
    if solidSol.gugg != None:
        form = "   %23s %15.10e %15.10e\n"
        inFile.write(form%("-Gugg_nondim",solidSol.gugg[0],solidSol.gugg[1]))
        pass

    return None

def gasSolution(chemicalState,iAnf,iEnd,inFile):
    """ 
        keyword GAS_PHASE, See the module chemistry.py
        
        Warning: A GAS_PHASE data block is not needed if fixed partial pressures of gas components are desired; use EQUILIBRIUM_PHASES instead.
        
        A fixed-volume gas phase always contains some amount of each gas component that is present in solution. 
        The initial composition of a fixed-pressure gas phase is defined by the partial pressures of each gas component. We have to set the pressure, otherwise
        that one will be fixed to the atmospheric pressure in atm. 1 bar = 100 000 Pa, 1 atmosphere being equal to 101325 Pa.
        By default, the pressure is of one atm. A pressure being given, the unit is supposed to be in atm.; but if the unit is gevin; the transformation is
        to atm is automatic.
        A volume or a pressure can be given. By default, a pressure of 1 atm is given.
        The initial composition of a fixed-volume gas may be defined by the partial pressures of each gas component or may be defined to be that which is in 
        equilibrium with a fixed-composition aqueous phase.
    
        The temperature along with volume and partial pressure are used
        to calculate the initial moles of each gas component in the fixed-pressure gas phase.
    
        example of the phreeqC input file issued from the manual, see p.91 (Manual V1999):
    
        GAS_PHASE 1-5 Air
             -fixed_pressure
             -pressure       1.0
             -volume         1.0
             -temperature    25.0
             
             CH4(g)          0.0
             CO2(g)          0.000316
             O2 (g)          0.2
             N2 (g)          0.78
    """
    _keywordWriter(inFile,"GAS_PHASE",iAnf,iEnd,chemicalState.name)
#
#   a lot of things to say:
#
#       fixed pressure / fixed volume
#
#       For the moment we use a fixed pressure option, the Richards formulation implies a fixed pressure of 1. atmosphere 
#
    solutionGasPhase = chemicalState.gasPhase
    print("degug ",solutionGasPhase.__class__.__name__)
    #print("degug ",solutionGasPhase.fixedpressure)
    #print("degug ",solutionGasPhase.pressure)
    if solutionGasPhase.pressure == None and solutionGasPhase.fixedpressure:
        inFile.write("        -fixed_pressure\n"\
                     "        -pressure 1.0 # the pressure is set to the atmospheric pressure\n"\
                     "        #-volume 1.0   # the volume is reaffected within the algorithm; warning\n")
        if solutionGasPhase.volume != None:
            inFile.write("        -volume %e # the volume is set in l.\n"%(solutionGasPhase.volume))
    elif solutionGasPhase.fixedpressure:
        inFile.write("        -fixed_pressure\n"\
                     "        -pressure %e # the pressure is set in atm. 1 atm being equal to 1e+5 Pa (1 bar)\n"%(solutionGasPhase.pressure))
        if solutionGasPhase.volume != None:
            inFile.write("        -volume %e # the volume is set in l.\n"%(solutionGasPhase.volume))
            pass
        pass
    else:
        inFile.write("        -fixed_volume\n"\
                     "        -volume %e # the volume is set in l.\n"\
                     "        #-volume 1.0   # the volume is reaffected within the algorithm; warning\n"%(solutionGasPhase.volume))
        if solutionGasPhase.pressure != None:
            inFile.write("        -pressure %e # the volume is set in l.\n"%(solutionGasPhase.pressure))
            pass
        pass
        
        
#
# Gas solution temperature, default is 25 celcius degree
#
    if chemicalState.aqueousSolution.temperature != None:
        form = "        -temperature    %15.10e\n"
        inFile.write(form%(chemicalState.aqueousSolution.temperature))
        pass
    else:
        form = "        -temperature    %15.10e\n"
        inFile.write(form%(25.0))
        pass
#
# Gas phase primary species
#
    ind = 0
    for gas in chemicalState.gasPhase.gas:
        if ind != 0:
            form = "%25s    %10.5e\n"
            pass
        else:
            form = "%25s    %10.5e              # gas name  ( included in PHASES), and partial pressure(s)\n"
            pass
        inFile.write(form%(gas.symbol,gas.value))
        ind+=1
    return None
    
class Phreeqc:        
    """
    Phreeqc class used to enable driving of the tool, mainly, interaction between chemistry and transport  within
    the coupling algorithm. Parallelism is also covered.
    """
    def __init__(self, numberOfProcessors = None, rank = None):
        """
        geochemical solver
        """
        self.cellPorosity = None
        self.cellsNumber = 0
        self.chemicalParameters = []
        self.comment = ""
        self.initialPorosity = None
        self.inFile = None
        self.kineticLaws = []
        self.porosityOption = None
        if (numberOfProcessors!=None):
            self.mpiSize  = numberOfProcessors
            from WPhreeqc_mpi import *
            self.solver = WPhreeqc_mpi()
            self.solverFileName = "phreeqCFile"+str(rank)
            pass
        else:
            self.numberOfProcessors = 1
            self.mpiSize = 1
            from WPhreeqc import *
            self.solver = WPhreeqc()
            self.solverFileName = "phreeqCFile"
            pass
        self.speciesBaseAddenda = []
#       self.solverFileName = "phreeqCFile"
        self.temperature = 0
        #
        #   gasOption:  two ways to treat a gas
        #       
        #       - using the GAS_PHASE treatment otherwise gasOPtion is let to None then the gas is treated 
        #               through the equilibrium_phase keyword 
        #   - None: the gas is treated through the equilibrium_phase 
        #
        self.gasOption = None
        self.thermalOption = None
        self.mMolarMassList = []
        self.mVolumicMassList = []
        self.problemDensityList = []
        self.problemMineralList = []
        self.basicLineId = 1
        self.intParamDict = None
        self.timeStep = None
        self.simulationTime = None
        self.batch = None
#
# For a sequential process, mpiSize is <=1, otherwise for //ism, mpiSize is greater than one.
#   
#   self.mpiSize = 1
#
# confer to phreeqc reference manual 99-4259
#       
        self.solverqcKeywords = ['NAMED_EXPRESSIONS',\
                'LLNL_AQUEOUS_MODEL_PARAMETERS',\
                # p 79
                'EQUILIBRIUM_PHASES',\
                # p 82
                'EXCHANGE',\
                # p 87
                'EXCHANGE_MASTER_SPECIES',\
                # p 88
                'EXCHANGE_SPECIES',\
                # p 91
                'GAS_PHASE',\
                # p 106
                'KINETICS',\
                # p 111
                'KNOBS',\
                # p 118
                'PHASES',\
                # p 124
                'RATES',\
                # p 154
                'SOLUTION_MASTER_SPECIES',\
                # p 156
                'SOLUTION_SPECIES',\
                # p 169
                'SURFACE_MASTER_SPECIES',\
                # p 170
                'SURFACE_SPECIES']
        self.integrationMethod = ["cvode",3,4.e-7,250]                  # cvode cvodeOrder cvodeTol cvodeStep
        pass

    def getHelp(self):
        print(self.__doc__)
        pass
        
    def init(self,inFile, output, StatesBounds,  trace, internalNodes, \
             chemicalParameters=None, porosityOption=None, thermalOption = None):
        """ 
        Used to define the input files and write the data file
        """
    
        if chemicalParameters!=None:
            self.chemicalParameters = chemicalParameters
            pass

        self.internalNodesNumber = internalNodes
        self.activeCellsNumber = internalNodes
        self.cellPorosity = [1.0]*self.internalNodesNumber
        print ("dbp phreeqc at init level: ", StatesBounds)
        print ("dbp phreeqc at init level: ", StatesBounds.keys())
        if StatesBounds != {} : 
            self.inFile = open(self.solverFileName,'w')
            self.dataSetup(StatesBounds)
            pass
        else:
            print("="*20+"\n Warning : No state bound defined: eventually check your case file"+"="*20)
            print("self.solverFileName",self.solverFileName)
            pass
        #print " pdbg init ",self.solverFileName,output
        self.defineInputOutput(self.solverFileName,output)
                                                                                            #
                                                                                            # We launch the solver
                                                                                            #
        self.solver.initialize(internalNodes,self.mpiSize)
        self.molarMassDict = self.getMolarMassList("phreeqc.dat",typ = {})
        #
        # porosity treatment: structure creation to treat the porosity variation
        #
        if self.porosityOption:
            #print self.mMolarVolumeList,len(self.problemMineralList)
            #raw_input("molar volume list ")
            self.solver.porosityInitialisation(self.problemMineralList,self.mMolarVolumeList,len(self.problemMineralList))
            pass
        return self.equilibrate("global")
        
    def setGasOption(self,gasOption = None):
        """ 
         Used to treat a gas phase through the GAS_PHASE keyword or in a standard way
        """
        if gasOption != None:
            self.gasOption = gasOption
            pass
        return None
        
    def setInternalCellsBeforeLaunching(self,intCellsBeforeLaunching):
        self.intCellsBeforeLaunching = intCellsBeforeLaunching
        return
    
    def getInternalCellsBeforeLaunching(self):
        return self.intCellsBeforeLaunching 
    
    def getPorosity(self, ind = None):
        """
        Used to get the porosity field
        from the chemistry and the fm0 for aqueousstateset
    
        """
        if ind == None:
            ind = 0
            pass
        epsilon = 1. + epsFP

        cellPorosity0 = self.solver.getPorosity()
        while epsilon > epsFP:
            ind+=1

            self.cellPorosity = self.solver.getPorosity()
            for cell in range(len(cellPorosity0)):
                epsilon += abs(cellPorosity0[cell] - self.cellPorosity[cell])
                pass
            epsilon/=len(cellPorosity0) 

            self.cellPorosity0 = self.cellPorosity
            self.solver.reactions(1, "internal")
#           print " pdbg getPorosity"
            self.cellPorosity = self.solver.getPorosity()
            pass
        self.solver.reactions(1, "internal")
        return self.cellPorosity

    def kinetics(self,kineticLaw):
        """ 
        Used to define user defined kinetic laws
        See the manual, version 2, page 41 NUMERICAL METHOD AND RATE EXPRESSIONS FOR CHEMICAL KINETICS
        See also page 121 of the manual, version 2.
                
        ReversibleKineticLaw,
        FreeKineticLaw
        """
        if isInstance(kineticLaw,ReversibleKineticLaw): # Reversible Kinetic law
            mineralFormula = kineticLaw.symbol
            p2Boolean = _exponentControl(kineticLaw.sphereModelExponent)
            p4Boolean = _exponentControl(kineticLaw.SRExponent)
            
            self.inFile.write("     %s\n"%(mineralFormula))
            self.inFile.write(" #   M : currrent amount of moles\n")
            self.inFile.write(" #   M0 : initial amount of moles for %s\n"%(mineralFormula))
            self.inFile.write(" #   PARM(1), PARM(2), PARM(3) and PARM(4) are law parameters,\n")
            self.inFile.write(" #   they are introduced with the KINETICS keyword, through -parms\n")
            self.inFile.write(" #   A0 : initial surface of %s in contact\n"%(mineralFormula))
            self.inFile.write(" #   V  : solution volume in contact with A0\n")
            if p2Boolean == 1:                                                          # the exponent is !=0 and !=1
                self.inFile.write(" #   PARM(1) : A/V, m2/l\n")
                self.inFile.write(" #   PARM(2) : M/M0 exponent (-) to account for changes in reactive surface sites\n")
                self.inFile.write(" #   PARM(3) : kinetic rate (mol/m2/s)\n")
                self.inFile.write(" #   PARM(4) : exponent for SR\n")
                pass
            else:
                self.inFile.write(" #   PARM(1) : A/V, m2/l multiplied by the kinetic rate (mol/m2/s)\n")
                self.inFile.write(" #   PARM(2) : exponent for SR\n")
                pass
            self.inFile.write("\n-start\n")
            #self.inFile.write("     5  if (m <= 0) then goto 81\n")
            #self.inFile.write(" #  20  sr_sh = SR(\"%s\")\n"%(mineralFormula))
            # 
            # sr : saturation ratio : IAP/K
            #
            sr_sh = "SR(\"%s\")"%(mineralFormula)
            #self.inFile.write("    20  if (M<= 0 and si_sh < 0) then goto 90\n")
            #
            m0_ctrl = 0.
            ind_ctrl = 0
            print (color.bold+" type of self.chemicalStateList type: "+color.end,type(self.chemicalStateList))
            print (color.bold+" length of self.chemicalStateList: "+color.end,len(self.chemicalStateList))
            print (color.bold+" self.chemicalStateList: "+color.end,self.chemicalStateList)
            print (color.bold+" self.chemicalStateList: [0]"+color.end,self.chemicalStateList[0])
            indCont = 0
            for state in self.chemicalStateList:
                print("state.mineralPhase: ",state.name)
                #print("state.mineralPhase: ",state.mineralPhase)
                if state.mineralPhase == [] or state.mineralPhase == None:
                    break
                for spezien in state.mineralPhase.minerals:
                    if (spezien.symbol == kineticLaw.symbol):
                        m0_ctrl = spezien.value
                        ind_ctrl = 1
                        if (ind_ctrl == 1):
                            if m0_ctrl>0:
                                self.inFile.write(" 40  t = M/M0\n")
                                self.inFile.write(" 50  if t = 0 then t = 1.\n")
                                pass
                            pass
                        else:
                            self.inFile.write("  30 t = 1.\n")
                            self.inFile.write("  40 if M0 > 0 then t = M/M0\n")
                            self.inFile.write("  50 if t = 0 then t = 1.\n")
                            pass
                        if p2Boolean == 1:                                                  # the exponent is !=0 and !=1
                            area = "PARM(1)*(t)^PARM(2)"
                            pass
                        elif p2Boolean == 0:                                                # the exponent is 1
                            area = "PARM(1)*t"
                            pass
                        else:                                                               # the surface is constant
                            area = "PARM(1)"
                            pass
                        #
                        # to avoid the product parm1*parm3, we should integrate in parm1 the product PARM(1)*PARM(3) 
                        #
                        if p4Boolean == 1:                                                  # the exponent is !=0 and !=1
                            self.inFile.write(" 80  moles = %s*PARM(3)*(1.-sr_sh^PARM(4))*time\n"%(area))
                            pass
                        elif p4Boolean == 0:                                                # the exponent is 1
                            self.inFile.write(" 80  moles = %s*(1.-%s)*time\n"%(area,sr_sh))
                            pass
                        else:                                                               # 
                            self.inFile.write(" 80  moles = %s*time\n"%(area))
                            pass
            
                        self.inFile.write(" 81  SAVE moles\n")
                        self.inFile.write("-end \n")
                        pass
                    elif isInstance(kineticLaw,WYMEKineticLaw): # WYME Kinetic law
                        spezien = kineticLaw.name
                        self.basicLineId = 1
                        self.inFile.write("\n%25s\n\n"%(spezien))
                        self.basicLineId+=1
                        self.inFile.write("\n-start\n")
                        self.inFile.write(" %s  rem M : current amount of moles\n"%(self.basicLineId))
                        self.basicLineId+=1
                        self.inFile.write(" %s  rem M0 : initial amount of moles for %s\n"%(self.basicLineId,spezien))
                        self.basicLineId+=1
                        self.inFile.write(" %s  rem PARM(1), PARM(2) represent a surface reaction and a kinetic rate\n"%(self.basicLineId))
                        self.basicLineId+=1
                        self.inFile.write(" %s  rem factor A0 and k0 of the law\n"%(self.basicLineId))
                        self.basicLineId+=1
                        self.inFile.write(" %s  ratew = 1.\n"%(self.basicLineId))
                        self.basicLineId+=1
                        self.inFile.write(" %s  ratey = 1.\n"%(self.basicLineId))
                        self.basicLineId+=1
                        self.inFile.write(" %s  ratem = 1.\n"%(self.basicLineId))
                        self.basicLineId+=1
                        self.inFile.write(" %s  ratee = 1.\n"%(self.basicLineId))
                        #
                        # W term 
                        #
                        ratew = "1"
                        if kineticLaw.WTerm != None:
                            ratew = ""
                            for IonenListe in [kineticLaw.WTerm]:
                                for ion in IonenListe:
                                    ratew += "ACT(\""+ion.symbol+"\")^"+ion.power.__str__()+"*"
                                    self.basicLineId += 1
                            self.inFile.write(" %s  ratew = %s\n"%(self.basicLineId,ratew[:-1]))
                        #
                        # Y term 
                        #
                        self.basicLineId +=10
                        ratey = "1"
                        if kineticLaw.YTerm != None:
                            rate_y = ""
                            for Mineralien in kineticLaw.YTerm:
                                power1 = Mineralien.power1.__str__()
                                power2 = Mineralien.power2.__str__()
                                symbol = Mineralien.symbol

                                self.basicLineId+=10
                                aux = "SR(\""+Mineralien.symbol+"\")"
                                if abs(Mineralien.power1-1.0)>1.e-20:
                                    aux = "("+aux+")^"+power1
                                    pass
                                else:
                                    aux = "("+aux+")"
                                    pass
                                self.basicLineId+=10
                                auy = "aux ="+aux
                                self.basicLineId+=10
                                self.inFile.write("   %s   %s\n"%(self.basicLineId,auy))
                  
                                if Mineralien.type == 'polynomial':
                                    if kineticLaw.rate.value < 0 and kineticLaw.lawType == None :
                                        auy = "aux = 1.-aux"
                                        self.basicLineId+=10
                                        self.inFile.write("   %s   %s\n"%(self.basicLineId,auy))
                                    if abs(Mineralien.power2-1.0)>1.e-20:
                                        rate_y = "(aux)^"+power2
                                        pass
                                    else:
                                        rate_y = "aux"
                                        pass
                                elif kineticLaw.rate.value > 0 and kineticLaw.lawType == None:
                                    auy = "aux = 1.-aux"
                                    self.basicLineId+=10
                                    self.inFile.write("   %s   %s\n"%(self.basicLineId,auy))
                                    auy = "if aux<0 then aux = 0"
                                    self.basicLineId+=10
                                    self.inFile.write("   %s   %s\n"%(self.basicLineId,auy))
                                    if abs(Mineralien.power2-1.0)>1.e-20:
                                        rate_y = "(aux)^"+power2
                                        pass
                                    else:  
                                        rate_y = "aux"
                                        pass
                                elif kineticLaw.lawType == "reversible":
                                    auy = "aux = 1.-aux"
                                    self.basicLineId+=10
                                    self.inFile.write("   %s   %s\n"%(self.basicLineId,auy))
                                if abs(Mineralien.power2-1.0)>1.e-20:
                                    rate_y = "(aux)^"+power2
                                    pass
                                else:  
                                    rate_y = "aux"
                                    pass

#                        else:
#                            aux = "LOG10("+aux+")"
#                            pass
#                        if x.rate.value < 0:
#                            if abs(Mineralien.power2-1.0)>1.e-20:
#                                rate_y = "(aux)^"+power2
#                                pass
#                            else:
#                                rate_y = "aux"
#                                pass
#                        else:
#                            if abs(Mineralien.power2-1.0)>1.e-20:
#                                rate_y = "(aux)^"+power2
#                                pass
#                            else:  
#                                rate_y = "aux"
#                                pass
#
#                        self.basicLineId+=10
#                        self.inFile.write("  %s   ratey = %s\n"%(self.basicLineId,rate_y))
#                        self.basicLineId+=10
#                        self.basicLineId+=10               
                        #
                        # M term 
                        #
                        if kineticLaw.MTerm != None:
                            for Spezien in kineticLaw.YTerm:
                                nenner = spezien.halfSat+"^"+spezien.power1+"MOL(\""+spezien.symbol+"\")^"+spezien.power1
                                rate_mi+= "(MOL(\""+spezien.symbol+"\")"+")/"+nenner+")^"+str(power2)
                                self.inFile.write(" %s  ratem = ratem*%s\n"%(self.basicLineId,rate_mi))
                                pass
                            pass
                        #
                        # E term 
                        #
                        if kineticLaw.ETerm != None:
                            ratee = ""
                            for Mineralien in kineticLaw.ETerm:
                                aux = "SR(\""+Mineralien.symbol+"\")"
                                self.basicLineId+=10
                                ratee+= "(1.- (1.- (SI(\""+Mineralien.symbol+"\"))^"+str(Mineralien.power1)+"))^"+str(Mineralien.power2)
                                self.basicLineId+=10
                                self.inFile.write("    %s   ratee = %s\n"%(self.basicLineId,ratee))
                                pass
                            pass

            self.basicLineId+=10
            #self.inFile.write("    %s  print ratey\n"%(self.basicLineId))
            self.basicLineId+=10
        
            #npx auxx = "(1.- (SR(\""+Mineralien.symbol+"\")))"
            #name = "\""+Mineralien.symbol+"\""
            #self.inFile.write("    %s  aux = %s\n"%(self.basicLineId,auxx))
            #self.basicLineId+=10
            #name = "\""+Mineralien.symbol+"\""
            #self.inFile.write("    %s  name = %s\n"%(self.basicLineId,name))
            self.basicLineId+=10

            self.basicLineId+=10
            if isInstance(kineticLaw,WYMEKineticLaw):
                self.inFile.write(" %s  rate = .001*parm(1)*parm(2)*ratew*ratey*ratem*ratee\n"%(self.basicLineId))
            else:
                self.inFile.write(" %s  rate = .001*parm(1)*parm(2)\n"%(self.basicLineId))
            self.basicLineId+=10
            #self.inFile.write("    %s  moles = ((m/m0)^0.666)*rate*time\n"%(self.basicLineId))
            self.inFile.write(" %s  moles = rate*time\n"%(self.basicLineId))
#            self.basicLineId+=10
#            self.inFile.write("    %s  if abs(moles) < 1.e-15 then moles = 0.\n"%(self.basicLineId))
            self.basicLineId+=10
        #aux = "if -moles > TOT(\""+spezien+"\") then moles = -tot(\""+spezien+"\""
        #aux = "if -moles > M then moles = -M"
        #aux = "if (moles > M) then moles = M"
        #aux = "if M+moles < 0 then moles = M"
            #self.inFile.write("    %s     %s\n"%(self.basicLineId,aux))
            self.basicLineId+=10
            self.inFile.write(" %s  SAVE moles\n"%(self.basicLineId))
            self.inFile.write("-end\n")
            pass
        elif isInstance(kineticLaw,FreeKineticLaw): # Reversible Kinetic law
            if kineticLaw.rate != None:
                #self.inFile.write("%s"%("\nRATES\n\n"))
                kineticLaw.rate = kineticLaw.rate.replace("RATES","")
                kineticLaw.rate = kineticLaw.rate.replace("-end","")
                if kineticLaw.description != None:
                    self.inFile.write("# %s\n"%(kineticLaw.description))
                self.inFile.write("%s"%(kineticLaw.rate))
                self.inFile.write("%s"%("\n-end\n"))
                self.inFile.write("%s"%("\n#~~~~~~~~~~~~\n# end of the rate for "+kineticLaw.symbol+"\n#~~~~~~~~~~~~\n"))
        else:   
            raise Exception("Wrong definition of the kinetic law type")
        return None

    def getCellPorosity(self, cell, ite):
        """
        porosity estimation within a cell
        """
        if ite == 0:
            cellPorosity = self.cellPorosity[cell]
            newCellPorosity = self.solver.getCellPorosity(cell,0)
#           print cell,cellPorosity,newCellPorosity
            epsP = abs(1.0-newCellPorosity/cellPorosity)
            ind = 0
#
# ind <2 to be considered as optimal.
#
            while epsP > epsFP and ind<2:
                self.solver.einzelequilibrium(cell)
                cellPorosity = newCellPorosity
                newCellPorosity = self.solver.getCellPorosity(cell,2)
                epsP = abs(1. - newCellPorosity/cellPorosity)
                ind+=1
                pass
            self.cellPorosity[cell] = newCellPorosity
            pass
        else:
            self.cellPorosity[cell] = self.solver.getCellPorosity(cell,1)
            pass
#   if cell < 5:
#       print " ph.py within getCellPorosity %d ite %d %e"%(cell,ite,self.cellPorosity[cell])
        return None
##
    def modifyKineticLaws(self,kineticLaws,index=None):
        """
        This function is used to modify dynamically the properties of a kineticLaw.
        for the moment, it can't be modified to work on cells and it allows only to modify WYME laws.
        \param kineticLaws (List of KineticLaw or A KineticLaw) the Kinetic Law(s)
        to be modified
        \param [index] (list of integer) List of the cells concerned by this modfification
        """
        for kineticLaw in kineticLaws:
            name = kineticLaw.getName()
            if (name and name in self.dictKineticLaws):
                if isInstance(kineticLaw,ReversibleKineticLaw):
                    mess = "only wyme laws can be modified for the moment"                    
                    raise mess
                elif isInstance(kineticLaw,WYMEKineticLaw):
                    kin =  self.defineWYMEKineticLaw(kineticLaw,self.dictKineticLaws[name])
                    if index:
                        return None
                    else:
                        if (kineticLaw.rate.unit == "mol/m2/s") or (kineticLaw.rate.unit==""):
                            parm1 = kineticLaw.rate.value
                            pass
                        self.solver.changeKinetics(kineticLaw.name,parm1,kineticLaw.surface.value)
                        pass
                    pass
                else:
                    raise TypeError("the type of kinetic law is not supported for the moment")
                pass
            else:
                mess = "No name specified for this Kinetic Law or not existant Kinetic \
                law defined with this name. So, impossible  to modified it"
                raise mess

        return 
    
    def getPorosityField(self,ite = None):
        #print "pdbg getPorosityfield "
        if (ite == None):
            ite = 1
            pass
        print(" within phreeqc get porosity field ")
        for node in range(self.internalNodesNumber):
            self.getCellPorosity(node,ite)
            #print "pdbg getPorosityfield ",node ,ite
            pass
        return self.cellPorosity
    
    def getMolarMassList(self,URL, typ = None):
        """
        can only take place un the soft module; a database analysis being mandatory.
        """
        print(" url getMolar: %s"%(URL))
        URL = URL.split("/")
        print(" url getMolar1: %s"%(URL))
        URL = os.getenv("WRAPPER")+"/Phreeqc_dat/"+URL[-1]
        print(" url getMolar2: %s"%(URL))
        try:
            print (" try url to be opened: %s"%(URL))
            URL = _fileIdentify(URL)
            print (" try url to be opened: %s"%(URL))
            dataBaseFile = open (URL, 'r')
            print (" try opened: %s"%(URL))
        except:
            raise Warning("")
                  
        if typ == DictType or type(typ) == DictType:
            molarMassDict = {}
            pass
        else:
            molarMassDict = None
            dbbPrimarysList = []
            dbbPrimarysMolarMassList = []
            pass
        line = dataBaseFile.readline()
        while not line.startswith("SOLUTION_MASTER_SPECIES"):
            line = dataBaseFile.readline()
            pass
        non_whitespace=recompile('\S+')
        line=dataBaseFile.readline()
        while not line.startswith("SOLUTION_SPECIES"):
            if not line.startswith("#"):
                match=non_whitespace.findall(line)
                if len(match)==5:
                    if molarMassDict != None:
                        molarMassDict[match[0]] = 0.001*float(match[4])
                        pass
                    else:
                        dbbPrimarysList.append(match[0])
                        #
                        # the coefficient 0.001 is intended to convert from g to kg
                        #
                        #print match
                        dbbPrimarysMolarMassList.append(0.001*float(match[4]))
                        pass
            line=dataBaseFile.readline()
        dataBaseFile.close()
        #print ("phreedbg ",dbbPrimarysList,dbbPrimarysMolarMassList)
        #raw_input("phreedbg ")
        if (molarMassDict):
            return molarMassDict
        else:
            return dbbPrimarysList,dbbPrimarysMolarMassList
        
    def setMpiSize(self,mpiSize):
        self.mpiSize = mpiSize

    def setTimeStep(self,timeStep):
        """
        used to set the time step over which equilibrium is reached
        times is necessarly expressed in seconds for a  treatment within Phreeqc
        """
        if isInstance(timeStep,Time):
            zeitInt = timeStep.inBaseUnits()
            zeitInt = timeStep.getValue()
            pass
        else:
            zeitInt = timeStep
            pass
        self.solver.setTimeStep(zeitInt)
        self.timeStep = zeitInt
        return None

    def setSimulationTime(self,simulationTime):
        """
        used to set the simulation time for a batch
        times is necessarly expressed in seconds for a  treatment within Phreeqc
        """
        if isInstance(simulationTime,Time):
            self.simulationTime = simulationTime.inBaseUnits()
            self.simulationTime = simulationTime.getValue()
            self.batch = True
            pass
        return None

    def setDataBase(self,urlName):
        """
        database to be emploied.
        """
        urlName = self.fileRecognition(urlName)
        #print(" dbgp setDataBase: %s"%(urlName))
        #print (type(self.solver))
        #print (dir(self.solver))
        self.solver.setDataBase(urlName)
        self.elementList, self.molarMassList = self.getMolarMassList(urlName)
        return None
    
    def setInitialPorosity(self,porosityField):
        """
        the initial porosity is set-up here, and then modified through the time dependant evolution
        of minerals within the system.
        """
        self.initialPorosity = porosityField
        cell = 0
        for initialNodePorosity in self.initialPorosity:
            self.solver.setInitialNodePorosity(cell,initialNodePorosity)
            cell+=1
            pass
        return None

    def setInitialNodePorosity(self, cell, cellInitialPorosityValue):
        """
        can be used to set-up the porosity on a specific cell 
        """
        self.solver.setInitialNodePorosity(cell,cellInitialPorosityValue)
        return None

    def setPorosity(self,porosityField):
        for porosity in range(len(porosityField)):
            self.solver.setInitialNodePorosity(porosity,porosityField[porosity])
        return None
    
    def defineInputOutput(self, inFile, outFile):
        """
        used to set and open input and output files
        """
        #print " pdbg inFile ",inFile
        #print " pdbg outFile ",outFile
        self.solver.defineInputOutput(inFile, outFile)
        if outFile != None:
            self.outFile = outFile
        return None
    
    def getGasConcentrationValues(self):
        """
        to get gases concentrations list
        """
        return self.solver.getGasConcentration()
    
    def getGasUnknowns(self):
        """
        to get the gas unknowns list
        """
        return self.solver.getGasUnknowns()

    def setParameter(self, outFile = None):
        """
        method used to define the input and output file
        """
        #print (" phreeqc dbg setParameter ",self.solverFileName,outFile)
        #raw_input("in setParameter")
        self.inFile = open(self.solverFileName,'w')
        StatesBounds = {}
        StatesBounds[self.chemicalState.name] = [[1,1],self.chemicalState]
        self.chemicalStateList = [self.chemicalState]
        self.dataSetup(StatesBounds)
        self.solver.defineInputOutput(self.solverFileName, outFile)
        self.outFile = outFile
        return None
        
    def setKineticParameter(self, integrationMethod = None,\
                                  intParamDict = None,\
                                  intOrder = None,\
                                  cvodeStep = None,\
                                  cvodeTol = None):
        """
        -bad_step_max     bad_steps
        -cvode_steps      steps
        -cvode_order      order

        -bad_step_max bad_steps--This option was used only in the
        Runge-Kutta method. Now, the value of this option is used for
        CVODE as well. The value entered is the number of times that
        PHREEQC will invoke CVODE to try to integrate a set of
        rates over a time interval. Default is 500.

        -cvode_steps steps--The value given is the maximum number of
        steps that will taken during one invocation of CVODE.   
        Default is 100.

        -cvode_order order--CVODE uses a specified number of terms in
        an extrapolation of rates using the BFD method. Legal values
        are 1 through 5. A smaller value (2) may be needed if the rate
        equations are poorly behaved. The default is 5.         
        
        parameters for the cvode method can be entered via a dictionnary
    
        """
        if integrationMethod.lower() in ["cvode","rungekutta"]:
            #print "integrationMethod.lower()", integrationMethod.lower()
            #raw_input("integrationMethod.lower()")

            if integrationMethod.lower() == "cvode":
                                                                                            #
                                                                                            # cvode integration
                                                                                            #
                if type(intParamDict).__name__ == "dict":
                    self.intParamDict = intParamDict

                self.integrationMethod[0] = "cvode"
                #
                #integrationMethod
                #
                if intOrder  == None:
                    self.intOrder = 5
                elif type(intOrder) == IntType:     
                    self.intOrder = min(intOrder,5)
                self.integrationMethod[1] = self.intOrder
                #    
                if cvodeTol  == None:
                    self.cvodeTol = 4.e-7
                else:
                    self.cvodeTol = min(cvodeTol,0.1)
                self.integrationMethod[2] = self.cvodeTol
                #    
                if cvodeStep  == None:
                    self.cvodeStep = 250
                elif type(cvodeStep) == IntType:     
                    self.cvodeStep = cvodeStep         
                self.integrationMethod[3] = self.cvodeStep
                
            elif integrationMethod.lower() == "rungekutta":
                                                                                                        #
                                                                                                        # runge kutta integration
                                                                                                        #
                self.integrationMethod[0] = "rungekutta"
                self.integrationMethod[1] = min(intOrder,6)                                             # by default 3
            

            else:
                if cvodeOrder == None:
                    self.cvodeOrder = 6
                elif type(cvodeOrder) == IntType:     
                    self.cvodeOrder = min(cvodeOrder,5)
                if cvodeTol  == None:
                    self.cvodeTol = 4.e-7
                else:
                    self.cvodeTol = cvodeTol
                if cvodeStep  == None:
                    self.cvodeStep = 400
                elif type(cvodeStep) == IntType:     
                    self.cvodeStep = cvodeStep
        else:
            self.integrationMethod = "cvode"
            self.cvodeOrder = 3
            self.cvodeTol = 4.e-7
            self.cvodeStep = 250        
            self.integrationMethod[1] = self.cvodeOrder
            self.integrationMethod[2] = self.cvodeTol
            self.integrationMethod[3] = self.cvodeStep
                
        return None
        
    
    def setPhysic(self, parameter):
        """
        To set the physic to be treated, only temperature for the moment
        """
        if parameter.lower()=='temperature':
            self.temperature = 1    
        return None

    def setStatesBounds(self,problem,StatesBounds,mesh = None):
        """
        Bounds determination for association to chemical states
        """
        chemicalStateList = []
        def StaatWahl(a,b):
            return cmp(a[3],b[3])
    
        def StaatWahl1(a,b):
            print(a[3],b[3],a[1],b[1])
            if a[3]==b[3]:
                if a[1]>b[1]:
                    return 1
                elif a[1]<b[1]:
                    return -1
                elif a[1]==b[1]:
                    return 0
                pass
            elif a[3]<b[3]:
                return -1
            else:
                return +1

        def reorganise(brauchbar,nx):
            liste = []
            min_i1 = nx
            for i in brauchbar:
                min_i1 = min(min_i1,i[1])
                pass
            for i in brauchbar:
                j1 = i[3]
                j2 = i[4]
                if j1!=j2:
                    if i[1]==min_i1 and i[2]==nx:
                        liste.append(i)
                    else:
                        for j in range(j1,j2+1):
                            liste.append([i[0],i[1],i[2],j,j,i[-1]])
                            pass
                        pass
                    pass                            
                else:
                    liste.append(i)
                    pass
            return liste
        #               
        phreeqcchem = problem.name
        input=phreeqcchem
        ind = input.rfind(".")
        if (ind == -1): ind = len(input)
        output = input[0:ind]+".phout"
        self.nx = 0
        print(color.green+" dbp setStatesBounds beg., chemicalStateList: "+color.end, chemicalStateList)
        if problem.initialConditions!=[]:
            #print "dbg grid type ", problem.initialConditions[0].getZone().__class__.__name__
            if problem.initialConditions[0].getZone().__class__.__name__ != "CartesianMesh2D":
                                                                                            #
                                                                                            # we treat elmer bodies
                                                                                            #   
                listOfBoundaryPoints = []        
                for boundary in problem.boundaryConditions:
                    for node in mesh.getBody(boundary.boundary.getBodyName()).getBodyNodesList():
                        if node not in listOfBoundaryPoints:
                            listOfBoundaryPoints.append(node)
                            pass
                        pass
                    pass
                
                kmin = 1000000
                kboundary = 0
                                                                                        #
                                                                                        # We consider initial conditions using elmer
                                                                                        #
                k1 = 0
                temporaryList = [] # that list is introduced to disable node sharing betweeen to surfaces
            
                for initialCondition in problem.initialConditions:
                    if isinstance(problem,ChemicalTransportProblem):
                        chemicalStateList.append(initialCondition.getValue())
                        print ("dbp setStatesBounds, initialCondition updating chemicalStateList: ", initialCondition.getValue().name)
                        print ("dbp setStatesBounds, initialCondition updating chemicalStateList: ", chemicalStateList)
                        pass
                    elif isinstance(problem,THMCProblem):
                        chemicalStateList.append(initialCondition.chemicalState)
                        pass
                    anz = 0
                    nodesList = initialCondition.body.getBodyNodesList()
                    for node in nodesList:
                        if node not in listOfBoundaryPoints and node not in temporaryList:
                            anz+=1
                            listOfBoundaryPoints.append(node)
                            temporaryList.append(node)
                            pass
                        pass
                    #print (" chemical state list ", chemicalStateList)
                    #raw_input("~~~\nwithin statesbounds, initial con. treatment\n~~~")

                    k1 += 1
                    if isinstance(problem,ChemicalTransportProblem):    
                        StatesBounds[initialCondition.getValue().name+str(k1)] =\
                                    [[kboundary+1,kboundary + anz],initialCondition.getValue()]
                        pass
                    elif isinstance(problem,THMCProblem):
                        StatesBounds[initialCondition.chemicalState.name+str(k1)] =\
                                    [[kboundary+1,kboundary + anz],initialCondition.chemicalState]
                        pass
                    kboundary = kboundary + anz
                    pass # end of treatment for the initial conditions
                    
#           k1 = min(tempList)
#           k2 = max(tempList)
#           print "phreeqc dbg initial cond ",k1,k2,kboundary+1,kboundary + k2- k1 + 1
#           if len(tempList) == k2 - k1 + 1:
#               print "phreeqc dbg contigue ",kboundary+1,kboundary + k2 - k1 + 1
#                        StatesBounds[initialCondition.getValue().name+str(k1)] = [[kboundary+1,kboundary + k2 - k1 + 1],initialCondition.getValue()]
#           kboundary = kboundary + k2 - k1 + 1
#           print " value of kboundary ",k1,kboundary
#           print "                    "
#           print "                    "
#
# eventually enhance that part through examples to test it
#
#           else:
#               print "phreeqc dbg len list ",k1,k2,len(tempList),k2-k1+1
#               tempList = initialCondition.zone.getElements()
                
#               print "dbg phreeqc tempList.sort",kboundary
#               print tempList
#               k1 = tempList[0]
#               print "phreeqc dbg kboundary",k1,kboundary
#           ind = 0
#           for i in tempList:
#               if i!=k1+ind:
#                                k2 = kboundary+ind
#               StatesBounds[initialCondition.getValue().name+str(k1)] = [[kboundary+1,k2],initialCondition.getValue()]
#               print " phreec dbg affectation ",kboundary+1,k2
#                   k1 = i
#                   kboundary = k2
#               ind=1
#               else:
#                   ind+=1
#           if (ind!=1):
#               StatesBounds[initialCondition.getValue().name+str(k1)] = [[kboundary+1,kboundary+ind],initialCondition.getValue()]
#                   print " phreec dbg out of loop affectation ",kboundary+1,kboundary+ind
#               kboundary = kboundary+ind
            #print " phreeeqc dbg out of loop",kboundary
#       kmin = kmin - 1
                for stb in StatesBounds.keys():
                    StatesBounds[stb][0][0] = StatesBounds[stb][0][0]
                    StatesBounds[stb][0][1] = StatesBounds[stb][0][1]
                    pass
                    
                #print " phreeqc dbg states bound ",StatesBounds
#               #raw_input("StatesBounds")
                kboundary+=1
#       print "kboundary ",kboundary;raw_input("tata")
                self.setInternalCellsBeforeLaunching(kboundary)

                for boundaryCondition in problem.boundaryConditions :
                    if isinstance(problem,ChemicalTransportProblem):    
                        chemicalStateList.append(boundaryCondition.getValue())
                        print ("type: ",type(boundaryCondition.value))
                        print (boundaryCondition.value)
                        print ("dbp setStatesBounds, boundaryCondition updating chemicalStateList: ", boundaryCondition.getValue().name)
                        print ("dbp setStatesBounds, boundaryCondition updating chemicalStateList: ", chemicalStateList)
                        pass
                    elif isinstance(problem,THMCProblem):
                         chemicalStateList.append(boundaryCondition.chemicalState)
                         pass
                    k1 = kboundary
#                    print " phreeqc dbg states bound bc ",dir(boundaryCondition)
#                    print boundaryCondition.boundary.getBodyName()
                    if isinstance(problem,ChemicalTransportProblem):    
                        StatesBounds[boundaryCondition.boundary.getBodyName()] = [[k1,k1],boundaryCondition.getChemicalStateValue()]
                        pass
                    elif isinstance(problem,THMCProblem):
                        StatesBounds[boundaryCondition.boundary.getBodyName()] = [[k1,k1],boundaryCondition.chemicalState]
                        pass
                    kboundary = kboundary+1
                    self.cellsNumber = kboundary-1      
            else:
                                                                                            #
                                                                                            # Then for a cartesian like support,
                                                                                            # tested for the mt3d cartesian one.
                                                                                            #   
                for boundaryCondition in problem.boundaryConditions:
                    chemicalStateList.append(boundaryCondition.getValue())
                    for zones in boundaryCondition.boundary.zones:
                        self.nx = max(self.nx,zones.getIndexMax().i)
                        pass
                    pass
                for initialCondition in problem.initialConditions:
                    chemicalStateList.append(initialCondition.getValue())
                    for zones in initialCondition.zone.zones:
                        self.nx = max(self.nx,zones.getIndexMax().i)
                        pass
                    pass
    #   
                kboundary = 1
    

                liste = []          
                brauchbar = []          
                for initialCondition in problem.initialConditions:
                    for zones in initialCondition.zone.zones:
                        iMin = zones.getIndexMin()
                        iMax = zones.getIndexMax()
                        indMin = iMin.i
                        indMax = iMax.i
                        jndMin = iMin.j
                        jndMax = iMax.j
        
                        brauchbar.append([initialCondition.getValue().name,\
                                  indMin, indMax, jndMin, jndMax, initialCondition.getValue()])
                        pass
                    pass
    
                brauchbar = reorganise(brauchbar,self.nx)
                brauchbar.sort(StaatWahl)
                brauchbar.sort(StaatWahl1)
    
                for initialCondition in brauchbar:
                    indMin = initialCondition[1]
                    indMax = initialCondition[2]
                    jndMin = initialCondition[3]
                    jndMax = initialCondition[4]
                    state = initialCondition[-1]
                    k1 = kboundary
                    k2 = kboundary+(jndMax - jndMin + 1)*(indMax - indMin + 1)-1
                    liste.append([[initialCondition[0]],k1,k2,state])
                    kboundary = k2+1
                    pass
    
                ind = 0
                for i in liste:
                    chemicalstatelist = i[0][0]+"_"+str(ind)
                    StatesBounds[chemicalstatelist] = [[i[1],i[2]],i[-1]]
                    ind+=1
                    pass
    
                self.setInternalCellsBeforeLaunching(kboundary-1)

                for boundarycondition in problem.boundaryConditions :
                    ind+=1
                    for zones in boundarycondition.boundary.zones:
                        ind_min = zones.getIndexMin()
                        ind_max = zones.getIndexMax()
                        iMin = zones.getIndexMin()
                        iMax = zones.getIndexMax()
                        indMin = iMin.i
                        indMax = iMax.i
                        jndMin = iMin.j
                        jndMax = iMax.j
                        
                        k1 = kboundary
                        k2 = kboundary+(jndMax - jndMin + 1)*(indMax - indMin + 1)-1
                        StatesBounds[boundarycondition.getValue().name] = [[k1,k2],boundarycondition.getValue()]
                        kboundary = k2+1
                        pass
                    pass
                self.cellsNumber = kboundary-1
                pass
        else:
            raise Exception("Warning: You should define initial conditions within your problem") 
            exit(0)
        print(color.green+" dbp setStatesBounds end, chemicalStateList: "+color.end, chemicalStateList)
        #raw_input
        return chemicalStateList
    
    def setChat(self,verbose):
        """
        Used to set verbose for phreeqC 
        """
        self.solver.defineVerbose(verbose)
        return None
    
    def getPrimarySpeciesNames(self):
        """
        to get chemical primary species names
        """
        #print "dbp getPrimarySpeciesNames"
        return self.solver.getPrimarySpecies()
    
    
    def getChemicalUnknownNames(self):
        """
        To get the list of chemicals unknowns: chemical components +  ionic strength and activity of water.
        """
        return self.solver.getChemicalUnknowns()
    
    def getPrimarySpecies(self):
        """
        see getPrimarySpeciesNames
        """
        #print "dbp getPrimarySpecies"
        return [Species(component) for component in self.solver.getPrimarySpecies()]
    
    def getGasSpecies(self,gasList):
        """
        Initialization based on input and database files
        """
        return [Species(gas) for gas in gasList]
        
    def aqueousStateDump(self):
        """
        Used to restart from a previous state
        """
        return self.solver.aqueousStateDump()
        
    def getVolumeFraction(self):
        """
        Retrieve all species concentrations necessary to define
        PhreeqC states all over internal cells
        """
        return self.solver.getVolumeFraction()
        
    def aqueousStateSet(self,celltype):
        """
        That function gives access to previous defined states ( the dump method)
        It is used in conjunction with the iterative algorithm.
        """
        return self.solver.aqueousStateSet(celltype)
    
    def getChemicalZero(self):
        """
        Is used to retrieve from Phreeqc the chemical zero. Chemical values
    which are below are considered as zero
        """
        return self.solver.getChemicalZero()

    def getMobileConcentrationField(self,celltype=None):
        """
        Retrieve primaries concentrations fields from PhreeqC
    celltype can be either internal or boundary. Default is set to internal.
    No control is made over the celltype string, this string being set through a module.
        """       
        celltype = _zellTyp(celltype)

        if (self.mpiSize==1) or (celltype =='boundary'):    
            return self.solver.getMobileConcentration(celltype)
        else:
            print(" pdbg getMobileConcentrationField mpi ")
            return self.solver.getMobileConcentration_mpi(celltype)

    def getJacobian(self,cell):
        """
        Retrieve the jacobian to use within a CG method.
        """
        return self.solver.getJacobian(cell)

    def getPJacobian(self,cell):
        """
        Retrieve the jacobian defined by phreeqc for comparison
        """
        return self.solver.getPJacobian(cell)
    
    def getDebug(self,celltype=None):
        """
        primaries concentrations from PhreeqC over the whole mesh
        """
        celltype = _zellTyp(celltype)       
        return self.solver.getMobileConcentration(celltype)
    
    def getTemperatureField(self):
        """
        to obain the temperature field
        """
        #print("dbg phreeq getTemperatureField")
        return self.solver.getTemperatureField()
    
    def getTotalCO2Field(self):
        """
        to obain the total CO2 field
        """
        #print("dbg phreeq getTotalCO2Field")
        return self.solver.getTotalCO2Field()   

    def getMobileConcentration(self,celltype=None):
        """
        master species concentrations from PhreeqC over the whole mesh
        """
        celltype =  _zellTyp(celltype)
        return self.solver.getMobileConcentration(celltype)
        
    def getConc(self,concentration,componentList,length):
        """
        Retrieve solution concentration for each cell
        """
        return self.solver.getConc(concentration,componentList,length)
        
    def getDensity(self):
        """
        Retrieve water density for each cell
        """
        return self.solver.getDensity()
    
    def getExchangeMasterlist(self):
        """
        to get the sorption sites list
        """
        return self.solver.getExchangemasterlist()
    
    def getExchangeSpecies(self):
        """
        to get the sorbed species concentration list
        """
        return self.solver.getExchangespecies(ex_conc)

    def getExchangeSpecieslist(self):
        """
        to get the list of sorption species
        """

    #if (self.mpiSize==1) or (celltype =='boundary'):    
        #    return self.solver.getImmobileConcentration(celltype)
    #else:
        #    #return self.solver.getImmobileConcentration(celltype)
        return self.solver.getExchangespecieslist()

    def getImmobileConcentration(self,celltype=None):
        return self.solver.getImmobileConcentration('internal')
    
    def getImmobileConcentrationField(self,celltype=None):
        """
        Retrieve concentration 'fixed' for each cell
    
        Input : celltype ( string ) is set to internal  
        Output : a list of concentrations
        
        """
        celltype = _zellTyp(celltype)
        
        if (self.mpiSize==1) or (celltype =='boundary'):    
            return self.solver.getImmobileConcentration(celltype)
        else:
            #return self.solver.getImmobileConcentration(celltype)
            return self.solver.getImmobileConcentration_mpi(celltype)
        
    def getCellConcAtEqui(self,cell):
        """
        Used to handle boundary conditions,
        it enables to get aqueous concentrations
        at the equilibrium, cell being an index
        """
        return self.solver.getCellConcAtEqui(cell)

    def getCellTempAtEqui(self,cell):
        """
        Send back to python the temperature of the cell considered,
        usefull for a boundary condition treatment, the argument cell being an integer
        """
        return self.solver.getNodeEquiTemperature(cell)
        
    def getMWContent(self):
        """
        Retrieve solution concentration for each cell
        """
        return self.solver.getMWContent()

    def getNodeGasEquiConc(self, cell):
        """
        Send back to python the temperature of the cell considered,
        usefull for a boundary condition treatment, the argument cell being an integer  
        """
        return self.solver.getNodeGasConcentration(cell)

    def getAqueousStateprimaryConcentrations(self):
        """
        Send back to python a list of values for aqueous primary species,
    to be used for the boundary conditions. We have to retrieve concentrations 
    related to a single chemicalstate represented by cell 1.
        """
        return self.solver.getCellConcAtEqui(1)
    
    def getPurePhase(self,pp_conc):
        """
        Retrieve the complete list of pure phases from phreeqc.
    The list has been defined by the user.
        """
    
        return self.solver.getPurePhase(pp_conc)
    
    def getPurePhaseList(self):
        """
        To retrieve from PhreeqC the complete list of pure phases involved in the simulation
        """
        return self.solver.getPurePhaseList()
    
    def getPurePhaseAmount(self):
        """
        To retrieve the complete list of pure phases from phreeqc over the domain
    Every mineral of the system has an amount on each cell
    see also setPurePhaseAmount
        """
        return self.solver.getPurePhaseAmount()
        
    def getState(self,states,length_aqueous_comp,length_exchange_comp,length_purephase):
        """
        Used to get all informations necessary for the chemical state definition on a cell
        """
        return self.solver.getState(concentration)

    def getTotalConcentrationValues(self,celltype=None):
        """
        Retrieve concentration 'fixed' + 'aqueous' for each cell
    
    Input : type ( string ) is set to internal
        
    Output : a list of concentrations by master species and cells [ C1_mesh, C2_mesh ]
        """
        celltype = _zellTyp(celltype)
        
        return self.solver.getTotalConcentrationValues(celltype)
    
    def initialize(self,internalNodes):
        """
        Initialization based on input and database files
        """
        self.internalNodesNumber = internalNodes
        self.activeCellsNumber = internalNodes
        self.totalNodesNumber = self.solver.initialize(internalNodes,self.mpiSize)
        return None
    
    def equilibrate(self,zellTyp=None):
        """
        To equilibrate the state cells
        default parameters for the reaction method are set to:
        ntime = 1
        time = 0.0
        """
        ntime = 1
        time = 0.0
#       self.solver.reactions(ntime,time)
        if (zellTyp==None):
            zellTyp = "internal"
            pass
        else:
            zellTyp = "global"
            pass
        if (self.mpiSize==1):
            #print   
            self.solver.reactions(1,zellTyp)
        else:
            self.solver.reactions_mpi(1)
        return 1
    
    def equilibrate_slave(self,zellTyp=None):
        """
        Permits the equilibrium simulation
        default parameters for the reaction method are set to:
        ntime = 1
        time = 0.0
        """
        ntime = 1
        time = 0.0
#       self.solver.reactions(ntime,time)
        if (zellTyp==None):
            zellTyp = "internal"
            pass
        else:
            zellTyp = "global"
            pass
        self.solver.reactions(1,zellTyp)
        return None

    def einzelequilibrium(self,cell):
        """
        To equilibrate a state cell :
        """
        print("one cell equilibrium"*100)
        self.solver.einzelequilibrium(cell)

    def fileRecognition(self,dataBaseName):
        return _fileIdentify(dataBaseName)

    def getAllOutput(self):
        """
        That function is used to get from PhreeqC the information previously defined by the user
        """
        return  self.solver.getOutputAll()
 
    def getOutput(self,name,outputType = None,anf = None,end = None, unit = None):
    
        """
        Permits to retrieve from PhreeqC the information on a physical quantity named by name
        It retrieves for the unknown considered a list of floats associated to each mesh point
    
        Input : 
    
        name (string) : name of the ouput to retrieve
        type (string) : indicates the type of cell considered : for the moment only internal cells are considered
        anf, output_indice_2 (integers) : mesh indices where to retrieve the physical unknowns
    
        The default unit for the outputs is molality: mol/l
    
        """
        if name=="Concentration_mass_water": name = "Concentration_watermass"
    
        name = name.replace('Concentration_','')
        if "Aqueous" in name:
            name = name.replace('Aqueous','')
            pass

        if (unit==None):
            self.unit = "mol/l"
            pass
        elif (unit.lower()=="molal"):
            self.unit = unit
            pass
        else:
            self.unit = "mol/l"
            pass
        
        string = str.find(name,"_")
    
        if (string==-1):
            self.outputname = name
        else:
            self.outputname = name[0:str.find(name,"_")]
            pass
    
        if not(outputType):
            outputType = 'internal'
            pass
        
        if not(anf):
            anf = 0
            end = self.internalNodesNumber
            pass
        
        if (outputType=='internal'):
            indA = 0
            indE = self.internalNodesNumber
            pass
        elif (outputType=='boundary'):
            indA = self.internalNodesNumber+1
            indE = self.internalNodesNumber+self.boundaryNodesNumber-1
            pass
        elif (outputType=='source'):
            indA = self.internalNodesNumber+self.boundaryNodesNumber
            indE = self.internalNodesNumber+self.boundaryNodesNumber+self.sourceNodesNumber
            pass
        elif (outputType=="point"):
            if anf != None:
                indA = anf;indE = anf+1
                pass
            else:
              raise Exception(" lack of an int ")
        else:
            raise Exception("bad type for getOutput %s"%(outputType))
            pass
        if  self.outputname.lower() == 'porosity':
            self.outputname = 'porosity'
            pass
        if (self.mpiSize==1) :
            liste = self.solver.getSelectedOutput(indA,indE,self.outputname,self.unit)
            return liste
        else:
        # only for internal cells
            liste = self.solver.getSelectedOutput_mpi(indA,self.internalNodesNumber, self.outputname,self.unit)

            if len(liste)>1: return liste

    def getOutputState(self,outFormat = None):
        """
        Used to get the following elements:
           activity of water
               electrical balance
           ionicstrength
               number of aqueous master species
               number of aqueous secondary species
               number of minerals               
               number of sorbeb species
           pe
               pH
               temperature
           total H
           total O
           and a list of tuples representing the aqueous and mineral state
        """
        #print("debug 16032016 getOutputState\n", end=' ') 
        if outFormat == None:
            return  self.solver.getOutputState()
        else:
            outputList = self.solver.getOutputState()
            #print outputList
            outputDict = {}
            outputDict ["comment"] = "species outputs are molalities and activities and for mineral; we give first the number of moles then the saturation index (ev. gas fugacity)"
            outputDict["pH"] = outputList[4]
            outputDict["pe"] = outputList[5]
            outputDict["activity of water"] = outputList[6]
            outputDict["ionic strength"] = outputList[7]
            outputDict["temperature"] = outputList[8]
            outputDict["total H"] = outputList[9]
            outputDict["total O"] = outputList[10]
            outputDict["electrical balance"] = outputList[11]
            outputDict["mass of water"] = outputList[12]
            ind = 13
            inf = 13+outputList[0]
            outputDict["primary species"] = outputList[ind:inf]
            ind = inf
            inf = ind+outputList[1]
            outputDict["secondary species"] = outputList[ind:inf]
            ind = inf
            inf = ind+outputList[2]
            outputDict["exchange species"] = outputList[ind:inf]
            ind = inf
            inf = ind+outputList[3]
            outputDict["mineral species"] = outputList[ind:inf]
            return outputDict
    
    def outputStateSaving(self):
        """
        Used to save within a file the following elements:
           activity of water
               electrical balance
           ionicstrength
               number of aqueous master species
               number of aqueous secondary species
               number of minerals               
               number of sorbeb species
           pe
               pH
               temperature
           total H
           total O
           and a list of tuples representing the aqueous and mineral state
        """
        state = self.solver.getOutputState()
        #print " we open self.outFile in outputStateSaving", self.outFile
        #print type(state)
        if self.outFile == None:
            outFile = open("phreeqCFile.out", 'w')
            pass
        else:
            print(" we open self.outFile", self.outFile)
            outFile = open(self.outFile, 'w')
            pass
            
        for i in state:
            outFile.write("%s"%str(i))
            pass
    
    def phiBalance(self):
        return "residual ",self.solver.phibalance()

    def run(self):
        """To equilibrate a single state cell"""
        if self.simulationTime and self.kineticLaws != []:
            self.solver.initialize(1,self.mpiSize)
            self.solver.setTimeStep(self.simulationTime)
            self.solver.reactions(1, "internal")
            pass
        else:
            self.solver.initialize(1,self.mpiSize)
            self.solver.einzelequilibrium(1)
            pass

    def setActivityLaw(self,activityLaw = None):
        """
        To determine which activity law will be used, the default one being Davies.
        """

        if isInstance(activityLaw,Davies):
            self.activityLaw = 'davies'
            pass
        elif isInstance(activityLaw,DebyeHuckel):
            self.activityLaw = 'debye-huckel'
            pass
        elif isInstance(activityLaw,Bdot):
            self.activityLaw = 'b-dot'
            pass
        else:
            self.activityLaw = 'davies'
            pass

    def setChemicalState(self,chemicalState):
        """
        In the case of an equilibrium study for
        a non dimensional case, you use that method normally
        followed by a call to get its equilibrium.
        no cell numbering, having just one to be defined
        """
        self.internalNodesNumber = 1
        self.chemicalState = chemicalState
        self.phreeqC = Phreeqc()
    
    def setComment(self,comment = None):
        """
        Calling that method enables the introduction of any comment within the 
        phreeqC command file
        """
        if type(comment) == StringType:
            self.inFile = open(self.solverFileName,'a')
            self.inFile.write(comment)
            self.inFile.close()
            pass
    
    def setChemicalStates(self,internal,boundaries=None,sources=None):
        """
        Sets the permutation between phreeqc and the mt3d transport
        
        Input 
          internal  indices list of internal cells
          boudaries indices list of boundary cells
          sources   to define
        """

        # internal cells 
        self.internalNodesNumber = len(internal)

        # boundary cells
        if (boundaries!=None):
            self.boundaryNodesNumber = len(boundaries)
        else:    
            self.boundaryNodesNumber = 0

        # source cells 
        self.sourceNodesNumber = 0
                   
        return None

    def setMobileConcentrationValues(self,celltype,concentration_list):
        """
        used to set Concentrations to PhreeqC, A list of species other 
    the mesh :  [Cb over the mesh, TH over the mesh, TO over the mesh, Na over the mesh..]
        """
        self.solver.setMobileConcentrationValues(celltype,concentration_list)

    def setGasConcentrationValues(self,celltype,concentration_list):
        """
        used to set Concentrations to PhreeqC, A list of species other 
        the mesh :  cf. setMobileConcentrationValues
        """
        self.solver.setGasConcentrationValues(celltype,concentration_list)

    def setExpectedOutputs(self,expectedOutputs):
        """
        Fixes the expected outputs

        Input 
        ComputedOutputs : 
        list of (parameter,unit) or parameter if
        no unit  needed (ex pH)
        parameter (str) : name of the output
        unit (str) : unit of the output
        """
        self.dictOutputs = {}
        indexOutputs = 0
        for expectedOutput in expectedOutputs:
            self.dictOutputs[expectedOutput.getName()] = indexOutputs
            indexOutputs += 1
            pass
        return
        


    def mineralSplit(self,mineralName):
        """
        function to split the mineral in an element way, the result is a list of elements
        Only one occurence of  brackets is treated
        """
        result = []
        ind = 0
        l = ""
        print(" mineral treated: ",mineralName)
        mineralName.replace("(g)","")
        for char in mineralName:
            if char in uppercase and ind ==0:
                if l!="":
                    result.append(_ascDi(l))
                    pass
                l = char
                pass
            elif char == "(":
                if l!="":
                    result.append(_ascDi(l))
                    pass       
                l = ""
                ind = 1
                pass
            else:
                l+=char
                pass
        #    print " liste intermediaire ",result
        if ")" in l:
            liste = l.split(")")
            coef = liste[1]
            if coef == "":
                coef = 1
                pass
            else:
                coef = float(coef)
        #        print "liste",liste[0],coef
        #        coef = ""
                pass
            l = ""
            for char in liste[0]:
                if char in uppercase:
                    if l!="":
                        tu = _ascDi(l)
                        aux = float(tu[1])*coef
                        result.append((tu[0],aux))
                        pass
                    l = char
                    pass
                else:
                    l+=char
                    pass
                pass
            tu = _ascDi(l)
            aux = float(tu[1])*coef
            result.append((tu[0],aux))
        elif l!="":
            result.append(_ascDi(l))
        #print " dbg mineral split ",result        
        return result

    def molarMassEvaluation(self, spezien):
        """
        That function is used to evaluate the molar mass of minerals
        """
        liste = self.mineralSplit(spezien.symbol)
        print(liste)
        molarMass = 0.
        for i in liste:
            print(" dbg molar mass list",i[0],i[1])
            molarMass += self.molarMassList[self.elementList.index(i[0])]*i[1]
            pass
        #print molarMass
        #raw_input("molar mass")
        return molarMass
    
    def setKineticLaws(self, kineticLaws):
        """ 
        List of kinetic laws to be brought in the data model
        """
        self.kineticLaws = kineticLaws


    def setMineralAmount(self,mineralName,amount):
        """
        To set the amount of every mineral present in the system on each cell
        arguments are a list and the name of the mineral to be considered
        """
        print(" py just before the call ",mineralName,len(amount))
        self.solver.setMineralAmount(mineralName, amount)
        return None
        
    def setSpeciesBaseAddenda(self,speciesBaseAddenda):
        """ 
        List of new species to be brought in the data model
        """
        for spezien in speciesBaseAddenda:
            if not isinstance(spezien, Species) and not isinstance(spezien, Salt):
                raise Exception(" not all elements of the speciesBaseAddenda are Species or Salt instances")
            pass
        self.speciesBaseAddenda=speciesBaseAddenda
    
    def setChemicalStateList(self, chemicalStateList, porosityOption = None, temperatureOption = None):
        """ 
        That function is used to determine the list of minerals being used within
        the list of chemical states to be treated. It returns a list of minerals: problemMineralList
        For densities, a default value of 2500 kg/m3 is defined
        For thermalConductivity, a default value of 0.6 W/m is defined
        """
        self.porosityOption = porosityOption
        self.chemicalStateList = chemicalStateList
        self.setSolverPorosityOption(self.porosityOption)
        self.temperature = temperatureOption
        if (self.porosityOption or self.thermalOption):
            #raw_input()
            for spezien in self.speciesBaseAddenda:
                if (isinstance(spezien,AqueousMasterSpecies)):
                    if spezien.molarMass:
                        spezien.molarMass.convertToUnit('kg/mol')                           # we use kg/mol as reference unit
                        self.molarMassList.append(spezien.molarMass.value)
                        #print spezien.name, spezien.molarMass.value
                        #raw_input()
##                      if spezien.molarMass.unit.name() == 'kg/mol':
#                           self.molarMassList.append(spezien.molarMass.value*1000)
##                          self.molarMassList.append(spezien.molarMass.value)
##                      elif spezien.molarMass.unit.name() == 'g/mol':   
#                           self.molarMassList.append(spezien.molarMass.value)
##                          self.molarMassList.append(spezien.molarMass.value*0.001)
##                      else:
##                          self.molarMassList.append(spezien.molarMass.value)
                        name = spezien.name[:]
                        if name =='CO3-2':
                            name = "C"
                            pass
                        name = name.replace("-","")
                        name = name.replace('+','')
                        self.elementList.append(name)
                        pass
                    pass
                pass
            #
            # Now, I have to retrieve the molar mass of each mineralist element
            #
            #print (" p dbg  length of self.chemicalStateList",len(self.chemicalStateList),self.chemicalStateList[1].mineralPhase)
            #raw_input()
            for cs in self.chemicalStateList:
                if cs.mineralPhase not in [None,[]]:
                    for mineral in cs.mineralPhase.minerals:
                        if mineral.symbol not in self.problemMineralList:
                            self.problemMineralList.append(mineral.symbol)
            self.problemMineralList.sort()
            #print " p dbg ",self.problemMineralList
            #raw_input(" p dbg ")
            ind = 0
            #
            # Volumic mass
            #
            # the volumic mass (density) is set by default to 2500 kg/m**3 cf. PhysicalQuantities.
            # 2500 corresponds approximatively to the feldspar density
            #
            self.mVolumicMassList = [2500.]*len(self.problemMineralList)
            #
            # ThermalConductivity
            #
            # the default thermal conductivity value is the thermal conductivity value of water.
            #
            self.thermalConductivityList = [0.6]*len(self.problemMineralList)
            self.mMolarMassList = [0.]*len(self.problemMineralList)
            #print "speciesBaseAddenda ",self.speciesBaseAddenda
            for spezien in self.speciesBaseAddenda:
                #print "self.problemMineralList", spezien.name, self.problemMineralList
                if isinstance(spezien,MineralSecondarySpecies) and spezien.name in self.problemMineralList:
                    #print " treatment of ",spezien.name,spezien.density
                    if spezien.density:
                        #print " ctmdbg ",spezien.name,spezien.density.value
                        print(self.problemMineralList)
                        ind = self.problemMineralList.index(spezien.name)
                        self.mVolumicMassList[ind] = spezien.density.value
                        pass
                    if spezien.thermalConductivity != None:
                        ind = self.problemMineralList.index(spezien.name)
                        self.thermalConductivityList[ind] = spezien.thermalConductivity.value
                        pass
                    if spezien.name.rfind("(g)")==-1 and spezien.name.rfind("Fix")==-1:
                        if spezien.name in self.problemMineralList:
                            ind = self.problemMineralList.index(spezien.name)
                            self.mMolarMassList[ind] = self.molarMassEvaluation(spezien)
                            pass
                        pass
                    pass
                pass
            
            ind = 0
            self.mMolarVolumeList = []
            for minerals in self.problemMineralList:
                #
                # the coefficient 1000 is introduced, because we deal within the chemistry solver with mol/L
                # molarMassList is kg/mol mVolumicMassList : kg/m3
                #
                self.mMolarVolumeList.append(1000.0*self.mMolarMassList[ind]/self.mVolumicMassList[ind])
                print(" molar mass and volumic mass ",minerals,self.mMolarMassList[ind],self.mVolumicMassList[ind])
                ind+=1
                pass
            #raw_input("mMolarMassList")
            pass

    def dataSetup(self,StatesBounds):
        """
        first, introduction of the different keywords to allow the update of the database
        then, keyword treatment
        """
        boolean_kinetics = 0
    
        if self.chemicalParameters!=[]:
           for chemicalParameter in self.chemicalParameters:
               self.inFile.write(chemicalParameter)
               pass
           
        print (color.red+"dbp phreeqc dataSetup: "+color.end, StatesBounds)
        print (color.red+"dbp phreeqc dataSetup: "+color.end, StatesBounds.keys())
        amsList = []
        assList = []
        mssList = []
        saltList= []
        ssmsList= []
        sssList = []
        ssList  = []
        ssmList = []
        for spezien in self.speciesBaseAddenda:
    
            if isinstance(spezien,AqueousMasterSpecies):
                amsList.append(spezien)
                pass
            elif isinstance(spezien,AqueousSecondarySpecies):
                assList.append(spezien)
                pass
            elif isinstance(spezien,MineralSecondarySpecies):
                mssList.append(spezien)
                pass
            elif isinstance(spezien,Salt):
                saltList.append(spezien)
                pass          
            elif isinstance(spezien,SorbingSiteMasterSpecies):
                ssmsList.append(spezien)
                pass                    
            elif isinstance(spezien,SorbedSecondarySpecies):
                sssList.append(spezien)
                pass          
            elif isinstance(spezien,SurfaceSecondarySpecies):
                ssList.append(spezien)
                pass          
            elif isinstance(spezien,SurfaceSiteMasterSpecies):     
                ssmList.append(spezien)
                pass
            pass
        #
        if len(amsList) !=0: self.inFile.write("\nSOLUTION_MASTER_SPECIES\n\n")
        for spezien in amsList:
            solutionMasterSpecies(spezien,self.inFile)
            pass
        if len(assList) !=0: self.inFile.write("\nSOLUTION_SPECIES\n\n")
        for spezien in assList:
            solutionSpecies(spezien,self.inFile)
            pass
        if len(mssList) !=0: self.inFile.write("\nPHASES\n\n")
        for spezien in mssList:
            self.inFile.write("      %s\n"%(spezien.name))
            mineralSpecies(spezien,self.inFile)
            pass
        if len(saltList) !=0: self.inFile.write("\nPITZER\n\n")
        saltSpecies(saltList,self.inFile)
        
        if len(ssmsList) !=0: self.inFile.write("\nEXCHANGE_MASTER_SPECIES\n\n")
        for spezien in ssmsList:
            sorbingSiteMaster(spezien,self.inFile)
            pass
        if len(sssList) !=0: self.inFile.write("\nEXCHANGE_SPECIES\n\n")
        for spezien in sssList:
            sorbedSpecies(spezien,self.inFile)
            pass
        if len(ssList) !=0: self.inFile.write("\nSURFACE_SPECIES\n\n")
        for spezien in ssList:
            surfaceSpecies(spezien,self.inFile)
            pass
        if len(ssmList) !=0: self.inFile.write("\nSURFACE_MASTER_SPECIES\n\n")
        for spezien in ssmList:
            surfaceSiteMaster(spezien,self.inFile)
            pass 
        if self.kineticLaws==None:
            self.kineticLaws = []
            pass
        elif self.kineticLaws != []:
            for kineticLaw in self.kineticLaws:
            #if boolean_kinetics==0 and kineticLaw.__class__.__name__ != "FreeKineticLaw":
                if boolean_kinetics==0:
                    self.inFile.write("RATES\n")
                    boolean_kinetics=1
                    pass
                self.kinetics(kineticLaw)
                pass
        print ("states bounds items :",StatesBounds.items())
        for stateBound in StatesBounds.items():

            Staat = stateBound[1][1]
            #print Staat.name
            #print stateBound[1][0]
            #dir(Staat)
            #raw_input("staat")
        
            gA = stateBound[1][0][0]            
            gE = stateBound[1][0][1]
            aqueousSolution(Staat,gA,gE,self.inFile)

            if Staat.solidSolution != None and Staat.solidSolution != []:
                solidSolution(Staat.solidSolution,gA,gE,self.inFile,Staat.name)
                pass

            if self.gasOption == None:
                if Staat.mineralPhase or Staat.gasPhase:
                    mineralSolution(Staat,gA,gE,self.inFile,self.kineticLaws,\
                    self.gasOption, self.integrationMethod, self.intParamDict,\
                    self.timeStep, self.simulationTime)
                    pass
                pass
            else:
                if Staat.mineralPhase:
                    mineralSolution(Staat,gA,gE,self.inFile,self.kineticLaws,\
                    self.gasOption, self.integrationMethod, self.intParamDict,\
                    self.timeStep, self.simulationTime)
                    pass
                #print ("Staat.gasPhase : ",Staat.gasPhase)
                #raw_input("Staat.gasPhase")
                if Staat.gasPhase != None:
                    gasSolution(Staat,gA,gE,self.inFile)
                    pass
                pass
            
            pass
        self.inFile.write("SELECTED_OUTPUT\n  -high_precision true\n")
        self.inFile.write("KNOBS\n  -iterations 500\n  -diag true \n  -tolerance 1.e-15\n")
    
        self.inFile.write("SOLUTION 0\n")

        if self.cellsNumber == 1:
            self.inFile.write("SOLUTION 2\n")

        self.inFile.write("PRINT\n  -reset  true\n"\
        "# hereafter the -cells parameter is the \n"\
        "# only relevant parameter \n")
        #
        # the keyword TRANSPORT is just introduced to enable the creation of C structures
        # wihin the solver
        #
        if self.batch == None:
            self.inFile.write("TRANSPORT\n")
            if self.cellsNumber == 1: self.cellsNumber = 2
            #
            #
            #
            self.inFile.write("  -cells          %i\n"%self.cellsNumber)
            self.inFile.write("  -time_step     100.\n"\
                              "  -shifts          5\n"\
                              "  -lengths         0.1\n"\
                              "  -flow_direction diff\n"\
                              "  -boundary_conditions        closed closed\n"\
                              "  -print_frequency      1\n"\
                              "  -warnings False\n"\
                              "END\n")
            pass
        
        self.inFile.close()
        return None

    def setPurePhaseAmount(self,amount):
        """
        To set the amount of every mineral present in the system on each cell
        """
        self.solver.setPurePhaseAmount(amount)
        return None

    def setSolverPorosityOption(self,porosityoption):
        """
        Used modify the porosity option
        """
        self.solver.setPorosityOption(porosityoption)
        return None
    
    def setTemperatureField(self,celltype,temperatureField):
        """
        Used to set the temperature field
        """
        self.solver.setTemperatureField(celltype,temperatureField)
        return None

    def end(self):
        pass
#
# internal functions
#
def _b0Writer(inFile,elements,b0, description):
    if description == None:
        inFile.write("    %-15s %-15s   %15.8e\n" %(elements[0],elements[1],b0))
    else:
        inFile.write("    %-15s %-15s   %15.8e # %-30s\n" %(elements[0],elements[1],b0, description))
_b1Writer = _b0Writer
_b2Writer = _b0Writer
_c0Writer = _b0Writer

def _logKWriter(inFile,logK):
    inFile.write("%20slog_k   %15.10e\n" %(" ",logK))
    
def _logKCoefWriter(inFile,logKC):
    cliste = [0.0]*5
    ind = 0
    for kcoef in logKC:
        cliste[ind] = kcoef
        ind += 1
        pass
    inFile.write("%20s-analytical_expression  %14.9e %14.9e %14.9e %14.9e %14.9e\n"\
                     %(' ',cliste[0],cliste[1],cliste[2],cliste[3],cliste[4]))

def _keywordWriter(inFile,keyword,anfang,ende,comment):
    keyword+= " "*(25-len(keyword))
    inFile.write("\n%25s %i-%i %s\n" %(keyword,anfang,ende,comment))
def _zellTyp(cellType):
    if not cellType:
        cellType =  'internal'
        pass
    return cellType
 
def _reaction(inFile,formationReaction,symbol):
    string = " "
    for elementTuple in formationReaction:
        if elementTuple[1] == 1:
            string += str(elementTuple[0])+" + "
            pass
        else:
            string += str(str(elementTuple[1])+elementTuple[0])+" + "
            pass
        pass
    string = string[:-2] + " = " + str(symbol)
    inFile.write("%15s%s\n"%(" ",string))
    
    
def _alphan(string):
    """
    a function to handle strings like "2O2".
    The string will be splitted in 2 and O2
    """
    ind = 0
    while string[ind].isdigit() or string[ind] == ".":
        ind+=1
        pass
    if ind == 0:
        numeric = 1
        pass
    else:
        numeric = string[0:ind]
        pass
    return numeric, string[ind:]
    
def _formationReaction(boolean,inFile,formationReaction,symbol):
    
    #print " ---------------\n boolean ",boolean
    #print "formationReaction",formationReaction
    #print "symbol",symbol
    if boolean ==0:
        string = ""
        pass
    else:
        string = str(symbol)+ " = "
        pass
    for elementTuple in formationReaction:
#        print(elementTuple,elementTuple[0],elementTuple[1])
#        if elementTuple[1] == 1:
#            string += str(elementTuple[0])+" + "
#            print " 1 string ",string
#        elif str(elementTuple[1])[0] == "-":
#        str(elementTuple[1])[0] == "-":
        numeric,alpha = _alphan(elementTuple[0])
        sign = " + "
        numeric = float(numeric)*float(elementTuple[1])
        if numeric < 0:
            sign = " - "
            numeric = abs(numeric)
            pass
        string += sign+str(str(numeric) + alpha)
        pass
    if boolean ==0:
        string = string+" = "
        string += str(symbol)
#    else:
#        string = string[:-2]
        pass
    inFile.write("%10s%s\n"%(" ",string))
    
    
def _speciesFormationReaction(inFile,formationReaction,symbol):
    string = ""
    for elementTuple in formationReaction:
        if elementTuple[1] == 1:
            string += str(elementTuple[0])+" + "
            pass
        elif str(elementTuple[1])[0] == "-":
            if string[len(string)-3:]== " = ":
                string = string
                pass
            else:
                string = string[:-3]
                string+=" "+str(str(elementTuple[1])+elementTuple[0])+" + "
                pass
        else:
            string += str(str(elementTuple[1])+elementTuple[0])+" + "
            pass
    string = string[:-2] + " = " + str(symbol)
    inFile.write("%10s%s\n"%(" ",string))
    
def _gamma(inFile,spezien):
    """
    used to write the gamma coefficient,
    at standard conditions:
        a = 0.509312
        b = 0.328308
    """
    #print("debug within the gamma function ")
    if (spezien.coefA !=None and spezien.coefB != None):
        inFile.write("%20s-gamma   %15.10e  %s  %15.10e\n" %(" ",spezien.coefA," ",spezien.coefB))
        pass

    elif spezien.activity_law != None:
        if isInstance(spezien.activity_law,Davies):
            inFile.write("%20s-llnl_gamma    %15.10e # Davies\n"%(" ",spezien.activity_law.A))
            pass
        elif isInstance(spezien.activity_law,DebyeHuckel):
            inFile.write("%20s-gamma   %15.10e  %s  %15.10e\n"\
            %(" ",spezien.activity_law.A," ",spezien.activity_law.B))
            pass
        elif isInstance(spezien.activity_law,Bdot):
            if spezien.activity_law.Bdot == "co2_llnl_gamma":
                inFile.write("%20s -%s\n"%(" ",spezien.activity_law.Bdot))
                pass
            else:
                raise Warning("lack of treatment")
        
        else:
            pass
def _exponentControl(exponent):
   """
   That function is used in the phreeqC kinetic treatment
   to avoid unnecessary exponent evaluation
   it returns  0 if the exponent is equal to 1.
   it returns -1 if the exponent is equal to 0.
   it returns  1 otherwise
   """
   if   abs(exponent-1.)< 1.e-6:
       return 0
   elif abs(exponent-0)< 1.e-6:
       return -1
   else:
       return 1

def _logK_analytic(a1,a2,a3,a4,a5,temp,name = None):
    a = [a1,a2,a3,a4,a5]
    if name == None:
        print("logK is ",a[0] + a[1]*temp +  a[2]/temp + a[3]*log10(temp)+a[4]/(temp*temp))
    else:
        print("logK of  %s is %e"%(name,a[0] + a[1]*temp +  a[2]/temp + a[3]*log10(temp)+a[4]/(temp*temp)))
        
        
def _ascDi(elem):
    asc = ""
    di = ""
    for i in elem:
        if i in ascii_letters:
            asc+=i
        else: 
            pass
    di = di + elem.replace(asc,"")
    if di=="":
        di=1
    return (asc,float(di))

def _fileIdentify(databaseName):
    """
    used to identify the path of the phreeqc database file
    """
    #print("url-1: %s"%(databaseName))
    url = os.path.splitext(databaseName)[0] + '.dat'                                        # we ensure that we have the right extension
    #print("url0: %s"%(url))
    if not os.path.isabs(url):
        url = os.environ['PHREEQCDAT'] + "/" + url
        #print("url1: %s"%(url))
        pass
    if os.path.isfile(url):
        return url.decode('utf-8')
    else:
        #print("url2: %s"%(url))
        url = os.getcwd()+ "/" + url.split("/")[-1]
        #print("url3: %s"%(url))
        if os.path.isfile(url.decode('utf-8')):
            #print (" we return the following string: %s"%(url.decode('utf-8')))
            #print (" we return the following string: %s"%(url.split("/")[-1]))
            return url.split("/")[-1]
            #return url.decode('utf-8')
        else:
                raise Warning("check the existence of the database file you identified")
        pass
    
def cvodewriter(inFile, kineticLaw, integrationMethod, intParamDict):
    """
    used to write within the phreeqc file the elements linked to the cvode solver.
    """
    if type(intParamDict).__name__ == "dict":
        inFile.write("    -cvode true\n")
        if kineticLaw.symbol in intParamDict:
            inFile.write("     -tol %15.10e\n"%(intParamDict[kineticLaw.symbol]["cvodetol"]))
            inFile.write("     -cvode_order %d\n"%(intParamDict[kineticLaw.symbol]["cvodeOrder"]))
            inFile.write("     -cvode_steps %d\n\n"%(intParamDict[kineticLaw.symbol]["cvodeStep"]))
            pass
        else:
            inFile.write("     -tol %15.10e\n"%(integrationMethod[2]))                      # default: 1.-8
            inFile.write("     -cvode_order %d\n"%(integrationMethod[1]))  
            inFile.write("     -cvode_steps %d\n\n"%(integrationMethod[3]))
            pass
        pass
                                #inFile.write(" -step_divide 2.0\n\n")
    elif integrationMethod[0] == "rungekutta":
        inFile.write("    -runge_kutta %s\n"%(3))                                           # default: 3
        pass
    else:
        inFile.write("    -cvode true\n")                               # default values
        inFile.write("    -tol %e\n"%(integrationMethod[2]))                                  # 
        inFile.write("    -cvode_order %d\n"%(integrationMethod[1]))    
        inFile.write("    -cvode_steps %d\n\n"%(integrationMethod[3]))
        pass
    
