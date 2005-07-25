class JunctionTreeEngine(InferenceEngine):

	def __init__ (self,bnet):
		InferenceEngine(self, bnet)
		joinTree = BuildJoinTree(bnet)
	
	def BuildJoinTree ( self, bnet ):
		#make moral graph by making all of the parents children,
		#basically create an undirected graph
		Gm = bnet.graph.copy()
		Gm += transpose(Gm)
		
		
	
	def TriangulateGraph(moralG):
		TgP = copy(moralG)
		Tg = copy(moralG)
		vars = size(Tg,1)
	#compute the number of edges added 
	#by each node, and therefore build 
	#binary heap
		heap = OrganizeHeap(TgP)
		while (var = heap.next()):
			cluster = InduceCluster(TgP,TgP,var)
			
