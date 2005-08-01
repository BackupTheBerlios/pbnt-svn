from numarray import *


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
				
				
def generateArrayIndex( dimsToIter, axesToIter, constValues, constAxes ):
	if len( axesToIter ) == 0:
		return constValues
	totalNumAxes = len( axesToIter ) + len( constAxes )
	indexList = [array([]) for dim in range( totalNumAxes )]
	
	indexList = generateArrayIndexHelper( 0, array(dimsToIter), array(axesToIter), indexList )
	
	nIndices = product(array( dimsToIter ))
	for (val, axis) in zip( constValues, constAxes ):
		indexList[axis] = ones([nIndices]) * val
	
	return array(indexList)

def generateArrayIndexHelper( val, dims, axes, indexList ):
	#if we have iterated through all of the dimensions
	if len( dims ) == 0:
		return indexList
	
	#if we have iterated through all of the values
	if val == dims[0]:
		return indexList
	
	indexList[axes[0]] = concatenate( (indexList[axes[0]], ones([product(dims[1:])]) * val) )
	indexList = generateArrayIndexHelper( 0, dims[1:], axes[1:], indexList )
	return generateArrayIndexHelper( val+1, dims, axes, indexList )
	
	
def convertIndex( baseIndex, weights ):
	nAxes = len( baseIndex )
	nIndex = len( baseIndex[0] )
	return sum(baseIndex * reshape(repeat( weights, nIndex ), (nAxes, nIndex)), axis=0)
	

def generateSetArrayCommand( indices, axes, nDims ):
	tmp = zeros([nDims]) + -1
	tmp[axes] = indices
	tmp = str( tmp ).replace( '-1', ':' )
	indexStr = "["
	for ch in tmp[1:-1]:
		if not ch == " ":
			indexStr += ch
			indexStr += ","
	#we don't want the last comma, and we need to add a ]
	indexStr = indexStr[:-1] + "]"
	return indexStr
		
	

	
