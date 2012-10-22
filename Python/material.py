""" Material class """

from types import FloatType,IntType,ListType,StringType,TupleType
#
from generictools import memberShip

from listtools import toList
#
from generictools import isInstance
#
from PhysicalQuantities import Scalar
#
from PhysicalQuantities import PhysicalQuantity as PQuantity
#
from PhysicalProperties import AquiferProperty
from PhysicalProperties import BiotCoefficient
from PhysicalQuantities import Concentration
from PhysicalProperties import Density
from PhysicalProperties import Dilatation
from PhysicalProperties import EffectiveDiffusion
from PhysicalProperties import HydraulicConductivity
from PhysicalProperties import HydraulicPorosity
from PhysicalProperties import IntrinsicPermeability
from PhysicalProperties import KinematicDispersion
from PhysicalProperties import MassSolubilityLimit
from PhysicalProperties import MatrixCompressibilityFactor
from PhysicalProperties import Permeability
from PhysicalProperties import PoreDiffusion
from PhysicalProperties import Porosity
from PhysicalProperties import RetardationFactor
from PhysicalProperties import ResidualSaturation
from PhysicalProperties import ResidualWaterContent
from PhysicalProperties import MaximumSaturation
from PhysicalProperties import SaturatedWaterContent
from PhysicalProperties import SharedFactor
from PhysicalProperties import SolidDensity
from PhysicalProperties import SolubilityLimit
from PhysicalProperties import SpecificHeat 
from PhysicalProperties import SpecificHeatCapacity
from PhysicalProperties import SpecificStorage
from PhysicalProperties import ThermalConductivity
from PhysicalProperties import Viscosity

from physicallaws import PermeabilityLaw, SolubilityLaw
from physicallaws import SaturationLaw, SolubilityByIsotope
from physicallaws import SorptionLaw,PhysicalLaw
from physicallaws import Freundlich, Langmuir, DistributionCoefficient
from species import createList

from physicallaws import IntrinsicPermeabilityLaw,FickVapeurLaw,FickAirDissousLaw,ThermalconductivityLaw

# =========================================================
# Material
# =========================================================

class Material:

    """A material support a list of physical quantities.
    
    """
    def __init__(self, name,**properties):
        """
        properties can be among :
        
        biotCoefficient ,
        concentrationAtSaturation,
        density,
        effectiveDiffusion,
        fickairdissouslaw ,
        fickvapeurlaw,
        hydraulicConductivity,
        hydraulicPorosity,
        intrinsicpermeability,
        intrinsicpermeabilitylaw, 
        kinematicDispersion,
        massSolubilityLimit,
        matrixcompressibilityfactor,
        masse_volumique_homogen, 
        maximumSaturation,
        permeability,
        permeabilityLaw,
        permeabiliteliquide ,
        permeabilitegaz 
        poreDiffusion,
        porosity,
        retardationFactor,
        residualSaturation,
        residualWaterContent,
        saturationLaw,
        saturatedWaterContent,
        sharedFactor,
        solidDensity,
        solubilityLaw,
        sorptionLaw,
        specificHeat, 
        SpecificStorage,
        thermalconductivitylaw
        viscosity
        
        Rem:    The property dictionnary contains only properties as strings with lower cases. It
                allows to better handle the properties naming.
        """
        
        try:
            type(name) is StringType
        except:
            raise TypeError, " name must be a string"
        self.name = name
        #
        self.propdict={
            
            'biotcoefficient':BiotCoefficient,
            'concentrationatsaturation':Concentration,
            'density':Density,
            'effectivediffusion':EffectiveDiffusion,
            'fickairdissouslaw':FickAirDissousLaw,
            'fickvapeurlaw':FickVapeurLaw,
            'hydraulicconductivity':HydraulicConductivity,
            'hydraulicporosity':HydraulicPorosity,
            'intrinsicpermeability':IntrinsicPermeability,
            'intrinsicpermeabilitylaw':IntrinsicPermeabilityLaw,
            'kinematicdispersion':KinematicDispersion,
            'masssolubilitylimit':MassSolubilityLimit,
            'matrixcompressibilityfactor':MatrixCompressibilityFactor,
            'masse_volumique_homogen':SolidDensity,
            'maximumsaturation':MaximumSaturation,
            'permeability':Permeability,
            'permeabilitylaw':PermeabilityLaw,
            'permeabiliteliquide':PermeabilityLaw,
            'permeabilitegaz':PermeabilityLaw,
            'porediffusion':PoreDiffusion,
            'porosity':Porosity,
            'retardationfactor':RetardationFactor,
            'residualsaturation':ResidualSaturation,
            'residualwatercontent':ResidualWaterContent,
            'saturatedwatercontent':SaturatedWaterContent,
            'saturationlaw':SaturationLaw,
            'sharedfactor':SharedFactor,
            'soliddensity':SolidDensity,
            'solubilitylaw':SolubilityLaw,
            'sorptionlaw':SorptionLaw,
            'specificstorage':SpecificStorage,
            'specificheat':SpecificHeat,
            'thermalconductivity':ThermalConductivity,
            'thermalconductivitylaw':ThermalconductivityLaw,
            'viscosity':Viscosity
            }
        for physicalproperty in self.propdict.values():
            if not (issubclass(physicalproperty,PhysicalLaw)+issubclass(physicalproperty,PQuantity)+issubclass(physicalproperty,AquiferProperty)):
                raise Exception, " check the class for %s"%(physicalproperty)
            pass
        self.density = None
        self.effectiveDiffusion_species =None
        self.effectiveDiffusion_property= None
        self.kinematicDispersion_species = None
        self.kinematicDispersion_property = None         
        self.residualSaturation = None
        self.maximumSaturation = None
        self.residualWaterContent = None
        self.saturatedWaterContent = None
        self.permeability = None
        self.permeabilityLaw = None
        self.intrinsicPermeability = None
        self.poreDiffusion_species = None
        self.poreDiffusion_property = None
        self.hydraulicConductivity = None
        self.hydraulicPorosity = None
	self.viscosity = None
        self.porosity_species = None
        self.porosity_property = None        
        self.retardationFactor_species = None
        self.retardationFactor_property = None
        self.sharedFactor_species = None
        self.sharedFactor_property = None
        self.saturationLaw = None
        self.solidDensity = None
##        self.solubilityLaw = None
        self.solubilityLaw_species = None
        self.solubilityLaw_property = None
        self.sorptionLaw_species = None
        self.sorptionLaw_property = None
        self.specificStorage = SpecificStorage(1.)
        self.matrixCompressibilityFactor = None
        self.massSolubilityLimit_species = None
        self.massSolubilityLimit_property = None
        self.concentration_species = None
        self.concentration_property = None
        #Ajouts TH
        self.fickVapeurLaw = None
        self.fickAirDissousLaw = None
        self.thermalconductivityLaw= None
        self.intrinsicPermeabilityLaw =  None
        self.biotCoefficient = None
        self.specificHeatCapacity =  None
        self.thermalConductivity =  None
        self.permeabiliteliquide = None
        self.permeabilitegaz = None

        for key in properties:
            #print "key",key,type(key)
            prop=properties[key]
            #print "prop",prop,dir(prop)
            self.setProperty(key,prop)
            pass
        # self.setProperty affecte 2 fois self.permeabilityLaw
        # d'abord a permeabiliteliquide puis  a permeabilitegaz
        # car propdict(permeabiliteliquide) = PermeabilityLaw  et propdict(permeabiliteliquide)= PermeabilityLaw
        # On contourne ce pb
        if properties.has_key('permeabiliteliquide'):
            self.permeabiliteliquide = properties["permeabiliteliquide"]
        if properties.has_key('permeabilitegaz'):
            self.permeabilitegaz = properties["permeabilitegaz"]
        #
        # if saturation is introduced we also set water contents through
        # the residual and maximum of saturation, and porosity
        #
        if properties.has_key("maximumsaturation"):
            if properties.has_key("porosity"):
                self.saturatedWaterContent = self.porosity * self.maximumSaturation
            else:
                raise Warning," constitency problem "
            if properties.has_key("residualsaturation"):
                self.residualWaterContent = self.porosity * self.residualSaturation

        elif properties.has_key("saturatedwatercontent"):
            if properties.has_key("porosity"):
                self.maximumSaturation = self.saturatedWaterContent / self.porosity
            else:
                raise Warning," constitency problem "
            if properties.has_key("residualsaturation"):
                self.maximumSaturation = self.saturatedWaterContent / self.porosity

                
            
        
        # Verification that both permeability and
        # intrinsicpermeability have not been set
        if (self.permeability and self.intrinsicPermeability):
            raise Exception, "Material with both permeability and intrinsic permeability can't be defined"

        #verification that both PoreDiffusion and EffectiveDiffusion
        #have not been set
        print " dbg material we are here "
        if (self.effectiveDiffusion_species and  self.poreDiffusion_species):
            raise Exception, "Material with both effectiveDiffusion and poreDiffusion can't be defined"

        # verification that if DistributionCoefficient, langmuir
        # or freundlich sorptionLaw is defined, solidDensity
        # should be set     
        if self.sorptionLaw_species:
            for prop in self.sorptionLaw_property:
                if isInstance(prop, [DistributionCoefficient, Langmuir, Freundlich]):
                    if not self.solidDensity:
                       raise Exception, "Material defined with DistributionCoefficient, langmuir or freundlich sorptionLaw should also be defined with solidDensity"
                    pass
                pass
            pass
        return
                
    def setEffectiveDiffusion(self,effectiveDiffusion):
        """set effectivediffusion property"""
        self.setProperty('EffectiveDiffusion',effectiveDiffusion)

    def changeProperty(self,PQ,value):
        """
        Change a material property value
        """
        if not issubclass(PQ,PhysicalLaw)+issubclass(PQ,PQuantity)+issubclass(PQ,AquiferProperty):
            raise Exception, "problem with class membership"
        key=PQ.__name__
#        print "dbg material changeProperty",PQ.__name__
        key=key[0].lower()+key[1:]
        print " dbg material key",key
        
        if hasattr(self,key):
            # property of the material only
            setattr(self,key,value)
        elif hasattr(self,key+'_species') and hasattr(self,key+'_property'):
            if not value:
                setattr(self,key+'_species',None)
                setattr(self,key+'_property',None)
                return
            # property depending on the material and species
##             print 'Classe :',PQ.__name__
            spec_list,prop_list=createList(value,PQ)
            spec_aux,prop_aux=getattr(self,key+'_species'),\
                               getattr(self,key+'_property')
            if not spec_aux:
                spec_aux=[]
            if not prop_aux:
                prop_aux=[]
            if len(spec_list)==1:
                if spec_list[0]!='ALL':
                    raise Exception
                spec_aux,prop_aux=spec_list,prop_list
            else:
                if len(spec_aux)==1:
                    if spec_aux[0]!='ALL':
                        raise Exception
                for spe in spec_list:
                    indexlist=spec_list.index(spe)
                    prop=prop_list[indexlist]
                    if spe in spec_aux:
                        indexaux=spec_aux.index(spe)
                        prop_aux[indexaux]=prop
                    else:
                        spec_aux.append(spe)
                        prop_aux.append(prop)
                        pass
                    pass
                pass
            setattr(self,key+'_species',spec_aux)
            setattr(self,key+'_property',prop_aux)
##             print key+'_species :',spec_aux
##             print key+'_property:',prop_aux
            pass
        else:
            raise Exception
        return

    def setProperty(self,keyword,property):
        """
        To set a material property
        """
        print "keyword",keyword
        keyword=keyword.lower()
        if keyword not in self.propdict.keys(): raise Exception, " check the set property function, property: "+keyword
        print "dbg property: ",keyword,property.__class__
        if isInstance(property,[PhysicalLaw,PQuantity,AquiferProperty]):
            print "setproperty propClass is ok "
            propClass=property.__class__
            pass
        elif type(property) is ListType:
            #
            # \begin{E.A.}[to allow : "Si", Prop('4.5), "Toto", Prop(5.4), ...]
            #
            # the usual way to do setProperty with a list is like that :
            # [Prop(4.5), ("toto", Prop(3.4)), ("titi", Prop(4.5))]
            # if I receive :
            # ["Si", Prop('4.5), "Toto", Prop(5.4)]
            # I transform this list in
            # [("Si", Prop('4.5)), ("Toto", Prop(5.4))]
            #
            myProperty = []
            aNewProp = []
            for prop in property:
                if len(aNewProp)==1:
                    aNewProp.append(prop)
                    myProperty.append(tuple(aNewProp))
                    aNewProp = []
                    pass
                from types import StringType
                if type(prop, StringType):
                    if len(aNewProp) != 0:
                        message  = "\n\n"
                        message += "Exception catched\n"
                        message += "to improve ...\n"
                        raise Exception(message)
                    aNewProp.append(prop)
                    pass
                pass
            if myProperty:
                property = myProperty
                pass
            #
            #
            property_buf = []
            for prop in property:
                if isInstance(prop,[PhysicalLaw,PQuantity,AquiferProperty]):
                    property_buf.append(prop)
                    pass
                elif type(prop,TupleType):
                    if isInstance(prop[0],[AquiferProperty,PhysicalLaw,PQuantity]):
                        property_buf.append(prop)
                    else:
                        property_buf.append((prop[1],prop[0]))
                        pass
                    pass
                else:
                    raise Exception, "object membership should be verified : %s"%prop
                pass
            property = property_buf
            for prop in property:
                if isInstance(prop,[AquiferProperty,PhysicalLaw,PQuantity]):
                    propClass=prop.__class__
                    pass
                elif type(prop,TupleType):
                    memberShip(prop[0],[AquiferProperty,PhysicalLaw,PQuantity])
                    propClass=prop[0].__class__
                    if propClass==self.propdict[keyword]:
                        PQ=propClass
                    elif issubclass(propClass,self.propdict[keyword]):
                        PQ=self.propdict[keyword]
##                        if propClass=='SolubilityByElement':
##                            print 'houla element'
##                            flag='SolubilityByElement'
                        pass
                        
                    key=PQ.__name__
                    key=key[0].lower()+key[1:]
                    if not hasattr(self,key+'_species'):
                        raise Exception, "No species allowed for %s"%key
                    pass
                else:
                    raise Exception, "object membership should be verified : %s"%prop
                pass
            pass
        else:
            if property:
                raise Exception, "object membership should be verified : %s"%property
            else:
                propClass=self.propdict[keyword]
        #propClass=property.__class__
#        print " dbg keyword ",keyword
#        print " dbg propClass ",propClass
#        print " dbg propdict ",self.propdict[keyword]
        if propClass!=self.propdict[keyword]:
            if not issubclass(propClass,self.propdict[keyword]):
                raise Exception, " problem with property class "
        #self.changeProperty(propClass,property)
        self.changeProperty(self.propdict[keyword],property)
        

    def getProperty(self,keyword, species_or_elem = None, list_elements = []):
        """
        Enables to get a material property
        """
        value = None
        keyword = keyword.lower()
        if keyword not in self.propdict.keys():
            raise Exception, " check the get property function property: "+keyword
        PQ = self.propdict[keyword]
        key = PQ.__name__
        key = key[0].lower()+key[1:]
        if hasattr(self,key):
            # property of the material only
            return getattr(self,key)
        elif hasattr(self,key+'_species') and hasattr(self,key+'_property'):
            spec_aux,prop_aux=getattr(self,key+'_species'),getattr(self,key+'_property')
            if spec_aux:
                if species_or_elem:
                    for spe in spec_aux:
                        if spe == species_or_elem:
                            indexaux = spec_aux.index(spe)
                            return prop_aux[indexaux]
                        pass
                    for el in list_elements:
                        isotopes = [x.lower() for x in el.getIsotopesNames()]
                        if species_or_elem.lower() in isotopes:
                            return None
                        pass
                    pass
                return prop_aux[0]
                #pass
                pass
            pass
        return value

    def hasProperty(self,keyword):
        """
        returns 1 if the property is
        defined for the material, and 0 if not.
        """
        boolean=0
        keyword = keyword.lower()
        if keyword not in self.propdict.keys(): raise Exception, " check the set property function "
        PQ = self.propdict[keyword]
        key = PQ.__name__
        key = key[0].lower()+key[1:]
        if hasattr(self,key) or hasattr(self,key+'_species'):
            boolean = 1
        return boolean

    def setResidualSaturation(self,residualSaturation):
        """
        That function enables to set the liquid residual saturation property
        """
        memberShip(residualSaturation, ResidualSaturation)
        self.residualSaturation = residualSaturation


    def setResidualWaterContent(self,residualWaterContent):
        """
        That function enables to set the liquid residual water content property
        """
        memberShip(residualWaterContent, ResidualWaterContent)
        self.residualWaterContent = residualWaterContent
        
    def setMaximumSaturation(self, maximumSaturation):
        """
        That function enables to set the liquid saturated  property
        """
        memberShip(maximumSaturation, MaximumSaturation)
        self.maximumSaturation = maximumSaturation
        
    def setSaturatedWaterContent(self, saturatedWaterContent):
        """
        That function enables to set the liquid saturated  property
        """
        memberShip(saturatedWaterContent, saturatedWaterContent)
        self.saturatedWaterContent = residualWaterContent
        
    def setPermeability(self,permeability):
        """set permeability property"""
        memberShip(permeability, Permeability)
        self.permeability = permeability
        
    def setPermeabilityLaw(self,permeabilityLaw):
        """set permeability law"""
        isinstance(permeabilityLaw, PermeabilityLaw)
        self.permeabilityLaw = permeabilityLaw

    def setIntrinsicPermeability(self,intrinsicpermeability):
        """set intrinsic permeability"""
        memberShip(intrinsicpermeability, IntrinsicPermeability)
        self.intrinsicPermeability = intrinsicpermeability
        
    def setPoreDiffusion(self,poreDiffusion ):
        """set pore diffusion"""
        self.setProperty('PoreDiffusion',poreDiffusion)
        
    def setPorosity(self,porosity):
        """set porosity"""
        self.setProperty('Porosity',porosity)
        
    def setViscosity(self,viscosity):
    	"""set viscosity"""
    	self.setProperty('Viscosity',viscosity)
        
    def setHydraulicPorosity(self,porosity):
        """set hydraulic porosity"""
        self.setProperty('hydraulicPorosity',porosity)
 
        
    def setRetardationFactor(self,retardationFactor):
        """set retardation factor"""
        retardationFactor_species, retardationFactor_property = createList(retardationFactor, RetardationFactor)
        if not self.retardationFactor_species:
            self.retardationFactor_species=[]
        if not self.retardationFactor_property:
            self.retardationFactor_property=[]
        self.retardationFactor_species += retardationFactor_species
        self.retardationFactor_property += retardationFactor_property
        #raise stop

    def setSaturationLaw(self,saturationLaw):
        """set saturation law"""
        memberShip(saturationLaw, SaturationLaw)
        self.saturationLaw = saturationLaw
        
    def setSolidDensity(self,solidDensity):
        """set solid density"""
        memberShip(solidDensity, SolidDensity)
        self.solidDensity = solidDensity
                
    def setSolubilityLaw(self,solubilityLaw):
        """set solubility law"""
        self.setProperty('solubilityLaw',solubilityLaw)
##         memberShip(solubilityLaw, SolubilityLaw)
##         self.solubilityLaw = solubilityLaw

    def setSorptionLaw(self,sorptionLaw):
        """set sorption law"""
        self.setProperty('sorptionLaw',sorptionLaw)
        
    def setSpecificStorage(self,SpecificStorage):
        """set SpecificStorage"""
        memberShip(SpecificStorage, SpecificStorage)
        self.specificStorage = SpecificStorage

    def getEffectiveDiffusion(self, species = None):
        """if effectiveDiffusion is defined :
               if a species is specified,
                   return the associated property value
               else return the default value
           else return None"""
        return self.getProperty('effectiveDiffusion', species)

    def setKinematicDispersion (self,kinematicDispersion):
        """ set kinematic dispersion"""
        self.setProperty('KinematicDispersion',kinematicDispersion)
        

    def setMatrixCompressibilityFactor(self,matrixCompressibilityFactor):
        """set MatrixCompressibilityFactor"""
        memberShip(matrixCompressibilityFactor,MatrixCompressibilityFactor)
        self.matrixCompressibilityFactor=matrixCompressibilityFactor
        return
    
    def getKinematicDispersion (self, species = None):
        """if KinematicDispersion is defined :
               if a species is specified,
                   return the associated property value
               else return the default value
           else return None"""
        return self.getProperty('KinematicDispersion', species )
        
    def getResidualWaterContent(self):
        """
        That function enables to retrieve the residual Saturation
        In Elmer it is named "Residual Water Content"
        """
        return self.getProperty('residualWaterContent')
        
    def getSaturatedWaterContent(self):
        """
        That function enables to retrieve the saturated water content
        In Elmer it is named "Saturated Water Content"
        """
        return self.getProperty('saturatedWaterContent')
    
    def setName(self,name):
        """ set material name"""
        self.name=name

    def getName(self):
        """get material name"""
        return self.name
    
    def getPermeability(self):
        """get permeability"""
        return self.getProperty('permeability')

    def getHydraulicConductivity(self):
        """get HydraulicConductivity"""
        return self.getProperty('HydraulicConductivity')

    def getPermeabilityLaw(self):
        """get permeability law"""
        return self.getProperty('permeabilityLaw')

    def getIntrinsicPermeability(self):
        """get intrinsic permeability"""
        return self.getProperty('intrinsicpermeability')

    def getPoreDiffusion(self, species = None):
        """if PoreDiffusion is defined :
               if a species is specified,
                   return the associated property value
               else return the default value
           else return None"""
        return self.getProperty('PoreDiffusion', species)
    
    def getPorosity(self, species = None):
        """if Porosity is defined :
               if a species is specified,
                   return the associated property value
               else return the default value
           else return None"""
        return self.getProperty('Porosity', species)
        
    def getViscosity(self):
        """if Viscosity is defined :
               return the associated property value
           else return None"""
        return self.getProperty('Viscosity')
    
    def getHydraulicPorosity(self):
        """get hydraulic porosity """
        return self.getProperty('hydraUlicpoRosity')
    

    def getRetardationFactor(self, species = None):
        """if RetardationFactor is defined :
               if a species is specified,
                   return the associated property value
               else return the default value
           else return None"""

        return self.getProperty('retardationFactor', species)

    def getSaturationLaw(self):
        """get saturation law"""
        return self.getProperty('SaturationLaw')
    
    def getSolidDensity(self):
        """get solid density"""
        return self.getProperty('solidDensity')
        
    def getBiotCoefficient(self):
        """ get BiotCoefficient """
        return self.getProperty('coefficientbiot')
        
    def getSpecificHeat(self):
        """ get specific Heat Capacity """
        return self.getProperty('specificHeat')
        
    def getThermalConductivity(self):
        """ get thermal conductivity """
        return self.getProperty('thermalconductivity')
        
    def getSolubilityLaw(self, species_or_elem = None, list_elements = []):
        """get solubility law"""
        return self.getProperty('solubilityLaw', species_or_elem, list_elements)

    def getSorptionLaw(self, species = None):
        """get sorption law"""
        return self.getProperty('sorptionLaw', species)

    def getSpecificStorage(self):
        """get specific storage coefficient"""
        return self.getProperty('SpecificStorage')

    def getMatrixCompressibilityFactor(self):
        """get matrix compressibility factor"""
        return self.getProperty('matrixCompressibilityFactor')

    def getFickVapeurLaw(self):
        return self.fickVapeurLaw
        
    def getFickAirDissousLaw(self):
        return self.fickAirDissousLaw
        
    def getThermalConductivityLaw(self):
        return self.thermalconductivityLaw
        
    def getIntrinsicPermeabilityLaw(self):
        return self.intrinsicPermeabilityLaw
        
    def getPermeabiliteLiquide(self):
        return self.permeabiliteliquide
        
    def getPermeabiliteGaz(self):
        return self.permeabilitegaz


    def arePropertiesSetted(self,species,*keywords):
        """check if properties are set or not for species"""
        for keyword in keywords:
            if not self.getProperty(keyword,species):
                return 0
            pass
        return 1

    def verifyPropertiesAreSetted(self,species,*keywords):
        """raise an exception if properties are not set for species"""
        for keyword in keywords:
            if not self.getProperty(keyword,species):
                msg=keyword+\
                     ' is not set for material %s'\
                     %self.getName()
                print msg
                raise Exception, msg
