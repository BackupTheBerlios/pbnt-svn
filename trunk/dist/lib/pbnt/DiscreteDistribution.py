from numarray import *
from SequenceGenerator import *
import GraphUtilities

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
        
        
class ConditionalDiscreteDistribution:
#to do listforthis class
#add different constructors
#1.give fullCPT
#2 give it for specific parents but
# randomfor others

    def __init__(self, CPT):
        self.CPT = CPT
        self.dims = shape(CPT)
        self.size = self.dims[-1]
        self.nDims = len(self.dims)
    
    def setValue( self, indices, value, axes=-1 ):
        if axes == -1:
            #if self.nDims == 1:
                #axes = 0
            #else:
                #axes = range( self.nDims )
            axes = range( self.nDims )
        #elif isinstance( indices, ArrayType ): 
            ##because of a bug in numarray have to reorder indices and axis
            ##should be able to do this with some sort of in place sort, but not sure how
            #oldIndices = indices.copy()
            #for i in range( self.nDims ):
                #indices[i] = oldIndices[axes==i]
        ###if value is an array of values, then we need to flatten, but if just a number
        ##then this will raise an exception
        ##put( self.CPT, indices, value )
        
        #try:
            #put( self.CPT, indices, value.flat, axis=axes )
        #except:
            #put( self.CPT, indices, value, axis=axes )
        
        indexStr = GraphUtilities.generateArrayStrIndex( indices, axes, self.nDims )
        #flatIndex = GraphUtilities.generateFlatIndex( indices, axes, self.nDims, self.dims )
        exec 'self.CPT' + indexStr + ' = ' + repr( value )
    
    def getValue( self, varAndParentValsArray, axes=-1 ):
        if axes == -1:
            axes = range(len(varAndParentValsArray))
        indexStr = GraphUtilities.generateArrayStrIndex(varAndParentValsArray, axes, self.nDims)
        values = eval('self.CPT' + indexStr)
        return values
        #return take(self.CPT, varAndParentValsArray, axis=axes)
        
    #def setMultipleValues( self, indices, axes, values ):
        ##have to do this special because the indices might be discontiguous
        #mask = ones( [self.nDims], type=Bool )
        #mask[axes] = 0
        #axesToIterateOver = array( range( self.nDims )  )[mask]
        #dimsToIterateOver = array(self.dims)[mask]
        #sequence = SequenceGenerator( dimsToIterateOver )
        #for seq in sequence:
            #put( self.CPT, concatenate(( seq, indices )), take( values, seq, axis=range(len( seq )) ), axis=concatenate(( axesToIterateOver, axes )).tolist())
        
    #def setMultipleIndex( self, indices, axes, value ):
        ##exact same as above, but only put one value in as opposed to a set of values
        ##have to do this special because the indices might be discontiguous
        #mask = ones( [self.nDims], type=Bool )
        #mask[axes] = 0
        #axesToIterateOver = array( range( self.nDims )  )[mask]
        #dimsToIterateOver = array(self.dims)[mask]
        #sequence = SequenceGenerator( dimsToIterateOver )
        #for seq in sequence:
            #put( self.CPT, concatenate(( seq, indices )), value, axis=concatenate(( axesToIterateOver, axes )).tolist())
        
        
    
    def normalise(self):
        if self.nDims > 1:
            seq = SequenceGenerator(self.dims[:-1])
            for s in seq:
                cArray = self.getValue(s, axes=self.dims[:-1])
                c = cArray.sum()
                if not c == 0:
                    cArray /= c
                    self.setValue(s, cArray, axes = self.dims[:-1])
        else:
            c = self.CPT.sum()
            if not c == 0:
                self.CPT /= c
    
            
    def ns(self):
        return self.ns
    
    
            