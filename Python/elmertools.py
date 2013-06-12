from posttables import Table
from listtools import toList
import string
import numpy
#
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#
def getTimeUnifiedTables(*ttuple):
    """ principe :
    on envoie N tables dans la fonction, et on recupere
    N tables dont les instants sont l'union des instants
    de chacune des tables initiales
    """
    
    tablist=toList(ttuple)
    glue=tuple([x.getColumn(0).tolist() for x in tablist])
    if not len(glue):return
    temporary=glue[0]
    for element in glue[1:len(glue)]:
        for item in element:
            if item not in temporary:
                temporary.append(item)
    temporary.sort()

    
    new_tables=[]
    for tabl in tablist:
        extravalues=interpolate(temporary,tabl)
        colt=tabl.getColumnTitles()
        tnew=Table(tabl.getTitle())
        tnew.addColumn(colt[0],temporary)
        tnew.addColumn(colt[1],extravalues)
        new_tables.append(tnew)
        pass
    return new_tables

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
def interpolate(TimeGlobColumn,oneTable):
    """ This function aim to interpolate one flux table to the whole
        times in the time_globa_column
        if the value of time to interpolate is in the oneTable Time, the
        interpolation will be linear :
          for  t(i) < t <= t(i+1)
               lamda  = (t - t(i))/(t(i+1)-t(i))
               flux_t = (1-lamda)*flux_i + lamda*flux_(i+1)
               
          if (t-t(0))/t(1) < 10e-6 then consider flux_t=flux_0
    """
    time   = oneTable.getColumn(0)
    flux_l = oneTable.getColumn(1)
    # create an empty flux time
    interp_flux = len(TimeGlobColumn)*[0]

    # boucle for every time in the Time Global Table
    for ti in TimeGlobColumn:
        i = TimeGlobColumn.index(ti)
        # if the time is out of the interval time of the current flux,
        #   put it to 0 (see initialisation before)
        if ti < time[0]:
            pos=1
        elif ti > time[-1]:
            pos=len(time)-1
        # else: - add the time to the list, even if it exists
        #       - sort list
        #       - get the index of the time in the new sorted list
        #       - get lamda with the next and the previous time
        #         of the old list
        #       - interpolate flux with the same next and previous
        else:
            local_time = time.tolist()
            local_time.append(ti)
            local_time.sort()
            pos = local_time.index(ti)
        lamda = (ti-time[pos-1])/(time[pos]-time[pos-1])
        l_flux = (1-lamda)*flux_l[pos-1]+lamda*flux_l[pos]
        interp_flux[i] = l_flux
    # transforme list to a numerical array
    result_column = Numeric.array(interp_flux)
    return result_column

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
class Dico:
    """ Dico class definition as dictionnary, ou les cles sont ordonnees en fifo
    """
    #---------------------------------------------------------------------------
    def __init__(self, name=''):
        """
        Constructor
        """
        self._name = name
        self._dict = {}
        self._cles = []
    #---------------------------------------------------------------------------
    def getName(self):
        """
        dictionnary name, see the class constructor
        """
        return self._name
    #---------------------------------------------------------------------------        

    def keys(self):
        """
        list of boundary keys
        """
        return self._cles
    #---------------------------------------------------------------------------
    def values(self):
        """
        List of associated key values
        """        
        listValues = []
        for  key in self._cles : listValues.append(self._dict[key])
        return listValues
    #---------------------------------------------------------------------------    
    def items(self):
        """ retourne une liste de couples :(cle, valeur), ou cle est une cle
            du dico et val est la valeur associee.
        """             
        listItems = []
        for  key in self._cles :listItems.append((key, self._dict[key]))
        return listItems
    #---------------------------------------------------------------------------
    def has_key(self, key):
        """ retourne 1 si key est une cle du dico et 0 sinon.
        """            
        return self._dict.has_key(key)
    #---------------------------------------------------------------------------
    def __len__(self):
        """ retourne le nombre de cles du dico.
        """           
        return len(self._cles)
    #---------------------------------------------------------------------------
    def __setitem__(self, key, value):
        """ affectation de la veleur 'value' a la cle 'key' du dico
            via l'operateur [].
        """             
        if not self._dict.has_key(key): self._cles.append(key)
        self._dict[key] = value
    #---------------------------------------------------------------------------

    def __getitem__(self, key):
        """ retourne la valeur associee a la cle 'key' via l'instruction
            via l'operateur [].
        """
        return self._dict[key]
    #---------------------------------------------------------------------------
    def __str__(self):
        """ conversion d'une instance de la classe dico en une chaine de
            caracteres. 
        """        
        lst = []
        for key  in self._cles:
            lst.append("%s:%s" % (key, self._dict[key]))
        ret = "Dico<name=%s>{%s}" % (self._name, string.join(lst, ", "))
        return ret
    #---------------------------------------------------------------------------   
    def __repr__(self):
        """ presentation d'une instance de la classe dico lors de l'impression.
        """              
        return  self.__str__()

    def delete(self,key):
        """ presentation d'une instance de la classe dico lors de l'impression.
        """
        del self._dict[key]
        self._cles.remove(key)
        return  




#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
def whichType(object):
    mytype = str(type(object))[7:-2]

    if mytype in ["list", "tuple"]:
       contenu = "vide"
       if len (object) : contenu = whichType(object[0])
       mytype = "%s<%s> len=%s" % (mytype,  contenu,len (object))
    if mytype == "instance":
       mytype = "instance<%s>" % (object.__class__.__name__) 
    return mytype
    
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
def myDir(object, name, nbCol=6):
   
   listDir = dir(object)
   lenCol = max(map(len, listDir))
 
   lenDir = len(listDir)
   print "dir(%s) = [" % name
   format = '%-' + "%ss " % lenCol
   for i in range (lenDir):
       if (i % nbCol) == 0: print format % listDir[i]
       else:                print format % listDir[i],    
   print "]"
   return

def linear1DMatc(dico, key, variable = None):
   """
   That function enables to write down a boundary condition or
   an initialcondition as a linear varying function
   of the spatial position
   
   """
   if variable == None:
       variable = key
   elif type(variable) == StringType:
       variable = variable
   else:
       raise Warning, " variable should be a string, it has been set to"+key
       string = key
   if variable.lower() == 'head' : variable = "Charge"
   polynomial = dico[key].coefList
   length = len(polynomial)
   #print "length of the polynomial function ",length
   #raw_input()
   cte =  polynomial[0]
   pollux = [cte]
   x =  polynomial[1]
#   t = polynomial[4]
   #
   # for the moment, only one dimension for variation is considered (ax+b or ay+b...)
   #
   if abs(x) > 1.e-15:
       string = "  %s = Variable Coordinate\n   Real MATC \"(%f + %f*(tx(0)))\"\n"
       pollux.append(x)
   elif abs(polynomial[2]) > 1.e-15:
       y = polynomial[2]
       string = "  %s = Variable Coordinate\n   Real MATC \"%f + %f*tx(1)\"\n"
       pollux.append(y)
   elif abs(polynomial[3]) > 1.e-15:
       z = polynomial[3]
       string = "  %s = Variable Coordinate\n   Real MATC \"%f + %f*tx(2)\"\n"
       pollux.append(z)
   print "dbg ",variable
   for i in polynomial:
       print i
   #raw_input("elmertools")
   return string,tuple([variable]+[i for i in pollux])
