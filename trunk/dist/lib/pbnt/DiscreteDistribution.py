from numarray import *
import GraphUtilities


class Potential:
    """ Potentials are very similar to a conditional distribution in that they specify the probability over a set of nodes.
    The difference is that potentials are not thought of as being centered on the value a one node given other nodes.  
    Therefore, a conditional distribution could be thought of as a special case of a potential.
    """
    
    def __init__(self, nodes=[], table=[]):
        assert((not nodes == []) or (not table == [])), "Atleast one input argument expected"       
        if table == []:
            self.dims = array([node.size() for node in nodes])
            self.table = ones(self.dims, type= Float32)
        else:
            self.table = table
            self.dims = shape(table)
        self.nDims = len(self.dims)
    
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
    
    def generateIndex(self, index, axis):
        # Takes in a list of indices and a list of corresponding axes.  Returns a list of slice objects that will access the 
        # equivalent position. Currently it only replaces missing axes with slice(None) objects, but eventually
        # I want to support more complex notions of i:j.
        s = [slice(None)] * self.nDims
        for i, val in enumerate(axis):
            s[val] = slice(index[i], index[i]+1)
        return s
    
    """ The following are the overloaded operators of this class. I want these distributions to be treated like tables, even
    if the underlying representation is not an array or table.  By overloading these, I can treat these classes as if they
    are just tables with a couple of extra methods specific to the distribution class I am dealing with.  There are two 
    advantages in particular.  First, if I need to improve performance, these classes could be implemented in C by inheriting
    from the numarray array object and adding the extra methods needed to deal with these objects as distributions.  Second, 
    if I decide to change the underlying array class from numarray to numeric or to something totally different, it wont affect
    anything else, because everything else with be abstracted away.  This is further guaranteed by generateIndex which
    generates an index for its class given which axes should be set and what the value of those axes are.
    """
    def __getitem__(self, index):
        return self.table[index]
    
    def __setitem__(self, index, value):
        self.table[index] = value
        
    
class DiscreteDistribution(Potential):
    """ The basic class for a distribution, it defines a simple distribution over a set number of 
    values.  This is not to be confused with ConditionalDiscreteDistribution, which is a discrete 
    distribution conditioned on other discrete distributions.
    """
    
    def __init__(self, numValues):
        self.table = zeros([numValues], type=Float32)
        self.size = numValues
        self.nDims = 1
        
    def set_value(self, value, probability):
        self.table[value] = probability
    
    def normalize(self):
        self.table /= self.table.sum()
        
        
class ConditionalDiscreteDistribution(Potential):
    """ This is very similar to a potential, except that ConditionalDiscreteDistributions are focused 
    on a single variable and its value conditioned on other variables.
    """

    def __init__(self, nodes=[], table=[]):
        Potential.__init__(self, nodes)
        self.size = self.dims[-1]    
     