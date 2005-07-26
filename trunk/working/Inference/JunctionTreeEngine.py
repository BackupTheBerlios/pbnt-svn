from numarray import *
from numarray.ieeespecial import *

class JunctionTreeEngine(InferenceEngine):

	def __init__ (self,bnet):
		InferenceEngine(self, bnet)
		joinTree = BuildJoinTree()
	
	def BuildJoinTree ( self ):
		#create the moral graph
		Gm = moralGraph()
		Gtri = triangulateMoralGraph( Gm )
			
					
		
	def moralGraph( self ):
		#connect all of the parents to eachother
		Gm = self.bnet.graph.copy()
		for child in range( self.bnet.numNodes ):				
			connectParents( Gm, node)
		
		#make graph undirected (basically double connect all nodes)
		Gm += transpose(Gm)
		return Gm
	
	def connectParents( self, moral, node ):
		parents = self.bnet.parents( node )
		#we don't want to connect the last parent to itself so sub 1
		for parentIndex in (range(size(parents)) - 1):
			moral[parentIndex, parents[parentIndex+1:]] = 1			
	
	def triangulateMoralGraph( self, Gm ):
		Gtri = Gm.copy()
		#triangulate the graph, basically make all nodes part of a triangle within
		#the graph.  We do it blind here, but there are many heuristics for this which
		#greatly increase speed and efficiency of jtree inference
		nodes = range( self.bnet.numNodes )
		while len(nodes) > 2:
			minCluster = Cluster( array([-1,-1,-1]), inf, array([]), inf )
			#we could optimize this more by saving the clusters of each node, and only
			#recomputing clusters that are the neighbor of a newly removed node
			for node in nodes:
				minCluster = zeroEdgeCluster( Gm, node, minCluster )
			
			if minCluster.numberOfEdges > 0:
				for node in nodes:
					minCluster = oneEdgeCluster( Gm, node, minCluster )
				
			if minCluster.numberOfEdges > 1:
				for node in nodes:
					minCluster = twoEdgeCluster( Gm, node, nodes, minCluster )
			
			if minCluster.numberOfEdges > 2:
				for node in nodes:
					minCluster = threeEdgeCluster( Gm, node, nodes, minCluster )
			
			if minCluster.numberOfEdges > 3:
				#throw error
			
			for edge in minCluster.edges:
				#doubly connect so that works for our undirected rep
				Gm[edge[0],edge[1]] = 1
				Gm[edge[1],edge[0]] = 1
				#add same edges to Gtri
				Gtri[edge[0],edge[1]] = 1
				Gtri[edge[1],edge[0]] = 1
				
				#remove the node from our list
				nodes.remove( minCluster.node() )
				#also remove the node from Gm
				Gm[node,:] = 0
				Gm[:,node] = 0
			
		#connect final two nodes, only do it in Gtri, cause we are throwing away Gm
		Gtri[nodes[0],nodes[1]] = 1
		Gtri[nodes[1],nodes[0]] = 1
		return Gtri
			
	def zeroEdgeCluster( self, moral, node, minCluster ):
		neighbors = where(moral[node,] == 1)[0]
		for neighbor in neighbors:
			#give me the neighbors of this neighbor
			neighborsOfNeighbor = where(moral[neighbor,] == 1)[0]
			#find out if any of the neighbors are the same as the neighbors of this neighbor
			connectedNodes = neighbors[neighbors == neighborsOfNeighbor]
			#first check: connected, don't have to add any edges
			if size(connectedNodes) > 0:
				weight = computeClusterWeights([node, neighbor, connectedNodes[0]])
				cluster = Cluster(array([node, neighbor, connectedNodes[0]]), 0, array([]), weight)
				if cluster < minCluster:
					minCluster = cluster
		return minCluster
	
	def oneEdgeCluster( self, moral, node, minCluster ):
		neighbors = where( moral[node,:] == 1 )[0]
		for neighbor in neighbors:
			#Second check: add one edge
			#iterate through the other neighbors if there are any (basically we want to know if this node is in 
			#structure similar to the following neighbor ---- node ---- otherNeighbor, then we can just connect
			#neighbor to otherNeighbor
			for otherNeighbor in concatenate((neighbors[where(neighbors==neighbor)[0][0]+1:,], neighborsOfNeighbor[neighborsOfNeighbor != node])):
				weight = computeClusterWeights([node, neighbor, otherNeighbor])
				if moral[node,otherNeighbor] == 1:
					cluster = Cluster(array([node, neighbor, otherNeighbor]), 1, array([neighbor, otherNeighbor]), weight)
				else:
					cluster = Cluster(array([node, neighbor, otherNeighbor]), 1, array([node, otherNeighbor]), weight)
				if cluster < minCluster:
					minCluster = cluster
		return minCluster
				
	
	def twoEdgeCluster( self, moral, node, nodes, minCluster ):
		neighbors = where( moral[node,:] == 1 )[0]
		for neighbor in neighbors:
			for nodeLocal in nodes:
				if not node == nodeLocal:
					weight = computeClusterWeights([node, neighbor, nodeLocal])
					cluster = Cluster( array([node, neighbor, nodeLocal]), 2, [array([node, nodeLocal]), array([neighbor, nodeLocal])], weight)
					if cluster < minCluster:
						minCluster = cluster
		return minCluster
	
	def threeEdgeCluster( self, moral, node, nodes, minCluster ):
		for nodeLocal in nodes:
			if not node == nodeLocal:
				for nodeL2 in nodes:
					if not node == nodeL2 and not nodeLocal == nodeL2:
						weight = computeCluterWeights([node, nodeLocal, nodeL2])
						cluster = Cluster( array([node, nodeLocal, nodeL2]), 3, [array([node, nodeLocal]), array([node, nodeL2]), array([nodeLocal, nodeL2])], weight)
						if cluster < minCluster:
							minCluster = cluster
		return minCluster
			 
	
	def computeClusterWeights( self, nodes ):
		return product( self.bnet.ns( nodes ) )					

class Cluster:
	
	#DO NOT VIOLATE ASSUMPTIONS BELOW
	def __init__( self, nodes, numberOfEdges, edges, weight ):
		self.nodes = nodes
		self.numberOfEdges = numberOfEdges
		self.edge = edge
		self.weight = weight
	
	def __lt__( self, other ):
		if self.numberOfEdges < other.numberOfEdges:
			return True
		elif self.numberOfEdges == other.numberOfEdges:
			if self.weight < other.weight:
				return True
			else:
				return False
		else:
			return False 
	
	#ASSUMES: "nodes" is created with array([node, neighbor, otherneighbor])
	def node( self ):
		return self.nodes[0]
			
