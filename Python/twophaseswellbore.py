"""
    pressureload: method to get the pressure field all along the pipe.

    It could work with an other module; but, for the moment, it works only with Elmer.

"""
from math import pi, log10
from generictools import color

def wellPressureLoad(transportTool,
                     referencePressure,
                     massFlowField,
                     liquidDensityField,
                     gasDensityField,
                     liquidDynamicViscosityField, 
                     gasDynamicViscosityField, 
                     staticQualityField):

    """
    that method is defined while using the properties of the transport module

    the problem to be solved is supposed to have only one boundary condition; which furnishes the reference pressure

    we suppose here the flow as homogeneous; in other terms that the gas velocity is equal to the liquid velocity.

    That hypothesis is very restricitive if considered with consistency.
    """
    pressureField = [1.e+5]*len(transportTool.coordinates)
    if (transportTool.twoPhasesPressureEvaluationControl == 0):
        transportTool.twoPhasesPressureEvaluationControl = 1
        #pressureField = [1.e+5]*len(transportTool.coordinates)
        #raw_input("we are at the first evaluation of the pressure field")
        for node in range(len(transportTool.coordinates)):
            liquidDensity = liquidDensityField[node]
            dpHydrostaticPerLengthUnit = liquidDensity*transportTool.gravityField[node]
            pressureField[node] = transportTool.deltaL[node]*dpHydrostaticPerLengthUnit
            pressureField[-1] = referencePressure+pressureField[-1]
            pressureField[0] =  pressureField[0]+pressureField[-1]
            pass
        for node in range(1,len(pressureField)-1):
            pressureField[node] = pressureField[node]+pressureField[node-1]
            pass
        return pressureField
    for node in range(len(transportTool.coordinates)):
        #
        # mass flow
        #
#        print color.green+" we deal with node "+color.end,node," at position: ",transportTool.coordinates[node]
        massFlow = abs(massFlowField[node])
#        print " dbg wellPressureLoad mass flow ",node,massFlow
        #
        # materialProperties
        #
        tubeDiameter = transportTool.tubeDiameters[node]
        roughness    = transportTool.roughnesses[node]
#        print " dbg wellPressureLoad tubeDiameter roughness",node, tubeDiameter, roughness
        #
        #
        #
        staticQuality  = staticQualityField[node]
        gasDensity = gasDensityField[node]
        liquidDensity = liquidDensityField[node]
        if (1.-staticQuality) > 1.e-5:
            voidFraction = (staticQuality/gasDensity)/(((1.-staticQuality)/liquidDensity)+(staticQuality/gasDensity))
        else:
            voidFraction = 0
#        print " dbg wellPressureLoad staticQuality ",node,staticQuality
#        print " dbg wellPressureLoad gasDensity ",node,gasDensity
#        print " dbg wellPressureLoad liquidDensity ",node,liquidDensity
#        print " dbg wellPressureLoad voidFraction ",node,voidFraction
#        print " dbg wellPressureLoad gasDynamicViscosityField ",node,gasDynamicViscosityField[node]
#        print " dbg wellPressureLoad liquidDynamicViscosityField ",node,liquidDynamicViscosityField[node]
        #
        # we evaluate mean properties
        #
        #
        # to avoid some values ( to disappear )
        #
        gasDynamicViscosity = min(1,gasDynamicViscosityField[node])
        #gasDynamicViscosity = gasDynamicViscosityField[node]
        
        fluidDynamicViscosity = liquidDynamicViscosityField[node]*(1.-staticQuality) + gasDynamicViscosity*staticQuality
        #gasDynamicViscosityField[node]*staticQuality
        fluidDensity          = gasDensity*voidFraction + liquidDensity*(1-voidFraction)
        #
        #
        #
        if (abs(massFlow) > 0.1):
            reynoldsNumber = 4.*abs(massFlow)/(pi*tubeDiameter*fluidDynamicViscosity)
            A = ((roughness/tubeDiameter)**1.1098)/2.8257 + (7.149/reynoldsNumber)**0.8991
            fD = 0.25*(log10(roughness/tubeDiameter/3.7065 - 5.0452/reynoldsNumber*log10(A)))**-2
            pass
        else:
            fD = 0.
            pass
        dpFrictionPerLengthUnit = fD*8.*abs(massFlow)**2/(fluidDensity*pi**2*tubeDiameter**5)
        dpHydrostaticPerLengthUnit = fluidDensity*transportTool.gravityField[node]
#        if (node <= 2):
        
#            print color.purple+" massFlow "+color.end,massFlow
#            print color.purple+" fluidDensity "+color.end,fluidDensity
#            print color.purple+" tubeDiameter "+color.end,tubeDiameter
#            print color.purple+" roughness "+color.end,roughness
#            print color.purple+" log10(A) "+color.end,log10(A)
#            print color.purple+" roughness/tubeDiameter/3.7065 - 5.0452/reynoldsNumber*log10(A)) "+color.end,roughness/tubeDiameter/3.7065 - 5.0452/reynoldsNumber*log10(A)
#            pass
        dpPerLengthUnit = dpFrictionPerLengthUnit + dpHydrostaticPerLengthUnit
        pressureField[node] = transportTool.deltaL[node]*dpPerLengthUnit
        pass
    pressureField[-1] = referencePressure+pressureField[-1]
    pressureField[0] =  pressureField[0]+pressureField[-1]
    for node in range(1,len(pressureField)-1):
        pressureField[node] = pressureField[node]+pressureField[node-1]
    return pressureField

def hydraulicDiameterEvolution(module,
                               listOfMinerals,
                               listOfMineralsMolarMass,
                               listOfMineralsDensity,
                               waterQualityField):
    """
    The hydraulic diameter evolves due to potential precipitation of minerals.
    the evaluated diameter is sent back to the solver. Its evolution impacts the pressure load.
    
    For the moment, we consider that 100 % of the precipitate is adhering to the pipe;
    that is false from a physical point of view; but enables to be in agreement with the phreeqC phases model.
    
    To evaluate the thickness, we retrieve from phreeqC the quantity of minerals associated to 1L of water.
    From that quantity of water we retrieve an initial thickness using the initial tube diameter.
    Then, we determine which part of the diameter is removed by the mineral precipitation issued from phreeqC. 
    
    """
    initialTubeDiameter = module.transport.boreHoleDiameter
    if len(listOfMinerals)!= 0:
        newDiameterEvaluation = []
        listOfConc = module.chemicalSolver.solver.getPurePhase(listOfMinerals)        # field of concentrations
        numberOfCells = len(module.transportSolver.coordinates)
        print listOfConc
        print "controlling the != lists ",len(listOfConc), len(module.transportSolver.coordinates)*4,numberOfCells
        #raw_input(" controlling the lists")
        for cell in range(numberOfCells):
            volume = 0
            initialTubeRadius = initialTubeDiameter[cell]*0.5
            h = 1./(pi*initialTubeRadius**2)                                               # height for 1L of water
            for mineral in listOfMinerals:
                if ("(g)" in mineral):
                    continue
                ind = listOfMinerals.index(mineral)
                indc = ind*numberOfCells
                numberOfMoles = listOfConc[cell+indc]*(1-waterQualityField[cell])
                massFlow = numberOfMoles*listOfMineralsMolarMass[ind]
                volume+= massFlow/listOfMineralsDensity[ind]
                pass
            #
            # pi*initialR*initialR*h - volume = pi*newR*newR*h
            #
            newDiameter = ((initialTubeRadius**2 - volume/(pi*h))**0.5)*2
            #newDiameterEvaluation[ind] = tubeDiameter[ind] -thickness
            newDiameterEvaluation.append(newDiameter)
            pass
        pass
    return newDiameterEvaluation

    
def wellVelocity(transportTool,
                 massFlowField,
                 liquidDensityField,
                 staticQualityField):
    """
    the well velocity is evaluated in one D and sent back to elmer.
    """
    for node in range(len(transportTool.coordinates)):
        #
        # mass flow
        #
#        print " we deal with node ",node," at position: ",transportTool.coordinates[node]
        massFlow = massFlowField[node]
        tubeDiameter = transportTool.tubeDiameters[node]
        liquiDensity = liquidDensityField[node]
        voidFraction = 0
        velocityField[node] = (massFlow*(1.-staticQualityField[node]))/(pi*tubeDiameter*tubeDiameter/4*liquiDensity*(1 - voidFraction)) # (1-voidFraction) factor to take the gas surface into account.
        pass
    return velocityField

