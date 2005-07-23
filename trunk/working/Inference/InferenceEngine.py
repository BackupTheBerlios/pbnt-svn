import numeric 

class InferenceEngine:
	
	def __init__(self, bnet):
		self.bnet = bnet
		self.evidence = zeros(bnet.numberOfNodes()) + -1

	def add_evidence ( self, varIndex, values ):
		self.evidence[varIndex] = values

	def evidence(self):
		return self.evidence
	def bnet(self):
		return self.bnet
	
	def marginalize(self):
		self.action()

	 #all child classes must implement marginal_nodes()
