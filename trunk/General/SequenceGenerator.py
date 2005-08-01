from numarray import *

class SequenceGenerator:
	
	def __init__( self, iterObjs ):
		self.stop = array(iterObjs) - 1
		#assuming here that the start of each dimension is zero
		self.value = zeros(size( iterObjs ))
		if len( self.value ) > 0:
			self.value[0] -= 1
		self.start = self.value.copy()
	
	def __iter__( self ):
		return self
	
	def next( self ):
		if alltrue( self.value == self.stop ):
			self.value = self.start.copy()
			raise StopIteration
		
		for i in range(size( self.stop )):
			if self.value[i] == self.stop[i]:
				self.value[i] = 0
			else:
				self.value[i] += 1
				break
		
		return self.value
			