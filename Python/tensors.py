# -*- coding: utf-8 -*-
"""
Tensors Module
"""

from generictools import isInstance

from wrappertools import verifyEqualFloats
import types
#from utilities import *
from vector import V as Vector

def _verifyIndices(i, j):
    """Internal method to verifying whether i and j are in range of 0 and 2."""
    if i > 2 or i < 0 or j > 2 or j < 0:
	raise "Tensor indices must be in range of 0 and 2."



            
class Tensor:
    """Global class for Anisotropic and isotropic tensor.
    Value attribute is an array of tensor's dimension"""

    def __init__(self):
        """Initialization will be executed for 2D and 3D anisotropic tensors, here nothing is done."""
	self.value = None

    def getValue(self, i, j):
        """Returns the value[i][j] of the tensor."""
	_verifyIndices(i, j)
	return self._get(i,j)

    def tolist(self):
        """Returns a list of tensor values."""
        return [self.value]

    def isIsotropic(self):
	return 0

    def _get(self, i, j):
        """Returns the value[i][j]"""
	if j > i:
	    t = i; i = j; j = t
	return self.value[i][j]

    def TensorMalVector(self,V):
        """
        returns the vector product of the tensor by the vector V.
	"""
        dim = V.getDims()
        if self.getDimension() != dim:
            raise Exception,"Vector and Tensor have not the same dimension"
        vector = []
        for i in range(dim):
            value = 0
            for j in range(dim):
                value = value + self._get(i,j)*V.comps[j]
            vector.append(value)
        return Vector(list(vector))

    def VectorMalTensor(self,V):
        """Multiplication of the vector V by the tensor self.
	Returns a list result of this operation."""
        dim = V.getDims()
        if self.getDimension() != dim:
            raise Exception,"Vector and Tensor have not the same dimension"
        val = []
        for i in range(dim):
            value = 0
            for j in range(dim):
                value = value + self._get(i,j)*V.comps[j]
            val.append(value)
        return val
        

    def VectorTensorVector(self,Va,Vb):
        """Multiplication:
	Va * self * Vb, returns a scalar value."""
        if isinstance(Va,V) and isinstance(Vb,V):
            if Va.__len__ != Vb.__len__:
                raise " dimension error on vectors "
        else:
            raise " Va, Vb type mismatch "
                
        dim = Va.getDims()
        if self.getDimension() != dim:
            raise Exception, "Vector and Tensor have not the same dimension"
        la = Va.getValues()
        vectb = self.TensorMalVector(Vb)
        som = 0
        for i in range(len(la)):
            som = som + la[i] * vectb.comps[i]
            pass
        return som


class Tensor2D(Tensor):
    """2D Anisotropic tensor
    could be initialized by :
    - two scalars (main directions are x and y)
    - 3 scalars
    - two scalars and two vectors (two directions). The constructor calcultates the coefficients to translate the tensor into the main direction x, y and z"""

    def __init__(self,alpha,beta, V1 = None, V2= None):
        """Constructor of the class."""
        verifyType(alpha,types.FloatType)
        verifyType(beta,types.FloatType)
        if (not V1 and (not V2)):
            # case of two scalars
            self.value = [[alpha],[0., beta]]
            pass
        elif ((V1 and (not V2)) or ((not V1) and V2)):
            #case of 3 scalars
            if V1:
                verifyType(V1,types.FloatType)
                self.value = [[alpha],[V1, beta]]
                pass
            else:
                verifyType(V2,types.FloatType)
                self.value = [[alpha],[V2, beta]]
                pass
            pass
        elif ((isInstance(V1,Vector)) and
              (isInstance(V2,Vector))):
             #case of 4 scalars
             if V1.__len__ != V2.__len__:
                 raise Exception, " vectors defing a 2D tensor have not the same dimension"
             
             V1.verifyUnitary()
             V2.verifyUnitary()
             verifyEqualFloats(V1.cross(V2).getValues()[2],1.)
             t = Tensor2D(alpha,beta)
             
             Kxx = t.VectorTensorVector(V1,V1)
             Kyy = t.VectorTensorVector(V2,V2)
             Kxy = t.VectorTensorVector(V1,V2)
             self.value = [[Kxx],[Kxy, Kyy]]
             pass
        else:
             raise Exception, " defining a 2D tensor, you have to enter scalars or vectors"
        return
     
    def getNbComponents(self):
        """Gets the number of tensor components (3)."""
        return 3
    
    def getDimension(self):
        """Gets tensor's dimension (2)."""
        return 2

    def isDiagonal(self):
        """Returns True if the given tensor is diagonal."""
        return (self.value[1,2] == 0)

    def tolist(self):
        """Returns a list of tensor values."""
        return [self.value[0][0],self.value[1][0],self.value[1][1]]
    
    def amult(self,scalar):
        """Multiplication of the tensor by the given scalar value.
	Returns a new tensor = scalar * self."""
        alpha = scalar*self.value[0][0]
        beta = scalar*self.value[1][1]
        V1 = scalar*self.value[1][0]
        return Tensor2D(alpha,beta,V1)

    def __neg__(self):
        """Returns a new tensor = - self."""
        t= self.amult(-1.)
        return t
    
    def __add__(self,other):
        """Addition of two given tensors.
	Returns a new tensor = self + other."""
        alpha = self.value[0][0] + other.value[0][0]
        beta = self.value[1][1] + other.value[1][1]
        V1 = self.value[1][0] + other.value[1][0]
        return Tensor2D(alpha,beta,V1)

    def __sub__(self,other):
        """Substraction of the given tensors.
	Returns a new tensor = self - other."""
        alpha = self.value[0][0] - other.value[0][0]
        beta = self.value[1][1] - other.value[1][1]
        V1 = self.value[1][0] - other.value[1][0]
        return Tensor2D(alpha,beta,V1)        
    
class Tensor3D(Tensor):
    """3D Anisotropic tensor
       could be initialized by :
       - 3 scalars (main directions are x, y and z)
       - 6 scalars
       - 3 scalars and 3 vectors (three directions). The constructor calcultates the coefficients to translate the tensor into the main direction x, y and z"""

    def __init__(self,alpha,beta,gamma, V1 = None, V2= None, V3 = None):
        """Constructor of the class."""

        verifyType(alpha,types.FloatType)
        
        verifyType(beta,types.FloatType)
        
        verifyType(gamma,types.FloatType)
        
        if (not V1 and (not V2) and (not V3)):
#
#                                                                                                               Diagonal terms
#
            self.value = [[alpha],[0., beta], [0.,0.,gamma]]
        elif ((V1 and (not V2) and (not V3)) or
#
#                                                                                                               vector terms
#
            (V1 and V2 and (not V3)) or
            ((not V1) and V2 and V3) or
            ((not V1) and (not V2) and V3) or
            (V1 and (not V2) and V3) or
            ((not V1) and V2 and (not V3))):
            raise Exception, "to define a tensor you give 3 diagonal terms or 6 for an isotropic one"
        if V1 : 
            if ((type(V1) is types.FloatType) and
                (type(V2) is types.FloatType) and
                (type(V3) is types.FloatType)):
                #case of 6 scalars
                self.value = [[alpha],[V1, beta], [V2,V3,gamma]]
            elif ((isInstance(V1,Vector)) and
                  (isInstance(V2,Vector)) and
                  (isInstance(V3,Vector))):
                # case of 3 scalars and 3 vectors
                if V1.__len != V2.__len:
                    raise " dimensionality error in Tensor3D "
                if V2.__len != V3.__len:
                    raise " dimensionality error in Tensor3D "
                
                V1.verifyUnitary()
                V2.verifyUnitary()
                V3.verifyUnitary()
                V3.verifyEquals(V1.cross(V2))
                t = Tensor3D(alpha,beta, gamma)
                     
                Kxx = t.VectorTensorVector(V1,V1)
                Kyy = t.VectorTensorVector(V2,V2)
                Kxy = t.VectorTensorVector(V1,V2)
                Kxz = t.VectorTensorVector(V1,V3)
                Kyz = t.VectorTensorVector(V2, V3)
                Kzz = t.VectorTensorVector(V3,V3)
                self.value = [[Kxx],[Kxy, Kyy], [Kxz,Kyz, Kzz] ]
            else:
                raise Exception, " defining a 3D tensor, you have to enter scalars or vectors"


    def getNbComponents(self):
        """Gets the number of tensor components (6)."""
        return 6

    def getDimension(self):
        """Gets tensor's dimension (3)."""
        return 3
    
    def isDiagonal(self):
        """Returns True if the given tensor is diagonal."""
        return ((self._get(0,1) == 0) and
                (self._get(0,2) == 0) and
                (self._get(1,2) == 0))

    def tolist(self):
        """Returns a list of tensor values."""
        return [self.value[0][0],self.value[1][0],self.value[1][1],self.value[2][0],self.value[2][1],self.value[2][2]]

    def amult(self,scalar):
        """Multiplication of the tensor by the given scalar value.
	Returns a new tensor = scalar * self"""
        alpha = scalar*self.value[0][0]
        beta = scalar*self.value[1][1]
        gamma = scalar*self.value[2][2]
        V1 = scalar*self.value[1][0]
        V2 = scalar*self.value[2][0]
        V3 = scalar*self.value[2][1]
        return Tensor3D(alpha,beta,gamma,V1, V2,V3)

    def __neg__(self):
        """Returns a new tensor = - self"""
        t= self.amult(-1.)
        return t

    def __add__(self,other):
        """Addition of two given tensors.
	Returns a new tensor = self + other"""
        alpha = self.value[0][0] + other.value[0][0]
        beta = self.value[1][1] + other.value[1][1]
        gamma = self.value[2][2] + other.value[2][2]
        V1 = self.value[1][0] + other.value[1][0]
        V2 = self.value[2][0] + other.value[2][0]
        V3 = self.value[2][1] + other.value[2][1]
        return Tensor3D(alpha,beta,gamma,V1,V2,V3)

    def __sub__(self,other):
        """Substraction of the given tensors.
	Returns a new tensor = self - other"""
        alpha = self.value[0][0] - other.value[0][0]
        beta = self.value[1][1] - other.value[1][1]
        gamma = self.value[2][2] - other.value[2][2]
        V1 = self.value[1][0] - other.value[1][0]
        V2 = self.value[2][0] - other.value[2][0]
        V3 = self.value[2][1] - other.value[2][1]
        return Tensor3D(alpha,beta,gamma,V1,V2,V3)


class IsotropicTensor(Tensor):
    """Isotropic Tensor : a diagonal tensor having the same value on its diagonal."""

    def __init__(self, value):
        """Constructor. The value is of float type."""
        try:
            type(value) is types.FloatType
        except:
            raise TypeError, " value is not of float type for the Isotropic Tensor Construction "  
	self.value = value

    def isIsotropic(self):
        """Returns True, because this tensor is isotropic."""
	return 1

    def getValues(self):
        """Returns the values of this tensor."""
        return self.value
    
    def tolist(self):
        """Returns a list of values of this tensor."""
        return [self.value]

    def _get(self, i, j):
        """Returns the value if i = j, else 0"""
	if i == j:
	    return self.value
	else:
	    return 0.

    def getNbComponents(self):
        """Gets the number of tensor components (1)"""
        return 1

    def isDiagonal(self):
        """Returns True because isotropic tensors are diagonal."""
        return 1

    def getDimension(self):
        """Gets tensor's dimension"""
        return len(self.tolist())

    def amult(self,scalar):
        """Multiplication of the tensor by the given scalar value.
	Returns a new tensor = scalar * self"""
        return IsotropicTensor(scalar*self.value)

    def __neg__(self):
        """Returns a new tensor = - self"""
        t= self.amult(-1.)
        return t
    
    def __add__(self,other):
        """Addition of two given tensors.
	Returns a new tensor = self + other"""
        return IsotropicTensor(self.value + other.value)
    
    def __sub__(self,other):
        """Substraction of the given tensors.
	Returns a new tensor = self - other"""
        return IsotropicTensor(self.value - other.value)


        
        
        
        
