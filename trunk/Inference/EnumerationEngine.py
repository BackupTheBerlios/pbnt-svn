from numarray import *
from InferenceEngine import *
from DiscreteDistribution import *

class EnumerationEngine(InferenceEngine):

	def marginal ( self, queryVar ):
		ns = self.bnet.ns(queryVar)
		distributionTable = zeros([ns], type=Float)
		Q = DiscreteDistribution(distributionTable, ns)
		if not (self.evidence[queryVar] == -1):
			for val in range( ns ):
				Q.set( val , 0 )
			Q.set( self.evidence[queryVar], 1 )
		else: 
			for val in range( ns ):
				self.add_evidence(queryVar, val)
				Q.set(val, self.enumerateAll())
			self.add_evidence(queryVar, -1)
			Q.normalise()
		return Q

	def enumerateAll (self):
		nonEvidence = where(self.evidence == -1)[0]
		self.initialize(nonEvidence)
		Q = self.probabilityOf(self.evidence)
		while self.nextState(nonEvidence):
			Q += self.probabilityOf(self.evidence)

		self.evidence[nonEvidence] = -1
		return Q
	
	def initialize( self, nonEvidenceNodes ):
		self.evidence[nonEvidenceNodes] = 0
	
	def nextState( self, nonEvidenceNodes ):
		nodeSizes = []
		for node in nonEvidenceNodes:
			nodeSizes.append(self.bnet.ns( node ))
		numberOfNodes = size(nonEvidenceNodes)
		for (node, ns) in zip(nonEvidenceNodes, nodeSizes):
			if self.evidence[node] == (ns - 1):
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
		Q = 1
		for (i) in range(size(state)):
			vals = concatenate((state[self.bnet.parentIndices(i)], state[i]))
			Q *= self.bnet.CPTs(i).probabilityOf(vals)
		return Q
		
					
	

