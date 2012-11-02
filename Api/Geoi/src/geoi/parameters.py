from geoi.chemistry_db import ChemistryDB
from geoi.material_db  import MaterialDB
import warnings
import datetime
import copy

from parameter import Parameter, IS_INTEGER, IS_NUMBER, IS_STRING

WRAPPER_DAT = '$WRAPPER_DAT'
CHEMISTRY_DB_EXTENSION = ".dat"
#from string import find

IMPORTED_CHEMISTRY_DB = 'IMPORTED_CHEMISTRY_DB'
CUSTOM_CHEMISTRY_DB = 'CUSTOM_CHEMISTRY_DB'
CUSTOM_MATERIAL_DB = 'CUSTOM_MATERIAL_DB'
IMPORTED_MATERIAL_DB = 'IMPORTED_MATERIAL_DB'

Mode_is_structured = 'Mode_is_structured'

Title = 'Title'
Concentration_Unit = 'Concentration_Unit'
Density_Unit = 'Density_Unit'
Dispersivity_Unit = 'Dispersivity_Unit'
EffectiveDiffusion_Unit = 'EffectiveDiffusion_Unit'
Enthalpy_Unit = 'Enthalpy_Unit'
Head_Unit = 'Head_Unit'
Length_Unit = 'Length_Unit'
Permeability_Unit = 'Permeability_Unit'
Temperature_Unit = 'Temperature_Unit'
Time_Unit = 'Time_Unit'
UNITS = [Concentration_Unit, Density_Unit, Dispersivity_Unit, EffectiveDiffusion_Unit, Enthalpy_Unit
         , Head_Unit, Length_Unit, Permeability_Unit, Temperature_Unit, Time_Unit]
UNITS_SI = ['moles/m3','kg/m3','m', 'm2/s', 'J/kg', 'm/s',"Kelvin" ]


#SOLVER_PHREEQC = 'PhreeqC'
SOLVER_CHEMISTRY = 'Chemistry'
SOLVER_MODFLOW_MT3D_PHREEQC= 'Modflow_Mt3d_PhreeqC'
SOLVER_ELMER_PHREEQC= 'Elmer_PhreeqC'
SOLVER_MODFLOW = 'Modflow'
SOLVERS = [SOLVER_CHEMISTRY, SOLVER_MODFLOW_MT3D_PHREEQC, SOLVER_MODFLOW,SOLVER_ELMER_PHREEQC]
Solver = 'Solver'

Thermal = 'Thermal'

ChemistryTool = 'ChemistryTool'
CHEMISTRY_TOOL_PHREEQC = 'PhreeqC'
CHEMISTRY_TOOL_ELMER_PHREEQC = 'Elmer_PhreeqC'
#CHEMISTRY_TOOLS = [CHEMISTRY_TOOL_PHREEQC, CHEMISTRY_TOOL_ELMER_PHREEQC]
CHEMISTRY_TOOLS = [CHEMISTRY_TOOL_PHREEQC]

InteractiveXYPlot_Parameters_list = 'InteractiveXYPlot_Parameters_list'
InteractiveXYPlot_AqueousComponentsToPlot_list = 'InteractiveXYPlot_AqueousComponentsToPlot_list'
InteractiveXYPlot_AvailableAqueousComponents_list = 'InteractiveXYPlot_AvailableAqueousComponents_list'

InteractiveXYPlot_Space_and_Time_Parameters_list = 'InteractiveXYPlot_Space_and_Time_Parameters_list'
InteractiveXYPlot_Space_and_Time_ElementsToPlot_list = 'InteractiveXYPlot_Space_and_Time_ElementsToPlot_list'
PLOT_I = 'I'
PLOT_J = 'J'

ExpectedOutputs_list = 'ExpectedOutputs_list'
Quantity_list = 'Quantity_list'
ExpectedOutputsQuantity_list = 'ExpectedOutputsQuantity_list'
EXPECTEDOUTPUTS_STANDARD_LIST = ['pH', 'pe', 'Eh', 'tc', 'mass_water', 'ionicstrength']
Times_list = 'Times_list'

PostprocessingXYPlot_Parameters_list = 'PostprocessingXYPlot_Parameters_list'
Postprocessing_ElementsToPlot_list   = 'Postprocessing_ElementsToPlot_list'

InteractiveContours_Parameters_list = 'InteractiveContours_Parameters_list'
InteractiveContours_AqueousComponentsToPlot_list = 'InteractiveContours_AqueousComponentsToPlot_list'
InteractiveContours_AvailableAqueousComponents_list = 'InteractiveContours_AvailableAqueousComponents_list'

PostprocessingContours_Parameters_list = 'PostprocessingContours_Parameters_list'
PostprocessingContours_AqueousComponentsToPlot_list = 'PostprocessingContours_AqueousComponentsToPlot_list'
PostprocessingContours_AvailableAqueousComponents_list = 'PostprocessingContours_AvailableAqueousComponents_list'

DefaultDatabase = 'DefaultDatabase'
CurrentDatabasePath = 'CurrentDatabasePath'
#CurrentDatabase = 'CurrentDatabase'
DATABASE_LLNL = 'llnl.dat'
DATABASE_PHREEQC = 'phreeqc.dat'
Available_Databases_list = 'Available_Databases_list'

AqueousStates_list = 'AqueousStates_list'
AqueousStates_Properties_list = 'AqueousStates_Properties_list'
AqueousStates_Species_list = 'AqueousStates_Species_list'
AqueousStates_Default_Temperature = 'AqueousStates_Default_Temperature'
AqueousStates_Default_pH = 'AqueousStates_Default_pH'
AqueousStates_Default_pe = 'AqueousStates_Default_pe'
AqueousStates_Default_Eh = 'AqueousStates_Default_Eh'

AqueousStates_MineralPhases_list = 'AqueousStates_MineralPhases_list'
AqueousStates_MineralPhases_Properties_list = 'AqueousStates_MineralPhases_Properties_list'

AqueousStates_ExchangeSpecies_list = 'AqueousStates_ExchangeSpecies_list'
AqueousStates_ExchangeSpecies_Properties_list = 'AqueousStates_ExchangeSpecies_Properties_list'

AqueousStates_SurfaceSpecies_list = 'AqueousStates_SurfaceSpecies_list'
AqueousStates_SurfaceSpecies_Properties_list = 'AqueousStates_SurfaceSpecies_Properties_list'

KineticRates_list = 'KineticRates_list'
AqueousStates_KineticRates_list = 'AqueousStates_KineticRates_list'
AqueousStates_KineticRates_Properties_list = 'AqueousStates_KineticRates_Properties_list'

Rate = 'Rate'
RATE_STANDARD = "Standard"
TemkinNumber = 'TemkinNumber'
KineticConstant = 'KineticConstant'
InitialExchangeSurface = 'InitialExchangeSurface'
SphereModelExponent_On = 'SphereModelExponent_On'
SphereModelExponent = 'SphereModelExponent'

AqueousStates_Gas_list = 'AqueousStates_Gas_list'
AqueousStates_Gas_Properties_list = 'AqueousStates_Gas_Properties_list'

#Database_Solution_Species_list = 'Database_Solution_Species_list'
#
#Database_Components_list = 'Database_Components_list'
#Database_ComponentSpecies_Name_list = 'Database_ComponentSpecies_Name_list'
#Database_ComponentSpecies_Formula_list = 'Database_ComponentSpecies_Formula_list'
#Database_Components_Log_k_list = 'Database_Components_Log_k_list'
#Database_Components_gfw_list = 'Database_Components_gfw_list'
#
#Database_AqueousSpecies_list = 'Database_AqueousSpecies_list'
#Database_AqueousSpecies_Formula_list = 'Database_AqueousSpecies_Formula_list'
#Database_AqueousSpecies_Log_k_list = 'Database_AqueousSpecies_Log_k_list'
#Database_AqueousSpecies_Species_list = 'Database_AqueousSpecies_Species_list'
#
#Database_Phases_Names_list = 'Database_Phases_Names_list'
#Database_Phases_Formula_list = 'Database_Phases_Formula_list'
#Database_Phases_Species_list = 'Database_Phases_Species_list'
#Database_Phases_Log_k_list = 'Database_Phases_Log_k_list'
#Database_Phases_Delta_h_list = 'Database_Phases_Delta_h_list'
#
#Database_ExchangeMasterSpecies_list = 'Database_ExchangeMasterSpecies_list'
#Database_ExchangeMasterSpecies_Formula_list = 'Database_ExchangeMasterSpecies_Formula_list'
#Database_Exchange_Species_list = 'Database_Exchange_Species_list'
#
#Database_SurfaceMasterSpecies_list = 'Database_SurfaceMasterSpecies_list'
#Database_SurfaceMasterSpecies_Formula_list = 'Database_SurfaceMasterSpecies_Formula_list'
#
#Database_SurfaceSpecies_list = 'Database_SurfaceSpecies_list'
#Database_SurfaceSpecies_Log_k_list = 'Database_SurfaceSpecies_Log_k_list'
#Database_SurfaceSpecies_Reactants_list = 'Database_SurfaceSpecies_Reactants_list'
#
#Database_gases_Names_list = 'Database_gases_Names_list'
#
#Components_list = 'Components_list'
#ComponentSpecies_Name_list = 'ComponentSpecies_Name_list'
#ComponentSpecies_Formula_list = 'ComponentSpecies_Formula_list'
#Components_Properties_list = 'Components_Properties_list'
#
#AqueousSpecies_list = 'AqueousSpecies_list'
#AqueousSpecies_Formula_list = 'AqueousSpecies_Formula_list'
#AqueousSpecies_Properties_list = 'AqueousSpecies_Properties_list'
#AqueousSpecies_Species_list = 'AqueousSpecies_Species_list'
#
#MineralPhases_list = "MineralPhases_list"
#MineralPhases_Formula_list = "MineralPhases_Formula_list"
#MineralPhases_Properties_list = "MineralPhases_Properties_list"
#MineralPhases_Species_list = "MineralPhases_Species_list"

Default_log_k = "Default_log_k"
Default_Enthalpy = "Default_Enthalpy"
Default_Density = "Default_Density"

#ExchangeMasterSpecies_list = "ExchangeMasterSpecies_list"
#ExchangeMasterSpecies_Formula_list = "ExchangeMasterSpecies_Formula_list"
#
#ExchangeSpecies_list = "ExchangeSpecies_list"
#ExchangeSpecies_Properties_list = "ExchangeSpecies_Properties_list"
#ExchangeSpecies_Reactants_list = "ExchangeSpecies_Reactants_list"

DebyeHuckel_a = "DebyeHuckel_a"
DebyeHuckel_b = "DebyeHuckel_b"
#Default_DebyeHuckel_a = "Default_DebyeHuckel_a"
#Default_DebyeHuckel_b = "Default_DebyeHuckel_b"

#SurfaceMasterSpecies_list = "SurfaceMasterSpecies_list"
#SurfaceMasterSpecies_Formula_list = "SurfaceMasterSpecies_Formula_list"
#
#SurfaceSpecies_list = "SurfaceSpecies_list"
#SurfaceSpecies_Properties_list = "SurfaceSpecies_Properties_list"
#SurfaceSpecies_Reactants_list = "SurfaceSpecies_Reactants_list"

#============================================================================= = "#============================================================================="
#========================================================= = "#========================================================="
Materials_list = "Materials_list"
Materials_Properties_list = "Materials_Properties_list"
DiffusionLaws_dict = "DiffusionLaws_dict"
DiffusionState = "DiffusionState"
DIFFUSIONSTATE_WINSAUER = "Winsauer"
DIFFUSIONSTATE_EXPONENTIAL = "Exponential"
DIFFUSIONSTATE_LINEAR = "Linear"
DIFFUSIONSTATE_PROPORTIONAL = "Proportional"
DIFFUSIONSTATE_CONSTANT = "Constant"
DIFFUSIONSTATES = [DIFFUSIONSTATE_WINSAUER,DIFFUSIONSTATE_EXPONENTIAL,DIFFUSIONSTATE_LINEAR,DIFFUSIONSTATE_PROPORTIONAL,DIFFUSIONSTATE_CONSTANT]

MaterialName = "MaterialName"
KxPermeability = "KxPermeability"
KyPermeability = "KyPermeability"
KzPermeability = "KzPermeability"
EffectivePorosity = "EffectivePorosity"
EffectiveDiffusion = "EffectiveDiffusion"
LongitudinalDispersivity = "LongitudinalDispersivity"
TransverseDispersivity = "TransverseDispersivity"

MaterialConductivity = "MaterialConductivity"
SpecificHeatCapacity = "SpecificHeatCapacity"
HydraulicConductivity = "HydraulicConductivity"

var_diff_list = "var_diff_list"

DefaultMaterialName = "DefaultMaterialName"
DefaultKxPermeability = "DefaultKxPermeability"
DefaultKyPermeability = "DefaultKyPermeability"
DefaultKzPermeability = "DefaultKzPermeability"
DefaultEffectivePorosity = "DefaultEffectivePorosity"
DefaultEffectiveDiffusion = "DefaultEffectiveDiffusion"
DefaultLongitudinalDispersivity = "DefaultLongitudinalDispersivity"
DefaultTransverseDispersivity = "DefaultTransverseDispersivity"
DefaultConductivity = "DefaultConductivity"

MeshLine_Direction = "MeshLine_Direction"
DIRECTION_I = "I"
DIRECTION_J = "J"
DIRECTIONS = [DIRECTION_I, DIRECTION_J]

GridLineInI = "GridLineInI"
GRIDLINE_NEW = "New"
GRIDLINE_OLD = "Old"
GRIDLINES = [GRIDLINE_NEW, GRIDLINE_OLD]
LineNumberInI = "LineNumberInI"
NumberOfLinesInI = "NumberOfLinesInI"

Mesh_list_InI = "Mesh_list_InI"
MeshLineInINumberOfCells = "MeshLineInINumberOfCells"
MeshLineInILength = "MeshLineInILength"
MeshLineInIGeometricRatio = "MeshLineInIGeometricRatio"

GridLineInJ = "GridLineInJ"
LineNumberInJ = "LineNumberInJ"
NumberOfLinesInJ = "NumberOfLinesInJ"

Mesh_list_InJ = "Mesh_list_InJ"
MeshLineInJNumberOfCells = "MeshLineInJNumberOfCells"
MeshLineInJLength = "MeshLineInJLength"
MeshLineInJGeometricRatio = "MeshLineInJGeometricRatio"

Elmerfile = "Elmerfile"

Zones_list = "Zones_list"
Zone_Material_AqueousState_list = "Zone_Material_AqueousState_list"
BoundaryConditionTimeVariation_dict = "BoundaryConditionTimeVariation_dict"

Unstructured_Zone_Material_list = "Unstructured_Zone_Material_list"
Zone_BCKind_list = "Zone_BCKind_list"

UnstructuredHydraulicBC_list = "UnstructuredHydraulicBC_list"

BCValues_list = "BCValues_list"

DarcyVelocity_kind = "DarcyVelocity_kind"
DARCYVELOCITY_BYCOMPONENT = 'By Component'
DARCYVELOCITY_BYFIELD = 'By Field'
DARCYVELOCITY_KINDS = [DARCYVELOCITY_BYCOMPONENT, DARCYVELOCITY_BYFIELD]
DarcyVelocity_list = "DarcyVelocity_list"

DarcyVelocityStatic_list_elmer = "DarcyVelocityStatic_list_elmer"
Boundary_Condition_Head = "Boundary_Condition_Head"
DarcyVelocityStaticElmer = "DarcyVelocityStaticElmer"
DarcyVelocityHeadElmer = "DarcyVelocityHeadElmer"
ReadDarcyVelocity      = "ReadDarcyVelocity"
#========================================================= = "#========================================================="
#============================================================================= = "#============================================================================="
#============================================================================= = "#============================================================================="
#========================================================= = "#========================================================="
Modflow_accl = "Modflow_accl"
Modflow_mxiter = "Modflow_mxiter"
Modflow_hclose = "Modflow_hclose"

Modflow_Default_accl = "Modflow_Default_accl"
Modflow_Default_mxiter = "Modflow_Default_mxiter"
Modflow_Default_hclose = "Modflow_Default_hclose"

Mt3d_mxiter = "Mt3d_mxiter"
Mt3d_iter1 = "Mt3d_iter1"
Mt3d_accl = "Mt3d_accl"
Mt3d_cclose = "Mt3d_cclose"
Mt3d_ConjugateGradientPreconditioner = "Mt3d_ConjugateGradientPreconditioner"
MT3D_CGP_JACOBI = 'Jacobi'
MT3D_CGP_SSOR = 'SSOR'
MT3D_CGP_MIC = 'MIC'
MT3D_CGPS = [MT3D_CGP_JACOBI, MT3D_CGP_SSOR, MT3D_CGP_MIC]

Mt3d_advection = "Mt3d_advection"
MT3D_ADVECTION_UPWIND = 'Upwind'
MT3D_ADVECTION_TVD = 'T.V.D.'
MT3D_ADVECTION_CENTRAL = 'Central'
MT3D_ADVECTIONS = [MT3D_ADVECTION_UPWIND,MT3D_ADVECTION_TVD, MT3D_ADVECTION_CENTRAL]
Mt3d_Default_Discretisation = "Mt3d_Default_Discretisation"
MT3D_DISCRETISATION = [MT3D_ADVECTION_UPWIND,MT3D_ADVECTION_TVD, MT3D_ADVECTION_CENTRAL]

Mt3d_Default_mxiter = "Mt3d_Default_mxiter"
Mt3d_Default_iter1 = "Mt3d_Default_iter1"
Mt3d_Default_accl = "Mt3d_Default_accl"
Mt3d_Default_cclose = "Mt3d_Default_cclose"
Mt3d_Default_CGPreconditioner = "Mt3d_Default_CGPreconditioner"
Mt3d_Default_advection = "Mt3d_Default_advection"

PhreeqC_NumberOfIterations = "PhreeqC_NumberOfIterations"
PhreeqC_ConvergenceCriterion = "PhreeqC_ConvergenceCriterion"
PhreeqC_KNOBS = "PhreeqC_KNOBS"
PhreeqC_pe_step_size_list = "PhreeqC_pe_step_size_list"
PhreeqC_Default_NumberOfIterations = "PhreeqC_Default_NumberOfIterations"
PhreeqC_Default_ConvergenceCriterion = "PhreeqC_Default_ConvergenceCriterion"
PhreeqC_Default_KNOBS = "PhreeqC_Default_KNOBS"
PhreeqC_Default_pe_step_size_list = "PhreeqC_Default_pe_step_size_list"

Available_Output_List_Old = "Available_Output_List_Old"
Available_Minerals_Output_List_Old = "Available_Minerals_Output_List_Old"
Available_ExchangeSpecies_Output_List_Old = "Available_ExchangeSpecies_Output_List_Old"
Available_SurfaceSpecies_Output_List_Old = "Available_SurfaceSpecies_Output_List_Old"
#
##
### Elmer
##
#
Elmer_Linear_Solver = "Elmer_Linear_Solver"
Elmer_Direct_Method = "Elmer_Direct_Method"
Elmer_Iterative_Method = "Elmer_Iterative_Method"
Elmer_Optimize_Bandwidth = "Elmer_Optimize_Bandwidth"
Elmer_Convergence_Tolerance = "Elmer_Convergence_Tolerance"
Elmer_GMRES_Restart = "Elmer_GMRES_Restart"
Elmer_Preconditioning = "Elmer_Preconditioning"
Elmer_ILUT_Tolerance = "Elmer_ILUT_Tolerance"
Elmer_Time_Stepping_Method = "Elmer_Time_Stepping_Method"
Elmer_BDF_Order = "Elmer_BDF_Order" 
Elmer_Iterate_InitialTime = "Elmer_Iterate_InitialTime"
Elmer_Iterate_InitialTimeStep = "Elmer_Iterate_InitialTimeStep"
Elmer_Iterate_SimulationTime = "Elmer_Iterate_SimulationTime"
Elmer_Min_Time_Step = "Elmer_Min_Time_Step"
Elmer_Max_Time_Step = "Elmer_Max_Time_Step"
TimeUnit = "TimeUnit"

Gmsh_Name_File2 = "Gmsh_Name_File2"
ResultDirectory = "ResultDirectory"

TimeStudy = "TimeStudy"

Elmer_Parameters = "Elmer_Parameters"

Elmer_Linear_System_Solver = "Elmer_Linear_System_Solver"
ELMER_LINEAR_SYSTEM_SOLVER_DIRECT = "Direct"
ELMER_LINEAR_SYSTEM_SOLVER_ITERATIVE = "Iterative"
#ELMER_LINEAR_SYSTEM_SOLVER_MULTIGRID = "Multigrid" 
ELMER_LINEAR_SYSTEM_SOLVER = [ELMER_LINEAR_SYSTEM_SOLVER_DIRECT , ELMER_LINEAR_SYSTEM_SOLVER_ITERATIVE]

Elmer_Solver_Direct = "Linear_System_Direct_Method"
ELMER_SOLVER_DIRECT_BANDED = "Banded"
ELMER_SOLVER_DIRECT_UMFPACK = "Umfpack"
ELMER_SOLVER_DIRECT = [ELMER_SOLVER_DIRECT_BANDED , ELMER_SOLVER_DIRECT_UMFPACK]
Elmer_Solver_Direct_Optimize_Bandwidth = "Optimize_Bandwidth"

Elmer_Solver_Iterative = "Linear_System_Iterative_Method"
ELMER_SOLVER_ITERATIVE_CG = "CG"
ELMER_SOLVER_ITERATIVE_CGS = "CGS"
ELMER_SOLVER_ITERATIVE_BICGSTAB = "BICGStab"
ELMER_SOLVER_ITERATIVE_TFQMP = "TFQMP"
ELMER_SOLVER_ITERATIVE_GMRES = "GMRES"
ELMER_SOLVER_ITERATIVE = [ELMER_SOLVER_ITERATIVE_CG , ELMER_SOLVER_ITERATIVE_CGS ,\
ELMER_SOLVER_ITERATIVE_BICGSTAB , ELMER_SOLVER_ITERATIVE_TFQMP , ELMER_SOLVER_ITERATIVE_GMRES]

Linear_System_GMRES_Restart = "GMRES_Restart"

Linear_System_GMRES_Preconditioning = "GMRES_Preconditioning"
GMRES_PRECONDITIONING_NONE = "None"
GMRES_PRECONDITIONING_DIAGONAL = "Diagonal"
GMRES_PRECONDITIONING_ILU0 = "ILU0"
GMRES_PRECONDITIONING_ILU1 = "ILU1"
GMRES_PRECONDITIONING_ILU2 = "ILU2"
GMRES_PRECONDITIONING_ILU3 = "ILU3"
GMRES_PRECONDITIONING_ILU4 = "ILU4"
GMRES_PRECONDITIONING_ILU5 = "ILU5"
GMRES_PRECONDITIONING_ILU6 = "ILU6"
GMRES_PRECONDITIONING_ILU7 = "ILU7"
GMRES_PRECONDITIONING_ILU8 = "ILU8"
GMRES_PRECONDITIONING_ILU9 = "ILU9"
GMRES_PRECONDITIONING_ILUT = "ILUT"
GMRES_PRECONDITIONING_MULTIGRID = "Multigrid"
GMRES_PRECONDITIONING = [GMRES_PRECONDITIONING_NONE ,\
GMRES_PRECONDITIONING_DIAGONAL , GMRES_PRECONDITIONING_ILU0 , GMRES_PRECONDITIONING_ILU1 ,\
GMRES_PRECONDITIONING_ILU2 , GMRES_PRECONDITIONING_ILU3 ,\
GMRES_PRECONDITIONING_ILU4 , GMRES_PRECONDITIONING_ILU5 ,\
GMRES_PRECONDITIONING_ILU6 , GMRES_PRECONDITIONING_ILU7 ,\
GMRES_PRECONDITIONING_ILU8 , GMRES_PRECONDITIONING_ILU9 ,\
GMRES_PRECONDITIONING_ILUT , GMRES_PRECONDITIONING_MULTIGRID ]

Linear_System_ILUT_Tolerance = "ILUT_Tolerance"
#
#========================================================="
#========================================================="
#Temperature
TemperatureVariable = "TemperatureVariable"

#========================================================="
#========================================================="
Iterate_Algorithm = "Iterate_Algorithm"
ITERATE_ALGORITHM_ONESTEP = 'NI'
ITERATE_ALGORITHM_CC = 'CC'
ITERATE_ALGORITHM_TC = 'TC'
ITERATE_ALGORITHM_TT = 'TT'
ITERATE_ALGORITHMS = [ITERATE_ALGORITHM_ONESTEP,ITERATE_ALGORITHM_CC]
#ITERATE_ALGORITHMS = [ITERATE_ALGORITHM_ONESTEP,ITERATE_ALGORITHM_CC,ITERATE_ALGORITHM_TC, ITERATE_ALGORITHM_TT]

Iterate_InitialTime = "Iterate_InitialTime"
Iterate_InitialTimeStepSize = "Iterate_InitialTimeStepSize"
Iterate_SimulationTime = "Iterate_SimulationTime"

Iterate_MinTimeStep = "Iterate_MinTimeStep"
Iterate_MaxTimeStep = "Iterate_MaxTimeStep"
Iterate_PicardMaxOfIterations = "Iterate_PicardMaxOfIterations"
Iterate_PicardTargetNumber = "Iterate_PicardTargetNumber"
Iterate_CouplingPrecision = "Iterate_CouplingPrecision"
Iterate_RelaxationMinFactor = "Iterate_RelaxationMinFactor"
Iterate_RelaxationMaxFactor = "Iterate_RelaxationMaxFactor"
Iterate_Default_Algorithm = "Iterate_Default_Algorithm"
PorosityState = "PorosityState"

IOutputs_list = 'IOutputs_list'
ITitle = 'ITitle'
ISubTitle = 'ISubTitle'
IFrequency = 'IFrequency'
IRotate = 'IRotate'
ISave = 'ISave'
ISaveFrequency = 'ISaveFrequency'
IOutputFormat = 'IOutputFormat'
IOutputFormat_List = 'IOutputFormat_List'

GlobalOutputs_list = 'GlobalOutputs_list'
GlobalDates_list = 'GlobalDates_list'
GlobalPlotUnits_list = 'GlobalPlotUnits_list'

SavingFormat = 'SavingFormat'
DataFileCWD = 'DataFileCWD'
AvailableSpecies_list = 'AvailableSpecies_list'
AvailableDates_list = 'AvailableDates_list'
SpeciesSelection_list = 'SpeciesSelection_list'
DatesSelection_list = 'DatesSelection_list'

PostprocessingVariablesToPlot_list = "PostprocessingVariablesToPlot_list"
Postprocessing1_Parameters_list = "Postprocessing1_Parameters_list"
Postprocessing2_VariablesToPlot_list = "Postprocessing2_VariablesToPlot_list"
Postprocessing2_tmin = "Postprocessing2_tmin"
Postprocessing2_tmax = "Postprocessing2_tmax"
#========================================================="
Parallel_NumberOfNodes = "Parallel_NumberOfNodes"
#========================================================="
AqueousSolutionToEquilibrate_list = "AqueousSolutionToEquilibrate_list"

InitialConditions_list = "InitialConditions_list"
BoundaryConditions_list = "BoundaryConditions_list"

PyOutputHandler = "PyOutputHandler"

class ParameterSet:
    """define all geoi parameters
    an instance contains a working set of parameters
    """

    def __init__(self):
        l = []

        l.append( Parameter(Mode_is_structured, True, "main mode of the geoi software") )

        l.append(  Parameter(Title,'title', 'Title of the study/case'
                      , lambda s: s is not None and s is not "" and s.find(' ') is -1) )

        check_is_number = IS_NUMBER
        check_is_string = IS_STRING
#----------------------------------
#  SetUnitsFrame Parameters
#----------------------------------
        l.append( Parameter(Concentration_Unit, description = "unit for concentration"
                            , values=['moles/l','moles/m3'] ) )
        l.append( Parameter(Density_Unit, values=['kg/m3'], description="unit for density") )
        l.append( Parameter(Dispersivity_Unit, values=['m'], description="unit for dispersitivity (Longitudinal Dispersivity") )
        l.append( Parameter(EffectiveDiffusion_Unit, values=['m2/s', "m2/year"], description="unit for effective diffusion") )
        l.append( Parameter(Enthalpy_Unit, values=['J/kg', "kJ/mol"], description="unit for enthalpy (of formation)") )
        l.append( Parameter(Head_Unit, values=['m']) ) # TODO
        l.append( Parameter(Length_Unit, values=['m']) )
        l.append( Parameter(Permeability_Unit, values=['m/s',"m/year"], description="unit for permeability_Unit") )
        l.append( Parameter(Temperature_Unit, values=['Celcius', "Kelvin"], description="unit for temperature") )
        l.append( Parameter(Time_Unit, values=['s',"year"],  description="unit of time") )

#-------------------------------
#  WhichSolverFrame Parameter
#-------------------------------
        check = lambda s: s in SOLVERS
        l.append( Parameter(Solver, SOLVER_MODFLOW_MT3D_PHREEQC, "the solver software to use", check) )
        l.append( Parameter(PorosityState, values=['constant porosity',"variable porosity"], description="?") )

        l.append( Parameter(Thermal, False, "set if thermal mode is on") )
#---------------------------------
#  Chemistry
#---------------------------------
        check = lambda c: c in CHEMISTRY_TOOLS
        l.append( Parameter(ChemistryTool, CHEMISTRY_TOOL_PHREEQC, "the chemistry software to use", check) )

        l.append( Parameter(IMPORTED_CHEMISTRY_DB, ChemistryDB(), "the imported chemistry database instance") )
        l.append( Parameter(CUSTOM_CHEMISTRY_DB, ChemistryDB(), "the custom chemistry database instance, user edited") )
#---------------------------------
#  Transport
#---------------------------------
        l.append( Parameter(CUSTOM_MATERIAL_DB, MaterialDB(), "the custom material database instance, user edited") )

#-------------------------------------------------------------
#  InteractiveXYPlotFrame Parameters (Time)
#-------------------------------------------------------------
        # TODO
        check_is_list = lambda t: isinstance(t,list)
        l.append( Parameter(InteractiveXYPlot_Parameters_list, [0, 0, 1], "??", check_is_list) )
        l.append( Parameter(InteractiveXYPlot_AqueousComponentsToPlot_list, [], "??", check_is_list) )
        l.append( Parameter(InteractiveXYPlot_AvailableAqueousComponents_list, [], "??", check_is_list) )
#---------------------------------------------------------------------------
#  InteractiveXYPlotFrame Parameters (Space & Time)
#---------------------------------------------------------------------------
        l.append( Parameter(InteractiveXYPlot_Space_and_Time_Parameters_list, [PLOT_I, 10], "??", check_is_list) )
        l.append( Parameter(InteractiveXYPlot_Space_and_Time_ElementsToPlot_list, [], "??", check_is_list) )

#----------------------------------------
# TablesFrame Parameters
#----------------------------------------
        l.append( Parameter(ExpectedOutputs_list, [], "??", check_is_list) )
        l.append( Parameter(Quantity_list, ['', 'AqueousConcentration', 'Concentration'], "??", check_is_list) )
        l.append( Parameter(ExpectedOutputsQuantity_list, [], "??", check_is_list) )
        l.append( Parameter(Times_list, [], "??", check_is_list) )

#----------------------------------------
# PostprocessingXYPlotFrame Parameter
#----------------------------------------
        l.append( Parameter(PostprocessingXYPlot_Parameters_list, [], "??", check_is_list) )
        l.append( Parameter(Postprocessing_ElementsToPlot_list, [], "??", check_is_list) )

#-------------------------------------------------------
#  InteractiveContoursFrame Parameters
#------------------------------------------------------
        l.append( Parameter(InteractiveContours_Parameters_list, [], "??", check_is_list) )
        l.append( Parameter(InteractiveContours_AqueousComponentsToPlot_list, [], "??", check_is_list) )
        l.append( Parameter(InteractiveContours_AvailableAqueousComponents_list, [], "??", check_is_list) )

#------------------------------------------------------------------
# PostprocessingContoursFrame Parameters
#------------------------------------------------------------------
        l.append( Parameter(PostprocessingContours_Parameters_list, [200, 's'], "??", check_is_list) )
        l.append( Parameter(PostprocessingContours_AqueousComponentsToPlot_list, [], "??", check_is_list) )
        l.append( Parameter(PostprocessingContours_AvailableAqueousComponents_list, [], "??", check_is_list) )

#-------------------------------------------------------------
#  DefaultDatabaseFrame Parameter
#----------------------------------------------------------------
        l.append( Parameter(DefaultDatabase, DATABASE_LLNL, 'Default Thermochemical Database name') )
        l.append( Parameter(CurrentDatabasePath, "", "Full path of the current Thermochemical Database") )
#     l.append( Parameter(CurrentDatabase, "", "current Thermochemical Database instance") )
        l.append( Parameter(Available_Databases_list, [DATABASE_PHREEQC], '?? - useless ? ') )

#-----------------------------------------
#  AqueousStateFrame Parameters
#-----------------------------------------
        l.append( Parameter(AqueousStates_list, [], '', check_is_list) )
#  In the aqueousStates_Properties_list, the properties for each aqueous state (solution) are given:')
#  It means that this list has the same number of elements as the aqueousStates_list.')
#  The positions of an Aqueous State and its own properties are the same in the two lists')
#  Each element of the aqueousStates_Properties_list is a list, containing:')
#')
#    - The Temperature of the corresponding Aqueous Solution.')
#    - The pH of the corresponding Aqueous Solution.')
#    - The pe of the corresponding Aqueous Solution.')
        l.append( Parameter(AqueousStates_Properties_list, [], '', check_is_list) )
#  The aqueousStates_Species_list is the list containing the species of each aqueous solution.')
#  This is a list of lists: there are 3 levels:')
#')
#    - The aqueousStates_Species_list contains the species and their concentrations')
#      for all aqueous solutions.')
#    - The second level contains the lists of all species and their concentrations')
#      within the considered solution, the three first elements are prespectively pH, T and pe')
#    - Each third-level list contains a species with its concentration in the considered solution.')
        l.append( Parameter(AqueousStates_Species_list, [], '', check_is_list) )

        l.append( Parameter(AqueousStates_Default_Temperature, 25.0, '', IS_NUMBER ) )
        check_is_real_positive = lambda x: IS_NUMBER(x) and x >= 0
        l.append( Parameter(AqueousStates_Default_pH, 7.0, '', check_is_real_positive) )
        l.append( Parameter(AqueousStates_Default_pe, 4.0, '', IS_NUMBER) )
        l.append( Parameter(AqueousStates_Default_Eh, 0.23668639, '', IS_NUMBER) )

#-----------------------------------------------
#  State_EquilibriumPhasesFrame Parameters
#-----------------------------------------------
        l.append( Parameter(AqueousStates_MineralPhases_list, [], '', check_is_list) )
        l.append( Parameter(AqueousStates_MineralPhases_Properties_list, [], '', check_is_list) )

#-------------------------------------------------
#  State_IonExchangeFrame Parameters
#-------------------------------------------------
        l.append( Parameter(AqueousStates_ExchangeSpecies_list, [], '', check_is_list) )
        l.append( Parameter(AqueousStates_ExchangeSpecies_Properties_list, [], '', check_is_list) )
#---------------------------------------------------------
#  State_SurfaceComplexationCompositionFrame Parameters
#---------------------------------------------------------
        l.append( Parameter(AqueousStates_SurfaceSpecies_list, [], '', check_is_list) )
        l.append( Parameter(AqueousStates_SurfaceSpecies_Properties_list, [], '', check_is_list) )
#----------------------------------------------
#  State_KineticRatesFrame Parameters
#----------------------------------------------
        l.append( Parameter(KineticRates_list, [], '', check_is_list) )
        l.append( Parameter(AqueousStates_KineticRates_list, [], '', check_is_list) )
        l.append( Parameter(AqueousStates_KineticRates_Properties_list, [], '', check_is_list) )

        l.append( Parameter(Rate, RATE_STANDARD, '') )
        l.append( Parameter(TemkinNumber, 1.0, '', check_is_number) )
        l.append( Parameter(KineticConstant, 1.0, '', check_is_number) )
        l.append( Parameter(InitialExchangeSurface, 1.0, '', check_is_number) )
        l.append( Parameter(SphereModelExponent_On, False, '') )
        l.append( Parameter(SphereModelExponent, 0.6666, '', check_is_number) )

#-------------------------------------
#  State_GasPhaseFrame Parameters
#-------------------------------------
        l.append( Parameter(AqueousStates_Gas_list, [], '', check_is_list) )
        l.append( Parameter(AqueousStates_Gas_Properties_list, [], '', check_is_list) )

#-------------------------------------
#  Chemistry database Parameters
#-------------------------------------


#        l.append( Parameter(Database_Solution_Species_list, [], '', check_is_list) )
#        l.append( Parameter(Database_Components_list, [], '', check_is_list) )
#        l.append( Parameter(Database_ComponentSpecies_Name_list, [], '', check_is_list) )
#        l.append( Parameter(Database_ComponentSpecies_Formula_list, [], '', check_is_list) )
#        l.append( Parameter(Database_Components_Log_k_list, [], '', check_is_list) )
#        l.append( Parameter(Database_Components_gfw_list, [], '', check_is_list) )
#
#        l.append( Parameter(Database_AqueousSpecies_list, [], '', check_is_list) )
#        l.append( Parameter(Database_AqueousSpecies_Formula_list, [], '', check_is_list) )
#        l.append( Parameter(Database_AqueousSpecies_Log_k_list, [], '', check_is_list) )
#        l.append( Parameter(Database_AqueousSpecies_Species_list, [], '', check_is_list) )
#
#        l.append( Parameter(Database_Phases_Names_list, [], '', check_is_list) )
#        l.append( Parameter(Database_Phases_Formula_list, [], '', check_is_list) )
#        l.append( Parameter(Database_Phases_Species_list, [], '', check_is_list) )
#        l.append( Parameter(Database_Phases_Log_k_list, [], '', check_is_list) )
#        l.append( Parameter(Database_Phases_Delta_h_list, [], '', check_is_list) )
#
#        l.append( Parameter(Database_ExchangeMasterSpecies_list, [], '', check_is_list) )
#        l.append( Parameter(Database_ExchangeMasterSpecies_Formula_list, [], '', check_is_list) )
#
#        l.append( Parameter(Database_Exchange_Species_list, [], '', check_is_list) )
#
#        l.append( Parameter(Database_SurfaceMasterSpecies_list, [], '', check_is_list) )
#        l.append( Parameter(Database_SurfaceMasterSpecies_Formula_list, [], '', check_is_list) )
#
#        l.append( Parameter(Database_SurfaceSpecies_list, [], '', check_is_list) )
#        l.append( Parameter(Database_SurfaceSpecies_Log_k_list, [], '', check_is_list) )
#        l.append( Parameter(Database_SurfaceSpecies_Reactants_list, [], '', check_is_list) )
#
#        l.append( Parameter(Database_gases_Names_list, [], '', check_is_list) )

##-----------------------------------------
##  AqueousMasterSpeciesFrame Parameters
##-----------------------------------------
#        l.append( Parameter(Components_list, [], '', check_is_list) )
#        l.append( Parameter(ComponentSpecies_Name_list, [], '', check_is_list) )
#        l.append( Parameter(ComponentSpecies_Formula_list, [], '', check_is_list) )
#        l.append( Parameter(Components_Properties_list, [], '', check_is_list) )
#
##---------------------------------------------------
##  AqueousSpeciesFrame Parameters
##---------------------------------------------------
#        l.append( Parameter(AqueousSpecies_list, [], '', check_is_list) )
#        l.append( Parameter(AqueousSpecies_Formula_list, [], '', check_is_list) )
#        l.append( Parameter(AqueousSpecies_Properties_list, [], '', check_is_list) )
#        l.append( Parameter(AqueousSpecies_Species_list, [], '', check_is_list) )
#
##----------------------------------
##  MineralPhasesFrame Parameters
##----------------------------------
#        l.append( Parameter(MineralPhases_list, [], '', check_is_list) )
#        l.append( Parameter(MineralPhases_Formula_list, [], '', check_is_list) )
#        l.append( Parameter(MineralPhases_Properties_list, [], '', check_is_list) )
#        l.append( Parameter(MineralPhases_Species_list, [], '', check_is_list) )
#  Initialization parameters:
        l.append( Parameter(Default_log_k, 0.0, '', check_is_number) )
        l.append( Parameter(Default_Enthalpy, 0.0, '', check_is_number) )
        l.append( Parameter(Default_Density, 3000.0, '', check_is_number) )
#------------------------------------------
#  ExchangeMasterSpeciesFrame Parameters
#------------------------------------------
#        l.append( Parameter(ExchangeMasterSpecies_list, [], '', check_is_list) )
#        l.append( Parameter(ExchangeMasterSpecies_Formula_list, [], '', check_is_list) )
#
##------------------------------------
##  ExchangeSpeciesFrame Parameters
##------------------------------------
#        l.append( Parameter(ExchangeSpecies_list, [], '', check_is_list) )
#        l.append( Parameter(ExchangeSpecies_Properties_list, [], '', check_is_list) )
#        l.append( Parameter(ExchangeSpecies_Reactants_list, [], '', check_is_list) )
#  Debye-Huckel Parameters
        l.append( Parameter(DebyeHuckel_a, 4.0, '', check_is_number) )
        l.append( Parameter(DebyeHuckel_b, 0.0, '', check_is_number) )
#        l.append( Parameter(Default_DebyeHuckel_a, 4.0, '', check_is_number) )
#        l.append( Parameter(Default_DebyeHuckel_b, 0.0, '', check_is_number) )

#----------------------------------------------------------
#  Data_SurfaceComplexationMasterSpeciesFrame Parameters
#----------------------------------------------------------
#        l.append( Parameter(SurfaceMasterSpecies_list, [], '', check_is_list) )
#        l.append( Parameter(SurfaceMasterSpecies_Formula_list, [], '', check_is_list) )
#----------------------------------------------------
#  Data_SurfaceComplexationSpeciesFrame Parameters
#----------------------------------------------------
#        l.append( Parameter(SurfaceSpecies_list, [], '', check_is_list) )
#        l.append( Parameter(SurfaceSpecies_Properties_list, [], '', check_is_list) )
#        l.append( Parameter(SurfaceSpecies_Reactants_list, [], '', check_is_list) )

#--------------------------------
#  MaterialsFrame Parameters
#--------------------------------
        check_is_dict = lambda h: isinstance(h, dict)
        l.append( Parameter(Materials_list, [], '', check_is_list) )
        l.append( Parameter(Materials_Properties_list, [], '', check_is_list) )
        l.append( Parameter(DiffusionLaws_dict, {}, '', check_is_dict) )
        l.append( Parameter(DiffusionState, DIFFUSIONSTATE_CONSTANT, '', lambda s: s in DIFFUSIONSTATES) )

        #  Initialization parameters:
        l.append( Parameter(MaterialName, '', '', None) )
        l.append( Parameter(KxPermeability, 1.0, '', check_is_number) )
        l.append( Parameter(KyPermeability, 1.0, '', check_is_number) )
        l.append( Parameter(KzPermeability, 1.0, '', check_is_number) )
        l.append( Parameter(EffectivePorosity, 1.0, '', check_is_number) )
        l.append( Parameter(EffectiveDiffusion, 4.e-10, '', check_is_number) )
        l.append( Parameter(LongitudinalDispersivity, 1.0, '', check_is_number) )
        l.append( Parameter(TransverseDispersivity, 0.1, '', check_is_number) )

        l.append( Parameter(MaterialConductivity, 0.0, '', check_is_number) )
        l.append( Parameter(SpecificHeatCapacity, 0.0, '', check_is_number) )
        l.append( Parameter(HydraulicConductivity, 0.0, '', check_is_number) )


        l.append( Parameter(var_diff_list, [], '', check_is_list) )

#--------------------------------------------------------------------
#  DefaultParametersFrame Parameters (dedicated to MaterialsFrame)
#--------------------------------------------------------------------
                #  Initialization parameters:
        l.append( Parameter(DefaultMaterialName, '', '', None) )
        l.append( Parameter(DefaultKxPermeability, 1.0, '', check_is_number) )
        l.append( Parameter(DefaultKyPermeability, 1.0, '', check_is_number) )
        l.append( Parameter(DefaultKzPermeability, 1.0, '', check_is_number) )
        l.append( Parameter(DefaultEffectivePorosity, 1.0, '', check_is_number) )
        l.append( Parameter(DefaultEffectiveDiffusion, 4.e-10, '', check_is_number) )
        l.append( Parameter(DefaultLongitudinalDispersivity, 0.0, '', check_is_number) )
        l.append( Parameter(DefaultTransverseDispersivity, 0.0, '', check_is_number) )
        l.append( Parameter(DefaultConductivity, 1.0, '', check_is_number) )

#--------------------------------------------
#  MeshBuildingUpDirectionFrame Parameters
#--------------------------------------------
        l.append( Parameter(MeshLine_Direction, DIRECTION_I, '', lambda s: s in DIRECTIONS) )

#--------------------------------
#  MeshLineInIFrame Parameters
#--------------------------------
        check_is_int = IS_INTEGER
        l.append( Parameter(GridLineInI, GRIDLINE_NEW, '', lambda s: s in GRIDLINES) )
        l.append( Parameter(LineNumberInI, 0, '', check_is_int) )
        l.append( Parameter(NumberOfLinesInI, 0, '', check_is_int) )

#------------------------------------------
#  MeshLineInIParametersFrame Parameters
#------------------------------------------
        l.append( Parameter(Mesh_list_InI, [(1,1.,1.),(0,0.,1.),\
                                                      (0,0.,1.),\
                                                      (0,0.,1.),\
                                                      (0,0.,1.),\
                                                      (0,0.,1.),\
                                                      (0,0.,1.),\
                                                      (0,0.,1.)], '', check_is_list) )
        l.append( Parameter(MeshLineInINumberOfCells, 0, '', check_is_int) )
        l.append( Parameter(MeshLineInILength, 0, '', check_is_int) )
        l.append( Parameter(MeshLineInIGeometricRatio, 1, '', check_is_int) )

#--------------------------------
#  MeshLineInJFrame Parameters
#--------------------------------
        l.append( Parameter(GridLineInJ, GRIDLINE_NEW, '', lambda s: s in GRIDLINES) )
        l.append( Parameter(LineNumberInJ, 0, '', check_is_int) )
        l.append( Parameter(NumberOfLinesInJ, 0, '', check_is_int) )
#------------------------------------------
#  MeshLineInJParametersFrame Parameters
#------------------------------------------
        l.append( Parameter(Mesh_list_InJ, [(1,1.,1.),(0,0.,1.),\
                                                      (0,0.,1.),\
                                                      (0,0.,1.),\
                                                      (0,0.,1.),\
                                                      (0,0.,1.),\
                                                      (0,0.,1.),\
                                                      (0,0.,1.)], '', check_is_list) )
        l.append( Parameter(MeshLineInJNumberOfCells, 0, '', check_is_int) )
        l.append( Parameter(MeshLineInJLength, 0, '', check_is_int) )
        l.append( Parameter(MeshLineInJGeometricRatio, 1, '', check_is_int) )
#---------------------------------------
#  SetZonesFrame Parameters
#---------------------------------------
        l.append( Parameter(Zones_list, [], '', check_is_list))
        l.append( Parameter(Zone_Material_AqueousState_list, [], '', check_is_list) )
        l.append( Parameter(BoundaryConditionTimeVariation_dict, {}, '', check_is_dict) )

        l.append( Parameter(Unstructured_Zone_Material_list, [], '', check_is_list) )

#-------------------------------
#  HydraulicBCFrame Parameter
#-------------------------------
        l.append( Parameter(Zone_BCKind_list, [], '', check_is_list) )

        l.append( Parameter(UnstructuredHydraulicBC_list, [], '', check_is_list) )
#-------------------------------------
#  HydraulicBCValuesFrame Parameter
#-------------------------------------
        l.append( Parameter(BCValues_list, [], '', check_is_list) )

#-------------------------------------
#  SetDarcyVelocity Parameter: Mt3d
#-------------------------------------
        l.append( Parameter(DarcyVelocity_kind, DARCYVELOCITY_BYCOMPONENT, '', lambda s: s in DARCYVELOCITY_KINDS) )
        l.append( Parameter(DarcyVelocity_list, ['0.0', '0.0', '0.0'], '', check_is_list) )
#-------------------------------------
#  SetDarcyVelocity Parameter: Elmer
#-------------------------------------
        l.append( Parameter(DarcyVelocityStatic_list_elmer, ['0.0', '0.0', '0.0'], '', check_is_list) )
        l.append( Parameter(Boundary_Condition_Head, [], '', check_is_list) )
        l.append( Parameter(DarcyVelocityStaticElmer, "False", "", check_is_string) )
        l.append( Parameter(DarcyVelocityHeadElmer, "False", "", check_is_string) )
        l.append( Parameter(ReadDarcyVelocity, "False", "", check_is_string) )

#--------------------------------------------------------
#  SolverParametersFrame Parameters
#--------------------------------------------------------
        l.append( Parameter(Modflow_accl, 1.0, 'Modflow acceleration Under Relaxation Factor', check_is_number) )
        l.append( Parameter(Modflow_mxiter, 200, 'Modflow: Number Of Iterations', check_is_int) )
        l.append( Parameter(Modflow_hclose, 1e-11, 'Modflow: Residual Convergence', check_is_number) )

        # TODO: useless now
        l.append( Parameter(Modflow_Default_accl, 1.0, 'Modflow acceleration Under Relaxation Factor', check_is_number) )
        l.append( Parameter(Modflow_Default_mxiter, 200, 'Modflow: Number Of Iterations', check_is_int) )
        l.append( Parameter(Modflow_Default_hclose, 1e-11, 'Modflow: Residual Convergence', check_is_number) )

        #Mt3d
        l.append( Parameter(Mt3d_mxiter, 1, 'Mt3d: Number Of Iterations', check_is_int) )
        l.append( Parameter(Mt3d_iter1, 30, '', check_is_int) )
        l.append( Parameter(Mt3d_accl, 1.0, '', check_is_number) )
        l.append( Parameter(Mt3d_cclose, 1e-15, '', check_is_number) )
        l.append( Parameter(Mt3d_ConjugateGradientPreconditioner, MT3D_CGP_JACOBI, '', lambda s: s in MT3D_CGPS) )
        l.append( Parameter(Mt3d_advection, MT3D_ADVECTION_TVD, '', lambda s: s in MT3D_ADVECTIONS) )
        l.append( Parameter(Mt3d_Default_Discretisation, MT3D_ADVECTION_TVD,\
                           'advection spatial discretisation', lambda s: s in MT3D_DISCRETISATION) )

        # TODO: useless now
        l.append( Parameter(Mt3d_Default_mxiter, 1, 'Mt3d: Number Of Iterations', check_is_int) )
        l.append( Parameter(Mt3d_Default_iter1, 30, '', check_is_int) )
        l.append( Parameter(Mt3d_Default_accl, 1.0, '', check_is_number) )
        l.append( Parameter(Mt3d_Default_cclose, 1e-16, '', check_is_number) )
        l.append( Parameter(Mt3d_Default_CGPreconditioner, MT3D_CGP_JACOBI, '', lambda s: s in MT3D_CGPS) )
        l.append( Parameter(Mt3d_Default_advection, MT3D_ADVECTION_TVD, '', lambda s: s in MT3D_ADVECTIONS) )

        #  PhreeqC:
        l.append( Parameter(PhreeqC_NumberOfIterations, 500, 'Number Of Iterations', check_is_int) )
        l.append( Parameter(PhreeqC_ConvergenceCriterion, 1.e-15, '', check_is_number) )
        l.append( Parameter(PhreeqC_KNOBS, '', '') )
        l.append( Parameter(PhreeqC_pe_step_size_list, ['0', ''], '', check_is_list) )

        # TODO: useless now
        l.append( Parameter(PhreeqC_Default_NumberOfIterations, 500, 'Number Of Iterations', check_is_int) )
        l.append( Parameter(PhreeqC_Default_ConvergenceCriterion, 1.e-15, '', check_is_number) )
        l.append( Parameter(PhreeqC_Default_KNOBS, '', '') )
        l.append( Parameter(PhreeqC_Default_pe_step_size_list, ['0', ''], '', check_is_list) )

        # alphabetic lists
        l.append( Parameter(Available_Output_List_Old, [], "Save of the Available Output List in alphabetic order", check_is_list))
        l.append( Parameter(Available_Minerals_Output_List_Old, [], "Save of the Available Mineral Output List in alphabetic order", check_is_list))
        l.append( Parameter(Available_ExchangeSpecies_Output_List_Old, [],\
        "Save of the Available Exchange Species List in alphabetic order", check_is_list)) 
        l.append( Parameter(Available_SurfaceSpecies_Output_List_Old, [],\
        "Save of the Available Surface Species List in alphabetic order", check_is_list))  
        
        
#        l.append(Parameter(Elmer_Parameters, {'preconditioner': 'NEUM', 'accelerator': 'cg', 'iterSolver': 1000, 'tolSolver': 1e-14, #'thetaScheme': 1, 'library': 'Gauss'}, '', check_is_dict))
        
        l.append( Parameter(Elmer_Linear_Solver, 'Iterative', 'Linear System Solver', check_is_string))
        l.append( Parameter(Elmer_Direct_Method, 'Banded', 'Direct Method', check_is_string))
        l.append( Parameter(Elmer_Iterative_Method, 'CG', 'Iterative Method', check_is_string))
        l.append( Parameter(Elmer_Optimize_Bandwidth, 'False', 'Optimize Bandwidth', check_is_string))
        l.append( Parameter(Elmer_Convergence_Tolerance, 1.e-8, 'Convergence Tolerance', check_is_number))
        l.append( Parameter(Elmer_GMRES_Restart, 0, 'Linear System GMRES Restart', check_is_int))
        l.append( Parameter(Elmer_Preconditioning, 'ILU1', 'Preconditioning', check_is_string))
        l.append( Parameter(Elmer_ILUT_Tolerance, 1.e-8, 'ILUT Tolerance', check_is_number))
        l.append( Parameter(Elmer_Time_Stepping_Method, 'BDF' , 'Time Stepping Method', check_is_string))
        l.append( Parameter(Elmer_BDF_Order, '1' , 'BDF Order', check_is_string))
        l.append( Parameter(Elmer_Iterate_InitialTime, 0 , 'Elmer Initial Time', check_is_number))
        l.append( Parameter(Elmer_Iterate_InitialTimeStep, 1 , 'Elmer Step Size', check_is_number))
        l.append( Parameter(Elmer_Iterate_SimulationTime, 1 , 'Elmer Simulation Time', check_is_number))
        l.append( Parameter(Elmer_Min_Time_Step, 0 , 'Elmer Min Time Step', check_is_number))
        l.append( Parameter(Elmer_Max_Time_Step, 0 , 'Elmer Max Time Step', check_is_number))
        l.append( Parameter(TimeUnit, 'year' , 'Elmer Times Unit', check_is_string))
        
        l.append( Parameter(Gmsh_Name_File2, 'toto.msh' , "Gmsh Name File" , check_is_string)) 
        l.append( Parameter(ResultDirectory, '' , "Directory in which the results will be written", check_is_string)) 
        
        l.append( Parameter(TemperatureVariable, 'False' , 'Temperature variable or constant', check_is_string)) 
        
        # Time Study
        
        l.append( Parameter(TimeStudy, [] , "List of the points and the parameters", check_is_list)) 
#------------------------------------------------
#  IterateFrame Parameters
#------------------------------------------------
        l.append( Parameter(Iterate_Algorithm, ITERATE_ALGORITHM_ONESTEP, '', lambda s: s in ITERATE_ALGORITHMS) )
        l.append( Parameter(Iterate_InitialTime, 0, '', check_is_int) )
        l.append( Parameter(Iterate_InitialTimeStepSize, 1, '', check_is_int) )
        l.append( Parameter(Iterate_SimulationTime, 10., '', check_is_int) )

        #  for CC, TC, or TT Algorithms:
        l.append( Parameter(Iterate_MinTimeStep, 1, '', check_is_int) )
        l.append( Parameter(Iterate_MaxTimeStep, 2, '', check_is_int) )
        l.append( Parameter(Iterate_PicardTargetNumber, 20, '', check_is_int) )
        l.append( Parameter(Iterate_PicardMaxOfIterations, 30, '', check_is_int) )
        l.append( Parameter(Iterate_CouplingPrecision, 1.e-5, '', check_is_number) )
        l.append( Parameter(Iterate_RelaxationMinFactor, 0.5, '', check_is_number) )
        l.append( Parameter(Iterate_RelaxationMaxFactor, 1.05, '', check_is_number) )
        l.append( Parameter(Iterate_Default_Algorithm, ITERATE_ALGORITHM_ONESTEP,\
                           'coupling algorithm ', lambda s: s in ITERATE_ALGORITHMS) )

#------------------------------------------------
#  Interactive plot parameters
#------------------------------------------------
        l.append( Parameter(IOutputs_list, default=[], description="Interactively ploted outputs", checkFunction=check_is_list))
        l.append( Parameter(ITitle, default='Etumos Interactive plot', description="Set the title", checkFunction=check_is_string))
        l.append( Parameter(ISubTitle, default='', description="under the title (new line)", checkFunction=check_is_string))
        l.append( Parameter(IFrequency, default=20, description="Display frequency", checkFunction=check_is_int))
        l.append( Parameter(IRotate, default= False, description="Axis directions"))
        l.append( Parameter(ISave, default= False, description="Saving Outputs"))
        l.append( Parameter(ISaveFrequency, default= 40, description="Frequency of the ouputs save"))
        l.append( Parameter(IOutputFormat, default= 'ps', description="Outputs Format"))
        l.append( Parameter(IOutputFormat_List, default= ['png', 'ps'], description="List of Outputs Format"))


#------------------------------------------------
#  Global plot parameters
#------------------------------------------------
        l.append( Parameter(GlobalOutputs_list, default=[], description="Global ploted outputs", checkFunction=check_is_list))
        l.append( Parameter(GlobalDates_list, default=[], description="Dates for outputs plot", checkFunction=check_is_list))
        l.append( Parameter(GlobalPlotUnits_list, default=['sec', 'hour', 'day', 'year'], description="Dates units for outputs plot", checkFunction=check_is_list))
        
#------------------------------------------------
#  Post Simulation Display
#------------------------------------------------
        l.append( Parameter(DataFileCWD, default= '\tNone\t\t\t', description="Directory of the datafile", checkFunction=check_is_string))
        l.append( Parameter(SavingFormat, default= 'png', description="Saving Format", checkFunction=check_is_string))
        l.append( Parameter(AvailableSpecies_list, default= [], description="", checkFunction=check_is_list))
        l.append( Parameter(AvailableDates_list, default= [], description="", checkFunction=check_is_list))
        l.append( Parameter(SpeciesSelection_list, default= [], description="", checkFunction=check_is_list))
        l.append( Parameter(DatesSelection_list, default= [], description="", checkFunction=check_is_list))

#--------------------------------------
# PostprocessingVariablesToPlotFrame
#--------------------------------------
        l.append( Parameter(PostprocessingVariablesToPlot_list, [], '', check_is_list) )

        l.append( Parameter(Postprocessing1_Parameters_list, [], '', check_is_list) )

        l.append( Parameter(Postprocessing2_VariablesToPlot_list, [], '', check_is_list) )
        l.append( Parameter(Postprocessing2_tmin, 0, '', check_is_int) )
        l.append( Parameter(Postprocessing2_tmax, 1, '', check_is_int) )

#----------------------------------------
# ParallelFrame Parameter
#----------------------------------------
        l.append( Parameter(Parallel_NumberOfNodes, 1, '', check_is_int) )

#-------------------------------------
#  EquilibrateFrame Parameter
#-------------------------------------
        l.append( Parameter(AqueousSolutionToEquilibrate_list, [], '', check_is_list) )
# added for Elmer
        l.append( Parameter(InitialConditions_list, [], '', check_is_list) )
        l.append( Parameter(BoundaryConditions_list, [], '', check_is_list) )
# added for python post

        l.append( Parameter(PyOutputHandler, "", '', check_is_string) )


        self.params = {}
        for p in l:
            if p.getName() in self.params:
                warnings.warn("duplicate key : " + p.getName())
            self.params[p.getName()] = p

    def count(self):
        return len(self.params)

    def getParamNames(self):
        keys =  self.params.keys()
        keys.sort()
        return keys

    def getParam(self, name):
        "get a Parameter by name. You should use the constants defined in this namespace"
        return self.params[name]

    def getParamValue(self, name):
        "get the value of a Parameter by name. You should use the constants defined in this namespace"
        return self.getParam(name).getValue()

    def __repr__(self):
        s = "ParameterSet : " + str(len(self.params)) + " parameters\n"
        keys = self.params.keys()
        keys.sort()
        for p in keys:
            s += str(self.params[p]) + "\n"
        return s

#    def __deepcopy__(self, memo={}):
#        from copy import deepcopy
#        result = self.__class__()
#        memo[id(self)] = result
#        result.__init__(deepcopy(tuple(self), memo))
#        return result

    def clone(self):
        return copy.deepcopy(self)
#        cloned = ParameterSet()
#        keys = self.params.keys()
#        for k in keys:
#            cloned.params[k] = self.params[k].clone()
##            cloned.getParam(k).setValue(self.getParam(k).getValue())
#        return cloned


    def read(self, file):
        dico = {}
#        for l in file.readlines():
#            code = l
#            print "code=", code
#            exec code in dico
        exec "from geoi.chemistry_db import ChemistryDB" in dico
        exec "from geoi.material_db  import MaterialDB" in dico
        exec file.read() in dico

        if '__builtins__' in dico:
            del dico['__builtins__']
        del dico['ChemistryDB']
        dico.pop('var_diff_list', None)

        # now check and set the values
        for k,v in dico.iteritems():
            # backwards compatibility : may happen that first letter is lower-case
            k = k[0].upper() + k[1:]
            #
            # printing string associated to parameter
            #
            #print str(k)
            if k not in self.params:
                warnings.warn("unknown parameter " + str(k) + " of value " + str(v) )
            else:
                p = self.getParam(k)
                if p.checkValue(v):
                    p.setValue(v)
                else:
                    warnings.warn("Bad Value " + str(v) + " of type " + str(type(v)) + " for parameter " + str(k) )

    def save(self, file):
        NOT_TO_BE_SAVED = {IMPORTED_CHEMISTRY_DB:True}

        file.write("###### Geoi Parameter Set Save File generated on " + str(datetime.date.today()) + "#####\n" )
        keys = self.params.keys()
        keys.sort()
        for k in keys:
            if k in NOT_TO_BE_SAVED:
                continue
            p = self.getParam(k)
            file.write('#' + p.getName() + " : " + p.getDescription() + "\n" )
            file.write(p.getName() + ' = ' )
            v = p.getValue()
#            if isinstance(v, str) or isinstance(v, unicode):
#                v = '"' + v + '"'
            file.write(repr(v) + "\n"  )

    def __eq__(self, o):
        # must have same nb of parameters
        if len(self.params) != len(o.params):

            return False

        # check that all params are the same
        keys = self.params.keys()
        keys.sort()
        for k in keys:
            p = self.getParam(k)
            if k not in o.params:
                return False
            p2 = o.getParam(k)
            if p != p2:
                return False

        return True

    def __ne__(self, o):
        return not self.__eq__(o)

if __name__ == '__main__':
    p = ParameterSet()
    #print p.getParam(Title)
    #print p
    import traceback
    filename = "../../data/truc2.geoi"
    try:
        case = open (filename,'r')
    except:
        traceback.print_exc()
        exit(1)
    p.read(case)
    #print p

    import StringIO
    out = StringIO.StringIO()
    p.save( out )
#   print out.getvalue()
    out.seek(0)

    p2 = ParameterSet()
    p2.read(out)
    #print p2
    print p == p2
    #print p2


