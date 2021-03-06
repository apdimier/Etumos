class UserDBTableDataModel:
    """
    This class is a base class for data model, for actions displaying a list of entries
    mixed from imported ones and user edited ones in a table, and allowing
    custom editing of individual rows/entries

    A data model is created empty, and will be filled/loaded using load() method
    """

    def __init__(self):
        pass

    def load(self, parameter_set):
        self._param_set = parameter_set

    def getParameterSet(self):
        return self._param_set

    def getStringValueAt(self, name, col):
        "return a string for the cell value at (row, col)"
        return str(self.getValueAt(name, col))

    def getStringsForEntry(self, name):
        return [self.getStringValueAt(name, col) for col in xrange(self.getColumnCount())]

    # =============== MAIN INTERFACE TO IMPLEMENT/OVERRIDE  =========================

    def getEntryIdColumn(self):
        "return the column containing the name of entry"
        return 0

    def deleteEntry(self, name):
        "delete the entry  : entry must be a custom one"
        pass

    def getParamsForNewEntry(self):
        """
        return a list of Parameter instances, intented to create a new entry from scratch
        """
        pass

    def getParamsForNewEntryFrom(self, name):
        """
        return a list of Parameter instances, initialized if needed in a way
        to allow the creation of a new entry with same values. So appropriate
        parameters such as Name or Id should be set to their default values, and thr others
        initialized from this entry current values
        """
        pass

    def getParamsForEntryEdit(self, name):
        """
        return a list of Parameter instances, initialized if needed in a way
        to allow the edition of current entry.
        """
        pass

    def submitEditedEntry(self, name, params_list):
        """
        modify if needed and appropriate the entry at row from the list of parameters.
        Typically it should check if the name or id is new, and then insert it in the custom db

        Return the new name if the entry has been modified, or ""
        """
        pass

    def submitNewEntry(self, params_list):
        """
        add this entry if possible (e.g if name does not collide with others...)
        return the name for this new entry, or "" if not new
        """
        pass


    def getEntriesCount(self):
        "return the number of rows/entries"
        pass

    def getColumnCount(self):
        "return the number of columns"
        pass

    def getHeaders(self):
        "return a list of strings, holding the name of table columns"
        pass

    def getAllStringValues(self):
        "return a matrix of all entries"
        pass

    def getValueAt(self, name, col):
        "return a string for the cell value at (name, col)"
        pass

    def isCustomEntry(self, name):
        "return True iff entry  is a custom aka user entry"
        pass
