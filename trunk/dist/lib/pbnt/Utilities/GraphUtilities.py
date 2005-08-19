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
            if not otherNeighbor in neighbor.neighborSet:
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


class InducedCluster:
    
    def __init__( self, node ):
        self.node = node
        self.edges = missingEdges( self.node )
        self.nEdges = len( self.edges )
        self.weight = self.computeWeight()
    
    
    def __lt__( self, other ):
        #less than means that it is better (pick it first)
        if self.nEdges < other.nEdges:
            return True
        if self.nEdges == other.nEdges and self.weight < other.weight:
            return True
        
        return False
    
    def recompute( self ):
        self.edges = missingEdges( self.node )
        self.nEdges = len( self.edges )
        self.weight = self.computeWeight()
    
    def computeWeight( self ):
        return product(array( [node.size() for node in self.node.neighbors] + [self.node.size()] ))
    
    
class ClusterBinaryHeap:
        
        def __init__( self ):
                self.heap = []
        
        def insert( self, node ):
                iCluster = InducedCluster( node )
                self.heap.append( iCluster )
                self.heap.sort()
        
        def __iter__( self ):
                return self
        
        def next( self ):
                if len( self.heap ) == 0:
                        raise StopIteration
                
                cluster = self.heap[0]
                
                del self.heap[0]
                
                #find the affected nodes
                tmpClusterList = []
                for node in cluster.node.neighbors:
                        for c in self.heap:
                                if c.node == node:
                                        c.node.neighbors.remove( cluster.node )
                                        tmpClusterList.append( c )
                                        break
                
                #recompute cluster score of effected clusters
                for c in tmpClusterList:
                        c.recompute()
                
                #reorder now that edges have changed
                self.heap.sort()
        
                return (cluster.node, cluster.edges)
                
        
        def hasNext( self ):
                return not len( heap ) == 0
                