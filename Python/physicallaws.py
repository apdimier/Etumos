# -*- coding: utf-8 -*-
#/usr/bin/python
"""
Physical laws, to be used in material and then for a transient simulation
Eventually refer to the etuser module to introduce your own laws 
"""
from __future__ import absolute_import
from __future__ import print_function
from generictools import isInstance, listTypeCheck, memberShip, SET_NUMBER
from listtools import toList
import exceptions
from types import ListType, TupleType, IntType, FloatType
import math

from PhysicalQuantities import PhysicalQuantity,_findUnit

from PhysicalQuantities import Concentration,\
                               Pressure,\
                               RefPressure,\
                               RefConcentration,\
                               RefTemperature,\
                               Temperature
                               
from species import Element,\
                    Species

from PhysicalProperties import Density,\
                               KineticTimeConstant,\
                               SolubilityLimit,\
                               Viscosity
from numpy import *
from six.moves import map
from six.moves import range
#
#
#
class PhysicalLaw:
    """
    A class used as a basis object for a physical law function.

    Example:    Heat capacity for a porous medium is a function of porosity, water and solid heat capacities.
                these three physical quantities will be the parameters, the arguments, the return value being
                the mean heat capacity evaluation
    """
    def __init__(self):
        pass
        
    def getValue(self):
        return self
        
    def getHelp(self):
        print(self.__doc__)
        pass

# ~~~~~~~~~~~~~~~
# Saturation laws
# ~~~~~~~~~~~~~~~

class SaturationLaw(PhysicalLaw):
    """
    Abstract : describes hydraulictensaturation law
    """
    def __init__(self,**args):
        PhysicalLaw.__init__(self)
        self.args = args
        
    def getargs(self):
        return self.args
    pass

class BrooksCoreySaturation(SaturationLaw):
    """
    brookscoreysaturation hydraulic saturation law
    sl = (referencesuction / suction)^lambdacoefficient         if suction > referencesuction
    
    sl = 1                                                      if suction <= referencesuction
    """
    def __init__(self, lambdacoefficient, referencesuction, unit = None, interval = None, name = None):
        """
        Constructor with :
        - lambdacoefficient : real
        - referencesuction : real
        ==> optional :
        - unit
        """
        self.lambdacoefficient = SET_NUMBER(lambdacoefficient)
        self.referencesuction = SET_NUMBER(referencesuction)
        self.unit = unit
        self.name = "brookscorey"
        if interval == None:
            from functions import interval
            interval = interval(0.,0.,0.1)
            pass
        self.interval=interval
        
    def eval(self, suction):
        """
        calculate liquid saturation value
        """
        if suction <= self.referencesuction:
            return 1.
        else:
            return pow((self.referencesuction / suction), self.lambdacoefficient)

    def getlambdacoefficient(self):
        """
        get lambdacoefficient
        """
        return self.lambdacoefficient
        
    def getreferencesuction(self):
        """
        get referencesuction
        """
        return self.referencesuction

    def getunit(self):
        """
        get unit
        """
        return self.unit
        
class VanGenuchtenSaturation(SaturationLaw):
    """
    Van Genuchten saturation hydraulic saturation law
    
    Sl = 1. / (1. + (alpha*suction)^n)^m                if suction > 0
    
    Sl = 1.                                             otherwise
    
    Two coefficients can be entered, but the definition can also conform to
    
    the definition of m as 1.-1./n
    
    """
    def __init__(self, alpha, n, m = None,interval = None, unit = None, name = None):
        """

        constructor with :
        - alpha : real
        - n : real
        - m : real
        ==> optional :
        - unit

        """
        self.alpha = SET_NUMBER(alpha)
        self.n = SET_NUMBER(n)
        if m != None:
            self.m = SET_NUMBER(m)
            pass
        else:
            self.m = 1. - 1./self.n
            pass
        if unit!=None:
            self.unit = _findUnit(unit)
            pass
        if interval == None:
            from functions import Interval
            interval = Interval(0.,0.,0.)
            pass

        self.interval=interval
        self.name = "van Genuchten"
        SaturationLaw.__init__(self, alpha = alpha, n = n, m = m, interval = interval, unit = unit)
        
    def eval(self, suction):
        """
        Evaluation of the liquid saturation
        """
        if suction <= 0.:
            return 1.
        else:
            return 1. / pow(1. + pow(self.alpha * suction, self.n), self.m) 
        
    def deriv_eval(self,suction):
        """
        evaluate liquid saturation derivative value
        """
        if suction <= 0.:
            return 0.
        else:
            m=  self.m
            n=  self.n
            alpha =  self.alpha
            return n*alpha*pow(alpha*suction,n-1)/(-m)*pow(1+pow(alpha*suction,n),m+1)

    def getN(self):
        """
        get n
        """
        return self.n
        
    def getM(self):
        """
        get m
        """
        return self.m

    def getAlpha(self):
        """
        get alpha
        """
        return self.alpha
    
    def getUnit(self):
        """
        get unit
        """
        return self.unit
#
    
class MaloideSaturation1(SaturationLaw):

    def __init__(self, alpha, n,interval=None,unit = None, name = None):
        """
        Constructor with :
        
        - alpha : REAL
        - n : REAL
        - m : REAL
        ==> OPTIONAL :
        - unit
        
            res = self.alpha* pow( suction, self.n)

        """
        SaturationLaw.__init__(self,alpha=alpha,n=n,fonction=self,interval=interval)
        self.alpha = SET_NUMBER(alpha)
        self.n = SET_NUMBER(n)
        if unit != None:
            self.unit = _findUnit(unit)
            pass
        self.name = "Maloide"
        if interval == None:
            from functions import Interval
            interval = Interval(0.,0.,0.)
            pass
        self.interval = interval 
        
    def eval(self, suction):
        """
        Calculate liquid saturation value
        input   suction
        output  saturation
        """
        if suction <= 0.:
            return 1.
        else:
            res = self.alpha* pow( suction, self.n)
            return res
        
    def deriv_eval(self,suction):
        """
        Calculate liquid saturation derivative value
        """
        if suction <= 0.:
            return 0.
        else:
            n = self.n
            alpha = self.alpha
            res = self.n*self.alpha* pow( suction, (self.n-1))
            return res

    def getN(self):
        """
        get n
        """
        return self.n
    def getAlpha(self):
        """
        get alpha
        """
        return self.alpha
    
    def getUnit(self):
        """
        get unit
        """
        return self.unit
        
class MaloideSaturation2(SaturationLaw):

    def __init__(self, beta, n, m, interval = None, unit = None, name = None):
        """
        constructor with :
        - alpha : REAL
        - n : REAL
        - m : REAL
        ==> OPTIONAL :
        - unit
        """
        SaturationLaw.__init__(self,beta=beta,n=n,m=m,fonction=self,interval=interval)
        self.beta = SET_NUMBER(beta)
        self.n = SET_NUMBER(n)
        self.m = SET_NUMBER(m)
        if unit!=None:
            self.unit = _findUnit(unit)
            pass
        if interval == None:
            from functions import Interval
            interval =Interval(0.,0.,0.)
            pass
        self.interval =interval
    def eval(self, suction):
        """
        Calculate liquid saturation value
        """
        if suction <= 0.:
            return 1.
        else:
            return self.beta* pow( suction, self.m - self.n)
        
    def deriv_eval(self,suction):
        """
        Calculate liquid saturation derivative value
        """
        if suction <= 0.:
            return 0.
        else:
            n=  self.n
            res = -self.n*self.beta* pow( suction, (-self.n-1))
            return res

    def getN(self):
        """
        get n
        """
        return self.n
    def getAlpha(self):
        """
        get alpha
        """
        return self.alpha
    
    def getUnit(self):
        """
        get unit
        """
        return self.unit
        
class ExponentialSaturation(SaturationLaw):
    """
    Exponential hydraulic saturation law:
    
        Sl= c / (c + (exp(alpha*suction))^n -1)     if suction > 0
        
        Sl = 1                                      if suction <=0
    """
    
    def __init__(self, alpha, c, n, unit = None, interval = None, name = None, description = None):
        """
        - alpha : REAL
        - c : REAL
        - n : REAL
        -  unit
                                Sl = c/(c - 1. + exp(alpha*S)**n)
        """
        self.alpha = SET_NUMBER(alpha)
        self.c = SET_NUMBER(c)
        self.n = SET_NUMBER(n)
        if name == None:
            self.name = "exponential"
            pass
        else:
            self.name = name
            pass
        if unit!=None:
            self.unit = _findUnit(unit)
            pass
        if interval == None:
            from functions import Interval
            interval = Interval(0.,0.,0.)
            pass
        self.interval=interval
        
        if ((not self.c and not self.alpha) or
            (not self.c and not self.n)):
            raise Exception(" Check the coefficients of the exponential law")
            
        self.description = description

    def eval(self, suction):
        """

        """
        if suction <= 0.:
            return 1.
        else:
            return self.c/(self.c -1. + pow(math.exp(self.alpha * suction), self.n))

    def getAlpha(self):
        """
        get alpha
        """
        return self.alpha

    def getC(self):
        """
        get c
        """
        return self.c

    def getN(self):
        """
        get n
        """
        return self.n

    def getName(self):
        """
        get name
        """
        return self.name

    def getUnit(self):
        """
        get unit
        """
        return self.unit

class LogarithmicSaturation(SaturationLaw):
    """
    LogarithmicSaturation hydraulic saturation law
    
    Sl = c / (c + (ln(alpha*suction))^n)                if suction > 1/alpha
    
    Sl = 1                                              if suction <= 1/alpha
    """
    def __init__(self, alpha, c, n, unit = None,interval = None):
        """construction with :
        - alpha : REAL
        - c : REAL
        - n : REAL
        -  unit
        """
        self.alpha = SET_NUMBER(alpha)        
        if not self.alpha:
            raise Exception("You have defined a Logarithmic law with alpha =0!!!!!!!")
        self.c = SET_NUMBER(c)
        self.n = SET_NUMBER(n)
        self.unit = _findUnit(unit)
        if interval == None:
            from functions import Interval
            interval = Interval(0.,0.,0.)
            pass
        self.interval=interval

    def eval(self, suction):
        """

        """
        oneoveralpha=1./self.alpha
        if suction <= oneoveralpha:
            return 1.
        else:
            per = self.c/(self.c + pow(math.log(self.alpha * suction), self.n))
            return per

    def getAlpha(self):
        """get alpha"""
        return self.alpha

    def getC(self):
        """get c"""
        return self.c

    def getN(self):
        """get n"""
        return self.n

    def getUnit(self):
        """get unit"""
        return self.unit
# ~~~~~~~~~~~~~~~
# Dispersion laws
# ~~~~~~~~~~~~~~~ 
class DispersionLaw(PhysicalLaw):
    """
    Container to describe a dispersion law
    """
    def __init__(self,**args):
        self.Args = args
    def getArgs(self):
        return self.Args
    pass

class TotalDispersion(DispersionLaw):
    """
    TotalDispersion dispersion law
    """
    def __init__(self):
        """constructor"""
        self.law='TotalDispersion'
        
    def getLaw(self):
        """get Law"""
        return self.law
#    def __init__(self,alphaT, alphaL):
#        self.alphaT = SET_NUMBER(alphaT)
#        self.alphaL = SET_NUMBER(alphaL)
#    def getAlphaL(self):
#        return self.alphaL

#    def getAlphaT(self):
#        return self.alphaT    

class DiagonalDispersion(DispersionLaw):
    """DiagonalDispersion dispersion law"""
    def __init__(self):
        """constructor"""
        self.law='DiagonalDispersion'

    def getLaw(self):
        """get Law"""
        return self.law
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Effective diffusion laws (function of porosity)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class EffectiveDiffusionLaw(PhysicalLaw):
    """
    Container to describe an effective diffusion law
    The effective difusion law will express diffusion as a function of porosity De = f(theta)
    """
    def __init__(self,**args):
        self.Args = args
    def getArgs(self):
        return self.Args
    pass

class WinsauerDiffusionLaw(EffectiveDiffusionLaw):
    """
    Effective diffusion law Winsauer et al (1952)
        effective diffusion = initialEffectiveDiffusion * (porosity-percolationPorosity)/(initial porosity-percolationPorosity) ** cementationCoefficient
    """

    def __init__(self,**args):
        lexikon = args
        if "cementationCoefficient" in lexikon:
            cementationCoefficient = lexikon["cementationCoefficient"]
            if type(cementationCoefficient) != FloatType:
                raise Warning(" the cementationCoeficient must be a float it has been set to zero")
                self.cementationCoefficient = 0.0
                pass
            else:
                self.cementationCoefficient = cementationCoefficient
                pass
        else:
            raise Exception(" the cementation coefficient is mandatory for the WinsauerDiffusionLaw definition")
            pass
        if "percolationPorosity" in lexikon:
            percolationPorosity = lexikon["percolationPorosity"]
            if type(percolationPorosity) != FloatType:
                raise Warning(" the percolationPorosity must be a float")
                self.percolationPorosity = 0.0
                pass           
            else:
                self.percolationPorosity = percolationPorosity
                pass
            pass
        else:
            self.percolationPorosity = 0.0
            pass
        
    def getpercolationPorosity(self):
        """
        to get the percolation porosity
        """
        return self.percolationPorosity

    def getCementationCoefficient(self):
        """
        To get the cementation coefficient
        """
        return self.cementationCoefficient

    def eval(self,porosity,initialPorosity,initialEffectiveDiffusion):
        """
        Return effective diffusion coefficients computed with a certain law via porosity values
           Input : actual porosity (float)
                   initial porosity (float)
                   initial effective diffusion
           Output : new effective diffusion 
        """
        
        percolPorosity = self.percolationPorosity
        archieExponent = self.cementationCoefficient
        diffusionValue = initialEffectiveDiffusion * ( (porosity-percolPorosity)/(initialPorosity-percolPorosity) )**archieExponent
        return diffusionValue
        

class ExpDiffusionLaw(EffectiveDiffusionLaw):
    """
    Effective diffusion law following an exponential formula :
    """
    def __init__(self, exponentialCoefficient):
        """
        Input: expCoefficient : float
        """
        if type(exponentialCoefficient) != FloatType:
            raise Exception("exponentialCoefficient must be a float ")
        self.exponentialCoefficient = exponentialCoefficient

    def getExponentialCoefficient(self):
        """
        Get coefficient in exponential term
           Output: float
        """
        return self.exponentialCoefficient

    def eval(self,new_porosity_value,initial_porosity_value,initial_effective_diffusion_value):
        """
        Return effective diffusion coefficients computed with a certain law via porosity values
           Input : new_porosity_value (float)
                   initial_porosity_value (float)
                   initial_effective_diffusion_value (float)
           Output : new effective diffusion value D, D11, D21, D22, D31, D32 or D33 (float)
        """

        factor = self.exponentialCoefficient
        new_diffusion_value = initial_effective_diffusion_value * exp(factor*(new_porosity_value-initial_porosity_value))
        return new_diffusion_value


class LinearDiffusionLaw(EffectiveDiffusionLaw):
    """
    Effective diffusion law following a linear formula :
        effective diffusion = linearCoefficient * (porosity - initial_porosity) + initial_effective_diffusion
    """
    def __init__(self, linearCoefficient):
        """
        Input:
           linearCoefficient : float
        """

        if type(linearCoefficient) != FloatType:
            raise Exception("the linear coefficient must be a float")
        self.linearCoefficient = linearCoefficient
        pass

    def getLinearCoefficient(self):
        """
        Get linearCoefficient
           Output: float
        """
        return self.linearCoefficient

    def eval(self,new_porosity_value,initial_porosity_value,initial_effective_diffusion_value):
        """
        Return effective diffusion coefficients computed with a certain law via porosity values
           Input : new_porosity_value (float)
                   initial_porosity_value (float)
                   initial_effective_diffusion_value (float)
           Output : new effective diffusion value D, D11, D21, D22, D31, D32 or D33 (float)
        """

        newEffDiffusionValue = self.linearCoefficient * (new_porosity_value-initial_porosity_value) + initial_effective_diffusion_value
        return newEffDiffusionValue


class ProportionalDiffusionLaw(EffectiveDiffusionLaw):
    """
    Effective diffusion law following a proportional formula :
        effective diffusion = initial_effective_diffusion * porosity
        Attention !!! this law is not consistent with the following requirement :
                      effective diffusion(initial_porosity) = initial_effective_diffusion
    """
    def __init__(self):
        """
        no input
        """
        pass

    def eval(self,new_porosity_value,initial_porosity_value,initial_effective_diffusion_value):
        """
        Return effective diffusion coefficients computed with a certain law via porosity values
           Input : new_porosity_value (float)
                   initial_porosity_value (float)
                   initial_effective_diffusion_value (float)
           Output : new effective diffusion value D, D11, D21, D22, D31, D32 or D33 (float)
        """

        newEffDiffusionValue = initial_effective_diffusion_value * new_porosity_value/initial_porosity_value
        return newEffDiffusionValue
    
class FickVapeurLaw(PhysicalLaw):
    """
    Thm Diffusion de Fick Vapeur Saturee
    Cette loi de diffusion doit etre donnee sous la forme d'un produit de 4 fonctions
    d une variable chacune (temperature saturation pression gaz pressionliquide)
    chaque fonction doit etre donnee sous la forme
    soit    d 'un objet de type DerivableFunction
    soit d 'un tuple (fonction, [derivee],[ interval])
    soit  d 'une constante
    la derivee est obligatoire pour les fonctions de la temperature et de la pression gaz
    """
    def __init__(self,**args):
        self.Args = args
        dict = {}
        dict['fickv_t']='fvte'
        dict['fickv_s']='fvsa'
        dict['fickv_pg']='fvpg'
        dict['fickv_pv']='fvpv'
        from functions import DerivableFunction,DerivableFunctionconst,Interval
        import types
        if('fickv_t' not in args):
            raise Exception("fickv_t doit etre present")
        self.func = []
        for k in args.keys():
            if isinstance(args[k],FloatType) or isinstance(args[k],IntType ):
                argument = DerivableFunctionconst(args[k])
            elif isinstance(args[k],TupleType):
                if len(args[k]) == 3 :
                    if (k == 'fickv_t' or k == 'fickv_pg'):
                        argument = DerivableFunction(args[k][0], args[k][1], args[k][2])
                    else:
                        if isinstance(args[k][1],Interval):
                            argument = DerivableFunction(args[k][0], args[k][1])
                            pass
                        elif isinstance(args[k][2],Interval):
                            argument = DerivableFunction(args[k][0], args[k][2])
                            pass
                        else:
                            raise Exception("Erreur Fickv_s ou fick_pv  triplet fourni")
                        pass
                    pass
                elif len(args[k]) == 1 :
                    if k == 'fickv_t' or k == 'fickv_pg':
                        raise Exception("fickv_pg ou fickv_t, You have to define the slope",k)
                    argument = DerivableFunction(args[k][0])
                    pass
                elif len(args[k]) == 2:
                    if isinstance(args[k][1],Interval):
                        if k == 'fickv_t' or k == 'fickv_pg':
                            raise Exception("fickv_pg ou fickv_t, Vous devez fournir la derivee")
                        else:
                            argument = DerivableFunction(args[k][0],interval=args[k][1])
                            pass
                    else:
                        argument = DerivableFunction(args[k][0],derivee=args[k][1])
                        pass
                    pass
                else:
                    pass
            elif  isinstance(args[k],DerivableFunction):
                if (k == 'fickv_t' or k == 'fickv_pg') and args[k].derivee == None :
                    raise Exception("fickv_pg ou fickv_t, Vous devez fournir la derivee")
                if  (k == 'fickv_s' or k == 'fickv_pv')  and args[k].derivee != None:
                    print(" derivee devrait etre nulle ",k,args[k].derivee) 
                    if args[k].interval == None:
                        fonc =  DerivableFunction(args[k])
                        pass
                    else:
                        fonc =DerivableFunction(args[k].fonction, interval= args[k].interval)
                        pass
                    args[k]=fonc
                    pass
                argument = args[k]
                pass
            else:
                raise Exception("On attend une DerivableFunction, ou une constante ou un tuple")
            self.func.append((argument,dict[k]))
#traitement des donnees manquantes
        for k in dict.keys():
            if(k not in args):
                argument = DerivableFunctionconst(1.)
                self.func.append((argument,dict[k]))
                pass
            pass
    def getArgs(self):
        return self.Args

# =================
# Permeability laws
# =================
class PermeabilityLaw(PhysicalLaw):
    """
    Container to describe a permeability law
    """
    def __init__(self,**args):
        self.Args = args
    def getArgs(self):
        return self.Args
    pass

class IntrinsicPermeabilityLaw(PhysicalLaw):
    """
    Class used to describe intrinsic permeability laws, basis of 
    absolute permeability laws which conducts to laws like:
    
        Examples:
    
            Carman-Kozeny
            
            cubic law
            
            Verma-Pruess
            
        units: The SI unit for permeability is m**2.
        
        User has to pay attention. Permeability is often given in Darcy:  1D = 1.e-12 m**2
        
        In the case of a saturated flow, the Darcy law uses the hydraulic conductivity (m/s)
        
        The porosity is given by the iteration loop over the mesh
    """
    def __init__(self,**kargs):
        #print 'IntrinsicPermeabilityLaw arg ',kargs
        lexikon = kargs
        self.args = kargs
        print(lexikon)
        if "initialPorosity" in lexikon:
            self.initialPorosity = lexikon["initialPorosity"]
            pass
        else:
            self.initialPorosity = 0.1
            pass
        if "k0" in lexikon:
            self.k0 = lexikon["k0"]
            pass
        else:
            self.k0 = 1.0
            raise Warning(" Due to the lack of k0, k0 constant has been set to one")
    pass
#
# Kozeny Carman Law
#    
class KozenyCarmanLaw(IntrinsicPermeabilityLaw):
    """
    
    Kozeny-Carman law defined as :
    
        k_i     initial intrinsic permeability
        por_i   initial porosity
        
        and via the eval function with :
        
        por     current porosity
        
        Ki * ((1. - por_i)/(1. - por))**2 * ( (por/por_i)**3 )
        
    """
    def __init__(self,**kargs):
        print(" args ",kargs)
        IntrinsicPermeabilityLaw.__init__(self,**kargs)
        #
        # the cst is evaluated once
        #
    def eval(self,currentPorosityValue):
        #print currentPorosityValue,self.k0,self.initialPorosity
        
        return  self.k0 * pow(  (1.-currentPorosityValue) / (1.-self.initialPorosity), 2) * \
                          pow( currentPorosityValue / self.initialPorosity , 3)
#
# Verma Pruess Law
#
class VermaPruessLaw(IntrinsicPermeabilityLaw):
    """
    Verma Pruess law (1988):
        
        k_i     initial permeability
        por_i   initial porosity
        por     current porosity
        por_c   critical porosity at which the permeability goes to zero ( also called percolation porosity)
        
        Ki * ( (por - por_c)/ (por_i - por_c) )**n
        
    """
    def __init__(self,**args):
        print(" args ",args)
        IntrinsicPermeabilityLaw.__init__(self,**args)
        if "criticalPorosity" in args:
            self.criticalPorosity = args["criticalPorosity"]
            pass
        else: 
            raise Exception(" the critical porosity is mandatory for the Verma Pruess law definition")
        #
        # the inverse is evaluated once
        #    
        self.denominator = 1.0/(self.initialPorosity -self.criticalPorosity)
        
        if "exponentLaw" in args:
            self.exponentLaw = args["exponentLaw"]
            pass
        else: 
            self.exponentLaw = 2
            pass
    def eval(self,currentPorosityValue):
        print(currentPorosityValue,self.k0,self.initialPorosity,self.exponentLaw)
        return self.k0*pow((currentPorosityValue-self.criticalPorosity)*self.denominator, self.exponentLaw)

class MualemPermeability(PermeabilityLaw):
    """
    The Mualem relative permeability law is related to the Van Genuchten saturation model
    with km = 1
    
    S normed saturation
        
    kr = sqrt(S) * [ [1. - (S)**(1/m) ]**m ]**2
        
    """
    def __init__(self, m,interval=None):
        """
        construction with :
        - m : REAL
        """
        self.m = SET_NUMBER(m) 
        if not self.m:
            raise Warning("You have defined a Mualem law without defining the m exponent, it has been set to 2")
            self.m = 2.
            pass
        if interval == None:
            from functions import Interval
            interval =Interval(0.,0.,0.)
            pass
        self.interval =interval

    def eval(self, sat):
        """calculate relative permeability value with S = sat"""
        b = 2.
        aux = 1 - pow(sat, 1./self.m)
        return pow(sat, 0.5) * pow(aux, self.m * b)

    def deriv_eval(self, sat):
        """calculate relative permeability derivative value with S = sat"""
        a = 0.5
        b = 2.
        m=self.m
        aux = 1 - pow(sat, 1./m)
        auxx = pow(sat,a-1)*pow(aux, m * b-1)
        return auxx*(a*aux -(sat*m * b/m)*pow(sat,(1-m/m)))
                     
    def getM(self):
        """get m"""
        return self.m


class BurdinePermeability(PermeabilityLaw):
    """
    The Burdine relative permeability law is related to the Van Genuchten saturation model
    with km = 2
    
    
    S normed saturation
    
    kr = (S^2)*[1-(S)^(1/m)]^m
    """
    def __init__(self, m,interval=None):
        """construction with :
        - m : REAL
        """
        self.m = SET_NUMBER(m)
        if not self.m:
            raise Exception("You have defined a Burdine law with m =0!!!!!!!")

        if interval == None:
            from functions import Interval
            interval = Interval(0.,0.,0.)
            pass
        self.interval=interval
    def eval(self, sat):
        """calculate relative permeability value with S = sat"""
        a = 2.
        b = 1.
        aux = 1 - pow(sat, 1./self.m)
        return pow(sat, a) * pow(aux, self.m * b)

    def getM(self):
        """get m"""
        return self.m

class BrooksCoreyPermeability(PermeabilityLaw):
    """
    BrooksCorey permeability law:
    
        S normed saturation
    
        kr = (S**a)*[S**(b+2/lambda)]
    """

    def __init__(self, a, b, lambdaCoefficient,interval=None):
        """
        construction with :
        - a : REAL
        - b : REAL
        - lambda : REAL
        """
        self.a = SET_NUMBER(a)
        self.b = SET_NUMBER(b)
        self.lambdaCoefficient = SET_NUMBER(lambdaCoefficient)
        if interval == None:
            from functions import Interval
            interval = Interval(0.,0.,0.)
            pass
        self.interval=interval
        if not self.lambdaCoefficient:
            raise Exception("You have defined a  BrooksCoreyPermeability law with lambdaCoefficient =0!!")

    def eval(self, sat):
        """
        Calculate relative permeability value with S = sat
        """
        return pow(sat, self.a) * pow(sat, self.b + 2. / self.lambdaCoefficient)

    def getA(self):
        """
        get a
        """
        return self.a

    def getB(self):
        """
        get b
        """
        return self.b

    def getLambda(self):
        """
        get lambdaCoefficient
        """
        return self.lambdaCoefficient

class CubicPermeabilityLaw(PermeabilityLaw):

    """
    The cubic permeability law is defined as
    
    Cubic permeability law:
    
        kr = ki(phi/phi_i)**3 // kr = ki*power(phi/phi_i,3)
    """

    def __init__(self,initialPermeability=None,initialPorosity = None):
        """
        Constructor
        """
        self.initialPermeability = initialPermeability
        self.initialPorosity = initialPorosity
        self.invInPor = self.initialPorosity

        pass

    def eval(self, porosity):
        """
        Calculate relative permeability value with S = sat
        """
        
        return self.initialPermeability*pow(porosity*self.invInPor, 3)

class ExponentialPermeability(PermeabilityLaw):
    """
    Exponential permeability law:
    
        kr = c / (c + (exp(alpha*suction))^n -1)                if suction > 0
        
        kr = 1                                                  otherwise
    """
    def __init__(self,  alpha, c, n, unit=None,interval=None):
        """
        Construction with :
        - alpha : REAL
        - c : REAL
        - n : REAL
        -  unit
        """
        self.alpha = SET_NUMBER(alpha)
        self.c = SET_NUMBER(c)
        self.n = SET_NUMBER(n)
        self.unit = _findUnit(unit)
        if interval == None:
            from functions import Interval
            interval = Interval(0.,0.,0.)
            pass
        self.interval=interval
        if ((not self.c and not self.alpha) or
            (not self.c and not self.n)):
            raise Exception("You define an Exponential law with c and alpha = 0 or wich c and n = 0!!!!")
            
    def eval(self, suction):
        """
        Calculate relative permeability value
        """
        if suction <= 0.:
            return 1.
        else:
            return self.c/(self.c + pow(math.exp(self.alpha * suction), self.n) - 1.)

    def getAlpha(self):
        """
        get alpha
        """
        return self.alpha

    def getC(self):
        """get c"""
        return self.c

    def getN(self):
        """
        get n
        """
        return self.n

    def getUnit(self):
        """
        get unit
        """
        return self.unit
        
class LogarithmicPermeability(PermeabilityLaw):
    """
    Logarithmic permeability law:
    
        kr = c / (c + (ln(alpha*suction))^n) si suction > 1/alpha
        kr = 1 si suction <= 1/alpha
    """
    def __init__(self, alpha, c, n, unit=None,interval=None):
        """
        Construction with :
        - alpha : REAL
        - c : REAL
        - n : REAL
        -  unit
        """
        self.alpha = SET_NUMBER(alpha)
        if not self.alpha:
            raise Exception("You have defined a Logarithmic law with alpha =0!!!!!!!")
        self.c = SET_NUMBER(c)
        self.n = SET_NUMBER(n)
        self.unit = _findUnit(unit)
        if interval == None:
            from functions import Interval
            interval = Interval(0.,0.,0.)
            pass
        self.interval=interval 

    def eval(self, suction):
        """
        Calculate relative permeability value
        """
        unsuralpha = 1./self.alpha
        
        if suction <= unsuralpha:
            return 1.
        else:
            return self.c/(self.c + pow(math.log(self.alpha * suction), self.n))

    def getAlpha(self):
        """
        get alpha
        """
        return self.alpha

    def getC(self):
        """
        get c
        """
        return self.c

    def getN(self):
        """
        get n
        """
        return self.n

    def getUnit(self):
        """
        get unit
        """
        return self.unit

class MaloidePermeabilite1(PermeabilityLaw):
    def __init__(self, alpha, n,interval=None,unit=None):
    
        """
        constructor with :
        
        - alpha : REAL
        - n : REAL
        ==> OPTIONAL :
        - unit
        """
        PermeabilityLaw.__init__(self,alpha=alpha,n=n,fonction=self)
        self.alpha = SET_NUMBER(alpha)
        self.n = SET_NUMBER(n)
        self.unit = _findUnit(unit)
        if interval == None:
            from functions import Interval
            interval =Interval(0.,0.,0.)
            pass
        self.interval =interval
    def eval(self, sat):
        """
        Calculate liquid saturation value
        """
        if sat <= 0.:
            return 1.
        else:
            res =self.alpha* pow( sat, self.n)
            return res
        
    def deriv_eval(self,sat):
        """
        Calculate liquid saturation derivative value
        """
        if sat <= 0.:
            return 0.
        else:
            n=  self.n
            alpha =  self.alpha
            res = self.n*self.alpha* pow( sat, (self.n-1))
            return res

    def getN(self):
        """
        get n
        """
        return self.n
    def getAlpha(self):
        """
        get alpha
        """
        return self.alpha
    
    def getUnit(self):
        """
        get unit
        """
        return self.unit
# ===============
# Solubility laws
# ===============
class SolubilityLaw(PhysicalLaw):
    """
    Abstract : describes solubility law
    """
    def __init__(self,**args):
        self.Args = args
    def getArgs(self):
        return self.Args
    pass

class SolubilityByIsotope(SolubilityLaw):
    """
    SolubilityByIsotope solubility law
    """
    def __init__(self, solubilityLimit,kineticTimeConstant=None):
        """construction with :
        - solubilityLimit is an object of type SolubilityLimit
        - kineticTimeConstant is an object of type KineticTimeConstant
        """
        memberShip(solubilityLimit, SolubilityLimit)
        self.solubilityLimit=solubilityLimit
        if kineticTimeConstant:
            memberShip(kineticTimeConstant, KineticTimeConstant)
            pass
        else:
            kineticTimeConstant=KineticTimeConstant(1.0e+4)
            pass
        self.kineticTimeConstant = kineticTimeConstant
        
    def getSolubilityLimit(self):
        return self.solubilityLimit

    def getKineticTimeConstant(self):
        return self.kineticTimeConstant

class SolubilityByElement(SolubilityLaw):
    """
    SolubilityByElement solubility law
    """
    def __init__(self, solubilityLimit,kineticTimeConstant=None):
        """
        Construction with :
        - solubilityLimit is an object of type SolubilityLimit
        - kineticTimeConstant : could be of type KineticTimeConstant
                            or a list of couple (KineticTimeConstant,Species)
                            or a list with a defaut value and couples (KineticTimeConstant,Species)
                            for example [kc,(kc1,species1),(kc2,species2)]
        """
        memberShip(solubilityLimit, SolubilityLimit)
        self.solubilityLimit=solubilityLimit
        listbid=0
        if kineticTimeConstant:
            if type(kineticTimeConstant) is ListType:
                for kine in kineticTimeConstant:
                    if type(kine) is TupleType:
                        memberShip(kine[0], KineticTimeConstant)
                        memberShip(kine[1], Species)
                    else:
                        memberShip(kine,KineticTimeConstant)
                        listbid=1
                        pass
                    pass
                pass
            else:
                memberShip(kineticTimeConstant, KineticTimeConstant)
                pass
            pass
        else:
            kineticTimeConstant=KineticTimeConstant(1.0e+4)
            pass
        self.kineticTimeConstant=kineticTimeConstant
        pass

    def getSolubilityLimit(self):
        return self.solubilityLimit

    def getKineticTimeConstant(self, species = None):
        """
        If KineticTimeConstant is defined :
               if a species is specified,
                   return the associated kineticconstant value
               else return the default value
           else return None
           """
        if self.kineticTimeConstant:
            if type(self.kineticTimeConstant) is ListType:
                for kine in kineticTimeConstant:
                    if type(kine) is TupleType:
                        if species:
                            if kine[1].getName().lower() == species.lower():
                                return kine[1]
                            pass
                        pass
                    pass
                for kine in kineticTimeConstant:
                    if not type(kine) is TupleType:
                        return kine
                    pass
                pass
            else:
                return self.kineticTimeConstant
            pass
        return None

##    def getElements(self):
##        """get elements"""
##        return self.solubilityLimit_elements
# ==============
# Sorption  laws
# ==============
 
class SorptionLaw(PhysicalLaw):
    """
    Abstract : describes SorptionLaw
    """
    def __init__(self,**args):
        self.Args = args
    def getArgs(self):
        return self.Args
    pass

class RetardationCoefficient(SorptionLaw):
    """
    Retardationcoefficient sorption law
    """
    def __init__(self, R):
        """
        Constructor with :
        - R : REAL
        """
        self.r = SET_NUMBER(R)

    def getR(self):
        """get R"""
        return self.r

class DistributionCoefficient(SorptionLaw):
    """
    DistributionCoefficient sorption law
    Csor = kd*C
    """
    def __init__(self, kd, unit = None):
        """constructor with :
        - kd : REAL
        --> OPTIONAL :
        - unit"""        
        self.kd = SET_NUMBER(kd)
        self.unit = _findUnit(unit, 'DistributionCoefficient')

    def getKd(self):
        """get kd"""
        return self.kd

    def getUnit(self):
        """get unit"""
        return self.unit

class Langmuir(SorptionLaw):
    """
    Langmuir sorption law
    Csor = a*C/(b+C)
    """
    def __init__(self, a, b):
        """constructor with :
        - a : REAL
        - b : REAL"""
        self.a = SET_NUMBER(a)
        self.b = SET_NUMBER(b)
    def getA(self):
        """get a"""
        return self.a

    def getB(self):
        """get b"""
        return self.b

class Freundlich(SorptionLaw):
    """
    Freundlich sorption law
    Csor = a*(C)^(1/n)
    """
    def __init__(self, a, n):
        """constructor with :
        - a : REAL
        - n : REAL"""
        self.a = SET_NUMBER(a)
        self.n = SET_NUMBER(n)

    def getA(self):
        """get a"""
        return self.a

    def getN(self):
        """get n"""
        return self.n
#
#
#
class StateLaw(PhysicalLaw):
    """StateLaw used to describe viscosity law and density law"""
    def __init__(self,*varCoeffs):
        """constructor"""
        self.law=None
##         placesForVars=(0,-1)
##         miroir={0:-1,-1:0}
##         p0=None
        listVarClasses=[Pressure,Concentration,Temperature]
        listRefClasses=[RefPressure,RefConcentration,RefTemperature]
        if len(varCoeffs):
            self.law=[]
            pass
        for vc in varCoeffs:
            if type(vc) not in [TupleType,ListType]:
                raise Exception("vc must be a list")
            varIsSpecified=0
            refIsSpecified=0
            for i in range(len(vc)):
                if vc[i] in listVarClasses:
                    if vc[i] not in listRefClasses:
                        varIsSpecified=1
                        varindex=i
                        indexvar=listVarClasses.index(vc[i])
                        pass
                    pass
                if isInstance(vc[i],listRefClasses):
                    refIsSpecified=1
                    refindex=i
                    #index1=listRefClasses
                    pass
                pass
            if not varIsSpecified:
                msg='a physical quantity must be set'
                msg+=' for waterLaw coefficients'
                raise exceptions.Exception(msg)
            if not refIsSpecified:
                msg='a physical quantity must be set'
                msg+=' for StateLaw coefficients'
                raise exceptions.Exception(msg)
            else:
                memberShip(vc[refindex],listVarClasses[indexvar])
        
        
            var=vc[varindex]
            p0=vc[refindex]
            coeffs=[]
            for x in vc:
                coeffs.append(x)
                pass
            law={}
            law['variable']=var
            coeffs.remove(p0)
            coeffs.remove(var)
            if len(coeffs)!=1 and isinstance(p0,RefPressure):
                msg='there should be only one coefficient for'
                msg='\n waterLaw dependance with Pressure.'
                raise Exception(msg)
            law['variableRef']=p0
            listTypeCheck(coeffs,[FloatType,IntType])
            list(map(lambda x:float(x),coeffs))
            law['coefficients']=coeffs
            law['lawType']=self.getLawType(var)
            self.law.append(law)
            pass

    def getLawType(self,lawvar):
        """get LawType : polynomial or exponential"""
        if lawvar in [Temperature,Concentration]:
            lawtype='polynomial'
            pass
        elif lawvar==Pressure:
            lawtype='exponential'
            pass
        else:
            raise Exception('Unknown variable for waterLaw')
        return lawtype
    
    def getLaw(self):
        """get law"""
        return self.law

    def getCoefficients(self,variable_class):
        """get Coefficients"""
        for law in self.law:
            if law['variable']==variable_class:
                return law['coefficients']
            pass
        

    def getDepend(self):
        """get Depend"""
        liste=[]
        for law in self.law:
            liste.append(law['variable'])
        return liste

    def getDependNames(self):
        """get depend names"""
        liste=[]
        for law in self.law:
            liste.append(law['variable'].__name__)
            pass
        return liste

class DensityLaw(StateLaw):
    """
    Density law
    """
    pass

class ViscosityLaw(StateLaw):
    """
    Viscosity law
    """
    def __init__(self,*varCoeffs):
        StateLaw.__init__(self,*varCoeffs)
        no=[Pressure,RefPressure]
        for vc in varCoeffs:
            for i in range(len(vc)):
                if (vc[i] in no) or \
                   isInstance(vc[i], no):
                    msg='Viscosity cannot depend on Pressure.'
                    raise Exception(msg)
                pass
            pass
                
                
class FickAirDissousLaw(PhysicalLaw):
    """Thm Diffusion de Fick Air dissous
    Cette loi de diffusion doit etre donne sous la forme d'un produit de 4 fonctions
    d une variable chacune (temperature saturation pression airdissous  pressionliquide)
    chaque fonction doit etre donnee sous la forme
    soit    d 'un objet de type DerivableFunction
    soit d 'un tuple (fonction, [derivee],[ interval])
    soit  d 'une constante
    la derivee est obligatoire pour la fonction  de la temperature 
    """
    def __init__(self,**args):
        self.Args = args
        dict = {}
        dict['ficka_t']='fate'
        dict['ficka_s']='fasa'
        dict['ficka_pa']='fapa'
        dict['ficka_pl']='fapl'
        from functions import DerivableFunction,DerivableFunctionconst,Interval
        import types
        if('ficka_t' not in args):
            raise Exception("FickAirDissousLaw, ficka_t(emperature) doit etre present")

        self.func = []
        for k in args.keys():
            if isinstance(args[k],FloatType) or isinstance(args[k],IntType ):
                argument = DerivableFunctionconst(args[k])
            elif isinstance(args[k],TupleType):
                if len(args[k]) == 3 :
                    if (k == 'ficka_t' ):
                        argument = DerivableFunction(args[k][0], args[k][1], args[k][2])
                    else:
                        if isinstance(args[k][1],Interval):
                            argument = DerivableFunction(args[k][0], args[k][1])
                        elif isinstance(args[k][2],Interval):
                            argument = DerivableFunction(args[k][0], args[k][2])
                        else:
                             raise Exception("Erreur Ficka_s, ficka_pl ou ficka_pa  triplet fourni")
                elif len(args[k]) == 1 :
                    if k == 'ficka_t' :
                        raise Exception("FickAirDissousLaw, ficka_t, Vous devez fournir la derivee")
                    argument = DerivableFunction(args[k][0])
                elif len(args[k]) == 2:
                    if isinstance(args[k][1],Interval):
                        if k == 'ficka_t' :
                            raise Exception("ficka_t, Vous devez fournir la derivee")
                        else:
                            argument = DerivableFunction(args[k][0],interval=args[k][1])
                    else:
                        argument = DerivableFunction(args[k][0],derivee=args[k][1])
                else:
                    pass
            elif  isinstance(args[k],DerivableFunction):
                if k == ('ficka_t' ) and args[k].derivee == None :
                    raise Exception(" ficka_t, Vous devez fournir la derivee")
                if  (k == 'ficka_s' or k == 'ficka_pa' or k == 'ficka_pl' )  and args[k].derivee != None:
                    print(" derivee devrait etre nulle ",k,args[k].derivee) 
                    if args[k].interval == None:
                        fonc =  DerivableFunction(args[k])
                        pass
                    else:
                        fonc =DerivableFunction(args[k].fonction, interval= args[k].interval)
                        pass
                    args[k]=fonc
                    pass
                argument = args[k]
                pass
            else:
                raise Exception("On attend une DerivableFunction, ou une constante ou un tuple")
            self.func.append((argument,dict[k]))
            pass
#traitement des donnees manquantes
        for k in dict.keys():
            if(k not in args):
                argument = DerivableFunctionconst(1.)
                self.func.append((argument,dict[k]))
                pass
            pass
    def getArgs(self):
        return self.Args
            
    
class ThermalconductivityLaw(PhysicalLaw):
    """    
    Thm thermal conductivity based on the product of 3 functions, each having one variable
                     as unknown ( temperature, saturation, porosity) plus a constant.
    Only the function with temperature as unknown is mandatory.
    """
    def __init__(self, **args):
        self.Args = args
        dict = {}
        dict['lamb_t']='late'
        dict['lamb_phi']='lapo'
        dict['lamb_s']='lasa'
        dict['lamb_ct']='laco' 
        from functions import DerivableFunction, DerivableFunctionconst, Interval
        import types      
        if('lamb_t' not in args):
            raise Exception("lamb_t doit etre present")
        if('lamb_ct' in args):
            if( not isinstance(args['lamb_ct'],FloatType) and  not isinstance(args['lamb_ct'],IntType)):
                raise Exception("lamb_ct doit etre constant")
        self.func = []
        for k in args.keys():
            if isinstance(args[k],FloatType) or isinstance(args[k],IntType ):
                argument = DerivableFunctionconst(args[k])
                pass
            elif isinstance(args[k],TupleType):
                if len(args[k]) == 3 :
                    argument = DerivableFunction(args[k][0], args[k][1], args[k][2])
                    pass
                elif len(args[k]) == 1 :
                    if k == 'lamb_t' or k == 'lamb_phi' or k == 'lamb_s':
                        raise Exception("lamb Vous devez fournir la derivee",k)
                    argument = DerivableFunction(args[k][0])
                    pass
                elif len(args[k]) == 2:
                    if isinstance(args[k][1],Interval):
                        if k == 'lamb_t' or k == 'lamb_phi' or k == 'lamb_s':
                            raise Exception("lamb, Vous devez fournir la derivee")
                        else:
                            argument = DerivableFunction(args[k][0],interval=args[k][1])
                            pass
                        pass
                    else:
                        argument = DerivableFunction(args[k][0],derivee=args[k][1])
                        pass
                    pass
                else:
                    pass
                pass
            elif  isinstance(args[k],DerivableFunction):
                if ( k == 'lamb_t' or k == 'lamb_phi' or k == 'lamb_s') and args[k].derivee == None :
                    raise Exception(", Vous devez fournir la derivee")
                argument = args[k]
                pass
            else:
                raise Exception("On attend une DerivableFunction, ou une constante ou un tuple")
            self.func.append((argument,dict[k]))
#traitement des donnees manquantes
        for k in dict.keys():
            if(k not in args):
                if k == 'lamb_ct' :
                    argument = DerivableFunctionconst(0.)
                else:
                    argument = DerivableFunctionconst(1.)
                self.func.append((argument,dict[k]))
                
        return
    def getArgs(self):
        return self.Args
        
class MeanThermalConductivityLaw(PhysicalLaw):
    
    """
    The mean law for thermal conductivity is defined by default as an arithmetic law:
    
    (1.-self.porosity)*self.solidThermalConductivity+self.porosity*self.fluidThermalConductivity
    
    The fluid thermal conductivity is introduced as a constant.
    
    unit : W/m.K    W: J/s  J: N*m  N: m*kg/s**2
    """
    def __init__(self, meanLaw = None):
        if (meanLaw == None) or meanLaw not in ["geometric","harmonic"]:
            print("The mean law for thermal conductivity is defined by default as an arithmetic law")
            self.meanLaw = "arithmetic"
            pass
        else:
            self.meanLaw = meanLaw
            pass
        self.solidThermalConductivity = solidThermalConductivity
        if fluidThermalConductivity == None:
            self.fluidThermalConductivity = 0.
            self.meanLaw = "arithmetic"
            pass
        else:    
            self.fluidThermalConductivity = fluidThermalConductivity
            pass
        self.porosity = porosity
    
    def eval(self,porosity, solidThermalConductivity, fluidThermalConductivity = None):
        if self.meanLaw == "geometric":
            return self.solidThermalConductivity**(1.-self.porosity) + self.fluidThermalConductivity**self.porosity
        elif self.meanLaw == "harmonic":
            return (1.-self.porosity)/self.solidThermalConductivity + self.porosity/self.fluidThermalConductivity
        else:
            return (1.-self.porosity)*self.solidThermalConductivity + self.porosity*self.fluidThermalConductivity
        
    def getLaw(self):
        return self.meanLaw

    pass

    def eval(self,x):
        aux = 1.
        from functions import DerivableFunction
        for k in self.Args.keys():
            if isinstance(self.Args[k],DerivableFunction):
                aux = aux*self.Args[k].eval(x)
                pass
            else:
                aux = aux*self.Args[k]
                pass
        return aux
    pass


#
# The mean heat capacity is based on a ponderation of water and solid heat capacities with dry and wet densities
#
class MeanHeatCapacityLaw(PhysicalLaw):
    """
    The mean heat capacity is based on a ponderation of water and solid calorific capacities with dry and wet densities
    """

    def __init__(self, porosity, solidHeatCapacity, fluidHeatCapacity, solidDensity, fluidDensity):

        if type(porosity) != FloatType:
            raise Exception("porosity must be a float")
        self.porosity = porosity
        memberShip(solidHeatCapacity, HeatCapacity)
        self.solidHeatCapacity = solidHeatCapacity
        memberShip(fluidHeatCapacity, HeatCapacity)
        self.fluidHeatCapacity = fluidHeatCapacity
        memberShip(solidDensity, Density)
        self.solidDensity = solidDensity
        memberShip(fluidDensity, Density)
        self.fluidDensity = fluidDensity
    
    def eval(self):
        """
        evaluation of the mean heat capacity
        """
        auxf = self.porosity*self.fluidDensity
        auxs = (1.-self.porosity)*self.solidDensity
        return (auxf*self.fluidHeatCapacity+auxs*self.solidHeatCapacity)/(auxf+auxs)
        
    ## To get the mean law
    # @return a string corrsesponding of the mean law used
    def getLaw(self):
        return self.meanLaw

    pass
