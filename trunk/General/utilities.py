from numarray import *
import numarray.random_array as ra


# Miscellaneous utility functions for use with the rest of the BayesNet Package


#Checks if a and b are equal within a fraction of error.  
#The error is that normally introduced by the imprecision of Floating point numbers
#now outdated, use allclose
def myFloatEQ ( a , b ):
	
	bHigh = b + 0.000000000100000000
	bLow = b - 0.000000000010000000
	
	if a < bHigh and a > bLow:
		return True
	
	return False

#returns an array of unique elements given the elements in the input arrays, all arrays must be input as a tuple
#this is VERY UNOPTIMIZED, should be replaced later by a UFUNC in Numarray, but we will wait to do that
#arrays assumed to be 1D
def unique( arrayTuple ):
	master = concatenate( arrayTuple )
	uniqueElements = []
	for element in master:
		if not (element in uniqueElements):
			uniqueElements.append( element )
	return array( uniqueElements )


def addToPriorityQueue( queue, element ):
	if len( queue) == 0:
		queue.append( element )
		return queue
	
	for e in queue:
		if element > e:
			index = queue.index( e )
			queue = queue[0:index] + [element] + queue[index:]
			return queue
	
	queue.append( element )
	return queue

def intersect( L1, L2 ):
	return [e for e in L1 if e in L2]
		

def sample(arr):
	#given an array of probabilities return a randomly generated int with 
	#probability equal to the values of array
	nPossibleValues = len(arr)
	rnum = ra.random()
	probRange = arr[0]
	i = 0
	for prob in arr[1:]:
		if rnum < probRange:
			break
		else:
			probRange += prob
			i += 1
	
	return i

def updateCounts(nodes, counts, data):
	assert(isinstance(bnet, Graph))
	assert(isinstance(counts, ArrayType))
	assert(isinstance(data, ArrayType))
	for node in nodes:
		count = counts[node.index]
		indices = data[concatenate((node.parentIndex, array([node.index])))]
		fIndex = flatIndex(indices, count.shape)
		count.flat[fIndex] += 1

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
	


