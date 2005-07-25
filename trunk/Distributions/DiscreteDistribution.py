from numarray import *

class DiscreteDistribution:
#to do listforthis class
#add different constructors
#1.give fullCPT
#2 give it for specific parents but
# randomfor others

	def __init__(self, CPT, ns):
		self.CPT = CPT
		self.ns = ns		 
	
	def set (self, indices, value):
		#there seems to be a bug in numarray.  If arg axis is more than 1 element,
		#then it can be a list / array, but if it is singular it has to be a single
		#number.
		nDim = size(shape(self.CPT))
		if nDim > 1:
			put(self.CPT, indices, value, range(nDim))
		else:
			put(self.CPT, indices, value)
	
	def normalise(self):
		self.CPT[where(self.CPT == 0)] = 1
		c = sum(reshape(self.CPT,(size(self.CPT),)))
		self.CPT = self.CPT/c
	
	def ns(self):
		return self.ns
	
	def probabilityOf (self, varAndParentValsArray):
		return take(self.CPT, varAndParentValsArray, axis=range(size(varAndParentValsArray)))
		
	
		    