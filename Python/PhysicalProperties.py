#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import print_function
from generictools import memberShip

from PhysicalQuantities import _findUnit,\
                               PhysicalQuantity,\
                               Scalar,\
                               Tensor,\
                               Vektor

from exceptions import Warning

from tensors import IsotropicTensor

from types import FloatType, IntType, NoneType
import six

class AquiferProperty:
    """
    class enabling to treat dimensionless aquifer properties
    """
    
    def __init__(self, unit=''):
        """         
        """    
        self.unit = None
        return
    
    def getDefaultUnit(self):
        return None

    def getUnit(self):
        return None
    
class AquiferPropertyScalar(AquiferProperty):
    """
    A scalar single value (float or int)
    """
    def __init__(self, value):
        AquiferProperty.__init__(self)
        self.checkValue(value)
        return
    
    def checkValue(self, value):
        valueOK=0
        try:
            if type(value) not in [FloatType,IntType]:
                raise Exception("value should be a float")
            value = float(value)
            valueOK = 1
            pass
        except TypeError:
            pass
        if not valueOK:
            try:
                memberShip(value, [Field, LinearFunction,TimeTabulatedFunction,\
                                   SpaceAndTimeTabulatedFunction,\
                                   PolynomialFunction,TimeFunction])
                valueOK = 1
                pass
            except TypeError:
                pass
            pass
        if not valueOK:
            raise Exception("physical quantity can\"t be defined, see the value %s"%(value))
        self.value = value
        return
    
    def getValue(self):
        return self.value
    
    def setValue(self, value):
        self.verifyValue(value)
        self.value = value
        return

class SolidProperty:
    """
    class enabling to treat rock properties
    A dimension can be introduced like for expansivity or compressibility
    """
    
    def __init__(self, value, unit = None):
        """         
        """    
        self.value = value
        self.unit = unit
        return None

    def getUnit(self):
        return self.unit
    
class SolidPropertyScalar(SolidProperty):
    """
    A scalar single value (float or int)
    """
    def __init__(self, value,unit = None):
        SolidProperty.__init__(self, value, unit)
        self.checkValue(value)
        return
    
    def checkValue(self, value):
        valueOK=0
        try:
            if type(value) not in [FloatType,IntType]:
                raise Exception("value should be a float")
            value = float(value)
            valueOK = 1
        except TypeError:
            pass
        if not valueOK:
            try:
                memberShip(value, [Field, LinearFunction,TimeTabulatedFunction,\
                                   SpaceAndTimeTabulatedFunction,\
                                   PolynomialFunction,TimeFunction])
                valueOK = 1
                pass
            except TypeError:
                pass
            pass
        if not valueOK:
            raise Exception("physical quantity can\"t be defined, see the value %s"%(value))
        self.value = value
        return
    
    def getValue(self):
        return self.value
    
    def setValue(self, value):
        self.verifyValue(value)
        self.value = value
        return

class BiotCoefficient(Scalar):
    """
    """
    default_unit = None
    pass

class Density(Scalar):
    """
    In physics, the density of a body is the measure of how tightly the matter within it is packed together.
    """
    default_unit = _findUnit('Density')
    pass

class ElectricPotential(Scalar):
    default_unit = _findUnit('ElectricPotential')
    pass

class FlowRate(Scalar):
    default_unit = _findUnit('FlowRate')
    pass

class PoissonRatio(SolidPropertyScalar):
    """
    Is the negative ratio of transverse to axial strain
    """
    def __init__(self,value):
        SolidPropertyScalar.__init__(self,value)
    
class SaturationDegree(Scalar):
    default_unit = None
    def verifyValue(self, value):
        Scalar.verifyValue(self, value)
        if type(value) in [FloatType,IntType]:
            if value>=(1.-1.e-10):
                msg='of Saturation Degree : \n '
                msg+='a 100% value cannot define a unique\n'
                msg+='value of water pressure.\n'
                raise IncorrectValue(msg)
            if value>=(1.+1.e-10):
                msg='of Saturation Degree :  \n '
                msg+='the latter must be less than 1.\n'
                raise IncorrectValue(msg)
        return
    pass
    
class SpecificHeat(Scalar):
    """
    Specific heat capacity, also known simply as specific heat (J/g/K), 
    is the measure of the heat energy required to increase the temperature of a unit quantity of a substance
    by a certain temperature interval.
    """
    default_unit = _findUnit("SpecificHeatCapacity")

class KineticTimeConstant(Scalar):
    default_unit = _findUnit('Time')
    pass
    

class MaximumSaturation(AquiferPropertyScalar):
    """
    porous media water content: without dimension
    
    We check that the water content is less than 1.
    
    """
    def __init__(self, value = None, unit = None):
        default_unit = None
        self.value = value
        if type(value) not in [FloatType,IntType]:
            raise Warning(" the max. liquid saturation should be a float ")
        if value>=(1.+1.e-15):
            msg='of Saturation Degree :  \n '
            msg+='the latter must be less than 1.\n'
            raise IncorrectValue(msg)
        elif value>=(1.-1.e-5):
            msg='of Saturation Degree : \n '
            msg+='a 100% value cannot define a unique\n'
            msg+='value of water pressure.\n'
            raise IncorrectValue(msg)

class SaturatedWaterContent(AquiferPropertyScalar):
    """
    porous media water content: without dimension
    
    We check that the water content is less than 1.
    
    """
    def __init__(self, value = None, unit = None):
        default_unit = None
        self.value = value
    #value = SaturatedWaterContent.getValue()
        if type(value) not in [FloatType,IntType]:
            raise Warning(" the liquid saturation should be a float ")
        if value>=(1.+1.e-15):
            msg='of Saturation Degree :  \n '
            msg+='the latter must be less than 1.\n'
            raise IncorrectValue(msg)
        elif value>=(1.-1.e-5):
            msg='of Saturation Degree : \n '
            msg+='a 100% value cannot define a unique\n'
            msg+='value of water pressure.\n'
            raise IncorrectValue(msg)
    pass

class ResidualSaturation(AquiferPropertyScalar):
    """
    Residual porous media saturation: without dimension
    """
    def __init__(self, value = None, unit = None):
        default_unit = None
        self.value = value

class ResidualWaterContent(AquiferPropertyScalar):
    """
    Residual porous media water content: without dimension
    
    Bounded to residual saturation via the product Wcontent = residualSaturation * porosity
    
    """
    def __init__(self, value = None, unit = None):
        default_unit = None
        self.value = value
    
LiquidResidualSaturation = ResidualWaterContent
    
class MassSolubilityLimit(Scalar):
    default_unit = _findUnit('MassConcentration')

class ReactionRate(Scalar):
    default_unit = _findUnit('ReactionRate')

class SpecificAreaPerMole(Scalar):
    default_unit = _findUnit('SpecificAreaPerMole')

class SpecificStorage(Scalar):
    """
    Specific storage coefficient, see the users's guide
    
    Dimension : 1/s
    """
    def __init__(self, value=None, unit=None):
        default_unit = _findUnit('SpecificStorage')
        Scalar.__init__(self, value,unit=default_unit)
        pass

class SolidDensity(Scalar):
    def __init__(self, value=None, unit=None):
        default_unit = _findUnit('Density')
        if unit == None:
            Scalar.__init__(self, value,unit=default_unit)
            pass
        else:
            Scalar.__init__(self, value,unit)
            pass
    
RockDensity = SolidDensity

class SpecificHeatCapacity(Scalar):
    """
    Specific heat capacity, also known simply as specific heat, 
    is the measure of the heat energy required to increase the temperature of a unit quantity of a substance
    by a certain temperature interval.
    
    unit: J/g/K
    """
    def __init__(self, value=None, unit=None):
        default_unit = _findUnit("SpecificHeatCapacity")
        Scalar.__init__(self, value,unit=default_unit)
        pass
    default_unit = _findUnit("SpecificHeatCapacity")
    
SpecificHeat    = SpecificHeatCapacity
Cp              = SpecificHeatCapacity

class EffectiveDiffusion(Tensor):
    """
    
    """
    unit = _findUnit('EffectiveDiffusion')
    def __init__(self, value = None, dxx = None, dyy = None, dzz = None, unit = unit):
        
        if type(dxx) not in [FloatType,IntType, NoneType]:
            raise Exception(" dxx should be a float")
        if type(dyy) not in [FloatType,IntType, NoneType]:
            raise Exception(" dyy should be a float")
        if type(dzz) not in [FloatType,IntType, NoneType]:
            raise Exception(" dzz should be a float")

        if value == None:
            if (dyy or dzz) and type(dxx) == NoneType:
                raise IncorrectValue("check the definition of the effective diffusion,\n"+\
                                        " at least one real component has to be introduced (dxx)")
            val=dxx
            if  type(dyy) != NoneType:    val=Tensor2D(dxx,dyy)
            if  type(dzz) != NoneType:    val=Tensor3D(dxx,dyy,dzz)
            pass
        elif  (type(value) != NoneType):
            if type(value) in [FloatType,IntType]:
                val=value
                if not type(dxx) == NoneType: val = Tensor2D(value,dxx)
                if not type(dyy) == NoneType: val = Tensor3D(value,dxx,dyy)
                pass
            else:
                if type(dxx) != NoneType:
                    raise Exception("dxx type error")
                if type(dyy) != NoneType:
                    raise Exception("dyy type error")
                val=value
                pass
            if type(dzz) != NoneType:
                six.reraise(TypeError, "dzz type error ", dzz)
            pass
        try:
            vol = val
        except:
            raise Warning("check the effective diffusion value ")
        Tensor.__init__(self, val,unit = unit)

class HydraulicConductivity(Tensor):
    """
    Portion of hydraulic conductivity which is representative of the properties of the porous medium along,
    see Permeability. The relation between permeability k and hydraulic conductivity K is:
    
    K[m/s] = k[m**2]*rho[kg/(m**3)]*g[m/(s**2)]/mu[kg/m/s]
           
    k permeability or intrinsic permeability (specific ) is only a characteristic of the structure
    while K depends from the fluid properties.
    """
    def __init__(self,value,unit=None):
        default_unit = _findUnit('HydraulicConductivity')
        if unit==None:
            unit = default_unit
            pass
        Tensor.__init__(self, value, unit)

class KinematicDispersion(Scalar):
    """
    The presence of spatially varying celerities induces a dispersion effect,
    referred to as kinematic dispersion.
    we have a dispersion tensor whose dimension is L*L/T. 
    We have two coefficients to characterize it, the longitudinal and the transversal dispersion.
    Those two coefficients have the dimension of a length.
    As a reminder, elements of the dispersion tensor coefficients are like :
    
     dispersivityCoefficient * (velocityComponent * velocityComponent ) / velocitymodule
     
    """
    unit = _findUnit('Length')
    def __init__(self, longitudinal, transverse = None, unit=unit):
        if transverse == None: transverse = 0.0
        for i in (longitudinal, transverse):
            Scalar.verifyValue(self, i)
            pass
        self.value = (longitudinal, transverse)
        return
    def getLongitudinal(self):
        return self.value[0]
    def getTransverse(self):
        return self.value[1]

class Permeability(Tensor):
    """
    A measure of the ability of a material (such as rocks) to transmit fluids [L*T-1]
    
    k = K * mu/ rho*g 
    
    with:
    
        K       : the intrinsic permeability
        k       : the hydraulic conductivity
        mu      : the dynamic viscosity [M/L*S]
        rho     : the density           [M/L**3]
        g       : the gravity           [L/T**2]
    """
    def __init__(self,value,unit=None):
        default_unit = _findUnit('Permeability')
        if unit==None: unit = default_unit
        Tensor.__init__(self,value,unit)

class IntrinsicPermeability(Tensor):
    """
    A measure of the ability of a material (such as rocks) to transmit fluids [L**2]
    """
    def __init__(self,value,unit=None):
        default_unit = _findUnit('IntrinsicPermeability')
        if unit==None:
            unit = default_unit
            print("default unit of ",default_unit,type(default_unit))
            pass
        Tensor.__init__(self,value,unit)

class PoreDiffusion(Scalar):
    default_unit = _findUnit('Diffusion')
    pass
    
class Dilatation(AquiferPropertyScalar):
    """
    Normally bounded to thermal variations, the coefficient of thermal expansion describing how the size of an object changes with a change in temperature has as dimension 1/K
    ( 1/V)*((delta V)/(delta T))
    """
    def __init__(self,value):
        AquiferPropertyScalar.__init__(self,value)
    pass
    
class ExchangeCapacity(Scalar):
    default_unit = _findUnit('ExchangeCapacity')
    pass

class MolarMass(Scalar):
    """
    molar mass is the mass of one mole of substance
    """
    default_unit = _findUnit('MolarMass')
    pass

class PoreCompressibility(SolidPropertyScalar):
    """
    the pore compressibility expresses the variation of volume of pores due to a variation of pressure (1/V)*(dV/dP) : default unit is (1/Pa)
    """
    def __init__(self,value,unit):
        SolidPropertyScalar.__init__(self,value, unit = "1/Pa")
    pass
    
class PoreExpansivity(SolidPropertyScalar):
    """
    the pore expansivity expresses the variation of volume of pores due to a variation of temperature (1/V)*(dV/dT) : default unit is (1/K)
    """
    def __init__(self,value,unit):
        SolidPropertyScalar.__init__(self,value, unit = "1/K")
    pass

class Porosity(AquiferPropertyScalar):
    """
    the porosity of a porous medium (such as rock or sediment) describes the fraction of void space in the material
    """
    def __init__(self,value):
        AquiferPropertyScalar.__init__(self,value)
    pass
    
class RetardationFactor(AquiferPropertyScalar):
    """
    describes the ratio of time spent in the stationary phase relative to time spent in the mobile phase
    """
    def __init__(self,value):
        AquiferPropertyScalar.__init__(self,value)
    pass

class SharedFactor(AquiferPropertyScalar):
    def __init__(self,value):
        AquiferPropertyScalar.__init__(self,value)
    pass
    
class SolubilityLimit(Scalar):
    default_unit = _findUnit('Concentration')
    pass

class EffectivePorosity(Porosity):
    """
    Refers to the fraction of the total volume in which fluid flow is effectively taking place
    (this excludes dead-end pores or non-connected cavities)
    """
    default_unit = None
    pass
    
HydraulicPorosity = EffectivePorosity

class ThermalConductivity(Tensor):
    """
    In physics, thermal conductivity, generally noted k,
    is the property of a material that indicates its ability to conduct heat.
    It appears primarily in Fourier's Law for heat conduction.
    
    we can give a value corresponding to an isotropic tensor, or three arguments
    corresponding to diagonal elements of the tensor. A unit can be associated too
    
    1W = 1 J/s the joule in SI units gives : kgm2/s2
    """
    def __init__(self,value = None,dxx = None,dyy = None,dzz = None, unit = "kg*m/s***3/K"):    

        self.dxx = dxx
        self.dyy = dyy
        self.dzz = dzz
        self.value = value
        self.unit = default_unit = _findUnit('ThermalConductivity')

        
        if (dxx or dyy or dzz) and not value:
            if (dyy or dzz) and type(dxx)==NoneType:
                raise Exception("check the effective diffusion definition")
            val=dxx
            if not type(dyy)==NoneType:val=Tensor2D(dxx,dyy)
            if not type(dzz)==NoneType:val=Tensor3D(dxx,dyy,dzz)
            pass
        elif  (not type(value)==NoneType):
            if type(value) in [FloatType, IntType] or isInstance(value,IsotropicTensor):
                val=value
                if isinstance(value,IsotropicTensor):
                    value = value.getValues()
                    pass
                if not type(dxx)==NoneType:val=Tensor2D(value,dxx)
                if not type(dyy)==NoneType:val=Tensor3D(value,dxx,dyy)
                pass
            else:
                if type(dxx) != NoneType:
                    raise Exception("dxx should be of none type")
                if type(dyy) != NoneType:
                    raise Exception("dyy should be of none type")
                val=value
                pass
            if type(dzz) != NoneType:
                raise Exception("dzz should be of none type")
            pass
        try:
            vol=val
        except:
            msg='ya should have given a value for effective diffusion'
            raise Warning(msg)
        Tensor.__init__(self, value=val,unit=self.unit)

    
class MatrixCompressibilityFactor(Scalar):
    """
    compressibility of the solid matrix
    """
    default_unit = _findUnit('1/Pressure')
    pass

class Tortuosity(AquiferPropertyScalar):
    """
    Tortuosity is a property of curve being tortuous, twisted. 
    It is commonly used to describe diffusion in porous media related to the ratio of the effective and free diffusion coefficients.
    
    The tortuosity is generally equal to the square root of effective diffusion to free diffusion.
    """
    def __init__(self,value):
        AquiferPropertyScalar.__init__(self,value)
    pass

class Velocity(Vektor):
    default_unit = _findUnit('Velocity')
    pass

class Viscosity(Scalar):
    """
    Viscosity is a measure of the resistance of a fluid which is being deformed by either shear stress or extensional stress.
    """
    default_unit = _findUnit('Viscosity')
    pass

class YoungModulus(Scalar):
    """
    Young's modulus is a measure of the stiffness of an elastic material and is a quantity used to characterize materials.
    It is defined as the ratio of the stress (force per unit area) along an axis to the strain (ratio of deformation over initial length) along that axis. So, 
    its unit is therefore the one of a pressure.
    """
    default_unit = _findUnit('YoungModulus')
