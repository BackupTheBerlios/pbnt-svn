


def connectNodes( node1, node2 ):
	node1.addNeighbor( node2 )
	node2.addNeighbor( node1 )


def getTree( forest, clique ):
	for tree in forest:
		if clique in tree.nodes:
			return tree


def addClique( cliqueList, clique ):
	add = 1
	for c in cliqueList:
		if c.contains( clique.nodes ):
			add = 0
			break
	
	if add:
		cliqueList.append( clique )

def unmarkAllNodes( graph ):
	for node in graph.nodes:
		node.visited = False


def missingEdges( node ):
	edges = []
	for (neighbor, i) in zip( node.neighbors, range(len( node.neighbors ) - 1) ):
		for (otherNeighbor, j) in zip( node.neighbors[i:], range(len( node.neighbors[i:] )) ):
			if not neighbor.isNeighbor( otherNeighbor ):
				edges.append( (i,j+i+1) )
	return edges
				
		

	
