# -*- coding: utf-8 -*-
"""
datamodel file to be imported in user script

_moduleDict = {
    "chemistry"            : chemistry,
    "chemicaltransport"    : chemicaltransport,
    "saturatedhydraulic"   : hydraulicproblem,
    }

    For the moment only these 3 problems are treated.

"""
from __future__ import absolute_import
from functions import *
#from tabulatedfunctions import makeHistogram, makeConstantFunction, ConstantFunction, makePWLinearFunction

from timespecification import SequenceTimeSpecs,\
                              TimeSequence,\
                              TimeSpecification

from posttables import Table,makeTableFromFile

##from graphs import *

from material import Material

from commonmodel import Cylinder,\
                        DiscreteEdge, \
                        Edge,\
                        Region
#
from PhysicalQuantities import MolesAmount


from PhysicalQuantities import Concentration,\
                               ConcentrationFlux,\
                               ConcentrationGradient,\
                               ConcentrationRate,\
                               SolidConcentration

from PhysicalProperties import AquiferProperty,\
                               Density,\
                               EffectiveDiffusion,\
                               KinematicDispersion,\
                               MolarMass,\
                               Permeability,\
                               PoissonRatio,\
                               PoreCompressibility,\
                               PoreDiffusion,\
                               Porosity,\
                               ReactionRate,\
                               RetardationFactor,\
                               SolidDensity,\
                               SpecificHeat,\
                               ThermalConductivity,\
                               Tortuosity,\
                               Velocity,\
                               YoungModulus

from PhysicalQuantities import Mass

#from radioelements import DecayReaction, DecayChain, Reaction, DecayChains

from species import AqueousMasterSpecies,\
                    AqueousSecondarySpecies,\
                    Element,\
                    GaseousSecondarySpecies,\
                    MasterSpecies,\
                    MineralSecondarySpecies,\
                    RedoxCouple,\
                    SecondarySpecies, \
                    SorbedSecondarySpecies,\
                    SorbingMasterSpecies, \
                    SorbingSiteMasterSpecies,\
                    Species,\
                    SurfaceSecondarySpecies,\
                    SurfaceSiteMasterSpecies

from tensors import Tensor2D, Tensor3D
from chemistry import ChemicalQuantity,Activity, SpeciesConcentration, \
     SpeciesMassConcentration, SpeciesMolalConcentration, ElementConcentration, \
     ElementMassConcentration, ElementMolalConcentration, TotalConcentration, \
     TotalMassConcentration, TotalMolalConcentration, MineralConcentration, MineralTotalConcentration, \
     MineralTotalMassConcentration, MineralTotalMolalConcentration, Fugacity , \
     SpecificSurfaceArea, SpecificAreaPerGram, VolumicSurfaceArea, RelativeTotalConcentration , \
     KineticLaw, ReversibleKineticLaw, ActivityLaw, Davies, TruncatedDavies, DebyeHuckel, Bdot , \
     ChemicalState, AqueousSolution, MineralPhase, GasPhase, \
     IonicExchangers, SurfaceComplexation, ExchangeBindingSpecies, ExchangeMineralBindingSpecies, \
     SolidSolution, SurfaceBindingSpecies, SurfaceMineralBindingSpecies
##import points
from vector import V as Vector   
from physicallaws import *

from chemistry import ChemicalProblem
from chemicaltransport import ChemicalTransportProblem
import chemistry
import chemicaltransport
import coupledTHMCmodule
import hydraulicproblem
from hydraulicproblem import HydraulicProblem

_problemType = None

_moduleDict = {
    "chemistry"            : chemistry,
    "chemicaltransport"    : chemicaltransport,
    "chemicalmechanics"    : coupledTHMCmodule,
    "saturatedhydraulic"   : hydraulicproblem,
    }

_message  = '\n\n'
_message += "Please, set the type of problem with setProblemType(name)\n"
_message += "where name is in :\n\n"
for name in _moduleDict.keys():
    _message += name + '\n'
    pass

def setProblemType(name):
    """ This method sets the current type of the problem """
    from types import StringType
    if type(name) != StringType:
        raise TypeError(" the name argument within SetProblemType should be a string ")
    _name = name.lower()
    #raw_input("we are at that level")
    global _problemType
    if _name in _moduleDict:
        _problemType = _name
        pass
    else:
        message  = "\n\n"
        message += "ProblemType : "+name+" ... unknown !"
        message += _message
        raise RuntimeError(message)
    return

def checkIfProblemTypeIsSet():
    if _problemType: return
    raise RuntimeError(_message)

def BoundaryCondition(*liste, **dico):
    #raw_input("BoundaryCondition ")
    checkIfProblemTypeIsSet()
    module = _moduleDict[_problemType]
#    print "type of 1",module
#    print "type of 2",liste
    #raw_input("toto")
    return module.BoundaryCondition(*liste, **dico)

def InitialCondition(*liste, **dico):
    #raw_input("InitialCondition ")
    checkIfProblemTypeIsSet()
    module = _moduleDict[_problemType]
    #print "type of ",type(module.InitialCondition(*list, **dict))
    #raw_input()
    return module.InitialCondition(*liste, **dico)

def Source(*list, **dict):
    checkIfProblemTypeIsSet()
    if _problemType in ['unsaturatedhydraulic', 'transienthydraulic','saturatedhydraulic']:
        return hydraulicproblem.Source(*list, **dict)
    else:
        module = _moduleDict[_problemType]
        return module.Source(*list, **dict)

def ZoneCondition(*list, **dict):
    checkIfProblemTypeIsSet()
    if _problemType in ['unsaturatedhydraulic', 'transienthydraulic','saturatedhydraulic']:
        return hydraulicproblem.Source(*list, **dict)
    else:
        module = _moduleDict[_problemType]
        return module.ZoneCondition(*list, **dict)

def ExpectedOutput(*list, **dict):
    checkIfProblemTypeIsSet()
    module = _moduleDict[_problemType]
    return module.ExpectedOutput(*list, **dict)    
