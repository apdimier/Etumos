#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This file is used to enable the introduction of 
# user defined functions. Through that way, the user can 
# introduce its own programming to handle specific parameters
# or physical parameters. The user has to pay attention to the 
# unknown definition due to the python paradigms:
# Every external variable and every method should have us as prefix
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from __future__ import print_function
from __future__ import absolute_import
from six.moves import input
def totoUser():
    print("It works")
    return None
    
def userList(ctmi):
    """
    the user defines here the lists involved in the user defined functions
    """
    ctmi.initialPorosity = []
    pass
def userTuple(ctmi):
    """
    the user defines here the lists involved in the user defined functions
    """
    pass
    
def effectiveYoungModulus0(ctmi):
    """
     Setting the porosity to variable, you 
     construct here the following effective Young modulus
    
     E = E0(1-w/w0)**f 
    """
#    print "It works too: ",ctmi.cpuTime()
    E0 = 57.73
    f = 2.1
    ctmi.usE = []
    porosityField = ctmi.chemical.getPorosityField()
    if ctmi.initialPorosity == []:
        for i in porosityField:
            ctmi.initialPorosity.append(i)
            pass
        pass
    ind = 0
    for i in porosityField:
        aux = E0*(1-i/ctmi.initialPorosity[ind])**f
        ctmi.usE.append(aux)
        ind+=1
        pass
    print(" effective Young modulus ",porosityField[0:10])
    pass
    
def effectiveYoungModulus(ctmi):
    """
     Setting the porosity to variable, you 
     construct here the following effective Young modulus
    
     E = E0(1-w/w0)**f 
    """
#    print "It works too: ",ctmi.cpuTime()
    E0 = 57.73
    f = 2.1
    ctmi.usE = []
    porosityField = ctmi.chemical.getPorosityField()
    if ctmi.initialPorosity == []:
        for porosity in porosityField:
            ctmi.initialPorosity.append(porosity)
            pass
        pass
    ind = 0
    for porosity in porosityField:
											    #
											    # We setup the list of updated Young moduli
											    #
        ctmi.usE.append(E0*(1-porosity/ctmi.initialPorosity[ind])**f)
        pass
#    print " effective Young modulus ",ctmi.usE[0:10]
    pass

    
def brasilianTestLaw(ctmi):
    """
     Setting the porosity to variable, you 
     construct here the following effective Young modulus.
     
     We feed the usE list which will be transmitted to the mechanical solver via the mechanical modulus.
    
     E = E0((1-w)/(1.-w0))**f 
    """
    print("It works too, brasilianTestLaw: ",ctmi.cpuTime())
    E0 = 57.73
    f = 2.1
    ctmi.usE = []
    porosityField = ctmi.chemical.getPorosityField()
    if ctmi.initialPorosity == []:
        for porosity in porosityField:
            ctmi.initialPorosity.append(1. - porosity)
            pass
        pass
    ind = 0
    for porosity in porosityField:
											    #
											    # We setup the list of updated Young moduli
											    #
        ctmi.usE.append(E0*((1-porosity)/ctmi.initialPorosity[ind])**f)
        pass
#    print " effective Young modulus ",ctmi.usE[0:10]
    pass
    
def heatConductivityLawCelcius(ctmi):
    """
    To set the thermal conductivity
    
      k(T) =  0.5636 +1.946 * 1.e-3 * T -8.151 * 1.e-6 * T**2
      
      http://syeilendrapramuditya.wordpress.com/2011/08/20/water-thermodynamic-properties
    """
    ctmi.usE = []
    temperatureField = ctmi.transport.getTemperatureField()
    thermalConductivityField = []
    for temperature in temperatureField:
        thermalConductivityField.append(0.5636 +1.946 * 1.e-3 * temperature -8.151 * 1.e-6 * temperature*temperature)
        pass
    pass
    
def heatConductivityLawKelvin0(ctmi):
    """
    To set the thermal conductivity
    
      k(T) =  -0.5752 + 6.397 * 1.e-3 * T -8.151 * 1.e-6 * T**2
      
      http://syeilendrapramuditya.wordpress.com/2011/08/20/water-thermodynamic-properties
    """
    ctmi.usE = []
    temperatureField = ctmi.transport.getTemperatureField()
    thermalConductivityField = []
    for temperature in temperatureField:
        thermalConductivityField.append(-0.5752 + 6.397 * 1.e-3 * temperature -8.151 * 1.e-6 * temperature*temperature)
        pass
    pass
    
def heatConductivityLawKelvin1(ctmi):
    """
    To set the thermal conductivity
    
      k(T) =  -1.48445 + 4.12292 *  T - 1.63866 * T**2 with T = T/298.15
      
      ref. conductivity is at 298.15 : 0.6065 W/ m/ K
      
      Standard Reference Data for the Thermal Conductivity Of Water
      
      M. L. V. Ramires and Al.: http://www.nist.gov/data/PDFfiles/jpcrd493.pdf
      
    """
    input("evaluating the thermal conductivity ")
    refConductivity = 0.6065
    ctmi.usE = []
    temperatureField = ctmi.transport.getTemperatureField()
    thermalConductivityField = []
    for temperature in temperatureField:
        temp = temperature/298.15
        thermalConductivityField.append(-1.48445 + 4.12292 * temperature - 1.63866 * temperature*temperature)*refConductivity
        pass
    pass
    ctmi.transport.setWHeatConductivityField(thermalConductivityField)

