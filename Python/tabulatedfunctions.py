"""A Hierarchy of functions

including:

- histograms
- linear functions
- splines?
"""


from __future__ import absolute_import
from bisect import bisect_left, bisect_right
from numpy import *
from numpy import float as Float
from six.moves import range

class TabulatedFunction:
    def __call__(self, x):
        raise NotImplementedError
    def derivative(self, x):
        raise NotImplementedError
    def integral(self, x0, x1):
        raise NotImplementedError


class ConstantFunction(TabulatedFunction):
    def __init__(self, value):
        self._value = value
    def __call__(self, x):
        return self._value
    def derivative(self, x):
        return 0.
    def integral(self, x0, x1):
        return max(0., self._value * (x1 - x0))


class PiecewisePolynomialFunction(TabulatedFunction):
    """A Piecewise Polynomial Function consists of:

    i. the integers 'k' and 'l', giving order and number of its pieces
    ii. the strictly increasing sequence [xi] of its breaks
    iii. the matrix (C_ij) of its right derivatives at the breaks:
         C_i,j = D^(j-1) f(xi_i)
         
    (Following C. de Boor, 'A Practical Guide to Splines')
    """
    def __init__(self, breaks, coeffs, outer_value=0., outer_right_value=None):
        outer_right_value = outer_right_value or 0.
        self._breaks = breaks
        self._coeffs = coeffs
        self._nb = len(breaks)
        self._k = coeffs.shape[0]
        self.outer_left = outer_value
        self._outer_right = outer_right_value
        return

    def __call__(self, xi):
        breaks = self._breaks
        if xi >= breaks[0] and xi < breaks[-1]:
            coeffs = self._coeffs
            i = bisect_right(breaks, xi) - 1
            j = self._k - 1
            h = xi - breaks[i]
            val = coeffs[j,i]
            while j > 0:
                j -= 1
                val = val * h + coeffs[j,i]
                pass
            return val
        elif xi < breaks[0]:
            return self.outer_left
        else:
            return self._outer_right
        
    def derivative(self, xi):
        breaks = self._breaks
        if xi >= breaks[0] and xi < breaks[-1]:
            coeffs = self._coeffs
            i = bisect_right(breaks, xi) - 1
            j = self._k - 1
            h = xi - breaks[i]
            d = j * coeffs[j,i]
            while j > 1:
                j -= 1
                d = d * h + j * coeffs[j,i]
                pass
            return d
        else:
            return 0.
        
    def integral(self, x0, x1):
        xs = self._breaks
        xa = max(x0, xs[0]); xb = min(x1, xs[-1])
        if xa >= xb:
            return 0.
        i0 = bisect_right(xs, xa) - 1
        i1 = bisect_left(xs, xb) - 1
        ave = self._average
        if i0 == i1: # it's just one interval
            sum = ave(i0) * (xb - xa)
        else: # it's several intervals
            sum = ave(i0) * (xs[i0+1] - xa)
            for i in range(i0+1,i1):
                sum += ave(i) * (xs[i+1] - xs[i])
                pass
            sum += ave(i1) * (xb - xs[i1])
            pass
        return sum

    def _average(self, i):
        coeffs = self._coeffs[:,i]
        h = self._breaks[i+1] - self._breaks[i]
        j = self._k - 1
        ave = coeffs[j] / (j+1)
        while j > 0:
            j -= 1
            ave = ave * h + coeffs[j] / (j+1)
            pass
        return ave
    

    
def makeHistogram(abscissas, ordinates):
    breaks = abscissas; values = ordinates
    nb = len(breaks); nv = len(values)
    if nb != nv + 1:
        raise ValueError
    breaks = array(breaks, Float)
    values = array(values, Float)
    coeffs = reshape(values, (1, nv))
    return PiecewisePolynomialFunction(breaks, coeffs)


def makePWLinearFunction(breaks, values):
    nb = len(breaks); nv = len(values)
    if nb != nv:
        raise ValueError
    _breaks = []; _coeffs = []
    for i in range(nb-1):
        if breaks[i+1] > breaks[i]:
            _breaks.append(breaks[i])
            der = float(values[i+1] - values[i]) / \
                  float(breaks[i+1] - breaks[i])
            _coeffs.append([values[i], der])
            pass
        else:
            pass
        pass
    _breaks.append(breaks[-1])
    coeffs = transpose(array(_coeffs))
    return PiecewisePolynomialFunction(_breaks, coeffs)

def makeConstantFunction(value, interval=None):
    if not interval:
        return ConstantFunction(float(value))
    else:
        breaks = array(list(interval), Float)
        values = array([value], Float)
        coeffs = reshape(values, (1, 1))
        return PiecewisePolynomialFunction(breaks, coeffs)


"""To do:

1. makeSpline()
"""
