from chemistry import *
from chemicalmodule import *
from phreeqc import *

Phreeqc_file = "column.txt"      # bounded to Phreeqc
ProblemName  = "column"          # Phreeqc file 
#~~~~~~~~~~~~~~~~~~~
# Chemical Addenda ~
#~~~~~~~~~~~~~~~~~~~
speciesAddenda = []
Na = AqueousMasterSpecies(symbol = "Na+",\
                          name = "Na",\
                          element = "Na",\
                          molarMass = MolarMass(0.0229898,"kg/mol"),\
                          alkalinity = 0.0)
speciesAddenda.append(Na)
Si = AqueousMasterSpecies(symbol = "H4SiO4",\
                          name = "Si",\
                          element = "SiO2",\
                          molarMass = MolarMass(0.0280843,"kg/mol"),\
                          alkalinity = 0.0)
speciesAddenda.append(Si)
NaSSp = AqueousSecondarySpecies(symbol = "Na+",\
                                formationReaction = [("Na+",1)],\
                                logK25 = 0.0,\
                                name = "Na",)
speciesAddenda.append(NaSSp)
SiSSp = AqueousSecondarySpecies(symbol = "H4SiO4",\
                                formationReaction = [("H4SiO4",1)],\
                                logK25 = 0.0,\
                                name = "Si",)
speciesAddenda.append(SiSSp)
H3SiO4SSp = AqueousSecondarySpecies(symbol = "H3SiO4-",\
                                    formationReaction = [("H4SiO4",1),("H+",-1)],\
                                    logK25 = -9.83,\
                                    name = "H3SiO4",)
speciesAddenda.append(H3SiO4SSp)
QuartzAd = MineralSecondarySpecies(symbol = "SiO2",\
                                   formationReaction = [("H2O",-2),("H4SiO4",1)],\
                                   logK25 = -3.6,\
                                   name = "Quartz",\
                                   density = Density(2648.29,"kg/m**3"))
speciesAddenda.append(QuartzAd)
#~~~~~~~~~~~~~~~~~
# Chemical State ~
#~~~~~~~~~~~~~~~~~
ChemicalStateList = []
columnAqueousSolution = AqueousSolution (elementConcentrations = [ElementConcentration ("Na",2.0e-2,"mol/l")
                                                                 ],\
                                         pH = 12.2545,\
                                         pe = 4)
columnChemicalState = ChemicalState ("column",columnAqueousSolution)

#~~~~~~~~~
# Module ~
#~~~~~~~~~
module = Chemical()
problem  = ChemicalProblem(name               = "column",\
                           chemistryDB        = "phreeqc.dat",\
                           speciesBaseAddenda = speciesAddenda,\
                           chemicalState      = columnChemicalState)
module.setData(problem)
module.initialise()
module.setParameter("column.out")
module.run()
module.outputStateSaving()

print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "        End of the column case ~"
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
