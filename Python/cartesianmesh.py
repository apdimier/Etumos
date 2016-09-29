"""
Used to handle a cartesian structured Mesh
ie a mesh where meshlines are straight lines"""

from __future__ import absolute_import
from __future__ import print_function
import numpy

from listtools import toList

from mpoints import *
from six.moves import range


def _verifyDimensions(obj1, obj2):
    """Raises an exception if the two objects don't have the same dimensions"""
    if obj1.getDimensions() != obj2.getDimensions():
        raise Warning("The two objects don't have the same dimension")

def _verifyIndexOrder(index1, index2):
    """Raises an exception if the two indices are not ordered"""
    if index1 > index2:
        raise Warning("Indices are not correctly ordered")

def _verifyIndices(index1, index2):
    _verifyDimensions(index1, index2)
    _verifyIndexOrder(index1, index2)


class AbstractIndex:
    """Abstract class for all n-dimensional Indexes."""

class Index1D(AbstractIndex):

    def __init__(self, i):
        self.i = i

    def getDimensions(self):
        return 1

    def getValues(self):
        return self.i

    def outOfBounds(self, min, max):
        return self.i < min or self.i >= max

    def __cmp__(self, other):
        return cmp(self.i, other.i)

class Index2D(AbstractIndex):

    def __init__(self, i, j):
        self.i = i
        self.j = j

    def getDimensions(self):
        return 2

    def getValues(self):
        return self.i, self.j

    def outOfBounds(self, xxx_todo_changeme, xxx_todo_changeme1):
        (i_min, j_min) = xxx_todo_changeme
        (i_max, j_max) = xxx_todo_changeme1
        return self.i < i_min or self.i >= i_max or \
               self.j < j_min or self.j >= j_max

    def __cmp__(self, other):
        return cmp([self.j, self.i], [other.j, other.i])

class Index3D(AbstractIndex):

    def __init__(self, i, j, k):
        self.i = i
        self.j = j
        self.k = k

    def getDimensions(self):
        return 3

    def getValues(self):
        return self.i, self.j, self.k

    def outOfBounds(self, xxx_todo_changeme2, xxx_todo_changeme3):
        (i_min, j_min, k_min) = xxx_todo_changeme2
        (i_max, j_max, k_max) = xxx_todo_changeme3
        return self.i < i_min or self.i >= i_max or \
               self.j < j_min or self.j >= j_max or \
               self.k < k_min or self.k >= k_max

    def __cmp__(self, other):
        return cmp([self.k, self.j, self.i], 
                   [other.k, other.j, other.i])

def Index(*values):
    """Return an instance of Index1D, Index2D or Index3D,
    based on the number of indexes (i,j,k) given."""
    if len(values) == 1:
        return Index1D(*values)
    elif len(values) == 2:
        return Index2D(*values)
    else:
        return Index3D(*values)


class CartesianZone:
    """Two indices and a name."""

    def __init__(self, name, index_min, index_max):
        """Multi-dimensional 'box'.

        index_min & index_max represent the two opposing corners of the box.
        If the box is defined between (i0,j0,k0) and (i1,j1,k1) _included_, then
        index_min = Index(i0, j0, k0)
        index_max = Index(i1+1, j1+1, k1+1)
        This is consistent with python list notation.
        """
        _verifyIndices(index_min, index_max)
        self.name = name
        self.min = index_min
        self.max = index_max

    def getDimensions(self):
        return self.dims

    getSpaceDimension = getDimensions
    
    
    def getName(self):
        return self.name

    def getIndexMin(self):
        return self.min

    def getIndexMax(self):
        return self.max

    def containsZone(self, other):
        """A Zone contains itself."""
        for corner_index in other.getCornerIndexes():
            if not self.containsIndex(corner_index):
                return 0
        return 1

    def intersectsZone(self, other):
        for corner_index in other.getCornerIndexes():
            if self.containsIndex(corner_index):
                return 1
        return 0


class CartesianZone1D(CartesianZone):
    dims = 1
    def containsIndex(self, index):
        i = index.getValues()
        i0 = self.min.getValues()
        i1 = self.max.getValues()
        return i0 <= i and i < i1

    def getCornerIndexes(self):
        i0 = self.getIndexMin().getValues()
        i1 = self.getIndexMax().getValues() - 1
        return [Index1D(i0), Index1D(i1)]

    def setMap(self, map, value):
        i0 = self.min.getValues()
        i1 = self.max.getValues()
        map[i0:i1] = value


class CartesianZone2D(CartesianZone):
    dims = 2
    def containsIndex(self, index):
        i,j = index.getValues()
        i0, j0 = self.min.getValues()
        i1, j1 = self.max.getValues()
        return i0 <= i and i < i1 and \
           j0 <= j and j < j1

    def getCornerIndexes(self):
        i0, j0 = self.getIndexMin().getValues()
        i1, j1 = self.getIndexMax().getValues()
        i1 -= 1; j1 -= 1
        return [Index2D(i0,j0), Index2D(i1,j0),
                Index2D(i1,j1), Index2D(i0,j1)]

    def setMap(self, map, value):
        i0, j0 = self.min.getValues()
        i1, j1 = self.max.getValues()
        map[i0:i1, j0:j1] = value


class CartesianZone3D(CartesianZone):
    dims = 3
    def containsIndex(self, index):
        i, j, k = index.getValues()
        i0, j0, k0 = self.min.getValues()
        i1, j1, k1 = self.max.getValues()
        return i0 <= i and i < i1 and \
           j0 <= j and j < j1 and \
           k0 <= k and k < k1

    def getCornerIndexes(self):
        i0, j0, k0 = self.getIndexMin().getValues()
        i1, j1, k1 = self.getIndexMax().getValues()
        i1 -= 1; j1 -= 1; k1 -= 1
        return [Index3D(i0,j0,k0), Index3D(i1,j0,k0),
                Index3D(i1,j1,k0), Index3D(i0,j1,k0),
                Index3D(i0,j0,k1), Index3D(i1,j0,k1),
                Index3D(i1,j1,k1), Index3D(i0,j1,k1)]

    def setMap(self, map, value):
        i0, j0, k0 = self.min.getValues()
        i1, j1, k1 = self.max.getValues()
        map[i0:i1, j0:j1, k0:k1] = value


class Cell:

    def getDimensions(self):
        return self.dims

    def getNbNodes(self):
        return self.nbNodes

    def getNbSides(self):
        return self.nbSides

class CartesianCell(Cell):
    def __init__(self, mesh, number):        
        self.mesh = mesh
        self.nb = number

    def getNb(self):
        return self.nb


class CartesianCell1D(CartesianCell):
    dims = 1
    nbNodes = 2
    nbSides = 2

    def __init__(self, mesh, number, index):
        CartesianCell.__init__(self, mesh, number)
        self.i = index.getValues()

    def getIndex(self):
        return Index1D(self.i)

    def getCenter(self):
        xs = self.mesh.coords[0]
        cx = 0.5 * (xs[self.i+1] + xs[self.i])
        return Point1D(cx)

    def getNeighborsNb(self):
        toNb = self.mesh.toCellNb
        i_west = Index1D(self.i-1)
        i_east = Index1D(self.i+1)
        return [toNb(i_west), toNb(i_east)]

    def getSidesNb(self):
        """Return a list of sides numbers.

        The order is: [west, east]."""
        side_west = self.i
        side_east = self.i + 1
        return [side_west, side_east]

    def getSidesVolumes(self):
        return [1., 1.]

    def getVolume(self):
        xs = self.mesh.coords[0]
        dx = xs[self.i+1] - xs[self.i]
        return dx


class CartesianCell2D(CartesianCell):
    dims = 2
    nbNodes = 4
    nbSides = 4

    def __init__(self, mesh, number, index):
        CartesianCell.__init__(self, mesh, number)
        i, j = index.getValues()
        self.i = i
        self.j = j

    def getIndex(self):
        return Index2D(self.i, self.j)

    def getCenter(self):
        xs = self.mesh.coords[0]
        ys = self.mesh.coords[1]
        cx = 0.5 * (xs[self.i] + xs[self.i+1])
        cy = 0.5 * (ys[self.j] + ys[self.j+1])

    def getNeighborsNb(self):
        toNb = self.mesh.toCellNb
        i_sud = Index2D(self.i, self.j-1)
        i_east = Index2D(self.i+1, self.j)
        i_north = Index2D(self.i, self.j+1)
        i_west = Index2D(self.i-1, self.j)
        return [toNb(i_sud), toNb(i_east), toNb(i_north), toNb(i_west)]

    def getSidesNb(self):
        """Return a list of sides numbers.

        The order is: [sud, east, north, west]."""
        i = self.i
        j = self.j
        getEastSide = self.mesh.getEastSideNb
        side_east = getEastSide(i, j)
        side_north = side_east + 1
        if i == 0:
            side_west = side_north + 1
        else:
            side_west =  getEastSide(i-1, j)
        if j == 0:
            side_sud = side_east - 1
        else:
            side_sud = getEastSide(i, j-1) + 1
        return [side_sud, side_east, side_north, side_west]

    def getSidesVolumes(self):
        xs = self.mesh.coords[0]
        ys = self.mesh.coords[1]
        dx = xs[self.i+1] - xs[self.i]
        dy = ys[self.j+1] - ys[self.j]
        return [dx, dy, dx, dy]

    def getVolume(self):
        xs = self.mesh.coords[0]
        ys = self.mesh.coords[1]
        dx = xs[self.i+1] - xs[self.i]
        dy = ys[self.j+1] - ys[self.j]
        return dx * dy

    def getCellNodes(self) :
        return self.i, self.j        

class CartesianCell3D(CartesianCell):
    dims = 3
    nbNodes = 8
    nbSides = 6

    def __init__(self, mesh, number, index):
        CartesianCell.__init__(self, mesh, number)
        i, j, k = index.getValues()
        self.i = i
        self.j = j
        self.k = k

    def getCenter(self):
        xs = self.mesh.coords[0]
        ys = self.mesh.coords[1]
        zs = self.mesh.coords[2]
        cx = 0.5 * (xs[self.i] + xs[self.i+1])
        cy = 0.5 * (ys[self.j] + ys[self.j+1])
        cz = 0.5 * (zs[self.k] + zs[self.k+1])
        return Point3D(cx, cy, cz)

    def getIndex(self):
        return Index3D(self.i, self.j, self.k)

    def getNeighborsNb(self):
        toNb = self.mesh.toCellNb
        i_bottom = Index3D(self.i, self.j, self.k-1)
        i_top = Index3D(self.i, self.j, self.k+1)
        i_sud = Index3D(self.i, self.j-1, self.k)
        i_east = Index3D(self.i+1, self.j, self.k)
        i_north = Index3D(self.i, self.j+1, self.k)
        i_west = Index3D(self.i-1, self.j, self.k)
        return [toNb(i_bottom), toNb(i_top),
                toNb(i_sud), toNb(i_east), toNb(i_north), toNb(i_west)]

    def getSidesVolumes(self):
        """[Z-, Z+, Y-, X+, Y+, X-]"""
        xs = self.mesh.coords[0]
        ys = self.mesh.coords[1]
        zs = self.mesh.coords[2]
        dx = xs[self.i+1] - xs[self.i]
        dy = ys[self.j+1] - ys[self.j]
        dz = zs[self.k+1] - zs[self.k]
        vxy = dx * dy
        vxz = dx * dz
        vyz = dy * dz
        return [vxy, vxy, vxz, vyz, vxz, vyz] 

    def getVolume(self):
        xs = self.mesh.coords[0]
        ys = self.mesh.coords[1]
        zs = self.mesh.coords[2]
        dx = xs[self.i+1] - xs[self.i]
        dy = ys[self.j+1] - ys[self.j]
        dz = zs[self.k+1] - zs[self.k]
        return dx * dy * dz

class CartesianMesh:

    flag_names = ['ZoneMap']

    def __init__(self, name):
        self.name = name
        self.coords = self.dims * [None]
        self.nb_of_intervals = self.dims * [None]
        self.zones = []
        self.zone_names = []
        self.boundaryZones = []
        self.boundaryZone_names = []
        self.flags = {}
        for key in self.flag_names:
            self.flags[key] = 0

    def getAxis(self, axis):
        """Return the NumPy array with the axis coordinates."""
        return self.coords[self.getAxisIndex(axis)]

    def getAxisNames(self):
        return self.axis_names

    def getAxisIndex(self, axis_name):
        return self.axis_names.index(axis_name)

    def getCells(self):
        cells = []
        for i in range(self.getNbCells()):
            cells.append(self.getCell(i))
        return cells

    def getCoordinateSystem(self):
        return self.coord_system

    def getDimensions(self):
        return self.dims

    def getElementTypes(self):
        return [self.element_type]

    def getNbPoints(self, axis):
        return self.nb_of_intervals[self.getAxisIndex(axis)] + 1

    def getMeshType(self):
        return "Cartesian"

    def getNbIntervals(self, axis):
        return self.nb_of_intervals[self.getAxisIndex(axis)]

    def getMeshType(self):
        return "Cartesian"

    def getSpaceDimensions(self):
        return self.dims
        
    getSpaceDimension = getSpaceDimensions

    def getType(self):
        return "Cartesian"
#-------------------------------------------
# Begin Zones operations

    def getZones(self):
        return self.zones

    def getNbZones(self):
        """ Return the number of define zones """
        return len(self.zones) 

    def getZone(self, index):
        nz = len(self.zones)
        for ii in range(nz):
            i = nz - 1 - ii
            zone = self.zones[i]
            if zone.containsIndex(index):
                return zone
        raise IncorrectValue("Ohoops, fell of the cliff")

    def getZoneIndex(self, zone_name):
        return self.zone_names.index(zone_name)

    def getZoneName(self, zone_index):
        return self.zone_names[zone_index]

    def setZone(self, name, index_min, index_max):
        """See CartesianZone for the specifications of the indices."""
        zone = self.makeZone(name, index_min, index_max)
        self.zones.append(zone)
        if name not in self.zone_names:
            self.zone_names.append(name)
        self.flags['ZoneMap'] = 0

# End of Zones operations
#----------------------------------------
# Begin of boundary zones operations

    def getBoundaryZones(self):
        return self.boundaryZones

    def getNbBoundaryZones(self):
        """ Return the number of define zones """
        return len(self.boundaryZones) 


    def getBoundaryZoneIndex(self, zone_name):
        return self.boundaryZone_names.index(zone_name)

    def getBoundaryZoneName(self, zone_index):
        return self.boundaryZone_names[zone_index]

    def setBoundaryZone(self, name, index_min, index_max):
        """See CartesianZone for the specifications of the indices."""
        zone = self.makeZone(name, index_min, index_max)
        self.boundaryZones.append(zone)
        if name not in self.boundaryZone_names:
            self.boundaryZone_names.append(name)
        self.flags['ZoneMap'] = 0


# End of Boundary Zones operations
#----------------------------------------

    def setAxis(self, axisName, coordinates):
        """
        A list of already defined coordinates is treated
        """
        if axisName not in self.axis_names: raise Exception(" checking the axis name  to be in setAxis")
        axisIndex = self.getAxisIndex(axisName)
        self.coords[axisIndex] = numpy.array(coordinates, numpy.float)
        self.nb_of_intervals[axisIndex] = len(coordinates) - 1

    def setdAxis(self, axisName, delta):
        """
        A list of already defined intervals is treated
        """
        if axisName not in self.axis_names: raise Exception(" checking the axis name  to be in setdAxis")
        axisIndex = self.getAxisIndex(axisName)
        coordinates = [0.0]
        for i in range (0, len (delta), 1):
            coordinates.append (coordinates[i] + delta[i])
        self.coords[axisIndex] = numpy.array(coordinates, numpy.float)
        self.nb_of_intervals[axisIndex] = len(delta)

    def buildZoneMap(self):
        map = numpy.zeros(tuple(self.nb_of_intervals)) - 1
        for zone in self.zones:
            zone.setMap(map, self.getZoneIndex(zone.getName()))
        self.map = map
        self.flags['ZoneMap'] = 1

    def getZoneMap(self):
        if self.flags['ZoneMap'] == 0:
            self.buildZoneMap()
        ordered_map = numpy.transpose(self.map)
        # ravel flatens the array
        return  numpy.ravel(ordered_map)

    def getZoneSupport(self, zone_name):
        map = self.getZoneMap()
        index = self.getZoneIndex(zone_name)
        equals = numpy.equal(map, index)
        return numpy.nonzero(equals).tolist()


class CartesianMesh1D(CartesianMesh):
    dims = 1
    def __init__(self, name, axis='X'):
        if axis not in ['X', 'Y', 'Z', 'R']: raise Exception(" check the axis denomination")
        if axis in ['X', 'Y', 'Z']:
            self.coord_system = 'Cartesian'
            self.axis_names = ['X']
            self.element_type = 'Seg2'
        elif axis == 'R':
            self.coord_system = 'Cylindrical'
            self.axis_names = ['R']
            self.element_type = 'Other'
        CartesianMesh.__init__(self, name)

    def getCell(self, cell_nb):
        if cell_nb > self.getNbCells():
            raise Exception("Cell number out of range")
        return CartesianCell1D(self, cell_nb, self.toCellIndex(cell_nb))

    def getNbNodes(self):
        return self.nb_of_intervals[0] + 1

    def getNbCells(self):
        return self.nb_of_intervals[0]

    def getNbSides(self):
        return self.nb_of_intervals[0] + 1

    def makeZone(self, name, index_min, index_max):
        return CartesianZone1D(name, index_min, index_max)

    def toCellIndex(self, cell_nb):
        i = cell_nb
        return Index1D(i)

    def toCellNb(self, cell_index):
        nx = self.nb_of_intervals[0]
        if cell_index.outOfBounds(0, nx):
            return None
        i = cell_index.getValues()
        return i

    def toNodeNb(self, node_index):
        i = node_index.getValues()
        return i

    def toNodeIndex(self, node_nb):
        return Index1D(node_nb)

class CartesianMesh2D(CartesianMesh):
    dims = 2
    def __init__(self, name, axis='XY'):
        if axis not in ['XY', 'XZ', 'YZ', 'RZ', 'RTeta']: raise Exception(" check the axis denomination")
        if axis in ['XY', 'XZ', 'YZ']:
            self.coord_system = 'Cartesian'
            self.axis_names = ['X', 'Y']
            self.element_type = 'Quad4'
        elif axis == 'RZ' or axis == 'RTheta':
            self.coord_system = 'Cylindrical'
            self.element_type = 'Other'
            if axis == 'RZ':
                self.axis_names = ['R', 'Z']
            else:
                self.axis_names = ['R', 'Theta']
        CartesianMesh.__init__(self, name)

    def getCell(self, cell_nb):
        if cell_nb > self.getNbCells():
            raise Exception("Cell number out of range")
        return CartesianCell2D(self, cell_nb, self.toCellIndex(cell_nb))

    def getNbNodes(self):
        nx = self.nb_of_intervals[0] + 1
        ny = self.nb_of_intervals[1] + 1
        return nx * ny

    def getNbCells(self):
        nx = self.nb_of_intervals[0]
        ny = self.nb_of_intervals[1]
        return nx * ny

    def getNbSides(self):
        nx = self.nb_of_intervals[0]
        ny = self.nb_of_intervals[1]
        return (nx + 1) * ny + nx * (ny + 1)

    def getEastSideNb(self, i, j):
        """The algorithm is based on the number of sides added per cell:

        3 2 2 ... 2
        ...........
        3 2 2 ... 2
        4 3 3 ... 3
        """
        if j == 0:
            if i == 0:
                return 1
            else:
                return i * 3 + 2
        elif j == 1:
            nx = self.nb_of_intervals[0]
            if i == 0:
                return nx * 3 + 1
            else:
                return nx * 3 + i * 2 + 2
        else:
            nx = self.nb_of_intervals[0]
            if i == 0:
                return (j * nx + i) * 2 + nx + j 
            else:
                return (j * nx + i) * 2 + nx + j + 1

    def makeZone(self, name, index_min, index_max):
        return CartesianZone2D(name, index_min, index_max)

    def toCellIndex(self, cell_nb):
        nx = self.nb_of_intervals[0] 
        j, i = divmod(cell_nb, nx)
        return Index2D(i,j)


    def toCellNb(self, cell_index):
        nx = self.nb_of_intervals[0]
        ny = self.nb_of_intervals[1]
        if cell_index.outOfBounds((0,0), (nx,ny)):
            return None
        i, j = cell_index.getValues()
        return j * nx + i

    def toNodeNb(self, node_index):
        i, j = node_index.getValues()
        if j > 1:  # 'regular' line
            nx = self.nb_of_intervals[0]
            nb = j * (nx + 1) 
            return nb + i
        elif j == 0:  # first line
            if i < 2:
                return i
            else:
                return 2 * i
        else:  # j == 1, i.e. second line
            if i == 0:
                return 3
            elif i == 1:
                return 2
            else:
                return 2 * i + 1

    def toNodeIndex(self, node_nb):
        raise NotYetImplemented


class CartesianMesh3D(CartesianMesh):
    dims = 3
    def __init__(self, name, axis='XYZ'):
        if axis not in ['XYZ', 'RTetaZ']: raise Exception(" check the axis denomination")
        if axis == 'XYZ':
            self.coord_system = 'Cartesian'
            self.axis_names = ['X', 'Y', 'Z']
            self.element_type = 'Hexa6'
        elif axis == 'RThetaZ':
            self.coord_system = 'Cylindrical'
            self.element_type = 'Other'
            self.axis_names = ['R', 'Theta', 'Z']
        CartesianMesh.__init__(self, name)

    def getCell(self, cell_nb):
        if cell_nb > self.getNbCells():
            raise Exception("Cell number out of range")
        return CartesianCell3D(self, cell_nb, self.toCellIndex(cell_nb))

    def getNbNodes(self):
        nx = self.nb_of_intervals[0] + 1
        ny = self.nb_of_intervals[1] + 1
        nz = self.nb_of_intervals[2] + 1
        return nx * ny * nz

    def getNbCells(self):
        nx = self.nb_of_intervals[0]
        ny = self.nb_of_intervals[1]
        nz = self.nb_of_intervals[2]
        return nx * ny * nz

    def getNbSides(self):
        nx = self.nb_of_intervals[0]
        ny = self.nb_of_intervals[1]
        nz = self.nb_of_intervals[2]
        return (nx + 1) * ny * nz + nx * (ny + 1) * nz + nx * ny * (nz + 1)

    def makeZone(self, name, index_min, index_max):
        return CartesianZone3D(name, index_min, index_max)

    def toCellIndex(self, cell_nb):
        nx = self.nb_of_intervals[0] 
        ny = self.nb_of_intervals[1]
        k, rest = divmod(cell_nb, (nx * ny))
        j, i = divmod(rest, nx)
        return Index3D(i,j,k)

    def toCellNb(self, cell_index):
        nx = self.nb_of_intervals[0]
        ny = self.nb_of_intervals[1]
        nz = self.nb_of_intervals[2]
        if cell_index.outOfBounds((0,0,0), (nx,ny,nz)):
            return None
        i, j, k = cell_index.getValues()
        return k * nx * ny + j * nx + i

class CartesianField:

    def __init__(self, name,support,components_names,type='Float',flags=None):
        #flag is a dictionnary with 3 keys: time, order and iteration
        self.name = name
        self.support=support
        nb_compos = len(components_names)
        self.components = components_names
        self.type = type
        if type not in ['Float','Int'] :
            raise Warning('Type unsupport by cartesian Fields')
        self.field={}
        if flags:
            self.iteration=flags[iteration]
            self.order=flags[order]
            self.time=flags[time]

    def getSupport(self):
        return self.support

    def getComponentsNames(self):
        return self.components

    def getNbComponents(self):
        return len(self.components)

    def getValues(self):
        pass

    def getTime(self) :
        return self.time

    def getIteration(self) :
        return self.iteration

    def setElementValues(self, element, values):
        """All components for one element."""
        pass

    def setValues(self, values):
        """All field values at once."""
        nb_expected_values=self.support.getNbCells()
        indice_component=0
        for value in values :
            component_name=self.components[indice_component]
            nb_values=len(value)  
            if nb_values!=nb_expected_values:
                print(nb_values,nb_expected_values)
                raise Warning('Invalid number of values in cartesian field read')
            if self.type=='Float' :
                self.field[component_name]=numpy.array(value, numpy.float)
            else :
                self.field[component_name]=numpy.array(value, numpy.int)
            indice_component=indice_component+1

    def setValue(self, element, component, value):
        """One element, one component."""
        pass

    def setComponentValues(self, component, values):
        """One component for all elements."""
        if component not in self.components:
            raise Warning('not in component list')
        nb_values=len(values)
        nb_expected_values=self.support.getNbCells()
        if nb_values!=nb_expected_values:
            raise Warning('Invalid number of values in cartesian field read: expected number=%d, number found=%d'%(nb_expected_values,nb_values))
        if self.type=='Float' :
            self.field[component]=numpy.array(values, numpy.float)
        else :
            self.field[component]=numpy.array(values, numpy.int)


    def getComponentValues(self, component):
        """One component for all elements."""
        if component not in self.components:
            raise Warning('not in component list')
        if component in self.field:
            return self.field[component]
        else :
            raise Warning('No field for this component')


class CartesianSupport:
    def __init__(self,name):
        pass

