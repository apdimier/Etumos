import warnings
import copy

def ALWAYS_TRUE_FUNCTION(v):
    return True


def IS_INTEGER(x):
    try:
        x = int(x)
        return True
    except:
        return False
        
def IS_NUMBER(x):
    try:
        x = float(x)
        return True
    except:
        return False

def IS_POSITIVE_NUMBER(x):
    return IS_NUMBER(x) and float(x) >= 0
    
def IS_ION(x):
    for i in x:
        print " ion ",i
        if not i.isalpha():
            if i.isdigit():
              if "(" not in x or ")" not in x: return 0
    return 1

def IS_STRING(x):
    try:
        x = str(x)
        return True
    except:
        return False
    
def IS_UNIT(x):
    for i in x:
        print "is unit ",i
        if i not in ["mmol/l","mol/l"] : return 0
    return 1

def IS_IN_LIST(x, list):
    return x in list

def inSecondsConverter(date, integer = True):
    # This function converts a date in form '20 days' or '1000 y' in the corresponding seconds numbers
    
    ref = [('seconds', 1), ('minutes', 60), ('hours', 3600), ('days', 86400), ('years', 31557600)]
    value = eval(date.split()[0])
    unit  = date.split()[1][0:3]
    
    i = 0
    found = False
    
    while not found and i < len(ref):
        if unit in ref[i][0][0:3]:
            found = True
            coef = ref[i][1]
        else:
            i += 1
    
    if not found:
        raise "Unit is not recognized"
    else:
        if integer:
            return int(value*coef)
        else:
            return value*coef

def inUnitConverter(date, unit):
    # This function converts a date in seconds to the value in specified unit
    
    ref = [('seconds', 1.), ('minutes', 60.), ('hours', 3600.), ('days', 86400.), ('years', 3.15576e+7)]
    
    i = 0
    found = False
    
    while not found and i < len(ref):
        if unit[0:3] in ref[i][0][0:3]:
            found = True
            coef = ref[i][1]
        else:
            i += 1
    
    if not found:
        raise "Unit is not recognized"
    else:
        return float(date)/coef

class Parameter:
    "the base class for defining a Geoi Parameter"

    def __init__(self, name, default=None, description="", checkFunction=None, values=None):
        """create a parameter

        keyword arguments:
            name - the parameter name
            default - the default value. if None, the first value in values will be used
            so in that case it must not be None or empty

        """


        self.name = name

        if default is None:
            if values is None or len(values) == 0:
                pass
            else:
                default = values[0]

        self.default = default
        self.description = description
        self.checkFunction = checkFunction
        self.values = values

        if checkFunction is None:
            if values is None:
                self.checkFunction = ALWAYS_TRUE_FUNCTION
            else:
                self.checkFunction = lambda x: IS_IN_LIST(x, values)


        self.value = default

    def clone(self):
        p = Parameter(self.name, copy.deepcopy(self.default), self.description, self.checkFunction, copy.deepcopy(self.values))
        v = self.getValue()
        p.setValue(copy.deepcopy(v))
        return p

    def getPossibleValues(self):
        """Return the list of possible values if any, or None"""
        return self.values

    def _transformValue(self, x):
        if IS_INTEGER(x):
            x = int(x)
        elif IS_NUMBER(x):
            x = float(x)
        return x

    def getValue(self):
        "the current value of the parameter"
        return self.value

    def setValueFromString(self, string, check=True):
        """
        usually, user-input values coming from GUIs are string values
        and may need to be converted to the actual type of value
        For instance "2" may be converted to int, "4e-2" to float etc...
        This function tries to automatically deduce the appropriate type
        of the value but may fail in some cases.
        So you may OVERRIDE it if you need a specific behaviour
        """
        v = self._transformValue(string)
        self.setValue(v, check)

    def setValueAsIs(self, value):
        """
        it is the opposite from setValueFromString() : it sets the value
        without trying to transform it, without any check
        """
        self.value = value

    def setValue(self, v, check=True):
        """
        set inconditionnaly the value of the parameter but may emit
        a warning if the value is not valid
        See checkValue()
        """
        if check and not self.checkValue(v):
            warnings.warn("Bad value " + str(v) + " for parameter " + str(self))
        #self.value = self._transformValue(v)
        self.value = v

    def getName(self):
        "the name of the parameter"
        return self.name

    def getDefault(self):
        "the default value of the parameter"
        return self.default

    def setDefault(self, v):
        "set the default value of the parameter, should usually be set from the constructor"
        self.default = self._transformValue(v)

    def setCheckFunction(self, function):
        self.checkFunction = function

    def getDescription(self):
        "the description of the parameter"
        return self.description

#    def clone(self):
#        """clone the object"""
#        p = Parameter(self.getName(), self.getDefault(), self.getDescription(), self.checkFunction)
#        p.setValue( copy.deepcopy(self.getValue()) )
#        v = self.getValue()
#        if hasattr(v, "clone"):
#            v = v.clone()
#        p.setValue(v)
#        return p

    def checkValue(self, value):
        """
        check if the given value is valid for this parameter
        N.B. if no check function has been defined, always return True

        Return: boolean
        """
        if self.checkFunction is None:
            return True
        else:
            return self.checkFunction(self._transformValue(value))



    def __deepcopy__(self, memo={}):
        p = self.clone()
        memo[id(self)] = p
        return p

    def __repr__(self):
        return self.getName() + "=" + str(self.getValue()) + "(" + str(self.getDefault()) + ") : " + self.getDescription()


    def __eq__(self, o):
#        print self.getValue(), o.getValue()
        v, ov = self.getValue(), o.getValue()
        return self.getName() == o.getName() and type(v) == type(ov) and v == ov

    def __ne__(self, o):
        return not self.__eq__(o)

if __name__ == '__main__':
    p = Parameter("toto", 0, 'fait pas grand chose', IS_INTEGER)
    print p
    from copy import deepcopy
    p2 = deepcopy(p)
    print p2
