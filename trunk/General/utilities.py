from numarray import *


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
		


