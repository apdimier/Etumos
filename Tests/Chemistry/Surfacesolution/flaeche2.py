from chemistry import *
from chemicalmodule import *
from phreeqc import *

Phreeqc_file = "flaeche2.txt"      # bounded to Phreeqc
ProblemName  = "flaeche2"          # Phreeqc file 
#~~~~~~~~~~~~~~~~~~~
# Chemical Addenda ~
#~~~~~~~~~~~~~~~~~~~
speciesAddenda = []
Fix_HAd = MineralSecondarySpecies(symbol = "H+",\
                                  formationReaction = [("H+",1)],\
                                  logK25 = 0.0,\
                                  name = "Fix_H+",\
                                  density = Density(3000,"kg/m**3"))
speciesAddenda.append(Fix_HAd)
Surf_s = SurfaceMasterSpecies(symbol = "Surf_sOH",\
                              name = "Surf_s")
Hfo_sOCap = SurfaceSecondarySpecies(symbol = "Hfo_sOCa+",\
                                    formationReaction = [("Hfo_sOH",1),("Ca+2",1),("H+",-1)],\
                                    logK25 = -5.85)
speciesAddenda.append(Hfo_sOCap)
Hfo_wOCap = SurfaceSecondarySpecies(symbol = "Hfo_wOCa+",\
                                    formationReaction = [("Hfo_wOH",1),("Ca+2",1),("H+",-1)],\
                                    logK25 = -5.85)
speciesAddenda.append(Hfo_wOCap)
#~~~~~~~~~~~~~~~~~
# Chemical State ~
#~~~~~~~~~~~~~~~~~
ChemicalStateList = []
flaeche2MineralPhase = MineralPhase([])
flaeche2AqueousSolution = AqueousSolution (elementConcentrations = [ElementConcentration ("Ca",1.e-6,"mol/l"),
ElementConcentration ("Cl",5.e-3,"mol/l"),
ElementConcentration ("Na",5.e-3,"mol/l"),
                                                                   ],\
                                           pH = 6.5,\
                                           pe = 4)
flaeche2ChemicalState = ChemicalState ("flaeche2",flaeche2AqueousSolution,flaeche2MineralPhase,charge=True)

#~~~~~~~~~
# Module ~
#~~~~~~~~~
module = Chemical()
problem  = ChemicalProblem(name               = "flaeche2",\
                           chemistryDB                = "phreeqc.dat",\
                           speciesBaseAddenda = speciesAddenda,\
                           chemicalState      = flaeche2ChemicalState)
module.setData(problem)
module.initialise()
module.setParameter("flaeche2.out")
module.run()
module.outputStateSaving()

print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "        End of the flaeche2 case ~"
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
