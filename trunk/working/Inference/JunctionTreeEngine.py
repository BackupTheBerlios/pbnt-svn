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
	
	def triangulateMoralGraph( self, Gm ):
		Gtri = Gm.copy()
		#triangulate the graph, basically make all nodes part of a triangle within
		#the graph.  We do it blind here, but there are many heuristics for this which
		#greatly increase speed and efficiency of jtree inference
		for i in (range( self.bnet.numNodes ) - 2):
			minCluster = Cluster( array([-1,-1,-1]),  -1 )
			for node in range( self.bnet.numNodes ):
				if any(Gm[node,]):
					cluster = minCluster( Gm, node )
					
			
					
			
	def connectParents( self, moral, node ):
		parents = self.bnet.parents( node )
		#we don't want to connect the last parent to itself so sub 1
		for parentIndex in (range(size(parents)) - 1):
			moral[parentIndex, parents[parentIndex+1:]] = 1			
			
	#move the visitor pattern up one level, so instead of looking for min cluster for this node, get all zero clusters
	#for all nodes, then all ones then all twos etc.
	def minCluster( self, moral, node ):
		minCluster = Cluster( array([-1,-1,-1]), inf, array([]), inf )
		minCluster = zeroEdgeCluster( moral, node, minCluster )

		if minCluster.numberOfEdges > 0:
			minCluster = oneEdgeCluster( moral, node, minCluster)
		
		if minCluster.numberOfEdges > 1:
			minCluster = twoEdgeCluster( moral, node, minCluster )
		
		if minCluster.numberOfEdges > 2:
			minCluster = threeEdgeCluster( moral, node, minCluster )
		
		if minCluster.numberOfEdges > 3:
			#throw an exception
		else:
			return minCluster
			
					
				
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
				
	
	def twoEdgeCluster( self, moral, node, minCluster ):
		#add code here
	
	def threeEdgeCluster( self, moral, node, minCluster ):
		#add code here
	
	def computeClusterWeights( self, nodes ):
		return product( self.bnet.ns( nodes ) )					

class Cluster:
	
	def __init__( self, nodes, numberOfEdges, edge, weight ):
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
			
			
