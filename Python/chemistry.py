"""Chemical Model 

All that is needed to define a chemical problem
and the specific part of a  ChemicalTransport problem
"""

from generictools import checkClassList, Generic, isInstance

from PhysicalProperties import ReactionRate,\
                               SpecificAreaPerMole

from PhysicalProperties import ElectricPotential

from PhysicalQuantities import MolesAmount,\
                               PhysicalQuantity,\
                               Scalar,\
                               Time,\
                               _findUnit                           

from physicallaws import PhysicalLaw

from species import *

from types import BooleanType,FloatType,IntType,ListType,StringType,TupleType

from cartesianmesh import CartesianMesh

from timespecification import TimeSpecification

from commonproblem import CommonExpectedOutput


#--------------------------------------------------------------
# Chemical Quantity 
#--------------------------------------------------------------
class ChemicalQuantity(Scalar):
    """
    Generic definition of a chemical quantity :
    a value and a unit associed to a chemical species or element
    """
    def __init__(self, symbol, value, unit):
        """
        Init
          Input :
            symbol (string)
            value (float)
            unit (string)
        
        """
        _typecontrol(symbol,[StringType]," the symbol must be a string ")
        self.symbol = symbol
        Scalar.__init__(self,value,unit)

    def getSymbol(self):
        
        return self.symbol

    def getHelp(self):
        
        print self.__doc__
    
    def getUnit(self):
        return self.unit

    pass

class Activity(ChemicalQuantity):
    """
    Species activity (only for aqueous ones)
      Unit type = None
      Init  as ChemicalQuantity

    Examples
      Na = Activity('Na[+]',0.1)
      """
    default_unit = None
    pass

class SpeciesConcentration(ChemicalQuantity):
    """
    Species concentration
      Unit type = Concentration
      Init as ChemicalQuantity

    Examples
      Na = SpeciesConcentration('Na[+]',0.1,'mol/l')
      Na = SpeciesConcentration('Na[+]',0.1,'mmol/l')
      Quartz = SpeciesConcentration('Quartz',0.1,'mmol/l')
    """
    default_unit = _findUnit('Concentration')
    pass
    
class SpeciesMassConcentration(ChemicalQuantity):
    """
    Species mass concentration
      Unit type = MassConcentration
      Input : as ChemicalQuantity

    Examples
      Na = SpeciesMassConcentration('Na[+]',0.1,'g/l')
      Na = SpeciesMassConcentration('Na[+]',0.1,'kg/m3')
      Quartz = SpeciesMassConcentration('Quartz',0.1,'g/l')
    """
    default_unit = _findUnit('MassConcentration')
    pass
    
class SpeciesMolalConcentration(ChemicalQuantity):
    """
    Species molal concentration 
      Unit type = MolalConcentration
      Init as ChemicalQuantity

    Examples
      Na = SpeciesMolalConcentration('Na[+]',0.1,'molal')
      Na = SpeciesMolalConcentration('Na[+]',0.1,'mmolal')
      Quartz = SpeciesMolalConcentration('Quartz',0.1,'molal')
    """
    default_unit = _findUnit('MolalConcentration')
    pass

class ElementConcentration(ChemicalQuantity):
    """
    Element total concentration
      Unit type = Concentration
      Init as ChemicalQuantity 

    Examples
      Na = ElementConcentration('Na',0.1,'mol/l')
      Na = ElementConcentration('Na',0.1,'mmol/l')
    """
    default_unit = _findUnit('Concentration')
    pass
    
class ElementMassConcentration(ChemicalQuantity):
    """
    Element mass  concentration
      Unit type = MassConcentration
      Init as ChemicalQuantity

    Examples
      Na = ElementMassConcentration('Na',0.1,'g/l')
      Na = ElementMassConcentration('Na',0.1,'kg/m3')
    """
    default_unit = _findUnit('MassConcentration')
    pass
    
class ElementMolalConcentration(ChemicalQuantity):
    """
    Element molal concentration
      Unit type = MolalConcentration
      Init as ChemicalQuantity

    Examples
      Na = ElementMolalConcentration('Na',0.1,'molal')
      Na = ElementMolalConcentration('Na',0.1,'mmolal')
    """
    default_unit = _findUnit('MolalConcentration')
    pass
  
class TotalConcentration(ChemicalQuantity):
    """
    Species  total concentration (only for aqueous ones)
      Unit type = Concentration
      Init as ChemicalQuantity

    Examples
      Na = TotalConcentration('Na[+]',0.1,'mol/l')
      Na = TotalConcentration('Na[+]',0.1,'mmol/l')
    """
    default_unit = _findUnit('Concentration')  
    pass

class TotalMassConcentration(ChemicalQuantity):
    """
    Species total mass concentration (only for aqueous ones)
      Unit type = MassConcentration
      Init as ChemicalQuantity

    Examples
      Na = TotalMassConcentration('Na[+]',0.1,'g/l')
      Na = TotalMassConcentration('Na[+]',0.1,'kg/m3')
    """
    default_unit = _findUnit('MassConcentration')
    pass

class TotalMolalConcentration(ChemicalQuantity):
    """
    Species  total molal concentration (only for aqueous ones)
      Unit type = MolalConcentration
      Init as ChemicalQuantity
      
    Examples
      Na = TotalMolalConcentration('Na[+]',0.1,'molal')
      Na = TotalMolalConcentration('Na[+]',0.1,'mmolal')
    """
    default_unit = _findUnit('MolalConcentration')
    pass
    
class MineralConcentration(ChemicalQuantity):
    """
    The user enters here a mineral species and its concentration
    Unit type = Concentration
    Init as ChemicalQuantity
    phreeqc uses minerals with a capital letter at first
      
    Examples
      Quartz = MineralTotalConcentration('Quartz',0.1,'mmol/l',saturationIndex=0.0)
    """
    def __init__(self,symbol, value, unit=None,saturationIndex = None):
        if symbol[0].upper() != symbol[0]:
            raise Exception, " check the mineral name, the first letter should be capitalized"
        ChemicalQuantity.__init__(self,symbol, value, unit=unit)
        if saturationIndex!=None:
            self.saturationIndex = saturationIndex
        else:
            self.saturationIndex = 0.
            
    default_unit = _findUnit('Concentration')
    pass

MineralTotalConcentration = MineralConcentration

class ToDissolveMineralTotalConcentration(ChemicalQuantity):
    """
    Species total mineral concentration of a mineral 
      Unit type = Concentration
      Init as ChemicalQuantity
      Enables to specify a mineral that can't precipitate
    Examples
      Quartz = toDissolveMineralTotalConcentration('Quartz',0.1,'mmol/l')
    """
        
## 	if self.saturationIndex == None:
## 	    self.saturationIndex = 0.

    default_unit = _findUnit('Concentration')
    pass


    
class MineralTotalMassConcentration(ChemicalQuantity):
    """
    Chemical total mineral mass concentration
      Unit type = MassConcentration
      Init as ChemicalQuantity
      
    Examples
      Quartz = MineralTotalMassConcentration('Quartz',0.1,'g/l')
    """
    default_unit = _findUnit('MassConcentration')
    pass
    
class MineralTotalMolalConcentration(ChemicalQuantity):
    """
    Chemical total mineral molal concentration
      Unit type = MolalConcentration
      Init as ChemicalQuantity
      
    Examples
      Quartz = MineralTotalMolalConcentration('Quartz',0.1,'mmol')
    """
    default_unit = _findUnit('MolalConcentration')
    pass
    
class Fugacity(ChemicalQuantity):
    """
    Chemical fugacity for gaseous species
      Unit type = None
      Init as ChemicalQuantity
      Fugacity is a measure of chemical potential in the form of 'adjusted pressure.' It reflects the tendency of a substance 
      to prefer one phase (liquid, solid, or gas) over another, and can be literally defined as 'the tendency to flee or escape'.

      Fugacity / Fugacity coefficient:

                fugacity_coefficient = fugacity / ideal_gas_pressure
    Examples
      mud = Fugacity('CO2(g)',0.2)

    The value is the partial pressure. For phreeqC, the default amount of moles is of 10,
    fugacity being considered as a saturation index.
    index
    """
    def __init__(self,symbol, value, unit = None):
        """
        value   <->     fugacity ( saturation index )
        amount  <->     amount of moles
        """
        default_unit = _findUnit("Fugacity")
        ChemicalQuantity.__init__(self, symbol, value, unit = default_unit)
        self.amount = 10.

    def setAmount(self,amount):
        """
        amount is the available amount of moles to reach the fugacity, the saturation index
        """
        self.amount = amount

    pass

class SpecificSurfaceArea(ChemicalQuantity):
    """
    Specific surface area
      Unit type = SpecificSurfaceArea default m2/kg
      Init as ChemicalQuantity  
       
    Examples
      SurfY =  SpecificSurfaceArea('Y',200,'m2/kg')
    """
    default_unit = _findUnit('SpecificSurfaceArea')
    pass

class SpecificAreaPerGram(ChemicalQuantity):
    """
    Specific surface area per gram
      Unit type = SpecificSurfaceArea
      Init as ChemicalQuantity  
       
    Examples 
    """
    default_unit = _findUnit('SpecificSurfaceArea')
    pass


class ConstantSurfaceArea(ChemicalQuantity):
    default_unit = _findUnit('Surface')
    pass


class VolumicSurfaceArea(ChemicalQuantity):
    """
    Volumic surface area
      Unit type = VolumicSurfaceArea
      Init as ChemicalQuantity  
       
    Examples  
      SurfY =  VolumicSurfaceArea('Y',200,'1/m3')
    """
    default_unit = _findUnit('VolumicSurfaceArea')
    pass

class CompositeSurfaceArea(ChemicalQuantity):

    ## @brief Constructor of the class
    def __init__(self,symbol, value, area,unit = None):
        ChemicalQuantity.__init__(self,symbol, value, unit)
        self.area = area
        default_unit = None
        pass
    pass


class LatticeSurfaceArea(ChemicalQuantity):
    default_unit = _findUnit('VolumicSurfaceArea')
    pass

#
## class RelativeTotalConcentration(ChemicalQuantity):
##     """
##     Relative total concentration
##       Unit type = None
##     """
##     default_unit = None

##     def __init__(self, *args,**kwargs):
##         """
##         Init
##           Input :
##             symbol (string)
##             mineral (string)
##             value (float)  
       
##           Examples
##             ConcY = RelativeTotalConcentration('Y','Halite',0.3)
          
            
##         """
##         ChemicalQuantity.__init__(self,self.symbol,self.value)
##         return None
##     pass
class RelativeTotalConcentration(ChemicalQuantity):
    """
    Relative total concentration
      Unit type = None
    """
    default_unit = None
    def __init__(self, symbol, mineral, value):
        """
        Init
          Input :
            symbol (string)
            mineral (string)
            value (float)  
       
          Examples
            ConcY = RelativeTotalConcentration('Y','Hematite',0.3)
          
            
        """
        ChemicalQuantity.__init__(self,symbol,value)
        _typecontrol(mineral,[StringType]," mineral within RelativeTotalConcentration should be a string ")
        self.mineral = mineral
        return
        
    def getMineral(self):
        """
        Get RelativeTotalConcentration mineral 
          Output :
            (string)
        """
	return self.mineral

    pass

#-------------
# Kinetics law
#-------------
class KineticLaw(PhysicalLaw):
    """
    Generic kinetic law
    """
    pass

class ReversibleKineticLaw(KineticLaw):
    """
    
    Reversible kinetic law
    
    """
    def __init__(self, symbol,
                rate, 
                SRExponent = None,
                sphereModelExponent = None,
                specificSurfaceArea = None,
                parameter=None
                ):
        """
        Init
          Input :
            symbol (string)
            rate (specific rate) : specific rate in mol/m2/s 
            
	    sphereModelExponent (float, OPTIONAL) : default 0
	    
	    specificSurfaceArea (float, OPTIONAL) : default 1.0 represents the ration A/V with:
	    
	        A surface area of 1kg soil
	        V volume of water in contact with 1 kg soil

            SRExponent (float, OPTIONAL) : default is 1
            
          Examples :
          
            KinSchoepite = ReversibleKineticLaw('Schoepite',ReactionRate(1e-11,'mol/m2/s'))
            
            KinSchoepite = ReversibleKineticLaw(symbol='Schoepite',rate=ReactionRate(1e-11,'mol/m2/s'),SRExponent =1.5)
            
        """        
        _typecontrol(symbol,[StringType]," symbol within ReversibleKineticLaw should be a string ")
        
        self.symbol = symbol

        if not isinstance(rate, ReactionRate):
            raise Exception, " rate instance has to be redefined"
        self.rate = rate 

        if SRExponent:
            _typecontrol(SRExponent,[FloatType,IntType]," power within ReversibleKineticLaw should be a float or an int ")
            self.SRExponent  = float(SRExponent)
        else:
            self.SRExponent  = 1.0
            pass
	    
        if sphereModelExponent:
            _typecontrol(sphereModelExponent,[FloatType,IntType]," the sphereModelExponent for ReversibleKineticLaw is of the wrong type ")
            self.sphereModelExponent  = float(sphereModelExponent)
        else:
            self.sphereModelExponent  = 0.0
            pass
	    
        if specificSurfaceArea:
            _typecontrol(specificSurfaceArea,[FloatType,IntType]," specificSurfaceArea within ReversibleKineticLaw should be a float")
            self.specificSurfaceArea  = float(specificSurfaceArea)
        else:
            self.specificSurfaceArea  = 0.0
            pass
        return

    def getSymbol(self):
        """
        Get Reversible kinetic rate Law symbol
          Output :
            (string)
        """
        return self.symbol
    
    def getRate(self):
        """
        Get Reversible kinetic rate Law rate
          Output :
            (float)
        """
        return self.rate
    
    def getSRExponent(self):
        """
        to get the exponent of the saturation ratio
          Output :
            (None or float)
        """
        return self.power
	
    def getSpecificSurfaceArea(self):
        """
        Get the specific surface area 
          Output :
            (None or float)
        """
        return self.SpecificSurfaceArea
	
    def getSphereModelExponent(self):
        """
        Get the exponent of the sphere model 
          Output :
            (None or float)
        """
        return self.sphereModelExponent

    pass

#---------------
# Activity Laws
#---------------
class ActivityLaw(PhysicalLaw):
    """
    Generic activity law
    """
    def __init__(self,A=None):
        """
        Init
          Input :            
            A (float, OPTIONAL) : default is 0.5114 for Chess and 0.509 for PhreeqC at standard conditions
        """

        if A:
            _typecontrol(A,[FloatType,IntType],"A coef within activitylaw should be a float or an int ")
            self.A = float(A)
        else:
            self.A = 0.5114
            pass

        return


    def getA(self):
        """
        Get A coefficient for ActivityLaw
          Output :
            (float)
        """
        return self.A

class Davies(ActivityLaw):
    """
    Davies activity law
      Init as ActivityLaw
    """
    def __init__(self,A=None):
        ActivityLaw.__init__(self,A)
        return


class TruncatedDavies(ActivityLaw):
    """
    Truncated Davies activity law
      Init  as ActivityLaw
    """
    def __init__(self,A=None):
        ActivityLaw.__init__(self,A)
        return
        
    
class DebyeHuckel(ActivityLaw):
    """
    Debye Huckel activity law
        
    """
    def __init__(self,A=None,B=None):
        """
        Init        
          Input :
            A (float, OPTIONAL) : default 0.509 for PhreeqC
            B (float, OPTIONAL) : default 0.3283 for PhreeqC
        """
        ActivityLaw.__init__(self,A)
        
        if (B!=None):
            _typecontrol(B,[FloatType,IntType],"B coef within Debye Huckel should be a float or an int ")
            self.B = float(B)
        else:
            self.B = 0.328
            pass
        
        return
        
class DebyeHuckel(ActivityLaw):
    """
    Debye Huckel activity law
        
    """
    def __init__(self,A=None,B=None):
        """
        Init        
          Input :
            A (float, OPTIONAL) : default 0.509 for PhreeqC
            B (float, OPTIONAL) : default 0.3283 for PhreeqC
        """
        ActivityLaw.__init__(self,A)
        
        if (B!=None):
            _typecontrol(B,[FloatType,IntType],"B coef within Debye Huckel should be a float or an int ")
            self.B = float(B)
        else:
            self.B = 0.328
            pass
        
        return

    def getB(self):
        """
        Get B coefficient for ActivityLaw
          Output :
            (float)
        """
        return self.B

    def setB(self,B):
        """
        Set B coefficient for ActivityLaw
        """
        _typecontrol(B,[FloatType,IntType],"B coef within Debye Huckel should be a float or an int ")
        self.B = B

class Bdot(ActivityLaw):
    """
    Bdot activity law
    """
    def __init__(self,A=None,B=None,Bdot=None):
        """
        Init        
          Input :
            A (float, OPTIONAL) : default is 0.509 for PhreeqC
            B (float, OPTIONAL) : default is 3.283e-01 for PhreeqC
        """
        print "bddddddddddddddddddddddddddddddddddot"
        ActivityLaw.__init__(self,A)
        
        if (B!=None):
            _typecontrol(B,[FloatType,IntType],"B coef within Debye Huckel should be a float")
            self.B = float(B)
        else:
            self.B = 0.328
            pass
            
        if Bdot:
        
            if  type(Bdot) == StringType:
                self.Bdot = "co2_llnl_gamma"
                return None
            _typecontrol(Bbot,[FloatType,IntType],"the Bdot coef. within Debye huckel should be a float")
            self.Bdot = float(Bdot)
        else:
            self.Bdot = 0.0410
            pass

        return None


    def getB(self):
        """
        Return B coefficient for ActivityLaw
          Output :
            (float)
        """
        return self.B

    def getAdot(self):
        """
        Return Adot coefficient for ActivityLaw
          Output :
            (float)
        """
        return self.Adot

    def getBdot(self):
        """
        Return Bdot coefficient of the ActivityLaw instance
          Output : float 
        """
        return self.Bdot

    def setBdot(self,Bdot):
        """
        Set B coefficient for ActivityLaw
        """
        _typecontrol(Bdot,[FloatType,IntType],"B coef within Debye Huckel should be a float or an int ")
        self.Bdot = Bdot

 
## @brief WKinetic term of the  WYME kinetic law
#  @par Example of use :
#  @code
#  wkt = WKineticTerm( symbol' = 'test',
#                      power   = 1.68
#                    )
#  @encode
class WKineticTerm:
    

    ## @brief Constructor of the class
    def __init__(self,symbol,power):
        _typecontrol(symbol,[StringType]," symbol for the W kinetic term should be a string ")
        _typecontrol(power,[FloatType]," power for the W kinetic term should be a float ")
        self.symbol = symbol
        self.power = power
        return None
    
    pass

## @brief YKinetic term of the  WYME kinetic law
# @par Example of use :
# @code:
# ykt = YKineticTerm(  symbol = 'test 2',
#                      type   = 'polynomial',
#                      power1 = '1.25',
#                      power2 = '1.325'
#                   )
#  @endcode
class YKineticTerm:
    
    ## @brief Constuctor of the class
    def __init__(self,symbol,type = None,power1 = None,power2 = None):
        if type(symbol) != StringType:
            raise TypeError, " symbol for the Y kinetic term should be a string "
        if type != None:
            if type(type) != StringType:
                raise TypeError, " type for the Y kinetic term should be a string "
        if type not in ['polynomial','logarithmic']:
            self.type = "polynomial"
        else:
            self.type = type
        if power1!= None:
            if type(power1) != FloatType:
                raise TypeError, " power1 for the W kinetic term should be a float "
            self.power1 = power1
        else:
            self.power1 = 1.
        if power2!= None:
            if type(power2) != FloatType:
                raise TypeError, " power2 for the W kinetic term should be a float "
        else:
            self.power2 = 1.
        self.symbol = symbol
        return
    
    pass

## @brief MKinetic term of the  WYME kinetic law
# @par Example of use :
# @code
# mkt = MKineticTerm ( symbol  = "test",
#                      halfSat = 0.264,
#                      power1  = 1.689,
#                      power2  = 0.0125
#                    )
# @endcode
class MKineticTerm:
          
    ## @brief Constructor of the class  
    def __init__(self,symbol,halfSat,power1,power2):
        if type(symbol) != StringType:
            raise TypeError, " symbol for the M kinetic term should be a string "
        if type(halfSat) != FloatType:
            raise TypeError, " halfSat for the M kinetic term should be a float "
        if type(power1) != FloatType:
            raise TypeError, " power1 for the M kinetic term should be a float "
        if type(power2) != FloatType:
            raise TypeError, " power2 for the M kinetic term should be a float "
        self.symbol = symbol
        self.halfSat = halfSat
        self.power1 = power1
        self.power2 = power2
        return

    pass

## @brief EKinetic term of the  WYME kinetic law
# @par Example of use :
# @code
# ekt = EKineticTerm( symbol = 'test',
#                     power1 = '2.34',
#                     power2 = '5.63'
#                   )
# @endcode
class EKineticTerm:

    def __init__(self,symbol,power1,power2):
        if type(symbol) != StringType:
            raise TypeError, " symbol for the E kinetic term should be a string "
        if type(power1) != FloatType:
            raise TypeError, " power1 for the E kinetic term should be a float "
        if type(power2) != FloatType:
            raise TypeError, " power2 for the E kinetic term should be a float "
        self.symbol = symbol
        self.power1 = power1
        self.power2 = power2
        return

    pass


class WYMEKineticLaw(KineticLaw):
    
    def __init__(self,symbol, rate, surface = None,WTerm = None,YTerm = None,MTerm = None, ETerm = None,name = None,
                 nucleus = None,lawType = None):

        if not StringType(symbol):
            raise "Error with the WYME declaration"
        
        if surface.__class__.__name__  not in ["VolumicSurfaceArea",\
                            "SpecificSurfaceArea",\
                            "ConstantSurfaceArea",\
                            "SugarSurfaceArea",\
                            "CompositeSurfaceArea",\
                            "LatticeSurfaceArea",None]:
            raise " Error for surface "
        else:
            self.surface = surface
            
        self.WKineticTerm = WKineticTerm
        self.YKineticTerm = YKineticTerm
        self.MKineticTerm = MKineticTerm
        self.EKineticTerm = EKineticTerm

        self.nucleus = nucleus

        if name != None:
            _typecontrol(name,[StringType]," name of WYMEKineticLaw is not of the right type ")            
        
        if isInstance(self.surface,CompositeSurfaceArea):
            try:
                checkClassList(self.rate,[ReactionRate,SpecificReactionRate,MolalSpecificReactionRate])

            except:
                raise TypeError, "In case of Composite surface law, the rate should be given with unit mol/l/s or molal/s"
            pass
        elif (isInstance(self.surface,LatticeSurfaceArea) and self.nucleus is None):
            raise TypeError, "For a lattice surface law, you have to define a nucleus attribute (minimum surface) for the reaction"
        if ((self.nucleus is not None) and (self.surface is None)):
            raise TypeError, "You specified a minimum surface but no surface!!"
        pass

class ChemicalState:
    """
    Chemical state definition     
    """

    def __init__(self,name,aqueousSolution,
                 mineralPhase = None,
                 gasPhase = None,
                 ionicExchanger = None,
                 surfaceComplexation = None,
                 solidSolution = None,
                 phFixed = None,
		 chargeBalance = None,
		 mineralEquilibrium = None,
		 charge = None,
		 gasMassBalance = None):
        """
        Init
          Input :
            name (string)
            aqueousSolution (AqueousSolution)
            mineralPhase (MineralPhase)
            gasPhase (GasPhase)
            ionicExchanger (IonicExchangers)
            surfaceComplexation (SurfaceComplexation)
            phFixed :	tuple . 	
	    		The first component is the species to add to reach this value.           
	    		The second component is the available amount to add to reach this value.
	    		
	    		Ex: phFixed = ("HCl", 10)
	    		         
            chargeBalance :	a 2 component tuple, 
            
                        Ex: balance = ("Cl", 1.e-3)
            
	    		the first being the element to consider to achieve charge balance and           
	    		the second, the maximum of the adjustable amount to reach it.           
            mineralEquilibrium :	tuple . 	
	    		The first component is the ion to consider to reach the equilibrium in.           
	    		association with the second component which is a mineral.   
	    charge enables to use the pH as variable for balance achievement, see the phreeqC manual p. 149        
        """

#        ChemicalState.__init__(self,name)

        _typecontrol(name,[StringType]," the chemical state name must be a string ")

        self.name = name

        if aqueousSolution.__class__.__name__ != "AqueousSolution":
            raise Exception, " aqueous solution is not of the right type "
        self.aqueousSolution = aqueousSolution

        if mineralPhase:
            mineralien = [mineralPhase]
            for minerals in mineralien:
                if not isinstance(minerals,MineralPhase):
                    raise Exception, " minerals should be instances of MineralPhase "
            pass
        self.mineralPhase  = mineralPhase

        if gasPhase:
            print " gas phase ",type(gasPhase)
            print " gas phase ",gasPhase
            gazen = [gasPhase]
            for gas in gazen:
                print " gas phase ",type(gas)
                print gas
                if not isinstance(gas,GasPhase):
                    raise Exception, " gas phase has to be redefined "
            pass
        self.gasPhase  = gasPhase

        if ionicExchanger:
            ionen = [ionicExchanger]
            for ion in ionen:
                if not isinstance(ion,IonicExchangers):
                    raise Exception, " ionic exchanger has to be redefined "
            pass
        self.ionicExchanger =ionicExchanger

        if surfaceComplexation:
            flaechen = [surfaceComplexation]
            for flaeche in flaechen:
                if not isinstance(flaeche,SurfaceComplexation):
                    raise Exception, " surface complexation has to be redefined "
            pass
        self.surfaceComplexation = surfaceComplexation

        self.solidSolution = solidSolution

        _typecontrol(phFixed,[TupleType]," the pH fixed option necessitates a tuple as argument ")
        self.phFixed = phFixed
	
        _typecontrol(chargeBalance,[TupleType]," the chargeBalance option must have a tuple as argument ")
        self.chargeBalance = chargeBalance

        _typecontrol(mineralEquilibrium,[ListType]," the mineralEquilibrium option should be a list ")
        self.mineralEquilibrium = mineralEquilibrium
	
        _typecontrol(charge,[BooleanType,IntType,StringType]," the charge argument has a wrong type ")          
        self.charge = charge
        #
        # used to switch between EQUILIBRIUM_PHASES and GAS_PHASE, see the phreeqC manual
        # OK -> GAS_PHASE otherwise EQUILIBRIUM_PHASES
        #
        self.gasMassBalance = gasMassBalance
        if self.gasMassBalance == None:
            self.gasMassBalance = "no"
        return None

    def getAqueousSolution(self):
        """
        Get ChemicalState aqueous solution
          Output :
            (AqueousSolution)
        """
        return self.aqueousSolution

    def getMineralPhase(self):
        """
        Get ChemicalState mineral phase
          Output :
            (MineralPhase)
        """
        return self.mineralPhase

    def getGasPhase(self):
        """
        Get ChemicalState gas phase
          Output :
            (GasPhase)
        """
        return self.gasPhase

    def getIonicExchanger(self):
        """
        Get ChemicalState ionic exchanger
          Output :
            (IonicExchanger)
        """
        return self.ionicExchanger

    def getSurfaceComplexation(self):
        """
        Get ChemicalState surface complexation
          Output :
            (SurfaceComplexation)
        """
        return self.surfaceComplexation

    def getPhFixed(self):
        """
        Get ChemicalState fixed pH
          Output :
            (tuple , see ChemicalState for the definition)
        """
        return self.phFixed

    pass

    def getchargeBalance(self):
        """
        Get ChemicalState charge Balance
          Output :
            (tuple , see ChemicalState for the definition)
        """
        return self.chargeBalance

    def getGasMassBalance(self):
        """
        Get ChemicalState gasMassBalance option
        """
        return self.gasMassBalance


class AqueousSolution:
    """ 
    That class enables to define a ChemicalState, that means a  a pH, a pe,
    envetually a temperature and a list of Concentrations.
    Temperature default is 25 Celcius degrees.
    """
    
    def __init__(self,elementConcentrations,
                 pH=None,pe=None,Eh=None,
                 balance=None,temperature = None):

        for spezien in list(elementConcentrations):
            if spezien.__class__.__name__ != "ElementConcentration":
                raise Exception, " problem within the aqueous solution definition "
        self.elementConcentrations = elementConcentrations
        
        _typecontrol(pH,[FloatType,IntType]," the pH type is wrong it should be a float ")
        self.pH = pH
	
        _typecontrol(pe,[FloatType,IntType]," the pe type is wrong it should be a float ")            
        self.pe = pe
        
        if Eh:
            if not isinstance(Eh, ElectricPotential):
                raise Exception, " Eh must be redefined "
        self.Eh = Eh
        
        _typecontrol(balance,[StringType]," balance should be a string ")            
        self.balance = balance
	
        if temperature:
            _typecontrol(temperature,[FloatType,IntType]," temperature of the solution should be a float ")            
            self.temperature = float(temperature)
	else:
            self.temperature = temperature
            
        return
    
    def getBalance(self):
        return self.balance    
    
    def getElementConcentrations(self):
        return self.elementConcentrations

    def getpH(self):
        return self.pH

    def getpe(self):
        return self.pe

    def getEh(self):
        return self.Eh

    def getConstraints(self):
        return self.constraints

    def getSurfaceAreas(self):
        return self.SurfaceAreas

    def getTemperature(self):
        return self.temperature
    pass

class SolidSolution(Generic):
    """
    Used to define a solid solution
    """
    def __init__(self,name,minerals,
		 gugg=None,temperature = None):
        Generic.__init__(self)
	self.name = name	 
        checkClassList(minerals,[MineralTotalConcentration,MineralConcentration,TotalConcentration])
        self.mineralAmounts = minerals
	
	if gugg:
          _typecontrol(gugg,[ListType]," gugg should be a list ")            
          _typecontrol(gugg[0],[FloatType]," gugg[0] should be a float ")            
	      
	  if len(gugg)>1:
              _typecontrol(gugg[1],[FloatType]," gugg[1] should be a float ")            
	      
	  self.gugg = gugg
        _typecontrol(temperature,[FloatType]," the solidSolution temperature should be a float ")            
	self.temperature = temperature
	         
    def getMinerals(self):
        return self.minerals
	         
    def getGuggenheim(self):
        return self.gugg
	         
    def getTemperature(self):
        return self.temp
	
    pass

class MineralPhase(Generic):
    """
    Used to define the mineral phase and to
    eventually treat the pH fixed option of phreeqC
    
    example = MineralPhase ([   TotalConcentration("quartz", 16.64, "mol/l"),
                                TotalConcentration("calcite", 9.99, "mol/l")], phFixed=("HCl",10.0))
    """
    def __init__(self,minerals,
		 phFixed=None):
        Generic.__init__(self)
        checkClassList(minerals,[MineralTotalConcentration,TotalConcentration])
        self.minerals = minerals
	
        _typecontrol(phFixed,[TupleType]," the pH fixed option requires a tuple element and quantity as option ")            
        self.phFixed  = phFixed
      
    def getMinerals(self):
        """
        to get the list of mineral phases associated to the chemical state
        """
        return self.minerals
	
    def getphFixed(self):
        return self.pHfixed

    pass

class GasPhase:
    """
    Definition of a gaseous phase
    """
    def __init__(self,gas):
        checkClassList(gas, Fugacity)
        self.gas = gas
        return None

    def append(self,aGas):
        self.gas.append(aGas)

    def getGas(self):
        return self.gas

    pass

class IonicExchangers:
    """Definition of a ionic exchanger"""
    def __init__(self,exchangers):
        for ionicexchangers in exchangers:
            if not isInstance(ionicexchangers,[ExchangeBindingSpecies,ExchangeMineralBindingSpecies]):
                raise Exception, "ExchangeBindingSpecies must be redefined"
	    pass
        self.exchangers = exchangers
        return

    def getExchangers(self):
        return self.exchangers

    pass

class SurfaceComplexation:
    """Definition of a surface complexation"""
    def __init__(self,surfaces):
        checkClassList(surfaces,
                        [SurfaceBindingSpecies,SurfaceMineralBindingSpecies])
        self.surfaces = surfaces
        return


    def getSurfaces(self):
        return self.surfaces

    pass

class ExchangeBindingSpecies(Species):
    """ This class can be used to characterise the quantity of exchange species in moles"""
    def __init__(self,symbol,exchangeAmount):

        Species.__init__(self,symbol)

        if not isinstance(exchangeAmount,MolesAmount):
            if not isinstance(exchangeAmount,Moles):
                raise Exception, "exchange amount must be redefined "
        self.exchangeAmount = exchangeAmount
    
    def getExchangeAmount(self):
        return self.exchangeAmount

class ExchangeMineralBindingSpecies(Species):
    """ This class can be used to characterise the mineral bounded to
    the exchange site and the number of moles per  moles of mineral
    """
    def __init__(self,symbol,mineral,exchangePerMole):

        Species.__init__(self,symbol)

        _typecontrol(exchangePerMole,[FloatType]," exchangepermole argument within ExchangeMineralBindingSpecies hasn't the right type ")            
        self.exchangePerMole = exchangePerMole
        
        _typecontrol(mineral,[StringType]," mineral arg. within ExchangeMineralBindingSpecies hasn't the right type")            
        
        self.mineral = mineral

    def getmineralphasename(self):
        return self.mineral
    
    def getExchangePerMole(self):
        return self.exchangePerMole
    
class SurfaceBindingSpecies(Species):

    """ This class can be used to characterise the quantity of exchange species in moles"""
    
    def __init__(self,symbol,sites,specificAreaPerGram=None,mass=None):

        Species.__init__(self,symbol)
	
	if not isinstance(sites,MolesAmount):
	    raise Exception, " SurfaceBindingSpecies must be redefined"
	self.sites = sites
	
	if specificAreaPerGram:
	    if not isinstance(specificAreaPerGram,SpecificAreaPerGram):
	        raise Exception, "specificAreaPerGram must be redefined"
	self.specificAreaPerGram = specificAreaPerGram
	
	if mass:
	    if not isinstance(mass,Mass):
	        raise Exception, "mass for %smust be redefined" %(symbol)
        self.mass = mass
    
    def getSites(self):
        return self.sites
    
    def getSpecificAreaPerGram(self):
        return self.specificAreaPerGram
    
    def getMass(self):
        return self.mass

class SurfaceMineralBindingSpecies(Species):
    """ This class can be used to characterise the mineral bounded to
    the exchange site and the number of moles per  moles of mineral
    """
    def __init__(self,symbol,mineral,sitesPerMole,specificAreaPerMole=None):

        Species.__init__(self,symbol)
        
        _typecontrol(mineral,[StringType]," mineral arg. within SurfaceMineralBindingSpecies hasn't the right type")            
        self.mineral = mineral

        _typecontrol(sitesPerMole,[FloatType]," sitesPerMole arg within SurfaceMineralBindingSpecies should be a float ")            
        self.sitesPerMole = sitesPerMole

	if specificAreaPerMole:
            if not isinstance(specificAreaPerMole,SpecificAreaPerMole):
                raise Exception, " specificAreaPerMole must be redefined "
        self.specificAreaPerMole = specificAreaPerMole

    def getmineralphasename(self):
        return self.mineral
    
    def getSitesPerMole(self):
        return self.sitesPerMole

    def getSpecificAreaPerMole(self):
        return self.specificAreaPerMole


#---------------
# Chemical Problem
#---------------

class ChemicalProblem:
    """
    Chemical problem Definition

    """

    def __init__(self,
                 name,
                 chemistryDB,
                 chemicalState,
                 speciesBaseAddenda=None,
                 kineticLaws =  None,
                 activityLaw = None,
                 timeStep=None,
                 outputs=None):
        """
        Init
        
          Input :
            name (string)
            dB (string) : it can be a name (in this case we automatically choose
                           the correct file for chess or phreeqc) or a URL
            speciesBaseAddenda (list of Species, OPTIONAL)
            kineticLaws (list of KineticLaw, OPTIONAL)
            activityLaw (list of ActivityLaw, OPTIONAL)
            timeStep (Time, OPTIONAL) : only if kinetic
            outputs (list of ExpectedOutput, OPTIONAL)

          Examples :
        """

        _typecontrol(name,[StringType]," name within ChemicalProblem should be a string ")            
        self.name = name.replace(" ","")
        
        _typecontrol(chemistryDB,[StringType]," dB within ChemicalProblem should be a string ")            
        self.dtb = chemistryDB
        
        if not isinstance(chemicalState,ChemicalState):
            raise Exception, "the chemical state must be redefined"
        self.chemicalState = chemicalState
                 
        if speciesBaseAddenda:
            checkClassList(speciesBaseAddenda, [Salt,Species])    
        self.speciesBaseAddenda = speciesBaseAddenda

        if kineticLaws:
            checkClassList(kineticLaws,KineticLaw)
        self.kineticLaws = kineticLaws
         
        if activityLaw:
            if not isinstance(activityLaw,ActivityLaw):
                raise Exception, " problem with the default activity law definition"
        self.activityLaw = activityLaw
##        else:
##            self.activityLaw = Davies()
 
        if timeStep:
            if not isinstance(timeStep,Time):
                raise Exception, " timeStep instance has to be redefined"
        self.timeStep = timeStep

        if outputs:
            checkClassList(outputs,ExpectedOutput)
        self.outputs =  outputs

    def getName(self):
        return self.name
    
    def getDB(self):
        return self.dtb
    
    def getDTB(self):
        return self.dtb
   
    def getSpeciesBaseAddenda(self):
        return self.speciesBaseAddenda
        
    def getKineticLaws(self):
        """
        Get ChemicalProblem kinetic laws 
        """
        return self.kineticLaws
        
    def getActivityLaw(self):
        return self.activityLaw
        
    def getChemicalState(self):
        return self.chemicalState
        
    def getTimeStep(self):
        return self.timeStep
        
    def getOutputs(self):
        return self.outputs
   
    def setSpeciesBaseAddenda(self,speciesBaseAddenda):
        self.speciesBaseAddenda = speciesBaseAddenda

#-------------------------------------------
# ExpectedOutput for transport and chemical 
#------------------------------------------
class ExpectedOutput(CommonExpectedOutput):
    """
    ExpectedOutput definition
    
    
      Input :
      
        quantity (string) : pH, pe, Eh, IonicStrength, Concentration, Activity,
                            TotalConcentration, AqueousTotalConcentration,
                            FixedTotalConcentration, numerics
                            
        unknown (string, OPTIONAL) : name of a species, needed if quantity is Concentration ...
        
        unit (string, OPTIONAL) : unit for the quantity, default is molal
        
        support (Support or  CartesianMesh) :
          is not specified support is full computaional domain
          
        timeSpecification (TimeSpecification, OPTIONAL) : is not specified all computational time

        
        format (string between 'field' or 'table') : default is field

        save (string between 'file' or 'memory') : default is memory


        name (string) : default is quantity_unknown_unit
        """
    def __init__(self, quantity = None, unknown = None, unit = None,
                 support = None, timeSpecification = None,  format = None, save = None, name = None):
        alltype = ['pH', 'pe', 'Eh', 'IonicStrength', 'Concentration', 'Temperature',
                   'Activity','TotalConcentration', 'AqueousTotalConcentration','AqueousConcentration','MineralPhaseConcentration'
                   'FixedTotalConcentration', 'numerics', 'porosity']
        facetype = []
	
        if quantity == None:
	    quantity = 'Concentration'
	elif quantity == 'concentration':
	    quantity = 'Concentration'
	    pass

        CommonExpectedOutput.__init__(self, alltype, facetype,quantity, support,
                                      name , unit, timeSpecification, None, unknown, save, 1)
	    
        if format:
            if format not in ['field',"table",]: raise Exception, "the ExpectedOutput format must be of type \"field\" or \"table\""
            self.format = format
        else:
            self.format = 'field'
            pass
        
        self.chemicalName = quantity
        
        if unknown:
            self.chemicalName += '_' + unknown
            pass

        if unit:
            self.chemicalName += '_' + unit
            pass

        if not name:
            self.name =  self.chemicalName
            pass
                
        return

    def getFormat(self):
        """
        Get ExpectedOutput format: a string: 'table' or 'field'
        """
        return self.format

    def getSave(self):
        """
        Get ExpectedOutput save mode: a string: 'memory' or 'file'
        """
        return self.save

    def getName(self):
        return self.name

    def getChemicalName(self):
        return self.chemicalName
 
    pass
    
def _typecontrol(obj,typListe,message):
    if obj:
            if type(obj) not in  typListe:
                raise TypeError, message

