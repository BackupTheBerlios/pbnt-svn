from numarray import *
from numarray.ieeespecial import *
from utilities import *
from Graph import *
from Node import *
from BayesNet import *
from MoralGraph import *

class JunctionTreeEngine( InferenceEngine ):
	#for reference please read, "Belief Networks: A Procedural Guide" by Cecil Huang and Adnan Darwiche (1994)

	def __init__ ( self, bnet ):
		InferenceEngine.__init__( self, bnet )
		joinTree = BuildJoinTree()
		inconsistentJoinTree = initializeJointTree()
	
	
	def maginal( self, query ):
		#ASSUMPTION: BuildJoinTree initializes potentials
		#do global propagation
		#for each message pass, maginalize over a X which means to find the instantiations
		#of X that are consitent with R and sum them
		#absorption identify the values of Y that are consisten with X (through sepset R)
		#and multiply each element and set Y to be that result (for pass from X to Y)
		consistentJoinTree = globalPropagation( incosistentJoinTree )
		
		#assuming no evidence
		distributions = []
		for node in query:
			Q = DiscreteDistribution( node.nodeSize )
			for value in node.nodeSize:
				Q.set( value, sumOverConsistentValues( node, value ) )
			distributions.append( Q )
		
		return distributions
		
		
	def globalPropagation( self, inconsistentJointTree ):
		#arbitrarily pick a cluster
		startCluster = inconsistentJointTree.clusters[0]
		
		unmarkAllClusters()
		#we use 0 to denote that there was no prevCluster and therefore no potential or mu
		collectEvidence( 0, startCluster, True, 0 )
		unmarkAllClusters()
		distributeEvidence( startCluster )
	
	def collectEvidence( self, prevCluster, currentCluster, isStart, sepset ):
		if not currentCluster.visited:
			currentCluster.visited = 1
			for (neighbor, sep) in zip(currentCluster.neighbors, currentCluster.sepsets):
				collectEvidence( currentCluster, toCluster, neighbor, 0, sep )
			
			if not isStart:
				passMessage( toCluster, fromCluster, sepset )
	
	def distributeEvidence( self, cluster ):
		cluster.visited = 1
		for neighbor in cluster.neighbors:
			passMessage( cluster, neighbor )
			if not neighbor.visited:
				distributeEvidence( neighbor )
	
	def passMessage( self, fromCluster, toCluster, sepset ):
		#projection
		oldSepsetPotential = sepset.CPT.copy()
		project( fromCluster, sepset ) 
		#absorption
		absorb( toCluster, sepset, oldSepsetPotential )
	
	def project( self, cluster, sepset ):
		mu = sepset.mu
		clusterAxes = sepset.cliqueAxes( cluster )
		sepsetAxis = sepset.axis
		for index in mu:
			#get the relevant entries out of the cluster potential
			values = cluster.CPT.getValue( index, clusterAxes )
			sepset.CPT.setValue( index, sepsetAxis, sum( values ) )
				
	def absorb( self, cluster, sepset, oldPotential ):
		mu = cluster.mu( sepset )
		potential = sepset.CPT / oldPotential
		#multiply and set potential, assumes that there is only one axis of difference between
		#sepset and cluster
		for (index, sepsetAxis, clusterAxis) in mu:
			sepsetValue = potential.getValue( index, sepsetAxis )
			clusterValues = cluster.CPT.getValue( index, clusterAxis )
			newValues = clusterValues * sepsetValue
			cluster.CPT.setMultipleValues( index, clusterAxis, newValues )
	
			
		
	

		
	
	
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
				joinTreeX = getTree( forest, sepset.cliqueX )
				joinTreeY = getTree( forest, sepset.cliqueY )
				if joinTreeX != joinTreeY:
					joinTreeX.merge( sepset, joinTreeY )
					joinTrees.remove( joinTreeY )
					break
			
		for tree in forest:
			tree.initCliquePotentials( self.bnet.nodes )
		
		#find out if we are dealing with a forest, if so return as list, otherwise return as individual tree
		if len( forest ) > 1:
			return forest
		else:
			return forest[0]	
			
					
		
