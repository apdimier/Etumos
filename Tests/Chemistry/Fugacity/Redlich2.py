from math import pi,acos,cos,log,exp
#
# list solubility as a function of temperature, pressure in bars is self explained
#
DuanValues_at100b = [(303.15,1.0958),(333.15,0.8405),(363.15,0.6767),(393.15,0.6015),(423.15,0.5759),(453.15,0.5751),(483.15,0.5755)]

DuanValues_at200b = [(303.15,1.1990),(333.15,1.0072),(363.15,0.9259),(393.15,0.9052),(423.15,0.9337),(453.15,1.0035),(483.15,1.1016)]

def cubeRoots(x):
    """Find three complex cube roots of real or complex x."""
    z = x + 0j
    s = 1
    if z.real < 0:
        z,s = -z,-s
    t = math.atan2(z.imag, z.real)/3
    a = s * (abs(z)**(1./3))
    w = complex(-0.5,math.sqrt(0.75))
    w_ = w.conjugate()
    u = a * complex(math.cos(t),math.sin(t))

def lameta(temperature,pressure):
    """
    to calculate the CO2 activity, the virial expansion of Gibbs is used  (Pitzer extension)
    The reference formula is found in the article of Duan and sun (2003)
    That extension being used only by considering CO2/Na and CO2/NaCl interactions, the extension is
    limited to up to 6 coefficients compared to the reference of Duan and Sun
    The initial extension for the activity coefficients is :

        Par(T,P)=c1+c2T+c3/T+c4T2+c5/(630−T)+c6P+c7PlnT+c8P/T+c9P/(630−T)+c10P2/(630−T)2+c11TlnP

    while the extension here is:

        Par(T,P)=c1+c2T+c3/T+c4*p/T+c5*p/(630−T)+c6TlnP

    """
    print "lameta temperature",temperature,pressure
    lc1 = -0.411370585
    lc2 =  6.07632013e-4
    lc3 = 97.5347708
    lc4 = -0.0237622469
    lc5 =  0.0170656236
    lc6 =  1.41335834e-5
#
    ec1 =  3.36389723e-4
    ec2 = -1.98298980e-5
    ec4 =  2.12220830e-3
    ec5 = -5.24873303e-3
#
# lamdda coefficient associated to  CO2/Na interaction
#
    c1 = lc1 +\
         lc2 * temperature +\
         lc3 / temperature +\
         lc4 * pressure/temperature +\
         lc5 * pressure/((630 - temperature)) +\
         lc6 * temperature*log(pressure) # neperian logarithm
#
# lamdda coefficient associated to  CO2/Na interaction
#
    c2 = ec1 +\
         ec2 * temperature +\
         ec4 * pressure/temperature +\
         ec5 * pressure/((630 - temperature))
    return c1,c2
    
def co2Fugacity(V,R,temperature,pressure,aco2,bco2):
    """
    We use the Prausnitz formulation to evaluate the fugacity coefficient. 
    The mole fraction of CO2 is approximated to 1. in the CO2 gas phase to avoid an iterative algorithm.
    
    Reference:
    International journal of greenhouse gas control 2 (2008) 65-77 Hassan Hassanzadeh

    Reminder: F

    For a perfect gas, the fugacity is equal to pressure. In the case of a
    component Gi , we have its activity Ai which is related to pressure by the
    relation Ai = Gi . Fi / p0. Fi is the fugacity,
    Gi the activity coefficient and p0 the standard pressure.
    
    As supposed   
    """
    #
    cte = R*(temperature**1.5)*bco2
    #
    phico2 = log(V/(V - bco2)) + (bco2/(V - bco2)) - \
        (2.*(1.*aco2)/( cte ) ) * log((V + bco2)/V) + \
        (aco2*bco2/(cte*bco2))*(log((V + bco2)/V) - (bco2/(V + bco2)) ) - \
        log(pressure*V/(R*temperature))
    phico2 = exp(phico2)
    raw_input(" phico2 "+str(phico2))
    return phico2

def h2oFugacity(V,R,temperature,pressure,aco2,bco2):
    """
    We use the Prausnitz formulation to evaluate the fugacity coefficient.
    
    Reference:
    International journal of greenhouse gas control 2 (2008) 65-77 Hassan Hassanzadeh
    
    We suppose yh2o = 0.
    
    """
    bh2o = 18.18                        # cm3.mol-1
    ah2o_co2 = 7.89e+7                  # bar.cm6.K0.5.mol-2
    am = aco2
    bm = bco2
    #
    cte = R*(temperature**1.5)*bm
    #
    phih2o = log( V / (V - bm) ) + ( bh2o / (V - bm) ) - \
        (2.*(1.*ah2o_co2)/( cte) )*log( (V + bm) / V) + \
        ( am*bh2o/(cte*bm) ) * ( log( (V + bh2o)/V) - (bm/(bm + V) ) ) - \
        log(pressure*V/(R*temperature))
    phih2o = exp(phih2o)
    raw_input(" phih2o "+str(phih2o))
    return phih2o
#
def cbrt(x):
    from math import pow
    if x >= 0:
        return pow(x, 1.0/3.0)
    else:
        return -pow(abs(x), 1.0/3.0) 
#
def polyCubicRoots(a, b, c):
    """
    we solve a monic cubic polynom: x3 + a * x2 + bx +c = 0
    see, among others,  Nickalls for a discussion about the solution
    
    A new approach to solving the cubic: Cardan's soluion revvealed
    1993
    The  Math. Gazette
    """
    xn = a / 3.0
    p = b - a*xn
    q = (2.*(xn**2) - b)*xn + c
    X =(p/3.0)**3
    Y = (q/2.0)**2
    Q = X + Y
    #
    # only one real root
    #
    if Q >= 0:
        sqQ = (Q)**0.5
#
#        A= (-q/2.0 + sqQ)**(1/3.0)
#        B= (-q/2.0 - sqQ)**(1/3.0)
#

        A= cbrt(-q/2.0 + sqQ)
        B= cbrt(-q/2.0 - sqQ)
        r1 = A + B- xn
        re = -(A+B)/2.0-xn
        im = (3.0)**0.5/2.0*(A-B)
        r2 = (re,im)
        r3 = (re,-im)
        return r1
    #
    # three real roots
    #
    else:
        p3by27= (-p**3/27.0)**0.5
        costheta = -q/2.0/ p3by27
        alpha = acos(costheta)
        mag = 2 * (-p/3.0)**0.5
        alpha = alpha/3.0
        r1 = mag * cos(alpha)  - xn
        r2 = -mag * cos(alpha + pi/3) - xn
        r3 = -mag * cos(alpha - pi/3) - xn
        print r1,r2,r3
        return  max(r1, r2, r3)

def cubicV(a2,a1,a0):
    """
    The cubic function should return the volume of gas
    under specific pressure and temperature conditions

    with substitution y = x+t and t = a/3, the cubic equation becomes

    y**3 + p*y + q = 0,

    where p = b-3*t**2 and q = c - b*t + 2*t**3.
    Then, one real root y1 = u+v can
    be determined by solving w**2 + qw -(p/3)**3

    w**2 + q*w - (p/3)**3 = 0
    """
#    
    from math import acos, cos
    xn = -a2/3.
    yn = 2*a2*a2*a2/27. - a2*a1/3. + a0
    print "delta",a2*a2 - 3*a1,xn
    print " yn squared ",yn*yn,a2*a2,3.*a1
    raw_input()
    delta_squared = (a2*a2 - 3.*a1)/9.
    print " delta_squared",delta_squared
    delta = (delta_squared)**0.5
    print "delta ",delta
    h_squared = 4*(delta_squared**3)
    print "yn_squared h_squared",h_squared
    yn_squared = yn*yn
    if yn_squared > h_squared:
        print " root ",(yn_squared - h_squared)**0.5
        print " yn ",yn
        return xn + (-yn+(yn_squared - h_squared)**0.5)**(1./3.)
    elif yn_squared < h_squared:
        adjacent = -yn/(h_squared)**0.5
        theta = acos(adjacent)/3.
        delta = (delta_squared)**0.5
        print " 3 roots "
        return xn+2.*delta*cos(theta),\
               xn+2.*delta*cos(2.094395102 + theta),\
               xn+2.*delta*cos(4.188790204 + theta)

def validation(saltAmount,pressure,temperature):
    """
    The initial assumption is that Yh2o = 0, and Yco2 = 1 in the mixing rools for CO2.
    Otherwise, the process to establish the CO2 coefficient would be iterative.
    
    saltAmount is in moles / kg water

    R = 83.1447 its units: bar.cm3.mol-1.K-1
    """
    mNa = saltAmount
    mCl = saltAmount
    #
    R = 83.1447 #  units bar cm3 mol-1 K-1
    #
    # critical pressure and temperature (should be checked ) in bars and K (s. LBNL 57952)
    #
    Tc = 304.19
    Pc = 73.82
    #
    # We evaluate the gas volume of one mole in cm3/mol
    #
    aco2 = 7.54e+7 - 4.13e+4*temperature        # bar cm6 K 0.5 mol -2
    bco2 = 27.8                                 # cm3/mol
    #
    # Modified Redlich-Kwong coefficients s a function of critical pressure and temperature
    #
    aco2 = 0.42748*R*R*(Tc**2.5)/Pc
    bco2 = 0.08662*R*Tc/Pc
    #
    ah2oco2 = 7.89e+7                           # bar cm6 K 0.5 mol -2
    bh2o = 18.18                                # cm3/mol
    #
    # Van der Waals mixing coefficients
    #
    bmixture = bco2
    #raw_input("bm : "+str(bmixture))
    amixture = aco2
    #raw_input("am : "+str(amixture))
    #
    # We solve The Redlich Kwong EOS to obtain the volume of one mole
    #
    a2 = -R*temperature/pressure
    #
    cte = pressure *( temperature**0.5)
    #
    a1 = (a2*bmixture + amixture/cte - (bmixture**2))
    #
    a0 = -amixture * bmixture / cte
    #
    # molar volume
    #
    vco2 = polyCubicRoots(a2,a1,a0)
    #
    raw_input(" volume of one mole "+str(vco2)+"\n")    
    #
    # compressibility factor
    #
    Z = pressure*vco2/(R*temperature)
    #
    # We evaluate the fugacity coefficient of CO2
    #
    co2FugacityCoef = co2Fugacity(vco2,R,temperature,pressure,aco2,bco2)
    #
    #
    Tc = (temperature - 273.15)
    #
    # K0_CO2_g value issued from the article of Spycher 2003 ( Mutual solubilities of CO2 and H2O ) 
    #
    K0_CO2_g = exp(1.189 + (1.304e-2 - 5.446e-5*Tc)*Tc)
    #
    Bcoef = co2FugacityCoef * pressure * exp((1. - pressure)*vco2/(R*temperature))/(55.508*K0_CO2_g)
    #
    # K0_H2O value issued from the article of Spycher ( Mutual solubilities of CO2 and H2O ) 
    #
    K0_H2O = exp(log(10)*(-2.209 + (3.097e-2 - 1.098e-4*Tc + 2.048e-7*Tc*Tc)*Tc))
    #
    h2oFugacityCoef = h2oFugacity(vco2,R,temperature,pressure,aco2,bco2)
    #
    Acoef = K0_H2O * exp((pressure - 1.)*vh2o/(R*temperature))/(pressure*h2oFugacityCoef)
    #
    yh2o = (1. - Bcoef)/(1./Acoef - Bcoef)
    print " yh2o ",yh2o
    raw_input(" yh2o "+str(yh2o))
    #
    # xh2o = 1 - xco2 - xsalt
    #
    #
    # Here salinity assumed to be equal 0
    #
    m0co2 = 55.508 * xco2/(1. - xco2)
    #
    # now, we introduce salinity
    #
    print " molality in fresh water",m0co2
    lametar = lameta(temperature,pressure)
    print " lameta ",lameta
    if mNa > 0:
        gamma = exp(2.*mNa*lametar[0] + 2.*mNa*mCl*lametar[1])
    else:
        gamma = 1./(1.+m0co2/55.508)
    print " gamma ",gamma
    mco2 = m0co2/gamma
    return mco2
    
#
#
# we want to determine the amount of dissolved co2
#
# The volume of the compressed gas phase is computed by recasting
# the Redlich and Kwong equation as a cubic equation with volume as unknown.
# The maximum root is always the volume of the gas phase
# The minimum root is the volume of the liquid phase
#
saltAmount = 4 # moles / kg water
xsalt = saltAmount
mNa = saltAmount
mCl = saltAmount
#
R = 83.14472 #  units bar cm3 mol-1 K-1
#
# pressure
#
pressure = 100.
#
# temperature
#
temperature = 353.15
#
# critical pressure and temperature (should be checked ) in bars and K (s. LBNL 57952)
#
Tc = 304.19-273.15
Tc = 304.19
Pc = 73.825
#
# We evaluate the gas volume of one mole in cm3/mol
#
#aco2 = 0.42748*R*R*(Tc**2.5)/Pc
#bco2 = 0.08662*R*Tc/Pc
#
aco2 = 7.54e+7-4.13e+4*temperature      # bar cm6 K 0.5 mol -2
bco2 = 27.8                             # cm3/mol
ah2oco2 = 7.89e+7                       # bar cm6 K 0.5 mol -2
bh2o = 18.18                            # cm3/mol is constant over the repssure and temperature range considered
vh2o = 18.18
#
# 
#
#
# Van der Waals mixing coefficients
#
bmixture = bco2
raw_input("bm : "+str(bmixture))
amixture = aco2
raw_input("am : "+str(amixture))
#
print " volume of one mole using the standard law ",83.1447*298.15/100.
a2 = -R*temperature/pressure
cte = pressure *( temperature**0.5)
#
# constants of the Redlich and Kwong equation
#
a = 0.4275*R*R*(Tc**2.5)/Pc
b = 0.08664*R*Tc/Pc

a1 = (a2*bmixture + amixture/cte - (bmixture**2))
a0 = -amixture * bmixture / cte
a1 = (a2*b + a/cte - (b*b))
a0 = -a * b / cte
a1 = (a2*bmixture + amixture/cte - (bmixture**2))
a0 = -amixture * bmixture / cte
print "coefficients ",a2,a1,a0
raw_input()
vco2 = polyCubicRoots(a2,a1,a0)
vh2o = 18.18
print "\n  volume of one mole using the cubic law \n ",vco2
raw_input()
#
# compressibility factor
#
Z = pressure*vco2/(R*temperature)
print "\n compressibility factor at %fdC and under %f pressure: %f\n"%(temperature,pressure,Z)
#
# We evaluate the fugacity coefficient of CO2
#
co2FugacityCoef = co2Fugacity(vco2,R,temperature,pressure,aco2,bco2)
h2oFugacityCoef = h2oFugacity(vco2,R,temperature,pressure,aco2,bco2)
#
# We evaluate the fugacity coefficient of CO2
#
# The fugacity coefficient for h2o is the same
#
# We evaluate the co2 molality in pure water
#
Tc = (temperature - 273.15)
#
# K0_CO2(g) value issued from the article of Spycher 2003 ( Mutual solubilities of CO2 and H2O ) 
#
K0_CO2 = exp(log(10)*(1.189 + (1.304e-2 - 5.446e-5*Tc)*Tc))
#
# coefficient associated to the co2 molality within the aqeous phase 32.6 is the average value as taken from Spycher (2003)
#
Bcoef = co2FugacityCoef * pressure * exp((1. - pressure)*32.6/(R*temperature))/(55.508*K0_CO2)
#
# K0_H2O value issued from the article of Spycher 2003 ( Mutual solubilities of CO2 and H2O ) 
#
K0_H2O = exp(log(10)*(-2.209 + (3.097e-2 - (1.098e-4 - 2.048e-7*Tc)*Tc)*Tc))
#
# coefficient associated to the water molality within the co2 phase
#
Acoef = K0_H2O * exp((pressure - 1.)*vh2o/(R*temperature))/(pressure*h2oFugacityCoef)
#
#
yh2o = (1. - Bcoef)*55.508/((1./Acoef - Bcoef)*(saltAmount + 55.508 + saltAmount*Bcoef))
print " yh2o comp ",yh2o,(1. - Bcoef)/((1./Acoef - Bcoef))/yh2o
print " Bcoef ",Bcoef
raw_input()#
# Here salinity assumed to be equal 0
#
xco2 = Bcoef * (1. - yh2o)
m0co2 = 55.508 * xco2 / (1. - xco2)
#
#
# xh2o = 1 - xco2 - xsalt
#
#
# Here salinity assumed to be equal 0
#
print " m0co2 ",m0co2
#
# now, we introduce salinity
#
lametar = lameta(temperature,pressure)
print " lametar ",lametar[0],lametar[1],mNa,mCl,temperature,2.*mNa*lametar[0] + 2.*mNa*mCl*lametar[1]
if mNa > 0:
    gamma = exp(2.*mNa*lametar[0] + 2.*mNa*mCl*lametar[1])
else:
    gamma = 1./(1.+m0co2/55.508)
print "gamma ",gamma
mco2 = m0co2/gamma
print " mco2  ",mco2
print " mco2b ",validation(saltAmount,pressure,temperature)
print h2oFugacity(vco2, R, temperature, pressure, aco2, bco2)
