from geoi.actions.user_db_table_action import UserDBTableAction
from geoi import parameters
from geoi.parameter import Parameter, IS_NUMBER, IS_POSITIVE_NUMBER
from geoi.chemistry_db import *
from geoi.chemistry_equation import Equation

from geoi.models.common_user_db_table_model import CommonUserDBTableModel


HEADERS = {EQUATION:"Surface Species Equation",
           LOGK:"Surface Species LogK"}
ORDER = [EQUATION, LOGK]

HELP = """
<h1>Surface Species</h1>

This frame is used to define the name of a surface binding site and the
associated surface species formula that is used in simulations.
Only additions or modifications, specific to the ongoing simulation, of the available data file
are introduced here.


<br><br>
In the table the <b>green</b> entries are those defined by the user,
while the others are those imported from the database, the last ones cannot be edited or renamed.

"""

class SurfaceSpecies(UserDBTableAction, CommonUserDBTableModel):
    """
    Add and Edit surface species, using those imported from the chemistry database
    """

    def __init__(self, win, params_mgr):
        CommonUserDBTableModel.__init__(self, HEADERS, ORDER)
        UserDBTableAction.__init__(self, params_mgr, win, "Surface Complexation Species",
                              "add and edit custom Surface Species (SURFACE_SPECIES)", self,
                    help=HELP)

    def getImportedDB(self, params):
        return params.getParamValue(parameters.IMPORTED_CHEMISTRY_DB).getSurfaceSpecies()

    def getUserDB(self, params):
        return params.getParamValue(parameters.CUSTOM_CHEMISTRY_DB).getSurfaceSpecies()

    def getParamsForNewEntry(self):

        l = []
        not_empty = lambda s: s != ""

#        p = Parameter(HEADERS[ELEMENT], "", 'Specie Name')
#        p.setCheckFunction(lambda v: self.entryNameCallback(p, v))
#        l.append(p)

        p = Parameter(HEADERS[EQUATION], "", "Association reaction for surface species.\n"+\
                                             "The defined species must be the first species\n"+\
                                             "to the right of the equal sign.\n")
                                             
        p.setCheckFunction(lambda s: s != "" and self.entryNameCallback(p, s))
        l.append(p)

        l.append(Parameter(HEADERS[LOGK], "","Log K for a master species is 0.0. Default is 0.0.", not_empty))

        return l

