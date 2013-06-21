from chemistry import *
from chemicalmodule import *
from phreeqc import *

Phreeqc_file = "test.txt"      # bounded to Phreeqc
ProblemName  = "test"          # Phreeqc file 
#~~~~~~~~~~~~~~~~~~~
# Chemical Addenda ~
#~~~~~~~~~~~~~~~~~~~
speciesAddenda = []
Al = AqueousMasterSpecies(symbol = "Al+++",\
                          name = "Al",\
                          element = "Al",\
                          molarMass = MolarMass(26.981538,"g/mol"),\
                          alkalinity = 0)
speciesAddenda.append(Al)
C = AqueousMasterSpecies(symbol = "HCO3-",\
                         name = "C",\
                         element = "C",\
                         molarMass = MolarMass(12.0107,"g/mol"),\
                         alkalinity = 1)
speciesAddenda.append(C)
C_p4_ = AqueousMasterSpecies(symbol = "HCO3-",\
                             name = "C(4)",\
                             element = "C",\
                             molarMass = MolarMass(12.0107,"g/mol"),\
                             alkalinity = 1)
speciesAddenda.append(C_p4_)
C_m4_ = AqueousMasterSpecies(symbol = "CH4",\
                             name = "C(-4)",\
                             element = "C",\
                             molarMass = MolarMass(12.0107,"g/mol"),\
                             alkalinity = 0)
speciesAddenda.append(C_m4_)
C_2_ = AqueousMasterSpecies(symbol = "CO",\
                            name = "C(2)",\
                            element = "C",\
                            molarMass = MolarMass(12.0107,"g/mol"),\
                            alkalinity = 0)
speciesAddenda.append(C_2_)
Ca = AqueousMasterSpecies(symbol = "Ca++",\
                          name = "Ca",\
                          element = "Ca",\
                          molarMass = MolarMass(40.078,"g/mol"),\
                          alkalinity = 0)
speciesAddenda.append(Ca)
Cl = AqueousMasterSpecies(symbol = "Cl-",\
                          name = "Cl",\
                          element = "Cl",\
                          molarMass = MolarMass(35.453,"g/mol"),\
                          alkalinity = 0)
speciesAddenda.append(Cl)
Cl_m1_ = AqueousMasterSpecies(symbol = "Cl-",\
                              name = "Cl(-1)",\
                              element = "Cl",\
                              molarMass = MolarMass(35.453,"g/mol"),\
                              alkalinity = 0)
speciesAddenda.append(Cl_m1_)
Cl_1_ = AqueousMasterSpecies(symbol = "ClO-",\
                             name = "Cl(1)",\
                             element = "Cl",\
                             molarMass = MolarMass(35.453,"g/mol"),\
                             alkalinity = 0)
speciesAddenda.append(Cl_1_)
Cl_3_ = AqueousMasterSpecies(symbol = "ClO2-",\
                             name = "Cl(3)",\
                             element = "Cl",\
                             molarMass = MolarMass(35.453,"g/mol"),\
                             alkalinity = 0)
speciesAddenda.append(Cl_3_)
Cl_p4_ = AqueousMasterSpecies(symbol = "ClO2",\
                              name = "Cl(+4)",\
                              element = "Cl",\
                              molarMass = MolarMass(35.453,"g/mol"),\
                              alkalinity = 0)
speciesAddenda.append(Cl_p4_)
Cl_p5_ = AqueousMasterSpecies(symbol = "ClO3-",\
                              name = "Cl(+5)",\
                              element = "Cl",\
                              molarMass = MolarMass(35.453,"g/mol"),\
                              alkalinity = 0)
speciesAddenda.append(Cl_p5_)
Cl_p7_ = AqueousMasterSpecies(symbol = "ClO4-",\
                              name = "Cl(+7)",\
                              element = "Cl",\
                              molarMass = MolarMass(35.453,"g/mol"),\
                              alkalinity = 0)
speciesAddenda.append(Cl_p7_)
Fe = AqueousMasterSpecies(symbol = "Fe++",\
                          name = "Fe",\
                          element = "Fe",\
                          molarMass = MolarMass(55.845,"g/mol"),\
                          alkalinity = 0.0)
speciesAddenda.append(Fe)
Fe_p2_ = AqueousMasterSpecies(symbol = "Fe++",\
                              name = "Fe(+2)",\
                              element = "Fe",\
                              molarMass = MolarMass(55.845,"g/mol"),\
                              alkalinity = -2)
speciesAddenda.append(Fe_p2_)
Fe_p3_ = AqueousMasterSpecies(symbol = "Fe+++",\
                              name = "Fe(+3)",\
                              element = "Fe",\
                              molarMass = MolarMass(55.845,"g/mol"),\
                              alkalinity = -2)
speciesAddenda.append(Fe_p3_)
K = AqueousMasterSpecies(symbol = "K+",\
                         name = "K",\
                         element = "K",\
                         molarMass = MolarMass(39.0983,"g/mol"),\
                         alkalinity = 0)
speciesAddenda.append(K)
Mg = AqueousMasterSpecies(symbol = "Mg++",\
                          name = "Mg",\
                          element = "Mg",\
                          molarMass = MolarMass(24.305,"g/mol"),\
                          alkalinity = 0.0)
speciesAddenda.append(Mg)
N = AqueousMasterSpecies(symbol = "NH3",\
                         name = "N",\
                         element = "N",\
                         molarMass = MolarMass(14.0067,"g/mol"),\
                         alkalinity = 1)
speciesAddenda.append(N)
N_m3_ = AqueousMasterSpecies(symbol = "NH3",\
                             name = "N(-3)",\
                             element = "N",\
                             molarMass = MolarMass(14.0067,"g/mol"),\
                             alkalinity = 1)
speciesAddenda.append(N_m3_)
N_0_ = AqueousMasterSpecies(symbol = "N2",\
                            name = "N(0)",\
                            element = "N",\
                            molarMass = MolarMass(14.0067,"g/mol"),\
                            alkalinity = 0)
speciesAddenda.append(N_0_)
N_m5_ = AqueousMasterSpecies(symbol = "CN-",\
                             name = "N(-5)",\
                             element = "N",\
                             molarMass = MolarMass(14.0067,"g/mol"),\
                             alkalinity = 0)
speciesAddenda.append(N_m5_)
N_p3_ = AqueousMasterSpecies(symbol = "NO2-",\
                             name = "N(+3)",\
                             element = "N",\
                             molarMass = MolarMass(14.0067,"g/mol"),\
                             alkalinity = 0)
speciesAddenda.append(N_p3_)
N_p5_ = AqueousMasterSpecies(symbol = "NO3-",\
                             name = "N(+5)",\
                             element = "N",\
                             molarMass = MolarMass(14.0067,"g/mol"),\
                             alkalinity = 0)
speciesAddenda.append(N_p5_)
Na = AqueousMasterSpecies(symbol = "Na+",\
                          name = "Na",\
                          element = "Na",\
                          molarMass = MolarMass(22.98977,"g/mol"),\
                          alkalinity = 0)
speciesAddenda.append(Na)
S = AqueousMasterSpecies(symbol = "SO4--",\
                         name = "S",\
                         element = "S",\
                         molarMass = MolarMass(32.064,"g/mol"),\
                         alkalinity = 0)
speciesAddenda.append(S)
S_m2_ = AqueousMasterSpecies(symbol = "HS-",\
                             name = "S(-2)",\
                             element = "S",\
                             molarMass = MolarMass(32.064,"g/mol"),\
                             alkalinity = 0)
speciesAddenda.append(S_m2_)
S_6_ = AqueousMasterSpecies(symbol = "SO4--",\
                            name = "S(6)",\
                            element = "S",\
                            molarMass = MolarMass(32.064,"g/mol"),\
                            alkalinity = 0)
speciesAddenda.append(S_6_)
S_4_ = AqueousMasterSpecies(symbol = "SO3--",\
                            name = "S(4)",\
                            element = "S",\
                            molarMass = MolarMass(32.064,"g/mol"),\
                            alkalinity = 0)
speciesAddenda.append(S_4_)
S_8_ = AqueousMasterSpecies(symbol = "HSO5-",\
                            name = "S(8)",\
                            element = "S",\
                            molarMass = MolarMass(32.064,"g/mol"),\
                            alkalinity = 0)
speciesAddenda.append(S_8_)
S_2_ = AqueousMasterSpecies(symbol = "S2O3--",\
                            name = "S(2)",\
                            element = "S",\
                            molarMass = MolarMass(32.064,"g/mol"),\
                            alkalinity = 0)
speciesAddenda.append(S_2_)
S_7_ = AqueousMasterSpecies(symbol = "S2O8--",\
                            name = "S(7)",\
                            element = "S",\
                            molarMass = MolarMass(32.064,"g/mol"),\
                            alkalinity = 0)
speciesAddenda.append(S_7_)
S_3_ = AqueousMasterSpecies(symbol = "S2O3--",\
                            name = "S(3)",\
                            element = "S",\
                            molarMass = MolarMass(32.064,"g/mol"),\
                            alkalinity = 0)
speciesAddenda.append(S_3_)
S_5_ = AqueousMasterSpecies(symbol = "S2O6--",\
                            name = "S(5)",\
                            element = "S",\
                            molarMass = MolarMass(32.064,"g/mol"),\
                            alkalinity = 0)
speciesAddenda.append(S_5_)
Si = AqueousMasterSpecies(symbol = "H4SiO4",\
                          name = "Si",\
                          element = "SiO2",\
                          molarMass = MolarMass(28.0855,"g/mol"),\
                          alkalinity = 0)
speciesAddenda.append(Si)
Sr = AqueousMasterSpecies(symbol = "Sr++",\
                          name = "Sr",\
                          element = "Sr",\
                          molarMass = MolarMass(32.064,"g/mol"),\
                          alkalinity = 0)
speciesAddenda.append(Sr)
#
AlpppSSp = AqueousSecondarySpecies(symbol = "Al+++",\
                                   formationReaction = [("Al+++",1)],\
                                   logK25 = 0,\
                                   activity_law = Davies(9.0),\
                                   name = "Al+++",)
speciesAddenda.append(AlpppSSp)
CappSSp = AqueousSecondarySpecies(symbol = "Ca++",\
                                  formationReaction = [("Ca++",1)],\
                                  logK25 = 0,\
                                  activity_law = Davies(6.0),\
                                  name = "Ca++",)
speciesAddenda.append(CappSSp)
ClmSSp = AqueousSecondarySpecies(symbol = "Cl-",\
                                 formationReaction = [("Cl-",1)],\
                                 logK25 = 0.0,\
                                 activity_law = Davies(3.0),\
                                 name = "Cl-",)
speciesAddenda.append(ClmSSp)
FeppSSp = AqueousSecondarySpecies(symbol = "Fe++",\
                                  formationReaction = [("Fe++",1)],\
                                  logK25 = 0,\
                                  activity_law = Davies(6.0),\
                                  name = "Fe++",)
speciesAddenda.append(FeppSSp)
H4SiO4SSp = AqueousSecondarySpecies(symbol = "H4SiO4",\
                                    formationReaction = [("H4SiO4",1)],\
                                    logK25 = 0,\
                                    activity_law = Davies(3.0),\
                                    name = "H4SiO4",)
speciesAddenda.append(H4SiO4SSp)
HCO3mSSp = AqueousSecondarySpecies(symbol = "HCO3-",\
                                   formationReaction = [("HCO3-",1)],\
                                   logK25 = 0,\
                                   activity_law = Davies(4.0),\
                                   name = "HCO3-",)
speciesAddenda.append(HCO3mSSp)
KpSSp = AqueousSecondarySpecies(symbol = "K+",\
                                formationReaction = [("K+",1)],\
                                logK25 = 0.0,\
                                activity_law = Davies(3.0),\
                                name = "K+",)
speciesAddenda.append(KpSSp)
MgppSSp = AqueousSecondarySpecies(symbol = "Mg++",\
                                  formationReaction = [("Mg++",1)],\
                                  logK25 = 0.0,\
                                  activity_law = Davies(8.0),\
                                  name = "Mg++",)
speciesAddenda.append(MgppSSp)
NapSSp = AqueousSecondarySpecies(symbol = "Na+",\
                                 formationReaction = [("Na+",1)],\
                                 logK25 = 0.0,\
                                 activity_law = Davies(4.0),\
                                 name = "Na+",)
speciesAddenda.append(NapSSp)
NH3SSp = AqueousSecondarySpecies(symbol = "NH3",\
                                 formationReaction = [("NH3",1)],\
                                 logK25 = 0.0,\
                                 activity_law = Davies(3.0),\
                                 name = "NH3",)
speciesAddenda.append(NH3SSp)
SO4mmSSp = AqueousSecondarySpecies(symbol = "SO4--",\
                                   formationReaction = [("SO4--",1)],\
                                   logK25 = 0.0,\
                                   activity_law = Davies(4.0),\
                                   name = "SO4mm",)
speciesAddenda.append(SO4mmSSp)
SrppSSp = AqueousSecondarySpecies(symbol = "Sr++",\
                                  formationReaction = [("Sr++",1)],\
                                  logK25 = 0.0,\
                                  activity_law = Davies(5.0),\
                                  name = "Srpp",)
speciesAddenda.append(SrppSSp)
H4SiOSSp = AqueousSecondarySpecies(symbol = "(SiO2)4(OH)4----",\
                                   formationReaction = [("4H4SiO4",1),("4H2O",-1),("4H+",-1)],\
                                   logK25 = -39.2,\
                                   logK = [-3.92000e+01, 0.00000e+00, 0.00000e+00, 0.00000e+00, 0.00000e+00],\
                                   activity_law = Davies(4.0),\
                                   name = "H4SiO",)
speciesAddenda.append(H4SiOSSp)
Al_OH_2SSp = AqueousSecondarySpecies(symbol = "Al(OH)2+",\
                                     formationReaction = [("Al+++",1),("2H2O",1),("2H+",-1)],\
                                     logK25 = -10.584,\
                                     logK = [3.00160e+02, 5.41526e-02, -2.07434e+04, -1.08328e+02, 9.54011e+05],\
                                     activity_law = Davies(4.0),\
                                     name = "Al(OH)2",)
speciesAddenda.append(Al_OH_2SSp)
AlH3SiO4SSp = AqueousSecondarySpecies(symbol = "AlH3SiO4++",\
                                      formationReaction = [("Al+++",1),("H4SiO4",1),("H+",-1)],\
                                      logK25 = -2.38,\
                                      logK = [-3.75313e+02, -2.92372e-02, 2.72955e+04, 1.28953e+02, -2.57662e+06],\
                                      activity_law = Davies(4.5),\
                                      name = "AlH3SiO4",)
speciesAddenda.append(AlH3SiO4SSp)
AlO2mSSp = AqueousSecondarySpecies(symbol = "AlO2-",\
                                   formationReaction = [("Al+++",1),("2H2O",1),("4H+",-1)],\
                                   logK25 = -22.873,\
                                   logK = [-1.78065e+02, -2.68922e-02, 1.86724e+03, 6.68385e+01, -7.50500e+05],\
                                   activity_law = Davies(4.0),\
                                   name = "AlO2m",)
speciesAddenda.append(AlO2mSSp)
AlOHppSSp = AqueousSecondarySpecies(symbol = "AlOH++",\
                                    formationReaction = [("Al+++",1),("H2O",1),("H+",-1)],\
                                    logK25 = -4.95,\
                                    logK = [1.61456e+02, 3.01851e-02, -1.15056e+04, -5.80546e+01, 6.07667e+05],\
                                    activity_law = Davies(4.5),\
                                    name = "AlOHpp",)
speciesAddenda.append(AlOHppSSp)
AlSO4SSp = AqueousSecondarySpecies(symbol = "AlSO4+",\
                                   formationReaction = [("Al+++",1),("SO4--",1)],\
                                   logK25 = 3.17,\
                                   logK = [2.31931e+03, 3.61431e-01, -1.34935e+05, -8.35858e+02, 8.61887e+06],\
                                   activity_law = Davies(4.5),\
                                   name = "AlSO4",)
speciesAddenda.append(AlSO4SSp)
Ca_HCO3_pSSp = AqueousSecondarySpecies(symbol = "Ca(HCO3)+",\
                                       formationReaction = [("HCO3-",1),("Ca++",1)],\
                                       logK25 = 1.103,\
                                       logK = [8.68609e+02, 1.45834e-01, -4.82814e+04, -3.16733e+02, 3.08324e+06],\
                                       activity_law = Davies(4.5),\
                                       name = "Ca(HCO3)p",)
speciesAddenda.append(Ca_HCO3_pSSp)
CaClpSSp = AqueousSecondarySpecies(symbol = "CaCl+",\
                                   formationReaction = [("Ca++",1),("1Cl-",1)],\
                                   logK25 = -0.29,\
                                   logK = [7.84304e+02, 1.29811e-01, -4.34926e+04, -2.85725e+02, 2.63001e+06],\
                                   activity_law = Davies(4.0),\
                                   name = "CaClp",)
speciesAddenda.append(CaClpSSp)
CaCl2SSp = AqueousSecondarySpecies(symbol = "CaCl2",\
                                   formationReaction = [("Ca++",1),("2Cl-",1)],\
                                   logK25 = -0.64,\
                                   logK = [1.56212e+03, 2.55796e-01, -8.58012e+04, -5.69819e+02, 5.22119e+06],\
                                   activity_law = Davies(3.0),\
                                   name = "CaCl2",)
speciesAddenda.append(CaCl2SSp)
CaCO3SSp = AqueousSecondarySpecies(symbol = "CaCO3",\
                                   formationReaction = [("HCO3-",1),("Ca++",1),("H+",-1)],\
                                   logK25 = -7.107,\
                                   logK = [6.95433e+02, 1.16330e-01, -3.61525e+04, -2.56844e+02, 1.74027e+06],\
                                   activity_law = Davies(3.0),\
                                   name = "CaCO3",)
speciesAddenda.append(CaCO3SSp)
CaOHpSSp = AqueousSecondarySpecies(symbol = "CaOH+",\
                                   formationReaction = [("Ca++",1),("H2O",1),("H+",-1)],\
                                   logK25 = -12.78,\
                                   logK = [1.31296e+02, 2.14182e-02, -1.01897e+04, -4.82243e+01, 2.70321e+05],\
                                   activity_law = Davies(4.0),\
                                   name = "CaOHp",)
speciesAddenda.append(CaOHpSSp)
CaSO4SSp = AqueousSecondarySpecies(symbol = "CaSO4",\
                                   formationReaction = [("Ca++",1),("SO4--",1)],\
                                   logK25 = 2.31,\
                                   logK = [1.72034e+03, 2.65735e-01, -9.42554e+04, -6.23564e+02, 5.49730e+06],\
                                   activity_law = Davies(3.0),\
                                   name = "CaSO4",)
speciesAddenda.append(CaSO4SSp)
CH4SSp = AqueousSecondarySpecies(symbol = "CH4",\
                                 formationReaction = [("HCO3-",1),("H+",1),("H2O",1),("2O2",-1)],\
                                 logK25 = -144.116,\
                                 logK = [1.12998e+03, 1.82310e-01, -1.12412e+05, -4.05513e+02, 4.62149e+06],\
                                 activity_law = Davies(3.0),\
                                 name = "CH4",)
speciesAddenda.append(CH4SSp)
Cl2SSp = AqueousSecondarySpecies(symbol = "Cl2",\
                                 formationReaction = [("Cl-",1),("1ClO-",1),("2H+",1),("1H2O",-1)],\
                                 logK25 = 10.874,\
                                 logK = [1.25714e+03, 2.11334e-01, -6.62374e+04, -4.57961e+02, 4.09635e+06],\
                                 activity_law = Davies(3.0),\
                                 name = "Cl2",)
speciesAddenda.append(Cl2SSp)
ClOmSSp = AqueousSecondarySpecies(symbol = "ClO-",\
                                  formationReaction = [("0.5O2",1),("1Cl-",1)],\
                                  logK25 = -15.089,\
                                  logK = [-1.27182e+02, -1.75488e-02, 4.91743e+03, 4.36329e+01, -6.34148e+05],\
                                  activity_law = Davies(4.0),\
                                  name = "ClOm",)
speciesAddenda.append(ClOmSSp)
ClO2mSSp = AqueousSecondarySpecies(symbol = "ClO2-",\
                                   formationReaction = [("O2",1),("1Cl-",1)],\
                                   logK25 = -23.095,\
                                   logK = [-1.61808e+02, -2.41055e-02, 5.18549e+03, 5.59816e+01, -8.90223e+05],\
                                   activity_law = Davies(4.0),\
                                   name = "ClO2m",)
speciesAddenda.append(ClO2mSSp)
ClO2SSp = AqueousSecondarySpecies(symbol = "ClO2",\
                                  formationReaction = [("1.25O2",1),("1Cl-",1),("1H+",1),("0.5H2O",-1)],\
                                  logK25 = -19.63,\
                                  logK = [1.72049e+02, 4.24307e-02, -9.64311e+03, -6.85214e+01, -2.16313e+05],\
                                  activity_law = Davies(3.0),\
                                  name = "ClO2",)
speciesAddenda.append(ClO2SSp)
ClO3mSSp = AqueousSecondarySpecies(symbol = "ClO3-",\
                                  formationReaction = [("1.5O2",1),("1Cl-",1)],\
                                  logK25 = -17.248,\
                                  logK = [-1.73543e+02, -2.71880e-02, 8.41489e+03, 5.99938e+01, -1.09094e+06],\
                                  activity_law = Davies(3.5),\
                                  name = "ClO3-",)
speciesAddenda.append(ClO3mSSp)
ClO4SSp = AqueousSecondarySpecies(symbol = "ClO4-",\
                                  formationReaction = [("2O2",1),("1Cl-",1)],\
                                  logK25 = -15.809,\
                                  logK = [-2.64670e+02, -4.03050e-02, 1.54460e+04, 9.16006e+01, -1.56335e+06],\
                                  activity_law = Davies(3.5),\
                                  name = "ClO4",)
speciesAddenda.append(ClO4SSp)
CNSSp = AqueousSecondarySpecies(symbol = "CN-",\
                                formationReaction = [("HCO3-",1),("1NH3",1),("0.5O2",-1),("2H2O",-1)],\
                                logK25 = -56.048,\
                                logK = [1.18527e+02, 1.72569e-02, -2.63240e+04, -4.01205e+01, 6.97619e+05],\
                                activity_law = Davies(3.0),\
                                name = "CN",)
speciesAddenda.append(CNSSp)

SCNmSSp = AqueousSecondarySpecies(symbol = "SCN-",\
                                  formationReaction = [("1CH4",1),("1NO3-",1),("1HS-",1),("1H+",1),("3H2O",-1)],\
                                  logK25 = 85.071,\
                                  logK = [3.28710e+02, 6.04959e-02, 7.96169e+03, -1.20818e+02, 9.40509e+05],\
                                  activity_law = Davies(3.5),\
                                  name = "SCN-",)
speciesAddenda.append(SCNmSSp)

NaHCO3SSp = AqueousSecondarySpecies(symbol = "NaHCO3",\
                                    formationReaction = [("1HCO3-",1),("1Na+",1)],\
                                    logK25 = -0.247,\
                                    logK = [7.69790e+02, 1.14620e-01, -4.14361e+04, -2.79679e+02, 2.38366e+06],\
                                    activity_law = Davies(3.0),\
                                    name = "NaHCO3",)
speciesAddenda.append(NaHCO3SSp)
KOHSSp = AqueousSecondarySpecies(symbol = "KOH",\
                                 formationReaction = [("1K+",1),("1H2O",1),("1H+",-1)],\
                                 logK25 = -14.46,\
                                 logK = [1.42384e+02, 1.63604e-02, -1.13130e+04, -5.17795e+01, 3.86363e+05],\
                                 activity_law = Davies(3.0),\
                                 name = "KOH",)
speciesAddenda.append(KOHSSp)
FeCO3SSp = AqueousSecondarySpecies(symbol = "FeCO3",\
                                   formationReaction = [("1HCO3-",1),("1Fe++",1),("1H+",-1)],\
                                   logK25 = -4.637,\
                                   logK = [9.47036e+02, 1.48162e-01, -5.17353e+04, -3.45654e+02, 2.93091e+06],\
                                   activity_law = Davies(3.0),\
                                   name = "FeCO3",)
speciesAddenda.append(FeCO3SSp)
H2S2O4SSp = AqueousSecondarySpecies(symbol = "H2S2O4",\
                                    formationReaction = [("1S2O4--",1),("2H+",1)],\
                                    logK25 = 2.8,\
                                    logK = [1.52382e+03, 2.41879e-01, -8.55041e+04, -5.51336e+02, 5.14655e+06],\
                                    activity_law = Davies(3.0),\
                                    name = "H2S2O4",)
speciesAddenda.append(H2S2O4SSp)
HSmSSp = AqueousSecondarySpecies(symbol = "HS-",\
                                 formationReaction = [("H+",1),("1SO4--",1),("2O2",-1)],\
                                 logK25 = -138.285,\
                                 logK = [1.04420e+03, 1.68673e-01, -1.06999e+05, -3.72414e+02, 4.23267e+06],\
                                 activity_law = Davies(3.5),\
                                 name = "HSm",)
speciesAddenda.append(HSmSSp)
HSO4mSSp = AqueousSecondarySpecies(symbol = "HSO4-",\
                                   formationReaction = [("1SO4--",1),("1H+",1)],\
                                   logK25 = 1.982,\
                                   activity_law = Davies(4.0),\
                                   logK = [8.16984e+02, 1.29499e-01, -4.74376e+04, -2.94022e+02, 2.93644e+06],\
                                   name = "HSO4-",)
speciesAddenda.append(HSO4mSSp)
HSO5mSSp = AqueousSecondarySpecies(symbol = "HSO5-",\
                                   formationReaction = [("0.5O2",1),("1H+",1),("1SO4--",1)],\
                                   logK25 = -17.22,\
                                   logK = [8.92767e+02, 1.40423e-01, -5.78293e+04, -3.20834e+02, 3.19924e+06],\
                                   activity_law = Davies(4.0),\
                                   name = "HSO5m",)
speciesAddenda.append(HSO5mSSp)
NaSO4mSSp = AqueousSecondarySpecies(symbol = "NaSO4-",\
                                    formationReaction = [("Na+",1),("1SO4--",1)],\
                                    logK25 = 0.936,\
                                    logK = [9.35875e+02, 1.44386e-01, -5.30229e+04, -3.38398e+02, 3.30639e+06],\
                                    activity_law = Davies(4.0),\
                                    name = "NaSO4-",)
speciesAddenda.append(NaSO4mSSp)
KAlO2SSp = AqueousSecondarySpecies(symbol = "KAlO2",\
                                   formationReaction = [("1Al+++",1),("1K+",1),("2H2O",1),("4H+",-1)],\
                                   logK25 = -24.222,\
                                   activity_law = Davies(3.0),\
                                   logK = [6.48972e+02, 9.81957e-02, -4.46804e+04, -2.31700e+02, 1.84110e+06],\
                                   name = "KAlO2",)
speciesAddenda.append(KAlO2SSp)
FeCO3pSSp = AqueousSecondarySpecies(symbol = "FeCO3+",\
                                    formationReaction = [("1HCO3-",1),("1Fe+++",1),("1H+",-1)],\
                                    logK25 = -0.607,\
                                    logK = [-6.06700e-01, 0.00000e+00, 0.00000e+00, 0.00000e+00, 0.00000e+00],\
                                    activity_law = Davies(4.5),\
                                    name = "FeCO3+",)
speciesAddenda.append(FeCO3pSSp)
S5O6mmSSp = AqueousSecondarySpecies(symbol = "S5O6--",\
                                    formationReaction = [("2.5S2O3--",1),("3H+",1),("1.5H2O",-1)],\
                                    logK25 = 0.872,\
                                    logK = [2.06895e+03, 3.32588e-01, -1.16108e+05, -7.50387e+02, 7.02004e+06],\
                                    activity_law = Davies(4.0),\
                                    name = "S5O6--",)
speciesAddenda.append(S5O6mmSSp)
Si3O6_OH_3mmmSSp = AqueousSecondarySpecies(symbol = "Si3O6(OH)3---",\
                                           formationReaction = [("3H4SiO4",1),("3H2O",-1),("3H+",-1)],\
                                           logK25 = -29.4,\
                                           activity_law = Davies(3.5),\
                                           logK = [-2.94000e+01, 0.00000e+00, 0.00000e+00, 0.00000e+00, 0.00000e+00],\
                                           name = "Si3O6(OH)3---",)
speciesAddenda.append(Si3O6_OH_3mmmSSp)
NO3mSSp = AqueousSecondarySpecies(symbol = "NO3-",\
                                  formationReaction = [("2O2",1),("1NH3",1),("1H+",-1),("1H2O",-1)],\
                                  logK25 = 62.093,\
                                  logK = [-8.29821e+02, -1.39902e-01, 6.88016e+04, 2.99153e+02, -3.32174e+06],\
                                  activity_law = Davies(3.0),\
                                  name = "NO3-",)
speciesAddenda.append(NO3mSSp)
FepppSSp = AqueousSecondarySpecies(symbol = "HFeO2",\
                                   formationReaction = [("Fe+++",1),("2H2O",1),("3H+",-1)],\
                                   logK25 = -31.8,\
                                   logK = [-1.76510e+02, -3.47558e-02, 4.90853e+02, 6.37165e+01, -3.76796e+05],\
                                   activity_law = Davies(4.5),\
                                   name = "Feppp",)
speciesAddenda.append(FepppSSp)
S2O4mmSSp = AqueousSecondarySpecies(symbol = "S2O4--",\
                                    formationReaction = [("2H+",1),("2SO4--",1),("1.5O2",-1),("1H2O",-1)],\
                                    logK25 = -118.281,\
                                    logK = [1.68947e+03, 2.71203e-01, -1.36622e+05, -6.06791e+02, 6.31906e+06],\
                                    activity_law = Davies(5.0),\
                                    name = "S2O4--",)
speciesAddenda.append(S2O4mmSSp)
NaCO3mSSp = AqueousSecondarySpecies(symbol = "NaCO3-",\
                                    formationReaction = [("1HCO3-",1),("1Na+",1),("1H+",-1)],\
                                    logK25 = -9.057,\
                                    logK = [8.87112e+02, 1.31444e-01, -5.11097e+04, -3.21239e+02, 2.75112e+06],\
                                    activity_law = Davies(4.5),\
                                    name = "NaCO3-",)
speciesAddenda.append(NaCO3mSSp)
MgOHSSp = AqueousSecondarySpecies(symbol = "MgOH+",\
                                  formationReaction = [("1Mg++",1),("1H2O",1),("1H+",-1)],\
                                  logK25 = -11.68,\
                                  logK = [2.43555e+02, 3.49076e-02, -1.77879e+04, -8.75035e+01, 9.36843e+05],\
                                  activity_law = Davies(4.5),\
                                  name = "MgOH",)
speciesAddenda.append(MgOHSSp)
NaOHSSp = AqueousSecondarySpecies(symbol = "NaOH",\
                                  formationReaction = [("1Na+",1),("1H2O",1),("1H+",-1)],\
                                  logK25 = -14.75,\
                                  logK = [5.63344e+02, 8.50749e-02, -3.41073e+04, -2.05917e+02, 1.81919e+06],\
                                  activity_law = Davies(3.0),\
                                  name = "NaOH",)
speciesAddenda.append(NaOHSSp)
MgSO4SSp = AqueousSecondarySpecies(symbol = "MgSO4",\
                                   formationReaction = [("1Mg++",1),("1SO4--",1)],\
                                   logK25 = 2.23,\
                                   logK = [1.69230e+03, 2.66884e-01, -9.18462e+04, -6.14813e+02, 5.30920e+06],\
                                   activity_law = Davies(3.0),\
                                   name = "MgSO4",)
speciesAddenda.append(MgSO4SSp)
MgCO3SSp = AqueousSecondarySpecies(symbol = "MgCO3",\
                                   formationReaction = [("1HCO3-",1),("1Mg++",1),("1H+",-1)],\
                                   logK25 = -7.347,\
                                   logK = [7.76983e+02, 1.26514e-01, -4.07179e+04, -2.86278e+02, 2.03515e+06],\
                                   activity_law = Davies(3.0),\
                                   name = "MgCO3",)
speciesAddenda.append(MgCO3SSp)
NOSSp = AqueousSecondarySpecies(symbol = "NO",\
                                formationReaction = [("0.166666666666667N2",1),("0.666666666666667NO2-",1),("0.666666666666667H+",1),("0.333333333333333H2O",-1)],\
                                logK25 = -7.261,\
                                logK = [5.42715e+02, 8.82677e-02, -3.44772e+04, -1.95732e+02, 2.10425e+06],\
                                activity_law = Davies(3.0),\
                                name = "NO",)
speciesAddenda.append(NOSSp)
SO32mSSp = AqueousSecondarySpecies(symbol = "SO3--",\
                                   formationReaction = [("SO4--",1),("0.5O2",-1)],\
                                   logK25 = -46.614,\
                                   logK = [9.67192e+01, 1.41608e-02, -2.07947e+04, -3.37931e+01, 5.16323e+05],\
                                   activity_law = Davies(4.5),\
                                   name = "SO32m",)
speciesAddenda.append(SO32mSSp)
Mg_HCO3_pSSp = AqueousSecondarySpecies(symbol = "Mg(HCO3)+",\
                                       formationReaction = [("1HCO3-",1),("1Mg++",1)],\
                                       logK25 = 1.038,\
                                       logK = [8.77196e+02, 1.38125e-01, -5.03249e+04, -3.17051e+02, 3.19785e+06],\
                                       activity_law = Davies(4.5),\
                                       name = "Mg(HCO3)+",)
speciesAddenda.append(Mg_HCO3_pSSp)
N2H6ppSSp = AqueousSecondarySpecies(symbol = "N2H6++",\
                                    formationReaction = [("1.33333333333333NH3",1),("0.333333333333333N2",1),("2H+",1)],\
                                    logK25 = -20.643,\
                                    logK = [-9.71471e+01, -2.89011e-02, -1.47842e+03, 3.72434e+01, -1.84580e+05],\
                                    activity_law = Davies(4.5),\
                                    name = "N2H6++",)
speciesAddenda.append(N2H6ppSSp)
N2H5pSSp = AqueousSecondarySpecies(symbol = "N2H5+",\
                                   formationReaction = [("1.33333333333333NH3",1),("0.333333333333333N2",1),("1H+",1)],\
                                   logK25 = -19.616,\
                                   logK = [5.85633e+01, -2.64097e-03, -9.63803e+03, -1.92028e+01, 2.17776e+05],\
                                   activity_law = Davies(4.5),\
                                   name = "N2H5+",)
speciesAddenda.append(N2H5pSSp)
NaAlO2SSp = AqueousSecondarySpecies(symbol = "NaAlO2",\
                                    formationReaction = [("1Al+++",1),("1Na+",1),("2H2O",1),("4H+",-1)],\
                                    logK25 = -23.629,\
                                    logK = [7.04223e+02, 1.11345e-01, -4.74887e+04, -2.53139e+02, 2.18701e+06],\
                                    activity_law = Davies(3.0),\
                                    name = "NaAlO2",)
speciesAddenda.append(NaAlO2SSp)
S2O8SSp = AqueousSecondarySpecies(symbol = "S2O8--",\
                                  formationReaction = [("0.5O2",1),("2H+",1),("2SO4--",1),("1H2O",-1)],\
                                  logK25 = -22.381,\
                                  logK = [1.52754e+03, 2.40604e-01, -9.48781e+04, -5.50368e+02, 5.19300e+06],\
                                  activity_law = Davies(4.0),\
                                  name = "S2O8",)
speciesAddenda.append(S2O8SSp)
S2O6SSp = AqueousSecondarySpecies(symbol = "S2O6--",\
                                  formationReaction = [("2H+",1),("2SO4--",1),("0.5O2",-1),("1H2O",-1)],\
                                  logK25 = -50.823,\
                                  logK = [1.56083e+03, 2.48323e-01, -1.06529e+05, -5.62141e+02, 5.56427e+06],\
                                  activity_law = Davies(4.0),\
                                  name = "S2O6",)
speciesAddenda.append(S2O6SSp)
S4O6mmSSp = AqueousSecondarySpecies(symbol = "S4O6--",\
                                    formationReaction = [("1S2O3--",1),("1S2O4--",1),("2H+",1),("1H2O",-1)],\
                                    logK25 = 27.056,\
                                    logK = [1.48816e+03, 2.38920e-01, -7.69903e+04, -5.37946e+02, 5.06684e+06],\
                                    activity_law = Davies(4.0),\
                                    name = "S4O6--",)
speciesAddenda.append(S4O6mmSSp)
CO3mmSSp = AqueousSecondarySpecies(symbol = "CO3--",\
                                   formationReaction = [("HCO3-",1),("1H+",-1)],\
                                   logK25 = -10.327,\
                                   logK = [-7.70584e+02, -1.24335e-01, 4.20388e+04, 2.77395e+02, -2.67274e+06],\
                                   activity_law = Davies(4.5),\
                                   name = "CO3mm",)
speciesAddenda.append(CO3mmSSp)
HSO3mSSp = AqueousSecondarySpecies(symbol = "HSO3-",\
                                   formationReaction = [("1SO3--",1),("1H+",1)],\
                                   logK25 = 7.17,\
                                   activity_law = Davies(4.0),\
                                   logK = [8.10377e+02, 1.30677e-01, -4.53602e+04, -2.91738e+02,     2.83198e+06],\
                                   name = "HSO3-",)
speciesAddenda.append(HSO3mSSp)
COSSp = AqueousSecondarySpecies(symbol = "CO",\
                                formationReaction = [("HCO3-",1),("1H+",1),("0.5O2",-1),("1H2O",-1)],\
                                logK25 = -41.718,\
                                logK = [8.53548e+02, 1.39334e-01, -6.46270e+04, -3.06481e+02, 3.40650e+06],\
                                activity_law = Davies(3.0),\
                                name = "CO",)
speciesAddenda.append(COSSp)
KClSSp = AqueousSecondarySpecies(symbol = "KCl",\
                                 formationReaction = [("1Cl-",1),("1K+",1)],\
                                 logK25 = -0.5,\
                                 logK = [7.89547e+02, 1.20470e-01, -4.47224e+04, -2.85535e+02, 2.71764e+06],\
                                 activity_law = Davies(3.0),\
                                 name = "KCl",)
speciesAddenda.append(KClSSp)
Mg4_OH_4SSp = AqueousSecondarySpecies(symbol = "Mg4(OH)4++++",\
                                      formationReaction = [("4Mg++",1),("4H2O",1),("4H+",-1)],\
                                      logK25 = -39.75,\
                                      logK = [1.52521e+03, 2.22192e-01, -9.25885e+04, -5.53196e+02, 4.28299e+06],\
                                      activity_law = Davies(5.5),\
                                      name = "Mg4(OH)4",)
speciesAddenda.append(Mg4_OH_4SSp)
NH4pSSp = AqueousSecondarySpecies(symbol = "NH4+",\
                                  formationReaction = [("1NH3",1),("1H+",1)],\
                                  logK25 = 9.241,\
                                  logK = [3.74946e+01, -1.54524e-03, -6.95604e+02, -1.14964e+01, 2.65551e+05],\
                                  activity_law = Davies(2.5),\
                                  name = "NH4+",)
speciesAddenda.append(NH4pSSp)
H2SSSp = AqueousSecondarySpecies(symbol = "H2S",\
                                 formationReaction = [("1HS-",1),("1H+",1)],\
                                 logK25 = 6.989,\
                                 logK = [7.48406e+02, 1.19818e-01, -4.13470e+04, -2.70323e+02, 2.70545e+06],\
                                 activity_law = Davies(3.0),\
                                 name = "H2S",)
speciesAddenda.append(H2SSSp)
ClO3SSp = AqueousSecondarySpecies(symbol = "ClO3-",\
                                  formationReaction = [("1.5O2",1),("1Cl-",1)],\
                                  logK25 = -17.248,\
                                  logK = [-1.73543e+02, -2.71880e-02, 8.41489e+03, 5.99938e+01, -1.09094e+06],\
                                  activity_law = Davies(3.5),\
                                  name = "ClO3",)
speciesAddenda.append(ClO3SSp)
N2SSp = AqueousSecondarySpecies(symbol = "N2",\
                                formationReaction = [("1.5O2",1),("2NH3",1),("3H2O",-1)],\
                                logK25 = 116.439,\
                                logK = [7.05822e+01, 1.09582e-03, 3.02218e+04, -2.43236e+01, 3.87339e+05],\
                                activity_law = Davies(3.0),\
                                name = "N2",)
speciesAddenda.append(N2SSp)
HClO2SSp = AqueousSecondarySpecies(symbol = "HClO2",\
                                   formationReaction = [("1ClO2-",1),("1H+",1)],\
                                   logK25 = 1.979,\
                                   logK = [7.88235e+02, 1.24334e-01, -4.45918e+04, -2.84503e+02, 2.68641e+06],\
                                   activity_law = Davies(3.0),\
                                   name = "HClO2",)
speciesAddenda.append(HClO2SSp)
CO2SSp = AqueousSecondarySpecies(symbol = "CO2",\
                                 formationReaction = [("HCO3-",1),("1H+",1),("1H2O",-1)],\
                                 logK25 = 6.353,\
                                 logK = [6.82172e+02, 1.14322e-01, -3.81658e+04, -2.46590e+02, 2.51368e+06],\
                                 activity_law = Davies(3.0),\
                                 name = "CO2",)
speciesAddenda.append(CO2SSp)
NaS2O3mSSp = AqueousSecondarySpecies(symbol = "NaS2O3-",\
                                     formationReaction = [("Na+",1),("1S2O3--",1)],\
                                     logK25 = 0.608,\
                                     logK = [1.60478e+03, 2.46830e-01, -8.86525e+04, -5.81598e+02, 5.21827e+06],\
                                     activity_law = Davies(4.5),\
                                     name = "NaS2O3-",)
speciesAddenda.append(NaS2O3mSSp)
S5mmSSp = AqueousSecondarySpecies(symbol = "S5--",\
                                  formationReaction = [("3HS-",1),("1S2O3--",1),("3H+",1),("3H2O",-1)],\
                                  logK25 = 27.95,\
                                  logK = [1.96401e+03, 3.20846e-01, -1.01625e+05, -7.13656e+02, 6.66939e+06],\
                                  activity_law = Davies(4.0),\
                                  name = "S5--",)
speciesAddenda.append(S5mmSSp)
H2S2O3SSp = AqueousSecondarySpecies(symbol = "H2S2O3",\
                                    formationReaction = [("1S2O3--",1),("2H+",1)],\
                                    logK25 = 2.32,\
                                    logK = [1.49785e+03, 2.38143e-01, -8.40489e+04, -5.42066e+02, 5.03796e+06],\
                                    activity_law = Davies(3.0),\
                                    name = "H2S2O3",)
speciesAddenda.append(H2S2O3SSp)
MgClpSSp = AqueousSecondarySpecies(symbol = "MgCl+",\
                                   formationReaction = [("1Cl-",1),("1Mg++",1)],\
                                   logK25 = 0.35,\
                                   logK = [8.36252e+02, 1.34226e-01, -4.68335e+04, -3.03733e+02, 2.90909e+06],\
                                   activity_law = Davies(4.0),\
                                   name = "MgCl+",)
speciesAddenda.append(MgClpSSp)
HClOSSp = AqueousSecondarySpecies(symbol = "HClO",\
                                  formationReaction = [("1ClO-",1),("1H+",1)],\
                                  logK25 = 7.55,\
                                  logK = [7.25218e+02, 1.14764e-01, -3.91213e+04, -2.61748e+02, 2.40081e+06],\
                                  activity_law = Davies(3.0),\
                                  name = "HClO",)
speciesAddenda.append(HClOSSp)
SO3mmSSp = AqueousSecondarySpecies(symbol = "H2SO3",\
                                   formationReaction = [("SO3--",1),("2H+",1)],\
                                   logK25 = 9.030,\
                                   logK = [1.29476e+03, 2.18164e-01, -7.30298e+04, -4.67718e+02, 4.57804e+06],\
                                   activity_law = Davies(3.0),\
                                   name = "SO3mm",)
speciesAddenda.append(SO3mmSSp)
S4mmSSp = AqueousSecondarySpecies(symbol = "S4--",\
                                  formationReaction = [("2.5HS-",1),("0.75S2O3--",1),("2H+",1),("2.25H2O",-1)],\
                                  logK25 = 18.037,\
                                  logK = [1.28520e+03, 2.10863e-01, -6.63227e+04, -4.67412e+02, 4.35576e+06],\
                                  activity_law = Davies(4.0),\
                                  name = "S4--",)
speciesAddenda.append(S4mmSSp)                              
HClSSp = AqueousSecondarySpecies(symbol = "HCl",\
                                 formationReaction = [("1Cl-",1),("1H+",1)],\
                                 logK25 = -0.71,\
                                 logK = [4.76805e+02, 9.08132e-02, -2.54571e+04, -1.77024e+02, 1.67351e+06],\
                                 activity_law = Davies(3.0),\
                                 name = "HCl",)
speciesAddenda.append(HClSSp)

KSO4mSSp = AqueousSecondarySpecies(symbol = "KSO4-",\
                                   formationReaction = [("1K+",1),("1SO4--",1)],\
                                   logK25 = 0.88,\
                                   logK = [9.15254e+02, 1.43488e-01, -5.12538e+04, -3.31519e+02, 3.11783e+06],\
                                   activity_law = Davies(4.0),\
                                   name = "KSO4-",)
speciesAddenda.append(KSO4mSSp)
Fe3pSSp = AqueousSecondarySpecies(symbol = "Fe+++",\
                                  formationReaction = [("0.25O2",1),("1Fe++",1),("1H+",1),("0.5H2O",-1)],\
                                  logK25 = 8.492,\
                                  logK = [-2.12373e+02, -3.53011e-02, 1.60599e+04, 7.47000e+01, -6.50245e+05],\
                                  activity_law = Davies(9.0),\
                                  name = "Fe3p",)
speciesAddenda.append(Fe3pSSp)
S2O3mmSSp = AqueousSecondarySpecies(symbol = "S2O3--",\
                                    formationReaction = [("2H+",1),("2SO4--",1),("2O2",-1),("1H2O",-1)],\
                                    logK25 = -133.412,\
                                    logK = [1.73328e+03, 2.79220e-01, -1.44725e+05, -6.21877e+02, 6.60133e+06],\
                                    activity_law = Davies(4.0),\
                                    name = "S2O3mm",)
speciesAddenda.append(S2O3mmSSp)
NaClSSp = AqueousSecondarySpecies(symbol = "NaCl",\
                                  formationReaction = [("1Cl-",1),("1Na+",1)],\
                                  logK25 = -0.5,\
                                  logK = [7.60519e+02, 1.20254e-01, -4.17744e+04, -2.76616e+02, 2.46299e+06],\
                                  activity_law = Davies(3.0),\
                                  name = "NaCl",)
speciesAddenda.append(NaClSSp)
NO2mSSp = AqueousSecondarySpecies(symbol = "NO2-",\
                                  formationReaction = [("1.5O2",1),("1NH3",1),("1H+",-1),("1H2O",-1)],\
                                  logK25 = 46.858,\
                                  logK = [-7.80342e+02, -1.31251e-01, 6.03156e+04, 2.82084e+02, -3.01919e+06],\
                                  activity_law = Davies(3.0),\
                                  name = "NO2-",)
speciesAddenda.append(NO2mSSp)
MgS2O3SSp = AqueousSecondarySpecies(symbol = "MgS2O3",\
                                    formationReaction = [("1Mg++",1),("1S2O3--",1)],\
                                    logK25 = 1.82,\
                                    logK = [1.82000e+00, 0.00000e+00, 0.00000e+00, 0.00000e+00, 0.00000e+00],\
                                    activity_law = Davies(3.0),\
                                    name = "MgS2O3",)
speciesAddenda.append(MgS2O3SSp)
#
#
Quartz_alphaAd = MineralSecondarySpecies(symbol = "SiO2",\
                                         formationReaction = [("2H2O",-1),("1H4SiO4",1)],\
                                         logK25 = 3.3953283,\
                                         logK = [1.45844e+01, 2.48382e-03, -1.88433e+03, -5.35743e+00, 4.55019e+04],\
                                         name = "Quartz_alpha",\
                                         density = Density(2650,"kg/m**3"))
speciesAddenda.append(Quartz_alphaAd)
Illite_MgAd = MineralSecondarySpecies(symbol = "K0.85Mg0.25Al2.35Si3.4O10(OH)2",\
                                      formationReaction = [("8.4H+",-1),("1.6H2O",-1),("2.35Al+++",1),("0.85K+",1),("0.25Mg++",1),("3.4H4SiO4",1)],\
                                      logK25 = 10.844,\
                                      logK = [-1.12970e+03, -1.92745e-01, 7.04402e+04, 4.04593e+02, -3.50116e+06],\
                                      name = "Illite_Mg",\
                                      density = Density(2770,"kg/m**3"))
speciesAddenda.append(Illite_MgAd)
PyriteAd = MineralSecondarySpecies(symbol = "FeS2",\
                                   formationReaction = [("3.5O2",-1),("1H2O",-1),("1Fe++",1),("2H+",1),("2SO4--",1)],\
                                   logK25 = 217.786,\
                                   logK = [-3.59065e+03, -5.80474e-01, 2.78096e+05, 1.29212e+03, -1.32014e+07],\
                                   name = "Pyrite",\
                                   density = Density(5010,"kg/m**3"))
speciesAddenda.append(PyriteAd)
Mg_Montmorillonite_NaAd = MineralSecondarySpecies(symbol = "Na0.33Mg0.33Al1.67Si4O10(OH)2",\
                                                  formationReaction = [("Al+++",1.67),("Mg++",0.33),("H+",-6),("0.33Na+",1),("H4SiO4",4),("H2O",-4)],\
                                                  logK25 = 2.999,\
                                                  logK = [-8.18158e+02, -1.38800e-01, 5.03309e+04, 2.92149e+02, -2.59365e+06],\
                                                  name = "Mg_Montmorillonite_Na",\
                                                  density = Density(2080,"kg/m**3"))
speciesAddenda.append(Mg_Montmorillonite_NaAd)
KaoliniteAd = MineralSecondarySpecies(symbol = "Al2Si2O5(OH)4",\
                                      formationReaction = [("6H+",-1),("2Al+++",1),("1H2O",1),("2H4SiO4",1)],\
                                      logK25 = 6.471,\
                                      logK = [-9.16789e+02, -1.50208e-01, 5.42404e+04, 3.28660e+02, -2.41129e+06],\
                                      name = "Kaolinite",\
                                      density = Density(2600,"kg/m**3"))
speciesAddenda.append(KaoliniteAd)
DolomiteAd = MineralSecondarySpecies(symbol = "CaMg(CO3)2",\
                                     formationReaction = [("2H+",-1),("2HCO3-",1),("1Ca++",1),("1Mg++",1)],\
                                     logK25 = 3.533,\
                                     logK = [-1.79236e+03, -2.89635e-01, 9.95945e+04, 6.51145e+02, -5.60084e+06],\
                                     name = "Dolomite",\
                                     density = Density(2830,"kg/m**3"))
speciesAddenda.append(DolomiteAd)
CalciteAd = MineralSecondarySpecies(symbol = "CaCO3",\
                                    formationReaction = [("H+",-1),("HCO3-",1),("Ca++",1)],\
                                    logK25 = 1.847,\
                                    logK = [-8.50102e+02, -1.39471e-01, 4.68810e+04, 3.09649e+02, -2.65915e+06],\
                                    name = "Calcite",\
                                    density = Density(2710,"kg/m**3"))
speciesAddenda.append(CalciteAd)
SideriteAd = MineralSecondarySpecies(symbol = "FeCO3",\
                                     formationReaction = [("1H+",-1),("1HCO3-",1),("1Fe++",1)],\
                                     logK25 = -0.473,\
                                     logK = [-9.15524e+02, -1.47685e-01, 5.05603e+04, 3.32122e+02, -2.87218e+06],\
                                     name = "Siderite",\
                                     density = Density(3740,"kg/m**3"))
speciesAddenda.append(SideriteAd)
#~~~~~~~~~~~~~~~~~
# Chemical State ~
#~~~~~~~~~~~~~~~~~
ChemicalStateList = []
essai4MineralPhase = MineralPhase([MineralTotalConcentration("Calcite",9.5023556, "mol/l",saturationIndex = 0.0),
                                  MineralTotalConcentration("Kaolinite",0.77411576, "mol/l",saturationIndex = 0.0),
                                  MineralTotalConcentration("Mg_Montmorillonite_Na",0.12864442, "mol/l",saturationIndex = 0.0),
                                  MineralTotalConcentration("Pyrite",0.7151211, "mol/l",saturationIndex = 0.0),
                                  MineralTotalConcentration("Illite_Mg",0.65161277, "mol/l",saturationIndex = 0.0),
                                  MineralTotalConcentration("Siderite",0.2913745, "mol/l",saturationIndex = 0.0),
                                  MineralTotalConcentration("Quartz_alpha",3.3953283, "mol/l",saturationIndex = 0.0),
                                  MineralTotalConcentration("Dolomite",0.26598307, "mol/l",saturationIndex = 0.0)])
essai4AqueousSolution = AqueousSolution (elementConcentrations = [ElementConcentration ("Ca",0.157e-1,"mol/l"),
                                                                  ElementConcentration ("Mg",0.26480e-2,"mol/l"),
                                                                  ElementConcentration ("Na",0.24487,"mol/l"),
                                                                  ElementConcentration ("K",0.45229e-2,"mol/l"),
                                                                  ElementConcentration ("Fe",0.70353e-4,"mol/l"),
                                                                  ElementConcentration ("Si",0.69203e-3,"mol/l"),
                                                                  ElementConcentration ("C(4)",0.35820e-2,"mol/l"),
                                                                  ElementConcentration ("S(6)",0.97838e-2,"mol/l"),
                                                                  ElementConcentration ("Al",0.26355e-7,"mol/l"),
                                                                  #ElementConcentration ("Cl",0.24998e-1,"mol/l")
                                                                 ],\
                                         pH = 6.162,\
                                         temperature =80.0,\
                                         pe = 4)
essai4ChemicalState = ChemicalState ("ultimate",essai4AqueousSolution,mineralPhase = essai4MineralPhase,\
                                     chargeBalance = ("Cl",0.24998e-1)
                                    )

#~~~~~~~~~
# Module ~
#~~~~~~~~~
module = Chemical()
problem  = ChemicalProblem(name               = "ultimate",\
                           chemistryDB        = "water_gui_brgm.dat",\
                           speciesBaseAddenda = speciesAddenda,\
                           chemicalState      = essai4ChemicalState)
module.setData(problem)
module.initialise()
module.setParameter("ultimate.out")
module.run()
module.outputStateSaving()
pH = 6.08544
IonicStrength = 0.292477418526
state = module.getOutput()
if abs(pH-state[4]) < 1.e-4:
    if abs(IonicStrength-state[7]) < 1.e-4:
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        print "Results can be considered as stable"
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    else:
        raise Warning, "problem with the ultimate solution test case"
else:
    raise Warning, "problem with the ultimate solution test case"

print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "        End of the ultimate test case ~"
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
