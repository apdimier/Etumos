#!/usr/bin/env python
from __future__ import absolute_import
import os,sys
from platform import uname, python_compiler
import re
import subprocess
"""
    that module is used to test the available configuration.
    It should be updated in terms of necessary sofs.

    Dimier Alain 04/10/2016
"""
machineInformation = uname()

print("system: %s\n"%(machineInformation[0]))
print("node: %s\n"%(machineInformation[1]))
print("release: %s\n"%(machineInformation[2]))
print("version: %s\n"%(machineInformation[3]))
print("machine: %s\n"%(machineInformation[4]))
print("processor architecture: %s\n"%(machineInformation[5]))
pyversion = sys.version.split(" ")[0]
print("Python version: %s\n"%(pyversion))
print("Python executable: %s\n"%(sys.executable))
print("number of digits: %s\n"%(sys.float_info.dig))
print("epsilon: %s\n"%(sys.float_info.epsilon))
print(" gcc compiler: %s"%(python_compiler()))
#gccVersion = os.system("gcc -dumpversion")
#print("gcc version: %s"%(gccVersion))
try:
    print("PYTHONPATH: %s"%(os.environ["PYTHONPATH"]))
except KeyError:
    print("check your PYTHONPATH in ~/.bashrc")
print("")
try:
    import WPhreeqc
    Wph = WPhreeqc.__version__.split("\n")[1]
    print("%20ls %s"%(" wrapping version of phreeqC:",Wph))
except:
    print("check your PYTHONPATH to have $WRAPPER/Wlib in your python path")
try:
    import WElmer
    WEl = WElmer.__version__.split("\n")[1]
    print("%20ls %s"%(" elmer wrapping version:",WEl))
except:
    print("check your PYTHONPATH to have $WRAPPER/Wlib in your python path")
#
# checking the platform software environment 
#
environmentDic = {}

def softEnvironmentTesting(moduleName,
                           informationText = None,
                           subModule=None,
                           minimalVersion = None,
                           versionAttribute = "__version__"):
    global environmentDic
    try:
        exec("import " + moduleName)
        if subModule:
            exec("from "+name+" import "+subModule)
            module=subModule
            pass
        moduleVersion = None
        try:
            moduleVersion=eval(moduleName+"."+versionAttribute)
        except AttributeError:
            pass
        if moduleVersion:
            moduleNameversion = moduleName+" version"
            moduleNameversion+= " "*(20-len(moduleNameversion))
            print("%20s %s %s"%(moduleNameversion,":",moduleVersion))
            if minimalVersion:
                print ("moduleVersion: %s"%(moduleVersion))
                moduleVersion = re.sub(u'\x00', '', moduleVersion)
                if map(int,moduleVersion.split(".")) < map(int,minimalVersion.split(".")):
                    raise Warning(" your installed version is not compatible,\n"\
                                  " you need at least version:%s\n"%(minimalVersion))
                else:
                    print(" "*(len(moduleNameversion)+3)+    "version compatible with requirements")
                    pass
        else:
            try:
                print (eval(moduleName+".__version__"))
            except:
                pass
    except ImportError:
        return False

def execVersion(execName,versionControl = None):
    string = execName + " --version"
    sub = subprocess.Popen(string, shell=True, stderr=subprocess.STDOUT,stdout=subprocess.PIPE)
    sub.wait()
    if sub.returncode == 0:
        version = "".join(sub.stdout.readlines()).replace("\n","")
        execName+= " "*(20-len(execName))
        print("%20s %s %s"%(execName,":",version))
        if versionControl != None:
            versionList = map(int,version.split("."))
            versionControlList = map(int,versionControl.split("."))
            if (versionList < versionControlList):
                #print("control: ",versionList,versionControl)
                raise Exception("the version of "+execName+" seems not compatible with the use of etumos")
            else:
                print(" "*(len(version)+3)+    "version compatible with requirements")
                pass
            pass
        return version
    else:
        raise Exception(" the soft "+execName+" is not installed")
    
print("checking installed version")
print("\n")
#
# module environment
#
softEnvironmentTesting("cython","Not used. Maybe can be used later to speedup the tool; first trials were not concluding")
softEnvironmentTesting("numpy",   "used in the frame of the simulation",     minimalVersion = "1.7.1")
softEnvironmentTesting("Tkinter", "used in the frame of the simulation")
softEnvironmentTesting("wx","ground stone of the interface",                 minimalVersion = "2.8.12")
softEnvironmentTesting("xml"," xml ")
softEnvironmentTesting("scipy","used in geothermaleos",                      minimalVersion = "0.16.1")
softEnvironmentTesting("Gnuplot","used for 2D plotting",                     minimalVersion = "1.8")
softEnvironmentTesting("Scientific","used in the chemical transport module", minimalVersion = "2.8")
softEnvironmentTesting("mpi4py","MPI for Python provides bindings of the Message Passing Interface (MPI) standard for the Python programming language", minimalVersion = "1.3")
softEnvironmentTesting("six"," It provides utility functions for smoothing differences between python versions", minimalVersion = "1.10.0")
softEnvironmentTesting("docx"," python-docx is a Python library for creating and updating Microsoft Word", minimalVersion = "0.8.5")
softEnvironmentTesting("pip"," tool for installing Python packages", minimalVersion = "1.3.1")
softEnvironmentTesting("CoolProp"," python wrapper of the CoolProp C++ library that implements\n"+\
                       "Pure and pseudo-pure fluid equations of state and transport properties for 122 components\n"\
                       , minimalVersion = "5.1")
if pyversion < "3.0.0":
    softEnvironmentTesting("PIL"," The Python Imaging Library (PIL) adds image processing capabilities")
    pass
else:
    softEnvironmentTesting("pillow"," The Python Imaging Library (PIL) adds image processing capabilities")
    pass

#
# soft environment
#
execVersion("gmsh","2.8.2")
execVersion("gnuplot")
execVersion("paraview")


