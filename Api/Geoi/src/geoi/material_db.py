import warnings
import pprint
import re
import copy

MATERIAL = "MATERIAL"
MATERIALDB = "CUSTOM_MATERIAL_DB"

PARTS = [MATERIAL,MATERIALDB]

COMMENT = '#'
EQUALS = ' = '

NAME = 'NAME'

INDENT = 2

class MaterialDB:

    def __init__(self, db=None):
        if db is None:
            self.db = dict([(i,{}) for i in PARTS])
        else:
            self.db = db

    def getDatabaseDict(self):
        return self.db

    def getMaterials(self):
        return self.db[MATERIAL]

    def _readNextLine(self, it):
        line = None
        try:
            line = it.next().rstrip()
        except StopIteration:
            pass
        return line

    def _makeFloat(self, s):
        if s is None or s == '':
            return ''
        return float(s)

    def clone(self):
        print "clone MaterialDB"
        c = MaterialDB()
        c.db = copy.deepcopy(self.db)
        return c

    def toExhaustiveStringDump(self):
        s = self.__class__.__name__ + "(" + pprint.pformat(self.db, indent=INDENT) + ")\n"
        #s = repr(self.db)
        return s

    def toSummaryStringRepresentation(self):
        s = ""
        max_elts = 5
        indent = INDENT
        parts = self.db.keys()
        parts.sort()
        for k in parts:
            v = self.db[k]
            nb = len(v)
            s += "===== " + k + " : " + str(nb) + " elements =====\n"
            # creates a hash with at most max_elts elements
            nb = max(nb, max_elts)
            to_print = {}
            for i in v.keys()[0:max_elts]:
                to_print[i] = v[i]

            s += pprint.pformat(to_print, indent=indent) + "\n\n"
        return s

    def __repr__(self):
        return self.toExhaustiveStringDump()

    def __eq__(self, o):
        equal = self is o or self.db == o.db
        return equal

    def __ne__(self, o):
        return not self.__eq__(o)

    def __str__(self):
        return self.toExhaustiveStringDump()

if __name__ == '__main__':
    import traceback
    file = 'llnl.dat'
    path = "../../data/" + file
    try:
        fh = open(path,"r")
    except:
        traceback.print_exc()

    db = MaterialDB()

    print db.toSummaryStringRepresentation()
    #print db
