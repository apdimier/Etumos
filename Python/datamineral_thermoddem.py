"""
data issued from:

    densities:  http://webmineral.com

    logk25      thermoddem

    logk        thermoddem
"""
dicMinerals = { 'Calcite': { 'DENSITY': 2710,
                           'EQUATION': 'CaCO3 + H+ = HCO3- + Ca++',
                           'FORMULA': 'CaCO3',
                           'MOLWEIGHT': 100.087,
                           'LOGK25': 1.847,
                           'LOGK': [-8.50102e+02, -1.39471e-01, 4.68810e+04, 3.09649e+02, -2.65915e+06],
                           'NAME': 'Calcite'},
              'Dolomite': { 'DENSITY': 2830,
                            'EQUATION': 'CaMg(CO3)2 + 2H+ = 2HCO3- + 1Ca++ + 1Mg++',
                            'FORMULA': 'CaMg(CO3)2',
                            'MOLWEIGHT': 184.409,
                            'LOGK25': 3.533,
                            'LOGK': [-1.79236e+03, -2.89635e-01, 9.95945e+04, 6.51145e+02, -5.60084e+06],
                            'NAME': 'Dolomite'},
              'Illite_Mg': { 'DENSITY': 2770,
                             'EQUATION': 'K0.85Mg0.25Al2.35Si3.4O10(OH)2 + 8.4H+ + 1.6H2O = 2.35Al+++ + 0.85K+ + 0.25Mg++ + 3.4H4SiO4',
                             'FORMULA': 'K0.85Mg0.25Al2.35Si3.4O10(OH)2',
                             'MOLWEIGHT': 389.34,
                             'LOGK25': 10.844,
                             'LOGK': [-1.12970e+03, -1.92745e-01, 7.04402e+04, 4.04593e+02, -3.50116e+06],
                             'NAME': 'Illite_Mg'},
              'Kaolinite': { 'DENSITY': 2630,
                             'EQUATION': 'Al2Si2O5(OH)4 + 6H+ = 2Al+++ + 1H2O + 2H4SiO4',
                             'FORMULA': 'Al2Si2O5(OH)4',
                             'MOLWEIGHT': 258.161,
                             'LOGK25': 6.471,
                             'LOGK': [-9.16789e+02, -1.50208e-01, 5.42404e+04, 3.28660e+02, -2.41129e+06],
                             'NAME': 'Kaolinite'},
              'Mg_Montmorillonite_Ca': { 'DENSITY': 2350,
                                         'EQUATION': 'Ca0.17Mg0.33Al1.68Si3.99O10(OH)2 + 6.04H+ + 3.96H2O = 1.68Al+++ + 0.17Ca++ + 0.33Mg++ + 3.99H4SiO4',
                                         'FORMULA': 'Ca0.17Mg0.33Al1.68Si3.99O10(OH)2',
                                         'MOLWEIGHT': 366.237,
                                         'LOGK25': 3.748,
                                         'LOGK': [-7.96060e+02, -1.39999e-01, 4.90443e+04, 2.85275e+02, -2.56428e+06],
                                         'NAME': 'Mg_Montmorillonite_Ca'},
              'Mg_Montmorillonite_Na': { 'DENSITY': 2350,
                                         'EQUATION': 'Na0.33Mg0.33Al1.67Si4O10(OH)2 + 6.0H+ + 4.0H2O = 1.67Al+++ + 0.33Na+ + 0.33Mg++ + 4.H4SiO4',
                                         'FORMULA': 'Na0.33Mg0.33Al1.67Si4O10(OH)2',
                                         'MOLWEIGHT': 367.021,
                                         'LOGK25': 2.999,
                                         'LOGK': [-8.18158e+02, -1.38800e-01, 5.03309e+04, 2.92149e+02, -2.59365e+06],
                                         'NAME': 'Mg_Montmorillonite_Na'},
              'Pyrite': { 'DENSITY': 5010,
                          'EQUATION': 'FeS2 + 3.5O2 + 1H2O = 1Fe++ + 2H+ + 2SO4--',
                          'FORMULA': 'FeS2',
                          'MOLWEIGHT': 119.975,
                          'LOGK25': 119.975,
                          'LOGK': [-3.59065e+03, -5.80474e-01, 2.78096e+05, 1.29212e+03, -1.32014e+07],
                          'NAME': 'Pyrite'},
              'Anhydrite': { 'DENSITY': 2770,
                           'EQUATION': 'CaSO4 = Ca++ + 2SO4--',
                           'FORMULA': 'CaSO4',
                           'MOLWEIGHT': 136.14,
                           'LOGK': -4.436,
                           'NAME': 'Anhydrite'},
              'Quartz_alpha': { 'DENSITY': 2650,
                                'EQUATION': 'SiO2 + 2H2O = 1H4SiO4',
                                'FORMULA': 'SiO2',
                                'MOLWEIGHT': 60.085,
                                'LOGK25': -3.738,
                                'LOGK': [1.45844e+01, 2.48382e-03, -1.88433e+03, -5.35743e+00, 4.55019e+04],
                                'NAME': 'Quartz_alpha'},
              'Siderite': { 'DENSITY': 3960,
                            'EQUATION': 'FeCO3 + 1H+ = 1HCO3- + 1Fe++',
                            'FORMULA': 'FeCO3',
                            'MOLWEIGHT': 115.856,
                            'LOGK25': -0.473,
                            'LOGK': [-9.15524e+02, -1.47685e-01, 5.05603e+04, 3.32122e+02, -2.87218e+06],
                            'NAME': 'Siderite'}
              }
               
def numberOfMoles(dicMinerals,mineralName,volumicpercent,porosity):
    """
    to define the number of moles given a volumic %
    """
    if volumicpercent >1.0:
        raise Warning, " a percentage should be lower than 1"
    if porosity >1.0:
        raise Warning, " the porosity should be lower than 1"
    dens = dicMinerals[mineralName]['DENSITY']              # mineral density
    rap = (1.-porosity)/porosity                            # balance between mineral and water
    rapVol = volumicpercent*rap                             # balance between the specific mineral and water
    molweight = dicMinerals[mineralName]['MOLWEIGHT']/1000. # kg / mol
    rapmolvol = dens / molweight                            # number of moles in 1 M3
    return rapVol * rapmolvol/1000

          
