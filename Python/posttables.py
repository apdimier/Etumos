"""
Tables are the way to extract data for post-processing
"""

from __future__ import absolute_import
from __future__ import print_function
from generictools import memberShip, listTypeCheck

import numpy

from typechecktools import verifyType

from types import FloatType,\
          IntType,\
          ListType,\
          StringType


from listtools import toList

from wrappertools import areClose

import string
from six.moves import range

def _getIndex(x, list):
    """Gets the index."""
    if type(x) == IntType:
        return x
    elif type(x) == StringType:
        return list.index(x)
    return
    
class GroundTable:
    """
    """
    def getValue(self):
        return self
    pass

class Table:
    """
    A list of 'columns' of values.
    """
    def __init__(self,name, column_names=None, column_units=None):
        """
        A table is made of a:
                - name which is a string
        and of eventually:
                - column names ( a list ) and 
                - column units ( a list )
        """
        if type(name) == StringType:
            self.name = name
            pass
        else:
            raise TypeError(" the name of one of the tables isn't mentionned")
        if column_names:
            if type(column_names) == StringType:
                self.column_names = column_names
                self.values = numpy.reshape(numpy.array([]),(len(column_names,0)))
                pass
            else:
                raise TypeError(" you forgot to mention the name of one of the tables")
            pass
        else:
            self.column_names = []
            self.values = numpy.reshape(numpy.array([]),(0,0))
            pass
                
        if column_units:
            if type(column_units) == StringType:
                self.column_units = column_units
                pass
            else:
                raise TypeError(" column units must be a string")
        else:
            self.column_units = ""
        return None                
            
    def getNbRows(self):
        """Gets the number of rows of the table."""
        return self.values.shape[1]
    
    def getNbColumns(self):
        """Gets the number of columns of the table."""
        return self.values.shape[0]
    
    def setName(self, name):
        """Sets the name of the table. """
        self.name = name
        pass
    
    def getName(self):
        """Gets the name of the table. """
        return self.name
    
    def setColumnNames(self,column_names):
        """Sets the names of each column of the table. """
        self.column_names=column_names

    def getColumnNames(self):
        """Gets the names of each column of the table. """
        return self.column_names

    def setColumnUnits(self,column_units):
        """Sets the units of each colum of the table."""
        self.column_units = column_units

    def getColumnUnits(self):
        """Gets the units of each column of the table. """
        return self.column_units
    
    def getColumnNb(self, name):
        return self.column_names.index(name)

    def addRow(self, row):
        """Adds a row to the table. """
        nc = len(row)
        if nc != self.values.shape[0]:
            msg="Row of wrong length : %s instead of %s"%(nc,self.values.shape[0])
            raise msg
        new_row = numpy.reshape(numpy.array(row),(-1,1))
        self.values = numpy.concatenate((self.values, new_row),1)
        return
    
    def addColumnValues(self, column):
        """Adds a column with values to the table."""
        nr1 = self.values.shape[1]
        nr = len(column)
        if nr1 == 0:
            # case 1: empty table
            if nr == 0:
                # case 1a: we're just adding a name
                self.values = numpy.reshape(self.values, (1, 0))
                pass
            else:
                # case 1b: we're adding a column of values
                self.values = numpy.reshape(numpy.array(column), (1, nr))
                pass
            pass
        else:
            # case 2: non-empty table
            if nr1 > 0 and nr != nr1:
                raise Exception("New column must have the same length as existing ones %s %s"%(nr1,nr))
            new_column = numpy.reshape(numpy.array(column), (1, nr))
            self.values = numpy.concatenate((self.values, new_column))
            pass
        return
    
    def addColumn(self, name, column):
        """Adds a column to the table. """
        self.column_names.append(name)
        self.addColumnValues(column)

    def getRow(self, i):
        """Returns a list of values contained in a specific row."""
        return self.values[:,i]
    
    def getColumn(self, x):
        """Returns a list of values contained in a specific column."""
        i = _getIndex(x, self.column_names)
        return self.values[i]
    
    def getItem(self, column, position):
        """Gets an item having a definite position in the table."""
        return self.values[column, position]
    
    def setRow(self, row_number, row):
        """Sets a row in the table"""
        self.values[:,row_number] = row
        return
    
    def setColumn(self, column_number, column):
        """Sets a column in the table."""
        self.values[column_number] = column
        return
    
    def setItem(self, column_number, row_number, value):
        """Sets a value in a definite column and row of the table. """
        self.values[column_number, row_number] = value
        return

    def isEqual(self,other,epsilon=None):
        """Compares two tables self and other. Returns 1 if they are completely identical, otherwise - 0."""
        memberShip(other,Table)
        Ok=0
        nbc1=len(self.getColumnNames())
        nbc2=len(other.getColumnNames())
        if nbc1!=nbc2:
            return 0
        nbu1 = len(self.getColumnUnits())
        nbu2 = len(other.getColumnUnits())
        if nbu1!=nbu2:
            return 0
        for i in range(nbc1):
            if self.getColumnNames()[i].lower().strip()!=\
               other.getColumnNames()[i].lower().strip():
                return 0
            pass
        for i in range(nbu1):
            if self.getColumnUnits()[i].lower().strip()!=\
               other.getColumnUnits()[i].lower().strip():
                return 0
            pass
        
        nbc1=self.getNbColumns()
        nbc2=other.getNbColumns()
        if nbc1!=nbc2:
            return 0
        nbl1=self.getNbColumns()
        nbl2=other.getNbColumns()
        if nbl1!=nbl2:
            return 0
        for i in range(nbl1):
            for j in range(nbc1):
                v1=self.getItem(j,i)
                v2=other.getItem(j,i)
                if not epsilon:
                    if v1!=v2:
                        return 0
                    pass
                elif not areClose(float(v1),float(v2),epsilon,'rel'):
                    return 0
                pass
            pass
        return 1
    
    def copy(self):
        """Copy method.
    Returns a new table, in which it inserts the rows from the given table."""
        new=Table(self.getName(),self.getColumnNames(),self.getColumnUnits())
        nlig=self.getNbRows()
        for i in range(nlig):
            lig=self.getRow(i)
            new.addRow(lig)
            pass
        return new

    def extractSubTable(self,**dico):
        """ Creates a subtable in different ways ordered by dico keys.
        1/ if somebody wants a table with several columns, the possibilities are:
             column = a number
             columns = a number (for only one column)
                     or
                     a list of numbers (where can be only
                                        one number)
             fromcolumn = a number
             tocolumn = a number
             columnname = 'a good column name'
             columnnames = a list of column names
        2/ if somebody wants a table with several rows, the possibilities are:
             row   = a number
             rows  = a number (for only one column)
                     or
                     a list of numbers (where can be only
                                        one number)
             fromrow = a number
             torow = a number
             withvaluesincolumn = a tuple (list of values, number of column
                                           or its name, a precision if wanted)
        """
        #
        if not len(dico):
            return self.copy()
        elif len(dico)>1:
            msg='only one argument allowed.'
            raise msg
        #
        cle=list(dico.keys())[0]
        val=dico[cle]
        cle=cle.lower()
        if cle=='withvaluesincolumn':
            model,numeroColonne=val[0],val[1]
            listTypeCheck(model,[IntType,FloatType])
            model=[float(x) for x in model]
            verifyType(numeroColonne,[StringType,\
                       IntType,FloatType])
            tttitres=self.getColumnNames()
            ttunits = self.getColumnUnits()
            if type(numeroColonne) is StringType:
                for tit in tttitres:
                    if tit==numeroColonne:
                        numCol=tttitres.index(tit)
                        pass
                    pass
                pass
            else:
                if numeroColonne>=len(tttitres):
                    msg='The table does not have\n'
                    msg+='that number of columns : %s'%numeroColonne
                    raise msg
                numCol=numeroColonne
                pass
                
            if len(val)==3:
                eps=val[2]
                pass
            else:
                eps=1.e-15
                pass
            new=Table(self.getName(),tttitres,ttunits)
            nlig=self.getNbRows()
            ip=0
            comp=[float(x) for x in self.getColumn(numCol)]
            for ip in range(len(model)):
                for i in range(len(comp)):
                    value=comp[i]
                    if ip==1 and i==len(comp)-1:
                        pass
                    if areClose(value,model[ip],eps,'rel'):
                        new.addRow(self.getRow(i))
                        pass
                    if ip==len(model):
                        break
                    pass
                pass
            pass           
        else:
            valeurs=toList(val)
            tttitres=self.getColumnNames()
            ttunits = self.getColumnUnits()
            for st in ['row','column']:
                if st=='row':nn=self.getNbRows()
                if st=='column':nn=self.getNbColumns()
                if cle.find(st)>=0:
                    cleOk=st
                    pass
                if cle==st:
                    if len(valeurs) != 1:
                        raise Exception(" list length problem within the extractSubTable function")
                if cle=='from'+st:
                    valeurs=valeurs[valeurs[0]:nn-1]
                    pass
                if cle=='to'+st:
                    valeurs=valeurs[0:valeurs[0]]
                    pass
                if cle.find('name')>=0:
                    newv=[]
                    for v in valeurs:
                        for tit in tttitres:
                            if tit==v:
                                newv.append(tttitres.index(tit))
                                break
                            pass
                        pass
                    valeurs=newv
                    pass
                pass
            if cleOk=='row':
                newtitres=tttitres
                newunits = ttunits
                pass
            if cleOk=='column':
                newtitres=[]
                newunits = []
                for i in valeurs:
                    newtitres.append(tttitres[i])
                    if len(ttunits):
                        newunits.append(ttunits[i])
                    pass
            new=Table(self.getName(),newtitres,newunits)
            for i in valeurs:
                if cleOk=='row':
                    liste=self.getRow(i)
                    new.addRow(liste)
                if cleOk=='column':
                    liste=self.getColumn(i)
                    new.addColumnValues(liste)
                    pass
                pass
            pass
        return new
                
    def write(self):
        names = self.column_names
        print("Table:", self.name)
        values = self.values
        for j in range(len(names)):
            print(names[j], ':', values[j,:])
            pass
        return
         

    def readFromFile(self,ffile,nbcolumns=None,columnsNames='yes',name='no',columnsUnits='no'):
        """Reads a table from the given file."""
        from exceptions import IOError
        try:
            if self.values.shape != (0,0):
                raise Warning("The table already contains values")
            file = open(ffile, 'r')
        except :
            msg="can't open file <%s>...\n"%ffile
            raise IOError(msg)


        fileNameColumns=[]
        fileNameUnits=[]
        fileName=None
        
        filemaxnbcol=0
        fileminnbcol=100
        isonvalues=0
        allvaluesbycolonne=[]
        nbvalueline=0
        cpt=1
        for line in file.readlines():
            separe = line.split()
            if (len(separe) == 0 ):
                # blank line
                continue
                
            
            if ( separe[0] == '#' ):
                # comment line
                cpt=cpt+1
                continue
            elif ( separe[0] == '#TITLE:' ):
                # name line
                separe = separe[1:]
                s=''
                for isep in range(len(separe)):
                    s=s+separe[isep]+' '
                    fileName=s
                    pass
                pass
            elif ( separe[0] == '#COLUMN_TITLES:' ):
                # column name line
                separe = separe[1:]
                s=''
                for isep in range(len(separe)):
                    s=s+separe[isep]
                    s=string.strip(s)
                    if ( len(s) == 0 ):
                        fileNameColumns=[]
                        continue
                    fileNameColumns = s.split('|')
            elif ( separe[0] == '#COLUMN_UNITS:' ):
                # unit name line
                fileNameUnits = separe[1:]
            elif ( cpt == 1 ):
                # column name line
                pass
            else:
                # values line
                nbvalueline=nbvalueline+1
                linenbcol=len(separe)
                filemaxnbcol=max(linenbcol,filemaxnbcol)
                fileminnbcol=min(linenbcol,fileminnbcol)
                linevalues=[]
        
                for isep in range(linenbcol):
                    linevalues.append(float(separe[isep]))
                    
                # adjust nb columns if not the same on each line
                # or if the first value's line
                if ( filemaxnbcol < len(allvaluesbycolonne) ):
                    for icol in range(filemaxnbcol,len(allvaluesbycolonne)):
                        allvaluesbycolonne.append([])
                        for il in range(nbvalueline-1):
                            allvaluesbycolonne[il].append(0)
                elif ( filemaxnbcol > len(allvaluesbycolonne) ):
                    for icol in range(len(allvaluesbycolonne),filemaxnbcol):
                        allvaluesbycolonne.append([])
                        for il in range(nbvalueline-1):
                            allvaluesbycolonne[icol].append(0)
                
                # add values
                for icol in range(linenbcol):
                    allvaluesbycolonne[icol].append(linevalues[icol])
                for icol in range(linenbcol,filemaxnbcol):
                    allvaluesbycolonne[icol].append(0)
                    pass
                pass
            pass   
        cpt=cpt+1
        file.close()
        
        # check consistency beetwen arguments and file contents
#
# controlling the table parameters
#        
        if ( fileminnbcol != filemaxnbcol ):
            raise IOError("colums must have the same number of rows")
    
        if nbcolumns:
            if ( filemaxnbcol != nbcolumns ):
                raise IOError(" problem with the number of columns")
        
        # Warnings
        if ( ( columnsNames.lower() == 'no' ) and ( len(fileNameColumns) > 0 ) ):
            raise Warning(" you should specify column names")
        
        if ( ( columnsNames.lower() == 'yes' ) and ( len(fileNameColumns) == 0 ) ):
            raise Warning("you specified columnName(s) but the file doesn\'t entail column names")
        
        if ( len(fileNameColumns) < filemaxnbcol ):
            nbcol=len(fileNameColumns)
            for icol in range (nbcol,filemaxnbcol):
                fileNameColumns.append('col'+str(icol+1))
        
            effectivecolumnNames=fileNameColumns
            
        
        if ( ( name.lower() == 'no' ) and fileName ):
            msg='WARNING: you specified no name but there is name in file'
            print(msg)
        
        if ( ( name.lower() == 'yes' ) and ( fileName == None ) ):
            msg='WARNING: you specified name but there is no name in file'
            print(msg)
        
        if ( ( columnsUnits.lower() == 'no' ) and ( len(fileNameUnits) > 0 ) ):
            msg='WARNING: you specified no units name but there are units name in file'
            print(msg)
    
        if ( ( columnsUnits.lower() == 'yes' ) and ( len(fileNameUnits) == 0 ) ):
            msg='WARNING: you specified units name but there are no units name in file'
            print(msg)
    
        if ( ( len(fileNameUnits) > 0 ) and ( len(fileNameUnits) < filemaxnbcol ) ):
            nbcol=len(fileNameUnits)
            for icol in range (nbcol,filemaxnbcol):
                fileNameUnits.append('col'+str(icol+1))
    


        if fileName:
            self.setName(fileName)
            pass
        if len(fileNameUnits):
            self.setColumnUnits(fileNameUnits)

        for i in range(filemaxnbcol):
            if columnsNames.lower()=='yes':
                self.addColumn(effectivecolumnNames[i],allvaluesbycolonne[i])
            else:
                self.addColumnValues(allvaluesbycolonne[i])
        return

    def writeToFile(self, ffile,name='yes',columnNames='yes',columnUnits='yes'):
        """Writes a table into a file."""
        file = open (ffile,'a')
        titre=self.getName()
        if name.lower()=='yes':
            file.write('#TITLE: table %s\n'%titre)
        ctitres = self.getColumnNames()

        Nbc = self.getNbColumns()
        Nbl = self.getNbRows()
        
        if columnNames.lower()=='yes':
            txt = '#COLUMN_TITLES: '
            lenctitres = len(ctitres)
            for i in range(lenctitres):
                txt+='%s' %ctitres[i]
                if i!=(lenctitres-1):
                    txt+=' | '
                    pass
                pass
            file.write(txt+'\n')
            pass
        
        if columnUnits.lower()=='yes':
            cunits = self.getColumnUnits()
            txt = '#COLUMN_UNITS: '
            lencunits = len(cunits)
            for i in range(lencunits):
                txt+='%s ' %cunits[i]
            
            file.write(txt+'\n')
            pass
            
            

        for i in range(Nbl):
            txt = ''
            for j in range (Nbc):
                val = self.getItem(j,i)
                txt+='%17.7e' %val
                pass
            file.write(txt+'\n')
            pass
        file.write('\n')
        file.close()
        pass

    def amult(self,coef):
        """ Multiplies all table columns, except the first,
        by a coefficient. Returns a new Table"""
        new_name = self.getName() + '_' + str(coef)
        newTable = Table(new_name)
        newTable.setColumnUnits(self.getColumnUnits())
        col_names= self.getColumnNames()
        # Copy the first column as it
        newTable.addColumn(col_names[0],self.getColumn(0))
        for i in range(1,len(col_names)):
            c = self.getColumn(i)*coef
            newTable.addColumn(col_names[i],c)
        return newTable


    def Norm(self,col_number,type='L1'):
        """ evaluate the L1 Norm of the table on the first column,
        if it is a time,
        example : for the first column after the column time [0]
        ---
        \   (abs(c2)+abs(c1))/2)*(t2-t1)    for L1 Norm
        /
        --- t in times
        Possible types of the Norm are: L1 and L2 (table.getColumn[1].[t]**2)
        """
        if col_number <=0 or col_number > (self.getNbColumns()-1):
            raise Warning("column number out of table, Please verify")
        else:
            c = self.getColumn(col_number)
            times = self.getColumn(0)
            res = 0
            for i in range(len(times)-1):
                if c[i]*c[i+1] > 0:
                    if type.lower()== 'l1':
                        res+= ((abs(c[i])+abs(c[i+1]))/2.) * (times[i+1]-times[i])
                    elif type.lower()== 'l2':
                        res+= (c[i]*c[i]+c[i+1]*c[i+1])*1./2 * (times[i+1]-times[i])
            return res

    
    def cumulate(self):
        """ Calculate the cumulate table of the current table on the first
            colomn and return a new table:
            table        = t[i]   f[i]
            table_cumule = t[i]   N[i]
                avec :  N[i] = (f[i]+f[i-1])/2 *(t[i]-t[i-1])+N[i-1]
        """
        name = self.getName() + '_Cumulated'
        c_names = self.getColumnNames()
        # create the new table an add the first column to it
        t_cumulate = Table(name)
        time = self.getColumn(0)
        t_cumulate.addColumn(c_names[0],time)
        # for each other column, cumulate values                             
        for i in range(1,self.getNbColumns()):
            c = self.getColumn(i)
            N = [0]
            for j in range(1,len(c)):
                n =  (c[j]+c[j-1])/2*(time[j]-time[j-1]) + N[-1]
                N.append(n)
            t_cumulate.addColumn(c_names[i],N)
            
        return t_cumulate
        
    def deriveFromIntegral(self,inverse='rectangle',t0=0.,newName='',newColumnNames=[]):
        """ Calculates the derivate table of the current table on the first
            colomn and return a new table:
            table        = t[i]   f[i]
            table_derive = t[i]   N[i]
                with :
                   if inverse=='rectangle' :
                       N[i] = (f[i]-f[i-1]) / (t[i]-t[i-1])
        """
        from exceptions import Exception
        if not inverse.lower()=='rectangle':
            msg="cannot yet derive without supposing\n"
            msg+='that the integration was first made\n'
            msg+='using rectangle method.'
            raise Exception(msg)
        verifyType(newName,StringType)
        if not len(newName):
            newName=self.getName()
            pass
        verifyType(newColumnNames,ListType)
        len_ini=len(newColumnNames)
        for i in range(len(self.getColumnNames())):
            if i<len_ini:
                titre=newColumnNames[i]
                verifyType(titre,StringType)
                if not len(titre):
                    newColumnNames[i]=self.getColumnNames()[i]
                    pass
                pass
            else:
                newColumnNames.append(self.getColumnNames()[i])
                pass
            pass
        #  real beginning :
        new=Table(newName)
        nlig=self.getNbRows()
        ncol=self.getNbColumns()

        time = self.getColumn(0)
        time=[t0]+time
        tt=t0
        for ii in range(len(time[1:])):
            tsup=time[1+ii]
            if tt>=tsup:
                msg='Time does not increase in table %s'%self.getName()
                msg+=' ;\n cannot derive !'
                msg+='\n\n info : t[%s] = %e\n        t[%s] = %e\n'\
                      %(ii,time[ii],1+ii,time[1+ii])
                raise Exception(msg)
            tt=tsup
            pass
        new.addColumn(newColumnNames[0],time)
        # for each other column, cumulate values                             
        for i in range(1,self.getNbColumns()):
##             print 'LONGUEUR self.getColumn(i):',len(self.getColumn(i))
            c = self.getColumn(i)
##             print 'LONGUEUR c : len(c)',len(c)
##             print 'type(c)',type(c)
##             c = [0.]+c    NE MARCHE PAS CAR type(c) = array
##             N = []
##             print 'LONGUEUR c : len(c)',len(c)
            N=[c[0]/(time[1]-time[0])]
            for j in range(1,len(c)):
                n =  (c[j]-c[j-1])/(time[j]-time[j-1])
                N.append(n)
                pass
##             print 'LONGUEUR N ,self.getColumn(i):',len(N),len(self.getColumn(i))
            new.addColumn(newColumnNames[i],N)

        return new
        
            

##################################################
#
def makeTableFromFile(ffile,name=None,nameInFile='No',\
                      columnsNames=None,columnsNamesInFile='Yes',
                      columnsUnits=None,columnsUnitsInFile='No'):
    """Makes a table from the given file. Reads table's names (if they are present) from the file.
    Line of Name in file should begin with #TITLE:
    Line of ColumnsName in file should begin with #COLUMN_TITLES: and colum names should be separate by |"""
    from exceptions import IOError
    t = None
    try:
        file = open(ffile, 'r')
    except :
        msg="can't open file <%s>...\n"%ffile
        raise IOError(msg)
    if name and nameInFile.lower()=='yes':
        raise Warning("You give a table name and ask to get name from file") 
    if columnsNames and columnsNameInFile.lower()=='yes':
        raise Warning("You ask for colum names in the file while already defining them")
    if columnsUnits and columnsUnitsInFile.lower()=='yes':
        raise Warning("You ask for units in the file while already defining them")
    # table creation
    if name:
        verifyType(name,StringType)
        t=Table(name)
        pass
    else:
        t=Table('table')
        pass
    # affect columns names if necessary
    if columnsNames:
        t.setColumnNames(columnsNames)
        pass
    # affect columns units if necessary
    if columnsUnits:
        t.setColumnUnits(columnsUnits)
        pass
    t.readFromFile( ffile,
                    columnsNames=columnsNamesInFile,name=nameInFile,
                    colonnesnames=columnsNames,columnsUnits=columnsUnitsInFile)

    return t


def makeTableFromLinearFunction(function,coords,time_list,name=None,columnUnits=None):
    """Constructs a table consisting of two columns.
    The first column contains a time list and the second column contains function values for space coordinates coords and times defined in the time list."""
    verifyType(time_list,ListType)
    from functions import LinearFunction
    memberShip(function,LinearFunction)
    nb_coeff = function.getNbCoefficients()
    coeffs = function.getCoefficients()
    if name:
        verifyType(name,StringType)
        tab=Table(name)
        pass
    else:
        tab = Table('Table')
        pass
    if columnUnits:
        listTypeCheck(columnUnits, StringType)
        if len(columnUnits) !=2:
            raise Exception("makeTableFromLinearFunction creates a two columns table : time and value. You have to give two units")
        tab.setColumnUnits(columnUnits)
        pass
    value_list = []
    for t in time_list:
        coo = coords + [t]
        value = function.eval(coo)
        value_list.append(value)
        pass
    tab.addColumn('time',time_list)
    tab.addColumn('value',value_list)
    return tab







        
            
