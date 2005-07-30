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
		#if value is an array of values, then we need to flatten, but if just a number
		#then this will raise an exception
		try:
			put( self.CPT, indices, value.flat, axis=axes )
		except:
			put( self.CPT, indices, value, axis=axes )
	
	def getValue( self, varAndParentValsArray, axes=-1 ):
		if axes == -1:
			axes = range( self.nDims )
		return take(self.CPT, varAndParentValsArray, axis=axes)
		
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
		self.CPT[where(self.CPT == 0)] = 1
		c = self.CPT.sum()
		self.CPT = self.CPT/c
	
	def ns(self):
		return self.ns
	
	
		    