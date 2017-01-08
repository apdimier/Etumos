from __future__ import absolute_import
from __future__ import print_function
from posttables import Table
from listtools import toList
from generictools import Dico
import string
import numpy
from six.moves import map
from six.moves import range
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
                pass
            pass
        pass
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
            pass
        elif ti > time[-1]:
            pos=len(time)-1
            pass
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
            pass
        lamda = (ti-time[pos-1])/(time[pos]-time[pos-1])
        l_flux = (1-lamda)*flux_l[pos-1]+lamda*flux_l[pos]
        interp_flux[i] = l_flux
    # transforme list to a numerical array
    result_column = Numeric.array(interp_flux)
    return result_column

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
def whichType(object):
    mytype = str(type(object))[7:-2]

    if mytype in ["list", "tuple"]:
       contenu = "vide"
       if len (object) : contenu = whichType(object[0])
       mytype = "%s<%s> len=%s" % (mytype,  contenu,len (object))
       pass
    if mytype == "instance":
       mytype = "instance<%s>" % (object.__class__.__name__)
       pass
    return mytype
    
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
def myDir(object, name, nbCol=6):
   
   listDir = dir(object)
   lenCol = max(list(map(len, listDir)))
 
   lenDir = len(listDir)
   print("dir(%s) = [" % name)
   format = '%-' + "%ss " % lenCol
   for i in range (lenDir):
       if (i % nbCol) == 0: print(format % listDir[i])
       else:                print(format % listDir[i], end=' ')    
   print("]")
   return

def linear1DMatc(dico, key, variable = None):
   """
   That function enables to write down a boundary condition or
   an initialcondition as a linear varying function
   of the spatial position
   
   """
   if variable == None:
       variable = key
       pass
   elif type(variable) == StringType:
       variable = variable
       pass
   else:
       raise Warning(" variable should be a string, it has been set to"+key)
       string = key
       pass
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
       pass
   elif abs(polynomial[2]) > 1.e-15:
       y = polynomial[2]
       string = "  %s = Variable Coordinate\n   Real MATC \"%f + %f*tx(1)\"\n"
       pollux.append(y)
       pass
   elif abs(polynomial[3]) > 1.e-15:
       z = polynomial[3]
       string = "  %s = Variable Coordinate\n   Real MATC \"%f + %f*tx(2)\"\n"
       pollux.append(z)
       pass
   print("dbg ",variable)
   for i in polynomial:
       print(i)
       pass
   #raw_input("elmertools")
   return string,tuple([variable]+[i for i in pollux])
