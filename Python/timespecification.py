"""TimeSpecification"""

import types

from species import Species

def floatRange(start, stop, step, epsilon=0.001):
    """Like range, but for floats.

    The last step is adjusted to fall into stop, all the while avoiding a step
    smaller than epsilon*step
    """
    eps = epsilon * step
    res = []
    if start + eps > stop:
        return res
    last = start
    while last + eps <= stop:
        res.append(last)
        last += step
    res.append(stop)
    return res

def extendFloatRange(float_range, stop, step, epsilon=0.001):
    """It extend an existing float range."""
    extension = floatRange(float_range[-1], stop, step, epsilon)
    float_range.extend(extension[1:])
    return float_range
def _count_args(*args):
    iargs = 0
    for arg in args:
        if arg:
            iargs += 1
    return iargs

def verifyNbArguments(nb, *args):
    nb_args = _count_args(*args)
    if nb_args < nb:
        raise Warning, "At least " +`nb`+ "  arguments must be provided"
    if nb_args > nb:
        raise Warning, "At most " +`nb`+ " arguments can be provided"

class TimeSpecification:
    """
    Several ways to specify the output time :
    
        by frequency, by period or by a times list
    """
    
    def __init__(self, frequency=None, period=None, times=None, unit='s'):
        """TimeSpecification initialisation with (ALL OPTIONAL):
        
        - a frequency (integer)
        - a period (a float)
        - a times (list of float)
        - a unit (default value is second)
        """

        self._setArgs(frequency, period, times, unit)
        return

    def _setArgs(self, frequency, period, times, unit):
        verifyNbArguments(1, frequency, period, times)
        if frequency:
            self.setFrequency(frequency)
        elif period:
            self.setPeriod(period)
        elif times:
            self.setTimes(times)
        else:
            raise RuntimeError
        self.setUnit(unit)
        return
    
    def setFrequency(self, frequency):
        self.frequency = None
        if frequency:
            self.frequency = int(frequency)
            self.specification = 'frequency'
        return

    def setPeriod(self, period):
        self.period = float(period)
        self.specification = 'period'
        return

    def setTimes(self, times):
        self.specification = 'times'
        self.times = TimeSequence(times)
        return
        
    def setUnit(self, unit):
        if self.getFrequency():
            self.unit = None
        else:
            if unit not in ['s','year']: raise Exception, " check the time specification unit"
            self.unit = unit
        return
        
    def getSpecification(self):
        """It can be 'frequency', 'period' or 'times'"""
        return self.specification
    
    def getFrequency(self):
        try:
            return self.frequency
        except AttributeError:
            return None
    
    def getPeriod(self):
        try:
            return self.period
        except AttributeError:
            return None
    
    def getTimes(self):
        try:
            return self.times
        except AttributeError:
            return None
    
    def getUnit(self):
        """get TimeSpecification unit"""
        return self.unit
    
    pass

class MyTimeSpecification(TimeSpecification):

    def setUnit(self, unit):
        if unit not in ['s','year']: raise Exception, " check the time specification unit"
        self.unit = unit
        return

    def getUnit(self):
        return self.unit

class PeriodTimeSpecs(MyTimeSpecification):
    def __init__(self, period, unit='s'):
        self.setPeriod(period)
        self.setUnit(unit)
        return

    def setPeriod(self, period):
        self.period = float(period)
        return

    def getPeriod(self):
        return self.period

class FrequencyTimeSpecs(MyTimeSpecification):
    def __init__(self, frequency=1):
        self.setFrequency(frequency)
        return

    def setFrequency(self, frequency):
        self.frequency = int(frequency)
        return

    def getFrequency(self):
        return self.frequency

class SequenceTimeSpecs(MyTimeSpecification):
    def __init__(self, sequence, unit='s'):
        self.setSequence(sequence)
        self.setUnit(unit)
        return

    def setSequence(self, sequence):
        self.sequence = TimeSequence(sequence)
        return

    def getSequence(self):
        return self.sequence


def _float_list(list):
    new = []
    for item in list:
        new.append(float(item))
    return new

def _verify_order(list):
    new = list[:]
    new.sort()
    if new != list:
        raise ValueError("Time list is not ordered")
    return

def _floatRange(start, stop, step, epsilon=0.001):
    """Like range, but for floats.

    The last step is adjusted to fall into stop, all the while avoiding a step
    smaller than epsilon*step
    """
    eps = epsilon * step
    res = []
    if start + eps > stop:
        return res
    last = start
    while last + eps <= stop:
        res.append(last)
        last += step
    res.append(stop)
    return res

def _extendFloatRange(float_range, stop, step, epsilon=0.001):
    """It extend an existing float range."""
    extension = _floatRange(float_range[-1], stop, step, epsilon)
    float_range.extend(extension[1:])
    return float_range

class TimeSequence(list):
    """A list of times.

    Verifications:
    - all items are convertible to floats
    - items are in non-decreasing order.
    """
    def __init__(self, a_list, unit='s'):
        self.unit = unit
        new = _float_list(a_list)
        _verify_order(new)
        list.__init__(self, new)
        return

    def insert(self, time):
        if time not in self:
            self.append(time)
            self.sort()
        return

    def merge(self, other):
        list = self + other
        list.sort()
        return TimeSequence(list)

    def extract(self, time_specification):
        ts_class = time_specification.__class__
        if ts_class == FrequencyTimeSpecs:
            return self.extractFromFrequency(time_specification.getFrequency())
        elif ts_class == PeriodTimeSpecs:
            return self.extractFromPeriod(time_specification.getPeriod())
        elif ts_class == SequenceTimeSpecs:
            return time_specification.getSequence()

    def extractFromPeriod(self, period):
        times = _floatRange(self[0], self[-1], period)
        return TimeSequence(times)


    def extractFromFrequency(self, jump):
        times = []
        nb = len(self)
        n_out = nb / jump
        for i in range(n_out):
            times.append(self[i*jump])
        if nb%jump != 0: # always include last time
            times.append(self[-1])
        return TimeSequence(times)
            
