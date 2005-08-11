from numarray import *
import numarray.ieeespecial as ieee
import GraphUtilities
from utilities import *
from Graph import *
from Node import *
from BayesNet import *
from InferenceEngine import *
from PriorityQueue import *
from JoinTree import *
from Sepset import *


class InferenceEngine:
	
	def __init__(self, bnet):
		self.bnet = bnet
		self.evidence = zeros(bnet.numNodes) + -1

	def add_evidence ( self, varIndex, values ):
		self.evidence[varIndex] = values
	
	def marginal(self):
		#all child classes must implement marginal()
		self.action()

	 

class EnumerationEngine(InferenceEngine):

	def marginal ( self, queryVar ):
		ns = self.bnet.ns(queryVar)
		distributionTable = zeros([ns], type=Float32)
		Q = DiscreteDistribution(distributionTable, ns)
		if not (self.evidence[queryVar] == -1):
			for val in range( ns ):
				Q.setValue( val , 0 )
			Q.setValue( self.evidence[queryVar], 1 )
		else: 
			for val in range( ns ):
				self.add_evidence(queryVar, val)
				Q.setValue(val, self.enumerateAll())
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
			Q *= self.bnet.CPTs(i).getValue(vals)
		return Q


class JunctionTreeEngine( InferenceEngine ):
	#for reference please read, "Belief Networks: A Procedural Guide" by Cecil Huang and Adnan Darwiche (1994)

	def __init__ (self, bnet):
		InferenceEngine.__init__(self, bnet)
		#create the moral graph
		moralGraph = MoralGraph( self.bnet )
		#triangulate the graph
		triangulatedGraph = TriangleGraph( moralGraph )
		#build a join tree and initialize it
		self.joinTree = self.BuildJoinTree(triangulatedGraph)
	
	def marginal(self, query):
		#ASSUMPTION: BuildJoinTree initializes potentials
		#do global propagation
		#for each message pass, maginalize over a X which means to find the instantiations
		#of X that are consitent with R and sum them
		#absorption identify the values of Y that are consisten with X (through sepset R)
		#and multiply each element and set Y to be that result (for pass from X to Y)
		if not self.joinTree.initialized:
			self.joinTree.reInitialize( self.bnet.nodes )
		
		self.joinTree.enterEvidence( self.evidence, self.bnet.nodes )
		self.globalPropagation()
		
		#assuming no evidence
		distributions = []
		for node in query:
			Q = DiscreteDistribution( zeros([node.nodeSize], type=Float32), node.nodeSize )
			for value in range( node.nodeSize ):
				#axis arg not needed, but nice for clarity
				Q.setValue( value, node.clique.CPT.getValue( [value], axes=[node.clique.nodes.index(node)] ).sum(), axes=[0] )
			Q.normalise()
			distributions.append( Q )
		
		return distributions
		
		
	def globalPropagation( self ):
		self.joinTree.initialized = False
		#arbitrarily pick a cluster
		startCluster = self.joinTree.nodes[0]
		
		GraphUtilities.unmarkAllNodes( self.joinTree )
		#we use 0 to denote that there was no prevCluster and therefore no potential or mu
		self.collectEvidence( 0, startCluster, 0, True )
		GraphUtilities.unmarkAllNodes( self.joinTree )
		self.distributeEvidence( startCluster )
	
	def collectEvidence( self, prevCluster, currentCluster, sepset, isStart ):
		currentCluster.visited = 1
		for (neighbor, sep) in zip(currentCluster.neighbors, currentCluster.sepsets):
			if not neighbor.visited:
				self.collectEvidence( currentCluster, neighbor, sep, 0 )
			
		if not isStart:
			self.passMessage( currentCluster, prevCluster, sepset )
	
	def distributeEvidence( self, cluster ):
		cluster.visited = 1
		for (neighbor, sep) in zip( cluster.neighbors, cluster.sepsets ):
			if not neighbor.visited:
				self.passMessage( cluster, neighbor, sep )
				self.distributeEvidence( neighbor )
	
	def passMessage( self, fromCluster, toCluster, sepset ):
		#projection
		oldSepsetPotential = self.project( fromCluster, sepset ) 
		#absorption
		self.absorb( toCluster, sepset, oldSepsetPotential )
	
	def project( self, cluster, sepset ):
		oldSepsetPotential = copy.deepcopy( sepset.potential )
		#not using mu anymore but not ready to delete yet
		mu = sepset.mu
		clusterAxes = sepset.cliqueAxes( cluster )
		sepsetAxis = sepset.axis
		for index in mu:
			#get the relevant entries out of the cluster potential
			values = array([cluster.CPT.getValue( index, clusterAxes )])
			sepset.potential.setValue( index, values.sum(), axes=sepsetAxis )
		return oldSepsetPotential
				
	def absorb( self, cluster, sepset, oldPotential ):
		mu = sepset.mu
		sepsetAxis = sepset.axis
		clusterAxes = sepset.cliqueAxes( cluster )
		zeroMask = oldPotential.CPT == 0
		oldPotential.CPT = sepset.potential.CPT / oldPotential.CPT
		oldPotential.CPT[zeroMask] = 0 
		#saxesToIter = [axis for axis in range(cluster.CPT.nDims) if not axis in clusterAxes]
		#multiply and set potential, assumes that there is only one axis of difference between
		#sepset and cluster
		for index in mu:
			sepsetValue = oldPotential.getValue( index, sepsetAxis )
			clusterValues = cluster.CPT.getValue( index, clusterAxes )
			newValues = clusterValues * sepsetValue
			cluster.CPT.setValue( index, newValues, clusterAxes )
			#if len( axesToIter ) > 0:
				#dimsToIter = array(cluster.CPT.dims)[axesToIter]
				#indices = generateArrayIndex( dimsToIter, axesToIter, index, clusterAxes )
				##flatindices = convertIndex( indices )
				#cluster.CPT.setValue( indices, newValues, clusterAxes )
			#else:
				##flatindex = sum( index * array([cluster.indexWeights[cA] for cA in clusterAxes]) )
				#cluster.CPT.setValue( index, newValues, clusterAxes )
			
	

	def BuildJoinTree (self, triangulatedGraph):
		
		#build the join tree from the cliques in triangulatedGraph
		cliques = triangulatedGraph.cliques
		forest = [JoinTree( clique ) for clique in cliques]
		sepsetHeap = PriorityQueue()
		for i in range(len( cliques ) - 1):
			for clique in cliques[i+1:]:
				sepset = Sepset( cliques[i], clique )
				sepsetHeap.insert( sepset )
		
		for n in range(len( forest ) - 1):
			#insert sepsets into JoinTree
			while sepsetHeap.hasNext():
				sepset = sepsetHeap.next()
				joinTreeX = GraphUtilities.getTree( forest, sepset.cliqueX )
				joinTreeY = GraphUtilities.getTree( forest, sepset.cliqueY )
				if joinTreeX != joinTreeY:
					joinTreeX.merge( sepset, joinTreeY )
					forest.remove( joinTreeY )
					break
			
		for tree in forest:
			tree.initCliquePotentials( self.bnet.nodes )
		
		#find out if we are dealing with a forest, if so return as list, otherwise return as individual tree
		if len( forest ) > 1:
			return forest
		else:
			return forest[0]
	


class JunctionTreeDBNEngine(JunctionTreeEngine):
        #this is named DBN, but really it only works for HMMs for now.
        
        def __init__(self, DBN):
                InferenceEngine.__init__(DBN)
                moral = MoralDBNGraph(DBN)
                #triangulate the graph
		triangulatedGraph = TriangleGraph( moralGraph )
		#build a join tree and initialize it
		self.joinTree = self.BuildJoinTree(triangulatedGraph)
		
