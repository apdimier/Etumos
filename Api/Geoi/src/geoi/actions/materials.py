
import wx

from geoi import parameters
from geoi.parameter import Parameter, IS_NUMBER, IS_POSITIVE_NUMBER
from geoi.parameters import *
from geoi.actions.user_db_table_action import UserDBTableAction
from geoi.models.common_user_db_table_model import CommonUserDBTableModel


HEADERS = {MaterialName:"Material Name",KxPermeability:"Kx",KyPermeability:"Ky",KzPermeability:"Kz",\
           EffectivePorosity:"Eff. Porosity", EffectiveDiffusion:"Eff. Diffusion",\
           LongitudinalDispersivity:"Long. Dispersivity", TransverseDispersivity:"Trans. Dispersivity",\
           MaterialConductivity:"Thermal Conductivity"}
ORDER = [MaterialName,KxPermeability,KyPermeability,KzPermeability,\
           EffectivePorosity, EffectiveDiffusion,\
           LongitudinalDispersivity, TransverseDispersivity,MaterialConductivity]

HELP = """
<h1>Material definition</h1>

<br>
This frame is used to define for each material within the domain, its <b>permeability</b>, its <b>effective porosity</b>, its<B>effective diffusion</b>, its <b> longitudinal and transverse dispersivity</b>, and its <b>thermal conductivity</b><br>
<b>Materials</b> are identified by theirname.

"""

class Materials(UserDBTableAction, CommonUserDBTableModel):
    """
    Add and Edit materials
    """

    def __init__(self, win, params_mgr):
        CommonUserDBTableModel.__init__(self, HEADERS, ORDER)

        UserDBTableAction.__init__(self, params_mgr, win, "Materials",
                              "To edit and add custom Materials ", self,
                    help=HELP)

    def getImportedDB(self, params):
#        print "toto",type(params.getParamValue(parameters.CUSTOM_MATERIAL_DB))
#        return params.getParamValue(parameters.IMPORTED_MATERIAL_DB).getMaterials()
        #
        # if we want to introduce a material base ....otherwie we return a {}
        #
        return {}

    def getUserDB(self, params):
        return params.getParamValue(parameters.CUSTOM_MATERIAL_DB).getMaterials()

    def getParamsForNewEntry(self):
        l = []
        not_empty = lambda s: s != ""
        is_number_or_empty = lambda s: s == "" or IS_NUMBER(s)

        p = Parameter(HEADERS[MaterialName], "",
                           'name: name of the material to be given\n in association with an aqeous state\nover a part f the mesh')
        p.setCheckFunction(lambda v: self.entryNameCallback(p, v))
        l.append(p)

        l.append(Parameter(HEADERS[KxPermeability], "1.0","Kx in S.I. units: [m2]", IS_POSITIVE_NUMBER))
        l.append(Parameter(HEADERS[KyPermeability], "1.0","Ky in S.I. units: [m2]", IS_POSITIVE_NUMBER) )
        l.append(Parameter(HEADERS[KzPermeability], "1.0","Kz in S.I. units: [m2]", IS_POSITIVE_NUMBER) )
        l.append(Parameter(HEADERS[EffectivePorosity], "1.0","Eff. Porosity: dimensionless", IS_POSITIVE_NUMBER) )
        l.append(Parameter(HEADERS[EffectiveDiffusion], "4.e-10","Eff. Diffusion in S.I. units: [m2/s]", IS_POSITIVE_NUMBER) )
        l.append(Parameter(HEADERS[LongitudinalDispersivity], "0.0","Long. Dispersivity in S.I. units: [m]", IS_POSITIVE_NUMBER) )
        l.append(Parameter(HEADERS[TransverseDispersivity], "0.0","Trans. Dispersivity in S.I. units: [m]", IS_POSITIVE_NUMBER) )
        l.append(Parameter(HEADERS[MaterialConductivity], "0.0","Thermal Conductivity in S.I. units: [W/m/K]", IS_POSITIVE_NUMBER) )


        return l

    # override to customize
#    def _createTable(self, parent):
#        table = UserDBTableAction._createTable(self, parent)
#        table.SetColumnWidth(1, 100)
#        return table

#    def createEntryEditDialog(self, params_list):
#        d = UserDBTableAction.createEntryEditDialog(self, params_list)
#        d.getEditorByName(HEADERS[FORMULA]).SetEditable(False)
#        return d
