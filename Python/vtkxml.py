#!/usr/bin/env python
from __future__ import absolute_import
from generictools import Generic

from types import StringType
from six.moves import range

class XmlVtkUnstructured(Generic):
    """
    
    USAGE:
    vtk_writer = XmlVtkUnstructured()
    vtk_writer.snapshot("filename.vtu", x, y, z, NumberOfCells, 
                        Connectivity, 
                        Offsets, 
                        TypeCells, 
                        NameScalarPoint, 
                        ScalarValuePoint, 
                        NameScalarCell, 
                        ScalarValueCell
                       )
    vtk_writer.writePVD("filename.vtu")
    
    """
    def __init__(self,fileName):
        Generic.__init__(self)
        if type(fileName) not in [StringType,noneType]:
            raise Exception(" the XmlVtkUnstructured class argument has to be a String ")
        else:
            if ".vtu" not in fileName:
                if "." in fileName:
                    fileName.replace(".","").append(".vtu")
                    pass
                pass
            self.fileName = fileName
                
                

    def snapshot(self,
                 x,                              # list of mesh point coordinates
                 y,
                 z,
                 NumberOfCells,                  
                 Connectivity,                   
                 Offsets,                        # list of number of points for each cells
                 TypeCells, 
                 NameScalarPoint, 
                 ScalarValuePoint, 
                 NameScalarCell         = None, 
                 ScalarValueCell        = None
                ):
        """
        ARGUMENTS:
        fileName         file name and/or path/filename
        x                array of x coordinates of particle centers
        y                array of y coordinates of particle centers
        z                array of z coordinates of particle centers
        NumberOfCells    number of cells 
        Connectivity     array of connectivity for each cell
        Offsets      array of number of points of each cells 
        TypeCells    array of type number of each cells
        NameScalarPoint  array of scalar name for a scalar on the points
        ScalarValuePoint array of scalar value of each points (first all the points with the value of the first scalar,
                 then all the points with the value of the second scalar...)
        NameScalarCell   idem for the cells 
        ScalarValueCell  idem for the cells
        """
        import xml.dom.minidom
        #import xml.dom.ext # python 2.5 and later        

        # Document and root element
        doc = xml.dom.minidom.Document()
        root_element = doc.createElementNS("VTK", "VTKFile")
        root_element.setAttribute("type", "UnstructuredGrid")
        root_element.setAttribute("version", "0.1")
        root_element.setAttribute("byte_order", "LittleEndian")
        doc.appendChild(root_element)

        # Unstructured grid element
        unstructuredGrid = doc.createElementNS("VTK", "UnstructuredGrid")
        root_element.appendChild(unstructuredGrid)

        # Piece 0 (only one)
        piece = doc.createElementNS("VTK", "Piece")
        piece.setAttribute("NumberOfPoints", str(len(x)))
        piece.setAttribute("NumberOfCells", str(NumberOfCells))
        unstructuredGrid.appendChild(piece)

        ### Points ####
        points = doc.createElementNS("VTK", "Points")
        piece.appendChild(points)

        # Point location data
        point_coords = doc.createElementNS("VTK", "DataArray")
        point_coords.setAttribute("type", "Float32")
        point_coords.setAttribute("format", "ascii")
        point_coords.setAttribute("NumberOfComponents", "3")
        points.appendChild(point_coords)

        string = str()
        for i in range(len(x)-1):
            string = string + repr(x[i]) + ' ' + repr(y[i]) \
                    + ' ' + repr(z[i]) + "\n"
            pass
        string = string + repr(x[len(x)-1]) + ' ' + repr(y[len(x)-1]) \
                    + ' ' + repr(z[len(x)-1]) 
        point_coords_data = doc.createTextNode(string)
        point_coords.appendChild(point_coords_data)

        #### Cells ####
        cells = doc.createElementNS("VTK", "Cells")
        piece.appendChild(cells)

        # Cell locations
        
        cell_connectivity = doc.createElementNS("VTK", "DataArray")
        cell_connectivity.setAttribute("type", "Int32")
        cell_connectivity.setAttribute("Name", "connectivity")
        cell_connectivity.setAttribute("format", "ascii")        
        cells.appendChild(cell_connectivity)

        # Cell location data
        
        string = str()
        k=0
        for i in range(1,len(Offsets)):
            if i!=1 :
                for j in range(1,Offsets[i-1]-Offsets[i-2]+1):
                    string = string + repr(Connectivity[k]) + ' '
                    k=k+1
                    pass
                pass
            else :
                for j in range(1,Offsets[i-1]+1):
                    string = string + repr(Connectivity[k]) + ' '
                    k=k+1
                    pass
                pass
            string = string + "\n"
            pass
        for j in range(1,Offsets[len(Offsets)-1]-Offsets[len(Offsets)-2]+1):
            string = string + repr(Connectivity[k]) + ' '
            k=k+1
            pass
                    
        connectivity = doc.createTextNode(string)
        cell_connectivity.appendChild(connectivity)

        cell_offsets = doc.createElementNS("VTK", "DataArray")
        cell_offsets.setAttribute("type", "Int32")
        cell_offsets.setAttribute("Name", "offsets")
        cell_offsets.setAttribute("format", "ascii")                
        cells.appendChild(cell_offsets)
        
        string = str()
        for i in range(len(Offsets)-1):
            string = string + repr(Offsets[i]) + "\n"
            pass
        string = string + repr(Offsets[len(Offsets)-1])
          
        offsets = doc.createTextNode(string)
        cell_offsets.appendChild(offsets)

        cell_types = doc.createElementNS("VTK", "DataArray")
        cell_types.setAttribute("type", "UInt8")
        cell_types.setAttribute("Name", "types")
        cell_types.setAttribute("format", "ascii")                
        cells.appendChild(cell_types)
        
        string = str()
        for i in range(len(TypeCells)-1):
            string = string + repr(TypeCells[i]) + "\n"
            pass      
        string = string + repr(TypeCells[len(TypeCells)-1]) 
        
        types = doc.createTextNode(string)
        cell_types.appendChild(types)

        #### Data at Points ####
         
        if len(ScalarValuePoint)>0 :
        
            NumberOfScalar = len (NameScalarPoint)
            point_data = doc.createElementNS("VTK", "PointData")
            for l in range (NumberOfScalar) :
                

                point_data.setAttribute("Scalar", NameScalarPoint[l])
                piece.appendChild(point_data)
        

    # Data at Points location data
    
                point_data_coords = doc.createElementNS("VTK", "DataArray")
                point_data_coords.setAttribute("type", "Float32")
                point_data_coords.setAttribute("Name", NameScalarPoint[l])
                point_data_coords.setAttribute("format", "ascii")
                point_data.appendChild(point_data_coords)        
        
                string = str()
                for i in range(len(x)):
                    string = string + repr(ScalarValuePoint[i+l*len(x)]) + "\n"
                    pass
                string = string + repr((l+1)*len(x)-1)    
        
                point_data_coords_data = doc.createTextNode(string)
                point_data_coords.appendChild(point_data_coords_data)
                pass    
        else:  
            point_data = doc.createElementNS("VTK", "PointData")
            piece.appendChild(point_data)
            pass
               

        #### Cell data (dummy) ####
        
        if len(ScalarValueCell)>0:
            
            NumberOfScalar = len (NameScalarCell)
            cell_data = doc.createElementNS("VTK", "CellData")
            for l in range (NumberOfScalar) :
            
                cell_data.setAttribute("Scalar", NameScalarCell)
                piece.appendChild(cell_data)
        

    # Data at Cells location data
    
                cell_data_coords = doc.createElementNS("VTK", "DataArray")
                cell_data_coords.setAttribute("type", "Float32")
                cell_data_coords.setAttribute("Name", NameScalarCell)
                cell_data_coords.setAttribute("format", "ascii")
                cell_data.appendChild(cell_data_coords)        
        
                string = str()
                for i in range(NumberOfCells-1):
                    string = string + repr(ScalarValueCell[i]) + "\n"
                    pass
                string = string + repr(ScalarValueCell[NumberOfCells-1])   
                   
                cell_data_coords_data = doc.createTextNode(string)
                cell_data_coords.appendChild(cell_data_coords_data)
                pass
            pass 
        else:
            cell_data = doc.createElementNS("VTK", "CellData")
            piece.appendChild(cell_data)
            pass

        # Write to file and exit
        outFile = open(fileName, 'w')
    #xml.dom.ext.PrettyPrint(doc, file)
        doc.writexml(outFile, newl='\n')
        outFile.close()
        self.fileNames.append(fileName)
        
    def writePVD(self, fileName):
        outFile = open(fileName, 'w')
        import xml.dom.minidom

        pvd = xml.dom.minidom.Document()
        pvd_root = pvd.createElementNS("VTK", "VTKFile")
        pvd_root.setAttribute("type", "Collection")
        pvd_root.setAttribute("version", "0.1")
        pvd_root.setAttribute("byte_order", "LittleEndian")
        pvd.appendChild(pvd_root)

        collection = pvd.createElementNS("VTK", "Collection")
        pvd_root.appendChild(collection)

        for i in range(len(self.fileNames)):
            dataSet = pvd.createElementNS("VTK", "DataSet")
            dataSet.setAttribute("timestep", str(i))
            dataSet.setAttribute("group", "")
            dataSet.setAttribute("part", "0")
            dataSet.setAttribute("file", str(self.fileNames[i]))
            collection.appendChild(dataSet)
            pass

        outFile = open(fileName, 'w')
        pvd.writexml(outFile, newl='\n')
        outFile.close()


