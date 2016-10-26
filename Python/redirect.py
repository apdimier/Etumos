from __future__ import absolute_import
import os, sys

class __output:
    def __init__(self, filename):
        self.my_os = os
        self.filename = None
        self.oldStdout = None
        self.sys_stdout = sys.__stdout__
        self.new_stdout = None
        if filename != None:
            self.setFileName(filename)
    
    def setFileName(self, filename):
        if filename == None:
            return
        if self.filename != None:
            os.close(self.new_stdout)
        self.filename = filename
        self.oldStdout = os.dup(1)
        if os.path.isfile(filename):
            os.remove(filename)
        self.new_stdout = os.open(filename, os.O_WRONLY|os.O_CREAT|os.O_APPEND, 0o666)
        
    def getFileName(self):
        if self.filename != "":
            return self.filename
        else:
            return None
        
    def toFile(self):
        if self.filename != None:
            os.dup2(self.new_stdout, 1)
            sys.stdout = open(self.filename, 'a', 0o666)

    def revert(self):
        if self.filename != None:
            os.dup2(self.oldStdout, 1)
            sys.stdout = self.sys_stdout

        
    def __del__(self):
        if self.new_stdout != None:
            self.my_os.close(self.new_stdout)
        
__outputObject = None

def output(filename=None):
    global __outputObject
    if __outputObject is None:
        __outputObject = __output(filename)
    elif filename != None:
        __outputObject.setFileName(filename)
    return __outputObject

