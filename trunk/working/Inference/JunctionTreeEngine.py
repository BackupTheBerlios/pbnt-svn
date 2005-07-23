class JunctionTreeEngine(InferenceEngine):

	def __init__ (self,bnet):
		moralGraph = ConstructMoralGraph(bnet)
		triGraph = 
		joinTree = BuildJoinTree(triGraph)

		self.bnet = bnet
		self.evidence = array()
		self.moralGraph = ConstructMoralGraph(self.bnet)
		self.triGraph = Triangulate(self.moralGraph)
		self.joinTree = BuildJoinTree(self.triGraph)
					      

	def ConstructMoralGraph(bnet):
		Gm = copy(bnet.table())
		#make undirected
		for i in range(shape(Gu))[0]:
			connections =  find(Gu[i,:]==1)
			for j in connections:
				take(Gu,j,i) = 0
		#connect parents
		for i in range(shape(Gu)[0]:
			parents = bnet.parents(i)
			for k in [0:parents.length()-1]:
				for l in [k+1:parents.length()-1]:
					take(Gu,parents[k],parents[l]) = 1
	
		return Gu
	
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
			
