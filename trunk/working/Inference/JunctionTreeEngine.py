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
			
	def minCluster( self, moral, node ):
		minCluster = Cluster( array([-1,-1,-1]), -1, array([-1,-1]), -1 )
		neighbors = where(moral[node,] == 1)[0]
		for neighbor in neighbors:
			#first check if connected to another node that is a neighbor of node
			neighborsOfNeighbor = moral[neighbor,]
			onesNeighbors = where(neighbors == 1)[0]
			onesNofNs = where(neighborsOfNeighbor == 1)[0]
			connected = onesNeighbors[onesNeighbors == onesNofNs]
			if size(connected) > 0:
				weight = product( self.bnet.ns([node, neighbor, connected[0]]) )
				cluster = Cluster(array([node, neighbor, connected[0]]), 0, array([]), weight)
				if cluster < minCluster:
					minCluster = cluster
					
				
			
	
	def computeClusterWeights( self, nodes ):
		return product( self.bnet.ns( nodes ) )					

class Cluster:
	
	def __init__( self, nodes, numberOfEdges, edge, weight ):
		self.nodes = nodes
		self.numberOfEdges = numberOfEdges
		self.edge = edge
		self.weight = weight
	
	def __lt__( self, other ):
		if other.weight == -1:
			return True
		if self.weight == -1:
			return False
		if self.numberOfEdges < other.numberOfEdges:
			return True
		elif self.numberOfEdges == other.numberOfEdges:
			if self.weight < other.weight:
				return True
			else:
				return False
		else:
			return False 
			
			
