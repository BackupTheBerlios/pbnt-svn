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
	
	def set (self, value, probability):
		put(self.CPT, value, probability, range(value.size()))
	
	def normalise(self):
		self.CPT[where(self.CPT == 0)] = 1
		c = sum(reshape(self.CPT,(size(self.CPT),)))
		self.CPT = self.CPT/c
	
	def ns(self):
		return self.ns
	
	def probabilityOf (varAndParentValsArray):
		return take(self.CPT, varAndParentValsArray, axis=range(size(varAndParentValsArray)))
		
	
		    