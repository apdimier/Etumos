"""
 To define Points and Coordinates.
"""

import bisect # Bisection algorithms.
from generictools import Generic
import math
import types

class GenericPoint(Generic):
    """
    The class used to define points in 1D, 2D and 3D.
    """
    def getDimension(self):
        return self.dimension

    def isClose(self, point, epsilon=0.001):
        return self.distance(point) < epsilon

class Point1D(GenericPoint):
    """
    Points in one space dimension
    """
    dimension = 1
    def __init__(self, x):
        self.x = x

    def distance(self, point):
        return abs(self.x - point.x)

    def getCoordinates(self):
        return self.x

    def __cmp__(self, point):
        return cmp(self.x, point.x)

    def __eq__(self, point):
	return self.x == point.x

    def __ne__(self, point):
	return self.x != point.x

class Point2D(GenericPoint):
    """
    Points in 2 space dimensions
    """
    dimension = 2
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, point):
        dist =  (self.x - point.x) ** 2 + \
                (self.y - point.y) ** 2
        return math.sqrt(dist)

    def getCoordinates(self):
        return self.x, self.y

    def __cmp__(self, point):
        return cmp([self.y, self.x], [point.y, point.x])

    def __eq__(self, point):
	return self.x == point.x and self.y == point.y

    def __ne__(self, point):
	return self.x != point.x or self.y != point.y

class Point3D(GenericPoint):
    """
    Points in 3 space dimensions
    """
    dimension = 3
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def distance(self, point):
        dist =  (self.x - point.x) ** 2 + \
                (self.y - point.y) ** 2 + \
                (self.z - point.z) ** 2
        return math.sqrt(dist)

    def getCoordinates(self):
        return self.x, self.y, self.z

    def __cmp__(self, point):
        return cmp([self.z, self.y, self.x], [point.z, point.y, point.x])

    def __eq__(self, point):
	return self.x == point.x and self.y == point.y and self.z == point.z

    def __ne__(self, point):
	return self.x != point.x or self.y != point.y or self.z != point.z

def Point(*coords):
    """
    Return an instance of Point1D, Point2D or Point3D,
    based on the number of coordinates (x,y,z) given.
    """
    if len(coords) == 1:
	return Point1D(*coords)
    elif len(coords) == 2:
	return Point2D(*coords)
    else:
	return Point3D(*coords)

def computeCenter1D(pointList):
    """
    Computes the center and returns a 1D point
    """
    center = 0.
    for point in pointList:
        center += point.getCoordinates()
    center = center / float(len(pointList))
    return Point1D(center)
    
def computeCenter2D(pointList):
    """
    computes the center and returns a 2D point
    """
    x = 0.
    y = 0.
    for point in pointList:
        x1, y1 = point.getCoordinates()
        x += x1; y += y1
    den = 1. / len(pointList)
    x = x * den
    y = y * den
    return Point2D(x, y)
    
def computeCenter3D(points):
    """
    computes the center and returns a 3D point
    """
    x = 0.
    y = 0. 
    z = 0.
    for point in pointList:
        x1, y1, z1 = point.getCoordinates()
        x += x1
        y += y1
        z += z1
    den = 1./len(pointList)
    x = x * den; y = y * den; z = z * den
    return Point3D(x, y, z)

def computeCenter(pointList):
    dimension = pointList[0].getDimension()
    if dimension == 1:
        return computeCenter1D(pointList)
    elif dimension == 2:
        return computeCenter2D(pointList)
    else:
        return computeCenter3D(pointList)
