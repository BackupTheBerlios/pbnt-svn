from numarray import *
import GraphUtilities


class Potential:
    """ Potentials are very similar to a conditional distribution in that they specify the probability over a set of nodes.
    The difference is that potentials are not thought of as being centered on the value a one node given other nodes.  
    Therefore, a conditional distribution could be thought of as a special case of a potential.
    """
    
    def __init__(self, nodes):
        self.dims = array([node.size() for node in nodes])
        self.table = ones(self.dims, type= Float32)
        self.nDims = len(self.dims)
        
    def set_value( self, index, value, axes=-1 ):
        if axes == -1:
            axes = range(self.nDims) 
        indexStr = GraphUtilities.generateArrayStrIndex(index, axes, self.nDims)
        exec 'self.table' + indexStr + ' = ' + repr(value)
    
    def get_value(self, index, axes=-1):
        if axes == -1:
            axes = range(self.nDims)
        indexStr = GraphUtilities.generateArrayStrIndex(index, axes, self.nDims)
        values = eval('self.table' + indexStr)
        return values
    
    def normalize(self):
        # Make sure that the last dimension adds to 1 along all other values.
        if self.nDims > 1:
            seq = SequenceGenerator(self.dims[:-1])
            for s in seq:
                cArray = self.getValue(s, axes=self.dims[:-1])
                c = cArray.sum()
                if not c == 0:
                    cArray /= c
                    self.setValue(s, cArray, axes = self.dims[:-1])
        else:
            c = self.table.sum()
            if not c == 0:
                self.table /= c
    
    # OPERATORS
    def __getitem__(self, index, axes=-1):
        return self.get_value(index, axes)
    
    def __setitem__(self, index, value, axes=-1):
        self.set_value(index, value, axes)
        
    
class DiscreteDistribution:
    """ The basic class for a distribution, it defines a simple distribution over a set number of 
    values.  This is not to be confused with ConditionalDiscreteDistribution, which is a discrete 
    distribution conditioned on other discrete distributions.
    """
    
    def __init__(self, numValues):
        self.table = zeros([numValues], type=Float32)
        self.size = numValues
        
    def set_value(self, value, probability):
        self.table[value] = probability
    
    def normalize(self):
        self.table /= self.table.sum()
        
        
class ConditionalDiscreteDistribution(Potential):
    """ This is very similar to a potential, except that ConditionalDistributions are focused on a single variable and its
    value given the value of other variables.
    """

    def __init__(self, nodes):
        Potential.__init__(self, nodes)
        self.size = self.dims[-1]    
     