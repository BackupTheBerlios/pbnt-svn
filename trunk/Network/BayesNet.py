from numarray import *

class BayesNet:
	
	#TODO: add optional arg node 
	#names.
	def __init__(self, adjMat, nodeSizes, CPT):
		#watch out cause next step wontwork if truly justby reference
		self.graph = adjMat
		self.nodeSizes = nodeSizes
		self.CPT = CPT
		self.numNodes = size(nodeSizes)
				
	def children (self, nI):
		return nonzero ( take ( self.graph, (nI,), 0))[1]

	def parents (self, nI):
		return nonzero (take ( self.graph, (nI,), 1))[0]
	
	def numberOfNodes(self):
		return self.numNodes
	
	def ns(self, varIndex):
		return self.nodeSizes[i]

		
