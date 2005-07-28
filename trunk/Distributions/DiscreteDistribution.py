from numarray import *
from SequenceGenerator import *

class DiscreteDistribution:
#to do listforthis class
#add different constructors
#1.give fullCPT
#2 give it for specific parents but
# randomfor others

	def __init__(self, CPT, ns):
		self.CPT = CPT
		self.ns = ns
		self.dims = shape( CPT )
		self.nDims = len( self.dims )
	
	def setValue( self, indices, value, axes=-1 ):
		if axes == -1:
			if self.nDims == 1:
				axes = 0
			else:
				axes = range( self.nDims )
		put( self.CPT, indices, value, axis=axes )
	
	def getValue( self, varAndParentValsArray, axes=-1 ):
		if axes == -1:
			axes = range( self.nDims )
		return take(self.CPT, varAndParentValsArray, axis=axes)
		
	def setMultipleValues( self, indices, axes, values ):
		#have to do this special because the indices might be discontiguous
		mask = ones( [self.nDims], type=Bool )
		mask[axes] = 0
		axesToIterateOver = array( range( self.nDims )  )[mask]
		dimsToIterateOver = array(self.dims)[mask]
		sequence = SequenceGenerator( dimsToIterateOver )
		for seq in sequence:
			put( self.CPT, concatenate(( seq, indices )), take( values, seq, axis=range(len( seq )) ), axis=concatenate(( axesToIterateOver, axes )).tolist())
		
			
		
	
	def normalise(self):
		self.CPT[where(self.CPT == 0)] = 1
		c = sum(reshape(self.CPT,(size(self.CPT),)))
		self.CPT = self.CPT/c
	
	def ns(self):
		return self.ns
	
	
		    