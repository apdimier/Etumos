import traceback
import os

import wx
from geoi.actions.params_action import ParamsAction

from geoi import parameters

description =\
       """
       You can load here a gmsh mesh file: .msh extension.
       """

HELP =\
       """ 
       The user can load a gmsh mesh file here, see http://geuz.org/gmsh and $WRAPPER/Doc               
       The file should have been created through built-in CAD gmsh facilities:                                      
         Geometry:      a bottom-up flow defining points, lines, triangles, quadrangles, tetrahedra,...    
                        The resulting file having a \".geo\" extension                                    
                                                                                                        
         Mesh:          A finite element mesh, the resulting file having a \".msh\" extension.             
       """ +\
       """ 
                                                                                                        
         The file should be in the same directory as the one where the GUI has been launched.           
       """

class LoadGmshMesh(ParamsAction):
    "LoadGmshMesh : Load a mesh created with Gmsh"

    def __init__(self, win, params_mgr):
        ParamsAction.__init__(self, params_mgr,  win, "Load a gmsh Mesh",description=description,help=HELP)
        self.param_mgr = params_mgr
        self.param_mgr.gmshMesh = ""


    def _createInterface(self, parent, params):
    	self.params = params  	
    	self.parent = parent  	
    	
    	sizer = wx.BoxSizer( wx.VERTICAL )
    	simul = self.GetDialogPanel()
    	
    	
    	box = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "") , wx.HORIZONTAL)
        box.SetMinSize((200,20)) 
    	 
    	meshFileName = params.getParam(parameters.Gmsh_Name_File2).getValue().split("/")[-1]
    	self.label = label = wx.StaticText(parent, -1, "Actual mesh file :\n" + meshFileName)
        label.SetHelpText("This is the help text for the label")
        box.Add(label, 0, wx.LEFT|wx.ALL, 2)
        
        self.load = wx.Button(parent, -1, "Load", (200,100))
        simul.Bind(wx.EVT_BUTTON, self._load, self.load)
        
    	parent.SetSizerAndFit(sizer) 
    	  	
    def _onOk(self, params):
        return True
    
    def _load(self,event):
        params = self.params
        curWorDir = os.getcwd()
        wildcard = ".msh file (*.msh)|*.msh|All files (*.*)|*.*"
        dlg = wx.FileDialog(
            self.getParent(), message="Choose a .msh file to open\n",
            defaultDir=curWorDir,
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.CHANGE_DIR | wx.FD_FILE_MUST_EXIST
            )
        
        if dlg.ShowModal() == wx.ID_OK:
            # This returns a Python list of files that were selected.
            nfile = dlg.GetPath()
            f1 = open(nfile,"r")
            # If the .msh file is not in current directory, we copy it in this directory
            if curWorDir == nfile[0:-len(nfile.split('/')[-1])-1] :
                meshFileName = nfile
                print ".msh file is in current directory"
            else :    
            	print ".msh file is not in currrent directory: a copy is made in this directory"   
                meshFileName = nfile.split('/')[-1]
#                meshFileName = os.getcwd()+\
#                self.params.getParam(parameters.Title).getValue()+".msh" 
                f2 = open(curWorDir + '/' + meshFileName,"w")
                f2.write(f1.read())
                f2.close()
            f1.close()

            params.getParam(parameters.Gmsh_Name_File2).setValue(str(meshFileName))
            
            # Updating the file name display
            meshFileName = params.getParam(parameters.Gmsh_Name_File2).getValue().split("/")[-1]
            self.label.SetLabel("Actual mesh file :\n" + meshFileName)
            os.chdir(curWorDir)
        dlg.Destroy()

        return None
