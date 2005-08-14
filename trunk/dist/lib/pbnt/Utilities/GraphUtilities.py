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

def unmark_all_nodes( graph ):
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
    

def generateArrayStrIndex( indices, axes, nDims ):
    indices = array(indices)
    axes = array(axes)
    tmp = zeros([nDims]) + -1
    if len(axes) > 0:
        tmp[axes] = indices
    #tmp = str( tmp ).replace( '-1', ':' )
    indexStr = "["
    for i in range(len(tmp) - 1):
        if tmp[i] == -1:
            indexStr += ':,'
        else:
            indexStr += str(tmp[i])
            indexStr += ','
    #now handle the last element
    if tmp[-1] == -1:
        indexStr += ':]'
    else:
        indexStr += str(tmp[-1])
        indexStr += ']'
    return indexStr

def flatIndex(indices, shape):
    assert(isinstance(indices, ArrayType))
    assert(isinstance(shape, types.TupleType))	
    flat = 0
    for i in range(len(indices)):
        flat += indices[i] * product(shape[i+1:])
    
    return flat


