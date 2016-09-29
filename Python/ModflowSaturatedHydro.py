""" Modflow saturated hydraulic component """

import os
import string

from cartesianmesh import *

from PhysicalProperties import Permeability

from saturatedhydraulicproblem import SaturatedHydraulicProblem

from string import ljust

from unsaturatedhydraulicproblem import InitialCondition

from saturatedhydraulicproblem import BoundaryCondition

from unsaturatedhydraulicproblem import InitialCondition

def foncfor(xfloat,m,n):
    exp =0
    sign=1
    if xfloat<0:
        sign=-1
        xfloat = sign*xfloat
    if xfloat>1:
        while xfloat/10. >= 1:
            exp = exp+1
            xfloat = xfloat/10
        ei = int(xfloat)
        ed = xfloat-ei
        if exp<9: exp="0"+str(exp)
        else: exp=str(exp)
#        print " ei ed exp sign ",ei,ed,exp[0:2],sign
        if sign==1:
            x=str(ei)+str(ed)[1:n+1]+"E+"+exp[0:2]
        else:
            x="-"+str(ei)+str(ed)[1:n+1]+"E+"+exp[0:2]

    elif xfloat>1.e-15:
#        print " on passe par le else: "
        while xfloat*10 < 1:
            exp = exp+1
            xfloat = xfloat*10
#        print "exp ",exp
        ei = int(xfloat)
        ed = xfloat-ei
        if exp<9: exp="0"+str(exp)
        else: exp=str(exp)
#        print " ei ed exp sign ",ei,ed,exp[0:2],sign
        if sign==1:
            x=str(ei)+str(ed)[1:]+"E-"+exp[0:2]
        else:
            x="-"+str(ei)+str(ed)[1:]+"E-"+exp[0:2]

    else:
        x = "0.0E+00"
    long = len(x)
    
    x = " "*(m-long)+x
    return x    

class SaturatedHydroModflow(SaturatedHydraulicProblem):
#    __init__xattributes__ = [
#        XAttribute("name",xtype=XString()),
#        XAttribute("regions_list",
#                   xtype= XList(sequence=XInstance("commonmodel.Region"))),
#        XAttribute("boundaryconditions_list",
#                   xtype= XList(sequence=XInstance(BoundaryCondition))),
#        XAttribute("initialconditions_list",
#                   xtype= XList(sequence=XInstance(InitialCondition)))]
        
        
    def __init__(self,name,regions_list,boundaryconditions_list,initialconditions_list):
   # def __init__(self,*args,**kwargs):       
	SaturatedHydraulicProblem.__init__(self,name=name,
					   regions=regions_list,
					   boundaryConditions=boundaryconditions_list)
	self.initialConditions = initialconditions_list
#
# page 37 of the document 96-485 " Strongly Implicit Procedure "
# 
    def setMesh(self,mesh):
        self.mesh=mesh
	
    def run(self):
        import os
        osStatus = os.system("which modflow96")
        if osStatus<>0:
            raise "modflow96 not found"
        osStatus = os.system("modflow96 < modf.fil")
        
    def setData(self):
        nom_fichier_fil = "modf.fil"
        self.file_fil=open(nom_fichier_fil,'w')
        self.file_fil.write("%25s\n"%(ljust("Monod.mod",25)))
        self.file_fil.write("%25s\n"%(ljust("Monod.bas",25)))
        self.file_fil.write("%25s\n"%(ljust("Monod.bcf",25)))
        self.file_fil.write("%25s\n"%(ljust("Monod.sip",25)))
        self.file_fil.write("%25s\n"%(ljust("Monod.oc" ,25)))
        self.file_fil.write("%25s\n"%(ljust("Monod.umt",25)))
        self.file_fil.close()
	
        nom_fichier_bas = "Monod.bas"
        nom_fichier_bcf = "Monod.bcf"
        nom_fichier_oc  = "Monod.oc"
        self.file_bas=open(nom_fichier_bas,'w')
#
# Physical properties are used to build up Monod.bas
#
        self.file_bas.write("%s \n"%("Python Interface generated"))
        self.file_bas.write("%s \n"%(self.name))
	print " Valeur de nrow"
        nrow = self.mesh.getNbPoints("Y")-1
	print " Valeur de nrow",nrow
        nlay = 1
        ncol = self.mesh.getNbPoints("X")-1
        print " Valeur de ncol",ncol
	#
        # Nper is the number of stress simulations
	#
        nper=1
	#
        # Itmuni =4 corresponds to a day time unit, it hasn't any incidence on the simulation
	#
        itmuni =4
        self.file_bas.write("%10i%10i%10i%10i%10i   !nlay,nrow,ncol,nper,itmuni\n"\
                            %(nlay,nrow,ncol,nper,itmuni))
        self.file_bas.write("%s\n"%(" 11 00 00  0  0  0  0 00 19  0  0 22 00 00 00 00 00 00 00 00 00 66 00 00"))
#	
# iapart indicates wether array BUFF is separate from RHS. if iapart = 0, the arrays occupy the same space
#. It is recommended to set iapart to 0.
#
        iapart = 0
# istrt = 0: the initial head is not kept.
        istrt = 0
        self.file_bas.write("%10i%10i   !iapart,istrt\n"%(iapart,istrt))
        # Ibound designates the way the cells are treated
        # -1 for a boundary cell
        # +1 for a live cell
        ibound=[1]
        ibound = ibound*nrow*ncol
        for boundaryzone in self.boundaryConditions:
            print " Randbedingungen ",boundaryzone.type,boundaryzone.boundary.name
	    print " type de boundaryzone.boundary.zones",boundaryzone.boundary.zones
	    ind_min = boundaryzone.boundary.zones[0].getIndexMin().getValues()
	    ind_max = boundaryzone.boundary.zones[0].getIndexMax().getValues()
            i_min = ind_min[0]
            i_max = ind_max[0]
            j_min = ind_min[1]
            j_max = ind_max[1]
	    
#	    i_min = boundaryzone.boundary.zones[0].min.i
#	    i_max = boundaryzone.boundary.zones[0].max.i
#	    j_min = boundaryzone.boundary.zones[0].min.j
#	    j_max = boundaryzone.boundary.zones[0].max.j
	    print " valeur des indices :",i_min,i_max,j_min,j_max
            for i in range(i_min,i_max+1,1):
                for j in range(j_min,j_max+1,1):
                    k = (j-1)*ncol+i
##                print " boundary affectation ",i
                    ibound[k-1] = -1
        # fmtin is the read format 
        fmtin = "("+str(ncol)+"I3)"
        self.file_bas.write("%10i%10i%20s%10i   !IBOUND\n"%(1,1,fmtin,-1))
	print " longueur de ibound ",len(ibound),nrow
        for i in range(0,len(ibound)):
            self.file_bas.write("%3i"%(ibound[i]))
            if ((i+1)%ncol==0)and(i!=nrow*ncol):
	        print " mod ncol ",i,nrow
                self.file_bas.write("\n")
#        self.file_bas.write("\n")
        print "*"*81
	#
        # HNOFLO is set to 999.99
	#
        self.file_bas.write("%10s\n"%(999.99))
	#
        # fmtin is the read format 
	#
        fmtin = "("+str(ncol)+"E15.8)"
        self.file_bas.write("%10i%10s%20s%10i   !HEAD\n"\
                            %(1,foncfor(1.e-15,10,4),ljust(fmtin,25),4))
        ci=[0.0]
        ci = ci*ncol*nrow
#
# Setting initial conditions for regions
#
        print " traitement des conditions initiales "
        for initialcondition in self.initialConditions:
            print self.initialConditions
            value = initialcondition.getValue()
	    #valeur = value.getValue()
	    print "initial condition ",type(initialcondition)
	    print "initial condition ",dir(initialcondition)
	    print "initial condition ",initialcondition.getRegion()
	    mesh = initialcondition.getRegion()
	    print mesh
	    print dir(mesh)
            zone = mesh.getZones()
	    
	    	    
	    ind_min = zone[0].getIndexMin().getValues()
	    ind_max = zone[0].getIndexMax().getValues()
            i_min = ind_min[0]
            i_max = ind_max[0]
            j_min = ind_min[1]
            j_max = ind_max[1]
            for i in range(i_min,i_max+1,1):
                for j in range(j_min,j_max+1,1):
                    k = (j-1)*ncol+i
                    ci[k-1]=value
        print " longueur du tableau ",len(ci),nrow
#
# Setting initial conditions for boundaries
#
        ind = 0

        for boundaryzone in self.boundaryConditions:
            print " Randbedingungen ",boundaryzone.type,boundaryzone.boundary.name
	    print " type de boundaryzone.boundary.zones",boundaryzone.boundary.zones
	    ind_min = boundaryzone.boundary.zones[0].getIndexMin().getValues()
	    ind_max = boundaryzone.boundary.zones[0].getIndexMax().getValues()
            i_min = ind_min[0]
            i_max = ind_max[0]
            j_min = ind_min[1]
            j_max = ind_max[1]
	    
	    
	    value = boundaryzone.getValue()
#	    value = value['__all__'].getValue()
	    value = value.getValue()
##                        print "valeur de i1 et i2",i1,i2
            for i in range(i_min,i_max+1,1):
                print " boucle en i de boundary ",i_min,i_max,value

                ci[i-1]=value
                print "valeur de i1 et i2 pour initialisation",i_min,i_max
	print ci

        for i in range(0,len(ci)):
##            print " boucle pour ic ",i,ci[i],foncfor(ci[i],15,8)
        
            self.file_bas.write("%s"%(foncfor(ci[i],15,8)))
            if ((i+1)%ncol==0)and((i+1)!=nrow*ncol):
                self.file_bas.write("\n")
        self.file_bas.write("\n")
        # perlen is the length of the stress period considered
        perlen=3.e+9
        nstp=1
        tsmult=1.0
        self.file_bas.write("%10s%10i%10s   !perlen, nstp, tsmult\n"\
                            %(foncfor(perlen,10,5),nstp,foncfor(tsmult,10,5)))
        self.file_bas.write("#")
        self.file_bas.write("See comment lines page 16 of the User's documentation\n")
        self.file_bas.write("the head is got from the table, and then multiplied by 1.E-8\n")
        self.file_bas.write("#")
        self.file_bas.close()
        self.file_bcf=open(nom_fichier_bcf,'w')
        iss = 1
        ibcfcb = 0
        self.file_bcf.write("%10i%10i   !iss,ibcfbd\n"%(iss,ibcfcb))
        self.file_bcf.write("%3i\n"%(0))
	#
        # fmtin is the read format 
	#
	intfmtin = ncol
        fmtin = "("+str(intfmtin)+"E15.8)"
        #
        # Introduction of the anisotropy factor taking 1. as value
        # So the medium is considered as isotropic
        # 
        self.file_bcf.write("%10i%10s%20s%10i   !Isotropy\n"\
                            %(11,foncfor(1.e-15,10,4),ljust(fmtin,20),4))
        por = 1.0
        por=[por]*nlay
        for i in range(0,nlay):
            self.file_bcf.write("%15s"%(por[i]))
            if (i+1)%intfmtin==0:
                self.file_bcf.write("\n")
        self.file_bcf.write("\n")  
	#      
        # Introduction of delr
	#
        self.file_bcf.write("%10i%10s%20s%10i   !Delr\n"\
                            %(11,foncfor(1.e-15,10,4),ljust(fmtin,20),4))
	#		  
        # Here we write the size of each element in the X direction
	#

        delr = self.mesh.getAxis("X")
        for i in range(0,ncol):
            delr[i]=delr[i+1]-delr[i]
##            print i,delr[i-1],delr[i]
        for i in range(0,ncol):
            self.file_bcf.write("%15s"%(delr[i]))
            if (i+1)%intfmtin==0 or (i+1)%ncol==0:
                self.file_bcf.write("\n")
#        self.file_bcf.write("\n")
        self.file_bcf.write("%10i%10s%20s%10i   !Delc\n"\
                            %(11,foncfor(1.e-15,10,4),ljust(fmtin,20),4))
        #
        # Here we write the size of each element in the Y direction
        #
	
        delc_length=self.mesh.getNbPoints("Y")
	print delc_length
        delc = self.mesh.getAxis("Y")
	for i in range(0,nrow):
            delc[i]=delc[i+1]-delc[i]
            print " delc",i,delc[i-1],delc[i]
        for i in range(0,nrow):
            self.file_bcf.write("%15s"%(delc[i]))
            if (i+1)%intfmtin==0 or (i+1)%nrow==0:
                self.file_bcf.write("\n")
        #
        # Here we make the hypothesis that the layer considered has a unit length
        # to ensure the egality between transmissivity and hydraulic conductivity
        #
        kx=[1.0]
        kx = kx*ncol*nrow
        self.file_bcf.write("%10i%10s%20s%10i   !Conductivities\n"\
                            %(11,foncfor(1.e-15,10,4),ljust(fmtin,20),4))
        # Creation of the hydraulic conductivity table
        print " region ",self.regions
        for region in self.regions:
            print "region consideree\n",region
	    support = region.getZone()
	    print "permeabilite ",region.material.permeability.getValue()
            hydcon = region.material.permeability.getValue()
	    
            print "valeur de Kx",hydcon.getValues()
            for zone in support.getZones():
	    	ind_min = zone.getIndexMin().getValues()
	        ind_max = zone.getIndexMax().getValues()
                i_min = ind_min[0]
                i_max = ind_max[0]
                j_min = ind_min[1]
                j_max = ind_max[1]
	    
                for i in range(i_min,i_max+1,1):
                    for j in range(j_min,j_max+1,1):		    
                        k = (j-1)*ncol+i
			kx[k-1]=hydcon.getValues()
        #
        for i in range(0,len(kx)):
            self.file_bcf.write("%15s"%(kx[i]))
            if (i+1)%intfmtin==0:
                self.file_bcf.write("\n")
        self.file_bcf.write("\n")


#            self.file_bas.write('MATErial TYPE %d ID=%s \n'%(i+1,nom_zone))
#            self.file_bas.write('FOR material %d \n'%(i+1))

        self.file_bcf.close()
        #
        # We write here the Modflow output file
        #
        self.file_oc=open(nom_fichier_oc,'w')
	#
        # ihedfm=6: is a write format for heads
	#
        ihedfm = 6
	#
        # iddnfm is a write format for drawdowns
	#
        iddnfm = 6
	#
        # ihedun=0: is the unit number where heads will be saved
	#
        ihedun = 0
	#
        # iddnum = 0:   is the unit number where drawdowns will be saved
	#
        iddnun = 0
        self.file_oc.write("%10i%10i%10i%10i   !Ihedfm, Iddnfm, Ihedun, Iddnun\n"\
                            %(ihedfm,iddnfm,ihedun,iddnun))
	#
        # incode=0: taking the 0 value, all layers will be treated the same way
	#
        incode = 0
        # 
        ihddfl = 1
	#
        # ibudfl!=0: the budget will be printed
	#
        ibudfl = 0
	#
        # icbcfl=1: cell by cell flow terms are printed
	#
        icbcfl = 1
        self.file_oc.write("%10i%10i%10i%10i   !Incode, Ihddfl, Ibudfl, Icbcfl\n"\
                            %(incode,ihddfl,ibudfl,icbcfl))
	#
        # hdpr!=0:  head is printed for the corresponding layer
	#
        hdpr = 1
	#
        # ddpr=0:   drawdown is printed for the layer
	#
        ddpr = 0
        # hdsv!=0:  head isn't saved
        hdsv = 1
	#
        # ddsv=0:   drawdown is saved for the layer
	#
        ddsv = 0
        self.file_oc.write("%10i%10i%10i%10i   !Hdpr, Ddpr, Hdsv, Ddsv\n"\
                            %(hdpr,ddpr,hdsv,ddsv))
        self.file_oc.close()
 
class setSolverParameter(SaturatedHydroModflow):
#    __init__xattributes__ = [
#        XAttribute("mxiter",xtype=XInt()),
#        XAttribute("accl",xtype= XFloat()),
#        XAttribute("hclose",xtype= XFloat())]
        

   # def __init__(self,*args,**kwargs):       

    def __init__(self,mxiter,accl,hclose):
	#
	# mxiter : Maximum number of iteration loop for dsystem solving
	#
		self.mxiter = mxiter
	#
	# nparm = 5: Number of iteration parameters to be used . fixe
	#
		self.nparm=5
	#
	# accl : Acceleration parameters
	#
		self.accl=accl
	#
	# hclose : head change criterion for convergence
	#
		self.hclose=hclose
	#
	# ipcalc : flag indicating where the seed for calculating
	# iteration parameters come from
	#
		self.ipcalc=0
	#
	# wseed : is the seed for calculating iterations parameter
	#
		self.wseed=1.e-11
	#
	# iprsip = 1: The maximum head change is printed whenever the time step
	#is an even multiple of IPRSIP. fixe
	#
		self.iprsip=1

    def sauvegarde(self,fichier) :
		print " Maximum number of iteration \n",self.mxiter
		print " Number of iteration parameters \n",self.nparm
		
		print " Acceleration parameters \n",self.accl,
		print " head change criterion \n",self.hclose,
		print " flag ipcalc \n",self.ipcalc,
		print " seed for calculating iterations parameter \n",self.wseed,
		print " maximum head change \n",self.iprsip
		self.file_sip=open(fichier,'w')
		print "ecriture dans fichier"
		self.file_sip.write("%10d%10d   !MXITER NPARM\n"%(self.mxiter,self.nparm))
		self.file_sip.write("%s%s%10d%s%10d"%(foncfor(self.accl,10,8),foncfor(self.hclose,10,8),\
                                                    self.ipcalc,foncfor(self.wseed,10,8),self.iprsip))
		self.file_sip.close()

                print "fermeture du fichier "
