from numarray import *
import numarray.objects as obj
import utilities as util
from InferenceEngine import *
import numarray.random_array as ra
from DiscreteDistribution import *

class MCMCEngine( InferenceEngine ):
	#implemented as described in Russell and Norvig
	#X is a list of variables
	#N is thenumber of samples
	def marginal ( self, X, N ):
		flipped = 0
		Nx = [DiscreteDistribution(zeros(x.nodeSize, type=Float32), x.nodeSize) for x in X]
		queryIndex = array([x.index for x in X])
		state = self.evidence.copy()
		nonEvMask = state == -1
		nonEv = obj.array(self.bnet.nodes)[nonEvMask]
		randMax = array([node.nodeSize for node in nonEv])
		#ASSUMPTION: zero is the minimum value
		randMin = zeros([len( nonEv )])
		#initialize nonEvidence variables to random values
		state[nonEvMask] = ra.randint( randMin, randMax )
		#FOR DEBUGGING ONLY
		valuesList = []

		for i in range( N ):
			valuesList += [state[3]]
			#record the value of all of the query variables
			if i > 100:
				for (q, dist) in zip(queryIndex, Nx):
					dist.CPT[state[q]] += 1
			for node in nonEv:
				val = self.sampleValueGivenMB(node, state)
				#change the state to reflect new value of given variable
				if not state[node.index] == val:
					state[node.index] = val
					flipped += 1

		for i in range(len( Nx )):
			Nx[i].normalise()
		
		return Nx


	def sampleValueGivenMB( self, node, state ):
		#init to be the prob dist of node given parents
		parents = node.parents
		parentsI = array([p.index for p in parents])
		#ASSUMPTION: node is arranged by parents
		MBval = node.CPT.getValue( state[parentsI], axes=range( node.CPT.nDims - 1 ) )
		children = node.children
		#want to save state
		oldVal = state[node.index]
		#OPTIMIZE: could vectorize this code
		for value in range(node.nodeSize):
			state[node.index] = value
			for child in children:
				childPsI = [p.index for p in child.parents]
				parentVals = state[childPsI]
				childVal = state[child.index]
				indices = concatenate((parentVals, childVal))
				MBval[value] *= child.CPT.getValue(indices)
		
		state[node.index] = oldVal
		#FIX THIS: better representation of distributions
		#normalize MBval
		MBval /= MBval.sum()
		
		val = util.sample(MBval)
		return val
	


