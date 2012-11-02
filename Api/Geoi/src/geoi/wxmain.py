# -*- Encoding: Latin-1 -*-
#============================================================================
#  FREE PROJECT
#  OPEN SOURCE
#  CHEMICAL-TRANSPORT COUPLING INTERFACE
#  Elmer as mechanical tool should be introduced in the near future
#  to provide a C-T-M coupling for Mt3d and Elmer bounded to phreeqC
#============================================================================
#  Authors :
#              Alain DIMIER:

#============================================================================
#  Version    : 1.1
#============================================================================

import sys
import os.path
# work-around for getting rid of annoying copy module in wrapper python modules
# directory
# The main collection of Python library modules is installed in the directory prefix + '/lib/pythonversion'
mainpath = os.path.join(sys.prefix, 'lib/python' + sys.version[:3])
sys.path.insert(0, mainpath)
print " import wx "
import wx 
from wx.lib.art import img2pyartprov

ourpath = os.path.split(os.path.dirname(__file__))[0]
sys.path.append( ourpath )

from geoi.main_window import    MainWindow
from geoi.actions import        coupling_algorithm
from geoi.actions import        aqueous_state
from geoi.actions import        chemistry
from geoi.actions import        toggle_action
from geoi.actions import        new
from geoi.actions import        switch_to_std_dialog
from geoi.actions import        open_file
from geoi.actions import        save_file
from geoi.actions import        save_file_as
from geoi.actions import        exit
from geoi.actions import        title, simulation_directory
from geoi.actions import        units, physics_software, open_chemistry_db
from geoi.actions import        aqueous_master_species,\
                                aqueous_secondary_species,\
                                mineral_phase,\
                                exchange_master_species,\
                                surface_master_species,\
                                surface_species, exchange_species
from geoi.actions import        equilibrium_state, exchange_state, surface_state
from geoi.actions import        launchingGmsh, load_gmsh_mesh, materials, materials_e, mesh_constructor, set_DarcyVelocity,\
                                set_DarcyVelocity_elmer, set_zones_gmsh, set_zones
from geoi.actions import        mt3d_solver_parameters, coupling_algorithm, parameters_elmer,\
                                time_study, time_discretisation_elmer, simulate_elmer
from geoi.actions import        set_PostProcessing, set_VtkPostProcessing ,set_VtuPostProcessing, plotOverTime,\
                                launching, help, open_shell, inspector, about,params_action
from geoi.actions import        show_params
from geoi.actions import        action
from geoi.actions import        set_PyPostProcessing,\
                                set_interactivePlot,\
                                set_globalGraphics,\
                                post_simulation_display
from geoi.actions import        __init__

import params_manager
import parameters
import geoi.gui.images as images

def createActionTree(mw, params_mgr,solverString):
    # create the tree of actions, for menus and tree widget

#    first element is the name of the subtree
    if solverString == "mt3d":
        transportList = ['Transport',
                        materials.Materials(mw, params_mgr),
                        mesh_constructor.MeshConstructor(mw, params_mgr),
                        set_zones.SetZones(mw, params_mgr),
                        set_DarcyVelocity.DarcyVelocityComponents(mw, params_mgr)
                  ]
        solverList = ['Solver', 
                       mt3d_solver_parameters.Mt3dSolverParameters(mw, params_mgr),
                       coupling_algorithm.CouplingAlgorithm(mw, params_mgr)

                  ]
    else:
        transportList = ['Transport',
                            materials_e.Materials(mw, params_mgr),
                            ["Gmsh", 
                            	launchingGmsh.Run(mw),
                                load_gmsh_mesh.LoadGmshMesh(mw, params_mgr),
                            ],
                            ["Materials/ Aqueous states", 
                                set_zones_gmsh.SetZonesGmsh(mw, params_mgr),
                            ],
                            ["Hydraulic", 
                                set_DarcyVelocity_elmer.DarcyVelocityComponentsElmer(mw, params_mgr)
                            ]
                        ]
        solverList = ['Solver', 
                           ['Elmer Solver',
                               parameters_elmer.ParametersElmer(mw,params_mgr),
                               time_discretisation_elmer.ElmerCouplingAlgorithm(mw,params_mgr),
                               set_VtkPostProcessing.VtkPostProcessing(mw, params_mgr),
#                               time_study.TimeStudy(mw, params_mgr),
                               simulate_elmer.SimulateElmer(mw,params_mgr)
                           ],
                      ]

    tree = [ 'Root',
    # File
                ['File', new.New(mw, params_mgr), open_file.OpenFile(mw, params_mgr)
                     , save_file.SaveFile(mw, params_mgr), save_file_as.SaveFileAs(mw, params_mgr)
                     , exit.Exit(mw) ],
    # Edit
                     
                ['Edit', params_mgr.getUndoAction(), params_mgr.getRedoAction()
                    ,switch_to_std_dialog.SwitchToStdDialog(mw)],
#                [':'],
    # Define
                ['Define'
                    , title.Title(mw, params_mgr), units.Units(mw, params_mgr)
                    , physics_software.PhysicsSoftware(mw, params_mgr)
#                    , chemistry.Chemistry(mw, params_mgr) 
                    ],
    # Chemistry
                    
                ['Chemistry', open_chemistry_db.OpenChemistryDB(mw, params_mgr)
                    ,['Base Addenda',
                        ['Aqueous Phase', aqueous_master_species.AqueousMasterSpecies(mw, params_mgr),
                         aqueous_secondary_species.AqueousSecondarySpecies(mw, params_mgr)
                         ],
                        ['Mineral Phase',mineral_phase.MineralPhases(mw, params_mgr)
                         ],
                         ['Exchange', exchange_master_species.ExchangeMasterSpecies(mw, params_mgr)
                          , exchange_species.ExchangeSpecies(mw, params_mgr) ],
                        ['Surface', surface_master_species.SurfaceMasterSpecies(mw, params_mgr)
                        , surface_species.SurfaceSpecies(mw, params_mgr)]
                      ],
                      ['Aqeous States',
                          aqueous_state.AqueousStatesDefinition(mw, params_mgr),
                          equilibrium_state.EquilibriumPhasesDefinition(mw, params_mgr),
                          exchange_state.ExchangeDefinition(mw, params_mgr),
                          surface_state.SurfaceDefinition(mw, params_mgr)
                      ],
                 ],
    # Transport
                 transportList,
    # Solve

                 solverList,
    # Plot
#                  'Simulate',coupling_algorithm.Coupling(mw, params_mgr)

                 ["Plot/ Outputs", ["Outputs",set_PostProcessing.PostProcessing(mw, params_mgr),
                                  set_PyPostProcessing.PyPostProcessing(mw, params_mgr),
                                  set_VtkPostProcessing.VtkPostProcessing(mw, params_mgr)],
                                 ["Interactive Plot",set_interactivePlot.interactivePlot(mw, params_mgr)],
                                 ["Paraview", launching.Run(mw)
                                  ],
#                                  plotOverTime.PlotOverTime(mw, params_mgr),
                                 ["Exit",exit.Exit(mw) ]
                 ],
    # Help

                ['Help', help.Help(mw), show_params.ShowParams(mw, params_mgr),
                  open_shell.OpenShell(mw), inspector.Inspector(mw), about.About(mw)],
            ]
    return tree

# parse args
def parse_args(argv, params_mgr):
    file_to_open = None
    if len (argv) == 2:
        if argv[1] == '-e' or argv[1] == 'e':
#            print " we try to launch the elmer interface "
            params = params_mgr.getCurrentParamSet()
            params.getParam(parameters.Mode_is_structured).setValue(False)
        else:
            file_to_open = argv[1]
    elif len (argv) == 3:
        if argv[2] == '-e' or argv[2] == 'e':
#            print " we try to launch the elmer interface "
            params = params_mgr.getCurrentParamSet()
            params.getParam(parameters.Mode_is_structured).setValue(False)
            file_to_open = argv[1]
    
    return file_to_open

def build_main_window(params):
    win = MainWindow(None, -1, "")
    #
    # 850 / width
    # 650 / height
    #
    win.SetMinSize((850,650))
    win.SetBackgroundColour("#1B56EA")
    win.SetForegroundColour("#1B56EA")
    win.SetFont(wx.Font(8,wx.FONTFAMILY_DEFAULT,wx.NORMAL,wx.NORMAL))
    if params.getParam(parameters.Mode_is_structured).getValue():
        win.SetTitle('Geochemical - Transport GUI - phreeqC/Mt3d')
    else:
        win.SetTitle('Geochemical - Transport GUI - phreeqC/Elmer')

    return win

class MyAppProvider(wx.ArtProvider):
    def __init__(self, size):
        wx.ArtProvider.__init__(self)
        self.size = size

    def CreateBitmap(self, id, client=wx.ART_OTHER, size=wx.DefaultSize):
        s = self.size
        if size != wx.DefaultSize:
            s = size
        b = wx.ArtProvider.GetBitmap(id, client, s)

        return b

app = wx.App(0)
params_mgr = params_manager.ParamsManager()
file = parse_args(sys.argv, params_mgr)

wx.ArtProvider.Push(MyAppProvider( (16,16) ))
#imagesProvider = img2pyartprov.Img2PyArtProvider(images, artIdPrefix='wx.ART_IMAGES_')
#wx.ArtProvider.Push(imagesProvider)
#wx.ArtProvider.Push(images)

#app = init_qt_and_set_styles(sys.argv)
mw = build_main_window(params_mgr.getCurrentParamSet())
params_mgr.createRedoAndUndoActions(mw)

if len (sys.argv) == 1: # structured case
    actionTree = createActionTree(mw, params_mgr,"mt3d")
elif len (sys.argv) == 2:
    if ".geoi" in str (sys.argv [1]): # structured case and an already defined file
        actionTree = createActionTree(mw, params_mgr,"mt3d")
    elif str (sys.argv [1]) == '-e' or str (sys.argv [1]) == 'e' or str (sys.argv [1][0])=='e' or str (sys.argv [1][0:1])=='-e': 
        actionTree = createActionTree(mw, params_mgr,"elmer")
    else:
        raise Exception(" there is a problem my friend")
elif len (sys.argv) == 3:
    if ".geoi" in str (sys.argv [1]): # unstructured case and an already defined file
        actionTree = createActionTree(mw, params_mgr,"elmer")
else:
    raise Exception(" there is a problem my friend")
mw.setup(actionTree)

params_action.ParamsAction.SetDialogPanel( mw.getDialogPanel() )

#frame = wx.Frame(None, -1, "Hello from wxPython")
#frame.Show()

#actionTree = createActionTree(mw, params_mgr)
mw.CenterOnScreen()
mw.Show()

if file:
    params_mgr.openFile(file)

app.MainLoop()


