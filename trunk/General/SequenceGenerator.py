from numarray import *

class SequenceGenerator:
	
	def __init__( self, iterObjs ):
		self.stop = array(iterObjs) - 1
		#assuming here that the start of each dimension is zero
		self.value = zeros(size( iterObjs ))
		self.value[0] -= 1
	
	def __iter__( self ):
		return self
	
	def next( self ):
		if all( self.value == self.stop ):
			raise StopIteration
		
		for i in range(size( self.stop )):
			if self.value[i] == self.stop[i]:
				self.value[i] = 0
			else:
				self.value[i] += 1
				break
		
		return self.value
			