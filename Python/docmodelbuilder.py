from __future__ import absolute_import
from __future__ import print_function
from collections import OrderedDict
from dotextract import *
#from neoutility import Attribute
from getpass import getuser
from types import StringType, BooleanType, ListType
from os import listdir
import re
from six.moves import range
"""

        Dimier Alain (alain.dimier at gmail dot com)
        
"""
global version

version = 1.0

class color:
    """
    to print colors; example : print color.bold+"what you want to print" + color.end
    """
    purple = '\033[95m'
    cyan = '\033[96m'
    darkcyan = '\033[36m'
    blue = '\033[94m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    bold = '\033[1m'
    underline = '\033[4m'
    end = '\033[0m'
    
    
class elementOfDoc():
    """
    class representing an element of the global document dictionary
    """
    def __init__(self,documentName, structure, group, author,phoneNumber,summary,projectId = None):
        self.documentName       = documentName
        self.structure          = structure
        self.group              = group
        self.author             = author
        self.phoneNumber        = phoneNumber
        self.summary            = summary
        self.projectId          = projectId
        
    def printer(self):
    
        print(color.bold+"name of the document: " + color.end,self.documentName)
        print(color.bold+"name of the structure: " + color.end,self.structure)
        print(color.bold+"name of the group: " + color.end,self.group)
        print(color.bold+"name of the author: " + color.end,self.author)
        print(color.bold+"associated phone number: " + color.end,self.phoneNumber)
        print(color.bold+"summary: " + color.end,self.summary)
        print(color.bold+"projectId: " + color.end,self.projectId)

def firstOccurence(whereToSearch, stringTofind):
    ind = 0
    stringTofind = stringTofind.lower()
    while ind < len(whereToSearch) and stringTofind not in whereToSearch[ind].lower():
        #print ind,stringTofind,whereToSearch[ind].lower()
        ind+=1
    print("ind ",ind)
    if ind==len(whereToSearch):
       print("No "+stringTofind+" present in the Document")
       return None
    else:
        return whereToSearch[ind]

def indOfFirstOccurence(whereToSearch, stringTofind, top = None):
    """
    from the top, if top == None; otherwise from the end 
    """
    stringTofind = stringTofind.lower()
    if top == None:
        ind = 0
        while ind < len(whereToSearch) and stringTofind not in whereToSearch[ind].lower():
        #print ind,stringTofind,whereToSearch[ind].lower()
            ind+=1
        if ind==len(whereToSearch):
           print("No "+stringTofind+" present in the Document")
           return None
        else:
            return ind
        pass
    else:
        listLength = len(whereToSearch)
        ind = listLength-1
        while ind >= 0 and stringTofind not in whereToSearch[ind].lower():
            ind+=-1
        if ind==-1:
           print("No "+stringTofind+" present in the Document")
           return None
        else:
            return ind

def cityBuilder(entityToBuild):
    """
    It enables to build the programming structures necessary to setup a simulation.
    """
    name = entityToBuild.name
    moduleName = name.lower()+"_city.py"
    if moduleName not in listdir("./"):
        #raw_input(moduleName)
        moduleFile = open(moduleName,"w")
        moduleFile.write("#!/usr/bin/env python\n")
        moduleFile.write("# -*- coding: UTF-8 -*-\n")
        moduleFile.write("#c\"it's marvellous, it's  ...!\"\n")
        moduleFile.write("#\n")
        moduleFile.write("# Module automatically created from a specification file; projection version %s\"\n"%(version))
        moduleFile.write("#\n")
        moduleFile.write("from neoutility import Attribute, BasicEntity, CompoundEntity, Rule\n")
        moduleFile.write("#\n")
        moduleFile.write("attributesList = []\n")
        moduleFile.write("#\n")
        for attribute in entityToBuild.attributes:
            print(attribute.name.lower(),attribute.name,attribute.atype,attribute.init,attribute.var)
            print(str(attribute.unit))
            if attribute.atype != StringType and attribute.atype != "String":
                format = "%s = Attribute(name = \"%s\",atype = \"%s\",init = %s, var = %s, "
                pass
            else:
                format = "%s = Attribute(name = \"%s\",atype = \"%s\",init = \"%s\", var = %s, "
                pass
            if attribute.unit == "None":
                format+="unit = %s);attributesList.append(%s)\n"
            else:
                format+="unit = \"%s\");attributesList.append(%s)\n"
            moduleFile.write(format\
                             %(attribute.name,attribute.name,
                               attribute.atype,
                               attribute.init,
                               _trbool(attribute.var),
                               str(attribute.unit),
                               attribute.name
                             ))        
        #    moduleFile.write("attributesList.append(%s)\n"%(attribute.name.lower()))
        #
        moduleFile.write("#\n")
        moduleFile.write("#\n")
        if (entityToBuild.__class__.__name__ == "PrimEntity"):
            moduleFile.write("class %s(BasicEntity):\n"%(name))
            moduleFile.write("    \"\"\"\n")
            moduleFile.write("    %s\n"%(entityToBuild.description))
            moduleFile.write("    \"\"\"\n")
            moduleFile.write("#\n")
            moduleFile.write("    def __init__(self, name, attributesList, rulesList, description = None, structure = None):\n")
            moduleFile.write("        BasicEntity.__init__(self,name, attributesList, rulesList, description)\n")
            moduleFile.write("        if description == None:\n")
            moduleFile.write("            self.description = \"defining the "+name+" type\"\n")
            moduleFile.write("            pass\n")
            moduleFile.write("        else:\n")
            moduleFile.write("            self.description = description\n")
            moduleFile.write("        self.attributesList = attributesList\n")
            moduleFile.write("        pass\n")
            ind = 0
            for attribute in entityToBuild.attributes:
                moduleFile.write("        self.%s = attributesList[%i] \n"%(attribute.name,ind))
                ind+=1
            moduleFile.write("#\n")
            moduleFile.flush()
            pass
        elif (entityToBuild.__class__.__name__ == "CumEntity"):
            moduleFile.write("class %s(CompoundEntity):\n"%(name))
            moduleFile.write("    \"\"\"\n")
            moduleFile.write("    %s\n"%(entityToBuild.description))
            moduleFile.write("    \"\"\"\n")
            moduleFile.write("#\n")
            moduleFile.write("    def __init__(self, name, attributesList, rulesList, container, environment = None, description = None, structure = None):\n")
            moduleFile.write("        CompoundEntity.__init__(self,name, attributesList, rulesList, description)\n")
            moduleFile.write("        if description == None:\n")
            moduleFile.write("            self.description = \"defining the "+name+" type\"\n")
            moduleFile.write("            pass\n")
            moduleFile.write("        else:\n")
            moduleFile.write("            self.description = description\n")
            moduleFile.write("            pass\n")
            ind = 0
            for attribute in entityToBuild.attributes:
                moduleFile.write("        self.%s = attributesList[%i] \n"%(attribute.name,ind))
                ind+=1
            moduleFile.write("#\n"*3)
            moduleFile.write("        self.container = container\n")
            moduleFile.write("#\n")
            moduleFile.flush()
            pass
    else:
        raise Warning(color.red+"Chek the list of modules already available\n         You try to create a module whose name already exists"+color.end)

    for rule in entityToBuild.rules:
        #print " rule name ",rule[0]
        #raw_input(" name of the rule")
        core = rule[1].replace("\n","\\\n")
        #print "~~\n%s\n~~\n"%core
        #raw_input("core of the rule")
        moduleFile.write("%sCore = \"\\\n"%(rule[0]))
        moduleFile.write("%s\" \n#"%(core))
        moduleFile.write("\n%s = Rule(name = \"%s\", core = %sCore, description = \"%s\")\n"%(rule[0],rule[0],rule[0],rule[2]))
        pass
    moduleFile.close()
#        
#getRequiredTemperatureCore = "EntityRefType ent(this);\n\
#std::cout << \"required temperature of the building: \"\
#          << \", \" <<  this->getDirectRequiredTemperature() << \" degree Celcius for : \" <<  \
#          ent -> getName()<<std::endl;\
#\
#\
#"
#getRequiredTemperature = Rule(name = "getRequiredTemperature", core = getRequiredTemperatureCore, description = " building Required Temperature")
#buildingRulesList.append(getRequiredTemperature)
#


def pyCityBuilder(entityToBuild):
    """
    It enables to build the programming structures necessary to setup a simulation.
    """
    name = entityToBuild.name
    moduleName = name.lower()+"_city.py"
    if moduleName not in listdir("./"):
        #raw_input(moduleName)
        moduleFile = open(moduleName,"w")
        moduleFile.write("#!/usr/bin/env python\n")
        moduleFile.write("# -*- coding: UTF-8 -*-\n")
        moduleFile.write("#c\"est pas beau ca!\"\n")
        moduleFile.write("#\n")
        moduleFile.write("# Module automatically created using a specification file; projection version %s\"\n"%(version))
        moduleFile.write("#\n")
        moduleFile.write("from neoutility import Attribute, BasicEntity, CompoundEntity, Rule\n")
        moduleFile.write("#\n")
        moduleFile.write("attributesList = []\n")
        moduleFile.write("#\n")
        moduleFile.write("rulesList = []\n")
        moduleFile.write("#\n")
        for attribute in entityToBuild.attributes:
            print(attribute.name.lower(),attribute.name,attribute.atype,attribute.init,attribute.var)
            print(str(attribute.unit))
            if attribute.atype != StringType and attribute.atype != "String":
                format = "%s = Attribute(name = \"%s\",atype = \"%s\",init = %s, var = %s, "
                pass
            else:
                format = "%s = Attribute(name = \"%s\",atype = \"%s\",init = \"%s\", var = %s, "
                pass
            if attribute.unit == "None":
                format+="unit = %s);attributesList.append(%s)\n"
            else:
                format+="unit = \"%s\");attributesList.append(%s)\n"
            moduleFile.write(format\
                             %(attribute.name,attribute.name,
                               attribute.atype,
                               attribute.init,
                               _trbool(attribute.var),
                               str(attribute.unit),
                               attribute.name
                             ))        
        #    moduleFile.write("attributesList.append(%s)\n"%(attribute.name.lower()))
        #
        moduleFile.write("#\n")
        moduleFile.write("#\n")
        if (entityToBuild.__class__.__name__ == "PrimEntity"):
            moduleFile.write("class %s(BasicEntity):\n"%(name))
            moduleFile.write("    \"\"\"\n")
            moduleFile.write("    %s\n"%(entityToBuild.description))
            moduleFile.write("    \"\"\"\n")
            moduleFile.write("#\n")
            moduleFile.write("    def __init__(self, name, attributesList, rulesList, description = None, structure = None):\n#\n")
            
            moduleFile.write("        self.name = name\n")
            moduleFile.write("        self.rulesList = rulesList\n\n")
            moduleFile.write("        self.structure = structure\n\n")
            moduleFile.write("        if description == None:\n")
            moduleFile.write("            self.description = \"defining the "+name+" type\"\n")
            moduleFile.write("            pass\n")
            moduleFile.write("        else:\n")
            moduleFile.write("            self.description = description\n")
            moduleFile.write("            pass\n")
            moduleFile.write("        self.attributesList = attributesList\n\n")
            ind = 0
            for attribute in entityToBuild.attributes:
                moduleFile.write("        self.%s = attributesList[%i] \n"%(attribute.name,ind))
                ind+=1
            moduleFile.write("#\n")
            moduleFile.flush()
            pass
        elif (entityToBuild.__class__.__name__ == "CumEntity"):
            moduleFile.write("class %s(CompoundEntity):\n"%(name))
            moduleFile.write("    \"\"\"\n")
            moduleFile.write("    %s\n"%(entityToBuild.description))
            #moduleFile.write("\n    %s\n"%(entityToBuild.author))
            moduleFile.write("    \"\"\"\n")
            moduleFile.write("#\n")
            moduleFile.write("    def __init__(self, name, attributesList, rulesList, container, environment = None, description = None, structure = None):\n#\n")
            moduleFile.write("        BasicEntity.__init__(self,name, attributesList, rulesList, description)\n#\n")
            moduleFile.write("#\n# Atributes\n#\n")
            ind = 0
            for attribute in entityToBuild.attributes:
                moduleFile.write("        self.%s = attributesList[%i] \n"%(attribute.name,ind))
                ind+=1
            moduleFile.write("#\n# Container\n#\n")
            moduleFile.write("        self.container = container\n")
            moduleFile.write("#\n# Environment\n#\n")
            moduleFile.write("        self.environment = environment\n")
            moduleFile.write("#\n")
            moduleFile.flush()
            pass
    else:
        raise Warning(color.red+"Chek the list of modules already available\n         You try to create a module whose name already exists"+color.end)
    #
    # we build the python functions
    #
    for rule in entityToBuild.rules:
        print(" rule name ",rule[0])
        #raw_input(" name of the rule")
        core = coreControl(rule[1])
        #if "\\\n" in rule[1]:
        #    core = rule[1].replace("\\\n","\\\n        ")
        #else:
        #    core = rule[1]
        #core = rule[1].replace("\n","\\\n")
        print(core)
        #raw_input("core of the rule")
        if len(rule[3]) == 0:
            moduleFile.write("    def %s(self):\n"%(rule[0]))
        else:
            attributesString = ""
            for att in rule[3]:
                attributesString+=","+str(att)
            moduleFile.write("    def %s(self%s):\n"%(rule[0],attributesString))
        moduleFile.write("        \"\"\"\n")
        moduleFile.write("        %s\n"%(rule[2]))
        moduleFile.write("        \"\"\"\n")
        #moduleFile.write("        %s \n#\n"%(core[0:].replace("\n","    \n")))
        for line in core:
            moduleFile.write("%s\n"%(line))
        moduleFile.write("#\n"*3)
        #moduleFile.write("        %s \n#\n"%(core[0:].replace("\n","    \n").replace("\\","\n")))
        #moduleFile.write("        %s \n#\n"%(core[0:]))
        #moduleFile.write("\n%s = Rule(name = \"%s\", core = %sCore, description = \"%s\")\n"%(rule[0],rule[0],rule[0],rule[2]))
        pass
    moduleFile.close()

def modelToBuild(path):
    """
    function enabling the generation of an elementary brick of a model
    """
    elementaryModel = get_doc_text(path)
    try:
        if ("class:" in elementaryModel):
            classToHandle = elementaryModel.index("class:") + 1
        pass
    except TypeError:
        print(color.bold+"the function you use doesn\'t apply to that document : " + color.end)

    """
    The document is supposed to have a header to name the entity   
    """
    modelDefinition = elementaryModel[indOfFirstOccurence(elementaryModel, "Model Definition",1):]
    #print modelDefinition
    print(color.bold+"modelDefinition"+ color.end)
    entityNameIndex = indOfFirstOccurence(modelDefinition, "Name")
    studyName = modelDefinition[entityNameIndex+1]
    simulationTime = 100.
    print(" entity name ",studyName)
    studyName = studyName[0].upper()+studyName[1:]
    """
    The document is supposed to have a table to describe the mesh   
    """
    meshLayerIndex = indOfFirstOccurence(modelDefinition, "meshLayer")
    endIndex = indOfFirstOccurence(modelDefinition, "ChemistrySolver:", 1)
    meshTable = modelDefinition[meshLayerIndex+2:endIndex] # 2 because of the comment introduced.
    #
    # We setup a list of layers to handle the file
    #
    listOfLayers = {}
    chemistrySolverIndex = indOfFirstOccurence(modelDefinition, "ChemistrySolver:", 1)
    chemistrySolverName = modelDefinition[indOfFirstOccurence(modelDefinition, "Chemistry Solver:", 1)+1]
    chemistryDatabaseIndexb = indOfFirstOccurence(modelDefinition, "ChemistryDatabase:", 1)
    chemistryDatabaseIndexe = indOfFirstOccurence(modelDefinition, "Materiallayers description", 1)
    print(chemistryDatabaseIndexb)
    print(chemistryDatabaseIndexb)
    chemistryDatabaseIndex = modelDefinition[chemistryDatabaseIndexb:chemistryDatabaseIndexe].index("database")
    chemistryDatabaseName = modelDefinition[chemistryDatabaseIndexb:chemistryDatabaseIndexe][chemistryDatabaseIndex+1]
    temTable = modelDefinition[meshLayerIndex+2:chemistrySolverIndex]
    print(color.bold+"temTable: "+color.end)
    print(temTable)
    print(color.bold+"temTable end "+color.end)
    indTable = 5
    while indTable <len(temTable):
        listOfLayers[temTable[indTable]] = temTable[indTable+1]
        indTable+=5
    print(listOfLayers)
    #raw_input("listOfLayers")     
    
    """
    The document is supposed to have some python constants   
    """
    pythonIndex = indOfFirstOccurence(modelDefinition, "Python Addendum:", 1)+1
    pythonEndIndex = indOfFirstOccurence(modelDefinition, "meshlayers", 1)
    #print modelDefinition[pythonIndex:pythonEndIndex]
    pythonConstants = modelDefinition[pythonIndex:pythonEndIndex]
   
    #raw_input()
    #print " meshTable ",meshTable
    """
    The document is supposed to have a table to describe the different material associated to the mesh   
    """
    #materialsIndex = indOfFirstOccurence(modelDefinition, "Materiallayers description")
    debIndex = indOfFirstOccurence(modelDefinition, "Materiallayers description")+2
    endIndex = indOfFirstOccurence(modelDefinition, "AqueousMasterSpecies", 1)
    materialTable = modelDefinition[debIndex:endIndex] # 2 because of the comment introduced.
    print("material table \n")
    print(materialTable)
    """
    The document is supposed to have a table to describe the different aqueous master species it entails  
    """
    #aqueousMasterSpeciesIndex = indOfFirstOccurence(modelDefinition, "AqueousMasterSpecies Definition")
    #endIndex = indOfFirstOccurence(modelDefinition, "SecondarySpecies Definition", 1)


    debIndex = indOfFirstOccurence(modelDefinition, "AqueousMasterSpecies Definition")+2
    endIndex = indOfFirstOccurence(modelDefinition, "SecondarySpecies Definition", 1)
    aqueousMasterSpeciesTable = modelDefinition[debIndex:endIndex] # 2 because of the comment introduced.
    print(color.bold+"aqueousMasterSpecies table \n"+ color.end)
    print(aqueousMasterSpeciesTable)
    """
    The document is supposed to have a table to describe the different secondary species it entails  
    """
    #secondarySpeciesIndex = indOfFirstOccurence(modelDefinition, "SecondarySpecies Definition")
    #endIndex = indOfFirstOccurence(modelDefinition, "MineralSpecies Definition", 1)
    
    
    debIndex = indOfFirstOccurence(modelDefinition, "SecondarySpecies Definition")+2
    endIndex = indOfFirstOccurence(modelDefinition, "MineralSpecies Definition", 1)
    secondarySpeciesTable = modelDefinition[debIndex:endIndex] # 2 because of the comment introduced.
    print(color.bold+"secondarySpecies table \n"+ color.end)
    print(secondarySpeciesTable)
    """
    The document is supposed to have a table to describe the different mineral secondary species it entails  
    """
    #mineralSecondarySpeciesIndex = indOfFirstOccurence(modelDefinition, "MineralSpecies Definition")
    #chemicalStatesIndex = indOfFirstOccurence(modelDefinition, "ChemicalStates Definition", 1)
    
    debIndex = indOfFirstOccurence(modelDefinition, "MineralSpecies Definition",1)+2
    endIndex = indOfFirstOccurence(modelDefinition, "ChemicalStates Definition",1)
    mineralSecondarySpeciesTable = modelDefinition[debIndex:endIndex] # 2 because of the comment introduced.
    print(color.bold+"mineralSecondarySpeciesTable table \n"+ color.end)
    print(mineralSecondarySpeciesTable)
    """
    The document is supposed to have a table to describe the different chemical states it entails  
    """
    #chemicalStatesIndex = indOfFirstOccurence(modelDefinition, "ChemicalStates Definition")
    #initialConditionIndex = indOfFirstOccurence(modelDefinition, "Initial Conditions", 1)
    
    
    debIndex = indOfFirstOccurence(modelDefinition, "ChemicalStates Definition",1)+1
    endIndex = indOfFirstOccurence(modelDefinition, "Initial Conditions",1)
    chemicalStateTable = modelDefinition[debIndex:endIndex]
    print(color.bold+"chemical states table \n"+ color.end)
    print(chemicalStateTable)
    #
    # Taking a list, we analyse it to build a dictionary
    # the keys are the states names
    #
    chemicalStatesTable = chemicalStatesAnalysis(chemicalStateTable)
    """
    The document is supposed to have a table to setup initial conditions  
    """
    #initialConditionIndex = indOfFirstOccurence(modelDefinition, "Initial Conditions", 1)
    #boundaryConditionIndex = indOfFirstOccurence(modelDefinition, "Boundary Conditions",1)
    
    
    debIndex = indOfFirstOccurence(modelDefinition, "Initial Conditions",1)+1
    endIndex = indOfFirstOccurence(modelDefinition, "Boundary Conditions",1)
    #
    initialConditionTable = modelDefinition[debIndex:endIndex]
    initialConditionsTable = initialConditionAnalysis(initialConditionTable, chemicalStatesTable, listOfLayers)
    """
    The document is supposed to have a table to setup boundary conditions  
    """
    #boundaryConditionIndex = indOfFirstOccurence(modelDefinition, "Boundary Conditions",1)
    #endIndex = indOfFirstOccurence(modelDefinition, "TransportSolver", 1)
    
    debIndex = indOfFirstOccurence(modelDefinition, "Boundary Conditions",1)+1
    endIndex = indOfFirstOccurence(modelDefinition, "TransportSolver",1)
    #
    boundaryConditionTable = modelDefinition[debIndex:endIndex]
    boundaryConditionTable = boundaryConditionAnalysis(boundaryConditionTable, chemicalStatesTable)
    """
    The document is supposed to have a table to give the transport solver name  
    """
    debIndex = endIndex
    endIndex = indOfFirstOccurence(modelDefinition, "SolverParameters",1)
    solverTable = modelDefinition[debIndex:endIndex]
    transportSolverName = solverTable[solverTable.index("Solver name:")+1]
    """
    The document is supposed to have a table to give the transport solver parameters  
    """
    debIndex = endIndex
    endIndex = indOfFirstOccurence(modelDefinition, "Coupling algorithm and coupling parameters",1)
    solverParameterTable = modelDefinition[debIndex:endIndex]
    transportSolverParameters = tansportSolverParameterAnalysis(solverParameterTable)
    """
    The document is supposed to have a table to give the coupling algorithm parameters  
    """
    debIndex = endIndex
    endIndex = indOfFirstOccurence(modelDefinition, "SimulationTime:",1)
    couplingAlgorithmParameters = modelDefinition[debIndex:endIndex]
    print(couplingAlgorithmParameters)
    couplingAlgorithmDic = couplingAlgorithmAnalysis(couplingAlgorithmParameters)
    #raw_input("couplingAlgorithmParameters")
    """
    The document is supposed to have a table to give the simulation time  
    """
    debIndex = endIndex
    endIndex = indOfFirstOccurence(modelDefinition, "Expectedoutputs",1)
    simulationTime = modelDefinition[debIndex+1]
    #print color.bold+" simulation time"+color.end,simulationTime
    #raw_input()
    """
    The document is supposed to have a table to give the expected outputs from the simulation  
    """
    debIndex = endIndex
    endIndex = indOfFirstOccurence(modelDefinition, "End Of Model",1)
    expectedOutputsTable = modelDefinition[debIndex:endIndex]
    print(expectedOutputsTable)
    #raw_input("expectedOutputsTable")
    expectedOutputs = expectedOutputsAnalysis(expectedOutputsTable)
    """
    Eventually a scrypt can be introduced for post-processing  
    """
    debIndex = indOfFirstOccurence(modelDefinition, "Postprocessing",1)
    endIndex = indOfFirstOccurence(modelDefinition, "End",1)
    postProcessingTable = modelDefinition[debIndex+1:endIndex]
    
    print(postProcessingTable)
    #raw_input()
    
    """
    The document is supposed to have a pararagraph to document the class to be built.
    that paragraph is name description
    """
    classDescription = modelDefinition[indOfFirstOccurence(modelDefinition, "Description")+1]
    classDescription = _descriptionStringControl(classDescription)

    print(color.bold+"name of the entity: "+ color.end,studyName)
    """
    The document is supposed to have a table made of a list of attributes.   
    """
    return studyName,\
           meshTable,\
           materialTable,\
           aqueousMasterSpeciesTable,\
           secondarySpeciesTable,\
           mineralSecondarySpeciesTable,\
           chemicalStatesTable,\
           initialConditionsTable,\
           boundaryConditionTable,\
           [transportSolverName, chemistrySolverName, chemistryDatabaseName],\
           transportSolverParameters,\
           expectedOutputs,\
           pythonConstants,\
           simulationTime,\
           couplingAlgorithmDic,\
           postProcessingTable

def _trbool(var):
    """
    the way to write a boolean with a string as input
    """
    if type(var) == StringType:
        if var.lower() in ["yes","oui","ja","true"]:
            var = "True"
            pass
        else:
            var = "False"
        pass
    elif type(var) == BooleanType:
        if var == False:
            var = "False"
        else:
            var = "True"
        pass
    else:
        var = "False"
    return var

def databaseToBuild(path):
    """
    function returning an element of a dictionary to build it, to amend or enrich it
    """
    material = get_docx_text(path)
    if ("Inhaltsverzeichnis" in material):
        indexToHanldTheList = material.index("Inhaltsverzeichnis") +1
        pass
    elif ("Table of Contents" in material):
        indexToHanldTheList = material.index("Table of Contents") +1
        pass
    else:
        indexToHanldTheList = len(material)

    material = material[0:indexToHanldTheList]
    #
    structure = material[0]
    group = material[1]
    address = material[2]+ " "+material[3]
    phoneNumber = material[4].replace("Tel :","")
    """
    Summary is supposed to be present; we take the first occurence of it.
    
    """
    summary = firstOccurence(material, "summary")
    """
    Author is supposed to be present; we take the first occurence of it.
    
    """
    author = firstOccurence(material, "author")
    """
    project number is supposed to be present; we take the first occurence of it.
    
    """
    projectId = firstOccurence(material, "project")
    
    return elementOfDoc(path, structure,group,author,phoneNumber,summary,projectId)
    
def _descriptionStringControl(stringToBeControlled):
    controlledString = re.sub(u"(\u2018|\u2019|'|\")", "\'",stringToBeControlled)
    return controlledString
    
def coreControl(core):
    """
    core should be a string.
    """
    
    b = core.split("\n")

    for ind in range(len(b)):
        line = b[ind]
        deb = 0
        ws = 0
        if len(line) > 0:
            while line[ws] == " ":
                ws+=1
        b[ind] = re.sub(u"(\u201d|\u2018|\u2019|'|\")", "\"",line[ws:])
    dec = 8
    for ind in range(len(b)):
        line = b[ind]
        b[ind] = " "*dec+b[ind]
        if "pass" in line and dec>=12:
            dec+=-4
        elif "if" in line or "for" in line or "while" in line:
            dec+=+4
       # b[ind] = " "*dec+b[ind]
    return b
    
def pythonControl(core):
    """
    core should be a string.
    """
    if type(core) == StringType:
        b = core.split("\n")
        pass
    elif type(core) == ListType:
        b = []
        lineToFeed = ""
        ind = 0
        for line in core:
            line = str(line)
            print(ind,line[0])
            if "\r" in line or "\\" or "\n" in line:
                if "="==line[0]:
                    print("dbg line0",line[0])
                    print("dbg line0",b[-1])
                    b[-1] = b[-1]+line
                    lineToFeed=""
                    pass
                else:
                    lineToFeed+=line
                    b.append(lineToFeed)
                    lineToFeed=""
                    pass
            else:
                lineToFeed+=line
                lineToFeed=""
                pass
            ind+=1
            pass
    b = quoteAnalysis(b)
    for ind in range(len(b)):
        line = b[ind]
        deb = 0
        ws = 0
        if len(line) > 0:
            while line[ws] == " ":
                ws+=1
        b[ind] = re.sub(u"(\u201d|\u2018|\u2019|'|\")", "\"",line[ws:])
    dec = 0
    for ind in range(len(b)):
        line = b[ind]
        b[ind] = " "*dec+b[ind]
        if "pass" in line and dec>=4:
            dec+=-4
        elif "if" in line or "for" in line or "while" in line:
            dec+=+4
       # b[ind] = " "*dec+b[ind]
    return b

def chemicalStatesAnalysis(listOfChemicalStates):
    
    """
    analysis of the chemical state table
    """
    print("listOfChemicalStates: ", listOfChemicalStates)
    print("length of listOfChemicalStates: ",len(listOfChemicalStates))
    statesName  =[]
    chemicalStatesTable = {}
    ind = 0
    for en in  listOfChemicalStates:
        if en.lower()=="chemical state name":
            statesName.append([ind+1,listOfChemicalStates[ind+1]])
            #print color.red+"statesName "+color.end,statesName
        ind+=1
    for state in range(len(statesName)-1):
        statesName[state].insert(1,statesName[state+1][0]-1)
    statesName[-1].insert(1,len(listOfChemicalStates)-1)
    print(statesName)
    #print color.red+statesName+color.end
    for state in statesName:
        print(color.red+" state: "+color.end,listOfChemicalStates[state[0]:state[1]])
    #raw_input(" states")
    ind = statesName[0][0]
    for state in statesName:
        ind = state[0]
        chemicalStatesTable[state[2]] = {}
        listToHandle = listOfChemicalStates[state[0]:state[1]]
        print(color.red+"listToHandle: "+color.end, listToHandle)
        print("ind: ", ind+2, ind+4,listOfChemicalStates[ind+2],listOfChemicalStates[ind+4])
        el = chemicalStatesTable[state[2]]
        el["pH"] = listOfChemicalStates[ind+2]
        el["pe"] = listOfChemicalStates[ind+4]
        indTemp = ind+6
        el["T"] = listOfChemicalStates[indTemp]
        el["species"] = []
        el["mineralSpecies"] = []
        print("el: ",el)
        indTemp+= 3
        print("indTemp",indTemp,len(listOfChemicalStates), end=' ')
        while  listOfChemicalStates[indTemp+1] != "Mineral species" and indTemp<state[1]:
            el["species"].append((listOfChemicalStates[indTemp+1],listOfChemicalStates[indTemp+2],listOfChemicalStates[indTemp+3]))
            indTemp+=3
            print("debug ",indTemp)
        print(color.cyan+"chemicalStatesTable: "+color.end,chemicalStatesTable)
        mineralspeciesIndex = listOfChemicalStates.index("Mineral species",state[0],state[1])
        indMS = mineralspeciesIndex+3
        #print color.bold+" ChemicalStates tables "+state[2]+" : "+color.end,chemicalStatesTable[state[2]]
        while indMS < state[1]-1:
            print("indMS", listOfChemicalStates[indMS+1])
            print("indMS", listOfChemicalStates[indMS+2])
            print("indMS", listOfChemicalStates[indMS+3])
            print("indMS", listOfChemicalStates[indMS+4])
            el["mineralSpecies"].append([listOfChemicalStates[indMS+1],listOfChemicalStates[indMS+2],listOfChemicalStates[indMS+3],listOfChemicalStates[indMS+4]])
            indMS+=4
        print(color.bold+" ChemicalStates tables "+state[2]+" : "+color.end,chemicalStatesTable[state[2]])
        print(color.bold+" end of ChemicalStates tables "+state[2]+" : "+color.end)
        ind = indMS+1
    print(chemicalStatesTable)
    return chemicalStatesTable

def initialConditionAnalysis(listOfInitialConditions, chemicalStatesTable, listOfLayers):
    """
    analysis of the initial condition table
    We have a list of Id's or names linked to chemical states names
    We check that chemical states names are available.
    """
    lengthOfValue = 0
    print(listOfLayers)
    listOfChemicalStates = []
    for state in chemicalStatesTable.keys():
        listOfChemicalStates.append(state.lower())
    indexOfLayers = listOfInitialConditions.index("layerName or layerId")+2
    if len(list(listOfLayers.keys()))!=(len(listOfInitialConditions)-2)/2: # listOfLayers is a dict of layer indices and names
        raise Warning(" there is a number of layers mismatch;\ncheck the number of layers\nand the table of initial conditions")
    ind = 0
    initialConditionsTable = {}
    print("list Of Initial Conditions: ", listOfInitialConditions[indexOfLayers:])
    print("listOfChemicalStates: ",listOfChemicalStates)
    for en in listOfInitialConditions[indexOfLayers:]:
        #print " analysis of en ",en,", ind: ",ind
        if ind%2 == 0:
            #print "listOfInitialConditions[indexOfLayers+ind+1] :",listOfInitialConditions[indexOfLayers+ind+1]
            if listOfInitialConditions[indexOfLayers+ind+1].lower() in listOfChemicalStates and en in list(listOfLayers.keys()):
                #print "ok",en,listOfInitialConditions[indexOfLayers+ind+1]
                keyToIntroduce = listOfLayers[en]
                #print "keyToIntroduce : ",keyToIntroduce
                initialConditionsTable[keyToIntroduce] = listOfInitialConditions[indexOfLayers+ind+1]
            else:
                #print " debug: ",listOfInitialConditions[indexOfLayers+ind+1],en
                pass
            pass
        else:
            pass
        ind+=1
        pass
    print("initialConditionsTable ",initialConditionsTable)
    #raw_input()
    return initialConditionsTable

def expectedOutputsAnalysis(table):
    """
    we analyse the table linked to the expected outputs
    """
    expectedOutputs = []
    debAnalyse =  table.index("Expected output names:")
    if len(table[debAnalyse:]) >=2:
        ind = debAnalyse+2
        while ind+2<=len(table):
            expectedOutputs.append([table[ind], table[ind+1]])
            ind+=2
        
    return expectedOutputs

    
def tansportSolverParameterAnalysis(solverParameterTable): 
    """
    we analyse the table linked to the transport solver parameters
    """
    transportSolverParameter = []
    algebraicResolution = solverParameterTable[solverParameterTable.index("algebraic resolution")+1]
    transportSolverParameter.append(algebraicResolution)
    numberOfIterations = solverParameterTable[solverParameterTable.index("itersolver")+1]
    transportSolverParameter.append(numberOfIterations)
    convergenceLimit = solverParameterTable[solverParameterTable.index("convSolver")+1]
    transportSolverParameter.append(convergenceLimit)
    timeStepMethodName = solverParameterTable[solverParameterTable.index("time stepping method")+1]
    transportSolverParameter.append(timeStepMethodName)
    timeStepMethodParam = solverParameterTable[solverParameterTable.index("time stepping method")+2]
    transportSolverParameter.append(timeStepMethodParam)
    preconditionner = solverParameterTable[solverParameterTable.index("preconditionner")+1]
    transportSolverParameter.append(preconditionner)
    accelerator = solverParameterTable[solverParameterTable.index("accelerator")+1]
    transportSolverParameter.append(accelerator)
    thetaScheme = solverParameterTable[solverParameterTable.index("theta scheme")+1]
    transportSolverParameter.append(thetaScheme)
    return transportSolverParameter

       
def boundaryConditionAnalysis(boundaryConditionsTable, chemicalStatesTable):
    """
    Analysis of the boundary condition table
    for the moment, dealing in 1D, we have only one boundary condition.
    We deliver a dictionnary with a boundary type and a chemical state name
    """
    boundaryConditionTable = {}
    bcType = boundaryConditionsTable[4]
    chemicalState = boundaryConditionsTable[5]
    boundaryConditionTable[boundaryConditionsTable[3]] = {"bcType":bcType,"chemicalState":chemicalState}
    #print boundaryConditionTable
    #raw_input("boundaryConditionTable")
    return boundaryConditionTable
    
def couplingAlgorithmAnalysis(couplingAlgorithmTable):
    couplingAlgorithmDic = OrderedDict()
    couplingAlgorithmDic["Algorithm"] = couplingAlgorithmTable[couplingAlgorithmTable.index("Algorithm:")+1]
    couplingAlgorithmDic["InitialTimeStep"] = couplingAlgorithmTable[couplingAlgorithmTable.index("InitialTimeStep:")+1]
    couplingAlgorithmDic["MinTimeStep"] = couplingAlgorithmTable[couplingAlgorithmTable.index("MinTimeStep:")+1]
    couplingAlgorithmDic["MaxTimeStep"] = couplingAlgorithmTable[couplingAlgorithmTable.index("MaxTimeStep:")+1]
    couplingAlgorithmDic["CouplingPrecision"] = couplingAlgorithmTable[couplingAlgorithmTable.index("CouplingPrecision:")+1]
    couplingAlgorithmDic["OptimalIterationNumber"] = couplingAlgorithmTable[couplingAlgorithmTable.index("OptimalIterationNumber:")+1]
    couplingAlgorithmDic["MaxIterationNumber"] = couplingAlgorithmTable[couplingAlgorithmTable.index("MaxIterationNumber:")+1]
    couplingAlgorithmDic["IncreaTimeStepCoef"] = couplingAlgorithmTable[couplingAlgorithmTable.index("IncreaTimeStepCoef:")+1]
    couplingAlgorithmDic["DecreaTimeStepCoef"] = couplingAlgorithmTable[couplingAlgorithmTable.index("DecreaTimeStepCoef:")+1]
    return couplingAlgorithmDic
    
def quoteAnalysis(bliste):
    """
    two quotes have to be found on a same python code line
    """
    rliste = []
    lastline = ""
    for line in bliste:
        rline = line
        if "\"" in line:
            nc = line.count("\"")
            if nc%2 == 0:
                pass
            elif "\"" in lastline:
                line = lastline+line
                lastline = ""
            else:
                lastline = line
                line = ""
        if line =="":
            pass    
        else:
            rliste.append(line)
    return rliste
