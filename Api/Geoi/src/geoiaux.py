def outputFormat(f,listOfTuples,fstparameterlength,scparameterlength):
    i = 0
    while i < len (listOfTuples):
	f.write ('\n')
        temp = str(listOfTuples [i][0]).ljust(fstparameterlength)
	string = str(temp+' '*(scparameterlength-len(temp))+" = ")\
	    	     .ljust(scparameterlength)
	f.write ("%45s"%(string))
        f.write (' ')
        f.write ("%12.8e\n"%(listOfTuples [i][1]))
        i = i+1
