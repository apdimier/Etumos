"""Species Data."""
from __future__ import absolute_import
from __future__ import print_function
from generictools import isInstance, listTypeCheck

from PhysicalProperties import Density,\
                               ExchangeCapacity,\
                               MolarMass,\
                               ThermalConductivity

from PhysicalQuantities import Enthalpy,\
                               Mass,\
                               Temperature                               
from re import findall

from string import digits

from types import FloatType,\
                  IntType,\
                  ListType,\
                  NoneType,\
                  StringType,\
                  TupleType
import six
from six.moves import range

def createList(property, propertyClass):
    """
    a utility to fill a property as two lists . First one contains species name and second one property  .
    """
    speciesList = ['ALL']
    speciesProperty = [None]
    if type(property) != ListType:
        if isInstance(property,propertyClass):
            speciesProperty[0] = property
    elif type(property) is ListType:
        for item in property:
            #print " item ",property.__class__
            if isInstance(item,propertyClass):
                speciesProperty[0] = item
            elif type(item) is TupleType:
                (prop, spec) = item
                if type(prop) != ListType:
                    if not isinstance(prop,propertyClass):
                        raise Exception(" problem  with property list definition")
                    pass
                if type(spec) is StringType:
                    spec = Species(spec)
                    pass
                if not isInstance(spec,[Species,Element]):
                    raise Exception("sped in the ceation list is not of the right type")
                speciesList.append(spec.name)
                speciesProperty.append(prop)
                pass
            pass
        pass
    return speciesList, speciesProperty

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
    ind = len(digital)
#
    #print " out of ion numbering ",element, ind, digital
#
    return ind, digital

def molarMassStringEval(mineralName):
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
    else:
        mineralString = [mineralName[:]]
        
    elementList = []
    listOfSpecies = []
    #print " mineralString to be treated ",mineralString
    for character in mineralString:
        if len(character)!=0:
            elementList.append((character,1.))
            pass
        pass
    #print " elementList",elementList
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
                            lange += 2                                                      # we will control that new element
                            if lange < lengthName:
                                iaux = lange
                                if (lange+1 == lengthName):
                                    digit = digit*float(elementName[-1])
                                    lange = lengthName
                                else:
                                    while (elementName[lange].isdigit()  or elementName[lange] == ".") and lange+1 < lengthName:
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
                        #print ind,digit
                        lange += ind+1
                    else:
                        #print "?"
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
            
    #print listOfSpecies
    return listOfSpecies

#----------
# Elements
#----------
class Element:
    """
    Element of the periodic table
    """

    def __init__(self,symbol, name = None):
        """
        Init
          Input :
            symbol (string)
            name (string, OPTIONAL)
        """
        if type(symbol) != StringType:
            raise Exception("symbol in the element definition must be a string")
        self.symbol = symbol
        if name:
            if type(name) != StringType:
                raise Exception("name in the element definition must be a string")            
            self.name = name
        else:
            self.name = symbol

    def setIsotopes(self, isotopes):
        """
        Set the corresponding isotopes
          Input :
            isotopes (list of Species)            
        """
        isotopes=list(isotopes)
        for isotopen in isotopes:
            if not isinstance(isotopen,Species):
                raise Exception(" not all supposed isotopes are right instanced ")
        self.isotopes = isotopes

    def getName(self):
        return self.name

    def getSymbol(self):
        return self.symbol

    def getIsotopes(self):
        """
        Returns the Element isotopes list
        """
        return self.isotopes
    
    def getIsotopesNames(self):
        """
        Returns the Element isotopes names list
        """
        return [iso.getName() for iso in self.isotopes]

    def initialize(self,**kwargs):
        """
         default initialisation method for the attributes of an Entity
        """
        if kwargs != None:
            for key, value in six.iteritems(kwargs):
                if key in self.__dict__:
                    self.__dict__[key].value = value
                    pass
                pass
            pass
        return None

class Salt:
    """
    Generic class to define all salt species related to Pitzer 
    """
    def __init__(self,formationElements,name=None,b0 = None, b1 = None, b2 = None, c0 = None, description = None):
        """
          Input :
                PITZER
                -B0
                  Na+       Cl-       0.0765     -777.03     -4.4706        0.008946   -3.3158E-6
                -B1                                              
                  Na+       Cl-       0.2664        0           0           6.1608E-5   1.0715E-6
                -C0
                  Na+       Cl-       0.00127     33.317      0.09421    -4.655E-5
            
        """
        if type(formationElements) != TupleType:
            raise Exception("formationElements should be a tuple")
        self.formationElements = formationElements
        
        if name:
            if type(name) != StringType:
                raise Exception("name in salt definition must be a string")
            self.name = name
            pass
        if b0:
            if type(b0) not in [FloatType,TupleType]:
                raise Exception("b0 should be a float or a tuple")
            pass
        self.b0 = b0
        if b1:
            if type(b1) not in [FloatType,TupleType]:
                raise Exception("b1 should be a float or a tuple")
            pass
        self.b1 = b1
        if b2:
            if type(b2) not in [FloatType,TupleType]:
                raise Exception("b2 should be a float or a tuple")
            pass
        self.b2 = b2

        if c0:
            if type(c0) not in [FloatType,TupleType]:
                raise Exception("c0 should be a float or a tuple")
            pass
        self.c0 = c0
        self.description = description
            
    def getName(self):
        """ Get the salt name        """
        return self.name
    
    def getformationElements(self):
        """ Get the tuple of elements constituting the salt
        """
        return self.formationElements

    def getb0(self):
        """ Get the Species coef b0"""
        return self.b0

    def getb1(self):
        """ Get the Species coef b1"""
        return self.b1

    def getb2(self):
        """ Get the Species coef b2"""
        return self.b2

    def getc0(self):
        """ Get the Species coef c0"""
        return self.c0

    def initialize(self,**kwargs):
        """
         default initialisation method for the attributes of an Entity
        """
        if kwargs != None:
            for key, value in six.iteritems(kwargs):
                if key in self.__dict__:
                    self.__dict__[key].value = value
                    pass
                pass
            pass
        return None

class InteractionParameters:
    """
    Generic class to define all chemical species
    """
    def __init__(self,ions=None,coef = 0.):
        if ions:
            if ions not in [TupleType,ListType]: raise Exception("ions should be a tple or a ist")
            self.ions = ions
            pass
        else: raise Exception("Pitzer interaction parameters should be defined with a tuple of ions, elements, cations or anions")
        if type(coef) != FloatType: raise Exception(" the coefficient should be a float")
        self.coef = coef

class Lambda(InteractionParameters):
    """
    the lambda coefficient treats interactions between neutral elements and anions or cations
        -LAMDA
            Na+       CO2       0.1
    """
    def __init__(self,ions=None,coef = 0.):
        InteractionParameters.__init__(self,ions=None,coef = 0.)
        if len(self.ions) != 2: raise Exception(" lambda interaction coefficient is not a couple")
        ne  = _getCharge(self.ions[0])
        nac = _getCharge(self.ions[1])
        if ne*nac == 0:
            if ne == 0 and nac == 0: raise Exception(" one tuple element should be an anion or a cation ")
            pass
            
class Teta(InteractionParameters):
    """
    The Teta coefficient treats interactions between anions and anions or cations and cations
    -THETA
      K+        Na+      -0.012
    """
    def __init__(self,ions=None,coef = 0.):
        InteractionParameters.__init__(self,ions=None,coef = 0.)
        if len(self.ions) != 2: raise Exception(" teta interaction coefficient is not a couple")
        ne  = _getCharge(self.ions[0]) 
        nac = _getCharge(self.ions[1])
        if ne*nac == 0: raise Exception(" all elements should be anion or a cation ")
        if ne*nac < 0: raise Exception("  all elements should be be of the same type ")
            
class Psi(InteractionParameters):
    """
    The lambda coefficient treats interactions between neutral elements and anions or cations
        -THETA
            K+        Na+      -0.012
    """
    def __init__(self,ions=None,coef = 0.):
        InteractionParameters.__init__(self,ions=None,coef = 0.)
        if len(self.ions) != 3: raise Exception(" psi interaction coefficient should be a triplet")
        n0 = _getCharge(self.ions[0]) 
        n1 = _getCharge(self.ions[1])
        n2 = _getCharge(self.ions[2])
        if n1*n2*n3 == 0: raise Exception(" all elements should be an anion or a cation ")
           

class Species:
    """
    The Generic class to define all chemical species
    """
    def __init__(self,symbol, name = None, coefA = None, coefB = None, molarMass = None):
        """
        Init
          Input :
            symbol (string)
            name (string, OPTIONAL)
            coefA (float, OPTIONAL) : Debye-Huckel activity law coefficient
            coefB (float, OPTIONAL) : Debye-Huckel activity law coefficient
        Default is the Davies law, otherwise 
        Activity is described page 11 of the phreeqC manual 99-4259
        coefA is the ion-size parameter coefB is 0.1 by default for uncharged species
            
        """
        if type(symbol) != StringType:
            raise Exception("symbol in species definition must be a string")
        self.symbol = symbol
        
        #print " sp dbg name control",name
        if name:
            if type(name) != StringType:
                raise Exception("name in species definition must be a string")
            self.name = name
            pass
        else:
            self.name = symbol
            pass

        self.charge = _getCharge(symbol)
        #print "sp dbg get charge ",self.name,self.charge

        if (coefA!=None):
            if type(coefA) != FloatType:
                raise Exception("coefA in species definition must be a float")
            pass
        self.coefA = coefA

        if (coefB!=None):
            if type(coefB) != FloatType:
                raise Exception("coefB in species definition must be a float")
            self.coefB = coefB
            pass
        elif (coefA!=None):
            self.coefB = 0.1
            pass
        else:
            self.coefB = None
            pass

#        print " class Species molar mass ",molarMass
        self.molarMass = molarMass
#        print " class Species molar mass end"
            
    def getName(self):
        """
        Get the Species name
          Ouput
            (string)
        """
        return self.name
    
    def getSymbol(self):
        """
        Get the Species symbol
          Ouput
            (string)
        """
        return self.symbol

    def getCharge(self):
        """
        To get the Species charge
         It returns the number of charges for the ion as an int
        """
        return self.charge
    
    def getcoefA(self):
        """
        To get the Species coefA coeficient
        It returns a float
        """
        return self.coefA
    
    def getcoefB(self):
        """
        To get the Species coefB coeficient
        It returns a float
        """
        return self.coefB

    def initialize(self,**kwargs):
        """
         default initialisation method for the attributes of an Entity
        """
        if kwargs != None:
            for key, value in six.iteritems(kwargs):
                if key in self.__dict__:
                    self.__dict__[key].value = value
                    pass
                pass
            pass
        return None

class MasterSpecies(Species):
    """
    Generic master species
    """
    def __init__(self, symbol, name = None, element = None, coefA = None, coefB = None):
        """
        Init
          Input :
            symbol (string)
            name (string, OPTIONAL)
            element (string, OPTIONAL)
            coefA (float, OPTIONAL) : Debye-Huckel activity law coefficient
            coefB (float, OPTIONAL) : Debye-Huckel activity law coefficient
            
        """

        Species.__init__(self, symbol, name, coefA, coefB)
#        print "MasterSpecies Species.__init__"
        if element:
            pass
        self.element = element
#        print "MasterSpecies Species.__init__ end"


    def getElement(self):
        """
        Returns the MasterSpecies associateded element
        """
        return self.element

class AqueousMasterSpecies(MasterSpecies):
    """
    Aqueous master species, cf. phreeqC manual: $WRAPPER/Doc/Pdf_doc/phreeqc_manual.pdf
    """
    def __init__(self, symbol, name = None, element = None, molarMass = None,
                 coefA = None, coefB = None, alkalinity = None):
        """
        Init
          Input :
            symbol string type
            name string type
            element string type
            molarMass MolarMass, type used to control porosity variations
            coefA float type : first Debye-Huckel activity law coefficient, see phreeqc manual
            coefB float type : second Debye-Huckel activity law coefficient, see phreeqc manual
            alkalinity float type
           
          Examples
            Ca = AqueousMasterSpecies('Ca++',
                                         element='Ca',
                                         molarMass=MolarMass(40.08E-3,'kg/mol'))  
        """
        MasterSpecies.__init__(self,symbol,name,element,coefA,coefB)
        if not isinstance(molarMass,MolarMass):
            if type(molarMass) != NoneType:
                raise Exception(" problem with molar mass definition of %s"%(name))
            pass
        self.molarMass = molarMass
        
        if alkalinity:
            if type(alkalinity) not in [FloatType,IntType]:
                raise Exception(" alkalinity must be a float ")
            pass
        self.alkalinity = alkalinity
        
    def getMolarMass(self):
        """
        Get the AqueousMasterSpecies molar mass
          Ouput
            (MolarMass)
        """
        return self.molarMass
    
        
    def getAlkalinity(self):
        """
        Get the AqueousMasterSpecies alkalinity
          Ouput
            (float)
        """
        return self.alkalinity

class SecondarySpecies( Species):
    """
    Generic secondary species
    """
    def __init__(self, symbol, formationReaction = None, logK25 = None, name = None,
                 coefA = None, coefB = None, logK = None, vanthoff_enthalpy = None,
                 activity_law = None, molarMass = None):
        """
        Init
          Input :
            symbol (string)
            formationReaction (list of tuple (string,float), ex : [('Al[3+]',1),('F[-]',2.)],
                               OPTIONAL)
            logK25 (float, OPTIONAL)
            name (string, OPTIONAL)
            coefA (float, OPTIONAL) : Debye-Huckel activity law coefficient
            coefB (float, OPTIONAL) : Debye-Huckel activity law coefficient
            logK: is log K of mineral species or secondary species at different Temperature (in Celsius degree)
            
                 A1 + A2 T + A3/T +A4*log10(T) + A5/(T*T)
            
            activity_law  activity law of secondary species
            vanthoff_enthalpy : vanthoff enthalpy of secondary species ( apparent enthalpy: deltaH at 25 Celsius degree) 
            molarMass molar mass of secondary species

        """
        
        Species.__init__(self,symbol,name,coefA,coefB,molarMass)

        if formationReaction:
            if type(logK25) not in [FloatType,IntType]  and type(logK) not in [FloatType,IntType]:
                raise TypeError("If a formation reaction is given, you have to give the logK at 25 or as a function of temperature")
            if type(formationReaction) not in  [TupleType,ListType]:
                six.reraise(TypeError, "type error for the formation reaction arguments", formationReaction)
            
            for x in formationReaction:
                if type(x[0]) != StringType:
                    raise TypeError("type error for the first formation reaction argument ")
                if type(x[1]) not in [FloatType,IntType]:
                    raise TypeError("type error for the second formation reaction argument ")
                pass
            pass
        self.formationReaction = formationReaction
        if logK25:
##            if not(formationReaction):
##                raise "If a logK25 is given, you have to give the formation reaction"
            if type(logK25) not in [FloatType,IntType]:
                raise Exception(" lok25 must be a float ")
            self.logK25 = float(logK25)
        else:
            self.logK25 = 0.0
            pass
        self.logK = logK
        self.vanthoff_enthalpy = vanthoff_enthalpy
        self.activity_law = activity_law


    def setFormationReaction(self,formationReaction):
        """
        Set a formation reaction
          Input :
            formationReaction (list of tuple (string,float), ex : [('Al[3+]',1),('F[-]',2.)])
        """
        listTypeCheck(formationReaction,TupleType)
        for x in formationReaction:
            if type(x[0]) != StringType:
                raise Exception(" the first argument of the formationReaction must be a string ")
            if type(x[1]) not in [FloatType,IntType]:
                raise Exception(" the second argument of the formationReaction must be a string or a float")
            
        self.formationReaction = formationReaction

    def getFormationReaction(self):
        """
        Get the SecondarySpecies formation reaction
          Output :
            (list of ...)
        """
        return self.formationReaction
    
    def getLogK25(self):
        """
        Get the SecondarySpecies logK at 25 degree
          Output :
            (float)
        """
            
        return self.logK25

    def getMolarMass(self,molarMassDictionary):
        """
        Get the Aqueous Secondary Species molar mass
          Ouput
            (MolarMass)
            
        That function is used with a prior call like:
             URL  = os.getenv("WRAPPER")+"/Phreeqc_dat/"+"phreeqc.dat"
             molarMassDictionary = chemistrySolver.getMolarMassList(URL,typ = {})
             where chemistrySolver is an instance of a chemical solver.
             For the moment, only phreeqc is available (chemistrySolver = Phreeqc()).
        """
        molarMass = 0
        aqueousMasterSpeciesAmount = molarMassStringEval(self.symbol) 
        for ion in aqueousMasterSpeciesAmount:
            molarMass+= molarMassDictionary[ion[0]]*ion[1]
            pass
        self.molarMass = molarMass
        return self.molarMass

    
    def getVantHoffFactor(self):
        """
        For most ionic compounds dissolved in water, the van 't Hoff factor is equal to the number of discrete ions in a formula unit of the substance.
        This is true for ideal solutions only, as occasionally ion pairing occurs in solution.  
        """
        ifactor = 0
        for comp in self.formationReaction:
            factl =  findall(r'\A[0-9-.]+',comp[0])
            isplit = 1
            if len(factl) != 0:
                isplit = float(factl[0])
                pass
            #print ("factl", factl, type(factl),comp[0])
            #print ("ifactor", ifactor, type(ifactor))
            #print ("isplit ",isplit, type(isplit))
            #print ("comp[1]",int(comp[1]),float(comp[1])*isplit)
            ifactor+=float(comp[1])*isplit
            pass
        #print ("vanthoff factor ",ifactor)
        self.vanthoffFactor = ifactor
        return self.vanthoffFactor

    
class SorbingMasterSpecies(MasterSpecies):
    """
    Sorbing master species
    """
    def __init__(self,symbol,mineral=None,aqueousSpecies=None,stochioCoef=None,exchangeCapacity=None,
                 name=None,element=None):
        """
        Init
          Input :
            symbol (string)
            mineral (string, OPTIONAL)
            aqueousSpecies (string, OPTIONAL)
            stochioCoef (float, OPTIONAL)
            exchangeCapacity  (ExchangeCapacity, OPTIONAL)
            name (string, OPTIONAL)
            element (string, OPTIONAL)

          Examples 
            New_X_Ca =
              SorbingMasterSpecies('X(Ca)',
                                      mineral='X',
                                      aqueousSpecies='Ca[2+]',
                                      stochioCoef=1,
                                      exchangeCapacity=ExchangeCapacity(1.023,'mol/m2'))
            
        """

        MasterSpecies.__init__(self, symbol, name, element)

        if mineral:
            if type(mineral) != StringType:
                raise Exception(" mineral within SorbingMasterSpecies must be a string ")
            pass
        self.mineral = mineral
        
        if aqueousSpecies:
            if type(aqueousSpecies) != StringType:
                raise Exception(" aqueousSpecies within SorbingMasterSpecies must be a string ")
            pass
        self.aqueousSpecies = aqueousSpecies

        if stochioCoef:
            if type(stochioCoef) not in [FloatType,IntType]:
                raise Exception(" stochioCoef within SorbingMasterSpecies must be a float ")
            pass
        self.stochioCoef = stochioCoef

        if exchangeCapacity:
            if not isinstance(exchangeCapacity,ExchangeCapacity):
                raise Exception("exchange capacity definition is not correctly defined")
            pass
        self.exchangeCapacity = exchangeCapacity

    def getMineral(self):
        """
        Get the mineral associated to the SorbingMasterSpecies  
          Ouput
            (string)
        """
        return self.mineral
    
    def getAqueousSpecies(self):
        """
        Get the aqueous species to the SorbingMasterSpecies 
        it returns a sring or
        a list of strings
        """
        return self.aqueousSpecies
    
    def getStochioCoef(self):
        """
        Get the SorbingMasterSpecies associated stochiometric coefficient
          Ouput
            (ExchangeCapacity)
        """
        return self.stochioCoef
    
    def getExchangeCapacity(self):
        """
        Get the SorbingMasterSpecies exchanAqueousSecondarySpeciesge capacity
          Ouput
            (ExchangeCapacity)
        """
        return self.exchangeCapacity

class SorbingSiteMasterSpecies(MasterSpecies):
    """
    Sorbing site  master species
    Init as MasterSpecies
    """
    def __init__(self,symbol,element=None,stochioCoef=None,exchangeCapacity=None,name=None):
        
        MasterSpecies.__init__(self,symbol,name,element)

        if stochioCoef:
            if type(stochioCoef) not in [FloatType,IntType]:
                raise Exception("stochiocoef must be a float ")
            pass
        self.stochioCoef = stochioCoef

        if exchangeCapacity:
            if not isinstance(exchangeCapacity,ExchangeCapacity):
                raise Exception("exchange capacity definition is not correctly defined")
            pass
        self.exchangeCapacity = exchangeCapacity
       
    def getStochioCoef(self):
        """
        Get the SorbingMasterSpecies associated stochiometric coefficient
          Ouput
             (ExchangeCapacity)
        """
        return self.stochioCoef
    
    def getExchangeCapacity(self):
        """
        Get the SorbingMasterSpecies exchange capacity
          Ouput
            (ExchangeCapacity)
        """
        return self.exchangeCapacity
    
    pass

class SurfaceSiteMasterSpecies(MasterSpecies):
    """
    Surface site  master species
    """
    def __init__(self,symbol,mineral=None,exchangeCapacity=None,name=None,element=None):
        """
        Init
          Input :
            symbol (string)            
            mineral (string, OPTIONAL)
            exchangeCapacity  (ExchangeCapacity, OPTIONAL)
            name (string, OPTIONAL)
            element (string, OPTIONAL)
        """        
        MasterSpecies.__init__(self,symbol,name,element)


        if mineral:
            if type(mineral) is not StringType:
                raise Exception(" mineral must be a string ")
            pass
        self.mineral = mineral
        
        if exchangeCapacity:
            if not isinstance(exchangeCapacity,ExchangeCapacity):
                raise Exception("exchange capacity definition is not correctly defined")
            pass
        self.exchangeCapacity = exchangeCapacity

    def getMineral(self):
        """
        Get the SurfaceSiteMasterSpecies associated mineral  species 
          Ouput
            (string)
        """
        return self.mineral
    
    def getExchangeCapacity(self):
        """
        Get the SurfaceSiteMasterSpecies exchange capacity
          Ouput
            (ExchangeCapacity)
        """
        return self.exchangeCapacity
#
# the surfacesitemasterspecies class should disappear
#
class SurfaceMasterSpecies(MasterSpecies):
    """
    Surface site  master species
    """
    def __init__(self,symbol,mineral=None,exchangeCapacity=None,name=None,element=None):
        """
        Init
          Input :
            symbol (string)            
            mineral (string, OPTIONAL)
            exchangeCapacity  (ExchangeCapacity, OPTIONAL)
            name (string, OPTIONAL)
            element (string, OPTIONAL)
        """        
        MasterSpecies.__init__(self,symbol,name,element)


        if mineral:
            if type(mineral) is not StringType:
                raise Exception(" mineral must be a string ")
        self.mineral = mineral
        SecondarySpecies
        if exchangeCapacity:
            if not isinstance(exchangeCapacity,ExchangeCapacity):
                raise Exception("exchange capacity definition is not correctly defined")
            pass
        self.exchangeCapacity = exchangeCapacity

    def getMineral(self):
        """
        Get the SurfaceSiteMasterSpecies associated mineral  species 
          Ouput
            (string)
        """
        return self.mineral
    
    def getExchangeCapacity(self):
        """
        Get the SurfaceSiteMasterSpecies exchange capacity
          Ouput
            (ExchangeCapacity)
        """
        return self.exchangeCapacity


class AqueousSecondarySpecies( SecondarySpecies):
    """
    Aqueous secondary species
    Init as SecondarySpecies

      Examples
        H3SiO4 =
          AqueousSecondarySpecies('H3SiO4[-]',
                                  formationReaction=[('H[+]',-1),('H4SiO4',1)],
                                  logK25 = -9.8)
    """
    pass

class GaseousSecondarySpecies( SecondarySpecies):
    """
    Definition of gaseous secondary species
    """
    pass


class MineralSecondarySpecies(SecondarySpecies):
    """
    Definition of minerals as secondary species
    """
    def __init__(self,symbol, formationReaction = None, logK25 = None,name = None,
                 density = None, logK = None, vanthoff_enthalpy = None,
                 activity_law = None, molarMass = None, thermalConductivity = None):
        """
        Init
          Input :
            symbol      a string
            formationReaction a list of tuple (string,float), ex : [('Na[+]',1),('Cl[-]',1)],
                               OPTIONAL)
            logK25      a float
            logK        a list of floats, see the phreeqC manual or the documentation
            ea          a float representing the energy of activation KJ/mol
            name        a string
            density (Density, OPTIONAL)

          Examples :
            Quartz =
              MineralSpecies('Quartz',
                                      formationReaction=[('H2O',-2),('H4SiO4',1)],
                                      logK25 = 3.6,
                                      density  = Density(2648.29,'kg/m**3'))
        """
        coefA = None
        coefB = None
        SecondarySpecies.__init__(self,symbol, formationReaction, logK25, name,
                                  coefA, coefB, logK,
                                  vanthoff_enthalpy,
                                  molarMass, activity_law)

        if density:
            if density.__class__.__name__ is not "Density":
                raise Exception(" problem with density definition of %s"%(symbol))
            pass
        self.density = density

        if thermalConductivity!=None:
            if thermalConductivity.__class__.__name__ is not "ThermalConductivity":
                raise Exception("the thermal conductivity os not an instance of the thermalConductivity class ")
            pass
        self.thermalConductivity = thermalConductivity
                                                                                            #
                                                                                            # Energy of activation kJ/mol
                                                                                            #
        self.ea = 0.
                                                                                            #
                                                                                            # Adding default parameters
                                                                                            #
        self.kinBoolean = 0
        self.iss = 0                                                                                
        self.dryPrecipitation = 0                                                                                
        self.kinConstraint = 0                                                             # a flag 0 equilibrium (ikin = 0), ikin = :  1 dissolution,
                                                                                            #                                           2 precipitation,
                                                                                            #                                           3 both        
    def setActivationEnergy(self,activationenergy):
        """
        Enthalpy of formation is supposed to be in kJ/mol like activation energy.
        According to the Arrhenius equation, we have:
    
            k = A exp (-Ea /RT)
        
            A is called the pre-exponential factor, R is the gas constant and T the absolute temperature. We can get rid of A takin the neperian log
            of that equation:
        
            ln k = ln A -Ea/RT => ln (k1/k2) = EA * (1/T2 - 1/T1)
        
            So, if the Van't Hoff enthalpy is given (deltaH at 25 Celsius degree) we should avoid to introduce the activation energy
        
        
        
       
        """
        self.ea = activationenergy
        return None
        
        
    def getDensity(self):
        """
        Get the  MineralSecondarySpecies density
          Output :
            (Density)
        """
        return self.density
        
class Mineral(MineralSecondarySpecies):
    pass
        
class RedoxCouple( SecondarySpecies):
    """
    Redox  couple
    Init as SecondarySpecies
    """
    pass

class SorbedSecondarySpecies( SecondarySpecies):
    """
    Sorbed secondary species
    Init as SecondarySpecies

      Examples
        New_X_Sr =
          SorbedSecondarySpecies('X(Sr)',
                                 [('X(Ca)',1),('Sr[2+]',1),('Ca[2+]',-1)],
                                 0.021)    
        
    """
    pass

class SurfaceSecondarySpecies( SecondarySpecies):
    """
    """
    pass
    
def _getCharge(symbol):
    """
    extracting charge from  element description like Ca, Ca[], Ca(), Ca{}, Ca++, Ca[++], Ca[2+]
       
    Ca2+ is not a correct expression
    """
    if "(" in symbol: symbol = symbol.replace("(","[").replace(")","]")
    if "{" in symbol: symbol = symbol.replace("{","[").replace("}","]")
    anal = symbol[-1]
    charge = symbol[:-1]
    if anal == ']':
        charge = charge[symbol.index('['):]
        if len(charge) > 1 and charge[1] in digits:
            # [2+]
            return int(charge[1]) * _getCharge(charge)
        else:
            # [++]
            return _getCharge(charge)
    elif anal == '+':
        return (1 + _getCharge(charge))
    elif anal == '-':
        return (-1 + _getCharge(charge))
    else:
        return 0
