#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This file is used to enable the introduction of 
# user defined functions. Through that way, the user can 
# introduce its own programming to handle specific parameters
# or physical parameters. The user has to pay attention to the 
# unknown definition due to the python paradigms:
# Every external variable and every method should have us as prefix
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def totoUser():
    print "It works"
def userList(ctmi):
    """
    the user defines here the lists involved in the user defined functions
    """
    ctmi.initialPorosity = []
    pass
def userTuple(ctmi):
    """
    the user defines here the lists involved in the user defined functions
    """
    pass
def effectiveYoungModulus(ctmi):
    """
     Setting the porosity to variable, you 
     construct here the following effective Young modulus
    
     E = E0(1-w/w0)**f 
    """
#    print "It works too: ",ctmi.cpuTime()
    E0 = 1.e+3
    f = 2.1
    ctmi.usE = []
    porosityField = ctmi.chemical.getPorosityField()
    if ctmi.initialPorosity == []:
        for i in porosityField:
            ctmi.initialPorosity.append(i)
    ind = 0
    for i in porosityField:
        aux = E0*(1-i/ctmi.initialPorosity[ind])**f
        ctmi.usE.append(aux)
        ind+=1
#    print " effective Young modulus ",ctmi.usE[0:10]
    pass
