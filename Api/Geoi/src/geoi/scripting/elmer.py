from geoi import parameters
from parameter import inSecondsConverter
from os import path
from platform import python_version

def _elmerimport(scriptFile):
    """
    That function import all necessary python modules for a elmer simulation
    """
    scriptFile.write("# -*- coding: utf-8 -*-\n")
    scriptFile.write("from constant import epspH\n")
    scriptFile.write("import os\n")
    scriptFile.write("from mesh import *\n")        
    scriptFile.write("from datamodel import *\n") 
    scriptFile.write("from hydraulicmodule import *\n") 
    scriptFile.write("import hydraulicproblem\n") 
    scriptFile.write("from material import *\n")
    scriptFile.write("import sys\n")
    scriptFile.write("from chemicaltransportmodule import *\n")
    pyver = python_version()
    pyver = int(pyver[0]+pyver[2])
    if pyver> 25:
        scriptFile.write("import Gnuplot, Gnuplot.funcutils\n")
    else:
        scriptFile.write("import _Gnuplot, Gnuplot.funcutils\n")
    scriptFile.write("from listtools import normMaxListComparison, subtractLists\n\n")
#    scriptFile.write("""class executer():
#    '''
#'''
#def __init__(self):
#    '''
#'''
#""")
    return None
#
# aqueous master species
#
def _meshimport(paramsDict,scriptFile):
    """
    That function import the mesh
    """
    meshFileName = paramsDict.getParam(parameters.Gmsh_Name_File2).getValue()
    meshFileName2 = meshFileName.split('/')[-1]

    scriptFile.write("mesh = MeshReader(\"")
    scriptFile.write(meshFileName2)
    scriptFile.write("\")\n")
    return None
	
def _materials(paramsDict,scriptFile):
    """
    writing the material properties
    """
    materials = paramsDict.getParamValue(parameters.CUSTOM_MATERIAL_DB).getMaterials()
    temperature = paramsDict.getParam(parameters.TemperatureVariable).getValue()
    
    for ind in materials.keys():
        materialName = str(ind)+"Material"
        length = len(materialName+" = Material (name =")

        longDisp =  str(materials[ind]["LongitudinalDispersivity"])
        transDisp = str(materials[ind]["TransverseDispersivity"])
        scriptFile.write(materialName+" = Material (name = \""+str(ind)+"\",")
        if "EffectiveDiffusion" in materials[ind]:
            scriptFile.write(" "*length+"effectiveDiffusion            = EffectiveDiffusion ("+str(materials[ind]["EffectiveDiffusion"])+",unit=\"m**2/s\"),\\\n")
            print '1'
        if "KxPermeability" in materials[ind]:
            scriptFile.write(" "*length+"permeability                = Permeability(value = "+str(materials[ind]["KxPermeability"])+"),\\\n")
        if "EffectivePorosity" in materials[ind]:
            scriptFile.write(" "*length+"porosity                    = Porosity(value = "+str(materials[ind]["EffectivePorosity"])+"),\\\n")
        scriptFile.write(" "*length+"kinematicDispersion         = KinematicDispersion ("+longDisp+","+transDisp+"),\\\n")
        if temperature:
            scriptFile.write(" "*length+"specificHeat            = SpecificHeat ( "+str(materials[ind]["SpecificHeatCapacity"])+"),\\\n")
            scriptFile.write(" "*length+"thermalConductivity     = ThermalConductivity ("+str(materials[ind]["MaterialConductivity"])+"),\\\n")
        
        scriptFile.write(" "*length+"\n)\n")
    return None


def _regions(paramsDict,scriptFile):
    """
    writing the regions
    """
    zone_list = paramsDict.getParam(parameters.Zones_list).getValue()
    zone_Material_AqueousState_list = paramsDict.getParam(parameters.Zone_Material_AqueousState_list).getValue() 
    ind = 0
    regionList = "["
    for zone in zone_list:
        if ind!=0: 
            regionList+=","
        materialName = str(zone_Material_AqueousState_list[ind][0])+"Material"
        scriptFile.write(str(zone)+str(ind)+"Region = Region(support="+str(zone)+str(ind)+"Body, material= "+materialName+")\n")
        regionList+=str(zone)+str(ind)+"Region"
        ind+=1
    regionList+="]"          
    return zone_Material_AqueousState_list,regionList
    
def _outputs(paramsDict,scriptFile):
    """
    writing the outputs
    """
    outputList = paramsDict.getParam(parameters.ExpectedOutputs_list).getValue()
#            print "outputList",outputList
    if outputList != []:
        string = "expectedOutputs = ["
        for out in outputList:
            if str(out) == "pH":
                string+="ExpectedOutput(\"pH\",format=\"table\",name=\"pH_output\"),\n"
            else:
                string+="ExpectedOutput(\"Concentration\",\""+out+"\",format=\"table\",name=\""+out+"Output\"),\n"
        string = string[0:-2]+"]\n"
        scriptFile.write(string)
    else:        
        scriptFile.write("expectedOutputs = []\n")			
    return None
    
def _problem(paramsDict, scriptFile, regionList, iCLS, bCLS):
    """
    writing the problem part
    """
    nameFile = paramsDict.getParam(parameters.Title).getValue()
    scriptFile.write("problem  = ChemicalTransportProblem(name               = \""+\
    nameFile+"\",\\\n")
    scriptFile.write("                                    regions            = "+regionList+",\\\n")
    scriptFile.write("                                    initialConditions  = "+iCLS+",\\\n")
    scriptFile.write("                                    boundaryConditions = "+bCLS+",\\\n")
    scriptFile.write("                                    calculationTimes   = ["+\
    str(paramsDict.getParam(parameters.Elmer_Iterate_InitialTime).getValue())+" , "+\
    str(paramsDict.getParam(parameters.Elmer_Iterate_SimulationTime).getValue()+\
    paramsDict.getParam(parameters.Elmer_Iterate_InitialTime).getValue())+"],\\\n")
    scriptFile.write("                                    sources            = None,\\\n")
    darcy=[]
    if darcy == []:
        scriptFile.write("                                    darcyVelocity      = None,\\\n")
    else:
        scriptFile.write("                                    darcyVelocity      = Velocity(Vector(["+darcyVelocity+"])),\\\n")
    dataBase = path.split(paramsDict.getParam(parameters.CurrentDatabasePath).getValue())[-1]
    scriptFile.write("                                    chemistryDB        = \""+dataBase+"\",\\\n")
    scriptFile.write("                                    speciesBaseAddenda = speciesAddenda,\\\n")
    scriptFile.write("                                    kineticLaws        = None,\\\n")
    scriptFile.write("                                    activityLaw        = None,\\\n")
    #
    # temperature evaluation
    #
    scriptFile.write("                                    temperature        = ")
    if paramsDict.getParam( parameters.TemperatureVariable).getValue() == "True" :
        scriptFile.write("\"variable\",\\\n")
    else :
        scriptFile.write("\"constant\",\\\n")
    scriptFile.write("                                    outputs            = expectedOutputs)\n\n")
    return None
        
def _chemicaltransportmodule(paramsDict, scriptFile, moduleName):
    """
    writing the chemical transport module part
    """
    scriptFile.write("module = ChemicalTransportModule()\n")
    algorithm = paramsDict.getParam(parameters.Iterate_Algorithm).getValue()
    scriptFile.write("module.setData (problem, trace = 0, mesh = mesh, algorithm=\"" + str(algorithm) + "\")\n")
    if str(algorithm) == "NI":
        minStepSize = paramsDict.getParam(parameters.Elmer_Iterate_InitialTimeStep).getValue()
        maxStepSize = paramsDict.getParam(parameters.Elmer_Iterate_InitialTimeStep).getValue()
    else:
        minStepSize = paramsDict.getParam(parameters.Iterate_MinTimeStep).getValue()
        maxStepSize = paramsDict.getParam(parameters.Iterate_MaxTimeStep).getValue()
    
    scriptFile.write("module.setComponent(\""+ moduleName + "\",\"Phreeqc\")\n")
    
    scriptFile.write("module.setCouplingParameter(initialTimeStep        = "+\
        str(paramsDict.getParam(parameters.Elmer_Iterate_InitialTimeStep).getValue())+","+\
            "\n                            minTimeStep            = "+\
        str(minStepSize)+","\
            "\n                            maxTimeStep            = "+\
        str(maxStepSize)+","\
            "\n                            couplingPrecision      = "+\
        str(paramsDict.getParam(parameters.Iterate_CouplingPrecision).getValue())+","\
            "\n                            optimalIterationNumber = "+\
        str(paramsDict.getParam(parameters.Iterate_PicardTargetNumber).getValue())+","\
            "\n                            maxIterationNumber     = "+\
        str(paramsDict.getParam(parameters.Iterate_PicardMaxOfIterations).getValue())+","\
            "\n                            decreaTimeStepCoef     = "+\
        str(paramsDict.getParam(parameters.Iterate_RelaxationMinFactor).getValue())+","\
            "\n                            increaTimeStepCoef     = "+\
        str(paramsDict.getParam(parameters.Iterate_RelaxationMaxFactor).getValue())+")\n\n")
    return None


        
def _algebraicResolution(paramsDict, scriptFile):
    """
    That function is used to write down the algebraic resolution parameters
    """
    scriptFile.write("module.transport.setTransportParameter(algebraicResolution = \""+\
    paramsDict.getParam( parameters.Elmer_Linear_Solver ).getValue()+"\",\\\n")
    if paramsDict.getParam( parameters.Elmer_Linear_Solver ).getValue() == "Direct" :
        scriptFile.write("                                       accelerator          = \""+\
        paramsDict.getParam( parameters.Elmer_Direct_Method ).getValue()+"\",\\\n")
        scriptFile.write("                                       optimizeBandwidth	  = "+\
        paramsDict.getParam( parameters.Elmer_Optimize_Bandwidth ).getValue())
    elif paramsDict.getParam( parameters.Elmer_Linear_Solver ).getValue() == "Iterative" :
        scriptFile.write("                                       accelerator          = \""+\
        paramsDict.getParam( parameters.Elmer_Iterative_Method ).getValue()+"\",\\\n")
        if paramsDict.getParam( parameters.Elmer_Iterative_Method ).getValue() == "GMRES" :
            scriptFile.write("                                       GMRESRestart         = "+\
            str(paramsDict.getParam( parameters.Elmer_GMRES_Restart).getValue())+",\\\n")
            scriptFile.write("                                       preconditioner       = \""+\
            paramsDict.getParam(parameters.Elmer_Preconditioning).getValue()+"\",\\\n")
            if paramsDict.getParam(parameters.Elmer_Preconditioning).getValue() == "ILUT" :
                scriptFile.write("                                       ILUTTolerance        = "+\
                str(paramsDict.getParam( parameters.Elmer_ILUT_Tolerance ).getValue())+",\\\n")                                         
        else :
            scriptFile.write("You have to put a Linear System Solver")
        scriptFile.write("                                       convSolver          = "+\
        str(paramsDict.getParam( parameters.Elmer_Convergence_Tolerance ).getValue())+"\\\n")    
        scriptFile.write("                                      )\n") 
    return None
    
def _moduleLooping(paramsDict, scriptFile):
    scriptFile.write("""\n# We initialize here the data necessary to the display within the while loop\n
                     module.launch()\n
                     module.stepLoop = 0.0\n
                     module.initLoop = 0\n
                     g = Gnuplot.Gnuplot(debug=1)\n
                     while (module.simulatedTime < module.times[-1]):\n
                         module.oneTimeStep()\n

                     # Current simulation display\n
                     """)
    
    IOutputList = paramsDict.getParam(parameters.IOutputs_list).getValue()
    IRotate = paramsDict.getParam(parameters.IRotate).getValue()
    IFrequency = paramsDict.getParam(parameters.IFrequency).getValue()
    ITitle = paramsDict.getParam(parameters.ITitle).getValue()
    ISubTitle = paramsDict.getParam(parameters.ISubTitle).getValue()
    ISave = paramsDict.getParam(parameters.ISave).getValue()
    ISaveFrequency = paramsDict.getParam(parameters.ISaveFrequency).getValue()
    IOutputFormat = paramsDict.getParam(parameters.IOutputFormat).getValue()

    scriptFile.write("module.iTimePlot({0},\
                     g,\
                     title = %s,\
                     subTitle = %s,\
                     frequency = %d,\
                     rotate = %d,\
                     savingFrequency = %d,\
                     outputType = %s)\n\
                     g('unset multiplot')\n\
                     g.close()"%(IOutputList,str(ITitle),\
                     str(ISubTitle),\
                     IFrequency, IRotate, ISaveFrequency, IOutputFormat))
    


def _postProcessing(paramsDict, scriptFile):
    
    materials = paramsDict.getParamValue(parameters.CUSTOM_MATERIAL_DB).getMaterials()
    diffusivity = materials[materials.keys()[0]]["EffectiveDiffusion"]
    
    ExpOutToPlot = paramsDict.getParam(parameters.GlobalOutputs_list).getValue()
    
    if ExpOutToPlot != [] and paramsDict.getParam(parameters.GlobalDates_list).getValue() != []:
        # Converting dates in seconds
        dates = []
        for i in range(len(paramsDict.getParam(parameters.GlobalDates_list).getValue())):
            dates.append(inSecondsConverter(paramsDict.getParam(parameters.GlobalDates_list).getValue()[i]))
        
        
    
    
        scriptFile.write("\ndates = %d"%(dates))
        scriptFile.write("\nNb_meters = 5.")
    
    

        scriptFile.write("if module.getOutput(%s)[-1][0] > {1}:				# Here is checked if results are saved\
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\\n\
	#     Post processing : every plots - Second Method     ~\\n\
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\\n\
	XListe   = module.getOutput(%s)[0][1].getColumn(1)\\n\
	ploting = %d"%(ExpOutToPlot[0], dates[0], ExpOutToPlot))
	
    #scriptFile.write("""
	#h = []
	#h_ind = 0
	#for name in ploting:
	
		# creating lib of the results concerning "name" variable
		
		#name_unk	 = module.getOutput(name)

		#name_back    = []
		#time         = []

		# On recherche les colonnes correspondant aux annees ou l'on veut connaitre la repartition du pH
		#k = 0
		#j = 1
		#while k < len(dates) and j == 1:							# tant qu'il reste des dates (k) et que les precedentes ont ete trouvees (j=1)
			#i = 0
			#j = 0

			#while i < len(name_unk) and j == 0:						# j = 1 signifie que l'on a trouve une date superieure a date[k]

				#if name_unk[i][0] >= dates[k]:
					#name_back.append(name_unk[i][1].getColumn(-1))
					#j=1
					#time.append(name_unk[i][0])
					#i += 1
				#else:
					#i+=1
			
			#k += 1

		
		# ploting the curves together
	


		# units changes
		#if name.lower() == 'porosity': 
			#coef = 100
		#elif name.lower() == 'ph':
			#coef = 1
		#else:
			#coef = 1


		#XListe2 = []
		#maximum  = 0
		#minimum = name_back[0][0]*coef
		#for i in range(len(name_back[0])):
		
		#	if (name.lower() != 'porosity' or i > 1) and XListe[i] <= Nb_meters :				# We delete the porosity terms equal to 0
				#XListe2.append(XListe[i])
	
				#for j in range(len(name_back)):
					#name_back[j][i] = name_back[j][i]*coef
					#if name_back[j][i]>maximum:
					#	maximum = name_back[j][i]
					#if name_back[j][i]<minimum:
					#	minimum = name_back[j][i]
					#if name.lower() != 'porosity':
					#	name_back[j][i-2] = name_back[j][i]

		

		



		#h.append(Gnuplot.Gnuplot(debug=1))
		

		
		#h[h_ind].title(name + ' profiles in case ' + str(module.problem.getName()) + '\\\\nporosity = ' + str(int(module.regions[0].getMaterial().getPorosity().getValue()*100)) + '% | diffusivity = ' + str(round({0}*10**12)/10**12))
		#h[h_ind]('set style data lines')

		# Label and scale of output axis
#		ecart = max(name_back[-1])-min(name_back[-1])
		#ecart = maximum - minimum
		#maximum = maximum + ecart/10
		#minimum = minimum - ecart/10
		#h[h_ind]('set xrange['+ str(minimum) + ':'+ str(maximum) + ']')
		#h[h_ind]('set xtics 0,' + str((maximum-minimum)/4) + "rotate by -20")
		#h[h_ind]('set xlabel "' + str(name) + '"')
		#h[h_ind]('set format x "%.3e"')
		
		#h[h_ind]('set yrange[0:'+ str(Nb_meters) +']')
		#h[h_ind]('set ytics 0,' + str(Nb_meters/4))
		#h[h_ind]('set ylabel "m"')
		#h[h_ind]('set format y "%10.1f"')
		
		
		# Plot
		#h[h_ind].plot(Gnuplot.Data(name_back[0][0:len(XListe2)], XListe2, title=str(int(round(time[0]/3.15576e+7))) +' years' ))
		
		#for j in range(1,len(name_back)):
		#		h[h_ind].replot(Gnuplot.Data(name_back[j][0:len(XListe2)], XListe2, title=str(int(round(time[j]/3.15576e+7))) +' years' ))
		
		# Saving the graphics
		#h[h_ind]('set term postscript portrait')
		#h[h_ind]('set output "'+ module.problem.getName() + '_' + name + '.ps"')
		#h[h_ind]('set size 0.7, 0.7')
		#h[h_ind].plot(Gnuplot.Data(name_back[0][0:len(XListe2)], XListe2, title=str(int(round(time[0]/3.15576e+7))) +' years' ))
		
		#for j in range(1,len(name_back)):
				#h[h_ind].replot(Gnuplot.Data(name_back[j][0:len(XListe2)], XListe2, title=str(int(round(time[j]/3.15576e+7))) +' years' ))

		#h_ind += 1
				
	
	
#else:					# If no results are saved
	#print 'Warning : selected dates are larger than simulation time limit'

#import wx
#wx.MessageDialog(self.parent, "You have to select an output\\nto complete that action."\\
#            , "Warning", wx.OK | wx.ICON_WARNING).ShowModal()

#import time
#time.sleep(3)
	
#""".format(diffusivity))
    
    scriptFile.write("""\nmodule.end()""")
    
    
    

