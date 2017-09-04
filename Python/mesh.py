"""
Module enabling the lecture of a gmsh file from python to be
handled in the coupling

This module takes a Gmsh output file (`.msh`) . This module should be able to 
read all kind of files issued from gmsh.
The mesh file must have the following structure:

    $MeshFormat
    $PhysicalNames
    $Nodes
    $Elements
    
Freely inspired from some Fipy python files in the sense of the GPL license
 #
 #  FILE: "/meshes/numMesh/gmshImport.py"
 #     www: http://www.ctcms.nist.gov/fipy/
"""
import numpy

import numpy.ma as MA

from generictools import Generic

import subprocess

from os import path as osdotpath

import sys

from time import sleep,clock, gmtime, time

from types import ListType, NoneType

def MeshReader(fileName):
    readFile = open (fileName)
    a = readFile.readline()
    while "PhysicalNames" not in  a:
        a = readFile.readline()
        #print a
        pass
    # 
    # gmsh 2.3 doesn't entail the entities dimension,
    # but 2.4 and upper it's ok
    # So, the default dimension is 2 and if version > 2.4 has been used for mesh generation,
    # the dimension is retrieved from physical entities
    #
    dimension = 2
    while "EndPhysicalNames" not in a[0]:
        a = readFile.readline().split()
        print a
        #print a
        #raw_input("dbd dimension: "+str(a))
        if len(a) == 3:
            dimension = max(int(a[0]),dimension)
            pass
        pass
    #raw_input("mesh dimension :"+str(dimension))
    readFile.close()
    while readFile.closed == False:
        pass
    print " pmesh dimension",dimension
    #raw_input()
    if dimension == 2: mesh = Mesh2D(fileName)
    elif dimension == 3: mesh = Mesh3D(fileName)
    else: raise Exception, "the dimension should be 2 or 3"
    return mesh

class MeshImportError(Exception):
    pass
    
class Body(Generic):
    """
    A class to handle bodies in the sense of the elmer or openfoam solvers
    """

    def __init__(self, body, bodyName = None, internalNodesAnz = None, nodes = None, dim = None, meshDimension = None):
        Generic.__init__(self)
        self.body = body
        self.bodyName = bodyName
        self.name = bodyName
        self.physicalName = bodyName
        self.internalNodesAnz = internalNodesAnz
        self.dim = dim
        if meshDimension != None:
            self.meshDimension = meshDimension
            pass
        else:
            self.meshDimension = dim
            pass
        self.nodes = nodes
        #print len(self.internalNodesAnz),bodyName
        #raw_input("class body ")

    def getBodyName(self):
        return self.name
    
    def getElements(self):
#        print "\nmesh dbg body getEntity function:",self.physicalName,"\n body number:",self.body[0],"\n entity list: ",len(self.body[1])
#        print " dir body ",type(self.body[1][0])
        return self.body[1]

    def getName(self):
        return self.name
    
    def getNodesNumber(self):
        return len(self.internalNodesAnz)
    
    def getBodyNodesList(self):
        return self.internalNodesAnz
        
    def getBodyDimension(self):
        return self.dim
    
    def getElementsNumber(self):
        return len(self.body[1])
    
    def getEntity(self):
        #print "\nmesh dbg body getEntity function:",\
        #self.physicalName,"\n body number:",self.body[0],"\n entity list: ",self.body[1]
        #raw_input()
        return self.body[0]
    
    def getMesh(self):
        return self.body[1]
        
    def getMeshType(self):
        return self.body[1]

    def getPhysicalName(self):
        return self.name

    def getSpaceDimension(self):
        #print("debug getSpaceDimension: ", self.dim, type(self.dim))
        #raw_input("debug")
        return self.dim

    def getMeshDimension(self):
        return self.dim

class DataGetter(Generic):
    """
    A class to retrieve the elements of the mesh.
    """
    def __init__(self) :
        """
        
        """
        Generic.__init__(self)
        
    def getData(self, filename, dimensions, coordDimensions = None):

        if coordDimensions is None: coordDimensions = dimensions

#        if (dimensions != 2 and dimensions != 3):
#            raise MeshImportError, "Number of dimensions must be 2 or 3"
            
        self.dimensions = dimensions
        self.dim = dimensions
        self.meshFileName = filename
        self.inFile = open (filename)
        line = self.inFile.readline()                                                       # skip the $MeshFormat
        self.version, self.fileType, self.datasize = self.inFile.readline().split()
        line = self.inFile.readline()                                                       # skip the $EndMeshFormat
        line = self.inFile.readline()                                                       # skip the $PhysicalNames
        nBodies = int(self.inFile.readline())
        self.boundaryNodes = []
        self.physicalBodyNames = {}
        for i in range(nBodies):
            tempList  = self.inFile.readline().split()
            if len(tempList) == 2:
                physicalDimension = dimensions                                              # the dimension is st by default
                ind =  tempList[0]
                name = tempList[1]
                pass
            else:                                                                           # physical-dimension physical-number physical-name
                physicalDimension = int(tempList[0])
                ind =  tempList[1]
                name = tempList[2]
                pass
            print ind,name
            #raw_input("datagetter bodies")
            self.physicalBodyNames[str(name)[1:-1]] = [int(ind), [], physicalDimension]
            pass
#        if not self.physicalBodyNames.has_key('domain'):
#            raise Exception, " the mesh must have at least a body name called \"domain\" and representing the whole mesh"
        print "dbg self.physicalBodyNames",self.physicalBodyNames
        line = self.inFile.readline()                                                       # skip the EndPhysicalNames
        self.vertexCoords = vertexCoords = self._calcVertexCoords(coordDimensions)
        print " number of vertices ",len(self.vertexCoords)
        print " vertex coordinates 1 ",self.vertexCoords[0]
        #raw_input("dbg vertex coordinates")
        self.internalNodesAnz = self.numVertices
        print " self.internalNodesAnz ",self.internalNodesAnz
        #raw_input("self.internalNodesAnz")
        print " call of _calcCellVertexIDs"
        self._calcCellVertexIDs()
        print " call of _calcCellVertexIDs over"
        #
        # we update the physicalBodyNames dictionnary with a list of elements bounded to the physical entity
        #
        self._associateElementIDs()
        print " call of _associateElementIDs over"
        #
        #print " vertex coordinates ",self.vertexCoords[0]
        #raw_input("dbg vertex coordinates")

#        self._calcBaseFaceVertexIDs()

#        print "dbg out of _calcBaseFaceVertexIDs"
#        print "dbg calling _calcFaceVertexIDs"

#        faceVertexIDs = self._calcFaceVertexIDs()

#        print "dbg out of _calcFaceVertexIDs"
#        print "dbg calling _calcCellFaceIDs"

#        cellFaceIDs = self._calcCellFaceIDs()

#        print "dbg out of _calcCellFaceIDs"
#        indPBN = []
#        for i in self.physicalBodyNames.keys():
#            if "domain" in i:
#                indPBN.append(self.physicalBodyNames[i][0])

        #
        # element types belonging to Physical Body Names of dimension N
        #
        if dimensions == 1:
                                                                                            #
                                                                                            # 1 : 2-node line
                                                                                            #
            indPBN = [1]
            pass
        elif dimensions == 2:
                                                                                            #
                                                                                            # 2 : 3 node triangle
                                                                                            # 3 : 4 node quadrangle
                                                                                            #
            indPBN = [2,3]
            pass
        else:
                                                                                            #
                                                                                            # 4 : 4 node tetrahedron
                                                                                            # 5 : 8 node hexahedron
                                                                                            # 6 : 6 node prism
                                                                                            # 7 : 4 node node pyramid
                                                                                            #
            indPBN = [4,5,6,7]
            pass
#        print " indPBN   ",indPBN,self.elementArray[0],self.elementArray[1]
#
# we identify nodes belonging to boundary 
#
        frontN = []
        #print  "self.elementArray \n",self.elementArray
        
        if self.dimensions != 1:
            for element in self.elementArray:
            #
            # We consider boundaries and identify nodes belonging to
            #
                if element[1] not in indPBN:        # we suppose boundaries being 1 dimension smaller as the problem dimension
                    indRef = 3 + element[2]
#                for vertex in  range(indRef,len(element)):
                    for vertex in range(indRef,indRef+_nodeElements(element[1])):
                        if element[vertex] not in frontN and element[vertex]>0:
                            frontN.append(element[vertex])
                            pass
                        pass
                    pass
                pass
            pass
        else:
            for element in self.elementArray:
                if element[1] not in indPBN:
                    frontN.append(element[0])
                    pass
                pass
            pass
        #print " nodes on boundaries: ",frontN                      
        indPDO = []
        #print " vertex coordinates2 ",self.vertexCoords[0]
#
# we identify nodes belonging to the internal data
#
        for element in self.elementArray:
            if element[1] in indPBN:
            #
            # element[1] is the elm-type
            #
                indRef = 3 + element[2]
                for ind in  range(indRef,indRef+_nodeElements(element[1])):
                    if element[ind] not in frontN and element[ind]>0:
                        if element[ind] not in indPDO:
                            indPDO.append(element[ind])
                            pass
                        pass
                    pass
                pass
            pass
        #print frontN
        print " vertex coordinates3 ",self.vertexCoords[0]
        self.internalNodesAnz -= len(frontN)
        
        #print " internal points ",frontN,self.internalNodesAnz
        #print indPDO
        #raw_input()
        self.internalNodesAnzList = indPDO
        self.inFile.close()
        #
        # to have a mesh enabling to handle efficiently multiple bodies
        #
        print " mesh file name control: ",self.meshFileName[0:-4]
        #raw_input()
        print " vertex coordinates4 ",self.vertexCoords[0]
        if not subprocess.os.path.isdir(self.meshFileName[0:-4]):
            self._nodesReordering()
            pass
            #print "mesh dbg we reorder the file"
            #raw_input()
        #else:
        #    if not subprocess.os.path.exists("commandfile.eg"):
        #        raise Exception, " problem with the mesh handling"
        #    pass
        #
        #
        #
#        print " self.numElements",self.numElements
#        print " internal points ",frontN,self.internalNodesAnz,len(self.internalNodesAnzList)
        #print " ? ",self.elementArray
        #print " vertex coordinates5 ",self.vertexCoords[0]
        #print " vertex coordinates5 ",self.vertexCoords[0:100]
        #print dir(self.vertexCoords)
        #print "self.vertexCoords[:]",self.vertexCoords[0:-1]
        #raw_input("dbg 281")
        return {'vertexCoords': self.vertexCoords},\
                self.numElements, self.elementArray, self.physicalBodyNames,\
                self.internalNodesAnz, self.internalNodesAnzList
#            'vertexCoords': vertexCoords,
#            'faceVertexIDs': faceVertexIDs,
#            'cellFaceIDs': cellFaceIDs
#            self.numElements, self.elementArray, self.physicalBodyNames,\
#            self.internalNodesAnz,self.internalNodesAnzList

#
# end of GetData
#
    def getVertexCoords(self):
        return self.vertexCoords
        
    def getPermutedVertexCoords(self):
        return self.permutedVertexCoords

    def getBody(self, bodyName):
        return Body(self.physicalBodyNames.get(bodyName))[0]

    def getBoundary(self, boundaryName):
        return self.physicalBodyNames.get(boundaryName)[0]
        
    def _calcVertexCoords(self, coordDimensions):

        a = self.inFile.readline()                                                          # initialize the file input stream

        nodeToVertexIDdict = {}

        self.numVertices = int(self.inFile.readline())                                      # get the vertex coordinates
        #print "dbg contr ",self.numVertices
        #raw_input()
        ## scan the number of spatial dimensions
        ## not to be confused with the ultimate dimensionality of the mesh 
        ## (polygonal cells vs. polyhedral cells)
        savePos = self.inFile.tell()
        ##dimensions = len(self.inFile.readline().split()) - 1
        self.inFile.seek(savePos)
        
        self.vertexCoords = numpy.zeros((self.numVertices, coordDimensions))
        #print self.vertexCoords
        self.vertexCoords = self.vertexCoords.astype(numpy.float)
        #print self.vertexCoords
        for i in range(self.numVertices):
            currLineArray = self.inFile.readline().split()
            nodeToVertexIDdict[int(currLineArray[0])] = i
            self.vertexCoords[i] = [float(n) for n in currLineArray[1: coordDimensions + 1]]
            pass
        maxNode = max(nodeToVertexIDdict.keys())
        nodeToVertexIDs = numpy.zeros((maxNode + 1,))
        for i in nodeToVertexIDdict.keys():
            nodeToVertexIDs[i] = nodeToVertexIDdict[i]
            pass
        self.nodeToVertexIDs = nodeToVertexIDs
        return self.vertexCoords

    def _associateElementIDs(self):
        """
        enables to get elements associated to physical entities
        """
        for physBodyNames in self.physicalBodyNames.keys():
#            print "dbg physBodyNames",physBodyNames,self.physicalBodyNames[physBodyNames]
            indPBN = self.physicalBodyNames[physBodyNames][0]
#            print " within _associateElementIDs",physBodyNames,indPBN
            #raw_input("_associateElementIDs")
            assElementList = []
            for element in self.elementArray:
                if element[3] == self.physicalBodyNames[physBodyNames][0]:
                    assElementList.append(element[0])
                    pass
                pass
#            print physBodyNames,assElementList
            self.physicalBodyNames[physBodyNames][1] = assElementList
            pass
        return None
        #print self.physicalBodyNames
        
    def _calcCellVertexIDs(self):
        """
        Get the elements.
        
        .. note:: all we care about are the three-dimensional elements (cells).
        
        .. note:: so far this only supports tetrahedral and triangular meshes.
        """
        a = self.inFile.readline()                                                          ## skip the $EndNodes
        a = self.inFile.readline()                                                          ## skip the $Elements
        self.numElements = numElements = int(self.inFile.readline())
        #raw_input("dbg _calcCellVertexIDs, numElements: "+str(numElements))
        numCells = 0
#
# le parametre maxLength doit etre ajuste par une lecture prealable.
#        
        if self.dimensions !=1: maxLength = (4*self.dimensions + self.dimensions)
        else: maxLength = 8
        self.elementArray = numpy.zeros((numElements, maxLength),dtype=numpy.int )
#        print " numElements:",numElements
        #raw_input()
        for elm_number in range(numElements):
            currLineArrayInt = []
            for x in self.inFile.readline().split():
                currLineArrayInt.append(int(x))
                pass
#            print "dbg currLineArrayInt",i, currLineArrayInt
            self.elementArray[elm_number, :len(currLineArrayInt)] = currLineArrayInt
            pass
#        print self.elementArray
#        print " out of loop "
        validElementArray = numpy.compress(self.elementArray[:, 1] == ((2 * self.dimensions) - 2), self.elementArray, 0)
        cellNodeIDs = validElementArray[:, 5:]
        if len(cellNodeIDs)!= 0: cellVertexIDs = numpy.take(self.nodeToVertexIDs, cellNodeIDs)
        else: cellVertexIDs = numpy.array([])
        self.cellVertexIDs = cellVertexIDs
        self.numCells = len(cellVertexIDs)
        return None

    def _calcBaseFaceVertexIDs(self):
        
        cellVertexIDs = self.cellVertexIDs
    ## compute the face vertex IDs.
        cellFaceVertexIDs = numpy.ones((self.numCells, self.dimensions + 1, self.dimensions))
        cellFaceVertexIDs = -1 * cellFaceVertexIDs

        if (self.dimensions == 3):
            cellFaceVertexIDs[:, 0, :] = cellVertexIDs[:, :3]
            cellFaceVertexIDs[:, 1, :] = numpy.concatenate((cellVertexIDs[:, :2], cellVertexIDs[:, 3:]), axis = 1)
            cellFaceVertexIDs[:, 2, :] = numpy.concatenate((cellVertexIDs[:, :1], cellVertexIDs[:, 2:]), axis = 1)
            cellFaceVertexIDs[:, 3, :] = cellVertexIDs[:, 1:]
            pass
        if (self.dimensions == 2):
            cellFaceVertexIDs[:, 0, :] = cellVertexIDs[:, :2]
            cellFaceVertexIDs[:, 1, :] = numpy.concatenate((cellVertexIDs[:, 2:], cellVertexIDs[:, :1]), axis = 1)
            cellFaceVertexIDs[:, 2, :] = cellVertexIDs[:, 1:]
            pass
        cellFaceVertexIDs = cellFaceVertexIDs[:, :, ::-1]
        self.unsortedBaseIDs = numpy.reshape(cellFaceVertexIDs, (self.numCells * (self.dimensions + 1), self.dimensions))

        cellFaceVertexIDs = numpy.sort(cellFaceVertexIDs, axis = 2)
        baseFaceVertexIDs = numpy.reshape(cellFaceVertexIDs, (self.numCells * (self.dimensions + 1), self.dimensions))

        self.baseFaceVertexIDs = baseFaceVertexIDs       
        self.cellFaceVertexIDs = cellFaceVertexIDs
        return None

    def _calcFaceVertexIDs(self):

        self.faceStrToFaceIDs = {}
        faceStrToFaceIDsUnsorted = {}

        currIndex = 0

        for i in range(len(self.baseFaceVertexIDs)):
            listI = self.baseFaceVertexIDs[i]
            listJ = self.unsortedBaseIDs[i]

            key = ' '.join([str(i) for i in listI])
            if(not (self.faceStrToFaceIDs.has_key(key))):
                self.faceStrToFaceIDs[key] = currIndex
                faceStrToFaceIDsUnsorted[' '.join([str(j) for j in listJ])] = currIndex
                currIndex = currIndex + 1
                pass
            pass
        numFaces = currIndex
        faceVertexIDs = numpy.zeros((numFaces, self.dimensions))
        for i in faceStrToFaceIDsUnsorted.keys():
            faceVertexIDs[faceStrToFaceIDsUnsorted[i], :] = [int(x) for x in i.split(' ')]
            pass
        return faceVertexIDs

    def _calcCellFaceIDs(self):

        cellFaceIDs = numpy.zeros(self.cellFaceVertexIDs.shape[:2])
        for i in range(len(self.cellFaceVertexIDs)):
            cell = self.cellFaceVertexIDs[i]
            for j in range(len(cell)):
                cellFaceIDs[i, j] = self.faceStrToFaceIDs[' '.join([str(k) for k in self.cellFaceVertexIDs[i, j]])]
                pass
            pass
        return cellFaceIDs

    def _nodesReordering(self):
        """
        That function enables to reorder nodes, taking nodes appearance as criterium.
        It means, that the bodies creation order is of importance in the gmsh geo file.

        For boundaries:

         Boundaries are supposed to be of dimension N-1, N being the dimension of the domain.

        """
        #
        # the file commandfile.eg should not exist
        #
        if subprocess.os.path.exists("commandfile.eg"):
            try:
                retcode = subprocess.Popen("rm -f ./commandfile.eg",bufsize=-1, shell = True)
                #print " retcode ",dir(retcode)
                #raw_input("retour de rm -f commandfile.eg")
                
                if retcode < 0:
                    print >>sys.stderr, "Child was terminated by signal", -retcode
                else:
                    print >>sys.stderr, "Child process on commandfile.eg returned", retcode
            except OSError, e:
                print >>sys.stderr, "Execution failed:", e
        #raw_input("writing the commandfile.eg file with "+str(self.meshFileName))
        commandfile = open("commandfile.eg","w")
        commandfile.write ("Input File = "+self.meshFileName+"\n")
        commandfile.write ("Output File = "+self.meshFileName[0:-4]+"\n")
        commandfile.write ("Input Mode = Gmsh"+"\n")
        commandfile.write ("Output Mode = ElmerSolver"+"\n")
        commandfile.flush()
        commandfile.close ()
        #print "commandfile",commandfile.name
        while not osdotpath.exists(commandfile.name):
                                                                                            #
                                                                                            # We wait for the creation of the file. That process should stop
                                                                                            #
            time.sleep(.1)
            pass
                                                                                            #
                                                                                            # element types belonging to Physical Body Names of dimension N
                                                                                            #
        if self.dimensions == 1:
                                                                                            #
                                                                                            # 1 : 2 node line
                                                                                            #
            elm_typePBN = [1]
            pass
        elif self.dimensions == 2:
                                                                                            #
                                                                                            # 2 : 3 node triangle
                                                                                            # 3 : 4 node quadrangle
                                                                                            #
            elm_typePBN = [2,3]
            pass
        else:
                                                                                            #
                                                                                            # 4 : 4 node tetrahedron
                                                                                            # 5 : 8 node hexahedron
                                                                                            # 6 : 6 node prism
                                                                                            # 7 : 4 node node pyramid
                                                                                            #
            elm_typePBN = [4,5,6,7]
            pass
#        print " indPBN   ",indPBN,self.elementArray[0],self.elementArray[1]
#
# we identify nodes belonging to boundary: frontN list
#
        frontN = []
        if self.dimensions != 1:
            for element in self.elementArray:
            #
            # We consider boundaries and identify nodes belonging to
            #
                if element[1] not in elm_typePBN: # we suppose boundaries being 1 dimension smaller as the problem dimension
                    indRef = 3 + element[2]
                    for vertex in  range(indRef,indRef+_nodeElements(element[1])):
                        if element[vertex] not in frontN and element[vertex]>0:
                            frontN.append(element[vertex])
                            pass
                        pass
                    pass
                pass
            pass
        else:
            for element in self.elementArray:
                if element[1] not in elm_typePBN:
                    frontN.append(element[0])
                    pass
                pass
            pass
        #
        # We build up the permutation
        #
        permutation = [-1]*(self.numVertices+1)
        #
        # indC is used to control the end of the loop
        #
        indC = 1                                # starting at 1 because nodes are indexed from 1 upwards
        #
        # keys are made of body names
        #
        indexBody = []
        for body in self.physicalBodyNames.keys(): indexBody.append(str(self.physicalBodyNames[body][0])+"_"+body)
        #
        # We respect the order introduced in the mesh file, first for physical body names of dimension N
        # ignoring boundary nodes
        #
        indexBody.sort()
        #print indexBody
        #raw_input("dbg index body ")
        for ibody in indexBody:
            #body = ibody[1:]
            body = ibody.split("_")[1]
            indPBN = self.physicalBodyNames[body][0]
            print "self.physicalBodyNames[body][0]: ",indPBN
            #
            print "self.physicalBodyNames[body][1]: ",self.physicalBodyNames[body][1]
            for elm_number in self.physicalBodyNames[body][1]:
            
                #print body,indPBN,elm_number,self.elementArray[elm_number-1]
                
                element = self.elementArray[elm_number-1]
                #print "element", element, "body: ",ibody
                if element[1] in elm_typePBN:
                    indRef = 3 + element[2]

                    for vertex_index in  range(indRef,indRef+_nodeElements(element[1])):
                
                        vertex = element[vertex_index]
                    
                        if permutation[vertex] == -1 and element[vertex_index]>0 and vertex not in frontN:
                            permutation[vertex] = indC
                            indC+=1
                            pass
                        pass
                    pass
                pass
            pass
        #raw_input()
        #
        # We use a second loop to get the permutation of boundary nodes
        #
        for vertex in frontN:
            permutation[vertex] = indC
            indC+=1
            pass
        indt = 0
        #for i in permutation:
        #    print "permutation ",indt,i
        #    indt+=1
        #    pass
        #raw_input()
        #
        # Now we reindex the nodes using a temporary file
        #
        self.permutedVertexCoords = [[0.0]*len(self.vertexCoords[0])]*(len(self.vertexCoords)+1)
        #raw_input(" dimension of self.vertexCoords[0]: "+str(len(self.vertexCoords[0])))
        #raw_input(" dimension of self.vertexCoords: "+str(len(self.vertexCoords)))

        for vertex_index in range(1,len(self.vertexCoords)+1):
            self.permutedVertexCoords[permutation[vertex_index]] = self.vertexCoords[vertex_index-1]
            pass
#        coordFile = open("coordFile","w")
#        coordFile.write ("POINTS %5d float\n"%(len(self.vertexCoords)))
        
#        for vertex_index in range(len(self.vertexCoords)+1):
#            coordFile.write(" %5d %15.10e %15.10e\n"%(vertex_index, tempCoordList[vertex_index][0], tempCoordList[vertex_index][1]))
            
#        coordFile.write("CELLS %5d float\n"%(len(self.elementArray)))
        #print self.elementArray
        #raw_input("elementArray")
        
        ind = 0
        for element in self.elementArray:
            indRef = 3 + element[2]
            if ind == 0: print indRef, element[1], _nodeElements(element[1])
            for vertex_index in range( indRef, indRef+_nodeElements(element[1])):                
                self.elementArray[ind][vertex_index] = permutation[self.elementArray[ind][vertex_index]]
                pass
            ind+= 1
            pass

        #print self.elementArray
        #raw_input("new elementArray")
#        for i in self.elementArray:
#            print i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9]
         #raw_input("reordering")
#        coordFile.write ("CELLS %5d float\n"%(len(self.elementArray)))
#        coordFile.close ()
        print " self.vertexCoords ", len(self.vertexCoords)
        del(self.vertexCoords)
        print " self.permutedVertexCoords ", len(self.permutedVertexCoords)
        #raw_input(" permuted coord")
        self.vertexCoords = self.permutedVertexCoords[1:]
        print " self.vertexCoords ", len(self.vertexCoords)
        #raw_input(" comparaison ")
        #print self.vertexCoords;raw_input("reordering1")
        #print "string  rm -f "+self.meshFileName
        #raw_input()
        #self.meshFileName = "essai.msh"
        if osdotpath.exists(self.meshFileName): 
            retcode = subprocess.call("mv -f"+self.meshFileName+" toto.msh", shell=True)
            pass
#        print " return code ",retcode
#        while (retcode != 0):
#            pass
#        print " return code ",retcode
        #raw_input()
        reorderedMeshFile = open (self.meshFileName,"w")
        #raw_input("we write the mesh again: "+reorderedMeshFile.name)
        reorderedMeshFile.write("$MeshFormat\n")
        reorderedMeshFile.write(" %s %s %s\n"%(self.version, self.fileType, self.datasize))
        reorderedMeshFile.write("$EndMeshFormat\n")
        reorderedMeshFile.write("$PhysicalNames\n")
        reorderedMeshFile.write("%2d\n"%(len(self.physicalBodyNames.keys())))
        ind = 1
        for ibody in indexBody:
            if ind < 10:
                format = "%d %2d \""+"%"+str(len(ibody.split("_")[1]))+"s"+"\"\n"
                reorderedMeshFile.write (format%(self.dimensions, ind, ibody.split("_")[1]))
                pass
            else:
                format = "%d %2d \""+"%"+str(len(ibody.split("_")[1]))+"s"+"\"\n"
                reorderedMeshFile.write (format%(self.dimensions, ind, ibody.split("_")[1]))
                pass
            ind+=1
            pass
        reorderedMeshFile.write("$EndPhysicalNames\n")
        reorderedMeshFile.write("$Nodes\n")
        reorderedMeshFile.write("%6d\n"%(self.numVertices))
        ind = 1
        for node in self.permutedVertexCoords[1:]: # node indexation beginning at 1
            if len(node) == 1:
                reorderedMeshFile.write ("%2d %15.8e 0 0\n"%(ind, node[0]))
                pass
            if len(node) == 2:
                reorderedMeshFile.write ("%2d %15.8e %15.8e 0\n"%(ind, node[0], node[1]))
                pass
            elif len(node) == 3:
                reorderedMeshFile.write ("%2d %15.8e %15.8e %15.8e\n"%(ind, node[0], node[1], node[2]))
                pass
            ind+=1
            pass
        reorderedMeshFile.write ("$EndNodes\n")
        reorderedMeshFile.write ("$Elements\n")
        reorderedMeshFile.write ("%6d\n"%(len(self.elementArray)))
        format = " %d"
        for element in self.elementArray:
            #
            # elm_number
            #
            reorderedMeshFile.write (format%(element[0]))
            #
            # elm_type
            #
            reorderedMeshFile.write (format%(element[1]))
            #
            # number of tags
            #
            reorderedMeshFile.write (format%(element[2]))
            indRef = 3 + element[2]
            for tag in range(3,indRef):
                reorderedMeshFile.write (format%(element[tag]))
                pass
            #
            # number of nodes
            #
            indRef = 3 + element[2]
            for node in range(indRef,indRef+_nodeElements(element[1])):
                reorderedMeshFile.write (format%(element[node]))
                pass
            reorderedMeshFile.write ("\n")
            pass
        reorderedMeshFile.write ("$EndElements\n")
        reorderedMeshFile.flush()
        #raw_input("closing the mesh : "+reorderedMeshFile.name)
        reorderedMeshFile.close()
        #print subprocess.os.system("ls -lt ./essai.msh")
        #raw_input()
        while not osdotpath.exists(reorderedMeshFile.name):
                                                                                            #
                                                                                            # It should wait
                                                                                            #
            time.sleep(0.1)
            pass
        if not subprocess.os.path.exists(self.meshFileName[0:-4]):
            print "  creating the directory ",self.meshFileName[0:-4]
            subprocess.os.mkdir (self.meshFileName[0:-4])
            while not osdotpath.exists(self.meshFileName[0:-4]):
                time.sleep(0.1)
                pass
            #
            # Now, we launch ElmerGrid
            #
            try:
                retcode = subprocess.call("ElmerGrid commandfile.eg", shell=True)
                #raw_input("we have called ElmerGrid")
                if retcode < 0:
                    print >>sys.stderr, "Child was terminated by signal", -retcode
                else:
                    print >>sys.stderr, "Child process ElmerGrid commandfile.eg returned", retcode
            except OSError, e:
                print >>sys.stderr, "Execution failed:", e
            pass
        else:
            #raw_input(" the directory exists")
            subprocess.Popen("./ElmerGrid commandfile.eg", shell = True)
            pass
        #
        # we call the Elmer processor
        #
        # The lines hereafter enable to consider the permutation induced by ElmerGrid
        #
        return None

class CommonMesh(object):
    """
    Generic mesh class defining implementation-agnostic behavior.

    Make changes to mesh here first, then implement specific implementations in
    `pyMesh` and `numMesh`.

    Meshes contain cells, faces, and vertices.

    """

    def __init__(self):
        self.scale = {
                      'length': 1.,
                      'area': 1.,
                      'volume': 1.
                      }
#
# commented but has to be reintroduced
#   
#   self._calcTopology()

#
# the line self._calcGeometry() has been commented
# to be handled.
#   
#   self._calcGeometry()
    
    def __add__(self, other):
        """
        Either translate a `Mesh` or concatenate two `Mesh` objects.
        
            >>> from fipy.meshes.grid2D import Grid2D
            >>> baseMesh = Grid2D(dx = 1.0, dy = 1.0, nx = 2, ny = 2)
            >>> print baseMesh.getCellCenters()
            [[ 0.5, 0.5,]
             [ 1.5, 0.5,]
             [ 0.5, 1.5,]
             [ 1.5, 1.5,]] 1
             
        If a vector is added to a `Mesh`, a translated `Mesh` is returned
        
            >>> translatedMesh = baseMesh + (5, 10)
            >>> translatedMesh.getCellCenters()
            [[  5.5, 10.5,]
             [  6.5, 10.5,]
             [  5.5, 11.5,]
             [  6.5, 11.5,]]
             
        If a `Mesh` is added to a `Mesh`, a concatenation of the two 
        `Mesh` objects is returned
        
            >>> addedMesh = baseMesh + (baseMesh + (2, 0))
            >>> addedMesh.getCellCenters()
            [[ 0.5, 0.5,]
             [ 1.5, 0.5,]
             [ 0.5, 1.5,]
             [ 1.5, 1.5,]
             [ 2.5, 0.5,]
             [ 3.5, 0.5,]
             [ 2.5, 1.5,]
             [ 3.5, 1.5,]]
        
        The two `Mesh` objects must be properly aligned in order to concatenate them
        
            >>> addedMesh = baseMesh + (baseMesh + (3, 0))
            Traceback (most recent call last):
            ...
            MeshAdditionError: Vertices are not aligned

            >>> addedMesh = baseMesh + (baseMesh + (2, 2))
            Traceback (most recent call last):
            ...
            MeshAdditionError: Faces are not aligned

        No provision is made to avoid or consolidate overlapping `Mesh` objects
        
            >>> addedMesh = baseMesh + (baseMesh + (1, 0))
            >>> addedMesh.getCellCenters()
            [[ 0.5, 0.5,]
             [ 1.5, 0.5,]
             [ 0.5, 1.5,]
             [ 1.5, 1.5,]
             [ 1.5, 0.5,]
             [ 2.5, 0.5,]
             [ 1.5, 1.5,]
             [ 2.5, 1.5,]]
             
        Different `Mesh` classes can be concatenated
         
            >>> from fipy.meshes.tri2D import Tri2D
            >>> triMesh = Tri2D(dx = 1.0, dy = 1.0, nx = 2, ny = 1)
            >>> triMesh = triMesh + (2, 0)
            >>> triAddedMesh = baseMesh + triMesh
            >>> triAddedMesh.getCellCenters()
            [[ 0.5       , 0.5       ,]
             [ 1.5       , 0.5       ,]
             [ 0.5       , 1.5       ,]
             [ 1.5       , 1.5       ,]
             [ 2.83333333, 0.5       ,]
             [ 3.83333333, 0.5       ,]
             [ 2.5       , 0.83333333,]
             [ 3.5       , 0.83333333,]
             [ 2.16666667, 0.5       ,]
             [ 3.16666667, 0.5       ,]
             [ 2.5       , 0.16666667,]
             [ 3.5       , 0.16666667,]]

        but their faces must still align properly
        
            >>> triMesh = Tri2D(dx = 1.0, dy = 2.0, nx = 2, ny = 1)
            >>> triMesh = triMesh + (2, 0)
            >>> triAddedMesh = baseMesh + triMesh
            Traceback (most recent call last):
            ...
            MeshAdditionError: Faces are not aligned

        `Mesh` concatenation is not limited to 2D meshes
        
            >>> from fipy.meshes.grid3D import Grid3D
            >>> threeDBaseMesh = Grid3D(dx = 1.0, dy = 1.0, dz = 1.0, 
            ...                         nx = 2, ny = 2, nz = 2)
            >>> threeDSecondMesh = Grid3D(dx = 1.0, dy = 1.0, dz = 1.0, 
            ...                           nx = 1, ny = 1, nz = 1)
            >>> threeDAddedMesh = threeDBaseMesh + (threeDSecondMesh + (2, 0, 0))
            >>> threeDAddedMesh.getCellCenters()
            [[ 0.5, 0.5, 0.5,]
             [ 1.5, 0.5, 0.5,]
             [ 0.5, 1.5, 0.5,]
             [ 1.5, 1.5, 0.5,]
             [ 0.5, 0.5, 1.5,]
             [ 1.5, 0.5, 1.5,]
             [ 0.5, 1.5, 1.5,]
             [ 1.5, 1.5, 1.5,]
             [ 2.5, 0.5, 0.5,]]

        but the different `Mesh` objects must, of course, have the same 
        dimensionality.
        
            >>> InvalidMesh = threeDBaseMesh + baseMesh
            Traceback (most recent call last):
            ...
            MeshAdditionError: Dimensions do not match
        """
        pass
        
    def __mul__(self, factor):
        """
        Dilate a `Mesh` by `factor`.
        
            >>> from fipy.meshes.grid2D import Grid2D
            >>> baseMesh = Grid2D(dx = 1.0, dy = 1.0, nx = 2, ny = 2)
            >>> print baseMesh.getCellCenters()
            [[ 0.5, 0.5,]
             [ 1.5, 0.5,]
             [ 0.5, 1.5,]
             [ 1.5, 1.5,]] 1
             
        The `factor` can be a scalar
        
            >>> dilatedMesh = baseMesh * 3
            >>> dilatedMesh.getCellCenters()
            [[ 1.5, 1.5,]
             [ 4.5, 1.5,]
             [ 1.5, 4.5,]
             [ 4.5, 4.5,]]
             
        or a vector
        
            >>> dilatedMesh = baseMesh * (3, 2)
            >>> dilatedMesh.getCellCenters()
            [[ 1.5, 1. ,]
             [ 4.5, 1. ,]
             [ 1.5, 3. ,]
             [ 4.5, 3. ,]]
        
        but the vector must have the same dimensionality as the `Mesh`
        
            >>> dilatedMesh = baseMesh * (3, 2, 1)
            Traceback (most recent call last):
            ...
            ValueError: frames are not aligned

        """
        pass
        
    def __repr__(self):
        return "%s()" % self.__class__.__name__
        
    """topology methods"""
    
    def _calcTopology(self):
        self._calcInteriorAndExteriorFaceIDs()
        self._calcInteriorAndExteriorCellIDs()
        self._calcCellToFaceOrientations()
        self._calcAdjacentCellIDs()
        self._calcCellToCellIDs()
        self._calcCellToCellIDsFilled()
        return None
       
    """calc topology methods"""
    
    def _calcInteriorAndExteriorFaceIDs(self):
        pass

    def _calcExteriorCellIDs(self):
        pass
    
    def _calcInteriorCellIDs(self):
        pass
##  self.interiorCellIDs = list(sets.Set(range(self.numberOfCells)) - sets.Set(self.exteriorCellIDs))
##        onesWhereInterior = numpy.zeros(self.numberOfCells)
##        numpy.put(onesWhereInterior, self.exteriorCells, numpy.zeros((len(self.exteriorCellIDs))))
##        self.interiorCellIDs = numpy.nonzero(onesWhereInterior)
##        self.interiorCellIDs = (0,0)
        
    def _calcInteriorAndExteriorCellIDs(self):
        self._calcExteriorCellIDs()
        self._calcInteriorCellIDs()
        return None

    def _calcCellToFaceOrientations(self):
        pass

    def _calcAdjacentCellIDs(self):
        pass

    def _calcCellToCellIDs(self):
        pass

    def _calcCellToCellIDsFilled(self):
        N = self.getNumberOfCells()
        M = self._getMaxFacesPerCell()
        cellIDs = numpy.reshape(numpy.repeat(numpy.arange(N), M), (N, M))
        cellToCellIDs = self._getCellToCellIDs()
        self.cellToCellIDsFilled = MA.where(MA.getmaskarray(cellToCellIDs), cellIDs, cellToCellIDs)

    
    """get topology methods"""

    def _getFaceVertexIDs(self):
        return self.faceVertexIDs

    def _getCellFaceIDs(self):
        return self.cellFaceIDs

    def getExteriorFaces(self):
        pass

    def getInteriorFaces(self):
        pass
    
    def _getExteriorCellIDs(self):
        """ Why do we have this?!? It's only used for testing against itself? """
        return self.exteriorCellIDs

    def _getInteriorCellIDs(self):
        """ Why do we have this?!? It's only used for testing against itself? """
        return self.interiorCellIDs

    def _getCellFaceOrientations(self):
        return self.cellToFaceOrientations

    def getNumberOfCells(self):
        return self.numberOfCells
    
    def _getNumberOfVertices(self):
        #print " dbg mesh vertex Coord ", self.vertexCoords[0]
        #print " dbg mesh vertex Coord1 ", self.vertexCoords[1]
        return len(self.vertexCoords)
    
    def _getAdjacentCellIDs(self):
        return self.adjacentCellIDs

    def getDim(self):
        return self.dim

    def _getCellsByID(self, ids = None):
        pass
        
    def getCells(self, filter = None, ids = None, **args):
        """Return `Cell` objects of `Mesh`."""
        cells = self._getCellsByID(ids)
    
        if filter is not None:
            cells = [cell for cell in cells if filter(cell, **args)]

        return cells
        
    def _getFaces(self):
        pass
    
    def getFaces(self, filter = None, **args):
        """Return `Face` objects of `Mesh`."""
        faces = self._getFaces()
    
        if filter is not None:
            return [face for face in faces if filter(face, **args)]

        return faces

    def _getMaxFacesPerCell(self):
        pass

    def _getNumberOfFaces(self):
        return self.numberOfFaces

    def _getCellToCellIDs(self):
        return self.cellToCellIDs

    def _getCellToCellIDsFilled(self):
        return self.cellToCellIDsFilled
    
    """geometry methods"""
    
    def _calcGeometry(self):
        self._calcFaceAreas()
        self._calcFaceNormals()
        self._calcOrientedFaceNormals()
        self._calcCellVolumes()
        self._calcCellCenters()
        self._calcFaceToCellDistances()
        self._calcCellDistances()        
        self._calcFaceTangents()
        self._calcCellToCellDistances()
        self._calcScaledGeometry()
        self._calcCellAreas()
        return None
       
    """calc geometry methods"""
    
    def _calcFaceAreas(self):
        pass
    
    def _calcFaceNormals(self):
        pass
    
    def _calcOrientedFaceNormals(self):
        pass
    
    def _calcCellVolumes(self):
        pass
    
    def _calcCellCenters(self):
        pass
    
    def _calcFaceToCellDistances(self):
        pass

    def _calcCellDistances(self):
        pass
        
    def _calcAreaProjections(self):
        pass

    def _calcOrientedAreaProjections(self):
        pass

    def _calcFaceTangents(self):
        pass

    def _calcFaceToCellDistanceRatio(self):
        pass

    def _calcFaceAspectRatios(self):
        self.faceAspectRatios = self._getFaceAreas() / self._getCellDistances()

    def _calcCellToCellDistances(self):
        pass

#    def _calcCellAreas(self):
#        from fipy.tools.numerix import MAtake
#        self.cellAreas =  MAtake(self._getFaceAreas(), self.cellFaceIDs)
    
    """get geometry methods"""
        
    def _getFaceAreas(self):
        return self.scaledFaceAreas

    def _getFaceNormals(self):
        return self.faceNormals
    
    def getCellVolumes(self):
        return self.scaledCellVolumes

    def getCellCenters(self):
        return self.scaledCellCenters

    def _getFaceToCellDistances(self):
        return self.scaledFaceToCellDistances

    def _getCellDistances(self):
        return self.scaledCellDistances

    def _getFaceToCellDistanceRatio(self):
        return self.faceToCellDistanceRatio

    def _getOrientedAreaProjections(self):
        return self.orientedAreaProjections

    def _getAreaProjections(self):
        return self.areaProjections

    def _getOrientedFaceNormals(self):
        return self.orientedFaceNormals

    def _getFaceTangents1(self):
        return self.faceTangents1

    def _getFaceTangents2(self):
        return self.faceTangents2
    
    def _getFaceAspectRatios(self):
        return self.faceAspectRatios
    
    def _getCellToCellDistances(self):
        return self.scaledCellToCellDistances

    def _getCellNormals(self):
        return self.cellNormals

    def _getCellAreas(self):
        return self.cellAreas

    def _getCellAreaProjections(self):
        return self.cellNormals * self._getCellAreas()[..., numpy.NewAxis]

    """scaling"""

    
    """point to cell distances"""
    


class Mesh(CommonMesh):
    """
        Generic mesh class using Numeric to do the calculations

        Meshes contain cells, faces, and vertices.

        This is built for a non-mixed element mesh.
    """

#    def __init__(self, vertexCoords, faceVertexIDs, cellFaceIDs):
    def __init__(self, vertexCoords = None, numElements = None, elementArray = None, physicalBodyNames = None,\
                 internalNodesAnzList = None):
        """
        faceVertexIds and cellFacesIds must be padded with minus ones.
        """

        self.vertexCoords       = vertexCoords
        self.numElements        = numElements
        self.elementArray       = elementArray
        self.physicalBodyNames = physicalBodyNames
        self.internalNodesAnzList = internalNodesAnzList
        if type(vertexCoords) == NoneType:
            self.dim = 2
            pass
        else:
            #print "1161 Mesh self.vertexCoords[0]:",self.vertexCoords
            self.dim = len(self.vertexCoords[0])
            pass
        #print " class mesh",self.dim
        #raw_input(" class mesh")
        self.meshType = "unstructured"
        #self.faceVertexIDs = MA.array(faceVertexIDs)
        #self.cellFaceIDs = MA.array(cellFaceIDs)

        CommonMesh.__init__(self)
        
    def getBody(self, bodyName):
        #
        # indPDO list of nodes associated to the body. A node can belong to several bodies
        #
        if self.physicalBodyNames.has_key(bodyName):
            indPBN = self.physicalBodyNames[bodyName][0]
            frontN = []
            indPDO = []
            #print " self.elementArray ",len(self.elementArray),self.elementArray[0]
            for element in self.elementArray:
                if element[3] == indPBN:
                    indRef = 3 + element[2]
                    for ind in range(indRef,len(element)):
                        if element[ind] not in indPDO and element[ind]!=0:
                            indPDO.append(element[ind])
                            pass
                        pass
                    pass
                pass
#            if element[3] == indPBN:
#              if element[6]!=0 and element[6] not in indPDO:
#                indPDO.append(element[6])
#              if element[7]!=0 and element[7] not in indPDO:
#                indPDO.append(element[7])
#              if element[8]!=0 and element[8] not in indPDO:
#                indPDO.append(element[8])
#              if element[9]!=0 and element[9] not in indPDO:
#                indPDO.append(element[9])
#
# a node can belong to several regions!!!!
#        
            #print " mesh dbg getBody nodes found ",len(indPDO),self.dim
            #raw_input()
            if len(self.physicalBodyNames[bodyName]) == 3:
                bodyDimension = self.physicalBodyNames[bodyName][2]
                pass
            else:
                bodyDimension = self.dim
                pass
            return Body(self.physicalBodyNames.get(bodyName), bodyName, indPDO, nodes = self.vertexCoords, dim = bodyDimension)
        else:
            return None

    """
    Topology methods
    """

    def __add__(self, other):
        if(isinstance(other, Mesh)): return self._concatenate(other, smallNumber = 1e-15)
        else: return self._translate(other)

    def __mul__(self, factor):
        newCoords = self.vertexCoords * factor
        newmesh = Mesh(newCoords, numpy.array(self.faceVertexIDs), numpy.array(self.cellFaceIDs))
        return newmesh

    def _concatenate(self, other, smallNumber):
        return Mesh(**self._getAddedMeshValues(other, smallNumber))

    def _connectFaces(self, faces0, faces1):
        """
        
        Merge faces on the same mesh. This is used to create periodic
        meshes. The first list of faces, `faces1`, will be the faces
        that are used to add to the matrix diagonals. The faces in
        `faces2` will not be used. They aren't deleted but their
        adjacent cells are made to point at `faces1`. The list
        `faces2` are not altered, they still remain as members of
        exterior faces.

           >>> from fipy.meshes.numMesh.grid2D import Grid2D
           >>> mesh = Grid2D(nx = 2, ny = 2, dx = 1., dy = 1.)

           >>> print mesh._getCellFaceIDs()
           [[ 0, 7, 2, 6,]
            [ 1, 8, 3, 7,]
            [ 2,10, 4, 9,]
            [ 3,11, 5,10,]]
            
           >>> mesh._connectFaces(mesh.getFacesLeft(), mesh.getFacesRight())

           >>> print mesh._getCellFaceIDs()
           [[ 0, 7, 2, 6,]
            [ 1, 6, 3, 7,]
            [ 2,10, 4, 9,]
            [ 3, 9, 5,10,]]
        
        """

        ## check for errors

        ## check that faces are members of exterior faces
        from sets import Set
        assert Set(faces0).union(Set(faces1)).issubset(Set(self.getExteriorFaces()))

        ## following assert checks number of faces are equal, normals are opposite and areas are the same
        assert numpy.take(self.areaProjections, faces0) == numpy.take(-self.areaProjections, faces1)

        ## extract the adjacent cells for both sets of faces
        faceCellIDs0 = self.faceCellIDs[:,0]
        faceCellIDs1 = self.faceCellIDs[:,1]
        ## set the new adjacent cells for `faces0`
        MA.put(faceCellIDs1, faces0, MA.take(faceCellIDs0, faces0))
        MA.put(faceCellIDs0, faces0, MA.take(faceCellIDs0, faces1))
        self.faceCellIDs[:,0] = faceCellIDs0
        self.faceCellIDs[:,1] = faceCellIDs1
        
        ## extract the face to cell distances for both sets of faces
        faceToCellDistances0 = self.faceToCellDistances[:,0]
        faceToCellDistances1 = self.faceToCellDistances[:,1]
        ## set the new faceToCellDistances for `faces0`
        MA.put(faceToCellDistances1, faces0, MA.take(faceToCellDistances0, faces0))
        MA.put(faceToCellDistances0, faces0, MA.take(faceToCellDistances0, faces1))
        self.faceToCellDistances[:,0] = faceToCellDistances0
        self.faceToCellDistances[:,1] = faceToCellDistances1

        ## calculate new cell distances and add them to faces0
        numpy.put(self.cellDistances, faces0, MA.take(faceToCellDistances0 + faceToCellDistances1, faces0))

        ## change the direction of the face normals for faces0
        for dim in range(self.getDim()):
            faceNormals = self.faceNormals[:,dim].copy()
            numpy.put(faceNormals, faces0, MA.take(faceNormals, faces1))
            self.faceNormals[:,dim] = faceNormals
            pass
        ## Cells that are adjacent to faces1 are changed to point at faces0
        ## get the cells adjacent to faces1
        faceCellIDs = MA.take(self.faceCellIDs[:,0], faces1)
        ## get all the adjacent faces for those particular cells
        cellFaceIDs = MA.take(self.cellFaceIDs[:], faceCellIDs)
        for i in range(len(cellFaceIDs[0,:])):
            ## if the faces is a member of faces1 then change the face to point at
            ## faces0
            cellFaceIDs[:,i] = MA.where(cellFaceIDs[:,i] == faces1,
                                        faces0,
                                        cellFaceIDs[:,i])
            ## add those faces back to the main self.cellFaceIDs
            tmp = self.cellFaceIDs[:,i]
            MA.put(tmp, faceCellIDs, cellFaceIDs[:,i])
            self.cellFaceIDs[:,i] = tmp
            pass
        ## calculate new topology
        _CommonMesh._calcTopology(self)

        ## calculate new geometry
        self._calcFaceToCellDistanceRatio()
        self._calcCellToCellDistances()
        self._calcScaledGeometry()
        self._calcFaceAspectRatios()
        
    def _getConcatenableMesh(self):
        return self
        
    def _getAddedMeshValues(self, other, smallNumber):
        """
        Returns a `dictionary` with 3 elements: the new mesh vertexCoords, faceVertexIDs, and cellFaceIDs.
        """
        
        other = other._getConcatenableMesh()
        
        selfNumFaces = self.faceVertexIDs.shape[0]
        selfNumVertices = self.vertexCoords.shape[0]
        otherNumFaces = other.faceVertexIDs.shape[0]
        otherNumVertices = other.vertexCoords.shape[0]
        ## check dimensions
        if(self.vertexCoords.shape[1] != other.vertexCoords.shape[1]):
            raise MeshAdditionError, "Dimensions do not match"
        ## compute vertex correlates
        vertexCorrelates = {}
        for i in range(selfNumVertices):
            for j in range(otherNumVertices):
                diff = self.vertexCoords[i] - other.vertexCoords[j]
                diff = numpy.array(diff)
                if (sum(diff ** 2) < smallNumber):
                    vertexCorrelates[j] = i
                    pass
                pass
            pass
        if (vertexCorrelates == {}):
            raise MeshAdditionError, "Vertices are not aligned"
        ## compute face correlates
        faceCorrelates = {}
        for i in range(otherNumFaces):
            currFace = other.faceVertexIDs[i]
            keepGoing = 1
            currIndex = 0
            for item in currFace:
                if (vertexCorrelates.has_key(item)):
                    currFace[currIndex] = vertexCorrelates[item]
                    currIndex = currIndex + 1
                    pass
                else:
                    keepGoing = 0
                    pass
                pass
            if (keepGoing == 1):
                for j in range(selfNumFaces):
                    if (self._equalExceptOrder(currFace, self.faceVertexIDs[j])):
                        faceCorrelates[i] = j
                        pass
                    pass
                pass
            pass
        if(faceCorrelates == {}): raise MeshAdditionError, "Faces are not aligned"

        faceIndicesToAdd = ()
        for i in range(otherNumFaces):
            if(not faceCorrelates.has_key(i)): faceIndicesToAdd = faceIndicesToAdd + (i,)
            pass
        vertexIndicesToAdd = ()
        for i in range(otherNumVertices):
            if(not vertexCorrelates.has_key(i)): vertexIndicesToAdd = vertexIndicesToAdd + (i,)
            pass

        ##compute the full face and vertex correlation list
        a = selfNumFaces
        for i in faceIndicesToAdd:
            faceCorrelates[i] = a
            a = a + 1
            pass
        b = selfNumVertices
        for i in vertexIndicesToAdd:
            vertexCorrelates[i] = b
            b = b + 1
            pass
        ## compute what the cells are that we need to add
        cellsToAdd = numpy.ones((other.cellFaceIDs.shape[0], self.cellFaceIDs.shape[1]))
        cellsToAdd = -1 * cellsToAdd

        for i in range(len(other.cellFaceIDs)):
            for j in range(len(other.cellFaceIDs[i])):
                cellsToAdd[i, j] = faceCorrelates[other.cellFaceIDs[i, j]]
                pass
            pass

        cellsToAdd = MA.masked_values(cellsToAdd, -1)


        ## compute what the faces are that we need to add
        facesToAdd = numpy.take(other.faceVertexIDs, faceIndicesToAdd)
        for i in range(len(facesToAdd)):
            for j in range(len(facesToAdd[i])):
                facesToAdd[i, j] = vertexCorrelates[facesToAdd[i, j]]
                pass
            pass
        #
        # compute what the vertices are that we need to add
        #
        verticesToAdd = numpy.take (other.vertexCoords, vertexIndicesToAdd)

        return {
            'vertexCoords': numpy.concatenate((self.vertexCoords, verticesToAdd)),
            'faceVertexIDs': numpy.concatenate((self.faceVertexIDs, facesToAdd)),
            'cellFaceIDs': MA.concatenate((self.cellFaceIDs, cellsToAdd))
            }

    def _equalExceptOrder(self, first, second):
        """
        Determines if two lists contain the same set of elements,
        although they may be in different orders.
        Does not work if one list contains duplicates of an element.
        """
        res = 0
        if (len(first) == len(second)):
            res = 1
            pass
        for i in first:
            isthisin = 0
            for j in second:
                if (i == j):
                    isthisin = 1
                    pass
                pass
            if(isthisin == 0):
                res = 0
                pass
            pass
        return res
    

    def _translate(self, vector):
        newCoords = self.vertexCoords + vector
        newmesh = Mesh(newCoords, numpy.array(self.faceVertexIDs), numpy.array(self.cellFaceIDs))
        return newmesh

    def _calcTopology(self):
        self.dim = len(self.vertexCoords[0])
        self.numberOfFaces = len(self.faceVertexIDs)
        self.numberOfCells = len(self.cellFaceIDs)
        self._calcFaceCellIDs()

    """
    calc Topology methods
    """

    def _calcFaceCellIDs(self):
        array = MA.indices((len(self.cellFaceIDs), len(self.cellFaceIDs[0])))[0]
        array = MA.array(data = array, mask = self.cellFaceIDs.mask()).flat
        cellFaceIDsFlat = MA.ravel(self.cellFaceIDs)
        firstRow = MA.zeros(self.numberOfFaces)
        secondRow = MA.zeros(self.numberOfFaces)
        MA.put(firstRow, cellFaceIDsFlat[::-1], array[::-1])
        MA.put(secondRow, cellFaceIDsFlat, array)
        secondRow = MA.array(data = secondRow, mask = (secondRow == firstRow))
        self.faceCellIDs = MA.zeros((len(firstRow),2))
        self.faceCellIDs[:,0] = firstRow[:]
        self.faceCellIDs[:,1] = secondRow[:]

class Mesh1D(Mesh):
    def __init__(self, filename):
        vertices, numElements, elementArray,\
        physicalBodyNames, internalNodesAnz, internalNodesAnzList =\
        DataGetter().getData(filename, dimensions = 1)
        self.spaceDimensions = 1
        self.vertices = vertices
        self.numElements = numElements
        self.numberOfCells = numElements
        self.physicalBodyNames = physicalBodyNames

        self.internalNodesAnz = internalNodesAnz
        self.internalNodesAnzList = internalNodesAnzList
        Mesh.__init__(self, vertices["vertexCoords"], numElements, elementArray, physicalBodyNames, internalNodesAnzList)
        self.meshFileName = filename
        self.xextension = max(self.getNodesCoordinates()) - min(self.getNodesCoordinates())
        #
        # we set by default the extension to 1 in the y and z direction
        #
        self.yextension = 1.
        self.zextension = 1.

    def getConnectivity(self):
        connectivity = []
        connectivitylist = []
        for key in self.physicalBodyNames.keys():
            print key,type(key)
            if self.physicalBodyNames[key]:
                elementId = self.physicalBodyNames[key][0]
                for element in self.elementArray:
                
                    if element[3] == elementId:
                        if element[0] not in connectivitylist:
                            connectivity.append(element)
                            connectivitylist.append(element[0])
                            pass
                        pass
                    pass
                pass
            pass
        return connectivity
           
    def getPhysicalBodyNames(self):
        return self.physicalBodyNames.keys()
        
    getBodies = getPhysicalBodyNames
        
    def getDimensionString(self):
        return "1D"

    def getElAnz(self):
        print "dbg getElAnz",self.numElements
        return self.numElements

    def getMeshType(self):
        return self.meshType
        
    def getName(self):
        return self.meshFileName
        
    def getNodesAnz(self):
        return len(self.vertices['vertexCoords'])
        
    def getSpaceDimensions(self):
        return self.spaceDimensions
        
    getDim = getSpaceDimensions
    getMeshDimension = getSpaceDimensions
        
    def getType(self):
        """
        We get only one element type. 
        It means that the mesh topology must be uniform: only one element type is treated. In 1D it is the case.
        """
        gmshType = self.elementArray[self.physicalBodyNames.items()[0][1][1][0]][1]
       
        return gmshType, _typeConverter(gmshType)
        
    def getNodesCoordinates(self):
        return self.vertices['vertexCoords']
        
    def getNodesXCoordinates(self):
        #print self.vertices['vertexCoords']
        #return map(lambda x: x[0],self.vertices['vertexCoords'].tolist())
        if type(self.vertices['vertexCoords']) == ListType:
            return map(lambda x: x[0],self.vertices['vertexCoords'])
            pass
        else:
            return map(lambda x: x[0], self.vertices['vertexCoords'].tolist())
            pass

class Mesh2D(Mesh):
    def __init__(self, filename):
        vertices, numElements, elementArray,\
        physicalBodyNames, internalNodesAnz, internalNodesAnzList =\
        DataGetter().getData(filename, dimensions = 2)
        self.spaceDimensions = 2
        self.vertices = vertices
        #print " self.vertices",len(vertices),vertices["vertexCoords"]
        #raw_input()
        self.numElements = numElements
        self.numberOfCells = numElements
        self.physicalBodyNames = physicalBodyNames

        self.internalNodesAnz = internalNodesAnz
        self.internalNodesAnzList = internalNodesAnzList
        #print ' dbg mesh element array', len(elementArray), numElements
        #print ' element array',physicalBodyNames, internalNodesAnz
        #raw_input("dbg mesh element array")
        #for i in elementArray:
            #print i
        #print vertices["vertexCoords"]
        #raw_input("vertices")
        Mesh.__init__(self, vertices["vertexCoords"], numElements, elementArray, physicalBodyNames, internalNodesAnzList)
        self.meshFileName = filename
        self.xextension = max(self.getNodesXCoordinates()) - min(self.getNodesXCoordinates())
        self.yextension = max(self.getNodesYCoordinates()) - min(self.getNodesYCoordinates())
        #
        # we set by default the extension to 1 in the z direction
        #
        self.zextension = 1.
        
    def getConnectivity(self):
        connectivity = []
        connectivitylist = []
#        print " mesh dbg",self.physicalBodyNames
        #raw_input("toto")
        for key in self.physicalBodyNames.keys():
            print key,type(key)
            if self.physicalBodyNames[key]:
#                print key
                elementId = self.physicalBodyNames[key][0]
#                print " dbg mesh elementId",key,elementId
                for element in self.elementArray:
                
                    if element[3] == elementId:
                        if element[0] not in connectivitylist:
#                            print element, type(element)
                            connectivity.append(element)
                            connectivitylist.append(element[0])
                            pass
                        pass
                    pass
                pass
            pass
#        print len(connectivity),len(connectivitylist)
        return connectivity
           
    def getPhysicalBodyNames(self):
        return self.physicalBodyNames.keys()
        
    getBodies = getPhysicalBodyNames
        
    def getDimensionString(self):
        return "2D"
        
    def getElAnz(self):
        print "dbg getElAnz",self.numElements
        return self.numElements

    def getName(self):
        return self.meshFileName
        
    def getNodesAnz(self):
        #print "dbg getNodesAnz 2D",len(self.vertices['vertexCoords'])
        #raw_input()
        return len(self.vertices['vertexCoords'])
        
    def getSpaceDimensions(self):
        return self.spaceDimensions
        
    getDim = getSpaceDimensions
    getMeshDimension = getSpaceDimensions
        
    def getType(self):
        """
        We get only one element type.
        It means that the mesh topology must be uniform: only one element type is treated.
        """
        #print " dbg getType ",self.elementArray[self.physicalBodyNames.items()[0][1][1][0]][1],self.elementArray[self.physicalBodyNames["domain"][1][0]][1]
        #raw_input(" dbg getType ")
        #gmshType = self.elementArray[self.physicalBodyNames["domain"][1][0]][1]
        gmshType = self.elementArray[self.physicalBodyNames.items()[0][1][1][0]][1]
       
        return gmshType, _typeConverter(gmshType)
        
    def getNodesCoordinates(self):
        #print self.vertices['vertexCoords']
        return self.vertices['vertexCoords']
    getVertexCoords = getNodesCoordinates
        
    def getNodesXCoordinates(self):
        #print self.vertices['vertexCoords']
        #print "self.vertices: ",type(self.vertices['vertexCoords'])
        #print dir(self.vertices)
        #raw_input("dbg getNodesXCoordinates")
        if type(self.vertices['vertexCoords']) == ListType:
            return map(lambda x: x[0],self.vertices['vertexCoords'])
            pass
        else:
            return map(lambda x: x[0], self.vertices['vertexCoords'].tolist())
            pass
        
    def getNodesYCoordinates(self):
        #print self.vertices['vertexCoords']
        if type(self.vertices['vertexCoords']) == ListType:
            return map(lambda x: x[-1],self.vertices['vertexCoords'])
            pass
        else:
            return map(lambda x: x[-1],self.vertices['vertexCoords'].tolist())
            pass
    
    def getMeshType(self):
        return self.meshType

class Mesh3D(Mesh):
    """
        To handle 3D meshes
    """
    def __init__(self, filename):
        vertices, numElements, elementArray, physicalBodyNames, internalNodesAnz, internalNodesAnzList =\
        DataGetter().getData(filename, dimensions = 3)
        self.spaceDimensions = 3
        self.vertices = vertices
        self.numElements = numElements
        self.numberOfCells = numElements
        self.physicalBodyNames = physicalBodyNames

        self.internalNodesAnz = internalNodesAnz
        self.internalNodesAnzList = internalNodesAnzList
        print ' number of vertices ',    len(self.vertices)
        print '         elments',       self.numElements
        print '         nbcells',       self.numberOfCells
#        print '         pBNames',       self.physicalBodyNames
        #raw_input("dbg azerty class Mesh")
        Mesh.__init__(self, vertices["vertexCoords"], numElements, elementArray, physicalBodyNames, internalNodesAnzList)
        print "data getter ",len(self.vertices)
        #raw_input( "Mesh3D")
        self.meshFileName = filename
        #raw_input(" dbg call to mesh init is over ")
        self.xextension = max(self.getNodesXCoordinates()) - min(self.getNodesXCoordinates())
        self.yextension = max(self.getNodesYCoordinates()) - min(self.getNodesYCoordinates())
        self.zextension = max(self.getNodesZCoordinates()) - min(self.getNodesZCoordinates())
        
    def getConnectivity(self):
        connectivity = []
        connectivitylist = []
        for key in self.physicalBodyNames.keys():
            print key,type(key)
            if self.physicalBodyNames[key]:
#                print key
                elementId = self.physicalBodyNames[key][0]
#                print " dbg mesh elementId",key,elementId
                for element in self.elementArray:
                
                    if element[3] == elementId:
                        if element[0] not in connectivitylist:
#                            print element, type(element)
                            connectivity.append(element)
                            connectivitylist.append(element[0])
                            pass
                        pass
                    pass
                pass
            pass
#        print len(connectivity),len(connectivitylist)
        return connectivity

    def getDimensionString(self):
        return "3D"
  
    def getElAnz(self):
        #print "dbg getElAnz",self.numElements
        return self.numElements

    def getMeshType(self):
        return self.meshType

    def getName(self):
        return self.meshFileName

    def getNodesAnz(self):
        return len(self.vertices['vertexCoords'])

    def getNodesCoordinates(self):
        #print self.vertices['vertexCoords'][0], self.vertices['vertexCoords'][1], self.vertexCoords[1]
        
        return self.vertices['vertexCoords']
    getVertexCoordinates = getNodesCoordinates
    
    def getPhysicalBodyNames(self):
        return self.physicalBodyNames.keys()

    getBodies = getPhysicalBodyNames

    def getSpaceDimensions(self):
        return self.spaceDimensions
        
    getDim = getSpaceDimensions
    getMeshDimension = getSpaceDimensions

    def getType(self):
        #print self.physicalBodyNames["domain"]
        #print " dbg getType ",self.elementArray[self.physicalBodyNames["domain"][1][0]]
        #raw_input(" dbg getType ")
        #gmshType = self.elementArray[self.physicalBodyNames["domain"][1][0]][1]
        gmshType = self.elementArray[self.physicalBodyNames.items()[0][1][1][0]][1]

        return gmshType, _typeConverter(gmshType)

    def getNodesXCoordinates(self):
        #print self.vertices['vertexCoords']
        #print "self.vertices: ",type(self.vertices['vertexCoords'])
        #print dir(self.vertices)
        #raw_input("dbg getNodesXCoordinates")
        if type(self.vertices['vertexCoords']) == ListType:
            return map(lambda x: x[0],self.vertices['vertexCoords'])
            pass
        else:
            return map(lambda x: x[0], self.vertices['vertexCoords'].tolist())
            pass
        
    def getNodesYCoordinates(self):
        #print self.vertices['vertexCoords']
        if type(self.vertices['vertexCoords']) == ListType:
            return map(lambda x: x[1],self.vertices['vertexCoords'])
            pass
        else:
            return map(lambda x: x[1],self.vertices['vertexCoords'].tolist())
            pass
        
    def getNodesZCoordinates(self):
        #print self.vertices['vertexCoords']
        if type(self.vertices['vertexCoords']) == ListType:
            return map(lambda x: x[-1],self.vertices['vertexCoords'])
            pass
        else:
            return map(lambda x: x[-1],self.vertices['vertexCoords'].tolist())
            pass
        
#    def getNodesXCoordinates(self):
#        #print self.vertices['vertexCoords']
#        return map(lambda x: x[0],self.vertices['vertexCoords'].tolist())
        
#    def getNodesYCoordinates(self):
#        #print self.vertices['vertexCoords']
#        return map(lambda x: x[1],self.vertices['vertexCoords'].tolist())
        
#    def getNodesZCoordinates(self):
#        #print self.vertices['vertexCoords']
#        return map(lambda x: x[-1],self.vertices['vertexCoords'].tolist())

class GmshImporter2D(Mesh2D):

    def __init__(self, filename):
        vertices, numElements, self.elementArray, physicalBodyNames, internalNodesAnz , internalNodesAnzList =\
        DataGetter().getData(filename, dimensions = 2)
#
        Mesh.__init__(self, vertices["vertexCoords"], numElements, self.elementArray, physicalBodyNames, internalNodesAnz)

    def getCellVolumes(self):
        return abs(mesh2D.Mesh2D.getCellVolumes(self))

    def getNodesAnz(self):
        #print "dbg getNodesAnz",len(vertices)
        return len(vertices)

class GmshImporter2DIn3DSpace(GmshImporter2D):
    def __init__(self, filename):
        GmshImporter2D.__init__(self, filename, coordDimensions = 3)

class GmshImporter3D(Mesh):
    """
        >>> mesh = GmshImporter3D('fipy/meshes/numMesh/testgmsh.msh')
    """
    def __init__(self, filename):
        vertices, numElements, self.elementArray, physicalBodyNames, internalNodesAnz = DataGetter().getData(filename, dimensions = 3)
        Mesh.__init__(self, vertices["vertexCoords"], numElements, self.elementArray, physicalBodyNames, internalNodesAnz)

    def getCellVolumes(self):
        return abs(mesh.Mesh.getCellVolumes(self))
   
def _typeConverter(cellType):
    """
    That function is used to connect gmsh to vtk.
    It returns the vtk cell type.
    """
    if cellType == 1:
        return 3
    if cellType == 2: # 3-node triangle
        return 5
    if cellType == 3: # 4-node quadrangle
        return 9
    if cellType == 4: # 4-node tetrahedron
        return 10
    if cellType == 5: # 8-node hexahedron
        return 12
    if cellType == 6: # 6-node prism
        return 13
    if cellType == 7: # 5-node pyradim
        return 14
        
def _nodeElements(element):
    """
    That function is used to return the number of
    nodes associated to the element
    """
    if element == 1: # 2-node line
        return 2
    elif element == 2: # 3-node triangle
        return 3
    elif element == 3: # 4-node quadrangle
        return 4
    elif element == 4: # 4-node tetrahedron
        return 4
    elif element == 5: # 8-node hexahedron
        return 8
    elif element == 6: # 6-node prism
        return 6
    elif element == 7: # 5-node pyradim
        return 5
    elif element == 15: # point
        return 1

