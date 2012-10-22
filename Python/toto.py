from types import ListType, TupleType, IntType, FloatType
from tables import Table
class PhysicalLaw:
    """
    A class used as a basis object for a physical law function.

    Example:    Heat capacity for a porous medium is a function of porosity, water and solid heat capacities.
                these three physical quantities will be the parameters, the arguments, the return value being
                the mean heat capacity evaluation
    """
    def getValue(self):
        return self
        
    pass
 
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
    Common Container to describe an intrinsic permeability law
    Example Carman-Kozeny
    """
    def __init__(self,**args):
        print args
        lexikon = args
        self.args = args
        print lexikon
        if lexikon.has_key("initialPorosity"):
            self.initialPorosity = lexikon["initialPorosity"]
        else: 
            raise Exception(" the initial porosity is mandatory for the IntrinsicPermeabilityLaw defintion")
        if lexikon.has_key("k0"):
            self.k0 = lexikon["k0"]
        else:
            self.k0 = 1.0
            raise Warning, " the k0 constant has been set to one"
    pass
    
class KozenyCarmanLaw(IntrinsicPermeabilityLaw):

    def __init__(self,**args):
        print " args ",args
        IntrinsicPermeabilityLaw.__init__(self,**args)
    def eval(self,currentPorosityValue):
        print currentPorosityValue,self.k0,self.initialPorosity
        return  self.k0*pow((1.-self.initialPorosity)/(1.-currentPorosityValue),2)/pow(currentPorosityValue/self.initialPorosity,3)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Effective diffusion laws (function of porosity)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class EffectiveDiffusionLaw(PhysicalLaw):
    """
    Container to describe an effective diffusion law
    The difusion law will express diffusion as a function of porosity
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
        if lexikon.has_key("cementationCoefficient"):
            cementationCoefficient = lexikon["cementationCoefficient"]
            if type(cementationCoefficient) != FloatType:
                raise Warning, " the cementationCoeficient must be a float it has been set to zero"
                self.cementationCoefficient = 0.0
            else:
                self.cementationCoefficient = cementationCoefficient
        else:
            raise Exception(" the cementation coefficient is mandatory for the WinsauerDiffusionLaw definition")
            pass
        if lexikon.has_key("percolationPorosity"):
            percolationPorosity = lexikon["percolationPorosity"]
            if type(percolationPorosity) != FloatType:
                raise Warning, " the percolationPorosity must be a float"
                self.percolationPorosity = 0.0
                pass           
            else:
                self.percolationPorosity = percolationPorosity
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
        
b = IntrinsicPermeabilityLaw(initialPorosity = 1,k0 = 0)
d = IntrinsicPermeabilityLaw(initialPorosity = 1)
b = KozenyCarmanLaw(initialPorosity = 1,k0 = 0)
c = WinsauerDiffusionLaw(cementationCoefficient=1.0,percolationPorosity = 0.2)

d = table(name = "toto")

