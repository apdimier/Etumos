# -*- coding: utf-8 -*-
"""
The module is used to get CO2 solubility as a function of pressure, temperature and salinity.
Salinity is only expressed as a function of Na and Cl ions. That point could be enhanced.
The "stem" article is the one of Duan and Sun:

An improved model calculating CO2 solubility in pure water and\n aqueous NaCl solutions from 273 to 533 K and from 0 to 2000 bar
Chemical geology 193 (2003) 257-271

and the algorithm itself is the one presented by Spycher & al.:

CO2-H2O mixtures in the geological sequestration of CO2 
Geochemica et Cosmochimica Acta
Vol. 67 N. 16 p 3015-3031 2003

Values to be tested are issued from the article. To check the validity range, just type:

                    python Redlich.py -t or python Redlich.py -test
                    
If you just want an estimation of the solubility, you can use the co2Solubility function
                    #
                    from Redlich import co2Solubility
                    #
                    co2Solubility(1.,100.,333.)
                    #
                    the first argument being the salinity, the second one the pressure and the last one,
                    the temperature.
                    
or directly type python Redlich.py 1. 100. 333.                    

"""
from math import pi,acos,cos,log,exp
import sys
import getopt
            
#
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
    #print "lameta temperature",temperature,pressure
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
         lc5 * pressure/((630. - temperature)) +\
         lc6 * temperature*log(pressure) # neperian logarithm
#
# lamdda coefficient associated to  CO2/Na interaction
#
    c2 = ec1 +\
         ec2 * temperature +\
         ec4 * pressure/temperature +\
         ec5 * pressure/((630. - temperature))
    return c1,c2
        
#
def cbrt(x):
    from math import pow
    if x >= 0:
        return pow(x, 1.0/3.0)
    else:
        return -pow(abs(x), 1.0/3.0) 

def polyCubicRoots(a, b, c):
    """
    we solve a monic cubic polynom: x3 + a * x2 + bx +c = 0
    see, among others,  Nickalls for a discussion about the solution
    
    A new approach to solving the cubic: Cardan's solution revealed
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
    #print "delta",a2*a2 - 3*a1,xn
    #print " yn squared ",yn*yn,a2*a2,3.*a1
    #raw_input()
    delta_squared = (a2*a2 - 3.*a1)/9.
    #print " delta_squared",delta_squared
    delta = (delta_squared)**0.5
    #print "delta ",delta
    h_squared = 4*(delta_squared**3)
    #print "yn_squared h_squared",h_squared
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
    #raw_input(" phico2 "+str(phico2))
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
    #raw_input(" phih2o "+str(phih2o))
    return phih2o

def co2Solubility(saltAmount,pressure,temperature):
    """
    The initial assumption is that Yh2o = 0, and Yco2 = 1 in the mixing rules for CO2.
    Otherwise, the process to establish the CO2 coefficient would be iterative.
    
    saltAmount is in moles / kg water

    R = 83.14467 its units: bar.cm3.mol-1.K-1
    
    co2Solubility(saltAmount,pressure,temperature)
    """
    mNa = saltAmount
    mCl = saltAmount
    #
    R = 83.14467 #  units bar cm3 mol-1 K-1
    #
    # critical pressure and temperature (should be checked ) in bars and K (s. LBNL 57952)
    #
    Tc = 304.19
    Pc = 73.825
    #
    # We evaluate the gas volume of one mole in cm3/mol
    #
    aco2 = 7.54e+7 - 4.13e+4*temperature        # bar cm6 K 0.5 mol -2
    bco2 = 27.8                                 # cm3/mol
    #
    # Modified Redlich-Kwong coefficients as a function of critical pressure and temperature
    #
    #aco2 = 0.42748*R*R*(Tc**2.5)/Pc
    #bco2 = 0.08662*R*Tc/Pc
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
    # constants of the Redlich and Kwong equation
    #
    a = 0.4275*R*R*(Tc**2.5)/Pc
    b = 0.08664*R*Tc/Pc
    #
    a1 = (a2*bmixture + amixture/cte - (bmixture**2))
    a0 = -amixture * bmixture / cte
    #
    # molar volume
    #
    vco2 = polyCubicRoots(a2,a1,a0)
    vh2o = 18.18
    #
    #raw_input(" volume of one mole "+str(vco2)+"\n")    
    #
    # compressibility factor
    #
    Z = pressure*vco2/(R*temperature)
    #
    # We evaluate the fugacity coefficient of CO2
    #
    co2FugacityCoef = co2Fugacity(vco2,R,temperature,pressure,aco2,bco2)
    print " co2 fugacity at temperature %e : %e"%(temperature,co2FugacityCoef)
    h2oFugacityCoef = h2oFugacity(vco2,R,temperature,pressure,aco2,bco2)
    #
    #
    Tc = (temperature - 273.15)
    #
    # K0_CO2_g value issued from the article of Spycher 2003 ( Mutual solubilities of CO2 and H2O ) 
    #
    K0_CO2_g = exp(log(10)*(1.189 + (1.304e-2 - 5.446e-5*Tc)*Tc))
    #
    Bcoef = co2FugacityCoef * pressure * exp((1. - pressure)*32.6/(R*temperature))/(55.508*K0_CO2_g)
    #
    # K0_H2O value issued from the article of Spycher ( Mutual solubilities of CO2 and H2O ) 
    #
    K0_H2O = exp(log(10)*(-2.209 + (3.097e-2 - (1.098e-4 - 2.048e-7*Tc)*Tc)*Tc))
    #
    Acoef = K0_H2O * exp((pressure - 1.)*vh2o/(R*temperature))/(pressure*h2oFugacityCoef)
    #
    yh2o = (1. - Bcoef)*55.508/((1./Acoef - Bcoef)*(saltAmount + 55.508 + saltAmount*Bcoef))
    #print " yh2o ",yh2o
    #raw_input(" yh2o "+str(yh2o))
    #
    # xh2o = 1 - xco2 - xsalt
    #
    #
    # Here salinity assumed to be equal 0
    #
    xco2 = Bcoef * (1. - yh2o)
    m0co2 = 55.508 * xco2 / (1. - xco2)
    #
    # now, we introduce salinity
    #
    #print " molality in fresh water",m0co2
    lametar = lameta(temperature,pressure)
    #print " lameta ",lameta
    if mNa > 0:
        #
        # The summation convention of einstein is not taken into accout in the articles ( it seems that..)
        #
        #gamma = exp(2.*mNa*lametar[0] + 2.*mNa*mCl*lametar[1])
        gamma = exp(2.*mNa*lametar[0] + mNa*mCl*lametar[1])
    else:
        #gamma = 1./(1.+m0co2/55.508)
        gamma = 1.
    #print " gamma ",gamma
    mco2 = m0co2/gamma
    return mco2

     

def comparisonToDuan(eps = None,verbose = None):
    """
    Enables a direct comparison to available duan data in the validity range considered
    """
#
# list solubility as a function of temperature, pressure in bars is self explained
#

    DuanValues_fw_at50b = [(303.15,1.0811),(333.15,0.6695),(363.15,0.4952),(393.15,0.4157),\
                           (423.15,0.3767)]
#
    DuanValues_fw_at100b = [(303.15,1.3611),(333.15,1.0275),(363.15,0.8219),(393.15,0.7314),\
                            (423.15,0.7054)]
#
    DuanValues_fw_at200b = [(303.15,1.4889),(333.15,1.2344),(363.15,1.1308),(393.15,1.1100),\
                        (423.15,1.1569)]
#
    DuanValues_fw_at300b = [(303.15,1.5989),(333.15,1.3495),(363.15,1.2802),(393.15,1.3184),\
                        (423.15,1.4427)]
#
    DuanValues_fw_at400b = [(303.15,1.7005),(333.15,1.4478),(363.15,1.3954),(393.15,1.4700),\
                        (423.15,1.6535)]
#
    DuanValues_fw_at500b = [(303.15,1.7965),(333.15,1.5368),(363.15,1.4954),(393.15,1.5972),\
                        (423.15,1.8287)]
#
    DuanValues_fw_at600b = [(303.15,1.8883),(333.15,1.6194),(363.15,1.5857),(393.15,1.7102),\
                        (423.15,1.9833)]
                        
    DuanValues_1m_at50b = [(303.15,0.8729),(333.15,0.5502), (363.15,0.4103), (393.15,0.3447),\
                       (423.15,0.3106), (453.15,0.2837), (483.15,0.2399)]
    DuanValues_1m_at100b = [(303.15,1.0958),(333.15,0.8405), (363.15,0.6767), (393.15,0.6015),\
                        (423.15,0.5759), (453.15,0.5751), (483.15,0.5755)]
    DuanValues_1m_at200b = [(303.15,1.1990),(333.15,1.0072), (363.15,0.9259), (393.15,0.9052),\
                        (423.15,0.9337), (453.15,1.0035), (483.15,1.1016)]
    DuanValues_1m_at300b = [(303.15,1.2910),(333.15,1.1012), (363.15,1.0456), (393.15,1.0696),\
                        (423.15,1.1551), (453.15,1.2973), (483.15,1.4926)]
    DuanValues_1m_at400b = [(303.15,1.3781),(333.15,1.1827), (363.15,1.1383), (393.15,1.1881),\
                        (423.15,1.3150), (453.15,1.5180), (483.15,1.8009)]
    DuanValues_1m_at500b = [(303.15,1.4620),(333.15,1.2577), (363.15,1.2191), (393.15,1.2869),\
                        (423.15,1.4458), (453.15,1.6993), (483.15,2.0593)]
    DuanValues_1m_at600b = [(303.15,1.5438),(333.15,1.3282), (363.15,1.2925), (393.15,1.3742),\
                        (423.15,1.5595), (453.15,1.8565), (483.15,2.2859)]    


    DuanValues_2m_at50b =  [(303.15,0.7135),(333.15,0.4583), (363.15,0.3451), (393.15,0.2905),\
                        (423.15,0.2608), (453.15,0.2362), (483.15,0.1982)]
    DuanValues_2m_at100b = [(303.15,0.8939),(333.15,0.6978), (363.15,0.5663), (393.15,0.5038),\
                        (423.15,0.4798), (453.15,0.4743), (483.15,0.4678)]
    DuanValues_2m_at200b = [(303.15,0.9801),(333.15,0.8359), (363.15,0.7729), (393.15,0.7543),\
                        (423.15,0.7721), (453.15,0.8192), (483.15,0.8834)]
    DuanValues_2m_at300b = [(303.15,1.0600),(333.15,0.9160), (363.15,0.8731), (393.15,0.8898),\
                        (423.15,0.9513), (453.15,1.0521), (483.15,1.1855)]
    DuanValues_2m_at400b = [(303.15,1.1377),(333.15,0.9873), (363.15,0.9518), (393.15,0.9878),\
                        (423.15,1.0803), (453.15,1.2250), (483.15,1.4191)]
    DuanValues_2m_at500b = [(303.15,1.2143),(333.15,1.0542), (363.15,1.0216), (393.15,1.0702),\
                        (423.15,1.1855), (453.15,1.3655), (483.15,1.6114)]
    DuanValues_2m_at600b = [(303.15,1.2905),(333.15,1.1182), (363.15,1.0859), (393.15,1.1436),\
                        (423.15,1.2771), (453.15,1.4865), (483.15,1.7771)]

    DuanValues_4m_at50b =  [(303.15,0.4945),(333.15,0.3314), (363.15,0.2554), (393.15,0.2169),\
                        (423.15,0.1942), (453.15,0.1737), (483.15,0.1430)]
    DuanValues_4m_at100b = [(303.15,0.6189),(333.15,0.5028), (363.15,0.4169), (393.15,0.3733),\
                        (423.15,0.3538), (453.15,0.3449), (483.15,0.3328)]
    DuanValues_4m_at200b = [(303.15,0.6849),(333.15,0.6060), (363.15,0.5705), (393.15,0.5590),\
                        (423.15,0.5679), (453.15,0.5924), (483.15,0.6234)]
    DuanValues_4m_at300b = [(303.15,0.7515),(333.15,0.6717), (363.15,0.6503), (393.15,0.6636),\
                        (423.15,0.7026), (453.15,0.7624), (483.15,0.8365)]
    DuanValues_4m_at400b = [(303.15,0.8200),(333.15,0.7340), (363.15,0.7170), (393.15,0.7434),\
                        (423.15,0.8034), (453.15,0.8921), (483.15,1.0042)]
    DuanValues_4m_at500b = [(303.15,0.8907),(333.15,0.7955), (363.15,0.7793), (393.15,0.8140),\
                        (423.15,0.8893), (453.15,1.0011), (483.15,1.1457)]
    DuanValues_4m_at600b = [(303.15,0.9639),(333.15,0.8571), (363.15,0.8395), (393.15,0.8798),\
                        (423.15,0.9671), (453.15,1.0982), (483.15,1.2709)]
    if eps == None: eps = 8.1e-2
    saltAmount = 0.
    ok = 1
    pressure = 50
    for data in DuanValues_fw_at50b[:-1]: 
        temperature = data[0]
        molality = data[1]
        saltamount = 0.
        mco2 = co2Solubility(saltAmount,pressure,temperature)
        error = abs(mco2 - molality)/molality
        if error > eps:
            ok = 0
        print " mco2 control ",temperature, mco2, molality
    if ok == 1:
        print " for 50 bar and fresh water results are ok"
    else:
        raise Exception(" for 50 bar and fresh water differences occur")
    if verbose: raw_input()
    saltAmount = 0.
    ok = 1
    pressure = 100
    for data in DuanValues_fw_at100b[:-1]: 
        temperature = data[0]
        molality = data[1]
        saltamount = 0.
        mco2 = co2Solubility(saltAmount,pressure,temperature)
        error = abs(mco2 - molality)/molality
        if error > eps:
            ok = 0
        print " mco2 control ",temperature, mco2, molality
    if ok == 1:
        print " for 100 bar and fresh water results are ok"
    else:
        raise Exception(" for 100 bar and fresh water differences occur")
    if verbose: raw_input()
    ok = 1
    pressure = 200
    for data in DuanValues_fw_at200b[:-1]:
        temperature = data[0]
        molality = data[1]
        saltamount = 0.
        mco2 = co2Solubility(saltAmount,pressure,temperature)
        error = abs(mco2 - molality)/molality
        if error > eps:
            ok = 0
        print " mco2 control ",temperature, mco2, molality
    if ok == 1:
        print " for 200 bar and fresh water results are ok"
    else:
        raise Exception(" for 200 bar and fresh water differences occur")
    if verbose: raw_input()
    ok = 1
    pressure = 300
    for data in DuanValues_fw_at300b[:-1]:
        temperature = data[0]
        molality = data[1]
        saltamount = 0.
        mco2 = co2Solubility(saltAmount,pressure,temperature)
        error = abs(mco2 - molality)/molality
        if error > eps:
            ok = 0
        print " mco2 control ",temperature, mco2, molality
    if ok == 1:
        print " for 300 bar and fresh water results are ok"
    else:
        raise Exception(" for 300 bar and fresh water differences occur")
    if verbose: raw_input()
    ok = 1
    pressure = 400
    for data in DuanValues_fw_at400b[:-1]:
        temperature = data[0]
        molality = data[1]
        saltamount = 0.
        mco2 = co2Solubility(saltAmount,pressure,temperature)
        error = abs(mco2 - molality)/molality
        if error > eps:
            ok = 0
        print " mco2 control ",temperature, mco2, molality
    if ok == 1:
        print " for 400 bar and fresh water results are ok"
    else:
        raise Exception(" for 400 bar and fresh water differences occur")
    if verbose: raw_input()
    ok = 1
    pressure = 500
    for data in DuanValues_fw_at500b[:-1]:
        temperature = data[0]
        molality = data[1]
        saltamount = 0.
        mco2 = co2Solubility(saltAmount,pressure,temperature)
        error = abs(mco2 - molality)/molality
        if error > eps:
            ok = 0
        print " mco2 control ",temperature, mco2, molality
    if ok == 1:
        print " for 500 bar and fresh water results are ok"
    else:
        raise Exception(" for 500 bar and fresh water differences occur")
    if verbose: raw_input()
    ok = 1
    pressure = 600
    for data in DuanValues_fw_at600b[:-1]:
        temperature = data[0]
        molality = data[1]
        saltamount = 0.
        mco2 = co2Solubility(saltAmount,pressure,temperature)
        error = abs(mco2 - molality)/molality
        if error > eps:
            ok = 0
        print " mco2 control ",temperature, mco2, molality
    if ok == 1:
        print " for 600 bar and fresh water results are ok"
    else:
        raise Exception(" for 600 bar and fresh water differences occur")
    if verbose: raw_input()
    #
    # 1 mole brine
    #
    ok = 1
    pressure = 50
    saltAmount = 1.
    for data in DuanValues_1m_at50b[:-3]:
        temperature = data[0]
        molality = data[1]
        saltamount = 0.
        mco2 = co2Solubility(saltAmount,pressure,temperature)
        error = abs(mco2 - molality)/molality
        if error > eps:
            ok = 0
        print " mco2 control ",temperature, mco2, molality
    if ok == 1:
        print " for 50 bar and 1 mole brine results are ok"
    else:
        raise Exception(" for 50 bar and 1 mole brine differences occur")
    if verbose: raw_input()
    ok = 1
    pressure = 100
    saltAmount = 1.
    for data in DuanValues_1m_at100b[:-4]:
        temperature = data[0]
        molality = data[1]
        saltamount = 0.
        mco2 = co2Solubility(saltAmount,pressure,temperature)
        error = abs(mco2 - molality)/molality
        if error > eps:
            ok = 0
        print " mco2 control ",temperature, mco2, molality
    if ok == 1:
        print " for 100 bar and 1 mole brine results are ok"
    else:
        raise Exception(" for 100 bar and 1 mole brine differences occur")
    if verbose: raw_input()
    ok = 1
    pressure = 200
    for data in DuanValues_1m_at200b[:-4]:
        temperature = data[0]
        molality = data[1]
        saltamount = 0.
        mco2 = co2Solubility(saltAmount,pressure,temperature)
        error = abs(mco2 - molality)/molality
        if error > eps:
            ok = 0
        print " mco2 control ",temperature, mco2, molality
    if ok == 1:
        print " for 200 bar and 1 mole brine results are ok"
    else:
        raise Exception(" for 200 bar and 1 mole brine differences occur")
    if verbose: raw_input()
    ok = 1
    pressure = 300
    for data in DuanValues_1m_at300b[:-3]:
        temperature = data[0]
        molality = data[1]
        saltamount = 0.
        mco2 = co2Solubility(saltAmount,pressure,temperature)
        error = abs(mco2 - molality)/molality
        if error > eps:
            ok = 0
        print " mco2 control ",temperature, mco2, molality
    if ok == 1:
        print " for 300 bar and 1 mole brine results are ok"
    else:
        raise Exception(" for 300 bar and 1 mole brine differences occur")
    if verbose: raw_input()
    ok = 1
    pressure = 400
    for data in DuanValues_1m_at400b[:-3]:
        temperature = data[0]
        molality = data[1]
        saltamount = 0.
        mco2 = co2Solubility(saltAmount,pressure,temperature)
        error = abs(mco2 - molality)/molality
        if error > eps:
            ok = 0
        print " mco2 control ",temperature, mco2, molality
    if ok == 1:
        print " for 400 bar and 1 mole brine results are ok"
    else:
        raise Exception(" for 400 bar and 1 mole brine differences occur")
    if verbose: raw_input()
    ok = 1
    pressure = 500
    for data in DuanValues_1m_at500b[:-3]:
        temperature = data[0]
        molality = data[1]
        saltamount = 0.
        mco2 = co2Solubility(saltAmount,pressure,temperature)
        error = abs(mco2 - molality)/molality
        if error > eps:
            ok = 0
        print " mco2 control ",temperature, mco2, molality
    if ok == 1:
        print " for 500 bar and 1 mole brine results are ok"
    else:
        raise Exception(" for 500 bar and 1 mole brine differences occur")
    if verbose: raw_input()
    ok = 1
    pressure = 600
    for data in DuanValues_1m_at600b[:-3]:
        temperature = data[0]
        molality = data[1]
        saltamount = 0.
        mco2 = co2Solubility(saltAmount,pressure,temperature)
        error = abs(mco2 - molality)/molality
        if error > eps:
            ok = 0
        print " mco2 control ",temperature, mco2, molality
    if ok == 1:
        print " for 600 bar and 1 mole brine results are ok"
    else:
        raise Exception(" for 600 bar and 1 mole brine differences occur")
    if verbose: raw_input()
    #
    # 2 mole brine
    #
    ok = 1
    pressure = 50
    saltAmount = 2.
    for data in DuanValues_2m_at50b[:-3]:
        temperature = data[0]
        molality = data[1]
        saltamount = 0.
        mco2 = co2Solubility(saltAmount,pressure,temperature)
        error = abs(mco2 - molality)/molality
        if error > eps:
            ok = 0
        print " mco2 control ",temperature, mco2, molality
    if ok == 1:
        print " for 50 bar and 2 mole brine results are ok"
    else:
        raise Exception(" for 50 bar and 2 mole brine differences occur")
    if verbose: raw_input()
    ok = 1
    pressure = 100
    saltAmount = 2.
    for data in DuanValues_2m_at100b[:-3]:
        temperature = data[0]
        molality = data[1]
        saltamount = 0.
        mco2 = co2Solubility(saltAmount,pressure,temperature)
        error = abs(mco2 - molality)/molality
        if error > eps:
            ok = 0
        print " mco2 control ",temperature, mco2, molality
    if ok == 1:
        print " for 100 bar and 2 mole brine results are ok"
    else:
        raise Exception(" for 100 bar and 2 mole brine differences occur")
    if verbose: raw_input()
    ok = 1
    pressure = 200
    for data in DuanValues_2m_at200b[:-3]:
        temperature = data[0]
        molality = data[1]
        saltamount = 0.
        mco2 = co2Solubility(saltAmount,pressure,temperature)
        error = abs(mco2 - molality)/molality
        if error > eps:
            ok = 0
        print " mco2 control ",temperature, mco2, molality
    if ok == 1:
        print " for 200 bar and 2 mole brine results are ok"
    else:
        raise Exception(" for 200 bar and 2 mole brine differences occur")
    if verbose: raw_input()
    ok = 1
    pressure = 300
    for data in DuanValues_2m_at300b[:-3]:
        temperature = data[0]
        molality = data[1]
        saltamount = 0.
        mco2 = co2Solubility(saltAmount,pressure,temperature)
        error = abs(mco2 - molality)/molality
        if error > eps:
            ok = 0
        print " mco2 control ",temperature, mco2, molality
    if ok == 1:
        print " for 300 bar and 2 mole brine results are ok"
    else:
        raise Exception(" for 300 bar and 2 mole brine differences occur")
    if verbose: raw_input()
    ok = 1
    pressure = 400
    for data in DuanValues_2m_at400b[:-3]:
        temperature = data[0]
        molality = data[1]
        saltamount = 0.
        mco2 = co2Solubility(saltAmount,pressure,temperature)
        error = abs(mco2 - molality)/molality
        if error > eps:
            ok = 0
        print " mco2 control ",temperature, mco2, molality
    if ok == 1:
        print " for 400 bar and 2 mole brine results are ok"
    else:
        raise Exception(" for 400 bar and 2 mole brine differences occur")
    if verbose: raw_input()
    ok = 1
    pressure = 500
    for data in DuanValues_2m_at500b[:-3]:
        temperature = data[0]
        molality = data[1]
        saltamount = 0.
        mco2 = co2Solubility(saltAmount,pressure,temperature)
        error = abs(mco2 - molality)/molality
        if error > eps:
            ok = 0
        print " mco2 control ",temperature, mco2, molality
    if ok == 1:
        print " for 500 bar and 2 mole brine results are ok"
    else:
        raise Exception(" for 500 bar and 2 mole brine differences occur")
    if verbose: raw_input()
    ok = 1
    pressure = 600
    for data in DuanValues_2m_at600b[:-3]:
        temperature = data[0]
        molality = data[1]
        saltamount = 0.
        mco2 = co2Solubility(saltAmount,pressure,temperature)
        error = abs(mco2 - molality)/molality
        if error > eps:
            ok = 0
        print " mco2 control ",temperature, mco2, molality
    if ok == 1:
        print " for 600 bar and 2 mole brine results are ok"
    else:
        print " mco2 control ",temperature, mco2, molality,error
        raise Exception(" for 600 bar and 2 mole brine differences occur")
    if verbose: raw_input()
    #
    #
    #
    # 4 mole brine
    #
    ok = 1
    pressure = 50
    saltAmount = 4.
    for data in DuanValues_4m_at50b[:-3]:
        temperature = data[0]
        molality = data[1]
        saltamount = 0.
        mco2 = co2Solubility(saltAmount,pressure,temperature)
        error = abs(mco2 - molality)
        if error > eps:
            ok = 0
        print " mco2 control ",temperature, mco2, molality
    if ok == 1:
        print " for 50 bar and 4 mole brine results are ok"
    else:
        raise Exception(" for 50 bar and 4 mole brine differences occur")
    if verbose: raw_input()
    ok = 1
    pressure = 100
    saltAmount = 4.
    for data in DuanValues_4m_at100b[:-3]:
        temperature = data[0]
        molality = data[1]
        saltamount = 0.
        mco2 = co2Solubility(saltAmount,pressure,temperature)
        error = abs(mco2 - molality)
        if error > eps:
            ok = 0
        print " mco2 control ",temperature, mco2, molality
    if ok == 1:
        print " for 100 bar and 4 mole brine results are ok"
    else:
        raise Exception(" for 100 bar and 4 mole brine differences occur")
    if verbose: raw_input()
    ok = 1
    pressure = 200
    for data in DuanValues_4m_at200b[:-3]:
        temperature = data[0]
        molality = data[1]
        saltamount = 0.
        mco2 = co2Solubility(saltAmount,pressure,temperature)
        error = abs(mco2 - molality)
        if error > eps:
            ok = 0
        print " mco2 control ",temperature, mco2, molality
    if ok == 1:
        print " for 200 bar and 4 mole brine results are ok"
    else:
        raise Exception(" for 200 bar and 4 mole brine differences occur")
    if verbose: raw_input()
    ok = 1
    pressure = 300
    for data in DuanValues_4m_at300b[:-3]:
        temperature = data[0]
        molality = data[1]
        saltamount = 0.
        mco2 = co2Solubility(saltAmount,pressure,temperature)
        error = abs(mco2 - molality)
        if error > eps:
            ok = 0
        print " mco2 control ",temperature, mco2, molality
    if ok == 1:
        print " for 300 bar and 4 mole brine results are ok"
    else:
        raise Exception(" for 300 bar and 4 mole brine differences occur")
    if verbose: raw_input()
    ok = 1
    pressure = 400
    for data in DuanValues_4m_at400b[:-3]:
        temperature = data[0]
        molality = data[1]
        saltamount = 0.
        mco2 = co2Solubility(saltAmount,pressure,temperature)
        error = abs(mco2 - molality)
        if error > eps:
            ok = 0
        print " mco2 control ",temperature, mco2, molality
    if ok == 1:
        print " for 400 bar and 4 mole brine results are ok"
    else:
        raise Exception(" for 400 bar and 4 mole brine differences occur")
    if verbose: raw_input()
    ok = 1
    pressure = 500
    for data in DuanValues_4m_at500b[:-3]:
        temperature = data[0]
        molality = data[1]
        saltamount = 0.
        mco2 = co2Solubility(saltAmount,pressure,temperature)
        error = abs(mco2 - molality)
        if error > eps:
            ok = 0
        print " mco2 control ",temperature, mco2, molality
    if ok == 1:
        print " for 500 bar and 4 mole brine results are ok"
    else:
        raise Exception(" for 500 bar and 4 mole brine differences occur")
    if verbose: raw_input()
    ok = 1
    pressure = 600
    for data in DuanValues_4m_at600b[:-3]:
        temperature = data[0]
        molality = data[1]
        saltamount = 0.
        mco2 = co2Solubility(saltAmount,pressure,temperature)
        error = abs(mco2 - molality)
        if error > eps:
            ok = 0
        print " mco2 control ",temperature, mco2, molality
    if ok == 1:
        print " for 600 bar and 4 mole brine results are ok"
    else:
        raise Exception(" for 600 bar and 4 mole brine differences occur")
    if ok == 1:
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        print " Module feets Duan data up to eps = %10.5e"%(eps)
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    if verbose: raw_input()


def co2MolarVolume(saltAmount,pressure,temperature):
    """
    The initial assumption is that Yh2o = 0, and Yco2 = 1 in the mixing rules for CO2.
    Otherwise, the process to establish the CO2 coefficient would be iterative.
    
    saltAmount is in moles / kg water

    R = 83.14467 its units: bar.cm3.mol-1.K-1
    
    co2Solubility(saltAmount,pressure,temperature)
    """
    mNa = saltAmount
    mCl = saltAmount
    #
    R = 83.14467 #  units bar cm3 mol-1 K-1
    #
    # critical pressure and temperature (should be checked ) in bars and K (s. LBNL 57952)
    #
    Tc = 304.19
    Pc = 73.825
    #
    # We evaluate the gas volume of one mole in cm3/mol
    #
    aco2 = 7.54e+7 - 4.13e+4*temperature        # bar cm6 K 0.5 mol -2
    bco2 = 27.8                                 # cm3/mol
    #
    # Modified Redlich-Kwong coefficients as a function of critical pressure and temperature
    #
    #aco2 = 0.42748*R*R*(Tc**2.5)/Pc
    #bco2 = 0.08662*R*Tc/Pc
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
    # constants of the Redlich and Kwong equation
    #
    a = 0.4275*R*R*(Tc**2.5)/Pc
    b = 0.08664*R*Tc/Pc
    #
    a1 = (a2*bmixture + amixture/cte - (bmixture**2))
    a0 = -amixture * bmixture / cte
    #
    # molar volume
    #
    return  polyCubicRoots(a2,a1,a0)*1.e-6," m3"
          
#

def main():
    # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:t", ["help","test"])
        print " opts ",opts
        print " args ",args
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print __doc__
            sys.exit(0)
        elif  o in ("-t","--test"):
            comparisonToDuan(verbose = 1)
            print " rumpf data comparison "
            pressure = 96.37
            temperature = 353.1
            saltAmount = 4.001
            print " co2 solubility ",co2Solubility(saltAmount,pressure,temperature)
            print " co2 solubility ",co2Solubility(0.0,100,333)
    # process arguments
    if len(args) == 3:
        print " co2 solubility : %15.10e\n\n   for %10.2e moles of brine, at %8.2e bars and %10.2e°K"\
        %(co2Solubility(float(args[0]),float(args[1]),float(args[2])),float(args[0]),float(args[1]),float(args[2]))
        
#
def cubeRoots(x):
    """Find three complex cube ro
    ots of real or complex x."""
    z = x + 0j
    s = 1
    if z.real < 0:
        z,s = -z,-s
    t = math.atan2(z.imag, z.real)/3
    a = s * (abs(z)**(1./3))
    w = complex(-0.5,math.sqrt(0.75))
    w_ = w.conjugate()
    u = a * complex(math.cos(t),math.sin(t))

if __name__ == "__main__":
    main()    

