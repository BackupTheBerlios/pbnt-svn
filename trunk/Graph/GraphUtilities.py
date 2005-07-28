


def connectNodes( node1, node2 ):
	node1.addNeighbor( node2 )
	node2.addNeighbor( node1 )


def getTree( forest, clique ):
	for tree in forest:
		if clique in tree.nodes:
			return tree


