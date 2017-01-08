from species import *
#
# SOLUTION_MASTER_SPECIES
#
Tr = AqueousMasterSpecies(symbol = "Tr+",\
                          name = "Tr",\
                          element = "Tr",\
                          molarMass = MolarMass(35.0,"kg/mol"),\
                          alkalinity = 0)
#
H = AqueousMasterSpecies(symbol = "H+",\
                         name = "H",\
                         element = "H",\
                         molarMass = MolarMass(0.001008,"kg/mol"),\
                         alkalinity = -1.)
#
E = AqueousMasterSpecies(symbol = "e-",\
                         name = "E",\
                         element = "0.0",\
                         molarMass = MolarMass(0.0,"kg/mol"),\
                         alkalinity = 0.0)
#
O = AqueousMasterSpecies(symbol = "H2O",\
                         name = "O",\
                         element = "O",\
                         molarMass = MolarMass(0.016,"kg/mol"),\
                         alkalinity = 0.0)
#
#
# SOLUTION_SPECIES
#
TrSSp = AqueousSecondarySpecies(symbol            = "Tr+",\
                                formationReaction = [("Tr+",1)],\
                                logK25            = 0,\
                                name              = "Tr")
#
emSSp = AqueousSecondarySpecies(symbol            = "e-",\
                                formationReaction = [('e-', 1)],\
                                logK25            = 0.000,\
                                name              = "em")
#
OHmSSp = AqueousSecondarySpecies(symbol            = "OH-",\
                                 formationReaction = [('H2O', 1), ('H+', -1)],\
                                 logK25            = -1.400000e+01,\
                                 logK              = [-2.8397100000e+02, -5.0698420000e-02, 1.3323000000e+04, 1.0224447000e+02, -1.1196690000e+06, ],\
                                 name              = "OH-")
#
H2SSp = AqueousSecondarySpecies(symbol            = "H2",\
                                formationReaction = [('H+', 2), ('e-', 2)],\
                                logK25            = -3.15,\
                                name              = "H2")
#
HpSSp = AqueousSecondarySpecies(symbol            = "H+",\
                                formationReaction = [('H+', 1)],\
                                logK25            = 0.000,\
                                name              = "Hp")
#
H2OSSp = AqueousSecondarySpecies(symbol            = "H2O",\
                                 formationReaction = [('H2O', 1)],\
                                 logK25            = 0.000,\
                                 name              = "H2O")
#
O2SSp = AqueousSecondarySpecies(symbol            = "O2",\
                                formationReaction = [('H2O', 2), ('H+', -4), ('e-', -4)],\
                                logK25            = -86.08,\
                                name              = "O2")
#
#
# PHASES
#
H2lbgrbMS = MineralSecondarySpecies(symbol            = "H2",\
                                    formationReaction = [('H2', 1)],\
                                    logK25            = -3.150,\
                                    name              = "H2lbgrb")
#
H2OlbgrbMS = MineralSecondarySpecies(symbol            = "H2O",\
                                     formationReaction = [('H2O', 1)],\
                                     logK25            = 1.51,\
                                     name              = "H2Olbgrb")
#
O2lbgrbMS = MineralSecondarySpecies(symbol            = "O2",\
                                    formationReaction = [('O2', 1)],\
                                    logK25            = -2.960,\
                                    name              = "O2lbgrb")
#
