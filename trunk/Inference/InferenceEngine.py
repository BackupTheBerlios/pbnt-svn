from numarray import *

class InferenceEngine:
	
	def __init__(self, bnet):
		self.bnet = bnet
		self.evidence = zeros(bnet.numNodes) + -1

	def add_evidence ( self, varIndex, values ):
		self.evidence[varIndex] = values
	
	def marginal(self):
		self.action()

	 #all child classes must implement marginal_nodes()
