"""
file to read the data linked to the analysis of the heat transfer between the well and the underground
"""
from __future__ import absolute_import
from __future__ import print_function
from os import environ, system
from six.moves import input

from re import split as resplit

def wellBoreDataLineAnalysis(line):
    line = line.replace("\t"," ")
    #lineList = line.split(" ")
    lineList = resplit("=| ",line)
    lineList = [a for a in lineList if a != ""]
    #print (lineList)
    if ("Real" in lineList) and ("!" in lineList):
        pythonString = lineList[0]+" = "+lineList[2].split("!")[0]
        #print ("dbg wellbore int",pythonString)
        #print ("dbg wellbore lineList[0]",lineList[0])
        #print ("dbg wellbore lineList[2]",lineList[2].split("!")[0])
        #raw_input()
        return pythonString,lineList[0],lineList[2].split("!")[0], "Real",lineList[4].replace("\n","")
    elif "Real" in lineList:
        pythonString = lineList[0]+" = "+lineList[2]
        #print ("dbg wellbore int",pythonString)
        #print ("dbg wellbore lineList[0]",lineList[0])
        #print ("dbg wellbore lineList[2]",lineList[2].split("!")[0])
        return pythonString,lineList[0],lineList[2].split("!")[0], "Real","! Int. coef"
    elif "Int" in lineList and ("!" in lineList):
        #print(" line list int: ",lineList)
        pythonString = lineList[0]+" = "+lineList[2].split("!")[0]
        return pythonString,lineList[0],lineList[2].split("!")[0], "Int","".join(lineList[4:]).replace("\n","")
    elif "Int" in lineList:
        #print(" line list int: ",lineList)
        pythonString = lineList[0]+" = "+lineList[2].split("!")[0]
        return pythonString,lineList[0],lineList[2].split("!")[0], "Int","! Int. coef"
    elif "Logical" in lineList:
        return lineList[0], lineList[1], lineList[2]
    elif "Material" in lineList:
        return lineList[lineList.index('Material')+1].replace("\n","")
    elif "Variable" in lineList:
        pythonString = lineList[0]+" = "+lineList[2].split("!")[0]
        return pythonString,lineList[0],lineList[2].split("!")[0], "Variable",lineList[4].replace("\n","")
    
def wellBoreDataRead(fileName = None, onePhase = None):
    """
    onePhase is a parameter linked to wellbore simulations.
    It is used to control the file that will be read:
    
        if onePhase == True:
            fileName = environ["PWD"]+"/Data/wellbore.dat"
            pass
        else:
            fileName = environ["PWD"]+"/Data/twophasewellbore.dat"
            pass
    
    
    """
    materialIndex = 1
    wellBoreDataDict = {}
    if onePhase == None:
        onePhase = True
        pass
    if fileName == None:
        if onePhase == True:
            fileName = environ["PWD"]+"/Data/wellbore.dat"
            pass
        else:
            fileName = environ["PWD"]+"/Data/twophasewellbore.dat"
            pass
    try:
        dataFile = open(fileName,"r")
    except:
        input(" Necessary data have been read from\n"+\
                  " the generic wellbore data file: $WRAPPER/Data/Wellbore/wellbore.dat\n"+\
                  " A copy of that file is now in your reference directory as $PWD/Data/wellbore.dat.\n"+
                  " Modify it now to your own specific wellbore data.\n"+\
                  " Now, enter any ascii key to continue the simulation")
        if (onePhase == True):
            system("mkdir -p $PWD/Data;cp -p $WRAPPER/Data/Wellbore/wellbore.dat ./Data;chmod u+w $PWD/Data/wellbore.dat")
            pass
        else:
            system("mkdir -p $PWD/Data;cp -p $WRAPPER/Data/Wellbore/twophasewellbore.dat ./Data;chmod u+w $PWD/Data/twophasewellbore.dat")
            pass
        dataFile = open(fileName,"r")
    line = dataFile.readline()
    #print("first line", line)
            
    while "Transient terms" not in line:
        line = dataFile.readline()
        if "material" in line.lower():
            wellBoreDataDict["Material"+str(materialIndex)] = {}
            wellBoreDataDict1 = wellBoreDataDict["Material"+str(materialIndex)]
            wellBoreDataDict[line.lower().replace("material","").replace("!","").replace("\n","").replace(" ","")] = "Material"+str(materialIndex)
            materialIndex+=1
        elif ("=" in line) and ("True" in line):
            var, varType, varValue = wellBoreDataLineAnalysis(line)
            wellBoreDataDict1[var] = {varType:[varValue]}
        elif "=" in line:
            #print "debug1 ",line
            pythonString, var, varValue, varType, unit = wellBoreDataLineAnalysis(line)
            if varType == "Real" or varType == "Int":
                wellBoreDataDict1[var] = {varType:[varValue,unit]}
            else:
                line = dataFile.readline().replace("\n","")
                wellBoreDataDict1[var] = {varType:[line,unit]}  # the type is implicitely variable due to the fact we have
                                                                # to deal with a formula,
                                                                # the variation is over the coordinate
                wellBoreDataDict1[var] = {varType:[line,unit]}
    #print(wellBoreDataDict); raw_input("wellBoreDataDict:"+"Material"+str(materialIndex))
    return  wellBoreDataDict
