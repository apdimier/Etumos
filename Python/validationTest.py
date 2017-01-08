from exceptions import Exception
import resource
from os import system,environ,chdir,sys
from time import sleep,clock, gmtime, time
import getopt
import redirect
import resource
pathtc = environ["WTCT"]
pathc = environ["WTC"]
pathf = environ["WTF"]
patht = "~/Wrapper/Tests/Chemicaltransport/Interactiveplot"
b = (patht,"testpv.py")
#
# to enable the use of mpipython 
#
#os.system("mpdboot &")
a = [(pathc+"/Acidifiedwaterandcarbonates","Acidified_and_carbonates.py"),\
     (pathc+"/Alkalinewater","test.py"),\
     (pathc+"/Calciteequilibrium","test.py"),\
     (pathc+"/Caprock","test.py"),\
     (pathc+"/Charmotte","charmotte.py"),\
     (pathc+"/Dogger","dogger.py"),\
     (pathc+"/Exchange","solution.py"),\
     (pathc+"/Gasphase","autoclave.py"),\
     (pathc+"/Gasphase","gasphase_ex7fp.py"),                           # fixed pressure, 1.1
     (pathc+"/Gasphase","gasphase_ex7fv.py"),                           # fixed volume,  22.5
     (pathc+"/Gasphase","gasphase.py"),\
     (pathc+"/Gebo","test.py"),                                         # testing the gebo addendum
     (pathc+"/Pitzer","test.py"),\
     (pathc+"/Pitzer","test1.py"),\
     (pathc+"/Simplifiedcaprockequilibrium","test.py"),\
     (pathc+"/Solidsolution","test.py"),\
     (pathc+"/Surfacesolution","flaeche1.py"),\
     (pathc+"/Surfacesolution","flaeche2.py"),\
     (pathc+"/Ultimate","test.py"),                                     # clay test
     (pathc+"/Waterevaporation","evaporation.py"),                      # evaporation test
#     (pathc+"/Evaporation","evaporationb.py"),                          # evaporation test with kinetics
     (pathtc+"/Analyticaltracer","teste.py"),                           # anal. tracer coarse mesh
     (pathtc+"/Analyticaltracer","testf.py"),                           # anal. tracer finer mesh
     (pathtc+"/Cec_column","guitest1.py"),                              # normalisation of the output, to continue from here
     (pathtc+"/Cec_column","column.py"),\
     (pathtc+"/Cec_column","boundary.py"),\
     (pathtc+"/Autoklav/A1","teste.py"),\
     (pathtc+"/Cec_column/Elmercase","teste.py"),\
     (pathtc+"/Cec_column_species_addenda/Elmercase","teste.py"),\
     (pathtc+"/Cesiummigration","guitest.py"),\
     (pathtc+"/Cesiummigration","column.py"),\
     (pathtc+"/Cesiummigration","boundary.py"),\
     (pathtc+"/Cesiummigration/Elmercase","teste.py"),\
     (pathtc+"/Chemval","guitest.py"),\
     (pathtc+"/Chemval","concrete.py"),\
     (pathtc+"/Chemval","clay.py"),\
     (pathtc+"/Chemval/Elmercase","teste.py"),\
     (pathtc+"/Diffusionprocess","teste.py"),\
     (pathtc+"/Diffusionprocessni","teste.py"),\
     (pathtc+"/Ex11","ultimate.py"),\
     (pathtc+"/Ex11","guitest.py"),\
     (pathtc+"/Ex11","column.py"),\
     (pathtc+"/Ex11","boundary.py"),\
     (pathtc+"/Ex11/Elmercase","teste.py"),\
     (pathtc+"/Threezoneborehole_cp/","teste.py"),\
     (pathtc+"/Heatcapacityvariation/","testeb.py"),\
     #(pathtc+"/Heatconductivityvariation/","teste.py"),\
     (pathtc+"/Porosityvariation/Constantdiffusion/","test.py"),\
     (pathtc+"/Restart","test.py"),\
     (pathtc+"/Restart","testbackup_restart.py"),\
     (pathtc+"/Silicadissolution","column.py"),\
     (pathtc+"/Silicadissolution","soda.py"),\
     (pathtc+"/Silicadissolution","test.py"),\
     (pathtc+"/Silicadissolution/Elmercase","teste.py"),\
     (pathtc+"/Soultzborehole","teste.py"),\
     (pathtc+"/Soultzborehole","testeb.py"),\
     (pathtc+"/Temperature","test.py"),\
     (pathtc+"/Urea","teste.py"),\
     (pathtc+"/2DSilicadissolution","column.py"),\
     (pathtc+"/2DSilicadissolution","soda.py"),\
     (pathtc+"/2DSilicadissolution","test_cc1.py"),\
     (pathtc+"/2DSilicadissolution/Elmercase","testf.py"),\
     (pathtc+"/2Dplot","test.py"),\
#     (pathtc+"/Porosityvariation/Youngpostprocessing","test.py"),\
     (pathtc+"/Fluxboundary","test.py"),\
#     (pathtc+"/Uraniumdioxyde/Elmercase","teste.py"),\
     (pathf+"/SDirichlet","test.py"),\
     (pathf+"/Arc","test.py"),\
     (pathf+"/2DLinear","test.py"),\
     (pathf+"/2DLinear","testi.py"),\
     (pathf+"/Specificstorage","test.py"),\
     ]
def main():
    """
    parse command line options
    
    Three options are available :
    
        - F for flow
        - CT for chemical transport
        - C for chemistry
        
        for example, just type "python validationTest.py ct"
    
    """
    startingDate = gmtime()
    initialCpuTime = clock()
    initialTime = time()
    redic = redirect.output("validation.log")
    redic.toFile()
    result = 0
    ind = 0
    #print " sys ",sys.argv[1:],sys.argv[1:][0],type(sys.argv[1:])
    if sys.argv[1:] != []:
        if sys.argv[1:][0].lower() in ["f","ct","c","wtf"]:
            if sys.argv[1:][0].lower() in ["f","wtf"]:
                option = "WTF"
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
            print " ~~~~~~~~~~~ "
            print " case run id ",ind," name: ",a[ind][1]," in the directory: ",a[ind][0]
            print " ~~~~~~~~~~~ "
            sys.stdout.flush()
            result = system(string)
            indc+=1
        elif stringc in a[ind][0]:
            path = chdir(a[ind][0])
            string = "python "+a[ind][1]
            print " ~~~~~~~~~~~ "
            print " case run id ",ind," name: ",a[ind][1]," in the directory: ",a[ind][0]
            print " ~~~~~~~~~~~ "
            sys.stdout.flush()
            result = system(string)
            indc+=1
        else:
            pass
        sleep(0.5)
        print " reg",ind,stringc, path
        ind+=1
        pass
#    path = chdir(path"/Cec_column","guitest1.py")
#    subprocess( -> mpdboot)
#    mpirun -np 2 mpipython guitest_mpi.py
#    subprocess( -> mpdballexit)
    if result != 0:
        raise Exception,  " problem with the test case %s in the directory: %s"%(a[ind-1][1],a[ind-1][0])
    else:
        print " test cases run fine",indc
    print " the elapsed time in seconds is",time()-initialTime
    print " the starting date is ",startingDate 
    print " the date is          ",gmtime()

def _syscpuTime():
    """ 
    that function is useless due to the call of system or subprocess
    """
    return resource.getrusage(resource.RUSAGE_SELF)[1]
    
if __name__ == "__main__":
    main()

