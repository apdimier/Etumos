from geoi.actions.user_db_table_action import UserDBTableAction
from geoi import parameters
from geoi.parameter import Parameter, IS_NUMBER, IS_POSITIVE_NUMBER
from geoi.chemistry_db import *
from geoi.chemistry_equation import Equation
from geoi.actions.aqueous_master_species import AqueousMasterSpecies
from geoi.models.common_user_db_table_model import CommonUserDBTableModel


HEADERS = {ELEMENT:"Element Name",
           FORMULA:"Chemical Formula", EQUATION:"Equation", GFW:"Molar Weight (g/mol)", LOGK:"Alkalinity (log k)"}
ORDER = [ELEMENT, FORMULA, EQUATION, LOGK ]

HELP = """
<h1>AqueousSecondarySpecies</h1>

The user can define here addenda to the available database.

<br>
In the table the <b>green</b> entries are those defined by the user.
The other entries are those imported from the database, and cannot be edited or renamed.

"""

class AqueousSecondarySpecies(UserDBTableAction, CommonUserDBTableModel):
    """
    Add and Edit solution secondary species, using those imported from the chemistry database
    """

    def __init__(self, win, params_mgr):
        CommonUserDBTableModel.__init__(self, HEADERS, ORDER)

        UserDBTableAction.__init__(self, params_mgr, win, "Aqueous Secondary Species",
                              "add and edit custom Aqueous secondary species (SOLUTION_SPECIES)", self,
                    help=HELP)

    def getImportedDB(self, params):
        return params.getParamValue(parameters.IMPORTED_CHEMISTRY_DB).getSolutionSecondarySpecies()

    def getUserDB(self, params):
        return params.getParamValue(parameters.CUSTOM_CHEMISTRY_DB).getSolutionSecondarySpecies()

    def getParamsForNewEntry(self):
        l = []
        not_empty = lambda s: s != ""

        p = Parameter(HEADERS[ELEMENT], "", 'Species Name')
        p.setCheckFunction(lambda v: self.entryNameCallback(p, v))
        l.append(p)

        l.append(Parameter(HEADERS[FORMULA], "",
                           "Aqueous Species formula. It is the first right member of the "
                           "formation reaction."
                           , not_empty) )

        l.append(Parameter(HEADERS[EQUATION], "",
                           'Chemical Formation Reaction : specie is the first term of right member\n'
                           ' and so should have a coefficient equals to 1'
                           , self.equationCallback) )

        l.append(Parameter(HEADERS[LOGK], "",
                           'Alkalinity contribution of the specie (0 if N/A)'
                           , IS_NUMBER) )

        return l


    def equationCallback(self, value):
        try:
            eq = Equation(str(value))
            rightmember = eq.parseRightMembers()[0]
            if rightmember[1] == 1:
                d = self.getCurrentEntryEditDialog()
                if d is not None:
                    editor = d.getEditorByName(HEADERS[FORMULA])
                    editor.SetValue( str(rightmember[0]) )
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
