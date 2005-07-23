from numarray import *

class EnumerationEngine(InferenceEngine):

	def marginal ( self, queryVar ):
		distributionTable = zeros([self.bnet.ns(queryVar)], type=float)
		Q = DiscreteDistribution(distributionTable)
		for val in range( x.ns() ):
				self.add_evidence(self.bnet.indexOf(x), val)
				Q.set(val, self.enumerateAll())
		Q.normalise()
		return Q

	def enumerateAll (self):
		nonEvidence = where(self.evidence() == -1)
		self.initialize(nonEvidence)
		Q = self.probabilityOf(self.evidence)
		while self.nextState(nonEvidence):
			Q *= self.probabilityOf(self.evidence)

		self.evidence[nonEvidence] = -1
		return Q
	
	def initialize( self, nonEvidenceNodes ):
		self.evidence[nonEvidence] = 0
	
	def nextState( self, nonEvidenceNodes ):
		nodeSizes = self.bnet.ns()[nonEvidenceNodes]
		numberOfNodes = size(nonEvidenceNodes)
		for (node, ns) in zip(nonEvidenceNodes, nodeSizes):
			if self.evidence[node] == ns - 1:
				if node == nonEvidenceNodes[numberOfNodes - 1]:
					return False
				else:
					self.evidence[node] = 0
					continue
			else:
				self.evidence[node] += 1
				break
			
		return True
		
	def probabilityOf (self, state):
		for (i,val) in zip(range(size(state)), state):
			
		
					
	

