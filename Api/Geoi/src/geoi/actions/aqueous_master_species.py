from geoi.actions.user_db_table_action import UserDBTableAction
from geoi import parameters
from geoi.parameter import Parameter, IS_POSITIVE_NUMBER, IS_NUMBER
from geoi.chemistry_db import *
from geoi.models.common_user_db_table_model import CommonUserDBTableModel

HEADERS = {ELEMENT:"Element Name", SPECIES:"Master Species Name",
           FORMULA:"Formula", GFW:"Molar Weight (g/mol)", LOGK:"Alkalinity"}
ORDER = [ELEMENT, SPECIES, FORMULA, GFW, LOGK]


HELP = """
<h1>AqueousMasterSpecies</h1>

The user can define here addenda to the available database.
<br>

<b>Aqueous master species</b> are to be defined here in association with the molar weight
and the alkalinity.<br>
Master species are not reduced here to species names but can be associated to different
oxydation states.

<br>
In the table the <b>green</b> entries are those defined by the user.<br>
The other entries are those imported from the database, they cannot be edited or renamed.

"""




class AqueousMasterSpecies(UserDBTableAction, CommonUserDBTableModel):
    """
    Add and Edit solution master species, using those imported from the chemistry database
    """

    def __init__(self, win, params_mgr):

        CommonUserDBTableModel.__init__(self, HEADERS, ORDER)

        UserDBTableAction.__init__(self, params_mgr, win, "Aqueous Master Species",
                              "add and edit custom Aqueous master species", self, help=HELP)



    # ======== IMPLEMENTATION of CommonUserDBTableModel INTERFACE  ==========

    def getImportedDB(self, params):
        return params.getParamValue(parameters.IMPORTED_CHEMISTRY_DB).getSolutionMasterSpecies()

    def getUserDB(self, params):
        return params.getParamValue(parameters.CUSTOM_CHEMISTRY_DB).getSolutionMasterSpecies()

    def getParamsForNewEntry(self):
        """
        return a list of Parameter instances, intented to create a new entry from scratch
        """

        l = []
        not_empty = lambda s: s != ""

        p = Parameter(HEADERS[ELEMENT], "",
                           'An element name: the element name must begin with a capital letter,\n followed by small ones.\nExamples: Ca or K')
        p.setCheckFunction(lambda v: self.entryNameCallback(p, v))
        l.append(p)

        l.append(Parameter(HEADERS[SPECIES], "",
                           'Primary species name, including valence.\nExamples:\n   - For Na: Na+\n   - For Si: H4SiO4'
                           , not_empty) )
        l.append(Parameter(HEADERS[FORMULA], "",
                           'Solution master species formula.\nExamples:\n   - For Na: Na\n   - For Si: SiO2'
                           , not_empty) )

        is_empty_or_positive_number = lambda x: x == "" or IS_POSITIVE_NUMBER(x)
        l.append(Parameter(HEADERS[GFW], "",
                           'gram formula weight of the primary master species (leave it empty if unknown)'
                           , is_empty_or_positive_number ) )

        l.append(Parameter(HEADERS[LOGK], "",
                           'Alkalinity contribution of the master species (0 if N/A)'
                           , IS_NUMBER) )

        return l



