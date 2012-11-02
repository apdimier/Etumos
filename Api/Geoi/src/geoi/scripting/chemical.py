from geoi import parameters
def _chemical(paramsDict,scriptFile):
    """
    That function enables to write the python script
    that will be launched to simulate the involved physics.
    """
    
    scriptFile.write("#~~~~~~~~~~~~~~~~~~~\n")
    scriptFile.write("# Chemical Addenda ~\n")
    scriptFile.write("#~~~~~~~~~~~~~~~~~~~\n")
    scriptFile.write("speciesAddenda = []\n")
#
# aqueous master species
#
    ams = paramsDict.getParamValue(parameters.CUSTOM_CHEMISTRY_DB).getSolutionMasterSpecies()
    for i in ams.keys() :
	        elementName = _strHandlung(i)
	        elementName = elementName.replace("(","")
	        elementName = elementName.replace(")","")
	        elementName+="AMS"
	        string = elementName + " = AqueousMasterSpecies("
	        length = len(string)
	        string += "symbol = \""+ ams[i]['SPECIES']+"\",\\\n"
	        scriptFile.write(string)
	        string = " "*length + "name = \""+ ams[i]['ELEMENT']+"\",\\\n"
	        scriptFile.write(string)
	        string = " "*length + "element = \""+ ams[i]['FORMULA']+"\",\\\n"
	        scriptFile.write(string)
	        string = " "*length + "molarMass = MolarMass("+ str(ams[i]['GFW'])+",\"g/mol\"),\\\n"
	        scriptFile.write(string)
	        string = " "*length + "alkalinity = "+ str(ams[i]['LOGK'])+")\n"
	        scriptFile.write(string)
	        scriptFile.write("speciesAddenda.append("+elementName+")\n")
#
# solution secondary species
#        
    ass = paramsDict.getParamValue(parameters.CUSTOM_CHEMISTRY_DB).getSolutionSecondarySpecies()
    for i in ass.keys() :
        print "solution secondary species ",i
        print "solution secondary species ",_strHandlung(i)
        string = _strHandlung(i) + "SSp = AqueousSecondarySpecies("
        length = len(string)
        string += "symbol = \""+ ass[i]['FORMULA']+"\",\\\n"
        scriptFile.write(string)
        #equation = ass[i]['EQUATION']
        #string = " "*length + "formationReaction = ["+ str(ass[i]['LOGK'])+",\\\n"
        #scriptFile.write(string)
        tlist = ""
        
        a = str(ass[i]['EQUATION']).split(" ")
        liste = []
        ind = a.index("=")
        a.remove(a[ind+1])
        dig = 1
        for el in a:
            if el.isdigit():
                dig = el
            elif el not in ["+","-","=",""]:
                if a.index(el) > ind:
                    print "dig",dig
                    digi = dig
                    dig = "-"+str(digi)
                    liste.append((el,dig))
                else:
                    liste.append((el,dig))
                dig = 1        
        print liste
        for el in liste:
            tlist += "(\""+el[0]+"\","+str(el[1])+"),"
        tlist = tlist[0:-1]
        print " tlist ",tlist
        string = " "*length + "formationReaction = [\\\n"
        scriptFile.write(string)
        string = " "*(length+len("formationReaction = ["))+tlist+"],\\\n"
        scriptFile.write(string)
        string = " "*length + "logK25 = "+ str(ass[i]['LOGK'])+",\\\n"
        scriptFile.write(string)
        string = " "*length + "name = \""+ ass[i]['ELEMENT']+"\")\n"
        scriptFile.write(string)
        scriptFile.write("speciesAddenda.append("+_strHandlung(i)+"SSp)\n")
#
# exchange master species
#            
    exms = paramsDict.getParamValue(parameters.CUSTOM_CHEMISTRY_DB).getExchangeMasterSpecies()
    for i in exms.keys() :
        string = str(i) + " = SorbingSiteMasterSpecies("
        string += "symbol = \"" + exms[i]['FORMULA']+"\","
        string += "name   = \"" + str(exms[i]['NAME'])+"\")\n"
        scriptFile.write(string)
        scriptFile.write("speciesAddenda.append("+str(i)+")\n")
#
# exchange species
#            
    exs = paramsDict.getParamValue(parameters.CUSTOM_CHEMISTRY_DB).getExchangeSpecies()
    for i in exs.keys():
        if i not in exms.keys(): continue
        if str(i)[-1] == "-":
            stresp = str(i)[0:-1]+"m"
            string = stresp + "ESp = SorbedSecondarySpecies("
        else:
            stresp = str(i)[0:]
            string = stresp + "ESp = SorbedSecondarySpecies("
    
        length = len(string)
        string += "symbol = \""+ exs[i]['FORMULA']+"\",\\\n"
        scriptFile.write(string)
    #equation = exs[i]['EQUATION']
    #string = " "*length + "formationReaction = ["+ str(exs[i]['LOGK'])+",\\\n"
    #scriptFile.write(string)
        tlist = ""
        
        a = str(exs[i]['EQUATION']).split(" ")
        liste = []
        ind = a.index("=")
        a.remove(a[ind+1])
        dig = 1
        for el in a:
            if el.isdigit():
                dig = el
            elif el not in ["+","-","=",""]:
                if a.index(el) > ind:
                    print "dig",dig
                    digi = dig
                    dig = "-"+str(digi)
                    liste.append((el,dig))
                else:
                    liste.append((el,dig))
                dig = 1        
        for el in liste:
            tlist += "(\""+el[0]+"\","+str(el[1])+"),"
        tlist = tlist[0:-1]
        string = " "*length + "formationReaction = ["+ tlist+"],\\\n"
        scriptFile.write(string)
        string = " "*length + "logK25 = "+ str(exs[i]['LOGK'])+",\\\n"
        scriptFile.write(string)
        string = " "*length + "name = \""+ exs[i]['ELEMENT']+"\",)\n"
        scriptFile.write(string)
        scriptFile.write("speciesAddenda.append("+stresp+"ESp)\n")

    for i in exs.keys():
        if i in exms.keys(): continue
        if str(i)[-1] == "-":
            stresp = str(i)[0:-1]+"m"
            string = stresp + "ESp = SorbedSecondarySpecies("
        else:
            stresp = str(i)[0:]
            string = stresp + "ESp = SorbedSecondarySpecies("
    
        length = len(string)
        string += "symbol = \""+ exs[i]['FORMULA']+"\",\\\n"
        scriptFile.write(string)
    #equation = exs[i]['EQUATION']
    #string = " "*length + "formationReaction = ["+ str(exs[i]['LOGK'])+",\\\n"
    #scriptFile.write(string)
        tlist = ""
        
        a = str(exs[i]['EQUATION']).split(" ")
        liste = []
        ind = a.index("=")
        a.remove(a[ind+1])
        dig = 1
        for el in a:
            if el.isdigit():
                dig = el
            elif el not in ["+","-","=",""]:
                if a.index(el) > ind:
                    print "dig",dig
                    digi = dig
                    dig = "-"+str(digi)
                    liste.append((el,dig))
                else:
                    liste.append((el,dig))
                dig = 1        
        for el in liste:
            tlist += "(\""+el[0]+"\","+str(el[1])+"),"
        tlist = tlist[0:-1]
        string = " "*length + "formationReaction = ["+ tlist+"],\\\n"
        scriptFile.write(string)
        string = " "*length + "logK25 = "+ str(exs[i]['LOGK'])+",\\\n"
        scriptFile.write(string)
        string = " "*length + "name = \""+ exs[i]['ELEMENT']+"\",)\n"
        scriptFile.write(string)
        scriptFile.write("speciesAddenda.append("+stresp+"ESp)\n")
#
# mineral species
#
    ePhases = paramsDict.getParamValue(parameters.CUSTOM_CHEMISTRY_DB).getMineralPhases()
    for i in ePhases.keys() :
        elementName = _strHandlung(i)
        elementName = elementName.replace("(","")
        elementName = elementName.replace(")","")
        
        string = elementName + "Ad = MineralSecondarySpecies("
        length = len(string)
        string += "symbol = \""+ ePhases[i]['FORMULA']+"\",\\\n"
        scriptFile.write(string)
        #equation = ass[i]['EQUATION']
        #string = " "*length + "formationReaction = ["+ str(ass[i]['LOGK'])+",\\\n"
        #scriptFile.write(string)
        tlist = ""
        
        a = str(ePhases[i]['EQUATION']).split(" ")[1:]
        liste = []
        ind = a.index("=")
        dig = 1
        for el in a:
            if el.isdigit():
                dig = el
            elif el not in ["+","-","=",""]:
                if a.index(el) < ind:
                    print "dig",dig
                    digi = dig
                    dig = "-"+str(digi)
                    liste.append((el,dig))
                else:
                    liste.append((el,dig))
                dig = 1        
        print liste
        for el in liste:
            tlist += "(\""+el[0]+"\","+str(el[1])+"),"
        tlist = tlist[0:-1]
        print " tlist ",tlist
        string = " "*length + "formationReaction = ["+ tlist+"],\\\n"
        scriptFile.write(string)
        string = " "*length + "logK25 = "+ str(ePhases[i]['LOGK'])+",\\\n"
        scriptFile.write(string)
        string = " "*length + "name = \""+ ePhases[i]['NAME']+"\",\\\n"
        if str(ePhases[i]['DENSITY']) == "":  
            string = string[0:-3] + ")\n"
        else:
            string +=" "*length + "density = Density("+ str(ePhases[i]['DENSITY'])+",\"kg/m**3\"))\n"
        
        scriptFile.write(string)
        scriptFile.write("speciesAddenda.append("+elementName+"Ad)\n")
#Quartz = MineralSecondarySpecies(symbol='SiO2',
#                                 formationReaction = [('H4SiO4', 1),('H2O', -2)],\
#                                 logK25 = -3.6,\
#                                 name ='Quartz',\
#                                 density  = Density(2648.29,'kg/m**3'))
#
# surface master species
#
    eSurface = paramsDict.getParamValue(parameters.CUSTOM_CHEMISTRY_DB).getSurfaceMasterSpecies()
    for i in eSurface.keys() :
        spec = str(i).replace("+","p")
        spec = str(spec).replace("-","m")
        spec = str(spec).replace(" ","")
        string = spec + " = SurfaceMasterSpecies("
        length = len(string)
        string += "symbol = \""+ eSurface[i]['FORMULA']+"\",\\\n"
        scriptFile.write(string)
        string = " "*length + "name = \"" + eSurface[i]['NAME'] + "\")\n"
        scriptFile.write(string)
#
# surface species
#
    eSurface = paramsDict.getParamValue(parameters.CUSTOM_CHEMISTRY_DB).getSurfaceSpecies()
    for i in eSurface.keys() :
#
# we replace + by p and - by m; the name being the species name on the right of "="
#        
        spec = str(i.split("=")[1]).replace("+","p")
        spec = str(spec).replace("-","m")
        spec = str(spec).replace(" ","")
        string = spec + " = SurfaceSecondarySpecies("
        length = len(string)

        string += "symbol = \""+ eSurface[i]['EQUATION'].split()[-1]+"\",\\\n"
        scriptFile.write(string)
        #equation = ass[i]['EQUATION']
        #string = " "*length + "formationReaction = ["+ str(ass[i]['LOGK'])+",\\\n"
        #scriptFile.write(string)
        tlist = ""

        a = str(eSurface[i]['EQUATION']).split(" ")[1:]
        liste = []
        ind = a.index("=")
        liste = _anal(str(eSurface[i]['EQUATION']).split("=")[0])
        for el in liste:
                tlist += "(\""+el[0]+"\","+str(el[1])+"),"
        tlist = tlist[0:-1]
    #print " tlist ",tlist
        string = " "*length + "formationReaction = ["+ tlist+"],\\\n"
        scriptFile.write(string)
        string = " "*length + "logK25 = "+ str(eSurface[i]['LOGK'])+")\n"
        scriptFile.write(string)
        scriptFile.write("speciesAddenda.append("+spec+")\n")
    del(ass)
    del(ams)
        
#Nabis = AqueousSecondarySpecies (symbol="Na+",
#                                 formationReaction = [("Na+", 1)],
#                                 logK25 =0.0,
#                                 name ="Na")
    scriptFile.write("#~~~~~~~~~~~~~~~~~~\n")
    scriptFile.write("# Chemical States ~\n")
    scriptFile.write("#~~~~~~~~~~~~~~~~~~\n")
    scriptFile.write("ChemicalStateList = []\n")
    aqueousStatesList = paramsDict.getParam(parameters.AqueousStates_list).getValue()
    aqueousStatesPropertiesList = paramsDict.getParam(parameters.AqueousStates_Properties_list).getValue()
    aqueousSpeciesList = paramsDict.getParam(parameters.AqueousStates_Species_list).getValue()
    mineralPhaseList = paramsDict.getParam(parameters.AqueousStates_MineralPhases_list).getValue()            
    mineralPhasePropertiesList = paramsDict.getParam(parameters.AqueousStates_MineralPhases_Properties_list).getValue()
    exchangeSpeciesList = paramsDict.getParam(parameters.AqueousStates_ExchangeSpecies_list).getValue()            
    exchangeSpeciesPropertiesList = paramsDict.getParam(parameters.AqueousStates_ExchangeSpecies_Properties_list).getValue()
#            print "mineralPhasePropertiesList",mineralPhasePropertiesList[0],mineralPhasePropertiesList[1][0][1]
    ind = 0
#            print aqueousStatesPropertiesList
    for aStates in aqueousStatesList:
        aSName = str(aStates) + "AqueousSolution"
        aSData = aqueousStatesPropertiesList[ind]
        pHString = "pH = " + aSData[0][1]
        peString = "pe = " + aSData[2][1]
        TString = "temperature = " + aSData[1][1]
        eCList = ""
        indiz = 1
        stringAssociation = ""
        for elementConcentration in aqueousSpeciesList[ind]:
            if elementConcentration[0].find("[") != -1:
                ionAssociation = elementConcentration[0][0:elementConcentration[0].find("[")]
                mineralAssociation = elementConcentration[0][elementConcentration[0].find("[")+1:elementConcentration[0].find("]")]
                #
                Association = [ionAssociation,mineralAssociation]
                #
                stringAssociation = ",mineralEquilibrium = [(\""+ionAssociation+"\",\""+mineralAssociation+"\","+elementConcentration[1]+")]"
                
            else:
                eCList += "ElementConcentration (\""+str(elementConcentration[0])+"\","+\
                            str(elementConcentration[1])+","+"\"mol/l\"),\n"
                if indiz < len(aqueousSpeciesList[ind]) :
                    eCList += " "*(len(aSName)+len(" = AqueousSolution (elementConcentrations = ")+1)
                    indiz+=1
#                
#                eCList += "]"
#
        eCList = eCList[0:-2]+"\n"
#
# mineralPhase associated to an aqueous state
#
        mineralPhaseName = str(aStates) + "MineralPhase = MineralPhase("
        mineralPhaseName_Length = len(mineralPhaseName)
        ePList = ""
        if len(mineralPhaseList[ind]) == 0:
            ePList = "[])"
            mineralPhaseName = ""
        else:
            ePList = "["
            indM = 0
            for equilibriumPhase in mineralPhaseList[ind]:
                if equilibriumPhase != None :
                    if indM == 0  :
                        ePList += "MineralTotalConcentration(\"" + str(equilibriumPhase) + "\"," +\
                    str(mineralPhasePropertiesList[ind][indM][1])+", \"mol/l\",saturationIndex = "+mineralPhasePropertiesList[ind][indM][0]+"),\n"
                    else:
                        ePList += " "*mineralPhaseName_Length+\
                    "MineralTotalConcentration(\"" + str(equilibriumPhase) + "\"," +\
                    str(mineralPhasePropertiesList[ind][indM][1])+", \"mol/l\",saturationIndex = "+mineralPhasePropertiesList[ind][indM][0]+"),\n"                    
                indM+=1
            ePList = ePList[0:len(ePList)-2]+"])"
            scriptFile.write(mineralPhaseName+ePList+"\n")
            mineralPhaseName = str(aStates) + "MineralPhase"
#
# exchange associated to an aqueous state
#
        exchangeName = str(aStates) + "IonicExchangers"
        iEList = ""
        if len(exchangeSpeciesList[ind]) == 0:
            iEList = "[])"
        else:
            iEList = "["
        indM = 0
        for exchangeSpecies in exchangeSpeciesList[ind]:
            iEList = iEList + "ExchangeBindingSpecies(\"" + str(exchangeSpecies) + "\", MolesAmount(" +\
            str(exchangeSpeciesPropertiesList[ind][indM][0])+", \"mol\")),\n"
            indM+=1
        if len(exchangeSpeciesList[ind]) != 0: 
            iEList = iEList[0:len(iEList)-2]+"])"
            scriptFile.write(exchangeName+" = IonicExchangers("+iEList+"\n")
            exchangeName = ",ionicExchanger = "+exchangeName
        else:
            exchangeName = ""
#
#
#                
        stringLength = " "*(len(aSName)+len(" = AqueousSolution ("))
        eCList += " "*(len(aSName)+len(" = AqueousSolution (elementConcentrations = "))
        scriptFile.write(aSName+" = AqueousSolution (elementConcentrations = ["+eCList+"],\\\n")
        scriptFile.write(stringLength+pHString+",\\\n")
        scriptFile.write(stringLength+peString+",\\\n")
        scriptFile.write(stringLength+TString+")\n")
        ind+=1
        cSName = str(aStates) + "ChemicalState"
        addenda = _addenda(mineralPhaseName,exchangeName)
        if aSData[3][0] in ["0","4"]:
            scriptFile.write(cSName+" = ChemicalState (\""+str(aStates)+"\","+aSName+addenda+stringAssociation+")\n\n")
        elif aSData[3][0] in ["2","5"]:
            scriptFile.write(cSName+" = ChemicalState (\""+str(aStates)+"\","+aSName+addenda+stringAssociation+",charge=True)\n\n")
        else:
            scriptFile.write(cSName+" = ChemicalState (\""+str(aStates)+"\","+aSName+addenda+stringAssociation+",phFixed=(\""+\
            aSData[3][1][1]+"\","+aSData[3][1][0]+"))\n\n")

def _addenda(mineralPhaseName,exchangeName):
    string = ""
    if mineralPhaseName != "":
        string += ",mineralPhase = "+mineralPhaseName
        if exchangeName != "":
            string += " "+exchangeName
    else:
        if exchangeName != "":
            string += " "+exchangeName
        
    return string
        
def _strHandlung(string):
     string = string.replace("+","p")
     string = string.replace("-","m")
     return string

