from exceptions import Exception
from os import system,environ,chdir,sys
import getopt
pathtc = environ["WTCT"]
pathc = environ["WTC"]
pathf = environ["WTF"]
patht = "~/Wrapper/Tests/Chemicaltransport/Interactiveplot"
b = (patht,"testpv.py")
#
# to enable the use of mpi4py 
#
system("mpdboot &")
a = [(pathc+"/Acidifiedwaterandcarbonates","Acidified_and_carbonates.py"),\
     (pathc+"/Alkalinewater","test.py"),\
     (pathc+"/Calciteequilibrium","alka.py"),\
     (pathc+"/Caprock","test.py"),\
     (pathc+"/Charmotte","Charmotte.py"),\
     (pathc+"/Dogger","dogger.py"),\
     (pathc+"/Exchange","Solution.py"),\
     (pathc+"/Surfacesolution","flaeche1.py"),\
     (pathc+"/Surfacesolution","flaeche2.py"),\
     (pathc+"/Solidsolution","test.py"),\
     (pathc+"/Pitzer","test.py"),\
     (pathc+"/Pitzer","test1.py"),\
     (pathc+"/Ultimate","test.py"),\
     (pathc+"/Gasphase","gasphase.py"),\
     (pathtc+"/Cec_column","guitest1.py"),\
     (pathtc+"/Cec_column","column.py"),\
     (pathtc+"/Cec_column","boundary.py"),\
     (pathtc+"/Porosityvariation/Constantdiffusion/","test.py"),\
     (pathtc+"/Cec_column/Elmercase","teste.py"),\
     (pathtc+"/Cesiummigration","guitest.py"),\
     (pathtc+"/Cesiummigration","column.py"),\
     (pathtc+"/Cesiummigration","boundary.py"),\
     (pathtc+"/Cesiummigration/Elmercase","teste.py"),\
     (pathtc+"/Ex11","ultimate.py"),\
     (pathtc+"/Ex11","guitest.py"),\
     (pathtc+"/Ex11","column.py"),\
     (pathtc+"/Ex11","boundary.py"),\
     (pathtc+"/Restart","test.py"),\
     (pathtc+"/Restart","testbackup_restart.py"),\
     (pathtc+"/Chemval","guitest.py"),\
     (pathtc+"/Chemval","concrete.py"),\
     (pathtc+"/Chemval","clay.py"),\
     (pathtc+"/Chemval/Elmercase","teste.py"),\
     (pathtc+"/2DSilicadissolution","column.py"),\
     (pathtc+"/2DSilicadissolution","soda.py"),\
     (pathtc+"/2DSilicadissolution","test_cc1.py"),\
     (pathtc+"/2DSilicadissolution/Elmercase","teste.py"),\
     (pathtc+"/Silicadissolution","column.py"),\
     (pathtc+"/Silicadissolution","soda.py"),\
     (pathtc+"/Silicadissolution","test.py"),\
     (pathtc+"/Silicadissolution/Elmercase","teste.py"),\
     (pathtc+"/Temperature","test.py"),\
     (pathtc+"/Porosityvariation/Youngpostprocessing","test.py"),\
     (pathtc+"/Fluxboundary","test.py"),\
#     (pathtc+"/Uraniumdioxyde/Elmercase","teste.py"),\
     (pathf+"/SDirichlet","test.py"),\
     (pathf+"/Arc","test.py"),\
     (pathf+"/2DLinear","test.py"),\
     (pathf+"/2DLinear","testi.py"),\
     (pathf+"/Specificstorage","test.py"),\
     (pathf+"/RichardsDyke","test.py"),\
     ]
def main():
    """
    parse command line options
    
    Three options are available :
    
        - F for flow
        - CT for chemical transport
        - C for chemistry
        
        for example, just type "python validationTest.py ct"
    
    """#
    result = 0
    ind = 0
    print " sys ",sys.argv[1:],type(sys.argv[1:])
    if sys.argv[1:] != []:
        if sys.argv[1:][0].lower() in ["f","ct","c"]:
            if sys.argv[1:][0].lower() == "f":
                option = "WT"+sys.argv[1:][0].upper()
            elif sys.argv[1:][0].lower() == "ct":
                option = "WT"+sys.argv[1:][0].upper()
            if sys.argv[1:][0].lower() == "c":
                option = "WT"+sys.argv[1:][0].upper()
        print option
        stringc = environ[option]
        print " stringc ",stringc
    else:
        stringc = "all"
    print " now ",len(a)
    path =""
    #
    # ind controls the test case list length
    # while indc is the number of successfully run test cases
    #
    indc = 0
    while result == 0 and ind+1 <= len(a):
        if stringc == "all":
            path = chdir(a[ind][0])
            string = "python "+a[ind][1]
            result = system(string)
            print " ~~~~~~~~~~~ "
            print " case run id ",ind
            print " ~~~~~~~~~~~ "
            sys.stdout.flush()
            indc+=1
        elif stringc in a[ind][0]:
            path = chdir(a[ind][0])
            string = "python "+a[ind][1]
            result = system(string)
            print " ~~~~~~~~~~~ "
            print " case run id ",ind
            print " ~~~~~~~~~~~ "
            sys.stdout.flush()
            indc+=1
        else:
            pass
        print " reg",ind,stringc, path
        ind+=1
        pass
#    path = chdir(path"/Cec_column","guitest1.py")
#    subprocess( -> mpdboot)
#    mpirun -np 2 mpipython guitest_mpi.py
#    subprocess( -> mpdballexit)
    if result != 0:
        raise Exception,  " problem with the test case "+a[ind-1][1]+" in the directory: "+ a[ind-1][0]
    else:
        print " test cases run fine",indc
        
if __name__ == "__main__":
    main()

