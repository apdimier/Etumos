"""
used to generate the script file in an automated way.
"""
from __future__ import absolute_import
from __future__ import print_function
from dotextract import *
from docmodelbuilder import modelToBuild, color, pythonControl
import os
import re
import sys
from six.moves import range
print(sys.argv)
try:
    print(sys.argv)
    if sys.argv[1] != None:
        fileToAnalyse = sys.argv[1]
except:
    raise Warning(" You have to give the file as argument of the scrypt")        
text = get_doc_text(fileToAnalyse)
studyName, meshList, materialList, aqueousMasterSpeciesTable, secondarySpeciesTable, mineralSecondarySpeciesTable, chemicalStatesTable, initialConditions, boundaryConditions, solvers, transportSolverParameters, expectedOutputs, pythonConstants, simulationTime, couplingAlgorithmDic, postProcessingTable = modelToBuild(fileToAnalyse)
"""
The meshlayers are described via the first table of the odt file.
we give the name of the study to the mesh to be generated; the mesh being a gmsh mesh.

"""
#
# mesh file
#
meshName = studyName[0].lower()+studyName[1:]+".geo"
meshFile = open(meshName,"w")
meshFile.write("//\"\"\"\n")
numberOfZones = get_tableDim(meshList)[1]-1
meshFile.write("// the mesh entails %s zones\n"%(numberOfZones))
meshFile.write("//\"\"\"\n")
numberOfZoneIdentifiers = get_tableDim(meshList)[0]
for zone in range(numberOfZones):
    izone = zone+1
    meshFile.write("nx%i = %s;\n"%(izone, meshList[numberOfZoneIdentifiers*izone+2]))
for zone in range(numberOfZones):
    izone = zone+1
    meshFile.write("L%i = %s;\n"%(izone, meshList[numberOfZoneIdentifiers*izone+3]))
meshFile.write("EX1=L1;\n")
for zone in range(numberOfZones):
    if zone != 0:
        izone = zone+1
        meshFile.write("EX%i = EX%s+L%s;\n"%(izone,zone,izone))
meshFile.write("Point(1) = {0.0,0.0,0.0,1};\n")
for zone in range(numberOfZones):
    izone = zone+1
    meshFile.write("Point(%s) = {EX%s,0.0,0.0,1};\n"%(izone+1,izone))
lzone = izone+1
izone = lzone
for zone in range(numberOfZones):
    izone = izone+1
    meshFile.write("Line(%s) = {%s,%s};\n"%(izone,zone+1,zone+2))
tzone = lzone
for zone in range(numberOfZones):
    tzone = tzone+1
    meshFile.write("Transfinite Line {%s} = nx%s Using Progression %s;\n"%(tzone,zone+1,meshList[numberOfZoneIdentifiers*(zone+1)+4]))
meshFile.write("Physical Point(\"inlet\")         = {1};\n")
tzone = lzone
for zone in range(numberOfZones):
    tzone = tzone+1
    meshFile.write("Physical Line(\"%s\")          = {%s};\n"%(meshList[numberOfZoneIdentifiers*(zone+1)+1],tzone))
meshFile.close()
os.system("gmsh %s -2"%(meshName))
#
# script file
#
studyName = studyName[0].lower()+studyName[1:]
scriptName = studyName[0].lower()+studyName[1:]+".py"
studyFile = open(scriptName,"w")
studyFile.write("from constant import epspH\n")
studyFile.write("import os                  # for file path\n")
studyFile.write("from mesh import *         # for Meshes treatment\n")
studyFile.write("from datamodel import *\n")
studyFile.write("import sys\n")
studyFile.write("from chemicaltransportmodule import *\n")
studyFile.write("from listtools import normMaxListComparison, subtractLists\n")
studyFile.write("from chemistry import FreeKineticLaw\n")
studyFile.write("from generictools import postPlotter, reportAddendum\n")
studyFile.write("from math import pi\n")
studyFile.write("import os\n")
#
#
#
studyFile.write("problemName  = \"%s\"            # Phreeqc file\n"%(studyName))
studyFile.write("setProblemType(\"ChemicalTransport\")\n")
studyFile.write("#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
studyFile.write("#~ Definition of specific constants ~\n")
studyFile.write("#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n")
if solvers[0].lower() == "elmer":
    studyFile.write("dico = { 'MethodChoice' : 'FE'}\n")
print(pythonConstants)
print(" list of pythonConstants")
for line in pythonConstants:
    print(line)
    pline = pythonControl(str(line))
    studyFile.write("%s\n"%(pline[0]))
    #studyFile.write("%s\n"%(pythonControl(pline)))
    #raw_input()
studyFile.write("#~~~~~~~~~~~~~~~~~~\n")
studyFile.write("#~ Mesh extension ~\n")
studyFile.write("#~~~~~~~~~~~~~~~~~~\n\n")
studyFile.write("meshFileName = \"%s.msh\"\n"%(studyName))
studyFile.write("mesh = Mesh1D(meshFileName)\n")
studyFile.write("numberOfVertices = mesh._getNumberOfVertices()\n")
for layer in range(numberOfZones):
    layerName = meshList[numberOfZoneIdentifiers*(layer+1)+1]
    studyFile.write("%sBody = mesh.getBody(\'%s\')\n"%(layerName, layerName))
studyFile.write("inletBody = mesh.getBody(\'inlet\')\n")
#
# we define the different materials // for the moment, the number
# of properties is fixed.
#
numberOfLines = numberOfZones+2
#silicateMaterial = Material (name = "silicate", effectiveDiffusion = EffectiveDiffusion (2.0e-10,unit="m**2/s"),\
#                             permeability = Permeability(value = 1.0),\
#                             porosity = Porosity(value = silicatePorosity),\
#                             kinematicDispersion = KinematicDispersion (5.e-7,0)
#                            )
numberOfColumns = len(materialList)/numberOfLines
print("number of columns: ",len(materialList),numberOfColumns,numberOfZones,numberOfLines)
studyFile.write("#~~~~~~~~~~~~~\n")
studyFile.write("#~ Materials ~\n")
studyFile.write("#~~~~~~~~~~~~~\n\n")
for layer in range(numberOfZones):
    layerName = meshList[numberOfZoneIdentifiers*(layer+1)+1]
    ind = numberOfColumns*(2+layer)
    #print ind
    #print materialList
    #raw_input()
    effectivediffusion      = materialList[ind+1]
    effectivediffusionUnit  = "\""+materialList[numberOfColumns+1]+"\""
    permeability            = materialList[ind+2]
    permeabilityUnit        = "\""+materialList[numberOfColumns+2]+"\""
    porosity                = materialList[ind+3]
    kinematicDispersion     = materialList[ind+4]
    kinematicDispersionUnit = "\""+materialList[numberOfColumns+4]+"\""
    length = len(layerName)+len("Material = Material (")
    miseenpage = "\n"+" "*length
    #string = "%sMaterial = Material (\\"+
    #         "%sname = \"%s\", effectivediffusion = EffectiveDiffusion (%s,unit = %s),\\"
    formatString = "%sMaterial = Material (\\"+\
                                            "%sname = \"%s\", effectivediffusion = EffectiveDiffusion (%s,unit = %s),\\"+\
                                            "%spermeability = Permeability(%s,%s),\\"+\
                                            "%sporosity = Porosity(%s),\\"+\
                                            "%skinematicDispersion = KinematicDispersion(%s,unit = %s),\\"+\
                                            "%s)\n"
    studyFile.write(formatString
                    %(layerName, miseenpage, layerName,\
                    effectivediffusion,effectivediffusionUnit,
                    miseenpage, permeability,permeabilityUnit,
                    miseenpage, porosity,
                    miseenpage, kinematicDispersion,kinematicDispersionUnit, miseenpage[:-1]))
studyFile.write("#~~~~~~~~~~~\n")
studyFile.write("#~ Regions ~\n")
studyFile.write("#~~~~~~~~~~~\n")
lengthOfKeys = 0
studyFile.write("listOfRegions = []\n")
for layer in range(numberOfZones):
    layerName = meshList[numberOfZoneIdentifiers*(layer+1)+1]
    lengthOfKeys = max(lengthOfKeys,len(layerName))
for boundaryCondition in boundaryConditions.keys():
    regionName = "%sRegion"%(boundaryCondition)+" "*(lengthOfKeys-len(boundaryCondition))
    studyFile.write("%s = Region(support =      %sBody,        material =       %sMaterial)\n"\
                    %(regionName,boundaryCondition, meshList[numberOfZoneIdentifiers*(0+1)+1]))
studyFile.write("listOfRegions.append(%sRegion)\n"%(boundaryCondition))
print(numberOfZones)
#raw_input()
for layer in range(numberOfZones):
    layerName = meshList[numberOfZoneIdentifiers*(layer+1)+1]
    regionName = "%sRegion"%(layerName)+" "*(lengthOfKeys-len(layerName))
    regionBody = "%sBody"%(layerName)+" "*(lengthOfKeys-len(layerName))
    studyFile.write("%s = Region(support =      %s,  material =       %sMaterial)\n"%(regionName,regionBody,layerName))
    studyFile.write("listOfRegions.append(%sRegion)\n"%(layerName))
studyFile.write("#~~~~~~~~~~~~~~~~~~~\n")
studyFile.write("# Chemical Addenda ~\n")
studyFile.write("#~~~~~~~~~~~~~~~~~~~\n")
studyFile.write("speciesAddenda = []\n")
#
# master species
#
#
# numberOfArguments is the number of arguments necessary to define the specices(length of a line)
#
numberOfArguments = 5
numberOfAMS = len(aqueousMasterSpeciesTable)/numberOfArguments-1
ind = numberOfArguments-1
for ams in range(numberOfAMS):
    ind+= (ams*(numberOfArguments))+1
    symbol = aqueousMasterSpeciesTable[ind]
    name   = aqueousMasterSpeciesTable[ind+1]
    element = aqueousMasterSpeciesTable[ind+2]
    molarMass = aqueousMasterSpeciesTable[ind+3]
    alkalinity = aqueousMasterSpeciesTable[ind+4]
    length = len(name)+len("AMS = AqueousMasterSpecies(")
    miseenpage = "\n"+" "*length
    formatString = "%sAMS = AqueousMasterSpecies(symbol = \"%s\",\\"+\
                   "%sname = \"%s\",\\"+\
                   "%selement = \"%s\",\\"+\
                   "%smolarMass = MolarMass(%s,\"g/mol\"),\\"+\
                   "%salkalinity = %s,\\"+\
                   "%s)\n"
    studyFile.write(formatString
                    %(name, symbol, miseenpage,  name, miseenpage,  element, miseenpage,  molarMass, miseenpage, alkalinity, miseenpage[:-1]))
    studyFile.write("speciesAddenda.append(%sAMS)\n"%(name))
#
# secondary species
#
#            formationReaction (list of tuple (string,float), ex : [('Al[3+]',1),('F[-]',2.)],
#                               )
numberOfArguments = 4
numberOfSSp = len(secondarySpeciesTable)/numberOfArguments-1
ind = 3
for ssp in range(numberOfSSp):
    ind+= (ssp*(numberOfArguments))+1
    symbol = secondarySpeciesTable[ind]
    name   = secondarySpeciesTable[ind+1]
    formationReaction = formationReactionIdentification(secondarySpeciesTable[ind+2])
    #print "formationReaction",formationReaction
    logK25 = secondarySpeciesTable[ind+3]
    length = len(name)+len("SSp = AqueousSecondarySpecies(")
    miseenpage = "\n"+" "*length
    formatString = "%sSSp = AqueousSecondarySpecies(symbol = \"%s\",\\"+\
                    "%sformationReaction = %s,\\"+\
                    "%slogK25 = %s,\\"+\
                    "%sname = \"%s\",\\"+\
                    "%s)\n"
    studyFile.write(formatString%(name, symbol, miseenpage, formationReaction, miseenpage, logK25, miseenpage, name, miseenpage[:-1]))
    studyFile.write("speciesAddenda.append(%sSSp)\n"%(name))

numberOfArguments = 4
numberOfMSSp = len(mineralSecondarySpeciesTable)/numberOfArguments-1
ind = 3
for mssp in range(numberOfMSSp):
    ind+= (mssp*(numberOfArguments))+1
    symbol = mineralSecondarySpeciesTable[ind]
    name   = mineralSecondarySpeciesTable[ind+1]
    name1   = name.replace("+","").replace("-","")
    formationReaction = formationReactionIdentification(mineralSecondarySpeciesTable[ind+2])
    logK25 = mineralSecondarySpeciesTable[ind+3]
    length = len(name1)+len("MSSp = MineralSecondarySpecies(")
    miseenpage = "\n"+" "*length
    formatString = "%sMSSp = MineralSecondarySpecies(symbol = \"%s\",\\"+\
                    "%sformationReaction = %s,\\"+\
                    "%slogK25 = %s,\\"+\
                    "%sname = \"%s\",\\"+\
                    "%s)\n"   
    studyFile.write(formatString%(name1, symbol, miseenpage, formationReaction, miseenpage, logK25, miseenpage, name, miseenpage[:-1]))
    studyFile.write("speciesAddenda.append(%sMSSp)\n"%(name1))
#
#Fix_HpAd = MineralSecondarySpecies(symbol = "H+",\
#                                   formationReaction = [("H+",1)],\
#                                   logK25 = 0.0,\
#                                   name = "Fix_H+")

#
# mineral species
#
studyFile.write("#~~~~~~~~~~~~~~~~~~\n")
studyFile.write("# Chemical States ~\n")
studyFile.write("#~~~~~~~~~~~~~~~~~~\n\n")
studyFile.write("ChemicalStateList = []\n")
for key in chemicalStatesTable.keys():
    #
    # aqueous
    #
    studyFile.write("#\n")
    keyNameTobeused = key[0].lower()+key[1:]
    studyFile.write("# %s chemical state: aqueous phase\n"%(keyNameTobeused))
    studyFile.write("#\n")
    dec1 = len("%sAqueousSolution = AqueousSolution("%(keyNameTobeused))
    line = "%sAqueousSolution = AqueousSolution(elementConcentrations = [\n"%(keyNameTobeused)
    lineLength = len(line)
    endOfList = " "*(lineLength-2)+"],\\\n"
    for tp in chemicalStatesTable[key]["species"]:
        line+= (lineLength-1)*" "+"ElementConcentration (\"%s\",%s,\"%s\"),\\\n"%(tp[0],tp[1],tp[2])
    ph = " "*dec1+"pH = %s,\\\n"%(chemicalStatesTable[key]["pH"])
    pe = " "*dec1+"pe = %s,\\\n"%(chemicalStatesTable[key]["pe"])
    temperature = " "*dec1+"temperature = %s)"%(chemicalStatesTable[key]["T"])
    studyFile.write("%s%s%s%s%s\n"%(line, endOfList, ph, pe, temperature))
    #
    # mineral
    #
    keyNameTobeused = key[0].lower()+key[1:]
    studyFile.write("#\n")
    studyFile.write("# %s chemical state: mineral phase\n"%(keyNameTobeused))
    studyFile.write("#\n")
    line = "%sMineralPhase = MineralPhase([\n"%(keyNameTobeused)
    lineLength = len(line)
    for minSp in chemicalStatesTable[key]["mineralSpecies"]:
        minSp[3] = minSp[3].replace(u"\u201c","").replace(u"\u201d","").replace("'","")
        #print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",minSp[0]
        #print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",minSp[1]
        #print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",minSp[2]
        #print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",minSp[3]
        #raw_input()
        line+= (lineLength-1)*" "+"MineralTotalConcentration (\"%s\", %s, \"%s\", saturationIndex = %s),\\\n"%(minSp[0],minSp[1],minSp[3].encode("utf-8"),minSp[2])
    endOfList = " "*(lineLength-2)+"])\n"
    studyFile.write("%s%s\n"%(line, endOfList))
    #
    # now we can write down the chemical state
    #
    studyFile.write("%sChemicalState = ChemicalState (\"%s\", %sAqueousSolution, mineralPhase = %sMineralPhase)\n"%(keyNameTobeused, keyNameTobeused, keyNameTobeused, keyNameTobeused))
    studyFile.write("ChemicalStateList.append(%sChemicalState)\n"%(keyNameTobeused))
#calciteChemicalState = ChemicalState ("calcite",calciteAqueousSolution,mineralPhase = calciteMineralPhase)
#ChemicalStateList.append(calciteChemicalState)
#
# initial conditions
#
studyFile.write("#~~~~~~~~~~~~~~~~~~~~\n")
studyFile.write("# Initial condition ~\n")
studyFile.write("#~~~~~~~~~~~~~~~~~~~~\n\n")
print(color.BOLD+"initialConditions: "+color.END,initialConditions)
lengthOfKeys = 0
studyFile.write("listOfInitialConditions = []\n")
for key in initialConditions.keys():
    lengthOfKeys = max(lengthOfKeys,len(key))
formIC = "%"+str(lengthOfKeys)+"sIC"
for initialCondition in initialConditions.keys():
    stringIC = "%sIC%s"%(initialCondition," "*(lengthOfKeys-len(initialCondition)))
    lenstringIC = len(stringIC)
    stringBody = "= InitialCondition (body  = %sBody%s"%(initialCondition," "*(lengthOfKeys-len(initialCondition)))
    lenstringBody = len(stringBody)
    studyFile.write("%s %s, value = %sChemicalState)\n"%(stringIC,stringBody,initialConditions[initialCondition]))
    studyFile.write("listOfInitialConditions.append(%sIC)\n"%(initialCondition))

studyFile.write("#~~~~~~~~~~~~~~~~~~~~~\n")
studyFile.write("# Boundary condition ~\n")
studyFile.write("#~~~~~~~~~~~~~~~~~~~~~\n\n")
studyFile.write("listOfBoundaryConditions = []\n")
for boundaryCondition in boundaryConditions.keys():
    stringBC = "%sBC"%(boundaryCondition)
    lenstringBC = len(stringBC)
    btype = boundaryConditions[boundaryCondition]["bcType"]
    stringBody = "= BoundaryCondition (boundary  = %sBody, btype = \"%s\""%(boundaryCondition,btype)
    chemicalState = boundaryConditions[boundaryCondition]["chemicalState"]
    lenstringBody = len(stringBody)
    studyFile.write("%s %s, value = %sChemicalState)\n"%(stringBC,stringBody,chemicalState))
    studyFile.write("listOfBoundaryConditions.append(%sBC)\n"%(boundaryCondition))
studyFile.write("#~~~~~~~~~~~~~~~~~~~\n")
studyFile.write("# Expected outputs ~\n")
studyFile.write("#~~~~~~~~~~~~~~~~~~~\n\n")
stringsEx = "expectedOutputs = ["
lenstringsEx = len(stringsEx)
stringFormat = "%s\\\n"
miseenpage = "\\\n"+" "*lenstringsEx+"ExpectedOutput(\"Concentration\",\"%s\", format=\"table\", name=\"%s\"),"
studyFile.write("%s"%(stringsEx))
maxlen = 0
for ex in expectedOutputs:
    maxlen = max(len(ex[0]),maxlen)
maxlen = maxlen+1
for ex in expectedOutputs:
    lenex0 = len(ex[0])
    miseenpage = "\\\n"+" "*lenstringsEx+"ExpectedOutput(\"Concentration\",\"%s\","+" "*(maxlen-lenex0)+"format=\"table\", name=\"%s\"),"
    stringFormat+=miseenpage
    print(ex[0],ex[1],type(ex[0]),type(ex[1]))
    studyFile.write(miseenpage%(str(ex[0]),str(ex[0])))
stringFormat="\\\n"+" "*(lenstringsEx-1)+"]\n"
studyFile.write("%s"%(stringFormat))
studyFile.write("#~~~~~~~~~~~~~~~~~~~~~~~\n")
studyFile.write("# Problem to be solved ~\n")
studyFile.write("#~~~~~~~~~~~~~~~~~~~~~~~\n\n")
problemString = "problem  = ChemicalTransportProblem("
lenPStr = len(problemString)
lenBC = len("speciesBaseAddenda")
stringFormat = "%sname               = \"%s\",\\"+\
                "\n%sregions            = listOfRegions,\\"+\
                "\n%sinitialConditions  = listOfInitialConditions,\\"+\
                "\n%sboundaryConditions = listOfBoundaryConditions,\\"+\
                "\n%sdarcyVelocity      = Velocity([ux,0.0,0.0]),\\"+\
                "\n%schemistryDB        = \"%s\",\\"+\
                "\n%scalculationTimes   = [0,%s],\\"+\
                "\n%sspeciesBaseAddenda = speciesAddenda,\\"+\
                "\n%skineticLaws        = None,\\"+\
                "\n%sactivityLaw        = None,\\"+\
                "\n%soutputs            = expectedOutputs)\n"
studyFile.write(stringFormat%(problemString,studyName," "*lenPStr," "*lenPStr," "*lenPStr," "*lenPStr," "*lenPStr, solvers[2]," "*lenPStr, simulationTime, " "*lenPStr, " "*lenPStr, " "*lenPStr, " "*lenPStr))

#problem  = ChemicalTransportProblem(name                = "piaexp",\
#                                    regions             = [silicateLowRegion, silicateUpRegion, calciteRegion, boundary0Region],\
#                                    initialConditions   = [silicateLowIC, silicateUpIC, calciteIC],\
#                                    boundaryConditions  = [boundaryBC],\
#                                    calculationTimes    = [0.0,temps_final],\
#                                    sources             = None,\
#                                    darcyVelocity       = Velocity([ux,0.0,0.0]),\
#                                    chemistryDB         = "phreeqc.dat",\
#                                    speciesBaseAddenda  = speciesAddenda,\
#                                    kineticLaws         = None,\
#                                    activityLaw         = None,\
#                                    outputs             = expectedOutputs)
studyFile.write("#~~~~~~~~~~\n")
studyFile.write("# solvers ~\n")
studyFile.write("#~~~~~~~~~~\n\n")
studyFile.write("module = ChemicalTransportModule()\n")
studyFile.write("module.setData (problem, unstructured = 1, trace = 0, mesh = %s, algorithm = \"%s\")\n"%("mesh",couplingAlgorithmDic["Algorithm"]))
studyFile.write("module.setComponent(\"%s\",\"%s\")\n"%(solvers[0],solvers[1]))
lenString = len("module.setCouplingParameter(")
string = "\n"+" "*lenString
studyFile.write("module.setCouplingParameter(")
lenKey = 0
for key in couplingAlgorithmDic.keys():
    lenKey = max(lenKey,len(key))
    pass
for key in couplingAlgorithmDic.keys():
    lenk = (lenKey-len(key)+1)*" "
    if key.lower()!="algorithm":
        keyi = key[0].lower()+key[1:]
        studyFile.write("%s%s = %s,\\%s"%(keyi, lenk, couplingAlgorithmDic[key], string))
studyFile.write(")\n")
#module.setCouplingParameter(initialTimeStep        = 30,
#                            maxTimeStep            = 20,
#                            minTimeStep            = 20,
#                            couplingPrecision      = 2.e-2,
#                            optimalIterationNumber = 20,
#                            maxIterationNumber     = 30,
#                            increaTimeStepCoef     = (0.5)**(-0.2),
#                            decreaTimeStepCoef     = 0.5)



studyFile.write("#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
studyFile.write("# transport solver Parameters ~\n")
studyFile.write("#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n")
stringsTP = "module.transport.setTransportParameter("
lenstringsTP = len(stringsTP)
miseenpage = ",\\\n"+" "*lenstringsTP
stringFormat = "%sconvsolver = %s%s"+\
               "iterSolver = %s%s"+\
               "indMemory = 0%s"+\
               "discretisation = dico[\'MethodChoice\']%s"+\
               "algebraicResolution = \"%s\"%s"+\
               "timeSteppingMethod = \"%s\", BDFOrder = %s%s"+\
               "preconditioner = \"%s\", accelerator = \"%s\", thetaScheme = %s)\n"
studyFile.write(stringFormat%(stringsTP, transportSolverParameters[2], miseenpage,
                              transportSolverParameters[1], miseenpage, miseenpage, miseenpage,
                              transportSolverParameters[0], miseenpage, 
                              transportSolverParameters[3], transportSolverParameters[4], miseenpage, 
                              transportSolverParameters[5], transportSolverParameters[6], transportSolverParameters[7]
                      )
               )
studyFile.write("#~~~~~~~~~~~~~\n")
studyFile.write("# Simulation ~\n")
studyFile.write("#~~~~~~~~~~~~~\n\n")
studyFile.write("module.launch()\n")
studyFile.write("while (module.simulatedTime < module.times[-1]):\n")
studyFile.write("    module.oneTimeStep()\n")
studyFile.write("    pass\n")
studyFile.write("#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
studyFile.write("# End of the coupling simulation ~\n")
studyFile.write("#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
studyFile.write("#~~~~~~~~~~~~~~~~~~~~~~~~\n")
studyFile.write("# End of the Simulation ~\n")
studyFile.write("#~~~~~~~~~~~~~~~~~~~~~~~~\n\n")
print("postProcessingTable:")
print(postProcessingTable)
print("postProcessingTable end")
pline = pythonControl(postProcessingTable)
for line in pline:
    studyFile.write("%s\n"%(line))


def _formationReactionIdentification(a):
    string = a[a.index("=")+1:]
    lString = string.split(" + ")
    listOfTuples = "["
    for string in lString:
        listOfTuples+"(\""+string+"\",1)"
    listOfTuples+= "]"
    return listOfTuples
    
