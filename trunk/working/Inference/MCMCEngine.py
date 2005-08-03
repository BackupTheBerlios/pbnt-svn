from numarray import *

class MCMCEngine( InferenceEngine ):
	#implemented as described in Russell and Norvig
	#X is a list of variables
	#N is thenumber of samples
	def marginal ( self, X, N ):
		Nx = [zeros( x.ns ) for x in X]
		queryIndex = array([x.index for x in X])
		state = self.evidence()
		nonEvMask = state == -1
		nonEv = self.bnet.nodes[nonEvMask]
		randMax = array([node.ns for node in nonEv])
		#ASSUMPTION: zero is the minimum value
		randMin = zeros([len( nonEv )])
		#initialize nonEvidence variables to random values
		state[nonEvMask] = randint( randMin, randMax )

		for i in range( N ):
			#record the value of all of the query variables
			Nx += state[queryIndex]
			for node in nonEv:
				val = sampleValueGivenMB(node, state)
				#change the state to reflect new value of given variable
				state[node.index] = val		

		for i in range(len( Nx )):
			Nx[i].normalise()
		
		return Nx


	def sampleValueGivenMB( self, node, state ):
		#init to be the prob dist of node given parents
		parents = node.parents
		parentsI = [p.index for p in parents]
		#ASSUMPTION: node is arranged by parents
		MBval = node.CPT.getValue( parentsI, axes=range( node.CPT.nDims - 1 ) )
		children = node.children
		for varI in selfChildren:
			MBval *= self.bnet().vars()[varI].prob(take(state, self.bnet().parents(varI)))
			
		return MBval


