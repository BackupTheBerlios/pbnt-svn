from numarray import *
from numarray.ieeespecial import *
from utilities import *
from Graph import *
from Node import *
from BayesNet import *
from MoralGraph import *
from TriangleGraph import *
from InferenceEngine import *
from PriorityQueue import *
from JoinTree import *
from Sepset import *
import GraphUtilities

class JunctionTreeEngine( InferenceEngine ):
	#for reference please read, "Belief Networks: A Procedural Guide" by Cecil Huang and Adnan Darwiche (1994)

	def __init__ ( self, bnet ):
		InferenceEngine.__init__( self, bnet )
		
		#when solve CliqueNode issue use this line
		#self.bnet.nodes = [CliqueNode( node ) for node in self.bnet.nodes]
		
		#build a join tree and initialize it
		self.joinTree = self.BuildJoinTree()
		
		#if needed
		#self.joinTree.reInitialize( self.bnet.nodes )
	
	
	def maginal( self, query ):
		#ASSUMPTION: BuildJoinTree initializes potentials
		#do global propagation
		#for each message pass, maginalize over a X which means to find the instantiations
		#of X that are consitent with R and sum them
		#absorption identify the values of Y that are consisten with X (through sepset R)
		#and multiply each element and set Y to be that result (for pass from X to Y)
		if not self.joinTree.initialized:
			self.joinTree.reInitialize( self.bnet.nodes )
		self.globalPropagation()
		
		#assuming no evidence
		distributions = []
		for node in query:
			Q = DiscreteDistribution( zeros([node.nodeSize], type=Float), node.nodeSize )
			for value in range( node.nodeSize ):
				#axis arg not needed, but nice for clarity
				Q.setValue( value, node.clique.CPT.getValue( [value], axes=[node.clique.nodes.index(node)] ).sum(), axes=0 )
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
		if not currentCluster.visited:
			currentCluster.visited = 1
			for (neighbor, sep) in zip(currentCluster.neighbors, currentCluster.sepsets):
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
		oldSepsetPotential = sepset.potential.CPT.copy()
		self.project( fromCluster, sepset ) 
		#absorption
		self.absorb( toCluster, sepset, oldSepsetPotential )
	
	def project( self, cluster, sepset ):
		mu = sepset.mu
		clusterAxes = sepset.cliqueAxes( cluster )
		sepsetAxis = sepset.axis
		for index in mu:
			#get the relevant entries out of the cluster potential
			values = cluster.CPT.getValue( index, clusterAxes )
			sepset.potential.setValue( index, values.sum(), axes=sepsetAxis )
				
	def absorb( self, cluster, sepset, oldPotential ):
		mu = sepset.mu
		sepsetAxis = sepset.axis
		clusterAxes = sepset.cliqueAxes( cluster )
		potential = sepset.potential.CPT / oldPotential
		#multiply and set potential, assumes that there is only one axis of difference between
		#sepset and cluster
		for index in mu:
			sepsetValue = potential.getValue( index, sepsetAxis )
			clusterValues = cluster.CPT.getValue( index, clusterAxes )
			newValues = clusterValues * sepsetValue
			cluster.CPT.setMultipleValues( index, clusterAxes, newValues )
			

	def BuildJoinTree ( self ):
		#create the moral graph
		moralGraph = MoralGraph( self.bnet )
		#triangulate the graph
		triangulatedGraph = TriangleGraph( moralGraph )
		
		#build the join tree from the cliques in triangulatedGraph
		cliques = triangulatedGraph.cliques
		forest = []
		sepsetHeap = PriorityQueue()
		for i in range(len( cliques )):
			forest.append(JoinTree( cliques[i] ))
			for clique in cliques[i:]:
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
	
		
			
					
		