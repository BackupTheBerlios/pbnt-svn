from Graph import *
import GraphUtilities
from ClusterBinaryHeap import *
from Clique import *

class TriangleGraph( Graph ):
        
        def __init__( self, moral ):
                Graph.__init__( self, copy.deepcopy( moral.nodes ) )
                heap = ClusterBinaryHeap( )
                #copy the graph so that we can destroy the copy as we go
                for (node, i) in zip( moral.nodes, range(len( moral.nodes )) ):
                        node.index = i
                        #have to copy so that when we destory neighbor lists it wont affect the actual graph
                        heap.insert( node )
                
                inducedCliques = []
                for (node, edges) in heap:
                        for edge in edges:
                                #a little messy, but we want to reference the nodes in the actual graph, not the ones from the heap
                                #we destroyed the neighbor lists of the nodes in the heap
                                GraphUtilities.connectNodes( self.nodes[node.neighbors[edge[0]].index], self.nodes[node.neighbors[edge[1]].index] )
                        
                        clique = Clique( [node] + node.neighbors )
                        #use addCluster which only adds if it is not contained in a previously added cluster
                        GraphUtilities.addClique( inducedCliques, clique ) 
                        
                
                self.cliques = inducedCliques
        
                        