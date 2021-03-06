
import wx

from geoi import parameters
from geoi.parameter import Parameter, IS_NUMBER, IS_POSITIVE_NUMBER
from geoi.chemistry_db import *
from geoi.chemistry_equation import Equation
from geoi.actions.user_db_table_action import UserDBTableAction
from geoi.models.common_user_db_table_model import CommonUserDBTableModel


HEADERS = {NAME:"Name",
           FORMULA:"Chemical Formula", EQUATION:"Equation", DENSITY:"Density (kg/m3)", LOGK:"Log K"}
ORDER = [NAME, FORMULA, EQUATION, LOGK, DENSITY ]

HELP = """
<h1>Mineral Phases</h1>

<br>
This frame is used to define the <b>name</b>, the <b>chemical reaction</b>, <B>logK</b>,
and <b>Temperature dependency</b> of log K for each mineral that is used for
speciation and transport simulations.

<br><br>
Only additions and modifications of the available simulation database are introduced here.
The name must be less than 20 characters,

<br><br>
In the table the <b>green</b> entries are those defined by the user.
The other entries are those imported from the database, and cannot be edited or renamed.

"""

class MineralPhases(UserDBTableAction, CommonUserDBTableModel):
    """
    Add and Edit mineral phases, using those imported from the chemistry database
    """

    def __init__(self, win, params_mgr):
        CommonUserDBTableModel.__init__(self, HEADERS, ORDER)

        UserDBTableAction.__init__(self, params_mgr, win, "Mineral Phases",
                              "Add and Edit custom mineral phases (PHASES)", self,
                    help=HELP)

    def getImportedDB(self, params):
        return params.getParamValue(parameters.IMPORTED_CHEMISTRY_DB).getMineralPhases()

    def getUserDB(self, params):
        return params.getParamValue(parameters.CUSTOM_CHEMISTRY_DB).getMineralPhases()

    def getParamsForNewEntry(self):
        l = []
        not_empty = lambda s: s != ""
        is_number_or_empty = lambda s: s == "" or IS_NUMBER(s)


        p = Parameter(HEADERS[NAME], "", 'Name')
        p.setCheckFunction(lambda v: self.entryNameCallback(p, v))
        l.append(p)

        l.append(Parameter(HEADERS[FORMULA], "",
                           "Chemical Formula for the defined phase. It is extracted from the dissolution reaction."
                           , not_empty) )

        l.append(Parameter(HEADERS[EQUATION], "",
"""
Dissolution reaction for mineral phase to aqueous species.
The phase in the chemical reaction must be the first term of the left member and
has necessary 1 as stoichiometric coefficient.
Aqueous species ( including e-) are given with stoichiometric coefficients and valence.
Example: Forsterite Mg2SiO4 + 4 H+ = SiO2 + 2 H2O + 2 Mg++
""" ,
         self.equationCallback) )

        l.append(Parameter(HEADERS[LOGK], "",
                           'Equilibrium Constant at 25 Celsius degrees.'
                           , IS_NUMBER) )

        l.append(Parameter(HEADERS[DENSITY], "",
                           'Density, leave it empty if not applicable'
                           , is_number_or_empty) )

        return l

    # override to customize
    def _createTable(self, parent):
        table = UserDBTableAction._createTable(self, parent)
        table.SetColumnWidth(1, 100)
        return table

    def equationCallback(self, value):
        try:
            eq = Equation(str(value))
            leftmember = eq.parseLeftMembers()[0]
            if leftmember[1] == 1:
                d = self.getCurrentEntryEditDialog()
                if d is not None:
                    editor = d.getEditorByName(HEADERS[FORMULA])
                    editor.SetValue( str(leftmember[0]) )
            else:
                return False
        except ValueError, err:
            #print err
            return False
        return True


    def createEntryEditDialog(self, params_list):
        d = UserDBTableAction.createEntryEditDialog(self, params_list)
        d.getEditorByName(HEADERS[FORMULA]).SetEditable(False)
        return d
