from cartesianmesh import *

from ModflowSaturatedHydro import *

from material import Material

from physicalquantities import Permeability, Head

from commonmodel import Region

from unsaturatedhydraulicproblem import InitialCondition

from saturatedhydraulicproblem import BoundaryCondition
import unittest
import redirect
class modflowcomponenttest(unittest.TestCase):
    def setUp(self):
        self.r = redirect.output("modflowcomponent_test.log")
        self.r.toFile()

#
# Definition of the mesh
#
        self.mesh = StructuredMesh2D("global","XY")
        self.nx = 42
        self.ny = 1
        self.nb_of_intervals = [self.nx,self.ny]
        self.dx = [0.002]
        self.dx = self.dx*self.nx
        self.dx[0] = self.dx[0]*0.5
        self.pointlist_x = [0.0]
        self.pointlist_y = [0.0]
        for i in range(1,len(self.dx),1):
            self.pointlist_x.append(self.pointlist_x[i-1]+self.dx[i-1])
        self.pointlist_y = [0.0]
        self.pointlist_y.append(1.0)
        self.mesh.setAxis("X",self.pointlist_x)
        self.mesh.setAxis("Y",self.pointlist_y)
#
# End of Definitions for the mesh
#
#        print " Study name:",self.study._name
#
# Definitions of materials
#
        print "-"*20
        print " Definition of materials :"
        print "-"*20
        self. clay_material = Material(name="clay",permeability=Permeability(value=1.0))
        self.cement_material = Material(name="Cement",permeability=Permeability(value=2.0e-7))
#
        print "-"*20
        print " Definition of meshes :"
        print "-"*20
        self.clay_reg_m   = StructuredMesh2D("Clay Region","XY")
        self.clay_reg_m.setZone("Clay Region",index_min = Index2D(2,1),index_max = Index2D(self.nx-1,1))
#
        print "-"*20
        print " Definition of meshes :"
        print "-"*20
        self.east_bo_m   = StructuredMesh2D("boundary east","XY")
        self.east_bo_m.setZone("boundary east",index_min = Index2D(1,1),index_max = Index2D(1,1))
#
# Definition of regions
#
        print "-"*25
        print " Definition of regions :"
        print "-"*25
        self.regions_list = []
        print type(self.clay_reg_m)," nom de la classe :",self.clay_reg_m.__class__.__name__
        print type(self.clay_material)," nom de la classe :",self.clay_material.__class__.__name__
        print "-"*20
        self.reg1 = Region(self.clay_reg_m,self.clay_material)
        self.regions_list.append(self.reg1)

#print "  ---- type ----", hasattr(reg1,"material")
#print "  ---- type ----", hasattr(reg1,"support")
#temp = reg1.__class__
#name = temp.__name__
#print " nom ",name
#pos = name.find('_objref_')
#print " pos ",pos
        tclasses=[Region]
#for c in tclasses:
#    if isinstance(reg1,c):
#        print " ok ",c
#
# Definition of boundary conditions
#
        print "-"*20
        print " Definition of boundary conditions :"
        print "-"*20
        self.boundaryconditions_list = []
        print "-"*10
        print " east_bo_m :"
        print "-"*10

        self.east_bo_m   = StructuredMesh2D("boundary east","XY")
        self.east_min = Index2D(1,1)
        self.east_max = Index2D(1,1)
#east_bo_m.setZone("boundary east",index_min = Index2D(1,1),index_max = Index2D(1,1))
#east_bo_m.setZone("boundary east",index_min = Index2D(1,1),index_max = Index2D(1,1))
        self.east_bo_m.setZone("boundary east",self.east_min,self.east_max)
        self.Boundary=self.east_bo_m
        self.head_value=Head(value=2.2e-7)
        print " class name ",self.head_value.__class__.__name__

        self.bc_east = BoundaryCondition(self.Boundary,'Dirichlet',self.head_value)
        print " on verifie la classe "
        if not isinstance(self.bc_east,BoundaryCondition):
            raise Exception, " the instanciation of the boundary class must be verified "
        print " on a verifie la classe "
        print " east_bo_m : append"
        self.boundaryconditions_list.append(self.bc_east)
#
        print "-"*10
        print " west_bo_w :"
        print "-"*10

        self.west_bo_m   = StructuredMesh2D("boundary west","XY")
        self.west_bo_m.setZone("boundary west",index_min = Index2D(41,1),index_max = Index2D(41,1))
        self.Boundary=self.west_bo_m
        self.Value=Head(value = 0.0)
        self.bc_west = BoundaryCondition(self.Boundary,'Dirichlet',self.Value)
        print " east_bo_m : append"
        self.boundaryconditions_list.append(self.bc_west)

#
# Definition of initial conditions
#
        self.initialconditions_list = []
        self.reg1_ic = InitialCondition(self.clay_reg_m,value=Head(value=1.e-8))
        self.initialconditions_list.append(self.reg1_ic)
# ----------------
# Darcy Resolution
# ----------------
        self.title = " One dimensional simulation"
        print "Title of the study : ",self.title
#
# Definition of Modflow specific parameters
#
        self.mxiter = 200
        self.accl = 1.0
        self.hclose = 1.e-15
        print " Study definition "
        self.Study_type = 'Saturated'
        print " SaturatedHydroModflow instance "
#        self.darcy = SaturatedHydroModflow(self.study._name,self.regions_list,
#	             self.boundaryconditions_list,self.initialconditions_list)
        self.darcy = SaturatedHydroModflow("Modflow_1/2D",self.regions_list,
	             self.boundaryconditions_list,self.initialconditions_list)
        print " SaturatedHydroModflow setMesh method "
        self.darcy.setMesh(self.mesh)
        print " SaturatedHydroModflow setData method "
        self.darcy.setData()
	self.darcy.run()
	
        self.filename_sip="Monod.sip" 
        self.modflow_sip=setSolverParameter(self.mxiter,self.accl,self.hclose)
        self.modflow_sip.sauvegarde(self.filename_sip)
    def testModflow(self):
        pass
	

if __name__ == '__main__':
    unittest.main()
