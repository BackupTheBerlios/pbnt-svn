from InducedCluster import *

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
                