# -*- coding: utf-8 -*-
"""

A. Dimier 

G.P.L. 

A list of functions to be useful for the simulation

Dictionnaries enable the interpolation switch 

        we can obtain here:

                the water density as a function of temperature
                
                the water density as a function of pressure
                
                the water density as a function of pressure and density changes
                
                the arguments are temperature and salinity.
                
                Temperature is mandatory, salinity is optional
                
                The references are given within the functions 

"""
from math import log,log10,exp

volumetricExpansionCoefficient = {

10:[88.e-6,999.80],
20:[207e-6,997.73],
30:[303e-6,994.71],
40:[385e-6,990.90],
50:[457e-6,986.39],
60:[522e-6,981.27],
70:[582e-6,975.59],
80:[640e-6,969.39],
90:[695e-6,962.70],
100:[695e-6],

} ## source Matt Web

def volumeExpanCoefWater(temperature):
    """
    An affine interpolation is made between data linking temperature
    and expansion coefficient.
    The temperature limits are:
    
        lower:  10. °C
        higher  99. °C
    """
    temperature = int(temperature)
    lowerLimit = (temperature // 10)*10
    upperLimit = lowerLimit + 10
    if lowerLimit < 10 or upperLimit > 100:
        raise Exception, "check the data"
    coef0 = volumetricExpansionCoefficient[lowerLimit][0]
    coef1 = volumetricExpansionCoefficient[upperLimit][0]
    print coef0,coef1
    return volumetricExpansionCoefficient[lowerLimit][1], lowerLimit, coef0 + (coef1-coef0)*(temperature-lowerLimit)/10.

def waterSpecificEnthalpy(temperature, salinity = None):
    """
    References:
    
    Heat capacities and enthalpies of sea salt solutions to 200.deg.
    Leroy A. Bromley, Anthony E. Diamond, Emilio Salami, David G. Wilkins
    J. Chem. Eng. Data, 1970, 15 (2), pp 246–253
       
    The IAPWS Formulation 1995 for the Thermodynamic Properties of Ordinary Water Substance for General and Scientific Use
    Wagner and PruB
    
    temperature:        Celcius degree
    salinity            [g/kg]
    
    specific enthalpy:          [J/kg]
    
    Specific enthalpy of seawater at 0.1 MPa (atmospheric pressure)
    
    validity range:
    
                10 < T < 120 C
                 0 < S < 120 g/kg
    """
    t = temperature
    if t<0 or t> 120:
        raise Exception, " Specific Enthalpy: the temperature range validity for temperature is [0:120] "
    s = salinity
    if salinity == None:
        s = 0.
        print "salinity:",s
    if s>=-1.e-20 and s<120.:
        specEnthalpy = 141.355 + 4202.07*t - 0.535*t**2 + 0.004*t**3
        a10  =-2.34825E+04;
        a20  = 3.15183E+05;
        a30  = 2.80269E+06;
        a40  =-1.44606E+07;
        a11  = 7.82607E+03;
        a12  =-4.41733E+01;
        a13  = 2.13940E-01;
        a21  =-1.99108E+04;
        a31  = 2.77846E+04;
        a22 = 9.72801E+01;
    
        return specEnthalpy - s*(a10 + a20*s + a30*s**2 + a40*s**3 + a11*t + a12*t**2 + a13*t**3 + a21*s*t + a31*(s**2)*t + a22*s*t**2)
    else:
        raise Exception, " Specific Enthalpy: the salinity range validity for temperature is [0:120] g/kg "

def waterLDensity(temperature):
    """
    rho1 = rho0 /(1+beta * (T1 - T0))
    """
    rho0, lowerLimit, beta = volExpanCoefWater(temperature)
    print rho0, lowerLimit, beta, temperature - lowerLimit
    
    return rho0 / (1. + beta * (temperature - lowerLimit))
    
def freshWaterDensity(temperature):
    """
    G. S. Kell (1975) J. Chem. Engng Data, 20(1), 97–105
    temperature is in Celcius degrees
    """
    from math import pow
    t = temperature
    if temperature > 273.15:# introduced to take kelvin temperature into account, temperature range supposed to be 0,100 Cel.
        temperature-=273.15
    return (999.83952 + 16.952577*t-7.9905127e-3*pow(t,2)-46.241757e-6*pow(t,3)+105.84601e-9*pow(t,4)-281.0301e-12*pow(t,5))/(1.+16.887236e-3*t)
    
def waterViscosity(temperature):
    """
    Dynamic viscosity is related to shearing stress:
    
        shearing stress = dynamic viscosity * dc/dy
    Viscosity-temperature correlation for liquids
    Christopher J. Seeton
    Tribology Letters, Vol. 22, N 1 April 2006
    
    viscosity of water:          [kg/m-s]
    
    1 Pa.s = 1 N s m** -2 = 1 kg/m-s
    
    Temperature is entered here in Celcius degrees
    """
    t = temperature
    return 2.414e-5*(10**(247.8/(t + 133.15)))
    
def salineWaterViscosity(temperature,salinity):
    """
    Desalination and Water Treatment, 2009
    Sharqawy M. H., Lienhard J. H., and Zubair, S. M., 

    IAPWS release on the viscosity of ordinary water substance 2008
    
    viscosity of water:          [kg/m-s]
    
    1 Pa.s = 1 N s m** -2 = 1 kg/m-s
    
    Temperature is entered here in Celcius degrees
    
    salinity in kg per kg
    
    """
    T = temperature
    s = salinity
    a1 = 1.5700386464E-01
    a2 = 6.4992620050E+01
    a3 = -9.1296496657E+01
    a4 = 4.2844324477E-05
    #
    a5 = 1.5409136040E+00
    a6 = 1.9981117208E-02
    a7 = -9.5203865864E-05
    a8 = 7.9739318223E+00
    a9 = -7.5614568881E-02
    a10 = 4.7237011074E-04
    #
    # viscosity with salinity equals to zero
    #
    mu = a4 + 1/(a1*(T+a2)**2+a3)
    A = a5 + a6 * T + a7 * T**2
    B = a8 + a9 * T + a10* T**2
    
    return mu*(1+ A*s + B*s**2)


def freshWaterSpecificHeat(temperature):
    """
    D. T. Jamieson, J. S. Tudhope, R. Morris, and G. Cartwright, 
      Physical properties of sea water solutions: heat capacity,
       Desalination, 7(1), 23-30, 1969
    
    temperature:        Celcius degree
    salinity            [g/kg]
    specific heat:          [J/kg K]
    
    Specific heat of seawater at 0.1 MPa
    
    """
    t = temperature
    if t<0 or t> 180:
        raise Exception, " SpecificHeat: the temperature range validity for temperature is [0:180] "
    return 4209.4 - 1.824*t + 3.0525e-2*t**2 - 1.2388e-4*t**3 + 1.2774e-7*t**4

def thermalConductivity(temperature, salinity = None):
    """
    REFERENCES:
        [1] D. T. Jamieson, and J. S. Tudhope, Desalination, 8, 393-401, 1970.
    INPUT:  (all must have same dimensions)
    t = temperature in degree C
    s = salinity    in g/kg
    
    OUTPUT:
        thermal conductivity [W/m K]
    """
    t = temperature
    s = salinity
    if t<0 or t> 180:
        raise Exception, " thermal conductivity: the temperature range validity is [0:180] C "
    if s<0 or s> 160:
        raise Exception, " thermal conductivity: the salinity range validity is [0:160] g/kg"
    t = 1.00024 * t     # convert from T_90 to T_68
    s = s / 1.00472     # from S to S_P
    return 0.001*(10**(log10(240+0.0002*s)+0.434*(2.3-(343.5+0.037*s)/(t+273.15))*((1-(t+273.15)/(647.3+0.03*s)))**(1./3.)));

def waterSpecificHeat(temperature, salinity = None):
    """
    D. T. Jamieson, J. S. Tudhope, R. Morris, and G. Cartwright, 
      Physical properties of sea water solutions: heat capacity,
       Desalination, 7(1), 23-30, 1969
    
    temperature:        Celcius degree
    salinity            [g/kg]
    specific heat:          [J/kg K]
    
    Specific heat of seawater at 0.1 MPa
    
    """
    t = temperature
    if t<0 or t> 180:
        raise Exception, " SpecificHeat: the temperature range validity for temperature is [0:180] "
    s = salinity
    if salinity == None:
        return 4209.4 - 1.824*t + 3.0525e-2*t**2 - 1.2388e-4*t**3 + 1.2774e-7*t**4
        pass
    elif s>0 and s<180:
        a = 4206.8e+0 - s*(6.6197e+0 + s*1.2288e-2)
        b =-1.1262e+0 + s*(5.4178e-2 - s*2.2719E-4)
        c = 1.2026e-2 - s*(5.3566e-4 + s*1.8906e-6)
        d = 6.8777e-7 + s*(1.5170e-6 - s*4.4268e-9)
        return (a + t*(b + t*(c* + t*d)))
    else:
        raise Exception, " SpecificHeat: the salinity range validity for temperature is [0:180] g/kg "
        
    
    
def waterDensity(temperature, salinity = None):
    """
    Mc Cutcheon, S.C. Martin, J.L. Barnwell, T.O. Jr. 1993
    Water Quality in Maidment
    Handbook of Hydrology
    Mc Graw-Hill, N.Y. 
    temperature in Celcius degree)
    """
    from math import pow
    t = temperature
    s = salinity
    if s == None:
        s = 0.
    rho0 = 1000.*(1-(t+288.9414)/(508929.2*(t+68.12963))*pow(t-3.9863,2))
    a = 8.24493e-1 - 4.0899e-3*t + 7.6438e-5*pow(t,2) -8.2467e-7*pow(t,3) + 5.3675E-9*pow(t,4)
    b =-5.724e-3 + 1.0227E-4*t - 1.6546E-6*pow(t,2)
    c = 4.8314e-4
    return rho0 + s * ( a + s*c) + b * pow(s,1.5)
    
def pressWaterDensity(temperature,pressure):
    """
    G. S. Kell (1975) J. Chem. Engng Data, 20(1), 97–105
    """
    from math import pow
    t = temperature
    p = pressure # in Pa (N/m2)
    E = 2.15e+9  # in Pa (N/m2)
    p0 = 101325  # in Pa (N/m2)
    return (999.83952 + 16.952577*t-7.9905127e-3*t**2-46.241757e-6*t**3+105.84601e-9*t**4-281.0301e-12*t**5)\
    /(1.+16.887236e-3*t)/(1.-(p-p0)/E)

def volumeExpanCoefWater(temperature):
    """
    An affine interpolation is made between data linking temperature
    and expansion coefficient.
    The temperature limits are:
    
        lower:  10. °C
        higher  99. °C
    """
    temperature = int(temperature)
    lowerLimit = (temperature // 10)*10
    upperLimit = lowerLimit + 10
    if lowerLimit < 10 or upperLimit > 100:
        raise Exception, "check the data temperature must lie in [10.,100.]"
    coef0 = volumetricExpansionCoefficient[lowerLimit][0]
    coef1 = volumetricExpansionCoefficient[upperLimit][0]
    print coef0,coef1
    return volumetricExpansionCoefficient[lowerLimit][1], lowerLimit, coef0 + (coef1-coef0)*(temperature-lowerLimit)/10.

def pressWaterHeatCapacity(temperature, pressure):
    """
    the Source: algorithms for computation of fundamental properties of seawater
                UNESCO report 44
    Salinity is fixed to zero 
    The temperature validity range is set to [0,50]
    The pressure validity range has been set to [1,100]
    the polynomial used should be changed to broaden the validity range
    """
    p = pressure
    t = temperature - 0.01
    a0 = -4.9592e-1
    a1 = 1.45747e-2
    a2 =-3.13885e-4
    a3 = 2.03570e-6
    a4 = 1.71680e-8
    
    b0 = 2.4931e-04
    b1 =-1.08645e-5
    b2 = 2.87533e-7
    b3 =-4.0027e-09
    b4 = 2.2956e-11
    
    c0 =-5.4220e-08
    c1 = 2.6380e-09
    c2 =-6.5637e-11
    c3 = 6.1360e-13
    
    cp_t = 4217.4 +t* (-3.720283 + t*(0.1412855 +t*(- 2.654387e-3 + t*2.093236e-5)))
    print " cp_t ",cp_t
    return cp_t + p* (a0 + t* (a1 + t*(a2 + t*(a3 + t*a4))) +\
           p* (b0 + t* (b1 + t*(b2 + t*(b3 + t*b4))) +\
           p* (c0 + t* (c1 + t*(c2 + t*c3))) ))

def surfaceVolumeFactor(porosity, density, grainDiameter):
    """
    That function enables to determine the surface to volume factor in the lasaga kinetic formulation A/V * ki * (1 -SR)
    
    units are SI units: kg m s
    """
    grainRadius = 0.5*grainDiameter
    
    grainSurface = 4.*3.1415926535897931*grainRadius**2         # surface of 1 grain
    
    print "grainSurface %e\n"%grainSurface
    
    grainVolume = grainSurface*grainRadius/3.                   # volume of 1 grain
    
    print "grainVolume %e\n"%grainVolume
    
    vMineral = 1./density                                       # volume of one kg of mineral
    
    numberOfGrains = vMineral/grainVolume                       # number of grains in 1 kg of mineral
    
    print " number of grains %e\n"%numberOfGrains
    
    A = numberOfGrains * grainSurface                           # surface area of 1 kg mineral
    
    V = vMineral*porosity/(1.-porosity)
    
    print " A : ",A," in  m2/kg V : ",V," in m-3"
    
    return A/(V*1000)
    
def hydraulicConductivity(intrinsicPermeability, temperature, salinity = None, g = None):
    """
    K = k *rho * g /mu
    
    K  is the hydraulic conductivity (m/s)
    k  is the intrinsic permeability (m**2)
    g  is the gravity                (m/s/s)
    mu is the viscosity              (kg/m:s)
    
    the fluid is supposed to be water; the temperature is expressed in Celsius degrees
    
    salinity is expressed in g/kg
    
    """
    if g == None:
        g = 9.8
    if salinity == None:
        salinity = 0.0
    elif salinity > 1:
       raise Warning, " salinity should be lower than 120 g/kg"
    if temperature > 100:
        raise Warning, " temperature should be expressed in Celcius degrees and lower than 100 Celcius degree"
      
    rho = waterDensity(temperature, salinity)
    mu  = waterViscosity(temperature)
    return intrinsicPermeability*rho*g/mu

def radius(density, surface):
    """
    that function is used to determine the radius from a given surface contact area
    surface is the surface contact area in contact with 1kg soil
    
    """        
    radius = 3./density/surface
    print radius
    
    return (1./density)*porosity/(1.-porosity)

def contactV1(density, porosity = None):
    """
    that function is used to determine volume of water in contact with 1kg soil
    
    volume of 1 kg soil is 1./density ((density in kg/m3)
    
    volume of water in contact with 1kg soil = volume of 1kg soil * porosity / (1. - porosity)
    
    """
    return 1.

def contactV2(density, porosity = None, percent = None):
    """
    that function is used to determine volume of water in contact with 1kg soil
    
    volume in m3 of 1 kg soil is 1./density ((density in kg/m3)
    
    volume of water in m3 in contact with 1kg soil = volume of 1kg soil * porosity / (1. - porosity)
       
    Specific surface area is a material property of solids which measures the total surface area per unit of mass,
    solid or bulk volume[2], or cross-sectional area, the unit is m2/kg.
    
    """        
#    radius = 3./density/surface
#    print radius
    if percent == None:
        percent = 1.
    
    return percent*(1./density)*(porosity/(1.-porosity))


def log10k(temperature, coef):
    """
      The log K is evaluated through the list of coefficients of the phreeqC formula:
      
        log10k = A1 + A2T + A3/T + A4log10T + A5/T/T 

        T is in Kelvin
    """
    print temperature
    print coef
    return coef[0] + coef[1]*temperature + coef[2]/temperature + coef[3]*log10(temperature) + coef[4]/(temperature*temperature)

def logtrk(temperature, coef):
    """
      The log K is evaluated through the list of coefficients of the toughreact formula: Record-4-3
      
        log10k = a*ln(Tk) + b +c*Tk + d/Tk + e/(Tk**2)

        T is in Kelvin
    """
    print temperature
    print coef
    return coef[0]*log(temperature) + coef[1] + coef[2]*temperature + coef[3]/temperature + coef[4]/(temperature*temperature)
    
def km(k25, Ea, temperature, referenceTemperature = None):
    """
    
    Arrhenius equation:
    
    the Arrhenius equation gives "the dependence of the rate constant k of chemical reactions on the temperature T
    (in    absolute temperature kelvins) and activation energy Ea", as shown below:[1]


    
    Ea: energy of activation in J/mol
    
    k25*exp(-Ea*((1./temperature) - (1./298.15))/R)
    
    R, the univeral constant expressed in J/[mol-K] takes the value 8.314
    """
    if referenceTemperature == None:
        referenceTemperature = 298.15
    return k25*exp(-Ea*((1./temperature) - (1./referenceTemperature))/8.314)

