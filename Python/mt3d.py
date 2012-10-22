# -*- coding: utf-8 -*-
""" 
 File used to define the class associated to the Mt3d software
 It uses head files issued from the modflow 96 software
"""

from chemicaltransport import ChemicalTransportProblem

from copy import *

from FortranFormat import FortranFormat, FortranLine

from generictools import isInstance, Generic
from numpy import array, float as Float
import os
from os import system

from PhysicalProperties import EffectiveDiffusion, KinematicDispersion, Velocity
from PhysicalQuantities import PhysicalQuantity,Head
from species import Species
from cartesianmesh import *
from subprocess import Popen
from sys import exit
import threading
import thread
from types import FloatType, ListType, StringType, TupleType
import WMt3d
#from datamodel import BoundaryCondition

_e104 = FortranFormat("E10.4")
_e105 = FortranFormat("E10.5")
_e106 = FortranFormat("E10.6")
_e108 = FortranFormat("E10.8")
_f100 = FortranFormat("F10.0")
_f158 = FortranFormat("E15.8")
_fe150 = FortranFormat("E15.0")
_fe158 = FortranFormat("E15.8")
_i10   = FortranFormat("I10")

def _foti10(arg):
    return str(FortranLine([arg],_i10))

def _fot158(arg):
    return str(FortranLine([arg],_f158))

def _fote104(arg):
    return str(FortranLine([arg],_e104))

def _fote105(arg):
    return str(FortranLine([arg],_e105))

def _fote106(arg):
    return str(FortranLine([arg],_e106))
    
def _fote108(arg):
    return str(FortranLine([arg],_e108))

def _fot100(arg):
    return str(FortranLine([arg],_f100))

def _fote150(arg):
    return str(FortranLine([arg],_fe150))

def _fote158(arg):
    return str(FortranLine([arg],_fe158))

def _initFunction(list_regionc,mesh,boundary_list,variables,fichier,fmtin):
    """
    A Dictionary is set up to treat boundary conditions.
    The semantic of mt3d is kept
    """
    from string import ljust

    ncol = mesh.nb_of_intervals[0]
    nlay = 1
    nrow = mesh.nb_of_intervals[1]
    numberOfCells = ncol*nrow*nlay
    ibc = {}
    for variablen in variables: 
#        print variablen.name
        ibc[variablen.name.upper()] = [0.e+00]*numberOfCells
    
    for boundary in boundary_list:
	ind_min = boundary.boundary.zones[0].getIndexMin()
        ind_max = boundary.boundary.zones[0].getIndexMax()
	iBeg = ind_min.i
	iFin = ind_max.i
	jBeg = ind_min.j
	jFin = ind_max.j
	for spezien in boundary.getValue().aqueousSolution.elementConcentrations :
	    wert = spezien.getValue()
	    symbol = spezien.getSymbol().upper()
            for i in range(iBeg, iFin+1,1):
                for j in range(jBeg, jFin+1,1):
                     k = (j-1)*ncol+i
                     ibc[symbol][k-1] = wert
		     pass
		pass

    for variablesName in variables:
        sch = variablesName.name.upper()
        fichier.write("%10i%10s%20s%10i   !%25s\n"\
                            %(100,_fote104(1.e+00),ljust(fmtin,20),4,ljust(sch,25)))
        for i in range(0,len(ibc[sch])):
            fichier.write("%15s"%(_fot158(ibc[sch][i])))
            if ((i+1)%ncol==0)and(i!=numberOfCells):
                fichier.write("\n")
		pass
        pass

class Mt3d(Generic):
    """
    The class Mt3D enables to handle a saturated coupled geochemical transport problem
    """
    def __init__(self):
        Generic.__init__(self)
        self.BoundaryConditions = None
        self.componentsNumber = None
        self.componentName = "Mt3d"
        self.coordinates = None
        self.fwel = "F" # set to true it can be used to treat flux boundary conditions
	self.hpor = 0
        self.name= None
        self.setupfile = None
	self.stop = 0
        self.timeBoundaryConditionVariation = []
        self.solver = WMt3d	
	pass
	
    def advanceTime(self):
        """
        Updating xnew and time
        """
        self.solver.advanceTime()

    advanceTimeStep = advanceTime

    def coucou(self,message = None):
        """
        Is it useful
        """
        if message == None:
            print "coucou"
            pass
        else:
            print "message"
            pass
	
    def defineDataFiles(self, input, trace, name=None):
        """
        Definition of input file name
        and a flag for trace
        """
	if (name!=None) : 
	    self.name = name
	else:
	    
	    self.name = "#"+str(input)
	    pass
        self.solver.defineDataset(input, trace)

    def getConcentration(self):
        """
        To obtain solution concentration vectors for each primary species
        """
        return self.solver.getConcentration()
	
    def getConcentrationValues(self):
        """
        To obtain solution concentration vectors for each primary species
        """
        return self.solver.getConcentration()
	
    def getRegions(self):
        """
        Building up the btn file with regions list
        """
        return self.regions
	
    def getCoordinatesValues(self):
    
        """
        Used to get coordinate values in 2 dimensions
	Should be modified to take a third dimension into account
	nx <--> self.delr
	ny <--> self.delc
        """
	if self.coordinates == None:
	    if (len(self.delr)!=1 and len(self.delc)!=1):
	        cellcenter_r = _cellCenter(self.delr)
	        cellcenter_c = _cellCenter(self.delc)

		cellcenter_rmesh = []
		cellcenter_cmesh = []
		for i in cellcenter_c:
		    for j in cellcenter_r[1:]:
		        cellcenter_rmesh.append(j)   
		for i in cellcenter_c:
		    for j in cellcenter_r[1:]:
		        cellcenter_cmesh.append(i)   
	        self.coordinates = [cellcenter_rmesh,cellcenter_cmesh]
	    elif len(self.delr)!=1:

	        cellcenter_r = _cellCenter(self.delr)

 	        #In one dimension, ind_min and ind_max are supposed to be identical
		#We just verify on which edge boundaries are
		# We are able here to treat multiple boundaries
		# These boundaries must be on the edge of the domain : 1, nx, 1, ny
		# On one direction we can only have up to two boundaries
		i1 = []
		boundary = self.getBoundaryConditions()
		if boundary != []:
	            for boundary in self.getBoundaryConditions():
	                ind_min = boundary.boundary.zones[0].getIndexMin()
	                ind_max = boundary.boundary.zones[0].getIndexMax()
                        if (boundary.btype!='Flux'):
	                    i1.append(ind_min.i)
		        pass
		else:
		    i1.append(1)
 		if i1 != []:
		    if i1[0]==1 and len(i1)!=1 and len(i1)!=2:
	                self.coordinates = [cellcenter_r[1:],[0.5]*len(self.delr[1:])]
 		    elif i1[0]==1 and len(i1)==1 and boundary != []:
                        self.coordinates = [self.delr[:-1],[0.5]*len(self.delr[:-1])]
 		    elif i1[0]==1 and len(i1)==1:
                        self.coordinates = [self.delr,[0.5]*len(self.delr)]
                    elif len(i1)==2:
                        self.coordinates = [self.delr[1:-1],[0.5]*len(self.delr[1:-1])]
                    else :
                        self.coordinates = [self.delr,[0.5]*len(self.delr[:-1])]
		else:
                    self.coordinates = [self.delr,[0.5]*len(self.delr)]
		
	    elif len(self.delc)!=1:

	        for boundary in self.getBoundaryConditions():
	            ind_min = boundary.boundary.zones[0].getIndexMin()
	            j1 = ind_min.j
		    if j1==1:
	                self.coordinates = [self.delc[1:],[0.5]*len(self.delc[1:])]
                    else:
                        self.coordinates = [self.delc[:-1],[0.5]*len(self.delc[:-1])]
	    else:
	        raise "getCoordinatesValues problem"
            pass
	else:
	    pass
	#print " mc dbg out of getcoordinates ",len(self.coordinates[0]) 
        return self.coordinates
	
    def init(self, name = None):
        """
        We begin initialization using input and database files
        """
	self.trace=1

	if name:
	    self.name  = name
	    
	else:
	    self.name  = "Generic_name"
	    raise " No name defines by the user"
	    pass
        self.setupfile = self.name+".fil"

	self.solver.defineDataset(self.setupfile,self.trace)
	
        self.solver.initialize()
        
	return None
	
    def Initialize(self):
        """
        Initialization based on input and database files
        """
        self.solver.initialize()

    def setAdditionalSourceValues(self,source):
        """
        Transfer of a concentration field to Mt3d, which corresponds to the source term necessary
	to the Picard algorithm.
        """
        self.solver.setSource(source)
	return
	
    def setBoundaryCondition(self,listOfConcentrations,i_min,i_max,j_min,j_max):
	"""
	We set new boundary conditions
	listOfConcentrations: list of concentrations is a list of floats 
	ind_min.i,ind_max.i,ind_min.j,ind_max.j are bounds of the domain where BC have to be set
	"""
        self.solver.setBoundaryCondition(listOfConcentrations,i_min,i_max,j_min,j_max)
        return

    def setConvection(self,scheme):
        """
        That function is used to define parameters controling the spatial disc. scheme 
        """
        from string import capwords
        if scheme.upper()=="CENTRAL":
            self.mixelm = 0
            self.nadvfd = 2
        elif scheme.upper().replace(".","")=="TVD":
            self.mixelm = -1
            self.nadvfd = 2
        elif scheme.upper()=="UPWIND":
            self.mixelm = 0
            self.nadvfd = 0
        else:
            print "Warning, the discretisation scheme hasn't been recognized,"\
                  "the upwind TVD default option will be taken"
            self.mixelm = -1
            self.nadvfd = 2
	    pass

    def setConcentrationValues(self,concentrations):
        """
        Transfer of concentrations to Mt3d, The concentrations have been
	previously reorganized in a Mt3d structure form.
        """
#	print " length of the conc list got from phreeqc ",len(concentrations)
        self.solver.setConcentration(concentrations)
	return
	
    def setHydraulicPorosityParameter(self,hpor):
        """
        hpor is equal to 1 if a hydraulic flux has to be taken into account, set to 0 by default otherwise
        """
        self.solver.setHydrVPorParameter(hpor)
        self.hpor = hpor
        if hpor ==1:
            print " mt3d dbg within setHydraulicPorosityParameter fwel is set to T"
            self.fwel = "T"
        else:
            print " mt3d dbg within setHydraulicPorosityParameter fwel is kept to F"

    def setNewVelocity(self):
        """
        We set the new velocity which has been set up by VelocityFieldRecover.
        """
        self.solver.setVelocity()
	return
        
    def VelocityFieldRecover(self,permeabilityField):
        """
	It takes the permeability as parameter and returns the new velocity field
	The hypothesis is made of a predefined head field
	"""
	from string import ljust
#
# We redefine the list of files necessary to simulate the case
#
	if (os.path.isfile("Monod.fil")):
	    os.remove('Monod.fil')
        self.file_fil=open("modf.fil",'w')
	if self.variablePorosityOption and self.velmod>1.e-20 and self.hpor == 1:

            self.file_fil.write("LIST 6 %25s\n",\
				"BAS 5  %25s\n",\
				"SIP 13 %25s\n",\
				"OC 14  %25s\n",\
				"WEL 15  %25s\n",\
				"BCF 11 %25s\n"\
				%(ljust("modhw.lst",25),\
				ljust("modhw.bas",25),\
				ljust("modhw.sip",25),\
				ljust("modhw.wel",25),\
				ljust("modhw.oc",25),\
				ljust("modhw.bcf" ,25)))
	else:
	    print "mc dbg self.variablePorosityOption without wells"
            self.file_fil.write("LIST 6 %25s\n",\
				"BAS 5  %25s\n",\
				"SIP 13 %25s\n",\
				"OC 14  %25s\n",\
				"BCF 11 %25s\n"\
				%(ljust("modhw.lst",25),\
				ljust("modhw.bas",25),\
				ljust("modhw.sip",25),\
				ljust("modhw.oc",25),\
				ljust("modhw.bcf" ,25)))
	if (os.path.isfile("modhw.lst")):
	    os.remove('modhw.lst')
#
# We destroy the .bas file, 
# it should contain the head we want to simulate
#
	if (os.path.isfile('modhw.bas')):
	    os.remove('modhw.bas')
#
# Once destroied we reconstruct the .bas file 
#
        self.basFile = open("modhw.bas",'w')
	
        self.basFile.write("%s \n"%("Python generated file"))
        self.basFile.write("%s \n"%("Er hatte vier Kinder"))
        ncol = self.mesh.getNbPoints("X")-1
        nrow = self.mesh.getNbPoints("Y")-1	    
	nlay = 1
	numberOfCells = ncol*nrow*nlay	    
        self.basFile.write("%10i%10i%10i%10i%10i   !nlay,nrow,ncol,nper,itmuni\n"\
                            %(nlay,self.mesh.getNbPoints("Y")-1,self.mesh.getNbPoints("X")-1,1,4))
	if self.variablePorosityOption and self.fwel == "T" and self.hpor == 1:
            self.basFile.write("%s\n"%(" 11 12 00  0  0  0  0 00 19  0  0 22 00 00 00 00 00 00 00 00 00 32 00 00"))
	else:
            self.basFile.write("%s\n"%(" 11 00 00  0  0  0  0 00 19  0  0 22 00 00 00 00 00 00 00 00 00 32 00 00"))
        self.basFile.write("%10i%10i   !iapart,istrt\n"%(0,1))
        iboundh=[1]*numberOfCells
	
        boundaryConditionsList = []
	#
	#  Velocity
	#
	if self.velmod < 1.e-20:
            if nrow>1:
                for column in range(0,ncol,1):
                    iboundh[column-1] = -1
                    iboundh[(nrow-1)*ncol+column-1] = -1
                    pass

            if ncol>1:
                for row in range(0,nrow,1):
                    iboundh[(row-1)*ncol] = -1
                    iboundh[(row-1)*ncol+ncol-1] = -1
                    pass
                pass
            
	else:
            if ((nrow>1) and abs(self.geschwin[1])>1.e-15):
    #        if nrow>1:
                for column in range(0,ncol,1):
                    iboundh[column-1] = -1
                    iboundh[(nrow-1)*ncol+column-1] = -1
                    pass

            elif  ((nrow>1) and (ncol==1)) :
                for column in range(0,ncol,1):
                    iboundh[column-1] = -1
                    iboundh[(nrow-1)*ncol+column-1] = -1
                    pass

            if ((ncol>1) and abs(self.geschwin[0])>1.e-15):
    #        if ncol>1:
                for row in range(0,nrow,1):
                    iboundh[(row-1)*ncol] = -1
                    iboundh[(row-1)*ncol+ncol-1] = -1
                    pass
                pass
            elif  ((ncol>1) and (nrow==1)):
                for row in range(0,nrow,1):
                    iboundh[(row-1)*ncol] = -1
                    iboundh[(row-1)*ncol+ncol-1] = -1
                    pass
                pass
        self.basFile.write("%10i%10i%20s%10i   !IBOUND\n"%(5,1,"("+str(ncol)+"I3)",-1))
        for i in range(0,len(iboundh)):
            self.basFile.write("%3i"%(iboundh[i]))
            if ((i+1)%ncol==0)and(i!=numberOfCells):
                self.basFile.write("\n")
		pass
	    pass
        self.basFile.write("%10s\n"%(999.99))
	
        self.basFile.write("%10i%10s%20s%10i   !HEAD\n"\
                            %(5,_fote104(1.e-0),ljust("("+str(ncol)+"E15.8)",25),4))
        if ((ncol>1) and abs(self.geschwin[0])>1.e-15):
	
            west_bo_m   = CartesianMesh2D("boundary west","XY")
            west_bo_m.setZone("boundary west",Index2D(1,1),Index2D(1,nrow))
	    
            boundaryConditionsList.append(Mt3dHeadBoundaryCondition(west_bo_m,'Dirichlet',Head(value=self.westHeadValue)))
#
            east_bo_m   = CartesianMesh2D("boundary west","XY")
            east_bo_m.setZone("boundary east",index_min = Index2D(ncol,1),index_max = Index2D(ncol,nrow))
            boundaryConditionsList.append(Mt3dHeadBoundaryCondition(east_bo_m,'Dirichlet',Head(value =self.eastHeadValue)))
#
        if ((nrow>1) and abs(self.geschwin[1])>1.e-15):
	
            south_bo_m   = CartesianMesh2D("boundary south","XY")
            south_bo_m.setZone("boundary south",index_min = Index2D(2,nrow),index_max = Index2D(ncol,nrow))
            boundaryConditionsList.append(Mt3dHeadBoundaryCondition(south_bo_m,'Dirichlet',Head(value =self.southHeadValue)))
#
            north_bo_m   = CartesianMesh2D("boundary north","XY")
            north_bo_m.setZone("boundary north",index_min = Index2D(2,1),index_max = Index2D(ncol,1))
            boundaryConditionsList.append(Mt3dHeadBoundaryCondition(south_bo_m,'Dirichlet',Head(value =self.northHeadValue)))
#
        ci = [0.]*numberOfCells
#
        for boundary in boundaryConditionsList:
	    ind_min = boundary.boundary.zones[0].getIndexMin().getValues()
	    ind_max = boundary.boundary.zones[0].getIndexMax().getValues()
	    realvalue = boundary.getValue().getValue()
            for i in range(ind_min[0],ind_max[0]+1,1):
                for j in range(ind_min[1],ind_max[1]+1,1):
                    ci[(j-1)*ncol+i-1]=realvalue
		    pass
		pass
		    
        for i in range(0,len(ci)):
            l = _fot158(ci[i])
            self.basFile.write("%s"%(_fot158(ci[i])))
            if ((i+1)%ncol==0)and((i+1)!=numberOfCells):
                self.basFile.write("\n")
		pass
	    pass
        self.basFile.write("\n%15s%10i%10s   !perlfn, nstp, tsmult\n\n"\
                            %(_fote158(3.e+9),1,_fote105(10.0)))
        self.basFile.close()
#
# End of the modhw.bas file
#	    
	if (os.path.isfile("modhw.bcf")):
	    os.remove('modhw.bcf')
        self.bcfFile = open("modhw.bcf",'w')
        self.bcfFile.write("%10i%10i\n"%(1,0))
        self.bcfFile.write("%3i\n"%(0))
	intfmtin = ncol
        fmtin = "("+str(ncol)+"E15.8)"
        self.bcfFile.write("%10i%10s%20s%10i   !Isotropy\n"\
                            %(11,_fote104(1.e-0),ljust(fmtin,20),4))
        por=[1.0]*nlay
        for i in range(0,nlay):
            self.bcfFile.write("%15s"%(por[i]))
            if (i+1)%intfmtin==0:
                self.bcfFile.write("\n")
		pass
	    pass
        self.bcfFile.write("\n")
	  
        self.bcfFile.write("%10i%10s%20s%20i   !Delr\n"\
                            %(11,_fote104(1.0e-0),ljust(fmtin,20),4))
			    
        delr1 = self.mesh.getAxis("X")
	
        for i in range(0,ncol):

            self.bcfFile.write("%15s"%(_fot158(delr1[i+1]-delr1[i])))
            if ((i+1)%ncol==0)and(i!=numberOfCells):
                self.bcfFile.write("\n")
		pass
	    pass
		
        self.bcfFile.write("%10i%10s%20s%10i   !Delcc\n"\
                            %(11,_fote104(1.e-0),ljust("("+str(nrow)+"E15.8)",20),4))
			    
        delc1=self.mesh.getAxis("Y")

        for i in range(0,nrow):
            self.bcfFile.write("%15s"%(_fot158(delc1[i+1]-delc1[i])))
            if ((i+1)%nrow==0)and(i!=numberOfCells):
                self.bcfFile.write("\n")
		pass
	    pass

        self.bcfFile.write("%10i%10s%20s%10i   !Conductivity\n"\
                            %(11,_fote104(1.e-0),ljust(fmtin,20),4))

        ind = 0
	per = [0]*numberOfCells
	for i in range(0,len(self.ibound)):
	    if self.ibound[i] == -1:
	        per[i] = 1.0
	    else:
	        per[i] = permeabilityField[ind]
	        ind+=1
	        
        for i in range(0,len(self.ibound)):
            self.bcfFile.write("%15s"%(per[i]))
            if (i+1)%intfmtin==0:
                self.bcfFile.write("\n")
		pass
	    pass
        self.bcfFile.write("\n")

        self.bcfFile.close()
        #
        # Now we define the well file: discharge / recharge used by Modflow
        #
	print " dbg mt3d: we write the well file "
	
	if self.fwel: 
	    self.wellFile = open("modhw.wel","w")
	    self.qwell = []
            nrow = self.mesh.getNbPoints("Y")-1
            ncol = self.mesh.getNbPoints("X")-1

	    ind = 0
	    #
	    # recharge coefficient
	    #
	    coef_emm = 1/self.dt
	    for i in range(1,ncol+1):
                for j in range(1,nrow+1):
                    k = (j-1)*ncol+i
		    if (self.ibound[k-1]==1):
		        self.qwell.append([1,i,j,coef_emm*0.01*(self.porosity_field_values_old[ind]-self.porosity_field_values[ind])])
		        ind+=1
		
#
# mxwell is the maximum number of wells treated within the stress period
#
# iwelcb is a flag for outputs. set to zero cell-by-cell flow terms will 
#
            self.wellFile.write("%10i%10i   !mxwell, iwelcb\n"\
                            %(len(self.qwell)+2,50))	    
#
# itmp: number of wells to  be used : It is set here to internal cells where 
# dw/dt can occur
#
            self.wellFile.write("%10i   !itmp\n"\
                            %(len(self.qwell)))
            for well in self.qwell:
	        self.wellFile.write("%10i%10i%10i%15.8e !itmp\n"%(well[0],\
	    						 well[2],\
							 well[1],\
							 well[3]))
            self.wellFile.write("%10i\n"\
                            %(-1))
            self.wellFile.close()
	    
	if (os.path.isfile("OUTF")):
	    os.remove("IOUTF")
        osStatus = system("which modflow.exe")
        raw_input(" we reached the osStatus")
        if osStatus<>0:
            raise Exception, "modflow.exe not found"
          
#        osStatus = system("modflow.exe < modf.fil")
#        def velocityWriter(Modflow_outputfile):
#	    import os
#	    print "modflow.exe < "+Modflow_outputfile
#	    os.system("modflow.exe < "+Modflow_outputfile)
#	    return
	#modflowpid = os.spawnlp(os.P_NOWAIT,system("modflow.exe < modf.fil"))
	#print " modflowpid",modflowpid
	#os.wait(modflowpid)
#	modflowexecution = thread.start_new_thread(velocityWriter,("modf.fil",))
	#modflowexecution.run()
	print " we try to get a new umt file"
	faden = Draht("modf.fil")
	faden.run()
	while faden.isAlive():
	    pass
	return None

    def setDarcyVelocity(self,dv):
        """
    	We define a Darcy velocity through its components over the domain. 
	    All porous medium parameters are set to standard values to set the velocity.
        """
        from string import ljust

#        print " hpor parameter",self.hpor
        self.file_fil=open("modf.fil",'w')
        if self.variablePorosityOption and self.velmod>1.e-20 and self.hpor == 1:

            self.file_fil.write("LIST 6 %25s\n",\
				"BAS 5  %25s\n",\
				"SIP 13 %25s\n",\
				"OC  14 %25s\n",\
				"WEL 15 %25s\n",\
				"BCF 11 %25s\n"\
				%(ljust("modhw.lst",25),\
				ljust("modhw.bas",25),\
				ljust("modhw.sip",25),\
				ljust("modhw.wel",25),\
				ljust("modhw.oc",25),\
				ljust("modhw.bcf",25)))
        else:
            print "mc dbg self.variablePorosityOption without wells"
            self.file_fil.write("LIST 6 %25s\n"\
				"BAS  5 %25s\n"\
				"SIP 13 %25s\n"\
				"OC  14 %25s\n"\
				"BCF 11 %25s\n"\
				%(ljust("modhw.lst",25),\
				ljust("modhw.bas",25),\
				ljust("modhw.sip",25),\
				ljust("modhw.oc",25),\
				ljust("modhw.bcf",25)))
	    self.file_fil.close()
        self.basFile=open("modhw.bas",'w')
	
        self.basFile.write("%s \n"%("Python Interface generated"))
        self.basFile.write("%s \n"%("Es war einmal ... nie vier"))
        
        ncol = self.mesh.getNbPoints("X")-1
        
        nrow = self.mesh.getNbPoints("Y")-1
           
        nlay = 1
	
	numberOfCells = ncol*nrow*nlay	    
        self.basFile.write("%10i%10i%10i%10i%10i   !nlay,nrow,ncol,nper,itmuni\n"\
                            %(nlay,nrow,ncol,1,4))
        if self.variablePorosityOption and self.fwel == "T":
            self.basFile.write("%s\n"%(" 11 12 00  0  0  0  0 00 19  0  0 22 00 00 00 00 00 00 00 00 00 32 00 00"))
        else:
            self.basFile.write("%s\n"%(" 11 00 00  0  0  0  0 00 19  0  0 22 00 00 00 00 00 00 00 00 00 32 00 00"))
        self.basFile.write("%10i%10i   !iapart,istrt\n"%(0,1))
        iboundh=[1]*numberOfCells
	#
	#  velocity vector
	#
        self.geschwin = dv.getValue()
        mod =  self.geschwin.magnitude()
        if mod < 1.e-20:
            if nrow>1:
                for i in range(0,ncol,1):
                    iboundh[i-1] = -1
                    iboundh[(nrow-1)*ncol+i-1] = -1
                    pass

            if ncol>1:
                for j in range(0,nrow,1):
                    iboundh[(j-1)*ncol] = -1
                    iboundh[(j-1)*ncol+ncol-1] = -1
                    pass
                pass
            
        else:
            if ((nrow>1) and abs(self.geschwin[1])>1.e-15):
#        if nrow>1:
                for i in range(0,ncol,1):
                    iboundh[i-1] = -1
                    iboundh[(nrow-1)*ncol+i-1] = -1
                    pass

            elif  ((nrow>1) and (ncol==1)) :
                for i in range(0,ncol,1):
                    iboundh[i-1] = -1
                    iboundh[(nrow-1)*ncol+i-1] = -1
                    pass

            if ((ncol>1) and abs(self.geschwin[0])>1.e-15):
    #        if ncol>1:
                for j in range(0,nrow,1):
                    iboundh[(j-1)*ncol] = -1
                    iboundh[(j-1)*ncol+ncol-1] = -1
                    pass
                pass
            elif  ((ncol>1) and (nrow==1)):
                for j in range(0,nrow,1):
                    iboundh[(j-1)*ncol] = -1
                    iboundh[(j-1)*ncol+ncol-1] = -1
                    pass
                pass

        self.basFile.write("%10i%10i%20s%10i   !IBOUND\n"%(5,1,"("+str(ncol)+"I3)",-1))
        for i in range(0,len(iboundh)):
            self.basFile.write("%3i"%(iboundh[i]))
            if ((i+1)%ncol==0)and(i!=numberOfCells):
                self.basFile.write("\n")
		pass
	    pass
        self.basFile.write("%10s\n"%(999.99))
        self.basFile.write("%10i%10s%20s%10i   !HEAD\n"\
                            %(5,_fote104(1.e-0),ljust("("+str(ncol)+"E15.8)",25),4))
        boundaryConditionsList = []
        length_x = self.delr[-1]-self.delr[0]
        length_y = self.delc[-1]-self.delc[0]

        print "grid dimensions x and y:",nrow,ncol,mod
        print "domain length:",length_x,length_y

        h0 = 1.e-20
        if ((ncol>1) and abs(self.geschwin[0])>1.e-15):
	
            west_bo_m   = CartesianMesh2D("boundary west","XY")
            west_bo_m.setZone("boundary west",Index2D(1,1),Index2D(1,nrow))
            l = h0 + self.geschwin[0]*length_x
	    self.westHeadValue = PhysicalQuantity(l,"m")
	    
            boundaryConditionsList.append(Mt3dHeadBoundaryCondition(west_bo_m,'Dirichlet',value = self.westHeadValue))
#
            east_bo_m   = CartesianMesh2D("boundary west","XY")
            east_bo_m.setZone("boundary east",index_min = Index2D(ncol,1),index_max = Index2D(ncol,nrow))
            self.eastHeadValue = PhysicalQuantity(h0,"m")
            boundaryConditionsList.append(Mt3dHeadBoundaryCondition(east_bo_m,'Dirichlet',self.eastHeadValue))
#
        if ((nrow>1) and abs(self.geschwin[1])>1.e-10):
	
            south_bo_m   = CartesianMesh2D("boundary south","XY")
            south_bo_m.setZone("boundary south",index_min = Index2D(2,nrow),index_max = Index2D(ncol,nrow))
	    self.southHeadValue = PhysicalQuantity(h0+self.geschwin[1]*length_y,"m")
            boundaryConditionsList.append(Mt3dHeadBoundaryCondition(south_bo_m,'Dirichlet',value =self.southHeadValue))
#
            north_bo_m   = CartesianMesh2D("boundary north","XY")
            north_bo_m.setZone("boundary north",index_min = Index2D(2,1),index_max = Index2D(ncol,1))
	    self.northHeadValue = PhysicalQuantity(h0,"m")
            boundaryConditionsList.append(Mt3dHeadBoundaryCondition(south_bo_m,'Dirichlet',value =self.northHeadValue))
#
        ci = [0.]*numberOfCells
#
        for boundary in boundaryConditionsList:
	    ind_min = boundary.boundary.zones[0].getIndexMin().getValues()
	    ind_max = boundary.boundary.zones[0].getIndexMax().getValues()
	    realvalue = boundary.getValue()
            for i in range(ind_min[0],ind_max[0]+1,1):
                for j in range(ind_min[1],ind_max[1]+1,1):
                    ci[(j-1)*ncol+i-1]=realvalue
		    pass
		pass
	        
        for i in range(0,len(ci)):
            l = ci[i]
            self.basFile.write("%s"%(_fot158(ci[i])))
            if ((i+1)%ncol==0)and((i+1)!=numberOfCells):
                self.basFile.write("\n")
		pass
	    pass
        self.basFile.write("\n")
#        self.basFile.write("%15s%10s%10s   !perlgn, nstp, tsmult"%(_fote150(3.e+4),_foti10(1),_fote105(20.0)))
        self.basFile.write("%10s%10s%10s   !perlen, nstp, tsmult\n"%("3.e+9","1","10.0"))
        self.basFile.close()
	#
	# modhw.bcf
	#
        self.bcfFile = open("modhw.bcf",'w')
        self.bcfFile.write("%10i%10i\n"%(1,0))
        self.bcfFile.write("%3i\n"%(0))
        intfmtin = ncol
        fmtin = "("+str(ncol)+"E15.8)"
        self.bcfFile.write("%10i%10s%20s%10i   !Isotropy\n"\
                            %(11,_fote104(1.e-0),ljust(fmtin,20),4))
        por=[1.0]*nlay
        for i in range(0,nlay):
            self.bcfFile.write("%15s"%(por[i]))
            if (i+1)%intfmtin==0:
                self.bcfFile.write("\n")
		pass
	    pass
        self.bcfFile.write("\n")
	  
        self.bcfFile.write("%10i%10s%20s%20i   !Delr\n"\
                            %(11,_fote104(1.0e-0),ljust(fmtin,20),4))
			    
        delr1 = self.mesh.getAxis("X")
	
        for i in range(0,ncol):

            self.bcfFile.write("%15s"%(_fot158(delr1[i+1]-delr1[i])))
            if ((i+1)%ncol==0)and(i!=numberOfCells):
                self.bcfFile.write("\n")
		pass
	    pass
		
        self.bcfFile.write("%10i%10s%20s%10i   !Delcc\n"\
                            %(11,_fote104(1.e-0),ljust("("+str(nrow)+"E15.8)",20),4))
			    
        delc1=self.mesh.getAxis("Y")

        for i in range(0,nrow):
            self.bcfFile.write("%15s"%(_fot158(delc1[i+1]-delc1[i])))
            if ((i+1)%nrow==0)and(i!=numberOfCells):
                self.bcfFile.write("\n")
		pass
	    pass
        kx=[1.0]*numberOfCells
        self.bcfFile.write("%10i%10s%20s%10i   !Conductivity\n"\
                            %(11,_fote104(1.e-0),ljust(fmtin,20),4))
        for i in range(0,len(kx)):
            self.bcfFile.write("%15s"%(kx[i]))
            if (i+1)%intfmtin==0:
                self.bcfFile.write("\n")
		pass
	    pass
        self.bcfFile.write("\n")

        self.bcfFile.close()
	#
	# oc file
	#
        self.file_oc=open("modhw.oc",'w')
        self.file_oc.write("%10i%10i%10i%10i   !Ihedfm, Iddnfm, Ihedun, Iddnun\n"%(6,6,0,0))
        self.file_oc.write("%10i%10i%10i%10i   !Incode, Ihddfl, Ibudfl, Icbcfl\n"%(0,1,0,1))
        self.file_oc.write("%10i%10i%10i%10i   !Hdpr, Ddpr, Hdsv, Ddsv\n"%(1,0,1,0))
        self.file_oc.close()
	
        self.file_sip=open("modhw.sip",'w')
        self.file_sip.write("%10d%10d   !MXITER NPARM\n"%(8000,5))
        self.file_sip.write("%10s%10s%10d%10s%10d\n"%(_fote104(0.5),_fote104(1.e-16),0,_fote104(1.e-17),100))
        self.file_sip.close()
 
#        def velocityWriter(Modflow_outputfile):
#	    import os
#	    print "modflow.exe < "+Modflow_outputfile
#	    os.system("modflow.exe < "+Modflow_outputfile)
#	    return
	#modflowpid = os.spawnlp(os.P_NOWAIT,system("modflow.exe < modf.fil"))
	#print " modflowpid",modflowpid
	#os.wait(modflowpid)
#	modflowexecution = thread.start_new_thread(velocityWriter,("modf.fil",))
	#modflowexecution.run()
        faden = Draht("modf.fil")
        faden.run()
        while faden.isAlive():
            pass
#	print " we reach this step "    
#	if (os.path.isfile('modhw.mod')):
#	    os.remove('modhw.mod')
#	#if (os.path.isfile('modhw.bas')):
#	    #os.remove('modhw.bas')
#	if (os.path.isfile('modhw.sip')):
#	    os.remove('modhw.sip')
#	if (os.path.isfile('modhw.bcf')):
#	    os.remove('modhw.bcf')
#	if (os.path.isfile('modhw.oc')):
#	    os.remove('modhw.oc')
#	if (os.path.isfile('IOUTF')):
#	    os.remove('IOUTF')
	    
	    return None

    def setGradient(self,scheme,residual):
        """
	Used to set the gradient method used to solve the implicit system
	"""
        if scheme=="JACOBI":
            self.isolve = 1
        elif scheme=="SSOR":
            self.isolve = 2
        elif scheme=="MIC":
            self.isolve = 3
        else:
            print "Warning, the method hasn't been recognized,"\
                  "the Jacobi default option has been taken"
            self.isolve = 1

        self.cclose = residual
	return
	
    def setInitialConcentration(self,concentrations):
        """
        Transfer of concentrations to Mt3d, The concentrations have been
	previously reorganized in a Mt3d structure form.
        """
        self.solver.setConcentration(concentrations)
	
    def setMesh(self, adelc, adelr):
        """ Allow to define the new position of points for meshing"""
        self.solver.setMesh(adelc,adelr)
	
    def headAdaption(self):
        self.solver.headadaption()
	
    def setPorosityField(self,porosityField):
        """
        That method is used to set the porosity field
                       
        """
        self.porosity_field_values_old = copy(self.porosity_field_values)
        self.porosity_field_values = copy(porosityField)
        self.solver.setPorosityField(porosityField)
	return None

    def setDiffusionValues(self,diffusionfield):
        """
        sets the diffusion field to Mt3d
                       
        Input  : a diffusion field in association to a cartesian mesh 
        """
        self.solver.setDiffusion(diffusionfield)
	return None
	
    def stop(self):
        """
        Used to stop the mt3d solver
        """
	Popen("rm -f MT3*.CNF MT3*.MAS MT3*.RES MT3*.UCN",  shell=True)
        print " mt3d stop method "
	self.solver.stop()
	self.stop = 1
	
    def end(self):
        """
        Used to stop the mt3d solver        
        """
	Popen("rm -f MT3*.CNF MT3*.MAS MT3*.RES MT3*.UCN",  shell=True)
	if self.stop == 0:
	    self.solver.stop()
	return None

    def go_step(self,dt,temps):
        """
        Transfer of concentrations to Mt3d, The concentrations have been
	previously reorganized in a Mt3d structure form
        """
        return self.solver.gostep(dt,temps)

    def AqueousComponentOneTimeStep(self):
        """
        This method enables to make one time step within transport
        """
        return self.solver.AqueousComponentOneTimeStep()

    def setRegions(self,regions):
    
        """
        This method is used to build up the btn file with regions list
        """
        self.regions = regions

    def setTimeStep(self,dt):
    
        """
        Setting the transport time step
        """
        self.dt = dt
	self.solver.dt(self.dt)
	
    def setBoundaryConditions(self,BoundaryConditions):
    
        """
        This method is used to build up the btn file with regions list
        """
        self.BoundaryConditions = BoundaryConditions
	
    def getBoundaryConditions(self):
    
        """
        This method is used to build up the btn file with regions list
        """
        return self.BoundaryConditions
	
    def getBoundaryConditionTimeVariation(self,boundaryConditionTimeVariation):
    
        """
        This method is used to retrieve for the algorithm the times BC variations
	We just have a control on list elements membership
        """
        if type(boundaryConditionTimeVariation) != ListType:
            raise TypeError, " the boundaryConditionTimeVariation argument must be a list "        
	
	for element in boundaryConditionTimeVariation:
	    if type(element) != TupleType:
	        raise TypeError, " element must be a tuple "	
	    if type(element[0]) != floatType:	
	        raise TypeError, " element[0] must be a float "	
	    if type(element[1]) != ListType:	
	        raise TypeError, " element[1] must be a list "	
	    for i in element[1]:
	        #self.kontrolle(element[1][0]	.__class__.__name__,'BoundaryCondition')
	        if type(i[1]) != ListType:	
	                raise TypeError, " i[1] must be a list"	
		for concentration in i[1]:
		
	            if type(concentration) != floatType:	
	                raise TypeError, " concentrations must be floats"	
	            	
	self.timeBoundaryConditionVariation = boundaryConditionTimeVariation
        return
    #
    # variable diffusion as a function of porosity
    #
    def getEffectiveDiffusionValues(self):
        """
        Access to the effective diffusion values as a list of floats at time t.
	An instance of Mt3d has already been created and initialised
        """
        return self.dif
    #
    # variable diffusion as a function of porosity
    #
    def getInternalEffectiveDiffusionValues(self):
        """
        Access to the effective diffusion values as a list of floats at time t. This supposes that
	an instance of Mt3d has already been created and initialised
        """
	
        return self.solver.getDiffusion()
	
    def setBoundaryConditionsTimeVariation(self,current_time):
    
        """
        This method is used to set the time variation. The parameter current time,
	is the time  BC variation occurence	
        """
	# we treat now the list of tuples (BC,values)
	#print  self.timeBoundaryConditionVariation
	if self.timeBoundaryConditionVariation != []:
	    #print "dbc mc list not empty "
	    statesConsidered = self.timeBoundaryConditionVariation[0][1]
	    #print "dbg mc in setBoundaryConditionsTimeVariation",statesConsidered
	# On verifie qu'i n'y a pas d'erreur dans l'algorithme
	    atTime = self.timeBoundaryConditionVariation[0][0]
	    #print "dbg mc  at Time",atTime
	    #print "dbg mc  at Time",current_time
	    if abs(current_time-atTime) > 1.e-7:
	        return
            else:
		#print " we treat a boundary condition "
	        pass

	    for boundary in statesConsidered:
                ind_min = boundary[0].boundary.zones[0].getIndexMin()
                ind_max = boundary[0].boundary.zones[0].getIndexMax()
	        #print "dbg mc  at Time",ind_min,ind_max
	        listOfConcentrations = boundary[1]
		#print "dbg listOfConcentrations",listOfConcentrations
	        if len(listOfConcentrations) == self.componentsNumber:
	            self.setBoundaryCondition(listOfConcentrations,ind_min.i,ind_max.i,ind_min.j,ind_max.j)
	        else:
	            raise " Discrepancy between the initial number of components and the number of components ", \
	    	      "to be introduced at time "+str(current_time  )
	        pass
	#
	# On detruit l'instant qui vient d'etre traitee
	# 
	    self.timeBoundaryConditionVariation.__delitem__(0)
	    pass
	
        pass

    def setPorosityOption(self,variablePorosityOption):
        self.variablePorosityOption = variablePorosityOption
    	
    def setData(self,mesh,variables,name=None,velocity=None,rank = None):
    
        from string import ljust

        self.mesh = mesh
        self.variables = variables
	
	self.qwell = []
	
	if rank == None:
 	    rank = ""
	else:
	    rank = str(rank)        
        if name!=None:
	    #print " Mt3dName",name
	    self.name= name.replace(' ','_')
	    self.setupfile = self.name+rank+".fil"
        #print "*"*81,"\n"
        #print "Mt3d.setData\n"
        #print variables
        #print "*"*81,"\n"
        variables = list(variables)
        for spezien in variables:
            if not isinstance(spezien,Species):
                raise Exception, "not all variables are right defined"
        self.variables = variables
 
        self.adv = "T"

	if isinstance(velocity,Velocity):
	    self.velmod = 0.
	    self.velmod = velocity.getValue().magnitude()
        dsp = "T"
        self.ssm = "T"
        rct = "F"
        gcg = "T"
	
        self.nom_fichier_fil = self.setupfile
	prefix = "modhw_"+str(rank)
        self.btnFileName = prefix+self.name+".btn"
        #self.nom_fichier_rct = "modhw_"+self.name+".rct"
        self.dspFileName = prefix+self.name+".dsp"
        self.ssmFileName = prefix+self.name+".ssm"
        self.ocFileName  = prefix+self.name+".oc"
        self.advFileName = prefix+self.name+".adv"
        self.gcgFileName = prefix+self.name+".gcg"
        self.outFileName = prefix+self.name+".out"
	self.setDefaultParameter(self.advFileName,self.gcgFileName)

        self.file_fil=open(self.nom_fichier_fil,'w')
        self.file_fil.write("%25s\n"%(ljust(self.outFileName,25)))
        self.file_fil.write("%25s\n"%(ljust(self.btnFileName,25)))
        if self.adv=="T":
	    self.file_fil.write("%25s\n"%(ljust(self.advFileName,25)))
        self.file_fil.write("%25s\n"%(ljust(self.dspFileName,25)))
        self.file_fil.write("%25s\n"%(ljust(self.ssmFileName,25)))
        #self.file_fil.write("%25s\n"%(ljust(self.nom_fichier_rct,25)))
        self.file_fil.write("%25s\n"%(ljust(self.gcgFileName ,25)))
        self.file_fil.write("%25s\n"%(ljust("Monod.umt",25)))
        self.file_fil.write("%s\n"%(ljust("n",25)))
        self.file_fil.close()
#
# btn file opening, that file contains information about meshing, initial and bound. conditions...
#
        self.btnFile = open(self.btnFileName,'w')
        self.btnFile.write("%25s\n"%(ljust(self.name,80)))
#
# Input Instructions for the basic transport package: Monod.btn
#
        self.btnFile.write("%s \n"%(self.name))
        #print " title",self.name
        ncol = self.mesh.nb_of_intervals[0]
        nlay = 1
        nrow = self.mesh.nb_of_intervals[1]
        numberOfCells = ncol*nrow*nlay
        #print " title",self.name,ncol,nrow
        # Nper is the number of stress simulations
        nper=1
        # Number of mobile concentrations
        mcomp = len(variables)
        ncomp = mcomp
	#
	# we retrieve the number of components
	#
	self.componentsNumber = mcomp
	#
        #print " valeur de nrow ncol ",nrow,ncol
        self.btnFile.write("%10i%10i%10i%10i%10i%10i   !nlay,nrow,ncol,nper,ncomp,mcomp\n"\
                            %(nlay,nrow,ncol,nper,ncomp,mcomp))
        #Units to declare, used only as postprocessing data
        tunit = "DAY"
        lunit = "M"
        munit = "KG"
        istrt = 1
        self.btnFile.write("%4s%4s%4s   !Tunit,Lunit,Munit\n"%(tunit,lunit,munit))
        mcomp = len(variables)
        self.btnFile.write("%2s%2s%2s%2s%2s    !adv,dsp,ssm,rct,gcg\n"%(self.adv,dsp,self.ssm,rct,gcg))
        # Introduction of delr
        # We suppose the model is confined by taking laycon to zero
        comment = "                                          !LAYCON"
        self.btnFile.write("%10i%50s\n"%(0,comment))
        #fmtin = "(15E15.8)"
        fmtin = "("+str(ncol)+"E15.8)"
        self.delz = array([1.0], Float)
        self.btnFile.write("%10i%10s%20s%10i   !Delr n\n"\
                            %(100,_fote104(1.),ljust(fmtin,20),4))
        # Here we write the size of each element in the X direction
        delr_old= self.mesh.getAxis("X").tolist()
        #print delr_old
        #print type(delr_old)
        #raw_input()

        delr = [0.0]*ncol
        delr[0] = delr_old[1]
        for i in range(1,ncol):
            delr[i]=delr_old[i+1]-delr_old[i]
	    
	self.delr = delr_old[1:]
	#print self.delr
        #raw_input()

        for i in range(0,ncol):
            self.btnFile.write("%15s"%(_fot158(delr[i])))
            if ((i+1)%ncol==0)and(i!=numberOfCells):
                self.btnFile.write("\n")
#            if (i+1)%15==0:
#                 self.btnFile.write("\n")
        fmtin = "("+str(nrow)+"E15.8)"
        self.btnFile.write("%10i%10s%20s%10i   !Delc\n"\
                            %(100,_fote104(1.e+00),ljust(fmtin,20),4))
        #
        # Here we write the size of each element in the Y direction
        #
        delc = [0.0]*nrow
        delc_old=self.mesh.getAxis("Y").tolist()
	self.delc = delc_old[1:]
        for i in range(0,nrow):
            delc[i]=delc_old[i+1]-delc_old[i]
            #print " delc",i,delc[i-1],delc[i]
	self.delc = delc_old[1:]	    
	
        for i in range(0,nrow):
            self.btnFile.write("%15s"%(_fot158(delc[i])))
            if ((i+1)%nrow==0)and(i!=numberOfCells):
                self.btnFile.write("\n")
            #if (i+1)%15==0:
                 #self.btnFile.write("\n")
        #self.btnFile.write("\n")
        #
        # Here we write the size of the layer: Htop
        #
        htop = 1.0
        self.btnFile.write("%10s%10f   !htop\n"%("0",htop))
        #
        # Here we write the size of the layer: dz
        #
        dz = 1.0
        self.btnFile.write("%10s%10f   !dz\n"%("0",dz))
        #
        # Here we write the porosity of the medium, it is set to one
        #
	fmtin = "("+str(ncol)+"E15.8)"
	
        self.btnFile.write("%10i%10s%20s%10i   !Porosity\n"\
                            %(100,_fote104(1.e+00),ljust(fmtin,20),4))
#
## Here, we introduce perhaps a limitation on the porosity treatment, the
## affectation thereafter imposes a porosity of one on the boundary.
## We have omitted to consider the treatment of porosity on boundaries
#
        poros=[1.0]
        print " nrow ncol ",nrow,ncol
        poros = poros*numberOfCells
#        list_regionc = self.getRegions()
        list_regionc = self.getRegions()

        for nom_region in list_regionc:
            porosity = nom_region.material.getPorosity().value
            ind_min = nom_region.support.zones[0].getIndexMin()
            ind_max = nom_region.support.zones[0].getIndexMax()
	    i1 = ind_min.i
	    i2 = ind_max.i
	    j1 = ind_min.j
	    j2 = ind_max.j
            for i in range(i1,i2+1,1):
                for j in range(j1,j2+1,1):
                     k = (j-1)*ncol+i
                     #print " k value ",k,porosity
                     poros[k-1]=porosity
        for i in range(0,numberOfCells):
             self.btnFile.write("%15s"%(poros[i]))
             if (i+1)%ncol==0:
                self.btnFile.write("\n")
		
        # Ibound designates the way the cells are treated
        # -1 for a Dirichlet boundary cell
        # +1 for a live or a well cell
        self.ibound=[1]
        self.ibound = self.ibound*numberOfCells
	
	
	listOfBoundaries = self.getBoundaryConditions()
        for boundary in listOfBoundaries:
	    
	    if (boundary.btype=='Dirichlet'):
	        ind_min = boundary.boundary.zones[0].getIndexMin()
                ind_max = boundary.boundary.zones[0].getIndexMax()
	        i1 = ind_min.i
	        i2 = ind_max.i
	        j1 = ind_min.j
	        j2 = ind_max.j
		print " mt3d dbg b.l. treat ",i1,i2,j1,j2
                for i in range(i1,i2+1,1):
                    for j in range(j1,j2+1,1):
                        k = (j-1)*ncol+i
                        self.ibound[k-1] = -1
		    pass
		pass
        # fmtin is the read format
	 #	
         # We treat cells with no flow by imposing inactive cells where porosity is zero
	 #
        for nom_region in list_regionc:
            porosity = nom_region.material.getPorosity().value
	    if (porosity<1.e-15):
	        print "porosity value 1",porosity
                ind_min = nom_region.support.zones[0].getIndexMin()
                ind_max = nom_region.support.zones[0].getIndexMax()
	        i1 = ind_min.i
	        i2 = ind_max.i
	        j1 = ind_min.j
	        j2 = ind_max.j
                for i in range(i1,i2+1,1):
                    for j in range(j1,j2+1,1):
                         k = (j-1)*ncol+i
                         self.ibound[k-1]=0
	 
        fmtin = "("+str(ncol)+"I3)"
        self.btnFile.write("%10i%10i%20s%10i   !ibound\n"%(1,1,fmtin,-1))
        for i in range(0,len(self.ibound)):
            self.btnFile.write("%3i"%(self.ibound[i]))
            if (i+1)%ncol==0:
                self.btnFile.write("\n")
#        self.btnFile.write("\n")
        #print "-"*81,"\n"
#        print " nom des variables ",variables
        #print "-"*81,"\n"
#        for i in variables:
#            print "Nom: ",type(i)
        fmtin = "("+str(ncol)+"E15.8)"

        #   self.btnFile.close()

        #   fmtin is the read format 
#        fmtin = "(15E15.8)"
        fmtin = "("+str(ncol)+"E15.8)"

        ##print "*"*81,"\n"
	##print boundary_list
        ##print "*"*81,"\n"
        _initFunction(list_regionc,self.mesh, listOfBoundaries, variables,self.btnFile,fmtin)
        self.ncol = mesh.nb_of_intervals[0]
        self.nrow = mesh.nb_of_intervals[1]
	
        #print "-"*81,"\n"
	#print " valeur de nrow et ncol ",self.nrow,self.ncol
        #print "-"*81,"\n"
        #   CINACT is set to -999.99 and THKMIN to zero
        self.btnFile.write("%10s%10s      !Cinact, Thkmin\n"%(-999.99,0))
        self.btnFile.write("%10i%10i%10i%10i%10s      !Ifmtcn, Ifmtnp, Ifmtrf, Ifmtdp, Savucn  \n"\
        %(0,0,0,0,"F"))
        # perlen is the length of the stress period considered
        perlen=9.e+9
        nstp=200
        tsmult=1.0
        self.btnFile.write("%10i   !nprs\n"%(0))
        self.btnFile.write("%10i%10i   !nobs nprobs\n"%(0,0))
        self.btnFile.write("%10s%10i   !chkmas nprmas\n"%("F",0))
#     3.E+8       100        1.             !PERLEN,NSTP,TSMULT
#    2.5E+5     55000       1.1         0   !DT0,MXSTRN,TTSMULT,TTSMAX
        self.btnFile.write("%10s%10i%10s   !perlen, nstp, tsmult\n"\
                            %(_fot100(perlen),100,_fot100(tsmult)))
        self.btnFile.write("%10s%10i%15s%10i   !dt0, mxstrn, ttsmult, ttsmax\n"\
                            %(_fot100(2.E+8),99000,_fote158(1.1),0))
        self.btnFile.close()
	print " btn file writing process is oK"
        #
        # Treatment of the dispersion package
	# Reference paragraph 6.6 page 6.29
        # the file has the extension .dsp
        #
        # Opening of the dsp file
        self.dspFile=open(self.dspFileName,'w')

        self.dspFile.write("%10i%10s%20s%10i   !Longitudinal Dispersivity\n"\
                            %(100,_fote104(1.e+00),ljust(fmtin,20),4))
        #
        # Let's consider longitudinal dispersivity
        #
        dis=[0.0]
        dis = dis*numberOfCells
	#
        # Creation of the dispersion table
	#	
        list_regionc = self.getRegions()
        for nom_region in list_regionc:
            if isinstance(nom_region.material.getKinematicDispersion(),KinematicDispersion):
	        longitudinal_dispersivity = nom_region.material.getKinematicDispersion().value[0]
	    else:
	    	longitudinal_dispersivity = 0.
            ind_min = nom_region.support.zones[0].getIndexMin()
            ind_max = nom_region.support.zones[0].getIndexMax()
	    i1 = ind_min.i
	    i2 = ind_max.i
	    j1 = ind_min.j
	    j2 = ind_max.j
	    print " i1 i2 j1 j2 ",i1,i2,j1,j2
            for i in range(i1,i2+1,1):
                for j in range(j1,j2+1,1):
                     k = (j-1)*ncol+i
                     dis[k-1]=longitudinal_dispersivity
#		     print " dis[k-1]",k-1,dis[k-1]
        for i in range(0,numberOfCells):
            self.dspFile.write("%15s"%(_fot158(dis[i])))
            if ((i+1)%ncol==0)and(i!=numberOfCells):
                self.dspFile.write("\n")
        #
        # Let's consider transverse dispersivity
        #
        for nom_region in list_regionc:
            if isinstance(nom_region.material.getKinematicDispersion(),KinematicDispersion):
            
                transverse_dispersivity = nom_region.material.getKinematicDispersion().value[1]
	    else:
                transverse_dispersivity = 0.
	    
            ind_min = nom_region.support.zones[0].getIndexMin()
            ind_max = nom_region.support.zones[0].getIndexMax()
            for i in range(0,nlay):
	        if (longitudinal_dispersivity>1.e-10):
		    #
		    # This has to stay in this form
		    #
                    dis[i]=transverse_dispersivity/longitudinal_dispersivity
                    #dis[i]=transverse_dispersivity
		else:
                    dis[i]=0.
	
        self.dspFile.write("%10i%10s%20s%10i   !Transverse Dispersivity\n"\
                            %(100,_fote104(1.e+00),ljust(fmtin,20),4))

        for i in range(0,nlay):
            self.dspFile.write("%15s"%(_fot158(dis[i])))
            if ((i+1)%nlay==0)and(i!=numberOfCells):
                self.dspFile.write("\n")
         
        self.dspFile.write("%10i%10s%20s%10i   !Vertical Transverse Dispersivity\n"\
                            %(100,_fote104(1.e+00),ljust(fmtin,20),4))
        for i in range(0,nlay):
            self.dspFile.write("%15s"%(_fot158(0.0)))
            if ((i+1)%nlay==0)and(i!=numberOfCells):
                self.dspFile.write("\n")

        #
        # Treatment of the dispersion package
        #
        self.dspFile.write("%10i%10s%20s%10i   !Pore Diffusion\n"\
                            %(100,_fote104(1.e+00),ljust(fmtin,20),4))

        self.dif = [1.0]*numberOfCells
	#
        # Creation of the diffusion table
	#
        for nom_region in list_regionc:
	    if isinstance(nom_region.material.getEffectiveDiffusion(),EffectiveDiffusion):
                effective_diffusion = nom_region.material.getEffectiveDiffusion().value.value
	    else:
                effective_diffusion = 0.0

            porosity_region = nom_region.material.getPorosity().value
	    ind_min = nom_region.support.zones[0].getIndexMin()
            ind_max = nom_region.support.zones[0].getIndexMax()
	    i1 = ind_min.i
	    i2 = ind_max.i
	    j1 = ind_min.j
	    j2 = ind_max.j
            print " porosity_region ",porosity_region,i1,i2,j1,j2
            for i in range(i1,i2+1,1):
                for j in range(j1,j2+1,1):
                    k = (j-1)*ncol+i
                    self.dif[k-1]=effective_diffusion/porosity_region
#
# Ici, on donne a la cellule inactive la diffusion de la cellule voisine. Ceci ne peut marcher
# qu'en 1 dimension d'espace.
#
        for i in range(0,numberOfCells):
            self.dspFile.write("%15s"%(_fote158(self.dif[i])))
            if ((i+1)%ncol==0)and(i!=numberOfCells):
                self.dspFile.write("\n")
        self.dspFile.write("\n") 
        self.dspFile.close()
	print " mt3d dbg end of the dsp file"
        #
        # Treatment of the reaction package: We do not introduce any sorption:
	# Reference paragraph 6.8 page 6.35
        #
        #self.file_rct=open(self.nom_fichier_rct,'w')
        #self.file_rct.write("%10i%10i   !Isothm, Ireact\n"%(0,0)) 
        #self.file_rct.close()
        #
        # Treatment of the Sink and Source Mixing package:
	# Reference paragraph 6.7 page 6.30
        # We eventually have flux boundary conditions, they are handled through the fwel mt3d package.
        #
        for boundary in self.BoundaryConditions:
            if (boundary.btype=='Flux'):
                self.fwel = "T"
		self.qwell = []
                break
            pass 
	self.iboundf = [1]*numberOfCells
	print "  mt3d dbg ssm ouverture du fichier 2108"
	self.ssmFile=open(self.ssmFileName,'w')
	print "  mt3d dbg ssm ecriture des booleens dont self.fwel",self.fwel
        self.ssmFile.write(self.fwel+" F F F F F    !fwel, fdrn, frch, fevt, friv, fghb\n") 
	
        if (self.fwel == "F"):
            self.ssmFile.write("%10i\n"%(3200)) 
            self.ssmFile.write("%10i\n"%(0)) 
            self.ssmFile.close()
	    print "self.fwel == \"F\""
            pass
        elif (self.fwel == "T") and not(self.variablePorosityOption):
	    print "mt3d self.fwel == \"T\""
	    ind = 0
            for boundary in listOfBoundaries:
		
	        if (boundary.type.lower()=='flux'):
	            indMin = boundary.boundary.zones[0].getIndexMin()
                    indMax = boundary.boundary.zones[0].getIndexMax()
	            i1 = indMin.i
	            i2 = indMax.i
	            j1 = indMin.j
	            j2 = indMax.j
                    for i in range(i1,i2+1,1):
                        for j in range(j1,j2+1,1):
                            k = (j-1)*ncol+i
			    self.iboundf[k-1] = -1
			    ind+=1
			    string = ""
			    for spezien in boundary.getValue().aqueousSolution.elementConcentrations:
			        string+=" "+str(spezien.getValue())
				pass
		            self.qwell.append([1,i,j,string])
		        pass
		    pass
	    self.nwell = ind
            self.ssmFile.write("%10i    !Mxss\n"%(ind*2)) 
            self.ssmFile.write("%10i    !Nss\n"%(ind))
	    #print "in qwell ",qwelle
            for well in self.qwell:
	        #self.ssmFile.write("%10i%10i%10i%s%10i !itmp\n"%(well[0],well[2],well[1],string,2))
	        self.ssmFile.write("%10i%10i%10i%10f%10i%s !itmp\n"%(well[0],well[2],well[1],0.,2,well[-1]))
		
	    self.ssmFile.write("%10i\n"%(0))
            self.ssmFile.close()
	    self.ipermut = []
	    ind = 0
	    for i in range(0,numberOfCells):
	        if self.iboundf[i] == -1:
	            self.ipermut.append(numberOfCells-self.nwell+ind)
		    ind+=1
		else:    
	            self.ipermut.append(i-ind)
		    
#	        print " plot permutation ",i,self.ipermut[i]
            pass
        else:
            self.ssmFile.write("%10i    !Mxss\n"%(3202))
	    iaux = 0
	    for i in self.ibound:
	        if i == 1:
		    iaux+=1 
            self.ssmFile.write("%10i    !Nss\n"%(53))
	    conc_eau = " 0.000000003653824 111.050650400     55.5253251970"
	    for i in range(3,self.componentsNumber):
	        conc_eau+=" 0.000000000000"

            for region in list_regionc:
                indMin = region.support.zones[0].getIndexMin()
                indMax = region.support.zones[0].getIndexMax()
	        i1 = indMin.i
	        i2 = indMax.i
	        j1 = indMin.j
	        j2 = indMax.j
                for i in range(i1,i2+1,1):
                    for j in range(j1,j2+1,1):
                        k = (j-1)*ncol+i
			if self.ibound[k-1] == 1:
		            self.ssmFile.write("%10i%10i%10i%10f%10i%s !itmpss\n"%(1,j,i,0.,2,conc_eau))


	    
#	        print "%10i%10i%10i%s%10i !itmp\n"%(well[0],well[2],well[1],string,2)
	        #self.ssmFile.write("%10i%10i%10i%s%10i !itmp\n"%(well[0],well[2],well[1],string,2))
#	        self.ssmFile.write("%10i%10i%10i%10f%10i%s !itmp\n"%(well[0],well[2],well[1],0.,2,well[-1]))
#	        if self.ibound[i]==1:
#		    self.ssmFile.write("%10i%10i%10i%10f%10i%s !itmps\n"%(1,1,i,0.,2,conc_eau))
	    self.ssmFile.write("%10i\n"%(0))
            self.ssmFile.close()
#	    print " dbg mt3d dbg the ssm is closed"
        #
	print " the setData method is over"
	return None

    def getMesh(self):

        return self.mesh

    def setDefaultParameter(self,Monodadv,Monodgcg):
        """
        We give here the two files bounded to advection discretisation parameters 
        and solver parameters
        """

        self.monodadv = Monodadv
        self.monodgcg = Monodgcg
        self.tinitial = 0.0
        self.tfinal = 1.e+9
        #
        # Treatment of the Advection Package:
	# Reference paragraph 6.5 page 6.24
        #
# mixelm :  Integer flag for the solver option
#           set to zero we use an upwind scheme or a central scheme depending
#           on the nadvfd value
#	    nadvfd = 0 or 1, upstream weighting
#	    nadvfd = 2, central-in-space weighting
#
        self.mixelm = 0
#
# percel : Is the Courant Friedrich Levy Number
#
        self.percel = 1.0
#
# mxpart : Is the number of particules: we will not use this Mt3d option
#
        self.mxpart = 0
#
# nadvfd : which scheme to be used with an implicit scheme
#    2 central in space
#    0/1 upwind
        self.nadvfd = 0
#
# Relative cell gradient below which advective terms are neglected
#
        self.dceps=1.e-20      
#
# The following parameters are set to a constant, they should be used with a particle method
#
        self.dchmoc = 1.0
        self.itrack = 1
        self.interp = 1
        self.nlsink = 1
        self.nph    = 0
        self.nplane = 1
        self.npl    = 0
        self.npmax  = 0
        self.npmin  = 0
        self.npsink = 1
        self.wd     = 0.5
        #
        # Treatment of the Gradient Conjuguate Solver:
	# Reference paragraph 6.9 page 6.39
        #
        # mxiter is the maximum of outer iterations of the gradient solver
        # a value of one is recommended.
        self.mxiter = 1
        # iter1 is the maximum of inner iterations of the gradient solver
        # a  value of 30-50 is recommended
        self.iter1 = 80
        #
        # isolve is the type of preconditioners
        #
        #   ISOLVE: 1 Jacobi
        #   ISOLVE: 2 SSOR
        #   ISOLVE: 3 Modified Incomplete Cholesky
        #
        self.isolve = 3
        #
        # ncrs: treatment of dispersion 0 for a lumped tensor
        #
        self.ncrs = 1
        self.accl = 1.0
        self.cclose = 1.0
        self.iprgcg = 0

    def getIndexSubMesh(self,regionName):
        """
        This method is used to supply a porosity list to the chemistry code Phreeqc which is 
        working with a current number of moles per liter of solution 
        """
        indMin = regionName.support.zones[0].getIndexMin()
        indMax = regionName.support.zones[0].getIndexMax()
	i1 = indMin.i
	i2 = indMax.i
	j1 = indMin.j
	j2 = indMax.j
	return i1, i2, j1 , j2
	
    def getMeshExtent(self):
        """
        Returns the mesh extansion over each direction
        """
        return [self.nrow,self.ncol,1]
	

    def getPorosityValues(self):
        """
        This method is used to supply a porosity list to the chemistry code Phreeqc which is 
        working with a current number of moles per liter of solution 
        """
        self.porosity_field_values = [1.0]*self.nrow*self.ncol
        for region in self.getRegions():
            porosity = region.material.getPorosity().value
            i1, i2 , j1 , j2 = self.getIndexSubMesh(region)
            for i in range(i1,i2+1,1):
                for j in range(j1,j2+1,1):
                     self.porosity_field_values[(j-1)*self.ncol+i-1]=porosity
	for boundary in self.BoundaryConditions:
            if (boundary.btype=='Dirichlet'):
	        ind_min = boundary.boundary.zones[0].getIndexMin()
                ind_max = boundary.boundary.zones[0].getIndexMax()
	        i1 = ind_min.i
	        i2 = ind_max.i
	        j1 = ind_min.j
	        j2 = ind_max.j
                for i in range(i1,i2+1,1):
                    for j in range(j1,j2+1,1):
		        self.porosity_field_values[(j-1)*self.ncol+i-1] = -1
	for i in range(self.nrow*self.ncol-1,-1,-1):  
	    if self.porosity_field_values[i] == -1:
	        self.porosity_field_values.__delitem__(i)
        self.porosity_field_values_old = copy(self.porosity_field_values)
        porosity_field = copy(self.porosity_field_values)
#
# Necessity to return a specific field, problem of pointers
#	
	return porosity_field

    def setParameter(self, value):
	"""
	Defines numerical parameters related to discretization
	"""
	i = 0
	schematta = 0
	while i < len(value):

            scheme = str(value[i]).upper()
	    if scheme.replace(".","")=="TVD":
                self.mixelm = -1
		schematta = 1
		print "TVD "
	    # this parameter is not used with a TVD scheme :
                self.nadvfd = 2
            elif scheme=="CENTRAL":
                self.mixelm = 0
                self.nadvfd = 2
		schematta = 1
		print "CENTRAL "
            elif scheme=="UPWIND":
                self.mixelm = 0
                self.nadvfd = 0
		schematta = 1
		print "UPWIND "
            elif scheme=="JACOBI":
                self.isolve = 1
                self.cclose = value[i+1]
		i+=1
		print 'JACOBI'
            elif scheme=="SSOR":
                self.isolve = 2
                self.cclose = value[i+1]
		i+=1
            elif scheme=="MIC":
                self.isolve = 3
                self.cclose = value[i+1]
		i+=1
	    i+=1	

        if (schematta==0):
            print "Warning, the scheme hasn't been recognized,"\
                  "the upwind default option has been taken"
            self.mixelm = 0
            self.nadvfd = 0
            self.isolve = 1
            self.cclose = 1.e-20
	#print "220103 residual ",self.cclose

    def advectionParametrisation(self):
#        monodadv = self.monodadv
#        file = self.monodadv

        self.advFile = open(self.advFileName,'w')
        self.advFile.write("%10d%10.1f%10d%10d   !mixelm,percel,mxpart,nadvfd\n"\
                                %(self.mixelm,self.percel,self.mxpart,self.nadvfd))
        self.advFile.write("%10d%10.0f  !itrack,wd\n"%(self.itrack,self.wd))
        self.advFile.write("%10s%10d%10d%10d%10d%10d !dceps,nplane,npl,nph,npmin,npmax\n"\
                            %(_fote106(self.dceps),self.nplane,self.npl,\
                            self.nph,self.npmin,self.npmax))
        self.advFile.write("%10d%10d%10d !interp,nlsink,npsink\n"\
                            %(self.interp,self.nlsink,self.npsink))
        self.advFile.write("%10.1f !dchmoc\n"\
                            %(self.dchmoc))
        self.advFile.close()

        monodgcg = self.monodgcg
        self.gcgFile = open(monodgcg,'w')
        self.gcgFile.write("%10d%10d%10d%10d   !mxiter,iter1,isolve,ncrs\n"\
                                %(self.mxiter,self.iter1,self.isolve,self.ncrs))
        self.gcgFile.write("%10s%10s%10d  !accl, cclose, iprgcg\n"\
                            %(_fote158(self.accl),_fote158(self.cclose),0))
        self.gcgFile.close()

    def kontrolle(a,argument,comment = None):
        if type(a).__name__ != argument:
	    if (comment!=None): print comment
	    message = " error in the type of data to analyse, instead of a "+str(argument)+" you use a "
            raise message+str(type(a).__name__)

class Draht(Generic):
    def __init__(self,modfile):
        Generic.__init__(self)

        print " dbg Draht init 08/2010 launching",modfile

	self.mod = modfile
	self.T = threading.Thread(target = self.velocityWriter,args=())
	self.T.setName("Draht")

    def start(self):
        print " Draht start "
        self.T.start()
        return None

    def run(self):
        print " Draht run "
        self.T.run()
        return None

    def isAlive(self):
        return self.T.isAlive()

    def velocityWriter(self):
        retcode = Popen("$WRAPPER/Modflow/bin/modflow96", shell=True)
        if retcode < 0:
            print "Child was terminated by signal", -retcode
        else:
            print "Child returned", retcode
        return None

class Mt3dHeadBoundaryCondition(Generic):
    """
    BoundaryCondition class used to define a darcy velocity
    """
    
    def __init__(self, boundary, btype,value = None,  velocity = None, flowRate = None,timeVariation = None):
        """constructor with :
        - boundary : an object associated to a cartesian Mesh
        - type :  string. Could be 'Dirichlet','Flux','Mixed','Neumann'
        - OPTIONAL :
        --> value : a PhysicalQuantity or a list of couple (PhysicalQuantity,species)
                    or a  ChemicalState
        --> velocity :		object Velocity
        --> flowRate :		object Flowrate
	--> timeVariation : 	a list of tuples [(time,chemical stage)] or [(time,(list of species))]"""
	Generic.__init__(self)
	print boundary
	print boundary.__class__
        grenzen = [boundary]
        for i in grenzen:
            if not isinstance(i,CartesianMesh):
                raise Exception, "boundary definition to enhance "
        self.boundary = boundary
        
        if type(btype) != StringType:
            raise TypeError," btype must be a string: 'Dirichlet' or 'Neumann'"
        if btype not in ['Dirichlet','Flux','Mixed','Neumann']: raise Exception, "check the head boundary condition type "
        self.type = btype
        
        self.value_species = None
        self.value_property = None
        self.value = None
        if value:
            self.value = value.getValue()
            pass
        
        if velocity:
            if not isinstance(velocity,Velocity):
                raise Exception, "velocity definition to enhance "
            pass
        self.velocity = velocity

        if flowRate:
            if not isinstance(flowRate,Flowrate):
                raise Exception, "flowRate definition to enhance "
            pass
        self.flowRate = flowRate

	
    def getBoundary(self):
        """
        To get boundary conditions
        """
        return self.boundary
	
    def getValue(self, species = None):
        """
        Enables to retrieve a value for
        a specified species using the
        speciesValues list.
        If no sspecies is given, it returns None
        """
        if self.value:
            return self.value
        elif self.value_species:
            if species:
                for spe in range(len(self.value_species)):
                    if (self.value_species[spe] == species):
                        return self.value_property[spe]
            
            return self.value_property[0]
        else:
            return None            
        
        return None
    
def _cellCenter(delta):
    cellCenterList = [delta[0]*0.5]
    for i in range(1,len(delta)): cellCenterList.append((delta[i-1]+delta[i])*0.5)
    return cellCenterList
        
