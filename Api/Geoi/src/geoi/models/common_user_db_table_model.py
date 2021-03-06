from user_db_table_model import UserDBTableDataModel


class CommonUserDBTableModel(UserDBTableDataModel):
    """
    This class implements a UserDBTableDataModel from common situations where entries
    are taken from two lists of dictionaries (called ImportedDB and UserDB)
    , where one key is used as the entry name/id.


    This is the case for example for AqueousMasterSpecies, AqueousSecondarySpecies...

    There are 3 methods left to implement: getImportedDB(), getUserDB() and getParamsForNewEntry()

    You may override getEntryIdColumn() if the entry name/id is not obtained with the first key
    of the order list.

    """

    def __init__(self, mapping, order):
        """
        headers is a dict mapping entry names/keys to user/display names

        order is a list of headers keys : this order will be used by the model
        """
        UserDBTableDataModel.__init__(self)
        self._mapping = mapping
        self._order = order


    # ======== INTERFACE TO IMPLEMENT ==========
    def getImportedDB(self, params):
        """ MUST BE OVERRIDEN IN DERIVED CLASSES !!!
        accessor for the imported db : dictionary of entries"""
        raise

    def getUserDB(self, params):
        """ MUST BE OVERRIDEN IN DERIVED CLASSES !!!
        accessor for the user db : dictionary of entries"""
        raise

    def entryNameCallback(self, parm, value):
        "useful function for derived classes"
        params = self.getDataModel().getParameterSet()
        db = self.getImportedDB(params)
        userdb = self.getUserDB(params)
        return value and value != '' and value not in db \
                and (value not in userdb or value == parm.getDefault())

    # ===== ACCESSOrS =====


    def getMapping(self):
        return self._mapping

    def getOrder(self):
        return self._order

    def _getImportedDB(self):
        return self.getImportedDB(self.getParameterSet())

    def _getUserDB(self):
        return self.getUserDB(self.getParameterSet())

    def getEntry(self, name):
        "return the entry using its name"
        db = self._getUserDB()
        if not name in db:
            db = self._getImportedDB()
        return db[name]

    # ======== IMPLEMENTATION OF UserDBTableDataModel interface ==========

    def deleteEntry(self, name):
        "delete the entry at given row : entry must be a custom one"
        if not self.isCustomEntry(name):
            raise ValueError, "entry %s must be a custom one " % name
        del self._getUserDB()[name]

    def getParamsForNewEntryFrom(self, name):
        """
        return a list of Parameter instances, initialized if needed in a way
        to allow the creation of a new entry with same values. So appropriate
        parameters such as Name or Id should be set to their default values, and thr others
        initialized from this entry current values
        """
        # should be a generic implementation : assume that the entry name/id
        # is the first element of the order list; so reuse getParamsForEntryEdit()
        params = self.getParamsForEntryEdit(name)
        params[self.getEntryIdColumn()].setValue("", check=False)
        return params

    def getParamsForEntryEdit(self, name):
        """
        return a list of Parameter instances, initialized if needed in a way
        to allow the edition of current entry.
        """
        # should be a generic implementation : use the params from getParamsForNewEntry()
        # then init then from the entry

        params = self.getParamsForNewEntry()
        for (col, p) in enumerate(params):
            v = self.getValueAt(name, col)
            p.setDefault(v)
            p.setValue(v, check=False)

        return params

    def submitEditedEntry(self, name, params_list):
        """
        modify if needed and appropriate the entry at row from the list of parameters.
        Typically it should check if the name or id is new, and then insert it in the custom db

        Return the new name if the entry has been modified, or ""
        """
        new_name = params_list[self.getEntryIdColumn()].getValue()

        if new_name == name:
            # check that it is new
            new_entry = self._makeEntryFromParams(params_list)
            old_entry = self._makeEntryFromParams(self.getParamsForEntryEdit(name))
            if params_list == self.getParamsForEntryEdit(name):
#            if new_entry == old_entry:
                return False
            self._getUserDB()[name] = new_entry

        else:
            if self.submitNewEntry(params_list):
                self.deleteEntry(name)
            else:
                return False
        return new_name

    def _makeEntryFromParams(self, params_list):
        entry = {}
        for (key, p) in zip(self.getOrder(), params_list):
            entry[key] = p.getValue()
        return entry

    def submitNewEntry(self, params_list):
        """
        add this entry if possible (e.g if name does not collide with others...)

        """
        new_id = params_list[self.getEntryIdColumn()].getValue()
        userdb = self._getUserDB()
        db = self._getImportedDB()
        if new_id in userdb or new_id in db:
            return ""

        userdb[new_id] = self._makeEntryFromParams(params_list)
        return new_id

    def getEntriesCount(self):
        "return the number of entries"
        return len(self._getImportedDB()) + len(self._getUserDB())

    def getColumnCount(self):
        "return the number of columns"
        return len(self.getOrder())

    def getHeaders(self):
        "return a list of strings, holding the name of table columns"
        m = self.getMapping()
        return [m[k] for k in self.getOrder()]

    def getAllStringValues(self):
        values = []
        for db in [self._getUserDB(), self._getImportedDB()]:
            keys = db.keys()
            keys.sort()
            for k in keys:
                values.append( self.getStringsForEntry(k))
        return values

    def getValueAt(self, name, col):
        "return a string for the cell value at (name, col)"
        return self.getEntry(name)[self.getOrder()[col]]

    def isCustomEntry(self, name):
        "return True iff entry at row # row is a custom aka user entry"
        return name in self._getUserDB()
